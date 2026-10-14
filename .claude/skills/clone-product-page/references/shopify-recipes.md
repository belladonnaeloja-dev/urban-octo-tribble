# Shopify recipes for clone-product-page

Exact queries and mutations for each phase, in run order. Every code block here
was validated against the Admin API schema with `validate_graphql_codeblocks`
when it was written; if Shopify moves a field, re-validate rather than guessing.
Run reads with `graphql_query` and writes with `graphql_mutation`.

Contents:

1. Confirm which store you're on
2. Phase 1 — product harvest
3. Phase 1 — read the template file (and the UTF-8 spill-file gotcha)
4. Phase 1 — resolve `shop_images` references to CDN URLs
5. Phase 2 — read the destination's brand styling
6. Phase 3 — confirm the page-builder sections exist
7. Phase 4 — `fileCreate` for section images
8. Phase 5 — `productCreate` with ordered media, then prices
9. Phase 6 — duplicate the theme, staged upload, `themeFilesUpsert`, verify
10. Phase 7 — publish and activate
11. Template naming convention
12. Gotchas collected from real runs

---

## 1. Confirm which store you're on

`get-shop-info` is the quick check (name, domain, currency). For the locale as
well:

```graphql
query WhichStore {
  shop { name myshopifyDomain primaryDomain { host } currencyCode }
  shopLocales { locale primary published }
}
```

Do this before the harvest (source) and again immediately after `switch-shop`
(destination), before any write.

## 2. Phase 1 — product harvest

Find the GID with `search_products` (handle or title), or directly:

```graphql
query ProductByHandle($handle: String!) {
  productByIdentifier(identifier: { handle: $handle }) { id title handle }
}
```

Then the full record. `media` comes back in gallery order; keep that order.

```graphql
query HarvestProduct($id: ID!) {
  product(id: $id) {
    id title handle status vendor productType tags templateSuffix
    descriptionHtml
    seo { title description }
    options { name position values }
    variants(first: 100) {
      nodes {
        id title sku price compareAtPrice inventoryPolicy taxable
        selectedOptions { name value }
        inventoryItem { tracked requiresShipping }
        media(first: 1) { nodes { id ... on MediaImage { image { url } } } }
      }
    }
    media(first: 100) {
      nodes {
        id alt mediaContentType
        ... on MediaImage { image { url width height } }
        ... on Video { sources { url mimeType } }
      }
    }
  }
}
```

Save the JSON response to your scratch directory as `product.json`. Media
`image.url` values are full CDN URLs and stay valid after `switch-shop` (they're
public), which is what makes the two-phase clone possible.

Variant images: if a variant's `media` names a specific gallery image, note the
mapping (variant title → image filename) in the manifest; after `productCreate`
you'll need to re-associate them via `productVariantsBulkUpdate` with
`mediaId`.

## 3. Phase 1 — read the template file

Get the MAIN theme id, then the template body:

```graphql
query MainTheme {
  themes(first: 1, roles: [MAIN]) { nodes { id name role } }
}
```

```graphql
query TemplateBody($themeId: ID!, $filenames: [String!]!) {
  theme(id: $themeId) {
    files(first: 1, filenames: $filenames) {
      nodes {
        filename size checksumMd5
        body { ... on OnlineStoreThemeFileBodyText { content } }
      }
    }
  }
}
```

with `{"themeId": "...", "filenames": ["templates/product.<templateSuffix>.json"]}`.

A PagePilot template is 50–70 KB, so the MCP will spill the result to a
`tool-results/...txt` file and give you the path. Extract it with the bundled
helper, which reads the spill as UTF-8, writes the body as UTF-8 without BOM,
checks it parses, and lists every `shop_images` reference:

```
python3 scripts/extract-template.py <spill.txt> scratch/source-template.json scratch/manifest.json
```

**Mojibake check.** If you ever see `Ã¼`, `Ã¶`, `â€™` in the extracted text,
the spill file was decoded as ANSI/cp1252. Re-read it as UTF-8 (the helper
does; if you're doing it by hand in PowerShell, use `Get-Content -Encoding UTF8
-Raw` and write with `[System.IO.File]::WriteAllText($path, $text,
[System.Text.UTF8Encoding]::new($false))` so there's no BOM).

**Header comment.** Template files start with an auto-generated `/* ... */`
comment. `json.loads` will refuse the raw body; strip the comment first
(the helper does). Keep the header out of the file you upload — Shopify
regenerates it — or leave it in; both are accepted, but validate the JSON on
the stripped version.

## 3b. Phase 1 — harvest the snippets the template renders

```graphql
query Snippets($themeId: ID!) {
  theme(id: $themeId) {
    files(first: 50, filenames: ["snippets/pb-*"]) {
      nodes {
        filename size checksumMd5
        body { ... on OnlineStoreThemeFileBodyText { content } }
      }
    }
  }
}
```

Use the prefix the template's `{% render '…' %}` calls actually name (grep
`render '` in the template body). If the response comes back inline rather
than spilled, request the snippets together with the template in one
`filenames` list so the combined result spills to a file and lands on disk
verbatim. Verify each saved body against its `checksumMd5`. Then grep the
snippets for `file_url` and `shop_images` and add those files to the
manifest.

## 3c. Phase 3 — does the destination already sell it?

```graphql
query ExistingProduct($handle: String!) {
  productByIdentifier(identifier: { handle: $handle }) {
    id title status templateSuffix
    variantsCount { count } mediaCount { count }
    priceRangeV2 { minVariantPrice { amount currencyCode } }
  }
}
```

A hit means offer the choice in SKILL.md Phase 3 before any product write. For
"replace the page only", upsert the translated template a second time under
`templates/product.<existing templateSuffix>.json` in the duplicate theme.

## 4. Phase 1 — resolve `shop_images` references to CDN URLs

The template refers to library files as `shopify://shop_images/<filename>`
(sometimes with a `?v=123` cache suffix — strip it). These are **not** the
product's gallery. Resolve each to a downloadable URL on the source:

```graphql
query ShopImage($q: String!) {
  files(first: 5, query: $q) {
    nodes {
      id fileStatus
      ... on MediaImage { image { url width height } originalSource { url } }
      ... on GenericFile { url originalFileSize }
    }
  }
}
```

with `{"q": "filename:image_124_1782119511205-79578416-82936164-89771420_0.jpg"}`.
Use `image.url` (the CDN URL). If the query returns several hits, pick the one
whose URL ends in the exact filename. Write every filename → URL pair into the
manifest. **Count them against the helper's list before you switch**; a
missing one is a blank section on the destination.

## 5. Phase 2 — read the destination's brand styling

Brand settings live in the `main` section of each PagePilot template, not in a
theme-wide setting, so read one existing template on the destination (this is
a read, so it's fine either before or after `switch-shop`, but you need to be
on the destination):

```graphql
query DestinationTemplates($themeId: ID!) {
  theme(id: $themeId) {
    files(first: 3, filenames: ["templates/product.pagepilot-*.json"]) {
      nodes { filename size }
    }
  }
}
```

Read one of them (recipe 3) and pull from `sections.main.settings`:

| key | meaning |
|---|---|
| `pp_brand_color` | accent color used across sections (e.g. `#04b67b` on Nestilia) |
| `pp_button_background_color`, `pp_button_text_color` | CTA styling |
| `pp_heading_color`, `pp_body_color` | text colors |
| `pp_border_radius` | corner radius (e.g. `12`) |
| `heading_font_size`, `body_font_size` | typography |

Copy those into the translated template's `main.settings`. Also search the
custom-liquid HTML for the *source* brand color as a hex literal (e.g. inline
`style="color: #04B67B"`) and replace it with the destination's; PagePilot
custom blocks often hard-code it.

## 6. Phase 3 — confirm the page-builder sections exist

```graphql
query PagePilotSections($themeId: ID!) {
  theme(id: $themeId) {
    files(first: 50, filenames: ["sections/pp-*"]) { nodes { filename } }
  }
}
```

Expect roughly: `pp-main-product`, `pp-image-with-text`, `pp-image-with-benefits`,
`pp-image-with-percentage`, `pp-call-to-action`, `pp-faqs`, `pp-review-grid`,
`pp-review-slider`, `pp-differences`, `pp-recommended-products`,
`pp-custom-liquid` (all `-v1-0-0.liquid`). Compare against the section `type`
values in your template; a type that has no matching section file will render
nothing, so stop and tell the user PagePilot needs installing on that store.

## 7. Phase 4 — `fileCreate` for section images

One mutation, all files, original filenames preserved:

```graphql
mutation UploadSectionImages($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files { id fileStatus alt ... on MediaImage { image { url } } }
    userErrors { field message code }
  }
}
```

```json
{ "files": [
  { "originalSource": "https://cdn.shopify.com/s/files/.../image_124_....jpg",
    "filename": "image_124_1782119511205-79578416-82936164-89771420_0.jpg",
    "contentType": "IMAGE",
    "duplicateResolutionMode": "RAISE_ERROR" }
] }
```

A `FILE_ALREADY_EXISTS`-type user error is fine (the destination already has
that image). Anything else, fix before continuing. Files land with
`fileStatus: UPLOADED` and become `READY` a few seconds later; you don't need
to wait for that before writing the template.

### 7b. When `fileCreate` is denied — theme-asset fallback and in-place replace

Snippet-referenced images can live in the theme instead of Files:

```graphql
mutation UpsertAssets($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    userErrors { filename code message }
  }
}
```

```json
{ "themeId": "gid://shopify/OnlineStoreTheme/…",
  "files": [ { "filename": "assets/pb-ugc-beige.webp",
               "body": { "type": "URL", "value": "https://cdn.shopify.com/…/pb-ugc-beige.webp" } } ] }
```

then change `{{ 'pb-ugc-beige.webp' | file_url }}` to `| asset_url` in the
snippet and re-upsert it. Verify with a `files(filenames: ["assets/pb-*"])`
read (size and `contentType`).

To replace a library image in place, keeping its filename and every reference:

```graphql
mutation ReplaceFile($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    files { id fileStatus ... on MediaImage { image { url } } }
    userErrors { field message code }
  }
}
```

```json
{ "files": [ { "id": "gid://shopify/MediaImage/…", "originalSource": "https://…/localized.png", "alt": "…" } ] }
```

The `image` comes back null while it reprocesses; re-query `files` a few
seconds later for the new `?v=` URL and confirm the live page references it.

## 8. Phase 5 — `productCreate` with ordered media, then prices

Media order is set by the order of the `media` array in the create call.
**Never** fix order afterwards with `productReorderMedia` — it drops the last
image.

```graphql
mutation CreateProduct($product: ProductCreateInput!, $media: [CreateMediaInput!]) {
  productCreate(product: $product, media: $media) {
    product {
      id handle status templateSuffix
      variants(first: 100) { nodes { id title selectedOptions { name value } } }
      media(first: 100) { nodes { id alt mediaContentType } }
    }
    userErrors { field message }
  }
}
```

```json
{
  "product": {
    "title": "…translated title…",
    "handle": "…",
    "descriptionHtml": "…translated…",
    "vendor": "…", "productType": "…", "tags": ["…"],
    "status": "DRAFT",
    "templateSuffix": "pagepilot-<see naming convention>",
    "seo": { "title": "…", "description": "…" },
    "productOptions": [
      { "name": "Size", "values": [ { "name": "S" }, { "name": "M" } ] }
    ]
  },
  "media": [
    { "originalSource": "https://cdn.shopify.com/…/gallery-1.jpg", "alt": "…translated alt…", "mediaContentType": "IMAGE" },
    { "originalSource": "https://cdn.shopify.com/…/gallery-2.jpg", "alt": "…", "mediaContentType": "IMAGE" }
  ]
}
```

`productCreate` with `productOptions` creates every option-combination variant
at price 0. Then set prices etc. in one call, matching variants by the
`selectedOptions` returned above (if the source had fewer variants than the
full combination grid, delete the extras with `productVariantsBulkDelete`):

```graphql
mutation SetVariants($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id title price compareAtPrice inventoryPolicy inventoryItem { tracked } }
    userErrors { field message }
  }
}
```

```json
{ "productId": "gid://shopify/Product/…",
  "variants": [
    { "id": "gid://shopify/ProductVariant/…",
      "price": "49.95", "compareAtPrice": "89.95",
      "inventoryPolicy": "CONTINUE",
      "inventoryItem": { "tracked": false, "requiresShipping": true },
      "mediaId": "gid://shopify/MediaImage/…" }
  ] }
```

Prices are copied as-is; the store's currency is whatever `currencyCode` says,
and the currency difference is flagged in the report, never converted.

If `templateSuffix` wasn't set at create time, set it now:

```graphql
mutation SetTemplate($input: ProductUpdateInput!) {
  productUpdate(product: $input) {
    product { id templateSuffix }
    userErrors { field message }
  }
}
```

with `{"input": {"id": "gid://shopify/Product/…", "templateSuffix": "pagepilot-…"}}`.

## 9. Phase 6 — theme duplicate, staged upload, upsert, verify

Writes to the live (MAIN) theme are blocked by policy. Duplicate it:

```graphql
mutation DuplicateLive($id: ID!, $name: String) {
  themeDuplicate(id: $id, name: $name) {
    newTheme { id name role processing }
    userErrors { field message }
  }
}
```

Name it so the user recognises it in the theme list, e.g.
`"<Live theme name> + <product> page 2026-09-14"`. Poll until `processing` is
false:

```graphql
query ThemeReady($id: ID!) { theme(id: $id) { id name role processing } }
```

Stage the upload (this returns a signed target; save `stagedTargets[0]`
verbatim to `scratch/staged-target.json`):

```graphql
mutation StageTemplate($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}
```

```json
{ "input": [ { "resource": "FILE", "filename": "product.pagepilot-….json",
               "mimeType": "text/plain", "httpMethod": "POST",
               "fileSize": "61234" } ] }
```

`fileSize` is the exact byte count of the local file as a string. Then push
the file:

```
pwsh scripts/upload-staged.ps1 -FilePath scratch/product.pagepilot-….json -TargetJson scratch/staged-target.json
# or, off Windows:
python3 scripts/upload-staged.py scratch/product.pagepilot-….json scratch/staged-target.json
```

Both print the local size and MD5 and end with the `resourceUrl`. Upsert into
the **duplicate** theme:

```graphql
mutation UpsertTemplate($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    userErrors { filename code message }
  }
}
```

```json
{ "themeId": "gid://shopify/OnlineStoreTheme/…",
  "files": [ { "filename": "templates/product.pagepilot-….json",
               "body": { "type": "URL", "value": "<resourceUrl>" } } ] }
```

An empty `upsertedThemeFiles` with no `userErrors` is not proof of anything.
Verify:

```graphql
query VerifyTemplate($themeId: ID!, $filenames: [String!]!) {
  theme(id: $themeId) {
    files(first: 1, filenames: $filenames) { nodes { filename size checksumMd5 updatedAt } }
  }
}
```

`size` must equal the local byte count and `checksumMd5` the local MD5 the
upload script printed. If Shopify has re-added its header comment the size
will differ; in that case read the body back (recipe 3), strip the header, and
compare the parsed JSON to your local parsed JSON instead. Only report
"verified" when one of those two comparisons passes.

## 10. Phase 7 — publish and activate

Online Store publication id:

```graphql
query OnlineStorePublication {
  publications(first: 10) { nodes { id catalog { title } } }
}
```

```graphql
mutation PublishProduct($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    publishable { ... on Product { id publishedOnPublication(publicationId: "gid://shopify/Publication/…") } }
    userErrors { field message }
  }
}
```

with `{"id": "gid://shopify/Product/…", "input": [{"publicationId": "gid://shopify/Publication/…"}]}`.
Then set `status: ACTIVE` with `productUpdate` (recipe 8's mutation, input
`{"id": …, "status": "ACTIVE"}`).

## 11. Template naming convention

PagePilot names its templates `product.pagepilot-<13-digit ms timestamp>-<6-digit random>.json`
(observed on Nestilia: `product.pagepilot-1782119554120-379366.json`). Generate
a fresh one for the clone (`pagepilot-$(date +%s%3N)-$((RANDOM % 900000 + 100000))`)
so the app keeps recognising the page as one of its own, and use the same
string (without `product.` and `.json`) as the product's `templateSuffix`.

## 12. Gotchas collected from real runs

- `switch-shop` revokes the source token. Harvest first, always.
- Query results over the MCP's output cap spill to a `.txt`; read them as
  UTF-8 or you get mojibake.
- `shop_images` references may carry `?v=…`; match `files` by bare filename.
- `fileCreate` must keep the original filename or the template's
  `shopify://shop_images/<name>` reference breaks.
- `productReorderMedia` drops the last media item; order at create time. To
  rebuild an existing product's gallery, `productCreateMedia` the full new set
  (it appends in array order) and *then* `productDeleteMedia` the old ids —
  the product never sits empty and no reorder is needed.
- Templates render snippets; harvest `snippets/` too or sections render Liquid
  errors on the destination.
- The destination may already sell the product at the same handle — check
  before `productCreate`.
- `fileCreate` needs the staff account's "Create files" permission, not just
  the app scope; theme assets are the fallback for snippet-referenced images.
- `productCreate` leaves every variant at price 0 until `productVariantsBulkUpdate`.
- Theme file writes to the MAIN theme are rejected; write to a duplicate.
- `themeFilesUpsert` can return an empty list on success; verify by checksum.
- Custom-liquid blocks hard-code the source brand color and often contain
  JavaScript with month/day names; translate the format, not only the words.

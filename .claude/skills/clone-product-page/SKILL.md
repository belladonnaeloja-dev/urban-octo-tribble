---
name: clone-product-page
description: >-
  Clone a complete Shopify product page from one of the user's stores to another
  and translate it into the destination store's language — product, variants,
  pricing, gallery images, section images, and the full PagePilot page template
  with every string translated. Use this whenever the user names a product and
  two stores, in any phrasing: "copy X from Zanaro to Nestilia", "duplicate this
  product page on Solundi", "put this product on Modlia in French", "replicate
  this page in English on Nestilia", or when they paste a product URL from one
  store and mention another store. The destination language is inferred from the
  store, so the user never has to state it. Also use it for partial requests like
  "clone the botaneman page over to Nestilia" or "I want this same page on my
  Dutch store". NOT for translating an existing product already on the
  destination store (that is a productUpdate job), and NOT for image-only
  localization (use localize-images-de-nl / localize-images-en-fr directly).
---

# Clone a product page across stores, translated

Port a product and its entire PagePilot page from a source store to a
destination store, rendering every piece of copy in the destination store's
language. The user should only need to say the product and the two stores.

This skill drives the **Shopify Admin MCP** (`graphql_query`, `graphql_mutation`,
`search_products`, `get-shop-info`, `switch-shop`) and, for the image pass, the
**Higgsfield** MCP via the existing localize-images skills.

## The one thing that will ruin the run if you get it wrong

`switch-shop` **revokes the current store's access token**. Once you switch to
the destination, the source store is gone — you cannot go back for a forgotten
image URL without another switch and possibly a full reconnect by the user.

So: **harvest everything from the source in one pass, save it to disk, and only
then switch.** Phase 1 below is that harvest. Treat leaving it incomplete as the
main failure mode of this skill.

The connector may also drop authorization entirely on switch and need the user
to reconnect. That is normal — tell them plainly, and note that all harvested
data is already safe on disk so nothing needs redoing.

## Store map

Read `references/store-map.md` for the language, currency and brand identity of
each store. If the user names a store that isn't in that file, ask which
language it sells in rather than guessing from the domain — a `.com` tells you
nothing, and getting this wrong means translating an entire page into the wrong
language.

## Phase 0 — Resolve the request

Work out the product, the source store, and the destination store. If the user
gave a URL, the handle is in it (`/products/<handle>`). If they gave a name,
you'll search for it in Phase 1.

Look up the destination language in the store map and **state it back in one
line** before doing the work ("Cloning to Nestilia, so translating into
English"). This is cheap and catches a misidentified store before you've spent
the whole run translating into the wrong language.

## Phase 1 — Harvest everything from the source

Confirm you're on the source store with `get-shop-info` first.

Collect, and write to a scratch directory as you go:

1. **The product** — `search_products` by handle or title to get the GID, then
   query the full record: title, `descriptionHtml`, `productType`, `vendor`,
   `tags`, `seo`, `options`, `status`, and for every variant its price,
   `compareAtPrice`, `sku`, `inventoryPolicy`, `selectedOptions`, and
   `inventoryItem { tracked requiresShipping }`. Also grab `media` in gallery
   order with full CDN URLs.

2. **`templateSuffix`** — this is what tells you the page is built with a page
   builder. If it's null, the page is just the product description and this job
   is much smaller.

3. **The template file** — from the source's `MAIN` theme, read
   `templates/product.<templateSuffix>.json`. It will likely blow past the tool's
   output limit and be spilled to a file; that's fine and actually convenient.
   Extract the body to your scratch directory with proper UTF-8 handling
   (see `references/shopify-recipes.md` — mojibake like `Ã¼` means you read the
   spill file as ANSI instead of UTF-8).

4. **Every `shopify://shop_images/<filename>` reference in that template.**
   These are *store-library* files, entirely separate from the product's gallery.
   Grep them out of the template, then resolve each to a CDN URL with a `files`
   query. Miss one and that section renders blank on the destination.

Save a manifest (product spec + every image URL) so Phase 3 onward can work
without the source.

## Phase 2 — Translate

Translate the template into the destination language, working on a copy. What
needs translating is easy to underestimate — walk the whole file, not just the
obvious headings:

- section and block settings: headings, subtitles, body text, button labels
- `pp_custom_liquid_block` and `pp-custom-liquid` HTML — rating text, stock
  alerts, trust badges, discount banners, Trustpilot slider cards
- `buy_buttons` labels (`add_to_cart_text`, `sold_out_text`, `unavailable_text`)
- FAQ questions *and* answers, every review's text and its "Verified Buyer" label
- `image_alt` fields
- any JavaScript containing day/month names or date formatting — rewrite the
  format to suit the locale, don't just swap the words

Translate as a native marketer would write it, not literally. This is sales
copy; it should read like it was written for that market.

**Fix inherited defects rather than faithfully copying them.** Source pages
routinely carry leftovers from whatever product they were cloned from — a
stale ™ brand name in a few sections, the source store's name in review cards,
an add-to-cart button still in a third language. Normalize these to the
destination product and store, and **list every such fix in your final report**
so the user can see what you changed and why. Copying a wrong brand name
faithfully into a new store helps nobody.

Two judgment calls worth making deliberately:

- **Brand styling.** Read the destination's own brand color and border radius
  from an existing PagePilot template there (recipe in references) and apply
  them, so the page looks native instead of imported.
- **Numbers stay numbers.** Never convert prices between currencies. Copy the
  figures and *flag* the currency difference — the user prices for margin, not
  by exchange rate.

Validate that the translated file still parses as JSON before going near
Shopify. A broken template means a broken storefront page.

## Phase 3 — Switch and verify

Call `switch-shop`, then **`get-shop-info` before any write at all.** Confirm the
domain is the destination the user asked for and say so in your response. The
user needs to be able to trust that a clone never writes to the wrong store, and
this check is what earns that.

If the connector needs reconnecting, stop and ask, then re-verify on return.

Then confirm the destination theme actually has the page builder's sections
installed (`sections/pp-*`). Without them the template renders nothing, and it's
better to find out now than after uploading everything.

## Phase 4 — Section images

Upload every harvested `shop_images` file with `fileCreate`, **preserving the
exact original filename** — the template refers to them by name, so a renamed
file is a broken image. Use `duplicateResolutionMode: RAISE_ERROR`; a collision
just means the destination already has that image, which is fine.

## Phase 5 — Product

Create the product with `productCreate`, passing the gallery images as `media`
**in the correct order in that same call**. Do not create them and reorder
afterwards: `productReorderMedia` drops the last image. Order at creation time is
the only safe way.

Create it as `DRAFT` for now — Phase 7 flips it live once the page actually
exists. Then set price, `compareAtPrice`, `inventoryPolicy` and inventory
tracking with `productVariantsBulkUpdate` (the create call leaves price at 0).

Set `templateSuffix` to the new template name you're about to create. Use the
page builder's own naming convention so the app still recognizes the page.

## Phase 6 — Theme and template

Writing theme files to a **live/published theme is blocked** by policy. Don't
burn a large upload discovering this — if you want to confirm, probe with a
tiny throwaway file first.

So: duplicate the destination's live theme (`themeDuplicate`), wait for
`processing` to become false, and write the template into the duplicate.

**Do not retype the template into the mutation.** It's typically 50–70KB, and
hand-escaping it into a GraphQL variable is slow and easy to get subtly wrong.
Instead push the file straight from disk:

1. `stagedUploadsCreate` (resource `FILE`, mimeType `text/plain`) → returns an
   upload URL and signed parameters
2. run `scripts/upload-staged.ps1` to POST the local file to that target
3. `themeFilesUpsert` with `body: { type: URL, value: <resourceUrl> }`

`themeFilesUpsert` may return an empty list with no errors, which tells you
nothing. **Verify by reading the file's `checksumMd5` and `size` back and
comparing to the local file.** Matching checksums are what let you tell the user
the page is correct rather than probably correct.

Full recipe with the exact mutations: `references/shopify-recipes.md`.

## Phase 7 — Go live, then images

Publish the product to the Online Store channel and set it `ACTIVE`.

Do this **last**, and be direct about the consequence in your report: the
template lives in the *duplicated, unpublished* theme, so until the user
publishes that theme, the live storefront renders this product with the
**default** product template — a bare page. The user has chosen this tradeoff
deliberately, so don't re-litigate it; just make sure they can't miss that
publishing the theme is the step that makes the page look right.

You cannot publish a theme yourself, and shouldn't want to — publishing swaps
their entire live theme. Hand them the theme name and tell them the duplicate
was taken today, so any live-theme edits made in the meantime would be lost on
publish. If they're mid-edit, copying the single template file across in Edit
code is the safer route.

Then localize text baked into the images. Identify which images actually carry
foreign text (source-language filenames are a hint, but check the images
themselves), and hand off to the matching skill by target language:
`localize-images-en-fr` for English or French, `localize-images-de-nl` for German
or Dutch. Pass the destination product name, since the rebranded name often
differs from the source.

## Phase 8 — Report

Close with something the user can act on:

- destination store, confirmed by domain
- product: title, status, price, image counts
- theme name to publish, and the checksum-verified template
- **what you changed rather than copied** — brand colors, normalized brand
  names, store names in reviews
- **what deserves their judgment** — currency meaning if it changed, social
  proof numbers inherited from the source store ("1,200 reviews", "8,000
  customers") that may not be defensible for a newer store, and any review or
  section that is obviously about a different product

That last group matters. A clone silently carries the source's claims into a
store where they may not be true, and the user is the only one who can decide
that. Surfacing them is part of doing this job well, not an optional extra.

## Scope discipline

Clone what exists. If the source page is weak, say so in a sentence and clone it
anyway — rebuilding a page for conversion is `optimize-product`, a different job
the user hasn't asked for here.

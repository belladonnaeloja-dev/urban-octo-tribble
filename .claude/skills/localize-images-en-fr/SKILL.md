---
name: localize-images-en-fr
description: "[EN + FR] Localize product-page IMAGES into American English (en-US) and French (France, fr-FR) using Higgsfield. Every run does the same three things by default: translates EVERY text-bearing gallery image into both languages, builds a comparison table and a before/after split in both languages, and re-backgrounds any plain-white tile onto an on-brand setting drawn from the store's own photos. Keeps layout pixel-identical across languages via a master-then-text-swap workflow, enforces a mobile-readable minimum font size on every caption, and always ends with one clickable table showing every gallery position side by side in 🇺🇸 EN and 🇫🇷 FR. Use when the user asks to translate/localize product images to American English or French, or to produce EN/FR versions of gallery graphics for their stores (Modlia FR, Nestilia EN, Zanaro EN, Cellumove EN/FR). Delivers files in chat by default; also replaces the live gallery when asked to, or when the request names a store (\"translate the images on Nestilia\") or comes from clone-product-page. THIS SKILL IS ENGLISH + FRENCH ONLY — for German (DE) or Dutch (NL) use localize-images-de-nl instead."
---

# Localize product images — American English & French (France)

Produce or translate product-page imagery in **American English (en-US) and
French (fr-FR)**, with layouts identical across both languages. Drives the
**Higgsfield** MCP (`generate_image`, `media_import_url`, `job_display`,
`show_generations`) and, when uploading, the **Shopify** Admin MCP
(`graphql_query`, `graphql_mutation`, `search_products`).

## Inputs (ask only for what's missing)

- **source** — a product URL, Shopify handle/GID, or pasted image URLs. REQUIRED.
- **mode** — not a question to ask. Every run is translate **and** create **and**
  re-background, in both languages. See *The baseline set* below.
- **source language** — for the translate half. Detect from the **images
  themselves**, not the page. See *Detect the language from the images* below.
- **extra asset types** — beyond the two mandatory ones, optionally: how-it-works
  diagram, spec/composition panel, care panel. Only on request.
- **product name** — including ™ if the user uses one. Never translate it.
- **delivery** — default **deliver files in chat as download links**. Only touch
  a live store if the user explicitly says to upload. **Exception: when invoked
  from a store workflow** (`clone-product-page`, or any ask phrased as "translate
  the images *on* / *in* <store>"), uploading IS the job — deliver the files AND
  replace the gallery, then verify the live order. "Do the images on Nestilia"
  does not mean "hand me PNGs"; if the user has to ask whether you are inserting
  them, the default was read wrong.

### Detect the language from the images, not the page

The storefront language and the baked-in image text are frequently different —
dropshipped tiles usually arrive in English or Chinese and get dropped into a
German, French, or Dutch store untouched. A German page can carry an entirely
English image set.

So: after downloading the tiles, read the text off the **images** and set the
source language from that. Then state the split explicitly before generating,
because it changes the render count — if the tiles are already English, the 🇺🇸
side is mostly done and only 🇫🇷 needs rendering. Do not infer source language
from the page title, description, or store domain.

### The baseline set — deliver all of this, every time

A request phrased as "translate these images" still means the whole set. Unless
the user explicitly narrows it, every run produces:

1. **Every text-bearing gallery image, in 🇺🇸 EN and 🇫🇷 FR.** Not just the ones
   in the source language you happened to find — both languages, complete.
2. **A comparison table, in 🇺🇸 EN and 🇫🇷 FR.** `<Product>™ vs. <the thing they
   use today>`.
3. **A before/after split, in 🇺🇸 EN and 🇫🇷 FR.**
4. **Every plain-white tile re-backgrounded on-brand** — see *Brand the
   background* below.

These four are the deliverable. Do not wait to be asked for the comparison table
or the before/after; their absence reads as an incomplete job and it will come
back as a follow-up request. If you are deliberately skipping one, say so in a
single line at the start with the reason — never omit it silently.

Photo-only tiles with no text still appear in the final table under both
languages, pointing at the original (or re-backgrounded) file, so the set reads
as complete.

### Images are never the whole page — audit it before you sign off

Finishing the image set is not finishing the job. Before you report done, look at
the PAGE the images live on and tell the user what else is missing. On a real
Modlia/RattlePals run the gallery shipped correctly and the operator then had to
find four missing page sections himself, one message at a time.

- Run the section list in `optimize-product`'s *Definition of Done* against the
  live page (problem/agitation, how-it-works steps, comparison table,
  objection-refutation, Pinterest-viral/low-stock, UGC grid, risk reversal, FAQ,
  specs + package contents…). Name the gaps even if fixing them is out of scope:
  "images done; the page is also missing X, Y, Z — want those?"
- **"Exactly as on {other store}" means diff that store, not guess.** Fetch
  `https://{store}/products/{handle}.json`, decode the escaped body, and list its
  heading spine and `<!-- N. SECTION -->` markers. Everything present there and
  absent here is in scope by default. Do not rebuild the reference from memory or
  from an earlier session's summary — a previous session's notes said "the Zanaro
  set" and left out half the page.
- Also check the theme-side images and any non-gallery tiles for stray foreign
  text; the product's `media` array is not the whole page.

## Core technique — master, then text-swap

This is the whole trick. Do NOT generate each language independently; layouts
will drift and the set will look inconsistent.

1. Generate (or import) **one master** image.
2. **Verify the master** by downloading and Reading it.
3. For each additional language, call `generate_image` with the *master's job id*
   as `medias[].value` (role `image`) and a prompt that says: *"Keep this image
   EXACTLY the same — same background, same photos, same layout, same fonts,
   font sizes, colors, positions, icons, spacing. ONLY replace the text, in
   place: 'X' → 'Y'; ..."*
4. Verify every output before delivering.

Pin every string as an explicit `'source' → 'target'` pair. Left to itself the
model invents copy.

**A job id works as `medias[].value` exactly like a `media_id`.** Chain freely:
original → EN master → FR swap → enlarged EN → matching FR. Each hop inherits
the previous layout, which is what keeps the pair identical.

## Pipeline

1. **Fetch + classify.** `WebFetch` the page for image URLs, or `graphql_query`
   the product's `media(first:50)`. Download candidates and Read them. Tag each
   on two axes: **TRANSLATE / SKIP** (photo-only, already localized, or animated
   GIF → always SKIP) and **REBRAND / KEEP** (plain-white background → REBRAND).
   The two are independent — a white-background photo with no text still gets
   rebranded, and a text tile already on a lifestyle background is translated but
   not rebranded. Note the store's background look from the lifestyle tiles now;
   you will reuse it.
2. **Transcribe.** For every TRANSLATE tile, open it full-res and transcribe the
   exact source text verbatim. Dense tiles (tables, feature lists, size charts)
   must be transcribed line by line.
3. **Import.** `media_import_url` each source → `media_id`. Imports are unmetered
   and don't count toward concurrency; do them all up front.
4. **Generate.** Model `nano_banana_pro`. Always pass `resolution: "2k"` —
   the default is `1k` and small type does not survive it. **Concurrency cap is
   8** — submit in batches of ≤8; the 9th errors `Rate limit reached`.
5. **Verify — ALWAYS.** Download every result and Read it. Run the full
   *Verification checklist* below. Never deliver an unseen image.
6. **Deliver.** Attach the verified files with `SendUserFile`, then post the
   **full-set table** — see *Delivery* below; the exact format is mandatory and
   is the last thing every run outputs. Upload to Shopify when asked or when
   invoked from a store workflow: `productDeleteMedia` the whole existing
   gallery, then ONE `productCreateMedia` listing every image in final order
   (`_min.webp` `minUrl` as `originalSource`). Never `productReorderMedia`.

### Verification checklist

Read every output and check all of it, not just the translation:

1. Correct target language, correct spelling, **all accents present**.
2. Layout, photos, icons intact — nothing redrawn that should have been copied.
3. Product name and ™ unchanged.
4. **Type passes the mobile legibility floor** — see below.
5. **Capitalization style matches the sibling language** — see below.
6. **No bare white background left**, and the product silhouette survived the
   re-background unchanged — see *Brand the background* below.
7. **Text contrast still works** against whatever background it now sits on.
8. All bullets in a group are the **same size** — the model silently shrinks one
   long line to make it fit, which is the tell that the copy needs shortening
   rather than the type needing scaling.
9. No clipping, no overlap, nothing running off the frame.
10. No watermark survived, no invented text, badge, rating, or reviewer.

## Mobile legibility floor — check this on EVERY tile

Most product-page traffic is mobile, where a 2048px tile renders at ~400px. Text
that looks fine while you're reading the full-res file is unreadable there. This
is the single most common defect in delivered sets, and it applies to
**translated tiles just as much as created ones** — an inherited layout inherits
its too-small captions.

**The floor: caption cap-height ≥ ~3% of image height.** Concretely:

| Output size | Minimum caption height | Comfortable |
|---|---|---|
| 1024 px | ~30 px | 40 px+ |
| 2048 px | ~60 px | 70 px+ |

Estimate it by eye against the frame — a caption that occupies less than about a
thirtieth of the image height is too small. Headlines are almost never the
problem; **icon-row captions, footnotes, spec labels, and quadrant captions are.**

When a tile fails the floor, re-render it from itself as master with a prompt
that:

- names the exact strings that are too small and asks for a specific increase
  (*"increase their font size by roughly 70 percent"*) — a bare "make it bigger"
  moves it a few pixels;
- asks for **bold, thick-stroked** weight, not just larger;
- explicitly permits the **container to grow** (*"make the white panel taller and
  wider as needed, let it extend toward the bottom edge"*) and the caption to
  wrap to two lines — otherwise the model shrinks the type back down to fit;
- scales icons up slightly alongside the text so the panel stays balanced;
- restates that wording, photos, and colors must not change.

Then re-verify. And re-check the sibling language, because the enlarged pair must
still match.

## Brand the background — never ship a bare white tile

Supplier tiles arrive on flat white cutout backgrounds. White reads as *generic
marketplace listing*, not as this store's product, and a gallery that mixes
white cutouts with real lifestyle photos looks assembled from scraps. **Any
image whose background is plain white or near-white gets re-backgrounded onto a
setting that matches the product page.** Do this without being asked; it is part
of the baseline set.

**Derive the background from the store's own photos, not your imagination.**
Import one or two of the product's real lifestyle gallery images and pass them as
extra `medias[]` references, then prompt for the same room, surfaces, palette and
light. That is what makes the new tile look like it came from the same shoot as
the rest of the page, which is the whole point.

If the product has no usable lifestyle photo, pick from the category:

| Product category | Background |
|---|---|
| Kitchen / homeware | Blurred kitchen — marble or wood counter, sink, pale cabinetry, warm daylight |
| Bath / body care | Soft bathroom — tile, folded towels, diffused light |
| Apparel / intimates | Warm neutral gradient studio, or a lifestyle interior |
| Baby / kids | Soft nursery, muted pastels, natural light |
| Tools / auto | Workshop bench, muted grey, shallow focus |
| Desk / tech | Wood desk, neutral wall, soft window light |

Rules for the re-background:

- **Blur it.** Shallow depth of field, product stays the hero. A sharp busy
  background competes with the product and the copy.
- **The product must not be redrawn.** State it explicitly — keep the product
  identical, only replace what is behind it. Then verify the silhouette.
- **Preserve every word of baked-in text at its existing size**, and re-check
  contrast: dark text that sat on white can disappear on a mid-tone background.
  Fix by lightening the background behind the text or adding the same
  semi-transparent scrim the rest of the set uses — never by shrinking the type.
- **One background family across the whole set.** Same room, same palette, same
  light, so the gallery reads as one shoot rather than six.
- **Dimension and spec diagrams:** brand them too, but keep the area behind the
  measurement lines pale and low-contrast so the numbers stay legible, and
  re-verify the product outline against the original per the drift rule below.

## Keep the two languages identical — watch for style drift

When both language versions are generated from the same master in the same batch,
the model can still style them differently — most often **capitalization**: one
comes back `DISH DRYING MAT` and the other `Tapis d'égouttage`. A page showing
one language in all-caps and the other in sentence case looks broken.

Compare the pair side by side before delivering. Check case, weight, bar/panel
height, and font size. If they diverge, **do not re-render both** — pick the
better one, then regenerate the other using the good one as `medias[].value`,
with the prompt stating the capitalization rule explicitly (*"SAME SENTENCE CASE
capitalization style — do NOT set the English captions in all capital letters"*).
Passing both images as references (good sibling first) helps the model lock the
style while swapping the words.

## Delivery — the full-set table (MANDATORY, always last)

Every run ends the same way: `SendUserFile` the verified files, then print the
block below. The user's job is to click and download — they should never have to
ask where a file is, scroll back through the transcript, or hunt a CDN URL out of
a tool result.

**One table covering every gallery position in both languages.** Users think in
terms of "my page has 12 images, give me the English set and the French set" —
not in terms of which files you happened to render. Photo-only tiles that carry
no text still belong in the table, listed under both languages, pointing at the
original URL. That is what makes the set look complete and lets them rebuild the
gallery position by position.

Rules for the block:

- **One row per gallery position**, numbered in page order, with created assets
  appended after the page images.
- **Two link columns**, 🇺🇸 English then 🇫🇷 French. Every cell gets a link —
  never leave one blank.
- **Bold the links you generated**; leave originals in plain text, and say so in
  a legend line above the table. This is how the user sees at a glance what is
  new and what is reused.
- **Link the `rawUrl`** for generated files (full resolution) and the original
  CDN URL for reused ones. Link text is the filename. Never paste a bare URL.
- Mark any row with a known defect `⚠️` and explain it in one line under the
  table, naming which language cell is affected. Never bury a flaw in prose.
- Keep local scratchpad paths out of the table — the attachments cover that.
- Follow with an **Outstanding** table if anything failed to render.
- Close with: one line on what changed if this was a fix pass, one line on where
  any new claims came from, one line on Shopify state, one line on credits.

Use exactly this shape:

```markdown
## <Product>™ — Full EN + FR Image Set

**Bold** = generated this session; plain = original page file, no text on it.

| # | Image | 🇺🇸 English | 🇫🇷 French |
|---|---|---|---|
| 1 | Lifestyle — product in use | [img01.png](originalUrl) | [img01.png](originalUrl) |
| 2 | Close-up detail | [img02.png](originalUrl) | [img02.png](originalUrl) |
| 3 | Split — Easy to Clean / Dishwasher Safe | [img03.jpg](originalUrl) | **[fr_tile3.png](rawUrl)** |
| 4 | Feature panel + icon row | **[en_tile4.png](rawUrl)** | **[fr_tile4.png](rawUrl)** |
| 5 | 4-quadrant use cases | **[en_tile5.png](rawUrl)** | **[fr_tile5.png](rawUrl)** |
| 6 | Size diagram ⚠️ | [img06.png](originalUrl) | **[fr_tile6.png](rawUrl)** |
| 7 | Colorways 🎨 | **[en_tile7.png](rawUrl)** | **[fr_tile7.png](rawUrl)** |
| 8 | Comparison table | **[en_compare.png](rawUrl)** | **[fr_compare.png](rawUrl)** |
| 9 | Before / After | **[en_beforeafter.png](rawUrl)** | **[fr_beforeafter.png](rawUrl)** |

🎨 = re-backgrounded off plain white onto the store's kitchen setting.

⚠️ **#6, French only** — <one-line description of the defect and what fixes it>.

Rows 8 and 9 are mandatory and always present. Mark rebranded rows with 🎨 and
add the one-line legend, so the user can see at a glance which tiles changed
background versus which only changed language.

### ⛔ Outstanding (N renders)

| Asset | Lang | Reason |
|---|---|---|
| Tile — No age limit | 🇺🇸 EN | job stalled in queue, never returned |
| Before / After | 🇫🇷 FR | out of credits |
```

Keep the row label identical across both language columns (`4-quadrant use cases`
appears once, worded the same) so the pair is obvious at a glance. If nothing is
outstanding, say so in one line rather than dropping the heading.

## Preflight — check credits BEFORE generating

Call `balance` first. **`nano_banana_pro` costs 2 credits per render** — confirm
with `get_cost: true` if unsure. Budget the whole baseline set:

| Work | Renders |
|---|---|
| Text tiles × 2 languages | 2 per text tile |
| Comparison table (master + FR swap) | 2 |
| Before/after (master + FR swap) | 2 |
| White-background tiles to rebrand | 1 per tile (+1 if it also carries text in the 2nd language) |
| Retries, font-size and contrast fix passes | 3–4 |

A typical page runs **16–24 renders / 32–48 credits**. Estimate out loud before
starting so the number is on the record.

Running dry mid-batch leaves a half-localized set, which is worse than not
starting — a product page with four English tiles and one French one looks broken.

- If the balance won't clearly cover the plan, **say so up front** with the
  render count you estimated, and let the user top up before you burn what's
  left. Do not start optimistically and discover it at tile 7. Do not spend the
  last credit or two on a partial set.
- Do the full audit anyway while you're blocked — classify every image,
  transcribe the text, and draft the target copy — so that "try now" after a
  top-up goes straight to generating.
- `list_workspaces` shows per-workspace credits; if another workspace has budget,
  offer `select_workspace` rather than stopping.
- If you do run dry mid-run, deliver every verified file immediately with the
  full table above, and put the un-rendered ones in **Outstanding** with
  `out of credits` as the reason. Never silently drop them.

## Language rules — American English

- **American** spelling and idiom: color, favorite, fiber, gray, analyze,
  traveled. Never colour/favourite/grey.
- Imperial first where a consumer number matters, metric in parentheses:
  `86°F / 30°C`. Decimal point, comma thousands separator: `4.6`, `25,000`.
- MM/DD/YYYY. `$` before the number.
- Sentence case for captions, Title Case for headlines — pick one and hold it
  across the whole set, **and across both languages**.
- Fix grammar rather than translating literally; source copy from another
  language is often stilted. "Relief from chafing and swelling" beats a
  word-for-word rendering.
- **English source text is not automatically shippable.** Dropshipped tiles are
  usually machine-translated English with dangling pronouns, double spaces, and
  missing articles (`Silicone  drying mat that protects it from high
  temperatures`). Read every English tile critically and rebuild the broken ones
  — that is a legitimate 🇺🇸 deliverable, not a no-op. Quote the before and after
  when you report it.
- Established terms: Before / After · Sizes · Care Instructions · Machine Wash ·
  Do Not Bleach · Do Not Iron · Do Not Dry Clean · Breathable · Opaque ·
  Compression · Satisfaction or Your Money Back · Free Size Exchange ·
  Elastane (US retail also accepts Spandex) · Nylon or Polyamide.

## Language rules — French (France)

- All accents must render: **é è ê ë à â ù û ô î ï ç É È À Ç**. State this in
  every prompt. Accents on capitals are correct in French (`ÉLASTHANNE`,
  `APRÈS`) — call this out explicitly when the label is set in capitals, or the
  model drops the accent.
- Metric only. Strip Fahrenheit entirely — `30 °C`, non-breaking space before °C.
  Decimal comma: `4,6`. Space before `!`, `?`, `:`, `;` and inside `« »`.
  **The space before `:` applies to HEADINGS too, not just body lines.** A spec
  panel shipped with `Spécifications:` above four correct `Taille : / Poids :`
  rows — the inconsistency is what reads as sloppy. List every colon in the tile
  in your prompt.
- **RARE diacritics fail and retrying makes them WORSE — reword instead.** The
  common accents (é è à î ô ç, including on capitals) render first time. The ï in
  `ouïe` came back as `ouie`, then as `ouïë` on two increasingly explicit retries,
  because a text-swap edit anchors on the reference image and keeps reproducing the
  error it can already see. **Budget ONE retry.** If a rare diacritic fails twice,
  go back to the ORIGINAL master (not your broken output) and re-render with copy
  that avoids the character — « Saisir et écouter se travaillent en jouant »
  replaced the `ouïe` line and landed first try, same meaning. Choosing words built
  from common accents up front is cheaper than any fix.
- **Strip imperial units from size and spec diagrams too**, not just
  temperatures: `32.5cm/12.67inch` → `32,5 cm`. Instruct removal explicitly —
  "metric only" alone often leaves the inches in place.
- French runs ~15–25% longer than English. Expect reflow; check nothing clips.
- **When a French line is too long, shorten the French — do not let the type
  shrink.** The model silently scales one overlong label down to fit, leaving it
  visibly smaller than its neighbors. `Plan de travail encombré` had to become
  `Désordre constant` to set at full size. Pick target copy short enough to
  match its siblings before you render, and check bullet groups for one odd
  small line afterward.
- *vous* for consumer e-commerce. Avoid Québécois forms (*magasiner*,
  *courriel*) — this is France French.
- Watch anglicisms: *short* (the garment) is fine and standard; *push-up* is
  fine; but prefer *frottements* over "chafing", *respirant* over "breathable".
- Established terms: Avant / Après · Tailles · Conseils d'entretien ·
  Lavage en machine · Ne pas blanchir · Ne pas repasser · Ne pas nettoyer à sec ·
  Respirant · Opaque · Compression · Satisfait ou remboursé ·
  Échange de taille gratuit · Élasthanne · Polyamide.
- Kitchen/homeware vocabulary that recurs: *tapis d'égouttage* (drying mat) ·
  *va au lave-vaisselle* (dishwasher safe) · *antidérapant* (non-slip) ·
  *silicone alimentaire* (food-grade silicone) · *plan de travail* (countertop) ·
  *évier* (sink) · *égouttoir* (dish rack) · *torchon* (dish towel).

## Never translate

Product/brand names and ™, prices, numbers, percentages, size codes (M/L/XL/3XL),
measurements, reviewer names, and **any text physically printed on the product
itself** (packaging, labels, garment prints). Say so explicitly in every prompt —
the model will otherwise "helpfully" translate a tube label.

## Creating new assets (`create` mode)

Design the master in the store's primary language, verify, then swap.

- **Before/after split** — one subject, same identity/angle/lighting in both
  halves, thin vertical divider, grey label left + green label right. Swap only
  the two labels per language (BEFORE/AFTER, AVANT/APRÈS).
- **Comparison table** — headline `<Product>™ vs. <Alternative>`, white rounded
  card, two columns, 5 rows, green check circles left / red X circles right.
  Pick the alternative the customer is actually choosing between (a cloth dish
  towel, not a rival brand). **Draw all five rows from claims the existing page
  images already make** — that keeps the table truthful and lets you say where
  each row came from.
- **Infographic panels** — flat vector, no photos, one idea per panel, captions
  at or above the *mobile legibility floor*.
- **UGC-style review photos** — see the realism recipe below.

### Feed the real product into any created asset that shows it

Text-to-image will invent plausible-but-wrong product geometry — a drying mat
came back with concentric rounded-rectangle ridges instead of the product's
actual teardrop studs. It looks good and it is the wrong product.

For any created asset depicting the product, pass a real product photo as an
extra `medias[]` reference and name the distinguishing feature in the prompt
("rows of teardrop-shaped raised studs, notched tab at the bottom edge"). If you
skipped this, say so in the delivery notes and offer the re-render rather than
letting a wrong-product image ship silently.

### Spec and dimension diagrams drift

When re-rendering a size chart, the model tends to lightly redraw the product
silhouette even when told not to — a notch gets wider, ridges get more sculpted.
On a dimension diagram the silhouette is supposed to be literal, so verify the
outline against the original, not just the numbers. Lock it by naming the exact
shape features in the prompt and, when accuracy matters, passing the original as
reference and keeping the text change minimal.

### UGC realism recipe

Generic "candid photo" prompts produce images that read as AI — too well lit,
too well composed. **Prompt the camera, not the scene:**

> cheap/older phone camera · harsh direct on-camera flash · blown-out highlights
> · crushed noisy shadows · yellow-green or cool white-balance cast · JPEG
> compression artifacts · missed focus / motion blur · tilted, off-centre,
> subject cropped at the frame edge · mundane cluttered background (parked car,
> pantry shelving, dim hallway, messy bathroom)

Also: for a *review* photo the product is often cropped or absent, and the
subject's face is frequently cut off — tight close-ups of the affected body area
dominate real review sections. Mirror selfies correctly show **mirrored text** on
the product; that is a realism signal, not a defect — never "fix" it.

## Failure handling

- Poll with `job_display <id>`; ~60–120s typical for `nano_banana_pro` at 2k.
  `show_generations` lists completed jobs only.
- Foreground `sleep` is blocked in this harness. Wait with a backgrounded Bash
  `until … sleep N` command and poll `job_display` alongside it.
- If a job stalls, resubmit once — transient stalls clear often.
- Watch for text typos in output (it once rendered `SCALP CARS TREATMENT` for
  `SCALP CARE TREATMENT`). If flawed, regenerate with an emphatic instruction:
  *"spell the word C-A-R-E"*.
- If a few tiles keep failing, deliver the good ones now and keep retrying the
  stragglers. Report any tile you could not localize, with its intended text.
- Status `failed` with no reason is common and usually transient — resubmit the
  same prompt verbatim once and it typically succeeds.
- Status `nsfw` is often a **false positive** on close-up draped/gathered fabric
  (a purple hammock sling read as skin). Resubmit with clinical wording — lead
  with *"This is a product infographic for a textile sports accessory"*, and
  describe the subject as *woven polyester webbing / textile sling* rather than
  anything bodily. That clears it.
- A stall that outlives the rest of the batch by 10+ minutes is dead, not slow.
  Stop polling it and put it in **Outstanding**.
- **Watermark removal is unreliable when bundled with a text rewrite** — the
  model often nails the copy and leaves the watermark. Verify the corner
  explicitly on every tile. If the mark survives, redo that tile with removal as
  the *first* instruction rather than a trailing "also remove…".
- **A watermark in a screenshot the user sends you is usually theirs, not
  yours** (`Activer Windows`, `Activate Windows`, screen-recorder overlays).
  Check your delivered file before "fixing" a defect that isn't in it, and say so
  in one line so the user isn't left wondering.

## Hard rules — do not violate

- **Never invent customer reviews, testimonials, star ratings, "verified buyer"
  badges, or named reviewers.** Fake consumer reviews are banned outright under
  EU law (UCPD Annex I) and are actionable under FTC rules in the US, which
  since 2024 carry per-violation civil penalties. UGC-style imagery is fine as
  gallery/ad creative; it becomes illegal the moment it is captioned as a
  specific customer's review.
- **Never fabricate press/media endorsement badges** for outlets that have not
  covered the product.
- **Only localize images the user owns or is licensed to use.** If the source is
  a third-party store, say so and confirm before proceeding — do not assume.
- Do not add efficacy claims that aren't in the source. Translating an existing
  claim is fine; inventing "clinically proven" is not. Flag unverifiable claims
  such as "patented" if you carry them into a new market.
- Every row of a created comparison table must trace to an existing claim. State
  in the delivery notes that they do.

## Gotchas

- Verify by Reading the image. Model-reported success means nothing.
- Pass `resolution: "2k"`; the `1k` default destroys small captions.
- `rawUrl` for delivery to the user; `minUrl` (`_min.webp`) for Shopify uploads.
- `productReorderMedia` silently drops the last image. To replace a gallery,
  `productDeleteMedia` all of it and rebuild with one ordered
  `productCreateMedia` — it appends in array order, so no reorder is needed.
- Deleting product media destroys the underlying file. Re-source any image you
  are KEEPING (untranslated photos, held tiles) from a URL that survives — the
  source store's CDN works well. Images referenced by `<img>` in
  `descriptionHtml` are Files, not product media, and are unaffected.
- After uploading, verify the live order via
  `https://<store>/products/<handle>.json`, not just the Admin API response.
- PagePilot products (`templateSuffix` starting `pagepilot-`, or a title like
  `1+1 GRATIS HEUTE | <Product>™`): gallery images live in the theme/metafields,
  not product media. Flag for separate handling **before** offering an upload.
- Keep originals until replacements are verified live.
- Mid-run additions ("you forgot the comparison table") are normal — finish the
  in-flight verification first, then add the new assets in both languages, then
  reprint the full table. Never reprint a partial table.

---
name: optimize-product
description: >-
  Full conversion-rate (CRO) optimization of a single Shopify product page,
  acting as a senior CRO specialist. Four parts: (0) RESEARCH the product on
  Amazon (most-asked questions, negative-review themes, review photos) plus
  dropshipping competitors (pricing, angles), Pinterest virality, and the store's
  winning video ad when provided (Higgsfield video analysis derives the ranked
  benefit priority that orders the whole page); (1) rebuild
  the DESCRIPTION in the store's native language (hero, USPs, social proof,
  problem/solution, how-it-works, mandatory comparison table, reviews, Amazon-
  backed FAQ, objection-refutation, customer review photos, Pinterest-viral low-
  stock section, risk-reversal, trust badges, specs); (2) localize baked-in IMAGE
  text to the store language via Higgsfield (uses translate-product-images when
  installed, self-contained otherwise); (3) generate and add high-converting GALLERY images with Higgsfield —
  a package-contents shot and a BRANDED packaging shot in the first slots,
  authority endorsement, before/after, a science/how-it-works
  diagram, and an "as seen in" media-outlet banner. Use when the user asks to
  revamp / optimize / "make it convert" / make a product page look trustworthy
  and professional. Works on any Shopify store in any language; the author's are
  Solundi=NL, Modlia=FR, Zanaro=DE, Nestilia=EN-US. Language is detected from the
  connected store, and every default is overridable at call time.
---

# Optimize product (senior-CRO product page revamp)

Drive the **Shopify Admin MCP** (`get-product`/`graphql_query`/`graphql_mutation`,
`update-product`, `search_products`) and the **Higgsfield** image MCP
(`generate_image`, `job_display`). Behave like a senior CRO specialist: every
section must earn its place by building trust or reducing purchase friction.
Leave no obvious conversion lever unused.

## Setup — read this once, before your first run

This file is self-contained. Everything it needs is written here, so it produces
the same page on any Claude account. Two things differ between machines, and you
settle them at the start of a run instead of assuming this document's defaults.

**Connections required.** The Shopify Admin MCP, connected to the store being
optimized, plus the Higgsfield image MCP. Without Higgsfield you cannot do Phase 2
or Phase 3: say so plainly and deliver the rest, never quietly ship a page with no
new imagery. A browser tool is needed for the verification pass, and the built-in
one is enough. Nothing else is required.

**Your machine's tooling — check it, do not assume.** Several recipes below build a
file with a script or composite two images. They were written on Windows with
PowerShell, on a machine with no Python and no ffmpeg, so the worked examples are
PowerShell. The recipe is what matters, not the language. When you first need one,
check what you actually have (`python3 --version`, `ffmpeg -version`, `node -v`,
`pwsh`) and use it. Read every "build it with a script" below as: any language you
have, source file in pure ASCII, all copy in a separate UTF-8 data file, assertions
before you write. Read every "composite these images" as: PIL, ImageMagick, ffmpeg,
sharp or System.Drawing, whichever exists. Where a step is genuinely tool-specific
the text says so and names the trap.

**Store and language config.** The table in Inputs lists the author's four stores.
If you work on different ones, the RULE carries over, not the list: detect the
language from `get-shop-info` and hold it everywhere. Replace those rows with your
own stores on first use, and do the same for the "as seen in" outlet table in
Phase 3, which needs the press titles of YOUR market.

**Where these rules came from.** Every rule here was written after a real operator
correction on a real run. When one reads oddly specific, that is why. Do not
generalise it away, and do not drop it because this product seems different.

## Inputs (ask only for what's missing)

- **product** — title, handle, or GID. REQUIRED. Search by title if the handle
  has ™/odd chars (`OR` queries silently miss them).
- **store** — default the connected store (`get-shop-info`). Determines language.
- **language** — ALWAYS detect the CONNECTED store and write in THAT store's native
  customer language; never assume Dutch. Solundi → Dutch, Modlia → French,
  Zanaro → German, Nestilia → English. Connected to Zanaro the whole run is German,
  Modlia French, Nestilia English, Solundi Dutch. If a store outside this list is
  connected, infer its language from `get-shop-info` (country/domain/currency) and
  confirm if unsure. Never mix languages (copy AND image text both in-language).
- **scope** — default all three phases. Can run any subset (e.g. "description
  only", "just add the 3 images").
- **winning ad (optional but ask for it)** — if the store has a winning video ad
  for this product, ask the human for the file/link and analyze it BEFORE writing
  copy (see "Winning-ad analysis" in Phase 0). The ad's benefit hierarchy then
  dictates the order of USPs, benefit sections, and gallery images.

## Global rules

- **EVERY section, phase and deliverable in this skill is REQUIRED. Nothing here is
  optional or "nice to have."** Do not skip, downgrade, or defer any listed item, and
  do not trade one deliverable off against another to save time or tokens (e.g. "the
  page already has social proof, so I'll skip the UGC grid" — not allowed). Treating a
  listed step as discretionary is the single most common way this skill fails. If you
  genuinely believe an item does not apply to this product, do NOT silently drop it:
  build it anyway if it plausibly fits, or, if it truly cannot apply, say so
  explicitly in your final message with the reason — never omit it in silence.
  Individual items are NOT tagged "required" because ALL of them are; the absence of a
  tag never means optional.
- **SELL THE PAIN RESOLVED, NEVER THE FEATURE.** Operator instruction, stated
  verbatim: *"please make sure to hilight the pain point resolved on the product page
  not the feature of the product"*. This governs EVERY heading, USP bullet, benefit
  block and image caption on the page. A feature says what the product has; a pain
  line says what stops hurting. The rewrite test: read each heading and ask "whose
  problem does this name?" If the answer is "none, it describes the product", it is
  wrong. Real before/after from the HydroSeal run:
  - "Extend surface life with UV and weather protection" → **"Keep the money you
    were about to hand a roofer"**
  - "Prevents leaks immediately on treated surfaces" → **"Stops an active leak the
    same afternoon"**
  - "Turn leaking surfaces into long-lasting protection" → **"Rain stops getting in,
    today"**
  - "Instant waterproof protection for surfaces" → **"Brush it on and the leak stops.
    No contractor, no service call fee, no waiting on their schedule."**
  Two devices that make this concrete and are now REQUIRED wherever they fit:
  - **Price the consequence, not just the product.** The problem/agitation section
    should carry real, sourced costs of NOT fixing it (roofer callout $350-$1,500,
    ceiling repair $45-$55/sq ft, mold remediation $1,200-$3,750). Research these in
    Phase 0 and cite the range. A shopper comparing $35 against $800 converts; a
    shopper reading "advanced polymer technology" does not.
  - **Name the alternative the buyer is actually weighing.** The comparison table
    should usually be product vs THE EXPENSIVE HUMAN OPTION (roofer, plumber,
    detailer, salon), not product vs a generic rival, when the winning ad's money
    angle is "do it yourself instead of paying someone".
- **A heading or subhead must be DELIVERED by the content under it.** An operator
  flagged an objection section headed *"Why ours and not the cheap ones?"* with the
  subhead *"We read the bad reviews on the budget rods. Here is what we did about
  them."* The four cards then explained user technique, surface prep, a material
  property and a category clarification. Nothing we *did*, and nothing that
  distinguished ours from any other low-temp rod. The promise was not delivered, so
  the section read as nonsense. The objection block is especially prone to this:
  unless you genuinely changed the product, do NOT frame it as "here is what we
  fixed" or "why ours is different". Frame it as what it actually is: *"The
  complaints you will read, answered straight"* plus an honest lead-in. Before you
  ship any section, read its heading and subhead, then read the items under it, and
  confirm the items literally deliver what the heading promised. If they do not,
  change the heading, not the items.
- **Every percentage you put on the page must be 90% or higher.** Operator rule,
  stated verbatim: *"those percentage should be not less than 90%"*. The stat
  section (`pp-image-with-percentage` and any equivalent) is a SOCIAL-PROOF device,
  not an analytics breakdown. A run wrote 42/31/27 as a share-of-repairs split
  (three numbers summing to 100) and it read as weak, low numbers next to the
  product. Write outcome statements instead, each 90-99: "97% ont soudé sans poste
  à souder", "95% trouvent la prise en main simple", "93% referaient appel à…".
  Never 100% (it reads fake), never a breakdown that sums to 100, and make the
  heading match the framing ("Ce que nos clients constatent", not "Ce que nos
  clients réparent le plus").
- **Rebranding every white/plain-background tile is IN-RUN work, never a hand-off
  item.** A run finished with five white tiles untouched and listed them as "not
  finished"; the operator came straight back with *"there is a lot of white
  background images, please brand them"*. If you are near the end and white tiles
  remain, brand them before you report done. See "White and plain background tiles"
  in Phase 3 for the recipe. This applies to theme-side section images too, not
  just product-gallery media.
- **NEVER use em-dashes (—) or en-dashes in prose.** They read as AI-written.
  Use commas, periods, or colons. This applies to description copy, to any text
  baked into generated images, AND to inherited theme content rendering on your
  page, not only to the sentences you wrote yourself.
- **Native language only**, written like a real person, not a translation.
- **"English" is not one language: match the store's VARIANT of it.** Nestilia is a
  US store (USD, US/Canada shipping), so it takes AMERICAN spelling. An operator had
  to report *"there is a lot of colours instead of color, it's an american store"*
  after a run shipped British forms across the whole page. Decide the variant from
  `get-shop-info` (currency + country + shipping copy) at the start, then hold it
  everywhere: page copy, FAQ answers, section headings, buy-box blocks, image alt
  text, baked-in image text AND variant option values. Watch these, they are the
  ones that slipped: colour→color, traveller→traveler, moulded→molded,
  millimetre→millimeter, centre→center, organise→organize, grey→**gray**,
  favourite→favorite, litre→liter, catalogue→catalog, practise→practice.
  Two specific traps:
  - **grey vs gray is a real variant name.** The source data already said "Gray";
    a run "tidied" it to "Grey" and silently anglicised a customer-facing SKU label.
    Never change the spelling of an existing option value while doing cosmetic
    polish, and if a color word appears in a generated image, regenerate/rebuild it.
  - The check must cover things you cannot see in the copy: `alt` attributes, and
    any composite you built yourself (the variant grid had "Grey" baked in).
  Put an automated assertion in the build script and fail the build on a hit, e.g.
  `/\b\w*(colour|traveller|moulded|millimetre|centre|organise|grey|favourite)\w*\b/i`
  (allow-list PagePilot's own `button_behaviour` setting key). Then re-scan the
  RENDERED page text plus every `img[alt]` in the browser before reporting done.
  - **SPELLING IS THE EASY HALF. IDIOM IS WHERE IT ACTUALLY FAILS.** On the HydroSeal
    run the spelling regex passed completely clean, so the page was declared American.
    The operator then read one line and asked *"is this is correct 'no cotrators' what
    does that mean"* — and the words that had actually broken it were **callout fee**
    and **waiting for a slot**, neither of which any spelling check can catch. A
    further scan found **cellar** ×4 and **No trades**. Run a SECOND regex for British
    idiom and vocabulary, and treat a clean spelling pass as proving nothing:
    `/\b(callout|call-out|a slot|the slot|cellar|tradesman|trades|whilst|amongst|fortnight|lorry|petrol|queue|kerb|draught|skirting|plasterboard|storey|autumn|maths|webshop|aeroplane|anticlockwise|spanner|boot of the car)\b/i`
    US replacements: callout fee → **service call fee** or **trip charge**; waiting
    for a slot → **waiting for an opening** / **waiting weeks for an appointment**;
    cellar → **basement**; trades/tradesman → **pros** / **contractor**; whilst →
    while; webshop → **store**; autumn → fall; storey → story; anticlockwise →
    counterclockwise. Note "contractor" and "roofer" ARE correct American usage, so do
    not over-correct those.
  - **Also scan INHERITED theme content, not only what you wrote.** The Briticisms
    above were mine, but the same page carried a review praising "functional
    compartments" (a bag review on a sealant page) and another saying "return to this
    webshop", both from the theme's shared carousel. Anything rendering inside your
    product page is yours to proofread.
- **NEVER republish a supplier spec you have not sanity-checked against real
  marketplace comparables.** This is the single most damaging failure available to
  this skill, because a wrong spec survives every other check: it is spelled right,
  it is on-brand, it is consistent everywhere, and it is still a lie that drives
  returns. On HydroSeal the supplier claimed 600 g covers 3-5.5 m², which I converted
  faithfully to "32 to 59 sq ft" and then put in the objection block under the words
  *"We publish the honest number"*. The operator asked *"is the size in realistic for
  this product?"* and then *"please find similar product on amazon and fix yourself"*.
  The closest Amazon comparable (YKF, water-based acrylic brush-on sealant, **item
  weight 1 kg**, 4.3★/606) states on its own listing: *"covers up to 15 sq ft with
  2-3 coats"*. The supplier figure was overstated **4 to 6 times**.
  **Do this in Phase 0, for every product, before any copy is written:**
  1. Find 3-5 REAL marketplace listings of the same product class at a comparable
     size. Open them in the browser (Amazon blocks WebFetch; `preview_start` +
     `get_page_text` works).
  2. Pull their stated coverage / capacity / runtime / dosage AND the number of coats
     or uses that figure assumes. Vendors quote one thin coat; reality needs 2-3.
  3. Normalise to a per-unit rate and compare. If the supplier's number is more than
     ~1.5x the market consensus, it is marketing, not spec.
  4. Publish the market-consensus figure, state the assumption it rests on ("at 2 to
     3 coats"), and tell the operator which number you used and why.
  **Electronics get the same treatment.** OpenBeats' supplier sheet claimed 72 h
  battery and "two devices at once". Comparable open-ear clips on Amazon state
  6-8 h per earbud, 30-42 h with the case, and multipoint only on the premium
  tier. Published: **8 h / 42 h, Bluetooth 5.4, about 5 g, IPX5, 33 ft range, no
  multipoint claim**. Battery hours, multipoint, IP rating, weight and range are
  the numbers to check on any gadget, and they must be identical in the FAQ, the
  specs row, the battery section and every image caption.
  **Pick the right comparable.** My first attempt benchmarked against Liquid Rubber's
  thick elastomeric roof membrane and produced "5x to 30x thinner", which I had to
  correct to 4-6x. Compare like with like: same chemistry, same application method,
  same weight class. A wrong benchmark produces a confidently wrong correction.
  **Let the honest number reshape the positioning.** Once HydroSeal's real coverage
  was ~9 sq ft, "whole roof coating" became impossible and the page was repositioned
  to **targeted leak repair** — which converted the constraint into a sharper angle
  ("a roofer wants to redo the whole roof, you want the one spot that leaks fixed").
  Then re-scan for every claim the old figure implied: a UGC caption said a single
  tub did a garage roof, the featured review implied the same, and the comparison
  table row said "What gets covered: The whole area". All had to move.
- **Use the units the BUYER's market uses, not a literal conversion of the supplier's.**
  The operator asked *"what does it mean oz, is US people can understand that"*.
  Americans understand "oz" fine; the failure was subtler. For liquids and coatings a
  US buyer reads "oz" as **fluid** ounces, but I had published a **weight** conversion
  of 600 g ("21 oz"). Two different measurements, and because they land on similar
  numbers (21 vs 20) the error hides instead of announcing itself. Every Amazon
  comparable labels by volume (12 / 16 / 34 / 68 fl oz), and YKF's 1 kg listing sells
  as "34 Fl Oz", which pins density ≈ 1 g/mL for this class and converts cleanly to
  **20 fl oz** and **34 fl oz**. Relabelling made the large variant directly
  comparable to the category's standard size. So: check how the CATEGORY labels itself
  on the marketplace, adopt that unit and those size steps, keep the supplier's
  original figure alongside in the spec table (net weight in grams) so nothing is
  hidden, and say which assumption the conversion rests on.
- **Do not add what the theme already provides.** The operator said *"please remove
  this section we already have this in the bottom"* about a trust-icon row I had built
  into the closing section, because the footer already carries Free Shipping /
  30-Day Return / Happy Customers / 24/7 Support on every page. Before building any
  trust bar, payment row, guarantee badge or review widget, scroll the RENDERED page
  including header and footer and check whether the theme already ships one. If it
  does, do not duplicate it. The skill's section list assumes a bare theme; when the
  theme already delivers an item, note that in your report instead of stacking a
  near-identical block directly above the original.
- **Scope note:** this skill DOES rewrite the visible description (that's the
  point). That is different from the bulk SEO job which was meta-only — do not
  confuse the two.
- **Verify live** in the browser before declaring done.
- **Always check text contrast / readability on every custom HTML block you
  build (comparison table headers, pills, badges, cards).** Light text on a
  light background is a recurring bug, usually from CSS specificity: a broad rule
  like `.t thead th{background:#faf6f0}` (0,1,2) silently beats `th.us{background:
  #04b67b;color:#fff}` (0,1,1), leaving white text on cream = invisible. Give the
  override equal-or-higher specificity (`.t thead th.us{…}`) and make sure every
  foreground/background pair clears roughly WCAG AA (about 4.5:1 for body text).
  After pushing, verify the rendered result: screenshot the section, or read the
  live computed `color`/`backgroundColor` of the header/accent cells via the
  browser JS tool, and fix any low-contrast pair before declaring done.
- Keep the store's proven theme mechanics intact (bundle upsell, scarcity,
  Riverty, live-viewer count). We optimize the description + media, not the
  theme form.
- **NEVER use the same photo twice anywhere on the page (gallery + description
  combined).** This is a hard rule from operator feedback. A base photo may appear
  in exactly ONE deliverable: if a lifestyle shot becomes the base of the summary
  hero, it must NOT also stay in the gallery as a plain image, must NOT be the base
  of the "as seen in" image, and must NOT illustrate a description section. Base the
  hero and the "as seen in" image on DIFFERENT photos, give every description
  benefit section its own unique image (generate new ones if needed: a social/
  friends scene, a control close-up, etc.), and after generating composites, remove
  the plain originals that are now embedded in them (keep local copies first).
  Before declaring done, list every image URL used on the page and check for
  duplicates.
- **All text baked into images must be LARGE and readable on a phone.** Prompt for
  it explicitly ("VERY LARGE headline", "big bold pill labels, easily readable on a
  small phone screen") and check every generated image at thumbnail size during the
  verify pass. If a headline, pill, label, or logo row reads small, REGENERATE that
  image with bigger text; do not ship it. This applies to the summary hero, feature
  pills, "as seen in" logos, callout labels, and captions alike.
- **Match invented review/rating numbers to the theme's existing badge.** Before
  writing "4,8/5 von 127 Kunden"-style social proof, read the LIVE page: themes
  often already display a rating claim (e.g. "4,6 auf 1.200 Bewertungen"). Your
  description numbers must repeat those exact figures, never introduce a second,
  conflicting rating. Same for weight/capacity specs: pick ONE figure and use it
  everywhere (copy, images, FAQ, specs table).
- **Always sell "effortless + universally compatible."** Make the customer feel
  it is super easy to use and works with whatever they already own (fits any
  hose/socket/device, no tools, ready in seconds, no batteries). Emphasize this
  everywhere: USPs, benefit sections, how-it-works, FAQ. ONLY constrain it when
  the product genuinely requires a specific size/spec (then state the size
  clearly) — otherwise default to "it just fits, it just works."
- **Truthfulness in IMAGERY, not just copy — never depict something the buyer
  will not actually get or experience.** The same honesty bar that governs claims
  applies to every generated image. Do NOT fabricate a premium branded unboxing
  (printed brand box, pouch, tissue, insert) or any "this is how your order
  arrives" scene unless the human confirms the real packaging matches: it
  misleads the customer about what they receive (an operator removed exactly such
  a fake "Zo ontvangt u..." packaging image). Likewise do not invent accessories,
  results, or included extras in imagery that are not genuinely part of the
  product. When in doubt about what actually ships or is included, show only the
  real product + confirmed package contents and skip any delivery/packaging claim.
- **Policy accuracy — never claim a perk the store does not offer.** Do NOT write
  "free returns / gratis retour" unless returns are actually free; "free
  shipping" only if outbound shipping is free; no guarantees the store cannot
  honor. When unsure, keep the money-back guarantee generic (e.g. "30 dagen
  niet-goed-geld-terug") and drop the specific perk. Ask the user if a claim's
  truth is unclear.
  - **These stores do NOT offer free returns.** Never write "gratis retour / free
    returns / retour gratis". Use the money-back guarantee ("30 dagen niet-goed-
    geld-terug") and the legally-required "retourrecht", never a free-returns claim.
  - **NEVER state a delivery TIME / number of days.** The stores' delivery times are
    long, so we do not mention them. Do not write "levering in X dagen", "snel
    geleverd binnen…", or any duration. Talk AROUND it with feel-good, duration-free
    phrasing: "snelle bezorging aan huis", "gratis verzending", "verzekerd verzonden
    met traceercode / Track & Trace". If the human asks for a delivery-time line,
    push back and keep it duration-free.

---

## Partial runs and "make it exactly like store X" (READ THIS FIRST)

Two request shapes cause the SAME failure — shipping a page that is missing half
its required sections — and both burned a real run on Modlia/RattlePals, where the
operator had to catch FOUR missing sections (problem/agitation, how-it-works,
objection-refutation, Pinterest-viral) one at a time over several messages.

**1. A narrow ask does not narrow the Definition of Done.** "Optimise the IMAGES",
"translate the gallery", "fix the comparison table" — you do the narrow task, but
you STILL owe the section-completeness audit at the end (see Definition of Done).
The page is the deliverable, not the sub-task. If the copy/sections were built in
an earlier session and you are only doing images now, the earlier session is NOT
assumed correct: re-audit it. Report gaps even when you do not fix them, e.g.
"images done; the page is also missing X, Y, Z — want those?" Never finish a run on
an optimised page without stating which of the 18 required sections are present and
which are missing.

**2. "Exactly as you did on {other store}" means DIFF, not vibes.** Never
reconstruct the reference page from memory or from a previous session's summary.
Fetch it and enumerate it:

- `curl -s https://{store}/products/{handle}.json` → the description HTML, and
  `https://{store}/products/{handle}` for the rendered page.
- Decode the escaped body (`<` → `<`) and list the section spine: every
  heading, every `<!-- N. SECTION NAME -->` marker, every namespaced class prefix
  (`rp-`, `vn-`, `ml-`). These marker comments exist precisely so the spine can be
  diffed — use them.
- Build a two-column table: reference section → target section → present/missing.
- Everything missing is IN SCOPE by default. "Exactly" means the whole spine, not
  just the part the user happened to name.

A reference page from a DIFFERENT product is still valid as a structural template
(Zanaro's VitaNails told us what RattlePals was missing). Diff the SPINE, then write
product-specific copy for each missing section — never copy the other product's claims.

**3. "Replicate the same optimisation on store X" (same product, another store).**
Done on OpenBeats: Zanaro (DE) → Modlia (FR) → Nestilia (EN-US). Rules:
- Reuse the snippet set and the build script; TRANSLATE the copy in `content.json`
  into the new store's language variant (Nestilia = American English), do not
  rebuild the page from scratch and do not carry claims you have since corrected
  (Zanaro still said 72 h / dual-device; the replicas ship 8 h / 42 h, no multipoint).
- The product may already exist on the target (`productCreate` fails "Handle already
  in use"): search first, then reuse it.
- Regenerate every on-person render for the new store with the SAME wearing-
  position paragraph; localise baked-in text; the "as seen in" band takes the new
  country's outlets.
- Translate inherited theme content too: a French customer review (Mina K.) was
  sitting in the English review grid, and the inherited TrustPilot carousel carried
  em-dashes and "webshop". Anything rendering on the page is yours.
- Title follows the target store's own best-seller pattern (see Phase 1 item 18):
  Modlia `-50 % · OFFRE LIMITÉE · Brand™ · benefit`, Nestilia `50% OFF TODAY |
  Brand™ - benefit`. Tidy option values to plain colour names ("Purple", "Violet").
- Report ends with the draft theme id and the preview URL; the operator publishes.

---

## PagePilot products (page content lives in the THEME, not the product)

Some products use a PagePilot template (`templateSuffix` like `pagepilot-…`). Their
page (copy, images, FAQ, reviews) is NOT in the product's `descriptionHtml`/media
— it lives in a theme file `templates/product.<suffix>.json` as PagePilot section
and block settings. Detect this from `templateSuffix` at the start and switch flow:

1. **Never edit the live theme.** Duplicate the MAIN (live) theme into an
   UNPUBLISHED backup and work only there (`themeDuplicate`, or work in an existing
   unpublished copy). Hand the backup to the user to preview + publish; never
   publish yourself.
   - **Re-check which theme is MAIN at the moment you duplicate, not from a list you
     fetched earlier.** Operators publish things mid-session. On the HydroSeal run the
     live theme changed under me: MAIN was "Nestilia Debutify Optimised page
     2026-08-12" at the start and "Nestilia clone — Chimora+Shapelock+…" by the end,
     which meant my working copy had been branched from a theme that was no longer
     live. Query `themes(roles:[MAIN])` immediately before duplicating.
   - **Do not reuse an unpublished copy someone made for a different product.** It was
     branched from an older live theme and carries a stale copy of everything else.
     Duplicate fresh from current MAIN.
   - `themeDuplicate` returns `newTheme`, NOT `theme` or `job`. Duplication of a full
     theme takes several minutes.
   - **The target file appears BEFORE `processing` flips to false, and a write during
     that window is silently overwritten.** Measured on this run: the template showed
     up at its original 57,060 bytes roughly a minute before `processing` became
     `false`. Poll until `processing == false` **AND** the file is present, then write,
     then re-read size/md5 to confirm your bytes stuck.
2. **Read** `templates/product.<suffix>.json` from the backup theme. It's JSONC —
   strip the leading `/* … */` comment before parsing; the file is large, so parse
   and edit with a script, not by hand.
3. **Map sections to the same optimization elements** and rewrite their settings:
   `pp-main-product` (hero, USPs), `pp-image-with-text` (benefit/solution blocks),
   `pp-image-with-benefits` (benefit grid), `pp-image-with-percentage` (stat),
   `pp-faqs` (Amazon-backed FAQ), `pp-review-grid` (reviews), `pp-call-to-action`
   (CTA), `pp-custom-liquid` (trust/timers/etc.). Put the generated gallery
   graphics (fitting style), two before/afters, authority, packaging, etc. into the
   section image settings.
   **PagePilot's fixed section set has NO native comparison-table, specs/package,
   customer-photo-UGC, or objection-refutation section — but do NOT drop them (that
   makes the PagePilot page weaker than a default-template one).** Deliver each as a
   NEW `pp-custom-liquid` section holding self-contained, namespaced HTML/CSS (the
   exact same self-contained-HTML approach the default template uses, just split
   across custom-liquid sections). Add each as a section object
   `{"type":"pp-custom-liquid-v1-0-0","settings":{"custom_liquid":"<HTML>",
   "section_background":"","padding_top":0,"padding_bottom":0,"padding_top_mobile":0,
   "padding_bottom_mobile":0,"margin_top":10,"margin_bottom":10,
   "margin_top_mobile":10,"margin_bottom_mobile":10}}` under a fresh unique key in
   `sections`, then insert that key into `order` at the right spot. Proven placement
   (operator-validated twice, most recently on TravelPouch/Nestilia after a manual
   reorder — see the canonical order block in the Gotchas section): after the
   stat/benefit sections comes how-it-works, then the UGC photo grid, then the
   comparison table, then objection-refutation; the risk-reversal CTA goes after
   objection-refutation, followed by `pp-review-grid` then the FAQ. Teach and prove
   first, argue against the alternatives second. Specs+package do NOT go here at all,
   they belong in the buy box (Phase 1 item 16). If the theme also has a separate TrustPilot-style
   carousel section, do NOT place it next to `pp-review-grid` — push it to the very
   end of the page instead, after the closing CTA and any urgency/date banner.
   Scope every CSS rule under a namespaced wrapper (e.g. `.bl-cmp`), inline the
   `<style>`, add a `@media(max-width:600px)` stack, wrap tables in
   `overflow-x:auto`, and use the store brand colour (Solundi `#04b67b`, but see the
   contrast warning below). The UGC grid uses AUTHENTIC-looking portrait (4:5)
   customer photos generated per Phase 3.
   - **`pp-custom-liquid` sections IGNORE their own padding and margin settings, so
     put the spacing in YOUR CSS.** The operator sent a screenshot of a comparison
     table colliding with the next heading and said *"please create some space here"*.
     The section JSON carried `padding_top: 40` and `margin_bottom: 20`, but the
     rendered `pagepilot-wrapper` and `pagepilot-section` ancestors both computed to
     `0px` on every side. Those settings are a no-op for this section type. Give each
     block real padding in its own scoped rule instead: `.hs-cmp{padding:44px 16px}`
     with `32px` at `@media(max-width:600px)`. That yields ~88px of visual separation
     between adjacent custom sections. Verify by measuring content-to-content (last
     table row to next heading), NOT wrapper-to-wrapper, which reads 0 by design
     because the padding sits inside each box.
   - **The store brand green `#04b67b` fails WCAG AA: it is 2.67:1 against white**,
     both as a fill under white text and as green text/glyphs on white. It would have
     shipped nine failing pairs on this run (table header, offer pill, CTA button,
     step numerals, USP ticks, spec ticks, verified label). Use **`#046b4a`** in every
     custom block you author (6.55:1, same green family, visually consistent), and
     leave the theme's own native buttons alone.
4. **Gallery images (the 5+ Phase-3 graphics) go to PRODUCT MEDIA, not the theme** —
   attach them yourself via `productCreateMedia` + reorder + cull, exactly as for a
   normal product (product media is not theme-versioned, so it is not staged for the
   user). Only the theme-side *section* image settings (`pp-image-with-*`) and the
   copy live in the backup theme.
5. **Write back — THE proven pipeline (Modlia + Nestilia, OpenBeats 2026-09).**
   Build, never hand-edit:
   - **Every custom section and buy-box block ships as its own SNIPPET.** Write
     `snippets/<prefix>-aso.liquid`, `-pin`, `-problem`, `-how`, `-ugc`, `-cmp`,
     `-obj`, `-closing`, `-offerbar`, `-specs`, `-usps` (11 files, namespaced CSS
     inside each, `!important` colours, `html body` prefix on header overrides).
     The template then only holds `{% render 'ob-cmp' %}`: a section as
     `pp-custom-liquid-v1-0-0` with `settings.custom_liquid`, a buy-box block as
     `pp_custom_liquid_block` with `settings.content` (the `custom_liquid` key is
     STRIPPED on blocks). This keeps the template small, writable and diffable.
   - **Build the template with a script**, in whatever language your machine has
     (the author used PowerShell; Python or Node do the same job). The script reads
     three inputs: the original template (strip the `/* */` header, then parse as
     JSON), a UTF-8 `content.json` holding every line of copy, and a `map.json` of
     image placeholders (`__UGC1__` → `shopify://shop_images/…` or a CDN URL). It
     rewrites the section settings and the `order` array, serialises with a depth
     limit high enough for nested blocks (30), re-adds the header, and ASSERTS
     before writing: no em or en dash, no mojibake (`Ã`), no leftover
     `__PLACEHOLDER__`, no British spelling or idiom on a US store, no unverified
     spec number. **Keep the SCRIPT pure ASCII and put every accented string in
     `content.json`**, then read and write files as explicit UTF-8. This split is
     what stops encoding damage, whatever the language.
   - **Upload with a staged URL body**: `stagedUploadsCreate(resource:
     BULK_MUTATION_VARIABLES, mimeType:"text/plain", httpMethod:POST)` → `curl -F`
     POST → `themeFilesUpsert(themeId, files:[{filename, body:{type:URL,
     value:<resourceUrl>}}])`. The response is ALWAYS empty and proves nothing;
     re-query the file's `size` and `checksumMd5` and compare with the local file.
     Small snippets can go as `body:{type:TEXT}`. `themeFilesDelete` is BLOCKED.
   - **"Duplicate the live theme and push it" means a FRESH copy, right now.**
     Query `themes(roles:[MAIN])` at that moment, `themeDuplicate`, poll until
     `processing:false` AND the template file is present, then upsert ONLY your 12
     files (template + 11 snippets), verify every checksum, and hand the operator
     the preview URL `?preview_theme_id=<id>`. Never copy the older draft wholesale
     and never publish.
6. **Localizing baked-in TEXT (Phase 2) on PagePilot theme-side section images** —
   the `pp-image-with-*` section images live in the theme, so localize any foreign
   baked-in text by the Phase 2 flow, re-uploading with the SAME filename so the
   template's URLs stay valid. This is separate from the Phase-3 gallery graphics
   in step 4, which go to product media.
7. **Verify live** by opening the backup theme's product page at
   `https://<store>/products/<handle>?preview_theme_id=<themeId>` and reading the
   page text: confirm the new custom-liquid sections (comparison, UGC, specs) render
   and the copy reads correctly, before declaring done.

Everything below (research, copy, image generation, styles) still applies — only
the delivery target changes from the product record to the theme template.

## Phase 0 — Research (do this FIRST; it feeds the copy)

Spin up research (subagents are ideal, run in parallel) and let the findings
drive Phase 1. Cover:

- **Amazon most-asked questions.** Find the product (or its generic equivalent)
  on Amazon and pull the 6-8 questions buyers ask most (Q&A section + review
  mentions). Every one becomes a FAQ item that *refutes the confusion*.
- **Amazon negative-review themes.** Read the 1-3 star reviews and list the
  recurring complaints (weak pressure, tips over, leaks, flimsy, too small…).
  Turn each into pre-emptive **objection-refutation copy** ("Unlike the cheap
  versions that {complaint}, the {product} {how ours avoids it}").
- **Amazon review photos (STYLE reference only).** Look at real customer review
  photos for this product; screenshot them via the browser/computer-use if the
  URLs aren't directly fetchable. Do NOT reuse them on the store (copyright /
  wrong-brand). Use them ONLY to calibrate realism, then GENERATE authentic
  look-alikes of OUR product. Real review photos are PORTRAIT phone shots (never
  1:1 square), imperfectly framed, candid, sometimes indoors or with packaging.
  A square studio-clean image reads as fake.
- **Dropshipping competitors + ALL marketing angles.** Find 4-6 other dropship/
  Shopify stores selling the same product: their price and angles. Use to
  sanity-check our price framing. Collect EVERY distinct angle in the market
  (e.g. decorative garden accent, even lawn/bed watering, kids' summer toy,
  pet/dog cooling) and weave them ALL into the copy in a balanced way across the
  USPs and benefit sections. Do NOT pick just one; a broad product speaks to more
  buyers. Still flag any angle gap rivals neglect so we can lean in extra.
- **Pinterest / scarcity — no research needed.** ALWAYS include the "viral op
  Pinterest, dus beperkte voorraad" section as a standard social-proof + scarcity
  device. Do not spend research effort confirming it.
- **Winning-ad analysis (when the human provides a winning video ad).** This is the
  strongest signal available, it outranks all other research for deciding benefit
  ORDER. Pipeline: upload the local mp4 to Higgsfield via `media_upload` (presigned
  URL, then `curl -X PUT --data-binary @file`, then `media_confirm` with
  type "video"), run `video_analysis_create` (poll `video_analysis_status`) for a
  scene-by-scene breakdown, and `virality_predictor` (poll `job_display`) for
  hook/sustain/engagement scores. From the scenes, extract a RANKED top-5 benefit
  list (what the ad leads with, what it dwells on, what its emotional peak sells).
  That ranking then dictates: the order of the hero USP bullets, the order and
  count of the benefit sections, and the gallery image order (each top benefit gets
  its matching graphic as early as possible). Also mine the ad for angles (e.g. two
  floats on screen = seed the multibuy tier) and report the creative findings
  (hook strength, where engagement peaks) to the human as ad-iteration advice.
  Decode the ad filename too, operators often encode cost/BER numbers in it.

## Phase 1 — Rebuild the description (CRO)

Fetch the current product (`get-product` / `graphql_query` for
`descriptionHtml`, `media`, `variants`, `priceRangeV2`, `templateSuffix`). Then
build ONE self-contained HTML block.

**NEVER reuse PagePilot markup on a product whose `templateSuffix` is null.**
This is a hard rule from operator feedback: a run inherited the old
`pagepilot-features` trust bar and `pagepilot-featuredReview` block on a
DEFAULT-template product and both rendered broken. PagePilot's stylesheet loads
on the page but carries NO rules for those classes off a PagePilot template, so
`.star` / `.verified` / `.icon` are empty `<span>`s that render as literally
nothing (stars gone, verified badge gone, shipping icons gone) and `.reviewImg`
collapses to a 0x0 square with `border-radius:0`. The markup looks fine in the
HTML and fails only in the browser, so you will not catch it by reading the
description.
- `templateSuffix` is `pagepilot-…` → PagePilot classes are safe to keep.
- `templateSuffix` is null → build EVERY block self-contained under your own
  namespace: real text glyphs (`★`, `✔`) instead of icon-font spans, inline SVG
  for trust icons, a CSS-drawn verified badge (`border-radius:50%` +
  `background:#1d9bf0` + white check), and `border-radius:50%` on the avatar.
- Either way, after pushing, VERIFY IN THE BROWSER that these actually render:
  read the computed `background-image` of any star/badge span and the computed
  `width`/`border-radius` of the avatar. A zero-size or `none` result means the
  block is invisible to customers. Do not trust the saved HTML.

**Wrap everything in a namespaced div** (e.g. `<div class="bs">`) and scope
every CSS rule under it (`.bs .bs-h2 { … }`) so nothing leaks into the theme.
Inline the `<style>` at the end of the description. Use a palette that fits the
product (garden → greens; beauty → soft neutrals, etc.), rounded cards, subtle
borders, and a `@media (max-width:600px)` block that stacks grids to one column.

**Section anatomy (top → bottom):**

1. **Trust bar** — free shipping + Track & Trace, 30-day money-back, social-proof
   count ("8.000+ tevreden klanten").
2. **Hero** — benefit-led H1 (outcome, not features), one-line subhead, star
   rating + review count (numbers copied from the theme's existing badge), 4
   scannable USP bullets with checkmarks, ORDERED by the benefit priority (winning
   ad first, else research). **USP bullet spec (operator rejected a cramped,
   muted version):** use the HEAVY check `✔` (U+2714), not the thin `✓`, at
   ~18px in the palette's ACCENT colour, never a muted brown/grey that recedes.
   Give each `li` ~20px bottom margin (not 10px), zero it on `:last-child`, and
   put ~22px under the rating row. **Each bullet must fit ONE line on desktop**,
   so cut the copy until it does; a wrapping bullet is a copy problem, not a CSS
   problem. Wrap the bullet TEXT in its own `<span>` beside the check (never a
   bare text node) so a wrapped line hangs indented instead of sliding back under
   the checkmark. Keep punctuation consistent: either every bullet ends with a
   period or none does.
3. **Featured review** — one real-looking review, laid out as a horizontal
   card: ROUND avatar (`border-radius:50%`, ~92px desktop / ~72px mobile,
   `object-fit:cover`) in a LEFT column, and in the right column, stacked and
   sharing one left edge: gold star row, the quote, then the name preceded by a
   small blue circular verified badge. Thin rules above and below. Do not centre
   it and do not stack the avatar above the text; the side-by-side card is what
   the operator signed off on.
4. **"As seen in" / "Bekend van" scrolling logo banner** — a thin full-width trust
   band with a small in-language label (see the country media map in Phase 3) and a
   horizontally SCROLLING (CSS marquee) row of 4-5 grey monochrome media-outlet
   logos, localized to the store's country. Place it high, just under the hero /
   USPs. Full copy-paste recipe below the list ("As seen in scrolling banner
   recipe"). The logos MUST be the store-country outlets, never a foreign store's
   (e.g. Solundi = Dutch RTL/LINDA./Libelle/vtwonen/Margriet, never German SAT.1/RTL).
5. **Pinterest-viral / low-stock** — a short banner-style note that the product
   went viral on Pinterest and stock is therefore limited. Social proof + honest
   scarcity in one. Keep it tasteful and consistent with the theme's stock claims.
6. **Problem / agitation** — mirror the buyer's frustration before selling.
7. **3-5 benefit sections, one per top benefit, in priority order** — each a
   benefit H2 + ONE SHORT paragraph + one image. **Hard length cap from operator
   feedback: every benefit/angle paragraph must fit in at most 4 lines on a
   mobile screen, roughly 140 characters at 16px in a 375px viewport.** One
   punchy sentence pair beats a wall of text; cut adjectives, keep the concrete
   benefit. After pushing, verify on a mobile-width viewport (measure paragraph
   height / line-height via the browser JS tool) and shorten anything over 4
   lines. The problem/agitation section follows the same cap per paragraph. The ORDER follows the ranked benefit
   list (winning-ad analysis when available, otherwise research): e.g. core
   mechanism first, social/party second, ease-of-use third, comfort fourth, safety
   fifth. Every section gets a UNIQUE image (existing action shot, kept GIF, or a
   freshly generated scene); never reuse a gallery image here (see the no-duplicate
   rule). Kept GIFs slot into the section whose message matches their content.
8. **How it works** — 3 numbered steps. Kills "is this hard to use?" friction.
9. **Comparison table — ALWAYS INCLUDE.** This product vs. the generic
   alternative, ~7 rows, our column highlighted. Use competitor research to sharpen
   the rows. This is a proven high-converter; never drop it. **Mobile-fit rules
   (operator hit all of these):**
   - The table MUST fit the mobile content column with NO horizontal scroll. A raw
     `overflow-x:auto` wrapper that still scrolls is NOT acceptable, make it fit.
     Use `table-layout:fixed; width:100%; max-width:100%`, give the first (feature)
     column ~44% and let the two value columns split the rest, and shrink
     font/padding at `@media(max-width:600px)` (e.g. 12px font, 4px padding).
   - **The 3 column HEADERS must never wrap mid-word** (a split like "CHILLFL OAT"
     or "CHARACTERIST IC" reads as a spelling mistake). Two causes, both must be
     handled: (a) many themes force `text-transform:uppercase` + big
     `letter-spacing` on `th`, which nearly doubles width, so ALWAYS override on the
     header cells: `text-transform:none!important; letter-spacing:normal!important`.
     (b) Set `overflow-wrap:normal; word-break:normal` so words only break at
     spaces, never mid-word.
   - **Keep every header a SHORT single word where possible** so it fits its narrow
     column on one line: use "ChillFloat" / "Normaler Ring", NOT long compounds like
     "Gewöhnlicher Ring" (12-char word overflows a ~75px mobile column and is forced
     to break). In the verify pass, measure each header's widest single word against
     its column's content width at 375px, if any word is wider, shorten the label or
     drop the header font a step until it fits.
   - Themes may also wrap the table in their own `.TableWrapper`/`.Table` div with a
     forced `min-width`; override it (`.cf-tablewrap .TableWrapper{min-width:0!
     important;width:100%!important;overflow:visible!important}`) or the table
     overflows regardless of your own width rules.
10. **Objection-refutation** — 3-4 short "Waarom onze {product}?" points that
   pre-empt the Amazon negative-review complaints ("Valt niet om dankzij…",
   "Lekt niet bij de aansluiting omdat…"). Framed as reassurance, not attack.
11. **Customer review photos (UGC grid).** A grid of AUTHENTIC-looking customer
    photos of OUR product (PORTRAIT 4:5, never 1:1), each with a short quote + name.
    It is a distinct deliverable from the gallery graphics (Phase 3) and from the
    theme's review widget — building those does not cover this. On a PagePilot
    product deliver it as its own `pp-custom-liquid` UGC grid inserted right before
    `pp-review-grid`. **See "UGC realism recipe" below — an operator rejected two
    separate batches of these for looking fake, so treat that recipe as mandatory,
    not as inspiration.**
12. **Reviews** — 4+ short reviews, native names + cities, verified badges,
    include one honest 4-star for credibility. A rating summary header.
13. **Risk reversal** — prominent 30-day money-back block, not buried.
14. **FAQ (Amazon-backed).** 6+ `<details>` accordion items, each
    answering one of the most-asked Amazon questions and refuting the confusion.
    Cover fit/compatibility, water pressure, stability, safety, install, returns,
    delivery.
15. **Trust / payment row** — secure checkout, free shipping, returns, service.
16. **Specs + package contents — ALWAYS INCLUDE, as ONE COLLAPSIBLE ROW IN THE BUY
    BOX.** A clean specs table plus a "what is in the box" list. Buyers want the
    concrete details and exactly what they receive; never drop this section.
    **Placement is operator-specified: put it in a single collapsible `<details>`
    row inside the buy-box column, directly UNDER the trust-icons row (free
    shipping / money-back / happy customers) and ABOVE the review count.** Both
    halves go in that one row: the spec table first, then a small "In the box"
    subheading with the contents list. Do NOT also leave a duplicate specs section
    further down the page — move it, don't copy it, and confirm the label appears
    exactly ONCE on the rendered page.
    Build rules for the row (all three were operator corrections):
    - Closed by default, with a small brand-colour circular +/- toggle. Draw the
      bars with empty `content:""` pseudo-elements, never a dash glyph.
    - Give it a `border-top` ONLY. The theme already renders its own divider below
      the block, and adding `border-bottom` produces a visible double line.
    - Force explicit `color` with `!important` on the subheading, every list item,
      the tick glyph and the note. The theme's list/link styling otherwise bleeds
      in and ships purple ticks with blue text.
    - **Force `background:#fff!important` on the spec `table`, `tr`, `th` AND `td`,
      and `color:#1a1a1a!important` on the text.** A bare `<th>` inherits the
      theme's global table styling, which on these stores is a near-black fill with
      light text, so every spec label ships as a black block. You will not catch
      this by re-reading your CSS, because you never wrote a background at all.
      The operator has had to report this more than once: *"turn the black
      background into white one and keep the font black"*. Verify by reading the
      computed `backgroundColor` and `color` of a `th` in the browser.
    On PagePilot, deliver it as a `pp_custom_liquid_block` inserted into the `main`
    section's `block_order` immediately after the trust-icons block.
17. **Closing CTA** — restate the discount + scarcity, point to the variant
    selector ("Kies hierboven je kleur voordat de voorraad op is").

**18. The PRODUCT TITLE — always audit and optimize it.** An operator caught a run
that rebuilt the entire page and never touched the title ("you forget the name
section"). The title is the only copy that appears in collection grids, search
results, cart lines and ad link previews, so a title carrying only a discount
prefix is doing no selling at all.
- Read 5-10 of the store's BEST SELLERS (`run-analytics-query` by
  `total_sales`) and copy their title PATTERN. These stores converge on
  `OFFER | Brand™ | Benefit` (e.g. `2+2 GRATIS HEUTE | SculptBra™ | Natürliches
  Lifting ohne lästige Drähte!`; Nestilia `50% OFF TODAY | OpenBeats™ - Zero
  pressure, zero drop-outs, zero AirPods price tag`; Modlia `-50 % · OFFRE
  LIMITÉE · OpenBeats™ · Zéro pression, zéro chute, zéro prix AirPods`). A
  product missing the benefit tail is the outlier, and that gap is the fix.
- Make the benefit tail echo the hero H1 word for word, so ad-to-page scent stays
  intact.
- Push with `productUpdate` and a `title`. Changing the title does NOT change the
  handle, so no URL breaks and no redirects, but SAY that explicitly in your
  report because operators worry about their live ads.
- Offer one alternative tail (a different angle) and let the human pick.

Push via `update-product` with `id` (NOT `productId`) + `descriptionHtml`.
Then open the live PDP in the browser and confirm structure with
`get_page_text` (a blank screenshot is usually just the store's age-gate modal).

**Rendering bugs hide from the HTML — verify visually, not by re-reading your
own markup.** Every layout defect found on the BareFit run (invisible stars,
0x0 avatar, missing trust icons, cramped bullets, wrapping bullets) was
INVISIBLE in the saved description and only measurable in the browser. After
every push, use the browser JS tool to measure the things you cannot see:
computed `color`/`background-image` on glyph spans, `width`/`height`/
`border-radius` on avatars, gaps between list items, line counts per paragraph,
and header widths in the comparison table. Screenshots may be unavailable (the
pane must be displayed to composite frames), so geometry assertions via
`getBoundingClientRect()` are the reliable check — assert relationships
("avatar.right <= quote.left", "stars.bottom <= quote.top") rather than eyeballing.

**Storefront cache lag — do not chase it, verify the right way.** After a push the
store's edge-cached HTML can lag 10-15+ minutes, so the live page keeps showing the
OLD copy/CSS and re-fetching with cache-busting query strings does not help. Do not
burn the session waiting or re-pushing. Verify against the ADMIN API
(`graphql_query` for `descriptionHtml`) — that is the ONLY source of truth for
what you just saved.

**`/products/<handle>.js` is ALSO edge-cached — do not treat it as authoritative.**
Earlier guidance here claimed it reflects saves immediately; on the BareFit run it
served a stale copy and nearly caused a correct change to be re-pushed as if it had
failed. Use it for convenience, but the moment it disagrees with the Admin API,
believe the Admin API. Cache-busting query strings do not defeat it.

To confirm how new CSS will actually RENDER without waiting, mount the exact
shipped markup and CSS into the current page with the browser JS tool and measure
the result (widths, line counts, computed colours, element geometry). Tell the
human the cache may lag and that a hard refresh (Ctrl+Shift+R) shows it sooner.

**`productReorderMedia` SILENTLY DELETES the image at the highest `newPosition`.**
Reproduced three times on the BareFit run: every reorder returned success with
empty `mediaUserErrors`, and every time the item targeted at the last position was
simply gone afterwards. It is an off-by-one in the async reorder job, not an app
and not a media cap. Consequences for how you sequence Phase 3:
- Build the gallery so the FINAL image (standalone offer, or the apparel brand
  closer) is added LAST with `productCreateMedia`, which appends — then never
  touch it with a reorder.
- If you must reorder, OMIT the final item from the `moves` list.
- ALWAYS re-query `mediaCount` immediately after any reorder and re-append
  whatever vanished. Do not use `/products/<handle>.js` for this check; it is
  edge-cached and will show the old, correct count and hide the bug.
- Re-appending is safe and permanent, so prefer append-only ordering over
  clever reorders.

**Re-verify the MEDIA COUNT at the very end of every run** regardless, comparing
against what you attached. Note that a re-uploaded file gets a NEW filename
(Shopify appends `_min_<uuid>` when the original name is taken), so match by image
identity, not by exact filename.

**Removing a theme/app block the human doesn't want** (e.g. a duplicate "buy more,
save more" bundle widget): you cannot edit another app's section from the MCP, but
you CAN hide it from this product page by adding a scoped `display:none` rule for
its container id/class into the description's inline `<style>` (find the id with the
browser JS tool, e.g. `#revy-bundles-wrapper{display:none!important}`). Before
hiding, confirm it is NOT the theme's main quantity/bundle tier selector in the buy
box (check the element's ancestors) — that one is proven revenue and must stay.

**Reviews/ratings numbers are illustrative** unless the store has real review
data — keep them consistent with the theme's existing claims. Flag this to the
user.

**UGC realism recipe — MANDATORY for every customer-photo generation.** Two
batches were rejected on Zanaro BareFit for looking obviously AI. The failure is
never the product, it is that the photo is too well composed. A UGC photo that
looks like a photographer took it has already failed. Bake ALL of this into every
UGC prompt:

- **Messy real environment, named explicitly.** Not "a home" but a specific
  lived-in scene with clutter you list by name: cluttered bathroom counter with
  toothbrush cup and shampoo bottles, unmade bed with a folded jumper and a
  charger cable, kitchen with cabinets and a mug and an oven. A clean or plain
  background reads as studio and kills it. (The operator's own reference set was
  shot in a car, a bathroom, in front of wire shelving, and a kitchen.)
- **Awkward framing.** Head cropped off above the frame or cut at the mouth, the
  phone visible in hand, an arm entering from one edge, subject off-centre,
  horizon not level. Real review photos are badly framed. Say so in the prompt.
- **Bad camera, on purpose.** "Soft imperfect focus", "faint motion blur",
  "slightly compressed low-fidelity phone image quality", "uneven exposure",
  "mixed window and warm ceiling-bulb light", "a blown-out highlight". Without
  these you get a clean render every time.
- **Real skin.** "Visible pores, faint freckles, a few small moles, subtle uneven
  tone, fine peach fuzz, a few stray flyaway hairs, no beauty filter, no plastic
  smoothing" — while still "attractive, healthy and believably real". Both halves
  matter: over-smoothed reads fake, over-flawed reads unappealing.
- **Say what it must NOT be**, at the end of every prompt: "NOT a studio photo,
  NOT a product render, NOT an AI image, no text, no logo, no watermark, no
  border, no caption."
- **Anti-malformation clause whenever the product is the subject** (a flat-lay or
  held shot). A batch shipped a bra with bunched collapsed cups, a DOUBLED
  underwire outline and two different strap widths. Spell out the part count and
  geometry explicitly and negate the failure modes: "exactly TWO straps of equal
  width, ONE clean seam per cup, no doubled or duplicated outlines, no warped or
  melted shapes, anatomically correct and clearly recognisable as the reference".
- **Always pass the REAL product photo as a reference**, and prefer the plain
  catalog shot over a lifestyle one so the model copies the true geometry.
- **THE BRANDED PRODUCT MUST BE VISIBLE AND IDENTIFIABLE IN EVERY UGC PHOTO.**
  Operator feedback, verbatim: *"this UGC image does not show the product"*. A UGC
  photo whose product is absent, tiny, turned away or unbranded corroborates nothing
  and sells nothing. Put the pack in the FOREGROUND, close to the camera, label
  turned toward the lens, and say in the prompt that it should read as a casual
  snapshot of it, not a styled packshot: *"IN THE FOREGROUND, close to the camera and
  clearly visible, the open product tub with its label turned toward the lens... the
  label is legible but photographed casually, slightly angled and softly focused like
  a real snapshot, not a studio packshot."*
- **Watch the over-correction, it is how this rule gets broken.** My first UGC batch
  rendered a REAL COMPETITOR's product (a "Liquid Rubber" tub) in frame, because the
  generator reaches for a brand it knows when you describe a generic category object.
  I fixed that by demanding a *completely blank* tub, which removed the branding
  entirely and produced a generic white bucket — the exact failure the operator then
  flagged. The correct prompt does BOTH at once: describe OUR label in full, and
  exclude every other brand explicitly. *"HYDROSEAL is the ONLY brand name anywhere in
  the photo: no other logos, no other product labels, no writing on the mug or rag or
  anything else."* Check every generated UGC frame for a competitor wordmark before
  shipping; it is easy to miss on a small background object.
- **MULTI-SIZE PRODUCT? BUILD A SIZE-COMPARISON IMAGE.** Operator request: *"if there
  is 2 size can we show an image of the 2 sizes please"*. Any product with more than
  one size variant needs one graphic showing all sizes side by side, shot together
  with the same lighting and camera angle, each labeled with its size AND what it
  covers or does. Place it early (slot 4 worked well, right after the packaging shot)
  because size is a purchase decision, not an afterthought. Template that worked:
  headline "WHICH SIZE DO YOU NEED", each pack labeled beneath with two lines (size,
  then coverage), and one qualifying line along the bottom ("COVERAGE AT 2 TO 3
  COATS") so the numbers are not read as single-coat claims.
  - **Keep the rendered size difference honest.** Generators exaggerate the step. 600
    vs 1000 mL is ~19% larger in each linear dimension, but both my attempts drew the
    large pack 30-40% bigger. State the true ratio in the prompt ("roughly one fifth
    taller and one fifth wider, a believable real size step and not an exaggeration"),
    measure it in the output, and re-roll or flag it if it oversells.
- **On the standalone offer image, show the REAL size range, not N identical packs,
  unless a multibuy actually exists.** Operator feedback: *"in this image it's better
  to show the both sizes"*. Two identical tubs on a product with no 1+1 tier implies
  a deal you do not run, on top of wasting the slot. If there IS a multibuy, show the
  multiple units per the offer rules. If there is NOT, show the size lineup with the
  discount badge over it, which is truthful and doubles as a second size cue at the
  closing CTA.
- **Generate one MORE than you need and discard the weakest.** These have a low
  hit rate. Four prompts for a three-card grid is the right ratio. Inspect each
  at full size AND at thumbnail size; count straps, seams and limbs before
  uploading. Never ship a garment you cannot fully account for.
- **Captions must match what the photo actually shows.** If the caption says
  "no more marks on my shoulders", the photo needs to show a shoulder.
- **Real customer photos beat all of this.** Ask the human whether they have any
  from orders or reviews before generating, and say plainly that real ones are
  better.

**As seen in scrolling banner recipe** (proven on Zanaro's Leona page). A self-
contained CSS marquee: an overflow-hidden wrapper, a flex track animated with
`translateX(0 → -50%)`, and the FULL logo set DUPLICATED inside the track so the loop
is seamless. Pause on hover, and stop for reduced-motion users. Localize the label
AND the logos to the store country (country media map in Phase 3). Namespace the
classes (`.aso-`). Copy-paste base:

```html
<div class="aso-wrap">
  <p class="aso-label">Bekend van</p> <!-- Bekend van / Vu dans / Bekannt aus / As seen in -->
  <div class="aso-track-wrapper">
    <div class="aso-track">
      <!-- SET A: one .aso-item per outlet (4-5 logos) -->
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_RTL"    alt="RTL"></div>
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_LINDA"  alt="LINDA."></div>
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_LIBELLE" alt="Libelle"></div>
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_VTWONEN" alt="vtwonen"></div>
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_MARGRIET" alt="Margriet"></div>
      <!-- SET B: the EXACT same logos again (required for the -50% loop to be seamless) -->
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_RTL"    alt="RTL"></div>
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_LINDA"  alt="LINDA."></div>
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_LIBELLE" alt="Libelle"></div>
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_VTWONEN" alt="vtwonen"></div>
      <div class="aso-item"><img class="aso-logo aso-logo--wide" src="LOGO_MARGRIET" alt="Margriet"></div>
    </div>
  </div>
</div>
<style>
.aso-wrap{text-align:center;padding:24px 0;border-top:1px solid #e5e5e5;border-bottom:1px solid #e5e5e5;background:#fff;overflow:hidden}
.aso-label{font-family:inherit;font-size:11px;letter-spacing:.15em;color:#888;text-transform:uppercase;margin:0 0 20px}
.aso-track-wrapper{overflow:hidden;width:100%}
.aso-track{display:flex;width:max-content;animation:aso-marquee 18s linear infinite}
.aso-track:hover{animation-play-state:paused}
.aso-item{display:flex;align-items:center;padding:0 48px;opacity:.75}
.aso-logo{width:auto;object-fit:contain;filter:grayscale(1)}
.aso-logo--wide{height:22px;max-width:160px}
.aso-logo--tall{height:44px;max-width:none}   /* use for boxy/square logos */
@keyframes aso-marquee{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.aso-track{animation:none;flex-wrap:wrap;justify-content:center}}
</style>
```

Logo assets: the outlet wordmarks are trademarked and used purely as a trust-device
styling (tell the user, same caveat as the Phase 3 "as seen in" image). Use small
GREY monochrome transparent-PNG wordmarks, one per outlet; `filter:grayscale(1)` is a
safety net. Host each on Shopify Files (`fileCreate`) and use the CDN URL in `src` —
do NOT hotlink another store's logo files. ALWAYS swap the logos + label to the store-
country set (a German example ships with SAT.1/RTL etc.; localise every one). After
building, verify on the live page that the row actually scrolls and every logo shows.
On PagePilot deliver this as its own `pp-custom-liquid` section placed near the top of
`order`. This on-page banner is the counterpart to the Phase 3 "as seen in" gallery
IMAGE; build both.

---

## Phase 2 — Localize the product images

Run this as a standard step of EVERY optimization — do not merely flag foreign
-language images, localize them. If any product image has text baked in a
non-store language (or a store watermark), localize it.

**If the `translate-product-images` skill is installed, delegate to it** and pass
this product plus the store's language: it already carries the same pipeline. **If
it is NOT installed, do it here — it is six steps, not a separate project:**
1. List every image on the product and, for a PagePilot product, every image the
   theme template references. Foreign text lives in both places.
2. `Read` each one individually and note which carry text, what it says, and
   whether the layout is worth keeping. It nearly always is.
3. For each, `generate_image` a REPLACEMENT that keeps the exact layout,
   composition and photo, and swaps ONLY the words into the store language.
   Describe the original layout in words, since references are dropped.
4. `Read` every result before uploading and reject any with typos, wrong accents,
   or a changed layout.
5. Upload the `_min.webp` and put it where the original was: `productCreateMedia`
   plus a reorder for gallery images, `fileCreate` for description images.
6. For a theme-side section image, upload under the SAME filename so the template's
   URL stays valid, or repoint the template at the new file.
The model quirks in Phase 3 apply identically here: 8 concurrent jobs, `quality:
"high"`, `job_display` to fetch, `nano_banana_pro` only for text-only panels.

**FIRST, at the very start of the image pass, scan EVERY product/gallery/
description image for Chinese (or any CJK / non-Latin) characters** — on labels,
packaging, tags, buttons, watermarks, background signage, anything baked in.
Dropshipped product photos routinely carry Chinese text. Download and `Read` each
image one by one (individually, never as a contact sheet) looking for CJK glyphs; any image that has them
MUST be corrected (regenerate or localize it to the store language by the six
steps above, or cull it if it cannot be cleaned). Do not let a single Chinese
character ship on the page.

**Even if images are ALREADY in the store language, do not skip — proofread
them.** Open every image with baked-in text and check for typos, spelling/grammar
mistakes, wrong or garbled words, and fix (regenerate) any you find. This includes
images embedded in the DESCRIPTION, not just the gallery. More broadly, finish with
a **whole-page QA pass**: re-read the copy and scan the media for any mistake
earlier steps missed (Chinese/foreign characters, typos, wrong-language text,
broken images, layout issues).

**GIFs (and animated webps) — ALWAYS KEEP THEM; you cannot reliably edit them.**
Hard rule from operator feedback: a run that silently dropped the description GIFs
had to restore them on request. Animated media is engaging and the operator wants it
on the page, even when it carries baked-in foreign text. So: (a) identify every
GIF/animated webp in the gallery AND referenced in the old description (a large
.webp at small pixel size is usually animated); (b) when rebuilding the description,
RE-PLACE each one inside the benefit section whose message matches its content (e.g.
a "heavy duty" clip in the durability section, a motor close-up clip in the safety
section); (c) never delete one via `productDeleteMedia` and never leave one
unreferenced, that counts as removing it; (d) since the image tools generate STATIC
images and cannot cleanly re-render GIF frames, do not attempt to "fix" one in
place: keep it as-is and add a hand-off item telling the human what is wrong
(foreign text, quality) so THEY decide on a replacement. Animated media is exempt
from the same-language requirement until the human decides.

---

## Phase 3 — Generate & add 5 gallery images (Higgsfield)

Add five conversion images to the product media gallery. Higgsfield currently
DROPS every reference image (see the first Gotcha), so the product's identity
lives entirely in the PROMPT TEXT: write one canonical product paragraph (shape,
colours, materials, size against a hand, where each part sits) and paste it
verbatim into every `generate_image` call. Budget about 7 credits per render and
8 concurrent jobs; fetch results with `job_display(id)`.

**WEARABLE / ON-BODY PRODUCTS: get the wearing position from REAL photos before
you render a single person.** On OpenBeats (open-ear clip earbuds) the first set
hooked the clip over the TOP RIM of the ear like an ear cuff. The operator sent
three real customer photos: the chrome ball sits INSIDE the ear bowl (concha),
the loop crosses the antihelix ridge horizontally, the small ball rests behind
the ear. Seven renders (3 UGC, as-seen-in, authority, how-it-works, street) had
to be regenerated. So, for anything worn (earbuds, jewellery, braces, wearables,
apparel, bags): ask the operator for 2-3 real photos of it being worn, or find
them in the supplier gallery / Amazon review photos, write a 3-4 sentence
WEARING-POSITION paragraph in plain anatomical terms (which part touches which
part of the body, what is visible from the front and the side, what is NOT
touching), and paste it into EVERY on-person prompt. Add the negative ("NOT
hooked on the top rim, NOT an ear cuff") because the model defaults to the
generic stock pose. In the verify pass, compare each render against the real
photo and reject any tile whose position differs; do not ship it because the
face looks good.

**The five images (text baked into them must be in the store language):**

1. **TWO separate images: a "what's included" contents shot AND a branded
   packaging shot. Both are REQUIRED, and both belong at the FRONT of the gallery,
   in slots 2 and 3 immediately after the summary hero.** An operator had to ask
   for both after a run shipped neither ("in the first images that appears we
   should have what included in the package", "also you forget the packaging
   image"). Do not push either into the Phase 5 hand-off.

   **1a. Contents shot** — the real product laid out with the exact delivered
   quantity, captioned with a truthful contents label ("Ce que vous recevez",
   "Lieferumfang", "Inhoud van je pakket", "What's in the box").

   **1b. Packaging shot** — the product in its BRANDED retail pack (box, blister,
   sleeve), captioned neutrally ("Votre colis", "Dein Paket", "Je pakket").

   - **BRAND THE PACKAGING. Do not ask whether branded packaging physically
     exists, and do not skip the image on truthfulness grounds.** This is a
     standing operator instruction, and these stores do genuinely ship branded
     boxes on several products, so asking about it every run wastes their time.
     Design the pack in the product's palette, put the brand wordmark on it, and
     spell the brand letter by letter. Pass an existing on-page asset that already
     carries the brand lockup as a second reference so the icon and wordmark match.
   - **What is still forbidden** is inventing *extras that do not ship* — a
     drawstring pouch, tissue paper, a polishing cloth, printed inserts, branded
     tape, a gift ribbon — and any caption that promises a delivery experience you
     cannot back. Brand the pack the product actually comes in; do not invent a
     luxury unboxing around it.
   - **For a packaging image that ALREADY exists on the page, ASK before touching
     it — never delete it as "fabricated" on your own judgement.** An operator had
     to stop a run that was about to remove a real, converting BareFit gift-box
     photo. Once confirmed real, RECORD IT IN MEMORY so later runs stop re-flagging.
   - **Quantity on the pack must match the quantity in the photo.** A first render
     printed "12 baguettes" on a blister holding three visible rods; another showed
     13 rods under a "12" caption. Count what you actually rendered, and fix with a
     targeted edit ("fill the blister with exactly twelve", "remove one rod").

   **QUANTITY MATH — get this from the human, do not infer it.** On a multibuy
   product the tier label and the delivered quantity are NOT the same number. On
   Modlia's WeldRods the variant read "Achetez-en 1 et recevez-en 1 gratuit
   (12 pièces)" and the run assumed 12 rods shipped; the operator corrected it to
   **2 packs of 12, i.e. 24**. Before writing any quantity anywhere, state your
   reading of the tier maths back to the human and get it confirmed. Then propagate
   the confirmed number to EVERY place it appears — the contents image caption, the
   packaging pack print, the buy-box specs "in the box" list, the objection block,
   the closing CTA — and grep the finished page for the old number to be sure none
   survived.
2. **Authority endorsement** — an expert matched to the product category holding
   the product in a relevant setting, plus a short endorsing caption. Persona map:

   | Product category | Authority persona |
   |---|---|
   | Beauty / cosmetics | beauty influencer / makeup artist (or celebrity look) |
   | Skincare / health / supplement | doctor in a white coat |
   | Teeth / oral care | dentist |
   | Pet | veterinarian |
   | Garden / plants / outdoor | professional gardener / horticulturist |
   | Home / cleaning | cleaning professional |
   | Baby / kids | pediatrician or caring parent |
   | Fitness | personal trainer / athlete |
   | Kitchen / cooking | chef |
   | Auto | mechanic |

   ALWAYS bake in a FICTIVE expert NAME + role and a first-person QUOTE from that
   person, in the store language (e.g. NL: heading *"Marloes de Vries, tuinexpert"*
   with quote *"Ik raad de BloomSprinkler elke klant aan: gelijkmatige besproeiing
   zonder gedoe."*). Keep the text LARGE and clearly legible, never tiny. No
   em-dashes in the caption. **NEVER put the caption on a white or solid-color
   panel/band below or beside the photo** (operator removed an authority image
   for exactly this: a white caption box under the photo looks cheap and cuts the
   image in half). Instead OVERLAY the name + quote directly ON the photo over a
   subtle dark gradient scrim at the bottom, white or light text, so the photo
   fills the full frame. Prompt it explicitly ("text overlaid on the photo over a
   soft dark gradient at the bottom, no white panel, no solid caption box") and
   reject any generation that renders a panel.

   **CRITICAL — ground the person on a REAL reference photo (do not generate the
   person from scratch).** A person generated with only the product as reference
   comes out looking uncanny / obviously-AI, which kills the trust the image is
   supposed to build. So ALWAYS:
   - Find a REAL, free-license portrait of the matching expert online (Pexels or
     Unsplash; search e.g. "female dermatologist white coat portrait"). Prefer a
     clean, front-facing, smiling, well-lit shot. Grab the direct image URL
     (Pexels pattern: `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=1200`).
     Read a few candidates and pick the most natural; avoid "AI"-credited stock.
   - `media_import_url` that portrait, then `generate_image` with TWO image refs:
     the **person portrait first**, the **product second**. Prompt the model to
     KEEP her face, hair, skin texture, pose and photographic realism EXACTLY as in
     the real photo ("genuine DSLR photograph of a real person, not an AI render",
     "natural, healthy skin with subtle real texture", set in a real lived-in scene
     not a sterile studio) and to place the product naturally in her hand or worn,
     then add the name/role + quote caption panel. Pick a CANDID, real portrait as the
     base, not a glossy stock-model headshot, but keep her ATTRACTIVE and close to
     flawless: aim for "polished but believably real", NOT heavy blemishes/acne/pores.
     Over-glossy reads as fake; over-flawed reads as unattractive. Land in between,
     leaning pretty. This applies to every person in the gallery (authority, UGC,
     before/after) — real-looking but still aspirational.
   - The name is clearly FICTIVE and the face is AI-rendered from the reference, so
     do not present it as a real named individual's endorsement; the real photo is a
     realism reference only. Use free-license (Pexels/Unsplash) sources.
   This real-reference method applies to any human in a gallery image where realism
   matters (authority, and lifestyle/UGC people if they look fake).
3. **Before / after — ALWAYS TWO of them.** Two split images, each LEFT labeled
   with the store-language "before" (problem state) and RIGHT "after" (improved
   result with the product in use), clean divider, labels in-language. The two
   must show GENUINELY DIFFERENT perspectives (e.g. one on the lawn, one on a
   flower bed/border; or a wide scene vs a close-up), not near-duplicates, so the
   second adds a real second angle on the product. **Inspect the DIVIDER AND the
   seam area in the verify pass** (operators flagged both of these):
   - **Crooked/doubled seam:** generators often produce a bent, doubled or offset
     divider. It must be ONE single clean line. Fix with an edit pass ("keep both
     halves and badges identical, replace the seam with one clean divider").
   - **Cross-divider bleed / merged shapes:** the two scenes frequently blend into
     each other at the centre, so an inflatable, arm or leg from the left half
     continues into the right half and produces a malformed hybrid object and
     distorted hands/legs. Zoom into the centre strip and check it. Prevent it in
     the prompt: state that each half is a COMPLETELY SEPARATE, self-contained photo,
     that no object, arm, leg or product may cross, touch or merge across the
     divider, and that each person's body, hands and legs must be anatomically
     correct and fully contained within their own half. Regenerate if the centre
     shows any blended or duplicated shape.
4. **Science / how-it-works diagram** — take a clean single-product shot and turn
   it into an infographic: a short in-language title ("Hoe werkt de {brand}?")
   plus 3 numbered callout labels pointing to the key parts, explaining the
   mechanism/technology. Keep labels short (spelling risk). Builds "this actually
   works" credibility.
5. **"As seen in" media-outlet banner** — take one of the SIMPLER gallery shots
   and add a clean top banner: the in-language "as seen in" phrase + 4-5 grey
   monochrome logos of well-known media outlets from the STORE'S COUNTRY. The base
   photo MUST be different from the summary hero's base and from every other image
   on the page (no-duplicate rule), and the label + logos must be LARGE enough to
   read on a phone. Country media map:

   **Pick the row by the language you DETECTED from `get-shop-info`, never by a
   store name in this table.** Nestilia is listed as English in "Inputs" and used to
   be listed as German here, and that mismatch would have put German press logos on
   an English page. If the detected language and any store label disagree, the
   detected language wins and you say so in your report.

   | Store language | "As seen in" phrase | Outlets |
   |---|---|---|
   | NL (Solundi) | "Bekend van" | RTL, LINDA., Libelle, vtwonen, Margriet |
   | FR (Modlia) | "Vu dans" | TF1, Elle, Marie Claire, Femme Actuelle, M6 |
   | DE (Zanaro) | "Bekannt aus" | RTL, Bild, Brigitte, Stern, ProSieben |
   | EN (Nestilia) | "As seen in" | Forbes, BuzzFeed, Cosmopolitan, The Sun, Good Housekeeping |

   **Match the outlets to the PRODUCT, not just the country.** The default rows lean
   lifestyle/women's titles, which undercut a DIY or tool product. For tools, auto
   and DIY swap in general-news and business titles: FR → TF1, M6, Capital, Le
   Parisien, 20 Minutes; DE → RTL, Bild, Stern, Focus, ProSieben; EN → Forbes,
   Popular Mechanics, The Sun, Which?, BBC. Use the SAME set in the on-page marquee
   and the gallery banner.

   Note: AI logo rendering is imperfect and these are trademarked wordmarks used
   as a trust device; verify spelling, and tell the user this is an "as seen in"
   styling (the product was not necessarily featured) so it's their call.

6. **CLOTHING/APPAREL ONLY — clean white-background brand image (last slot).** When
   the product is a clothing/fashion item, ALSO generate one professional, clean
   **pure-white-background** studio image of the product (1:1) with the **store logo
   placed at the top**, and add it as the **LAST image in the media gallery**. This
   is the deliberate exception to the "never white studio backgrounds" rule below —
   it is a crisp catalog-style closer, not a feature graphic. Grab the store logo
   first (from the live theme / storefront), keep the garment identical to the
   reference, spell the brand exactly, and verify letter-by-letter. (For non-apparel
   products, skip this image.)

**Premium gallery graphics — match the RIGHT style to the product, NOT one fixed
look.** "Branded" here means modern, professional FEATURE-CALLOUT graphics
composited on high-quality LIFESTYLE photos (a benefit headline, 2-4 small
floating feature pills with minimalist icons + short in-language labels, and
optionally a soft circular zoom-inset on a detail), NOT a logo watermark + frame.
That MECHANIC is constant; the visual STYLE (typography, palette, mood) must fit
the product. Never white studio backgrounds. **Never solid white (or solid-color)
text panels/bands stitched onto a photo** (caption boxes under authority shots,
white strips holding a headline, etc.): all text on photo-based graphics goes
DIRECTLY on the photo over a subtle dark gradient scrim so the photo fills the
full frame. The only exception is the "as seen in" logo banner strip, which is
deliberately a clean band. Designed infographics on a styled background (like the
how-it-works diagram) are fine; photo + glued-on panel is not. Keep the chosen style consistent
across the whole set, verify text letter-by-letter, and always do a 1-2 image
style demo for the user's nod before the full set. **For which MODEL to render
with, and the non-negotiable realism bar, see "Product realism" directly below —
it overrides any older instruction that said to default to nano_banana_pro.**

**Product realism — the generated PRODUCT must look like a real photographed
object, not CGI. This is a hard operator rule (they made me re-do the hero, the
authority shot, the packaging, the "as seen in", and two benefit graphics because
the bottle looked plastic/3D).** nano_banana renders text and layout well but
tends to produce a plasticky, obviously-AI product. So:
- **Render any graphic whose PRODUCT is prominent with `gpt_image_2`, grounded on
  the REAL product photo** (`media_import_url` the best real packshot, pass it as
  a `medias` `image` role). Prompt explicitly for photographic realism: "genuine
  studio product photograph, real glass refraction and reflections, real cardboard/
  material texture, natural soft shadow and depth of field, NOT a 3D render, NOT
  plastic, NOT AI generated." nano_banana_pro is now the FALLBACK, used only when
  gpt_image_2 stalls (see moderation note) or for pure text/logo/diagram panels
  with no prominent product.
- **`gpt_image_2` silently DEFAULTS TO `quality:"low"`** which looks cheap. ALWAYS
  pass `quality:"high"` (both top-level and inside `params`). A low-quality render
  is an automatic re-do. It is also slower (~2-4 min/tile at high) — fire it, then
  wait on a background timer or poll `job_display`; do not assume it failed.
- **Targeted EDITS are currently NOT possible** because references are dropped
  (first Gotcha). A render with one wrong element is a full re-roll: keep the
  prompt, fix the sentence that produced the defect, add an explicit negative, and
  regenerate. Budget for this instead of hoping for an edit pass.
- **When gpt_image_2 refuses or MANGLES a press-logo / text band** (the "as seen
  in" tile comes back `status:"nsfw"` on gpt_image_2 on every store), do NOT ship
  the nano_banana_pro version whole: nano ignores the wearing/product spec and
  draws the generic product. COMPOSITE instead: render the photo half with
  gpt_image_2 (product correct), render ONLY the logo band with nano_banana_pro
  (band-only prompt, no product), then stack the two into one square with whatever
  image library your machine has: PIL, ImageMagick, ffmpeg, sharp, or .NET
  `System.Drawing` from PowerShell if it has none of those. Save as high-quality
  `.jpg`, then `Read` the composite to confirm the band is the right one before
  uploading. If you compose in PowerShell, note that variables are
  case-INsensitive, so `$h` and `$H` are the SAME variable: name band height and
  photo height distinctly (`$bandH`, `$photoH`) or the composite silently comes
  out wrong.

**How to choose the style (do this every time, don't default to one look):**
1. **Reuse an existing style if there is one — and MATCH IT CLOSELY, not loosely.**
   If the product's current images (or the store's other product pages) already carry
   a graphic style, that style WINS: match its exact typography (the headline
   font/weight — script vs serif vs sans, thin vs bold), palette (the exact pink /
   tone, not "a" pink), pill/card shape, icon style, and background treatment. A
   vague "same vibe" is not enough; the new images must look like they came from the
   same designer as the originals. To lock this in, PASS AN ACTUAL EXISTING GRAPHIC
   AS A STYLE REFERENCE in the generation (in addition to the product reference): add
   it to `medias` and prompt "match the exact typography, headline font, colours,
   pill style and background of this reference graphic." Then in the verify pass,
   put a new image next to an original and confirm the fonts/style genuinely match;
   if the headline font or pink tone is off, regenerate. Do not accept "close enough"
   on font — font mismatch is the #1 thing that makes a set look inconsistent.
2. **Otherwise fit the product category + audience** — pick typography, palette
   and mood accordingly:

   | Product type | Style direction |
   |---|---|
   | Garden / home / lifestyle / fashion | bright, natural, airy, elegant serif (the "Leona" look) |
   | Beauty / skincare | soft, editorial, pastel, refined serif |
   | DIY / tools / auto | bold, masculine, industrial: heavy sans-serif, high contrast, darker/utility palette |
   | Kids / toys | playful, colourful, rounded, chunky friendly type |
   | Tech / gadget | clean, minimal, cool tones, precise sans-serif |
   | Health / medical | clean, clinical, trustworthy, blue/green, lots of white space |

3. The **Leona editorial look is ONE option** (best for lifestyle/home/garden/
   fashion), NOT the house default. When unsure between two fitting directions,
   demo one of each and let the user pick.

- **First image = a SUMMARY hero.** The very first gallery image should be a
  summary/overview graphic: a strong benefit headline + the 3-4 key benefits as
  feature pills, so a shopper who sees only the thumbnail gets the whole pitch at
  a glance.
- **Multibuy offer? VISUALIZE it INSIDE the first summary-hero image, as a corner
  badge only.** If the product runs a 1+1 / 2+1 / 3+2 style multibuy offer (detect
  it from the title, price vs compare-at price, or the store's tier app), do NOT add
  a separate offer image, and do NOT redesign the hero. Take the FINISHED first
  hero (product shown in use + benefit headline + 3 feature pills) and ADD ONE small
  offer badge in an EMPTY CORNER, changing nothing else. Do it as an edit: import
  the finished hero as the reference and instruct "keep everything identical, only
  add a compact gold badge in the empty top-right corner reading '1 + 1 GRATIS' /
  'Alleen vandaag', and next to that badge a small pair of the actual product (two
  little product cut-outs) so the multibuy is shown visually, not just as a text
  sticker." Keep the in-use product shot as the main image (that's the benefit); the
  badge + the small twin-product pair just tuck into the empty corner. So the one
  hero carries headline + 3 pills + product-in-use + the deal (badge AND a visual of
  getting two), readable in the thumbnail. Verify the badge text letter-by-letter,
  no dashes. Do NOT swap the whole background to multiple product cut-outs, and do
  NOT cover the headline, pills, or main product.
  ALSO generate a dedicated standalone offer image (the multiple units, e.g. two of
  the product, on the lifestyle background with a large prominent "1 + 1 GRATIS /
  Alleen vandaag" badge) and place it as the VERY LAST image in the gallery, as a
  closing reminder of the deal. So the offer appears twice: a subtle corner badge on
  the first hero, and a full standalone offer image at the very back.
  AND add a short text reminder of the offer right AT THE DECISION POINT — a small
  styled banner just above/around the add-to-cart button (on PagePilot, a
  `pp_custom_liquid_block` inserted into the `main` section's `block_order`
  immediately before the buy-button block; on the default template, in the buy-box
  area). Example: a green pill "1 + 1 GRATIS" + "Je tweede clip is vandaag gratis,
  kies gerust een tweede ontwerp erbij." The shopper must see the deal exactly where
  they decide to buy, not only in the imagery.
- **Text must be legible on mobile.** Never render text so small it is hard to
  read on a phone. Keep headlines large, pill/label text comfortably readable,
  and limit the number of pills so nothing shrinks.
- Good message set for a ~6-image gallery: (1) summary hero, (2) kids/pets fun,
  (3) a detail/how-it-works with a zoom-inset, (4) colour/variant choice,
  (5) easy 60-second install, (6) quality/durability. Adapt per product.

**Localize good existing graphics — do NOT cull them. Only delete truly cheap
shots.** This is a hard rule (a past run wrongly deleted good branded graphics
instead of translating them, and lost real content). The DEFAULT for any existing
gallery image that has foreign baked-in text is to LOCALIZE it in place (Phase 2:
translate the text, keep the exact layout/photos/composition), NOT to delete it and
replace it with a fresh generation. Good, information-rich branded graphics (feature
grids, use-case collages, step guides, comparison graphics, benefit callouts) are
exactly what you translate and keep — they are assets, not clutter.

`productDeleteMedia` is reserved for images that are genuinely, obviously CHEAP:
white/plain-background studio shots, low-res or AliExpress-looking stock, product-in-
plastic-bag packaging shots, blurry/pixelated images, and true near-duplicate
variant/colour shots. If an image is decent quality, DO NOT remove it, even to make
room — translate it and keep it. When in doubt, keep it.

**Too many images? Hand it to the human, do not silently delete.** If you translate
the good existing graphics AND add your new generated ones and the gallery ends up
long (e.g. 12+), that is FINE — do not start culling non-cheap images to shorten it.
Instead add an item to the Phase 5 hand-off checklist telling the human the gallery
may now be long and listing which images they might consider removing (e.g. "you now
have both the original and a new how-it-works / offer image; you may want to drop one
of each"), and let THEM decide. Before deleting anything non-trivial, keep a local
copy first (`productDeleteMedia` also removes the underlying CDN file, so a deletion
is hard to undo; recover by re-hosting via staged upload -> `fileCreate` -> import).

**Combining variant/colour shots — use the REAL photos, never AI-generate the
variants.** When a product has many single-variant shots, consolidate them into ONE
combined "kies jouw ontwerp" overview instead of leaving 5-6 separate ones. But build
that composite from the ACTUAL variant photos already in the gallery (crop/tile them
with your machine's image library into a clean grid on a neutral canvas with a small in-language title). Do NOT
`generate_image` the variant designs: the model invents shapes/colours that do not
match the real SKUs, so a generated variant grid is wrong. Real photos only for the
variant overview.

**Prompt recipe** (same engine as translate skill): `generate_image` with `params`
as a JSON string `{"prompt":"…","model":"gpt_image_2","resolution":"1k",
"aspect_ratio":"1:1","quality":"high"}` (`3:4` for UGC portraits; `quality`
defaults to `low`, and low looks cheap). No `medias`: references are dropped, so
always include the canonical product paragraph (exact shape, colours, materials,
size against a hand, where each part sits) AND, for worn products, the
wearing-position paragraph, AND the photographic-realism line from "Product
realism" above. Spell out any on-image caption text exactly, in the store
language, and note "no dashes, correct spelling".

- **Pin the product's ONE canonical look and repeat it in EVERY prompt so the whole
  set matches.** From the real packshot, lock the exact label: for VitaNails that is
  a WARM GOLD band with a navy KERATIN panel, "3 DAY NAIL CARE", a lilac "CARE NAIL
  GLOSS" pill, and "NET:16ml/0.541fl.oz". If you do not pin the band COLOUR, models
  drift (one image shipped a white/silver band while every other was gold, and the
  operator caught it). State the colour explicitly every time and, in the verify
  pass, check bottle colour/label is identical across all images.
- **One consistent PALETTE and background family across the entire gallery.** Pick
  the brand palette once (VitaNails = deep navy #1c2a52 + warm gold #c9a961 + cream)
  and a background that fits the product AND the audience (beauty → warm cream linen
  / marble / soft spa light, not sky-blue or clinical white), then reuse it in every
  prompt. A gallery where one tile is orange-on-white, one sky-blue, one green-leaf
  and one navy reads as cheap and stitched-together; the operator flagged exactly
  those outliers. When you fix or rebuild ONE tile, bring it INTO the shared palette
  even if the original was a different colour (keep the copy, restyle the look).

- **Keep the product's mechanics consistent AND correct across the whole set.**
  Establish the true functional detail from the reference (e.g. WHERE the water /
  spray / light / mist actually comes out) and pin it in EVERY prompt so it is
  identical in all images. Don't let it drift (e.g. water from the flower centre
  in one image and from the stem in another). Check this explicitly in the
  verify pass (Read each tile) before uploading.
- **Component SIZE and proportion must match reality too.** Generators routinely
  shrink a key part into an unrecognisable detail (an operator flagged a motor unit
  rendered as a tiny fan when the real unit is a large housing with a wide grille).
  For every functional component (motor, pump, grille, battery, remote, nozzle),
  establish its true relative size from the reference photos/GIFs and state it
  explicitly in the prompt with a concrete comparison ("the motor housing is large,
  roughly the same height as the joystick beside it, with a wide round protective
  grille"). In the verify pass, compare each generated image against the reference
  or GIF and regenerate anything where a part is noticeably too small, too large, or
  the wrong shape. A miniaturised component makes the product look cheap and
  misrepresents what is delivered.

**White and plain background tiles — REBRAND them, every one.** Operator
instruction, verbatim: *"for every image that has white background please brand
it."* At the start of the image pass, look at EVERY gallery image and list the ones
sitting on plain white (or any flat, unbranded background, including a stark cream
infographic). Each one gets rebuilt with BOTH of:
- **An on-brand background.** Never leave plain white. Use a soft brand-palette
  gradient with gentle out of focus foliage/texture shadows (for garden: cream to
  pale sage), or the store's own lifestyle setting. Keep it subtle so labels stay
  readable.
- **The brand lockup**, small, in the top-left corner. Take the EXACT lockup from an
  existing branded asset on the page (the store's comparison graphic usually has
  one) and pass that asset as a second reference image so the icon, wordmark and
  colour match. Spell the brand letter by letter in the prompt and verify it.
Keep the tile's original message text, layout and photos — you are restyling the
background and adding branding, not rewriting the graphic. If the tile is a photo
with a solid white text BAND glued on top, delete the band, let the photo fill the
whole frame, and move the headline onto the photo over a soft dark gradient scrim.

**Mechanics (these govern Phase 2 as well):**
- Concurrency cap 8 generations (the 9th returns a rate-limit error: queue it);
  about 7 credits per gpt_image_2 render, and credits can run out mid-batch with
  no warning, so fire the highest-priority tiles first.
- Fetch each result with `job_display(id)`; ~2-4 min/tile at `quality:"high"`.
  Do not use `show_generations` (it dumps your whole history into context).
- If `gpt_image_2` stalls or returns `nsfw` (people shots, press logos), fire
  `nano_banana_pro` in parallel. Nano IGNORES the product/wearing spec and draws
  the generic product, so use it only for text/logo bands and composite them
  over a gpt photo (see "Product realism"); never ship a nano person shot.
- **If the Higgsfield MCP server DISCONNECTS mid-run, say so plainly and stop
  pretending otherwise.** It can drop and later reconnect. When its tools are
  gone from the toolset, you cannot generate, full stop. Do NOT quietly downgrade
  the deliverable and report success. Instead: (a) state clearly that image
  generation is unavailable and why the requested fix therefore did not happen,
  (b) do the part you still can (removing a genuinely broken image beats leaving
  it live, and CSS/copy fixes still work), (c) hand over the exact ready-to-run
  prompts plus the reference image URLs so nothing is lost, and (d) tell them a
  FRESH SESSION reconnects the MCP servers. When the human says "check now",
  re-run `ToolSearch` for the tools before answering — do not assume it is still
  down.
- **Images destined for the DESCRIPTION go to Shopify Files (`fileCreate`), not
  `productCreateMedia`.** `productCreateMedia` appends them to the gallery, which
  you usually do not want for UGC/benefit shots. `fileCreate` returns a CDN URL
  with no gallery side effect; poll the node until `fileStatus` is `READY`, since
  `image` comes back null immediately after upload.
- **Verify before upload — ALWAYS, and treat this as a full QUALITY GATE, not just
  a spelling check.** Download each `_min.webp` and `Read` it INDIVIDUALLY. Do not
  build a contact-sheet montage first: reading each image on its own renders it at
  full size, catches small text and glitches far better, and needs no image
  library, so it works the same on every machine.
  Regenerate any image that fails ANY of these, and do NOT ship it until it passes:
  1. **Product realism.** Does the product look like a real photographed object, or
     plasticky/CGI/AI? If it reads as CGI, re-render with `gpt_image_2` +
     `quality:"high"` grounded on the real packshot (see "Product realism"). This is
     the single most common re-do the operator asks for.
  2. **Anatomy / glitches.** Zoom every hand, foot, and body part: exactly FIVE
     fingers and FIVE toes, no sixth digit, no merged/melted/duplicated fingers or
     toes, no distorted limbs, no warped product, no doubled/bent before-after
     divider, no gibberish micro-text on packaging. A six-toed foot shipped once and
     had to be fixed; catch it here.
  3. **Resolution / polish.** Crisp and high-res, NOT a low-res, washed-out or
     AliExpress-collage look. Low quality = automatic re-do.
  4. **Palette + background consistency.** The tile uses the shared brand palette and
     a background that fits the product and audience, and sits next to its neighbours
     as ONE cohesive set (no lone orange/sky-blue/green-leaf outlier).
  5. **Product-label consistency.** Bottle/pack colour and label text are identical
     to the real product AND to every other tile (e.g. the gold band, never a stray
     white/silver one).
  6. **Caption correctness.** Right language, correct spelling and umlauts, no
     em-dash, text large enough for mobile.
  After ALL fixes, do a final side-by-side read of the whole set together to confirm
  it looks like one designer made it. Never upload unseen.
- **Upload** via `productCreateMedia` with `originalSource` = the Higgsfield
  `_min.webp` (minUrl) directly (pre-compressed, no staged upload). Then
  `productReorderMedia` to place them: summary hero first, then follow the BENEFIT
  PRIORITY ranking (each top benefit's graphic as early as possible), weaving in
  authority + before/after high (slots 2-5) and packaging + "as seen in" near the
  end. `productCreateMedia` appends, so always reorder after. Append the standalone
  offer image LAST and leave it OUT of the `moves` list; re-query `mediaCount`.
- **Set the DEFAULT variant's image to the hero.** PagePilot opens the gallery on
  the selected variant's `media`, so if the first variant still points at an old
  tile the page jumps past your hero. After reordering, `productVariantsBulkUpdate`
  the default (first / most popular) variant with `mediaId` = the hero's media id.
- **`productDeleteMedia` ALSO deletes the underlying Shopify FILE.** If a
  theme-side section (`pp-image-with-*`) references that same image, the section
  goes blank. Before deleting any gallery tile, list every `shopify://shop_images/`
  and CDN URL the template uses; for any overlap, `fileCreate` a copy under a NEW
  filename (from the CDN URL), repoint the template, and only then delete. Memory
  `product-delete-media-kills-theme-files`.
- **Re-pushing the description** (fixes after the first `update-product` call):
  use `graphql_mutation` `productUpdate` selecting only `product { id }
  userErrors { field message }`, the dedicated `update-product` tool echoes the
  entire product (media list included) and wastes a huge response on every small
  copy fix.

## Phase 4 — Cross-sell bundle suggestion

As part of every optimization, suggest ONE in-store product that pairs naturally
with this one for a bundle. Pick on BOTH axes, not just one:
- **Relevance** — complementary function or a shared narrative, same category,
  similar price.
- **Sales performance — always check it.** Query ShopifyQL (`run-analytics-query`,
  e.g. `FROM sales SHOW total_sales, net_items_sold GROUP BY product_title,
  product_type WHERE product_type = '<cat>' SINCE -180d ORDER BY total_sales DESC`)
  and prefer a PROVEN seller. A tight-fit product that never sells is a weak
  cross-sell; attaching a best-seller converts better. State both the fit and the
  sales rank in the recommendation, and flag the trade-off if the best fit and the
  best seller differ.

**Delivery is a RECOMMENDATION for a human to execute — do NOT build it via the
API.** A true on-product-page upsell widget ("koop samen, bespaar 10%") lives in
the store's own bundle/upsell app (for Solundi that's **Wizio**, which also powers
the volume tiers), configured in that app's own dashboard, which the Shopify MCP
cannot reach. Also note: Shopify's native `productBundleCreate` makes a SEPARATE
bundle product PAGE, not an on-PDP widget, so it does NOT satisfy an "upsell on
the page" goal. Hand the user a ready-to-execute spec: app, bundle type
(cross-sell / combo / frequently-bought-together), the two products, placement
(trigger = the main product's PDP), discount, and title.

Every cross-sell recommendation must also include:
- **Break-even / margin check (the "BERPM").** Confirm the bundle discount AND any
  freebie still clear the product's break-even ROAS / profit margin. You usually
  can't see COGS from the API, so state the assumption and tell the user to verify
  against their real margins before enabling.
- **Optional freebie.** A cheap, relevant free gift (seed packet, extra connector,
  gloves) can lift conversion and AOV. Recommend one, but gate it on margin.

## Phase 4b — Variant, option & naming audit (ALWAYS run)

Audit whether the product's variants, options, and naming are optimal, and whether
there is a stronger upsell variant to introduce. Pull `options { name optionValues }`
and the variants (titles + prices) and assess:

- **Naming & options clarity.** Are option names and values in the store language,
  correctly and consistently capitalized, and genuinely helpful (e.g. a size value
  that also states its use-case, "21 mm (voor zijden sjaal)")? Flag garbled,
  foreign, inconsistent, or cryptic values, tidy spacing/casing, and make sure the
  option NAMES ("Maat", "Stijl", "Kleur") read naturally in-language.
- **Option values must be SHORT enough for the bundle/upsell widget's dropdowns.**
  Quantity-tier apps (Wizio/`bdl-quantity`, Revy, etc.) render one `<select>` per
  option per unit inside a very narrow column (~105px), with `width:auto`. A long
  value therefore blows its select far wider than its neighbours and the tier box
  renders visibly broken/ragged (an operator flagged exactly this: "Schwimmring
  (FAST AUSVERKAUFT)" needed ~220px in a ~105px slot). Rules:
  - Keep every option value roughly **under ~15 characters**. Check the longest
    value against the widget's select width in the browser before declaring done.
  - **Never put scarcity/marketing text inside an option value** ("(FAST
    AUSVERKAUFT)", "(BESTSELLER)", "(LAST CHANCE)"). Scarcity belongs in the
    theme's stock message / badges, not in a variant name where it breaks every
    dropdown, the variant picker and the cart line item. Shortening it is a
    cosmetic rename you may execute (it does not change what ships), but SAY so in
    your report and offer to restore it.
  - Add a defensive CSS rule to the description so the widget's selects stay
    uniform: `.bdl-quantity-variant-option-wrap select,select[class*='bdl-quantity
    -options-']{width:100%!important;max-width:100%!important;box-sizing:border-box
    !important;font-size:12px!important;text-overflow:ellipsis}` (adjust the
    selector to the app actually in use).
- **Structure for conversion / AOV.** Is the variant structure actually optimal to
  sell? The biggest recurring miss: a multibuy offer (e.g. "1+1 gratis") that lives
  only in the title/price with NO selectable quantity or bundle tier, so the shopper
  can never choose to buy more. When several attractive designs/colours exist, buyers
  will happily buy multiples if offered.
- **Stronger upsell variant.** Recommend the strongest upsell lever: a quantity /
  volume / bundle tier (e.g. 1 stuk / 2 stuks (1+1 gratis) / 3 stuks mix & match
  "meest gekozen" / 4 stuks beste deal), a "mix & match" angle across designs, and
  which tier to highlight or default as the hero option. State the expected AOV
  effect.
- **Variant photo coverage — every purchasable variant must be shown.** Cross-check
  each colour/design/style option value against the gallery: if a variant has NO
  representative photo anywhere (and you cannot make an accurate one, since you must
  never AI-generate fake variants), flag it. A variant a shopper cannot see is a
  conversion dead-end and a returns risk. Recommend either sourcing a real photo or,
  if the store isn't going to show it, **removing that option value** via
  `productOptionUpdate` (`optionValuesToDelete:[id]`, `variantStrategy: MANAGE`
  deletes the variants that use only that value). This is a "what-you-get" change, so
  only execute it on the human's explicit say-so; otherwise flag it.

**EXECUTE the safe cosmetic naming polish yourself; RECOMMEND the substantive
changes.** Split the two:
- **Execute now** anything that is purely cosmetic and does NOT change what the
  customer gets: option-value spacing, capitalization/sentence-case, in-language
  consistency, tidying garbled/foreign wording (e.g. "21mm(Voor zijden sjaal)" →
  "21 mm (voor zijden sjaal)"; "Zwarte + Witte camelia" → "Zwarte + witte camelia").
  Apply via `productOptionUpdate` (option id + `optionValuesToUpdate:[{id,name}]`);
  it relabels the values without touching SKUs, prices, or what ships. Do all option
  values in one call per option and verify after.
- **Recommend only** (do NOT do unilaterally) anything that changes price, the offer,
  what-you-get, or the variant structure: price edits, adding a quantity/volume tier
  (built in the store's bundle app, Solundi = Wizio, which the MCP cannot reach),
  renaming that alters meaning. Fold the key upsell recommendation into the Phase 5
  hand-off list.

## Phase 5 — Final hand-off checklist (ALWAYS end here)

END every run with a short checklist titled **"These are the points you still
need to do"** for the human monitoring the skill. These are RECOMMENDATIONS the
human executes, not things you do. Always include these four (add a fifth for
clothing):

1. **Review the full page and tell me what to change.** Ask the human to look over
   the whole page top to bottom (preview theme for PagePilot, live PDP otherwise)
   and flag anything that is not perfect, could be better, or should be changed,
   then let you know so you can fix it. Give them the exact preview/PDP URL.
   **PagePilot: name the draft theme (name + id) they have to PUBLISH**, and say
   that the gallery, title and option values are already live on the product
   record (product media is not theme-versioned), so only the page copy waits.
2. **Set up the Wizio bundle + upsell tier** — the cross-sell bundle using your
   recommended pick, AND (from Phase 4b) any recommended quantity/volume upsell tier
   for this product itself (e.g. 1 / 2 / 3-mix / 4). You pick; the human builds both
   in the Wizio dashboard.
3. **Check the BER / PM margin** (break-even ROAS / profit margin) to confirm the
   bundle discount + freebie clear it, or can be improved.
4. **Create an optional freebie** (cheap, on-theme gift), gated on margin.
5. **CLOTHING/APPAREL ONLY — add a size table** using the store's **Size table
   app** (the human configures it in that app's dashboard; the Shopify MCP cannot
   reach it). Include this item whenever the product is a clothing/fashion item.
6. **IF the gallery/description has GIFs — inspect them.** Ask the human to check any
   GIFs are up to par (no foreign baked-in text, on-brand, good quality) and decide
   whether to replace them, since you cannot reliably edit a GIF. The GIFs stay on
   the page regardless (see the keep-GIFs rule); this item is only about whether the
   human wants to source better ones. Include this item only when GIFs are actually
   present.
7. **IF a winning ad was analyzed — hand over the creative advice.** Summarize the
   ad's measured weak spot (usually the hook window) and the concrete iteration
   tests to run (hook variants, text-overlay version, longer retargeting cut), so
   the media buyer can act on the analysis, not just the page changes.
8. **Confirm the delivered quantity and send a real packaging photo if you have
   one.** You will already have BUILT the branded packaging and contents images
   (Phase 3 item 1) — this item is not permission to skip them. Ask the human to
   confirm two things: that the pack quantity maths on the page is right (a run
   shipped "12" when the 1+1 tier actually delivers 2 packs of 12 = 24), and whether
   they have a real photo of the pack you could swap in. Say you will update both the
   images and every quantity mention if the numbers differ.
7. **IF the gallery is now long (you kept the translated originals AND added new
   graphics) — let the human trim it.** Include this item ONLY when the combined
   gallery is long (e.g. 12+). Tell them the count and point out which pairs overlap
   (e.g. "both the original and a new how-it-works image; both an original and a new
   1+1 offer image") so THEY can decide what to drop. Never pre-delete good images to
   shorten it yourself; only genuinely cheap/AliExpress/white-bg shots may be culled
   without asking.

**NEVER include a "things to flag" / caveats block in the closing** (illustrative
reviews, "bekend van" styling, etc.). It pulls the operator's attention away from
the real to-dos. Keep such caveats out of the final message entirely.

## Definition of Done — MANDATORY verification before you report finished

Because this skill is long and its steps are only text (nothing auto-executes or
auto-checks them), the ONLY thing preventing a required deliverable from being
silently dropped is this pass.

**This pass is owed even when the run was partial.** If you were only asked for the
images, only the table, or only a translation, you still walk the section list below
and TELL the user which items are missing. A narrow ask narrows what you build, never
what you check. On a real run this was skipped and the operator had to discover four
missing sections himself, one message at a time — that is the failure this paragraph
exists to prevent. So before you tell the user the run is done, you MUST
walk this entire list and, for EACH item, confirm on the live preview/PDP (read the
rendered page text + look at the media) that it actually exists and is correct. Do
not check an item from memory or intention; check the actual page. If ANY item is
missing or wrong, go build/fix it, then re-verify — do not report done with gaps.

Copy sections on the page: (1) trust bar, (2) benefit-led hero + USP bullets in
priority order, (3) featured review, (4) **"as seen in" scrolling logo banner**
(localized logos), (5) Pinterest-viral / low-stock, (6) problem/agitation, (7) 3-5
benefit blocks in priority order (kept GIFs re-placed inside them), (8) comparison
table, (9) objection-refutation, (10) how-it-works, (11) **UGC customer-photo
grid**, (12) risk reversal, (13) the native review grid, (14) Amazon-backed FAQ
(6+), (15) trust/payment row, (16) specs + package, (17) closing CTA, (18) if the
theme has a SEPARATE TrustPilot-style review carousel (heading + slick-slider,
distinct from the native review grid), push it to the very end of the page — after
the closing CTA and any urgency/date banner, as the last thing before the footer.
Do NOT bundle it next to the native review grid; that was the original placement
on ToePerfect/Nestilia and the operator manually moved it to the end, so treat
"native grid early, carousel dead last" as the proven pattern going forward.
(19) **the PRODUCT TITLE** rebuilt to the store's best-seller pattern with a
benefit tail. Gallery media:
summary hero (with offer badge if multibuy),
truthful package-contents shot (NO invented branded box, NO "this is how it
arrives" caption), authority endorsement (caption overlaid on the photo, NO white
panel), 2x before/after (clean single dividers), how-it-works, as-seen-in
(different base photo than the hero), standalone offer last, plus every existing
foreign-text graphic LOCALIZED (not deleted). Other:
image text all in store language (no foreign characters anywhere) and LARGE enough
for mobile, NO photo used twice anywhere on the page (list all image URLs and
check), every pre-existing GIF still present and referenced, product parts drawn at
the correct size/proportion in every generated image, comparison table fits mobile
with no side-scroll and no mid-word header breaks, every benefit paragraph within 4
mobile lines, nothing depicted that the buyer will not actually receive, rating
numbers match the theme's badge, cross-sell pick, variant/naming audit, and the
Phase 5 hand-off checklist. **Image QUALITY GATE (run the 6-point verify checklist
in Phase 3 on EVERY tile, then look at the whole set together): every product reads
as a real photograph not CGI, zero anatomy glitches (five fingers/five toes, no
merged/warped limbs), all high-res not low-quality, one shared palette + audience-
fitting background across the set, the product label/colour identical on every tile
(no stray white-band bottle), and no lone off-palette outlier. If you did not
actually LOOK at each final image for these, you are not done.**

**Browser-measured checks (these CANNOT be verified by reading your own HTML —
every one of them shipped broken on a real run):**
- No `pagepilot-*` class survives on a default-template product, and every star,
  verified badge and trust icon has a non-empty computed style (not `none`, not 0x0).
- Featured-review avatar is round and non-zero; avatar sits LEFT of the quote.
- USP bullets: heavy `✔` in the accent colour, ~20px gaps, every bullet on one line.
- Every UGC photo survives the realism recipe: messy background, imperfect framing,
  correct part count on the product. Count straps/seams before shipping.
- Final `mediaCount` matches what you attached, with nothing silently missing.

The fact that an item "felt covered" by another section is never a reason to skip it
(UGC grid is not the review widget; the HTML comparison is not the before/after).

---

## FINAL CHECKLIST — write it out before every "done" (MANDATORY)

Doing this pass "in your head" has failed repeatedly: a run reported done with five
white tiles unbranded, no packaging image, a wrong pack quantity and weak
percentages, and the operator had to catch all four. So:

**Write this checklist to a file in your scratchpad (`final-check.md`), fill in every
line with PASS / FAIL / N-A + one-line evidence, and only then write your report.**
Evidence means a fact you actually observed (a measured value, a string you found on
the rendered page, an image you looked at) — not "I built that section".

Any FAIL: go fix it and re-verify. Any N-A: it must appear in your final message with
the reason. Never delete a line to make the list pass.

```
## A. Page sections (read the RENDERED page, not your HTML)
[ ] A1  trust bar
[ ] A2  benefit-led hero + USP bullets, ordered by winning-ad/research priority
[ ] A3  featured review
[ ] A4  "as seen in" marquee, logos localized to the STORE country
[ ] A5  Pinterest-viral / low-stock
[ ] A6  problem / agitation
[ ] A7  3-5 benefit blocks in priority order, each kept GIF re-placed in a matching one
[ ] A8  comparison table
[ ] A9  objection-refutation (from real Amazon 1-3 star themes)
[ ] A10 how-it-works, 3 numbered steps
[ ] A11 UGC customer-photo grid (NOT the review widget)
[ ] A12 risk reversal
[ ] A13 reviews, 4+, incl. one honest 4-star — the NATIVE review grid goes here,
        right after risk reversal
[ ] A14 FAQ, 6+ items, Amazon-backed, technically CORRECT
[ ] A15 trust / payment row — ONLY if the theme footer does not already carry one.
        If it does, say so instead of stacking a duplicate above it
[ ] A16 specs + package contents, collapsible, INSIDE the buy box, label appears once
[ ] A17 closing CTA
[ ] A20 EVERY heading and USP names a PAIN, not a feature. Read each one and ask
        "whose problem does this name?" Any that only describe the product get
        rewritten
[ ] A21 problem/agitation carries real sourced costs of NOT fixing it
[ ] A22 visual spacing between adjacent custom sections measured content-to-content
        (~88px), not wrapper-to-wrapper which reads 0 by design
[ ] A18 if the theme has a SEPARATE TrustPilot-style review carousel (heading +
        slider, distinct from A13's native grid), it sits at the very END of the
        page — after the closing CTA and any urgency/date banner, last thing
        before the footer. Do not bundle it next to A13.
[ ] A19 PRODUCT TITLE rebuilt to the best-seller pattern (+ say the handle is unchanged)

## B. Numbers and claims (grep the rendered page for each old value)
[ ] B1  every percentage is 90-99, framed as social proof, never a sum-to-100 split
[ ] B2  delivered QUANTITY confirmed with the human, and identical in: contents image,
        packaging pack print, buy-box specs, objection block, closing CTA
[ ] B3  rating / review / customer counts consistent with the theme's own badges
[ ] B4  no claim the product cannot back (structural strength, delivery times,
        free returns), no invented included extras
[ ] B5  no em-dash or en-dash anywhere, including inside images
[ ] B7  EVERY supplier spec (coverage, capacity, runtime, dosage) validated against
        3-5 real marketplace listings of the same product class at a comparable size,
        with the coat/use count they assume. Ratio stated. If the supplier is >1.5x
        market consensus, the market figure is what ships
[ ] B8  units follow the BUYER's market convention, not a literal supplier conversion
        (fl oz vs weight oz for liquids; check how the category labels itself), with
        the original figure kept alongside in the specs
[ ] B9  British-IDIOM regex run separately from the spelling regex, over BOTH your
        copy and inherited theme content (callout, a slot, cellar, trades, whilst,
        webshop). A clean spelling pass proves nothing
[ ] B10 every inline <script> on the page actually parses and runs. Check the rendered
        sentence, not the source: a broken date script left "Order up to and including
        __ to take advantage" live for months
[ ] B11 no inherited foreign-language review or theme string is left on the page
        (a French review in the English grid, "webshop" in the carousel), and the
        spelling + idiom scans ran over the RENDERED page including that carousel
[ ] B6  every heading and subhead is DELIVERED by the content beneath it. Read each
        one, then read its items, and confirm the promise is actually kept. Watch the
        objection block: do not claim "what we fixed" or "why ours is different"
        unless the cards genuinely say so

## C. Imagery
[ ] C1  summary hero first, with offer badge if multibuy
[ ] C2  contents shot in slot 2
[ ] C3  BRANDED packaging shot in slot 3
[ ] C4  authority endorsement, caption overlaid on photo, no white panel
[ ] C5  2x before/after, different perspectives, one clean divider, no cross-bleed
[ ] C6  how-it-works diagram
[ ] C7  "as seen in" on a DIFFERENT base photo than the hero
[ ] C8  standalone offer image LAST (appended last, never reordered after)
[ ] C9  ZERO white/plain-background tiles left, gallery AND theme-side section images
[ ] C10 every tile carries the brand lockup where the recipe calls for it
[ ] C11 no photo used twice anywhere (list every image URL and diff them)
[ ] C12 every pre-existing GIF still present and referenced
[ ] C13 6-point quality gate on EVERY tile: photoreal not CGI, no anatomy glitches,
        high-res, shared palette, consistent product label, correct caption spelling
[ ] C14 counted objects match their captions (rods, straps, seams, pieces)
[ ] C16 the BRANDED product is visible and identifiable in EVERY UGC photo, and NO
        competitor wordmark appears on any background object
[ ] C17 multi-size product: a size-comparison image exists, placed early, with the
        rendered size step matching the true ratio rather than exaggerating it
[ ] C18 standalone offer image shows the real size range, not N identical packs,
        unless a multibuy tier genuinely exists
[ ] C15 all baked-in text in store language, accents rendered, large enough on mobile
[ ] C19 worn / on-body product: EVERY person render matches the operator's real
        wearing photos (which part touches which part of the body), not the
        generic stock pose. Rejected renders listed, not shipped
[ ] C20 before any productDeleteMedia: every theme-referenced image copied under
        a new filename via fileCreate and the template repointed
[ ] C21 default variant's mediaId = the hero, so the page opens on the hero
[ ] C22 every render looked at with Read individually, never as a contact sheet,
        and any nano_banana_pro tile is a text/logo band only, composited over a
        gpt_image_2 photo

## D. Browser-measured (these cannot be verified by reading your own markup)
[ ] D1  comparison table fits 375px, no side-scroll, no mid-word header break
[ ] D2  header/accent cells clear ~4.5:1 contrast (read computed color + background).
        The store brand green #04b67b is 2.67:1 and FAILS; use #046b4a in your blocks
[ ] D3  USP bullets: heavy ✔ in accent colour, ~20px gaps, one line each
[ ] D4  every benefit paragraph within 4 mobile lines
[ ] D5  specs row: single border, closed by default, label appears exactly once
[ ] D6  marquee actually animates; every logo visible
[ ] D7  UGC images actually load (force-load them: lazy images report 0x0 and lie)
[ ] D8  any horizontal overflow proven PRE-EXISTING by hiding your sections and
        re-measuring, or else fixed
[ ] D9  no pagepilot-* class on a default-template product; stars/badges non-empty
[ ] D10 final mediaCount matches what you attached, nothing silently dropped
[ ] D11 PagePilot: every pushed theme file's checksumMd5 equals the local md5 (the
        upsert response is always empty and proves nothing)
[ ] D12 the draft theme was duplicated from CURRENT main right before the push and
        only your template + snippets were layered on it; preview URL in the report
[ ] D13 the urgency/date banner prints a real date on the preview (IIFE + Liquid
        `{{ "now" | date }}` pre-fill), not an empty span

## E. Non-page deliverables
[ ] E1  cross-sell pick, chosen on BOTH fit and sales rank, trade-off stated
[ ] E2  variant / option / naming audit (cosmetic fixes done, structural ones proposed)
[ ] E3  Phase 5 hand-off checklist written
[ ] E4  every genuinely unfinished item stated explicitly in the report
[ ] E5  new reusable learnings saved to memory
```

**Then re-read your draft report against reality.** If a line says PASS but you
cannot point at the evidence, it is a FAIL. When every line is ticked, only then have
you earned "done".

## Gotchas checklist

- **Higgsfield accepts NO reference images at all in the current MCP build. Plan for
  it.** `medias` inside `params` is a hard validation error; `medias` at top level and
  `image_ids` are both accepted and then silently dropped (the stored job shows
  `"medias":[]`). `media_import_url` still returns a valid id that cannot be attached
  to anything. Consequences: (a) the targeted-EDIT technique is dead, so a good render
  with one wrong element cannot be repaired and must be fully re-rolled; (b) the
  product identity has to live entirely in the PROMPT TEXT. Write one canonical
  product paragraph and repeat it verbatim in every prompt of the set, spelling the
  brand letter by letter. On HydroSeal this produced a consistent, label-accurate
  product across a dozen tiles with zero references, so the workaround is good enough
  — just budget for whole-tile regenerations instead of edits. Memory
  `higgsfield-medias-silently-dropped`.
- **Fetch generation results with `job_display` (one `id` per call).**
  `show_generation_by_ids` rejects every argument shape tried. Avoid
  `show_generations`, which dumps every prompt in your history into context.
- **`gpt_image_2` can stall for 7+ minutes or return `status: "nsfw"` on brand
  wordmarks.** The "as seen in" press-logo tile came back `nsfw` on gpt_image_2 and
  rendered fine on `nano_banana_pro`. When a job passes ~5 minutes, fire the fallback
  in PARALLEL rather than waiting or cancelling, then pick the better result. On the
  offer image both completed and gpt_image_2 won because it put captions on the photo
  while nano put them in black boxes.
- **How to write a big PagePilot template: staged URL body, built by script.** This
  is the ONE method (PagePilot step 5 above). Earlier notes in this file claimed URL
  bodies write nothing and that the file must be retyped as a GraphQL block string;
  both were wrong and cost whole sessions. `body:{type:URL}` works (Nestilia ×8,
  Modlia ×3, OpenBeats ×2), the response is always empty, and `size` +
  `checksumMd5` are the only proof. The block-string paste (`"""…"""`, memory
  `graphql-block-string-theme-writes`) remains a fallback for a small file when
  staged uploads fail; never retype a template above ~30 KB by hand.
  - Move every legacy inline blob (SVG logos, payment strips, review sliders) and
    every custom section into `snippets/*.liquid` first so the template itself
    stays small and diffable. Say in your report which legacy elements you moved.
  - Build the new file with a script from the original, then unescape any `\uXXXX`
    back to literal UTF-8 and verify the unescaped text re-parses identically before
    writing. Some serialisers, PowerShell's `ConvertTo-Json` among them, escape every
    non-ASCII character by default, which inflates the file and your token count for
    no benefit.
  - **A too-large `graphql_query` result is auto-saved to a file** instead of
    entering context. Use that: fetch the template body, then parse the saved file
    with a script rather than reading 60 KB into context.
- **Inherited theme scripts can be broken on EVERY product template.** Nestilia's
  urgency banner (`Order by <span id=date>` + a date script) rendered an empty span
  on every page because the script never ran inside the section. Fix in the
  build: wrap the script in an IIFE AND pre-fill the span with Liquid
  `{{ "now" | date: "%A, %B %d" }}` so the sentence is correct even if JS fails.
  Read the rendered sentence on the preview to confirm (checklist B10 / D13).
- **Shopify SANITIZES HTML in section/block settings.** A `"type":"text"` block
  whose `settings.text` carries inline `style=` is rejected outright:
  *"Attribute 'style=…' contains styles that are not permitted on tag '<span>'"*.
  Styled markup (USP bullets with a coloured heavy `✔`, custom gaps) must live in a
  `pp_custom_liquid_block`, whose `content` accepts arbitrary HTML plus `<style>`.
  `<strong>` and `<p>` are still fine in a `text` block. Memory
  `pagepilot-text-block-strips-styles`.
- **Encoding: keep the script ASCII and the copy in a data file.** Accented text
  typed directly into a build script is the most reliable way to ship mojibake to
  a customer, because the script file's encoding and the interpreter's assumption
  disagree silently. The universal fix, on any platform and in any language: the
  script contains no accented characters at all, every string with accents lives in
  a UTF-8 JSON data file, and both reads and writes name UTF-8 explicitly. Then
  assert the output contains no `Ã` before you upload. **On Windows PowerShell 5.1
  specifically**, `.ps1` is read as ANSI unless the file carries a BOM, so `rachète`
  becomes `rachÃ¨te`; read with `[IO.File]::ReadAllText($p,[Text.Encoding]::UTF8)`
  and write with `[IO.File]::WriteAllText($p,$s,(New-Object Text.UTF8Encoding
  $false))`. Three more PowerShell traps that each cost a run: variables are
  case-INsensitive, so `$h` and `$H` collide; hyphenated JSON keys need quoting
  (`$m.blocks.'icons_with-text_x2enz4'`); and a `$(…)` subexpression containing
  `(function(){` mis-parses, so assign the JavaScript to a variable first. If `jq`
  is missing, every language named above parses JSON natively.
- **`productReorderMedia`: the omit-the-last-item workaround works.** Confirmed
  three times on Modlia with no loss. Move items to positions `0..n-2` and leave the
  intended final image out of the `moves` list entirely; it settles into the last
  slot by itself. Re-query `mediaCount` after every reorder regardless.
- `update-product` wants `id`, not `productId`.
- No em-dashes anywhere, including image captions and the FAQ accordion glyph
  (use `content:"\2212"` for the open-state minus, not an en-dash).
- PagePilot products (`templateSuffix` `pagepilot-…`): some gallery images are
  theme-side, not in product media — flag for separate handling.
- Use `_min.webp` (minUrl), never the raw PNG — keeps the store fast.
- Reviews/ratings you write are illustrative; tell the user so they can swap in
  real data.
- `templateSuffix: null` means NO PagePilot CSS. Never inherit `pagepilot-features`
  or `pagepilot-featuredReview` there; they render as invisible empty spans.
- Optimize the TITLE too, not just the description. It is the easiest step to forget.
- Render prominent-product graphics with `gpt_image_2` (real packshot as ref) for a
  PHOTOREAL product; nano_banana is fallback only. `gpt_image_2` defaults to
  `quality:"low"` — always force `quality:"high"`. Fix one broken element (bottle,
  foot, label colour) with a targeted gpt_image_2 EDIT, not a full re-roll.
- Before finalizing, LOOK at every generated image for: CGI-looking product,
  anatomy glitches (six toes/fingers, merged limbs), low resolution, off-palette or
  wrong background, and inconsistent product label/colour across tiles. The operator
  repeatedly caught these; reading your own prompt is not enough.
- `/products/<handle>.js` is edge-cached and can lie. The Admin API is the truth.
- Description images → `fileCreate`. Gallery images → `productCreateMedia`.
- `productReorderMedia` silently deletes the image at the highest `newPosition`.
  Append the final image last and never reorder it. Re-check `mediaCount` after
  every reorder.
- Never delete an existing packaging photo as "fabricated" without asking first.
- Generate one extra UGC shot and discard the weakest; the hit rate is low.
- Verify the final page live before reporting done, by MEASURING it in the browser,
  not by re-reading the HTML you just wrote.
- **The package-contents box must be big enough to hold the product.** Operator
  rejected a box drawn shorter than the folded panel it supposedly ships in. Work
  out the product's real closed dimensions FIRST, then state them in the prompt
  ("the folded panel is about 59 inches long, so the carton must be clearly LONGER
  than it and deep enough to contain it"). Check it at verify time: could this
  object physically fit in that box? Fix with a targeted edit, not a re-roll.
- **Rebrand EVERY plain-white tile, do not just leave it.** See "White and plain
  background tiles" in Phase 3.
- **Specs and package contents belong in a COLLAPSIBLE row in the buy box**, not
  only in a long section far down the page. See Phase 1 item 16.
- **Never stack your own border on top of a theme divider.** A custom block with
  `border-bottom` sitting next to the theme's own 1px divider renders as two lines
  and operators notice. Measure the actual rendered lines around any block you
  insert and keep exactly one separator per side.
- **Theme styles bleed into custom blocks — set BACKGROUND as well as colour, and
  never ship a bare `<th>`/`<td>`/`<tr>`.** This is the most repeated operator
  correction on this skill; it has been given many times across runs, so treat it as
  mandatory rather than as a debugging tip. Two real failures: a plain `<ul>`
  inherited the theme's link colour and shipped purple ticks with blue text; and a
  bare `<th>` in the buy-box specs table inherited a near-black fill with light
  text, so every spec label rendered as a black block (operator: *"turn the black
  background into white one and keep the font black"*). The trap is that you never
  wrote a background at all, so re-reading your own CSS can never reveal it — the
  theme's global `table`/`th` rule is the only source. So in EVERY custom-liquid
  block you ship:
  - Force `background:#fff!important; background-image:none!important` on `table`,
    `tr`, `th`, `td` and any card/list wrapper, unless you deliberately want a fill,
    in which case declare that fill explicitly with `!important`.
  - Force `color` with `!important` on every text node: headings, `th`, `td`, list
    items, tick glyphs, captions and notes.
  - Neutralise inherited `text-transform` and `letter-spacing` on `th`.
  - VERIFY in the browser by reading the computed `backgroundColor` AND `color` of
    each `th`/`td` and asserting the pair clears ~4.5:1. Never trust your own CSS.
- **`themeDuplicate` is ASYNC and will silently overwrite a write made too early.**
  Poll `theme(id){processing}` until it is `false` AND the target file is present
  before `themeFilesUpsert`, then re-read the file size to confirm your write stuck.
  This cost a silent lost edit on a real run.
- **`themeFilesUpsert` is blocked against the live theme.** If your backup gets
  published mid-run, duplicate again and write to the new draft. `themeFilesDelete`
  is blocked outright (even on a draft) — you cannot clean up your own probe files,
  so do not create throwaway assets you would need to remove.
- **`body: {type: URL}` recipe** (re-verified on Nestilia 2026-08-14 with a
  ~160 KB template written EIGHT times, and again on OpenBeats 2026-09-05):
  1. `stagedUploadsCreate(resource: BULK_MUTATION_VARIABLES, mimeType: "text/plain",
     httpMethod: POST)`
  2. `curl -F` POST the file to the returned target with all returned parameters
  3. `themeFilesUpsert` with
     `body:{type:URL, value:"https://storage.googleapis.com/shopify-staged-uploads/<key>"}`
  **The response is ALWAYS `{"upsertedThemeFiles":[],"userErrors":[]}` — empty, no
  errors — whether it worked or not. That response is meaningless; ignore it.** Verify
  by re-reading `size` and `checksumMd5`. Shopify did NOT minify these templates, so
  the returned `size` matched the local byte count exactly every time, which makes
  byte-for-byte comparison a reliable check. Full recipe in memory
  `theme-write-url-body-works`.
- **Never `Read` a whole PagePilot template into context** (75 KB measures ~85k
  tokens and truncates). Let the oversized `graphql_query` result auto-save to a
  file and parse that file with a script; the build script edits it, you never do.
- **Check `platform_customizations.custom_css` in `config/settings_data.json`
  before debugging any "my text is invisible" report.** On Modlia it contained
  `ul li {color:#ffffff !important;}`, which whitens EVERY list on the storefront
  and silently broke a spec section's checklist. Fix it at the source by scoping it
  (`footer ul li {…}`) instead of out-specifying it in every block you add. Do NOT
  rewrite `settings_data.json` yourself to do it — that one file also holds the
  colour schemes, app embeds and announcement bar, and it is whole-file-write only;
  hand the operator the one-line change instead.
- Shopify **minifies** the template on save, so a pretty-printed 158 KB file coming
  back as 77 KB is normal, not truncation. Verify by reading a value back, not size.
- **Operator-reordered the ToePerfect/Nestilia page in the theme editor after
  delivery — that reorder is now the proven section order, not the earlier draft.**
  NOTE: point (1) is SUPERSEDED by "THE CANONICAL SECTION ORDER" in the very next
  bullet, which the operator corrected again on TravelPouch. How-it-works and the
  UGC grid now come BEFORE the comparison table and objection refutation, not after
  them. Point (2) still stands. Two changes: (1) how-it-works moved from right after
  the benefit blocks to right before the UGC grid; (2) the TrustPilot-style review carousel (heading + slick-slider)
  was split off from the native review grid and moved to the very end of the page
  — after the closing CTA and the urgency/date banner — while the native grid
  stayed early, right after the risk-reversal CTA. See the updated section-order
  list and A-checklist above; this is now the default to build on the first pass,
  not something to wait for the operator to fix by hand again.
- **THE CANONICAL SECTION ORDER — build exactly this, first pass, every time.**
  Read back off the TEMPLATE FILE (not the rendered page, which can be cached) on
  TravelPouch / Nestilia 2026-08-12 AFTER the operator reordered it by hand. This
  **supersedes point (1) of the ToePerfect note directly above**: the operator has now twice moved
  the teaching-and-proof pair (how-it-works, then the UGC grid) ABOVE the
  argue-and-defend pair (comparison table, then objection refutation). The logic is
  show them how easy it is and who else uses it, and only then argue against the
  alternatives. Do not put the comparison table straight after the stat block.
  Whenever you finish a run, re-fetch `templates/product.*.json` and diff the
  `order` array against this list; if the operator has moved anything, update this
  list in the skill rather than assuming your own write survived. Page-level
  `order` array:

  ```
   1 main                          (buy box, see block order below)
   2 tp_aso                        as-seen-in marquee
   3 tp_pinterest                  Pinterest viral / low stock
   4 tp_problem                    problem / agitation
   5 image_with-benefits           benefit #1 + the 4-benefit grid
   6 image_with-text               benefit #2
   7 image_with-text               benefit #3
   8 image_with-text               benefit #4
   9 image_with-percentage         stat block (all percentages 90-99)
  10 tp_howitworks                 how it works, 3 steps
  11 tp_ugc                        UGC customer-photo grid
  12 tp_compare                    comparison table
  13 tp_objections                 objection refutation
  14 call_to-action                risk reversal
  15 review_grid                   NATIVE review grid (early)
  16 faqs                          Amazon-backed FAQ
  17 tp_closing                    trust/payment row + closing CTA
  18 custom_liquid (urgency)       date / discount banner
  19 custom_liquid (trustpilot)    TrustPilot heading
  20 custom_liquid (carousel)      TrustPilot carousel, DEAD LAST
  ```

  And the `main` section's `block_order` (the buy box), also operator-corrected:

  ```
   1 star rating          8 stock alert          15 divider
   2 title                9 offer banner         16 review_numbers
   3 subtitle            10 buy_buttons          17 review_block (featured review)
   4 price               11 sticky ATC + payment 18 USP bullets  <- LAST, under the review
   5 discount label      12 trust icons
   6 payment / shipping  13 specs + in the box
   7 divider             14 (specs sits directly under the trust icons)
  ```

  The USP bullets moved to the very bottom of the buy box, directly beneath the
  featured review, on operator instruction. Give them their own single `border-top`
  there, because the theme renders no divider after the review block.
- **Fallback only: chunked block-string paste.** If staged uploads are unavailable,
  a 150 KB template can still be pasted into ONE `themeFilesUpsert` `body:{type:
  TEXT, value:"""…"""}` by `Read`-ing it in ~8 chunks of 13-15K characters and
  pasting them back to back. The usual failure is a real newline inside a JSON
  string transcribed as a literal `\n` outside any string; Shopify answers with a
  location-free `"Invalid JSON in <filename>"`. `body:{type:BASE64}` does not help
  (GraphQL literals cannot be concatenated). Treat this as the last resort; the
  staged URL body is the default.
- **`switch-shop` invalidates the Shopify connector.** After switching stores the
  next call fails until the operator reconnects the MCP; say so and wait, do not
  retry in a loop.

# Winning Product Ledger — find-winning-products-2.0

Persistent anti-exhaustion state (SKILL.md §31). Load every section before a run; update every
section after a run. The spreadsheet is still the master source of truth for dedupe (§32) — this
ledger is what lets the search strategy itself improve run over run, and what backstops the
spreadsheet if it is briefly unreachable.

## SEEN_PRODUCT_IDS
WinningHunter IDs already evaluated (qualified or rejected), so a run never re-fetches or
re-scores the same row.

### 2026-09-08 (run 1 of the day)
- 1260750122119171 (Seure Apple Watch band, Meta) — qualified, delivered TEST NOW
- 1454583159242928 (Vega Ring stacking set, Meta) — qualified, delivered TEST NOW
- 986246334209468 (AirStyler Pro 6-in-1, Meta) — qualified, delivered TEST NOW
- 27156347597386572 (Vaoth Infinity Lamp, Meta) — qualified, delivered TEST NOW
- 847832694450978 (Toddla Montessori Busy Board, Meta) — qualified, delivered WATCH (sold out)
- 1622702748607165 (Gourmetific Cookware Set, Meta) — qualified, delivered WATCH (sold out)
- 1447345176809196 (LDN LUNA Fajas Colombianas, Meta) — qualified, delivered WATCH (sold out)
- 1082368799926274 (Lhanel Pilates Kit, Meta) — qualified, delivered WATCH (sold out)
- 2239643873228733 (Setago AutoFold Pro, Meta) — qualified, delivered WATCH (unverified)
- Pinterest pin 687295152692 (Adora Delight Handiva) — qualified, delivered TEST NOW
- Pinterest pin 687312387169 (Dironia chiffon skirt) — qualified, delivered WATCH (sold out)
- ~30 further Meta/Pinterest ids scanned and rejected by the discovery agents (established brand,
  image-only media, empty shopify_shopifydomain, duplicate concept) — full per-search detail not
  retained here to keep this file lean; see run report in conversation for the breakdown.

## SEEN_DOMAINS
Store domains already evaluated, one line each, with the niche and the outcome (qualified /
rejected / recheck).

### 2026-09-08 (run 1)
- seure.co — Men's fashion — qualified, TEST NOW
- vegaring.com — Women's fashion — qualified, TEST NOW
- aceandtaylor.com — Beauty — qualified, TEST NOW
- adoradelightusa.com (redirects from adoradelight.com) — Healthcare — qualified, TEST NOW
- vaoth.com — Lighting — qualified, TEST NOW
- toddla.co — Hobbies — qualified, WATCH (sold out)
- dironia.com — Women's fashion — qualified, WATCH (sold out) — NOTE: dironia.com already has a
  Lighting product delivered in an earlier run; this is a distinct product/niche, not a repeat
- gourmetific.com — Home care — qualified, WATCH (sold out)
- weareluna.store — Underwear — qualified, WATCH (sold out); feed URL 404'd, correct URL recovered
  via site search
- lhanel.co — Fitness — qualified, WATCH (sold out)
- setago.co — Car accessories — qualified, WATCH (unverified — page did not fully render)
- brinoa.com — REJECTED (Fitness/posture-corrector search) — "Cerviless Pro" is an exact duplicate
  of the product already delivered 2026-08-17 under minopia.com; brinoa.com itself already has 2
  other products delivered under Beauty in prior runs
- weareluna.store (2nd hit, shapewear/DE) — REJECTED — blank shopify_shopifydomain in that
  particular row (this appears to be the operator's own store per prior session context)
- Numerous marketplace/established-brand domains rejected across both Pinterest agents and both
  expansion agents: amazon.com/amzlink.to, ebay.com, wayfair.com, temu.com, walmart.com,
  target.com, homedepot.com, shein.com, lightinthebox.com, plus established brands (FitVille,
  Ölend, Melinda Maria, OGEE, Storelli, Inno Supps, Quntis, Dreamegg, Bon Charge, HOTO, Ottocast,
  Asarai, Tiny Land, Mighty Paw, BAEBROW, Hermosa Hair, Dokotoo (watch, not full reject), ecozy
  (watch, not full reject))

## SEEN_PRODUCT_CONCEPTS
Underlying product concepts already delivered or rejected as duplicates — not store-specific, so a
different brand selling the same object is caught here even under a new domain.

### 2026-09-08 (run 1)
- Magnetic silicone Apple Watch band — NEW, delivered (Seure)
- Sterling silver stacking ring set — NEW, delivered (Vega Ring)
- 6-in-1 ceramic hot-air styler ("Airwrap dupe") — NEW, delivered (AirStyler Pro)
- Electric handheld neck/shoulder kneading massager — NEW concept for the ledger, but delivered
  product (Handiva) is itself resold under >=2 storefronts (Adora Delight + Valcero) — low moat,
  flagged in killers
- Infinity-mirror upcycled-bottle lamp — NEW, delivered (Vaoth)
- All-inclusive kids arts & crafts kit — NEW, delivered (Craftikit)
- Vitamin C/niacinamide brightening serum duo — NEW, delivered (EQQUALBERRY)
- Mandelic acid body-acne serum — NEW, delivered (Level 2)
- Multi-use waterproof car seat cover towel — NEW, delivered (Sprints)
- Under-desk walking pad with incline — NEW, delivered (YAGUD)
- Cordless rechargeable heating pad/uterus warmer belt — NEW, delivered (Comfytemp)
- Montessori busy board — NEW, delivered (Toddla, WATCH/sold out)
- Chiffon/polka-dot midi-length skirt — NEW, delivered (Dironia, WATCH/sold out)
- Ceramic non-stick cookware set — NEW, delivered (Gourmetific, WATCH/sold out)
- Fajas Colombianas post-surgical shapewear — judged sufficiently distinct from the generic
  tummy-control bodysuits already in the master sheet (Lovushape, Bombonds, Floralshe) on the
  post-surgical/medical-adjacent positioning; delivered WATCH/sold out
- Pilates/reformer accessory kit — NEW, delivered (Lhanel, WATCH/sold out)
- Portable car desk (fold-out laptop/writing surface) — NEW, delivered (Setago, WATCH/unverified)
- **Posture corrector "Cerviless Pro"** — DUPLICATE (already delivered 2026-08-17 under a different
  store domain) — REJECTED
- **Generic tummy-control bodysuit shapewear** (SHAPERX zip-up bodysuit from TikTok) — judged a
  duplicate concept of Lovushape/Bombonds/Floralshe already delivered — REJECTED, not delivered
- **Generic leather bifold wallet** (TikTok candidates + Meta's Forge Wallet) — judged a duplicate
  concept of Dailyardplus wallet already delivered under Men's fashion — REJECTED, not delivered
- **Ab/core toning machine** (RELIFESPORTS foldable ab machine, Megelin SlimCore toning belt) —
  judged duplicate concept of CoreDisk/PostureFlex/Marnetic PowerFlex/Ultrabooty already delivered
  — REJECTED, not delivered
- **Neck/shoulder massager** (Omumax, Noxa Massager, BodyAlign pillow) — self-duplicate within this
  run's own Healthcare pick (Handiva already filled that slot) — not delivered, kept as watchlist

## SEEN_KEYWORDS
Keywords already searched, with language, country (or "global"), and outcome, so §29's "before
running a search, check SEARCH_HISTORY" rule has something to check against.

### 2026-09-08 (run 1) — see full per-keyword breakdown in the conversation's run report.
Summary: ~35+ Pinterest keyword/country combos across all 10 niches (US then DE), ~12 TikTok
keyword/country combos (DE returned zero results for every TikTok query — see SEARCH_HISTORY),
~10 Meta niche-code/country combos (US full depth, DE only reached Beauty/Lighting/Underwear).
High-yield keywords (kept qualifying rows): "posture corrector" (US), "neck massager" (US),
"seamless underwear" (US), "midi skirt" (US) on Pinterest; niches FT/HT/SP/LS on Meta US p1.
Zero-yield keywords worth deprioritizing next run: "diamond painting", "scrapbooking kit",
"herrenhemd"/"herren armbanduhr" (DE), "car organizer"/"car vacuum" (US, all marketplace noise),
"led strip lights"/"galaxy projector" (US, near-zero video volume).

## SEARCH_HISTORY
One line per search actually run: `date | endpoint | keyword | language | country | page/scroll |
candidates | new_candidates | qualifying`.

### 2026-09-08 (run 1)
Full log retained in the conversation transcript (4 parallel discovery agents' search logs). Key
structural finding: TikTok Shop DE coverage is zero — 5 separate DE queries (localized keywords,
English keywords, no keyword) all returned `meta.total: 0`. Record this so future runs do not
re-spend budget on TikTok DE queries; go straight to TikTok US + Meta DE instead.
Meta DE pass was only run for Beauty/Lighting/Underwear this run (time-budgeted) — Home care, Car
accessories, Fitness, Healthcare, Hobbies, Men's and Women's fashion DE were never queried on Meta
this run — top of the list for next run's Germany-priority pass.
No dedicated Pinterest HISTORICAL (mindays/maxdays "last year" window) pass was run separately —
Pinterest's live-ads endpoint already surfaces long-running survivors within the normal live sweep
(several qualifiers this run were already 300-650+ days old), so a distinct historical pass was
folded into Pass 1. A true seasonal-window historical sweep (§25) is still owed for a future run.

## REJECTED_PRODUCTS
`product | reason | rejected_date | recheck_after (or "permanent")` — per §36. Brand/trademark risk
is normally permanent; everything else gets a recheck date.

### 2026-09-08 (run 1)
- Brinoa "Cerviless Pro" Posture Corrector | duplicate of existing minopia.com listing | 2026-09-08 | permanent
- SHAPERX Zip-Up Tummy Control Bodysuit (TikTok) | duplicate concept (generic shapewear bodysuit) | 2026-09-08 | permanent unless a genuinely distinct mechanism variant appears
- Forge Wallet / TikTok leather bifold wallets | duplicate concept (Dailyardplus wallet already delivered) | 2026-09-08 | permanent unless a genuinely distinct wallet mechanism appears
- RELIFESPORTS foldable ab machine / Megelin SlimCore toning belt | duplicate concept (ab/core device oversaturated) | 2026-09-08 | permanent unless distinct mechanism
- Vollyc Vacuum System | collection-page only, ambiguous HKD/USD pricing, some variants >$200 | 2026-09-08 | recheck after 2026-10-01 with a direct single-product link
- HINU Growth Oil (Meta) | fails 30-day floor (20 days) | 2026-09-08 | recheck after 2026-09-25 (~35 days live)
- FemPDRN Balm (Meta) | barely clears 30-day floor, weak differentiation vs other Beauty picks this run | 2026-09-08 | recheck after 2026-09-25

## QUALIFIED_PRODUCTS
Products that cleared every gate in a given run, whether or not they were ultimately delivered
(niche cap, dedupe against a stronger duplicate, etc.) — kept so a near-miss isn't re-discovered
and re-scored from scratch next run.

### 2026-09-08 (run 1)
All 17 delivered products (11 TEST NOW + 6 WATCH) qualified and were delivered — see
DELIVERED_PRODUCTS below. No qualified-but-undelivered overflow this run (niche caps were not
exceeded by the candidate pool).

## DELIVERED_PRODUCTS
Products actually written to the spreadsheet, one dated block per run — mirrors the sibling skill's
ledger format so the two stay easy to cross-check:

## 2026-09-08 (run 1 of the day — via /find-winning-products-2.0)
- Seure Fearless Silicone Magnetic Band for Apple Watch — seure.co — 1260750122119171 — Men's fashion — US — SOURCE: Meta — TEST NOW
- Vega Ring Morning Dew Stacking Ring Set — vegaring.com — 1454583159242928 — Women's fashion — US — SOURCE: Meta — TEST NOW
- AirStyler Pro 6-in-1 (Ceramiq Pink) — aceandtaylor.com — 986246334209468 — Beauty — US — SOURCE: Meta — TEST NOW
- Adora Delight Handiva Neck & Shoulder Massager — adoradelightusa.com — pin 687295152692 — Healthcare — US — SOURCE: Pinterest — TEST NOW
- Vaoth Infinity Lamp (bottle upcycle) — vaoth.com — 27156347597386572 — Lighting — US — SOURCE: Meta — TEST NOW
- Craftikit 20-Piece Arts & Crafts Kit — TikTok Shop 1729485968684716209 — Hobbies — US — SOURCE: TikTok — TEST NOW
- EQQUALBERRY Vitamin Illuminating Duo — TikTok Shop 1732315297481462699 — Beauty — US — SOURCE: TikTok — TEST NOW
- Level 2 Mandelic Acid Body Acne Serum — TikTok Shop 1729666844449280302 — Beauty — US — SOURCE: TikTok — TEST NOW
- Sprints Car Seat Cover Towel — TikTok Shop 1729498071032043102 — Car accessories — US — SOURCE: TikTok — TEST NOW
- YAGUD Walking Pad w/ Incline — TikTok Shop 1729492505494853464 — Fitness — US — SOURCE: TikTok — TEST NOW
- Comfytemp Cordless Heating Pad / Uterus Warmer Belt — TikTok Shop 1731166125700190658 — Healthcare — US — SOURCE: TikTok — TEST NOW
- Toddla Montessori Busy Board — toddla.co — 847832694450978 — Hobbies — US — SOURCE: Meta — WATCH (sold out)
- Dironia White & Black Polka Dot Chiffon Skirt — dironia.com — pin 687312387169 — Women's fashion — US — SOURCE: Pinterest — WATCH (sold out)
- Gourmetific Cookware Set — gourmetific.com — 1622702748607165 — Home care — US — SOURCE: Meta — WATCH (sold out)
- LDN LUNA Fajas Colombianas Shapewear — weareluna.store — 1447345176809196 — Underwear — DE — SOURCE: Meta — WATCH (sold out)
- Lhanel Pilates Kit — lhanel.co — 1082368799926274 — Fitness — US — SOURCE: Meta — WATCH (sold out)
- Setago AutoFold Pro Portable Car Desk — setago.co — 2239643873228733 — Car accessories — US — SOURCE: Meta — WATCH (unverified)

## RECHECK_QUEUE
Emerging winners (§35) and recheckable rejects (§36) due for another look, with the date they
become worth rechecking.

### From this run (recheck_after dates above), plus:
- **All 6 WATCH products above** — recheck stock status in 2-3 weeks (~2026-09-22 to 2026-09-29);
  Lhanel Pilates Kit (639-day survivor, 9/10 Pinterest fit) and Gourmetific Cookware Set (574-day
  survivor) are the highest-priority rechecks in this batch.
- **Vaoth Infinity Lamp, Level 2 Mandelic Acid Serum, YAGUD Walking Pad** — TEST NOW on product
  signal but "no qualifying supplier" found this run — re-run supplier sourcing with more search
  term variations before committing ad budget.
- **Near-misses reported by the discovery agents** (not qualified, but close): Norla Organic Cotton
  Boxer Briefs (glizm.com, 39 repins vs 50 needed), several products blocked purely by an empty
  `shopify_shopifydomain` field despite an obviously-Shopify storefront (Auto-Transforming Cube
  desk toy/shopicco.com, Mechanic Toolbox Mug/alohave.com, a shoe-rack organizer video at 6,777
  repins/48 ads/380 days — the single strongest raw signal found this run, blocked only by that
  field) — worth a manual theme/CMS check next run rather than a hard API-field trust.
- **HINU Growth Oil** and **FemPDRN Balm** — see REJECTED_PRODUCTS recheck dates above.

## LEARNING LOG (§54)
End-of-run notes on which keyword families, languages, markets, historical windows, and niches
produced the highest new-qualifying rate (§55) — read this before planning the next run's depth
allocation.

### 2026-09-08 (run 1)
- **Best source this run: Meta** (27 raw qualifiers, 9 delivered) and **TikTok** (25 raw
  candidates, 6 delivered) — both far outperformed direct Pinterest keyword search (only 4
  qualifiers total across ~35 keyword/country combos). Pinterest's own "live ads" endpoint is
  extremely sparse for video + dropship-Shopify + repin>=50 simultaneously; most keyword hits are
  either big-brand/marketplace noise or image-only.
- **Best niche: Beauty** (3/3 delivered, all TEST NOW, two from TikTok with 6-figure 30-day
  revenue). **Worst niches: Lighting and Car accessories on Pinterest specifically** (zero
  qualifiers from ~14 combined keyword/country searches) — Meta/TikTok rescued both niches.
- **Best market: USA**, as mandated — nearly every qualifier came from US-targeted searches. DE
  coverage was thin this run (Meta DE only reached 3/10 niches, TikTok DE returned zero results
  platform-wide) — Germany-priority depth is the clearest gap to close next run.
- **Structural finding worth weighting into future runs**: a striking fraction (5 of 12, ~42%) of
  Shopify-hosted Meta/Pinterest candidates that cleared every WinningHunter-reported gate were
  **sold out** on live verification despite strong/scaling ad spend. This matches a pattern also
  seen in an earlier run today (Corecare, ReabTec). Recommend budgeting for live-page verification
  as a near-universal filter, not an edge case, and treating "sold out despite spend" as its own
  tracked category (their ads are still working — worth recheck in 2-3 weeks rather than discard).
- **Keyword family worth reusing**: TikTok's revenue-sorted keyword search (no niche filter needed)
  produced a much higher new-qualifying rate than Pinterest's fuzzy keyword match — prioritize
  TikTok keyword search depth over additional Pinterest keyword variations next run.
- **Adjacent path to explore next run**: winner-derived and store-derived search loops (§22/§23)
  were not run this time (budget went to breadth across 10 niches x 2 markets instead) — next run
  should spend some budget chasing the Handiva/Valcero double-listing and the Fajas Colombianas
  concept across US/global keyword search per §13's cross-market expansion rule.

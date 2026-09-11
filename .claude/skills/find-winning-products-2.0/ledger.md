# Winning Product Ledger — find-winning-products-2.0

Persistent anti-exhaustion state (SKILL.md §31). Load every section before a run; update every
section after a run. The spreadsheet is still the master source of truth for dedupe (§32) — this
ledger is what lets the search strategy itself improve run over run, and what backstops the
spreadsheet if it is briefly unreachable.

## SEEN_PRODUCT_IDS
WinningHunter IDs already evaluated (qualified or rejected), so a run never re-fetches or
re-scores the same row.

### 2026-09-11 (run 4 — PINTEREST-ONLY, READY-TO-SHIP BAR — 2nd course correction)
**Why this run exists**: operator feedback on run 3: "the last result is still as not expected."
Asked directly what was wrong (via AskUserQuestion rather than guessing a 3rd time) and got 3
concrete answers: (1) too few products overall, (2) too many WATCH/sold-out rows, (3) the
video-only gate was too strict for Pinterest — plus a 4th, unprompted but critical: several
delivered rows had no real Pinterest link, AliExpress link, or COGS (run 3's WATCH rows used
`pending` placeholders for supplier/COGS since sold-out items weren't sourced). Operator's answer on
tradeoffs: keep repin/ad-count/day thresholds strict, but allow image ads (not just video).
**This run's design change**: each of the 5 discovery agents now runs a complete 3-stage pipeline
per candidate — (1) Pinterest hard-gate qualification with BOTH image and video accepted,
(2) live stock verification via WebFetch, (3) real AliExpress supplier sourcing via WebFetch — and
only returns a candidate if it clears ALL THREE. Nothing sold-out, dead-linked, or supplier-less is
returned as a "result" at all; those are logged as "found but not deliverable" for the record but
never written to the sheet. This directly fixes complaint (2) and (4) by construction — every
delivered row is complete by definition. It does not fully fix complaint (1): allowing image ads
raised the raw candidate pool, but the strict traction gates plus the now-364-then-368-row
exclusion index (this skill's own prior 3 runs have saturated several niches already) meant only
3 products survived the full pipeline. See LEARNING LOG for the explicit tradeoff writeup.
- Pinterest pin 687293690694 (Madepants Utility Pants) — qualified, delivered TEST NOW
- Pinterest pin 687307541814 (SohoBloo SmoothSilk Epilator) — qualified, delivered TEST NOW
- Pinterest pin 687317792733 (LumeVibe Car Door Projector) — qualified, delivered TEST NOW
- ~15 candidates cleared Stage 1 (Pinterest traction gates) but failed Stage 2 (sold out/dead link)
  or Stage 3 (no qualifying supplier) — see REJECTED_PRODUCTS/RECHECK_QUEUE below, full detail in
  conversation transcript.
- 6 of 10 niches (Hobbies, Women's fashion, Home care, Underwear, Healthcare, Lighting) returned
  zero end-to-end survivors — mostly concept-saturation against this sheet's own prior 3 runs'
  deliveries (posture correctors, neck massagers, wall sconces, shapewear all explicitly flagged
  as "mined out" by the agents), not a search-depth failure.

### 2026-09-10 (run 3 — PINTEREST-ONLY, operator-requested course correction)
**Why this run exists**: after run 2 delivered mostly Meta/TikTok-sourced products, the operator
said explicitly: "results are still not expected. I want results to be mostly pinterest winners."
This was a legitimate critique — §14 says Pinterest is the *primary* source and Meta/TikTok are
*expansion only*, but runs 1-2 both leaned on Meta/TikTok for volume because direct Pinterest
keyword search (2-4 keywords/niche/market) was too shallow to fill niches on its own. This run
fixes that by actually doing the exhaustive multi-keyword-family (§19, families A-I) x multi-market
sweep the skill spec calls for, using Pinterest ONLY — zero Meta/TikTok tool calls.
**Also on load**: the live sheet was re-read fresh and run 2's entire 29-product delivery
(rows 363-391) was gone too — a third concurrent-write collision (see LEARNING LOG). Given the
operator's message arrived at the same time, it's plausible this was the operator clearing results
they didn't want rather than another session's accident; either way, this run did not attempt to
restore run 2's Meta/TikTok-heavy set — it replaces that approach entirely rather than patching it.
**Result: exhaustive Pinterest-only search across all 10 niches found only 8 qualifying candidates
total**, and only 1 confirmed in stock. This is the honest yield of prioritizing source-purity over
volume — see full breakdown in DELIVERED_PRODUCTS and LEARNING LOG below.
- Pinterest pin 687308366734 (GlowBare hair removal serum, Marnetic) — qualified, delivered TEST NOW (under $25 floor, flagged)
- Pinterest pin 687314997020 (Tiktrove scalp massage comb) — qualified, delivered WATCH (price hidden on live page)
- Pinterest pin 687299035734 (Shana Paris lash serum) — qualified, delivered WATCH (HTTP 402 on verification)
- Pinterest pin [Swivolt Max wireless car charger, nimebrand.com] — qualified, delivered WATCH (sold out)
- Pinterest pin 687313751047 (CoreLift Posture Bra, shop-rosemary.co.uk) — qualified, delivered WATCH (sold out, currency corrected USD→GBP)
- Pinterest pin 687312387169 (Dironia chiffon skirt) — re-surfaced independently a 3rd time, still sold out — delivered WATCH
- 2 more qualifying-but-not-delivered: Skale lash serum (skalecosmetics.com, US) and Ausbury lash
  serum (ausbury.co.uk, GB) — both cross-validate the eyelash-serum concept but were not delivered
  to avoid stacking 3 near-identical products; logged for the recheck queue instead.
- ~15 near-misses and ~30+ dedupe rejections across the 5 discovery agents — see SEEN_PRODUCT_CONCEPTS
  and REJECTED_PRODUCTS below; full per-keyword search logs retained in the conversation transcript
  (roughly 250+ keyword x market combinations run — Hobbies 39, Women's fashion + Home care ~30
  before one agent hit a context limit mid-sweep, Beauty + Underwear ~50, Car + Fitness 62,
  Healthcare + Lighting ~75).

### 2026-09-10 (run 2)
**CRITICAL CONTEXT FOR THIS RUN**: on load, the live spreadsheet was read fresh and found to have
lost ALL 17 products delivered in run 1 (2026-09-08) — rows 343-359 had been overwritten by at
least one other session's write (a 10-product run dated 2026-09-08 in a different format, then a
4-product Halloween-scoped run dated 2026-09-10) that did not read the sheet fresh before writing.
This is a **concurrent-write collision**, not data corruption on this skill's part — see LEARNING
LOG below for the operational implication. 16 of the 17 lost products were re-verified live today
(not copied blind) and re-delivered with today's date; 1 (Setago AutoFold Pro) was dropped after
its product page failed to render on 2 separate verification attempts, 2 days apart.
- 1260750122119171 (Seure) — re-verified live, re-delivered TEST NOW
- 1454583159242928 (Vega Ring) — re-verified live, re-delivered TEST NOW
- 986246334209468 (AirStyler Pro) — re-verified live, re-delivered TEST NOW
- 27156347597386572 (Vaoth) — re-verified live, re-delivered TEST NOW
- 847832694450978 (Toddla) — re-verified STILL sold out, re-delivered WATCH
- 1622702748607165 (Gourmetific) — re-verified STILL sold out, re-delivered WATCH
- 1447345176809196 (LDN LUNA) — re-verified STILL sold out, re-delivered WATCH
- 1082368799926274 (Lhanel) — re-verified STILL sold out, re-delivered WATCH
- 2239643873228733 (Setago) — UNVERIFIABLE 2nd time running — DROPPED, not re-delivered
- New this run: Firewalky (firewalky.com), Favvity (favvity.com), Hyperblade Cervitrax
  (hyperbladeusa.com), INTERGREAT (TikTok 1732261179638190676), INNERSY (TikTok
  1729544355421196668) — qualified, delivered TEST NOW
- New WATCH (sold out/unverified): 3D Relief Art Pen (cur8trend.com), MEMO Whiteboard Wallet
  (newthingslab.com), Shape-curve 2pc Set (shape-curve.com), Pinauto (pinauto-store.com), LumeAuto
  (lumeauto.com), Blauzone (blauzone.com), LumiBeam (trylumibeam.com), SwanSway (swanswaywear.com)
- ~40 further Meta/Pinterest/TikTok ids scanned and rejected across 4 discovery agents (established
  brand, duplicate concept, price out of band, insufficient traction) — see SEEN_PRODUCT_CONCEPTS
  and REJECTED_PRODUCTS below.

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

## 2026-09-11 (run 4 — PINTEREST-ONLY, READY-TO-SHIP BAR, via /find-winning-products-2.0)
3 delivered, ALL TEST NOW, ALL SOURCE: Pinterest, ALL with a real Pinterest link + real AliExpress
supplier link + real COGS (no placeholders — this was the explicit fix this run made).
- Madepants Men's Vintage-Inspired Casual Utility Pants — madepants.com — Men's fashion — US — image ad — TEST NOW
- SohoBloo SmoothSilk 2-in-1 Hair Removal Epilator & Trimmer — shopsohobloo.com — Beauty — US — video ad — TEST NOW
- LumeVibe Car Door Logo Projector Light — mylvera.com — Car accessories — US — video ad — TEST NOW (only 8 left in stock on live check — recheck soon)

## 2026-09-10 (run 3 — PINTEREST-ONLY, via /find-winning-products-2.0)
6 delivered (1 TEST NOW + 5 WATCH), ALL SOURCE: Pinterest. Niches with zero qualifying candidates
after exhaustive search: Hobbies, Men's fashion, Home care, Underwear, Fitness, Lighting.
- GlowBare Smooth Skin Hair Removal Serum — marnetic.com — Beauty — US — SOURCE: Pinterest — TEST NOW (in stock, but $17.95 < $25 floor, margin-risk flagged)
- Tiktrove Electric Spray Air Cushion Massage Comb — tiktrove.com — Beauty — Global — SOURCE: Pinterest — WATCH (price hidden on live page)
- Shana Paris Premium Lash Serum — shanacosmetics.com — Beauty — US (historical, days_min=180) — SOURCE: Pinterest — WATCH (HTTP 402 on verification)
- Swivolt Max Wireless Car Charger & Mount — nimebrand.com — Car accessories — US (historical) — SOURCE: Pinterest — WATCH (sold out)
- CoreLift Posture Bra — shop-rosemary.co.uk — Healthcare — GB — SOURCE: Pinterest — WATCH (sold out, currency corrected)
- Dironia White & Black Polka Dot Chiffon Skirt — dironia.com — Women's fashion — US — SOURCE: Pinterest — WATCH (sold out, 3rd consecutive check)

## 2026-09-10 (run 2 — via /find-winning-products-2.0)
16 recovered from run 1 (re-verified, not copied blind) + 13 new = 29 total (16 TEST NOW + 13 WATCH).
- Seure Fearless Silicone Magnetic Band for Apple Watch — seure.co — Men's fashion — US — SOURCE: Meta — TEST NOW (recovered)
- Vega Ring Morning Dew Stacking Ring Set — vegaring.com — Women's fashion — US — SOURCE: Meta — TEST NOW (recovered)
- AirStyler Pro 6-in-1 — aceandtaylor.com — Beauty — US — SOURCE: Meta — TEST NOW (recovered)
- Adora Delight Handiva Massager — adoradelightusa.com — Healthcare — US — SOURCE: Pinterest — TEST NOW (recovered)
- Vaoth Infinity Lamp — vaoth.com — Lighting — US — SOURCE: Meta — TEST NOW (recovered)
- Craftikit 20-Piece Arts & Crafts Kit — TikTok Shop — Hobbies — US — SOURCE: TikTok — TEST NOW (recovered)
- EQQUALBERRY Vitamin Illuminating Duo — TikTok Shop — Beauty — US — SOURCE: TikTok — TEST NOW (recovered)
- Level 2 Mandelic Acid Body Acne Serum — TikTok Shop — Beauty — US — SOURCE: TikTok — TEST NOW (recovered)
- Sprints Car Seat Cover Towel — TikTok Shop — Car accessories — US — SOURCE: TikTok — TEST NOW (recovered)
- YAGUD Walking Pad w/ Incline — TikTok Shop — Fitness — US — SOURCE: TikTok — TEST NOW (recovered)
- Comfytemp Cordless Heating Pad/Belt — TikTok Shop — Healthcare — US — SOURCE: TikTok — TEST NOW (recovered)
- Toddla Montessori Busy Board — toddla.co — Hobbies — US — SOURCE: Meta — WATCH (recovered, still sold out)
- Dironia Chiffon Skirt — dironia.com — Women's fashion — US — SOURCE: Pinterest — WATCH (recovered, still sold out)
- Gourmetific Cookware Set — gourmetific.com — Home care — US — SOURCE: Meta — WATCH (recovered, still sold out)
- LDN LUNA Fajas Colombianas — weareluna.store — Underwear — DE — SOURCE: Meta — WATCH (recovered, still sold out)
- Lhanel Pilates Kit — lhanel.co — Fitness — US — SOURCE: Meta — WATCH (recovered, still sold out)
- Firewalky 360 Rotating Faucet — firewalky.com — Home care — DE — SOURCE: Meta — TEST NOW (new)
- Favvity Balance Board — favvity.com — Fitness — DE — SOURCE: Meta — TEST NOW (new, supplier mechanism mismatch flagged)
- Hyperblade Cervitrax Gen 2 — hyperbladeusa.com — Healthcare — US+DE double-validated — SOURCE: Meta — TEST NOW (new)
- INTERGREAT Folding Bed — TikTok Shop — Home care — US — SOURCE: TikTok — TEST NOW (new)
- INNERSY Plus-Size Underwear 4-Pack — TikTok Shop — Underwear — US — SOURCE: TikTok — TEST NOW (new)
- 3D Relief Art Pen — cur8trend.com — Hobbies — US — SOURCE: Meta — WATCH (new, sold out)
- MEMO Whiteboard Wallet — newthingslab.com — Men's fashion — US — SOURCE: Meta — WATCH (new, sold out, price rose $89→$99)
- Shape-curve 2pc Set — shape-curve.com — Women's fashion — US — SOURCE: Meta — WATCH (new, unverifiable)
- Pinauto Trunk Organizer — pinauto-store.com — Car accessories — US — SOURCE: Meta — WATCH (new, unverified, currency corrected USD→GBP)
- LumeAuto Door Projector Light — lumeauto.com — Car accessories — DE — SOURCE: Meta — WATCH (new, unverifiable)
- Blauzone Reader Night Light — blauzone.com — Lighting — US — SOURCE: Pinterest — WATCH (new, sold out, no supplier)
- LumiBeam Portable Projector — trylumibeam.com — Lighting — US — SOURCE: Meta — WATCH (new, sold out)
- SwanSway Push-Up Bra — swanswaywear.com — Underwear — US — SOURCE: Meta — WATCH (new, sold out)

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

### 2026-09-11 (run 4) — the explicit volume-vs-completeness tradeoff, quantified
Run 3 predicted this tradeoff; run 4 measured it. Adding a hard "must verify in-stock AND must
source a real supplier before counting as a result" bar (fixing the operator's complaints about
incomplete WATCH rows) on top of run 3's already-strict repin/ad/day gates dropped the deliverable
count from 8 (run 3, mostly WATCH/incomplete) to 3 (run 4, all complete). Allowing image ads (the
other operator-requested change) widened the Stage-1 candidate pool noticeably per agent report,
but nearly all of the extra volume died at Stage 2 (sold out) or Stage 3 (no AliExpress match) —
**the bottleneck has moved from "can we find candidates" to "can we verify and source them,"** which
loosening the media-type filter doesn't fix. **The lever that would actually raise the count from
here is the repin/ad-count/day thresholds themselves** (operator explicitly chose to keep these
strict this run) — if a future run wants more than a handful of products from Pinterest-only
search, that's the parameter to revisit, not search breadth (which is now genuinely near-exhausted
for many niches given 4 runs' worth of accumulated exclusion-index saturation).
- **Only niche combo with zero Stage-1-to-Stage-3 survivors across ALL FOUR runs so far**:
  Healthcare + Lighting on the 4th attempt again returned nothing new — every qualifying hit was a
  duplicate of a posture-corrector/neck-massager/wall-sconce concept already in the sheet. These two
  niches are the most saturated in the whole 10-niche set at this point.
  Underwear is close behind (zero new in runs 3 and 4; the one promising store found in run 4 had
  its entire catalog stuck on a broken "ships after 19041994" placeholder — a data-quality problem
  on WinningHunter's index, not a gate failure).
- **Beauty and Car accessories/Men's fashion remain the most productive niches** across runs 3-4
  (5 of 8 run-3 candidates were Beauty; run 4's 3 deliverables spread across Men's/Beauty/Car,
  the same three niches that also produced run 3's one delivered TEST NOW).
- **Dead links and broken stock flags are becoming a recurring Stage-2 failure mode**, not just
  "sold out" — hudsongrace.co.uk had rebranded/redirected mid-run, eaksone.com 404'd, mrsaker.com's
  entire storefront shows a broken date placeholder. Treat "store appears broken" as its own category
  in future runs' near-miss logs, distinct from ordinary stock-outs.

### 2026-09-10 (run 3) — Pinterest-only course correction: what exhaustive search actually costs
This run answers a question runs 1-2 left open: what does the mission's actual spec (§14: Pinterest
primary, Meta/TikTok expansion-only; §19: full A-I keyword-family sweep) yield if followed strictly?
**Answer: far fewer products, and most of what survives is WATCH, not TEST NOW.** ~250+ keyword x
market searches across 5 parallel agents, all 10 niches, US/DE/GB/global markets, plus a
historical-survivor pass, returned only 8 qualifying candidates — and after live verification, only
1 was confirmed purchasable. 6 of 10 niches (Hobbies, Men's fashion, Home care, Underwear, Fitness,
Lighting) returned genuinely zero qualifying candidates, not from thin search effort but from thin
underlying inventory — the agents' logs show hundreds of raw hits per niche, the overwhelming
majority static-image or duplicate-mechanism (same posture corrector/neck massager/copper-wire
lights resold by 3-4 storefronts each). **This is the real, structural tradeoff the operator should
know about going forward**: Meta/TikTok-inclusive runs (1-2) delivered 17-29 products with maybe
40-60% eventually confirmable in stock; a Pinterest-only run delivers a genuine handful with the
same ~10-15% in-stock rate on top. Neither number is a search failure — they're accurately measuring
two different things (Pinterest's actual current ad-creative mix vs. a broader cross-platform net).
Recommend making this tradeoff explicit to the operator each run rather than assuming which they want.
- **Best niche this run**: Beauty (5 of 8 total qualifiers, and the only 1 confirmed-in-stock pick).
  Beauty's Pinterest video-ad inventory is meaningfully deeper than every other niche checked.
- **Cross-market validation worth noting**: "eyelash serum" independently qualified from 3 unrelated
  stores across 3 markets (Skale/US, Shana Paris/US-historical, Ausbury/GB) — strong evidence this
  specific concept is a genuine, currently-live Pinterest trend, even though only 1 was delivered.
- **Historical-survivor pass (days_min=180) pulled its weight**: 2 of the 8 total qualifiers
  (Shana Paris lash serum, Swivolt Max charger) were found only via this pass, not the base search.
  Keep running it every time — cheap and it surfaces real durable-survivor evidence the live sweep
  alone misses.
- **Agent context limits are a real constraint on "exhaustive"**: one agent (Women's fashion/Home
  care) hit a hard context/tool-call limit mid-sweep and had to wrap up honestly with partial
  coverage rather than fabricate the rest. For niches where this matters, consider narrower
  per-agent scope (1 niche, not 2) if a future run needs guaranteed-complete coverage logs.

### 2026-09-10 (run 2) — MOST IMPORTANT FINDING: concurrent-write collision
This run opened by discovering that run 1's entire 17-product delivery had been overwritten by
another session's write to the same spreadsheet range. **Operational lesson for every future run,
this skill or the sibling**: "read the last populated row, then append" is not safe against two
sessions running close together — the second session's read can be stale by the time it writes.
There is no locking mechanism available here. Mitigations for next time: (1) always re-read the
live sheet immediately before the actual write call, not just at the start of the run (this run did
that and it caught a SECOND round of concurrent writes — rows 357-362 appeared between this run's
initial read and its final write); (2) if a large date-stamped gap in row content looks suspicious,
verify against this ledger's DELIVERED_PRODUCTS before assuming the spreadsheet's absence means
"not yet delivered"; (3) consider recommending the operator stagger scheduled runs of the different
skills so they don't overlap.
- **Stock-out rate keeps compounding**: this is now the 3rd run in a row (2 by this skill, 1 by
  whatever produced the 09-08/09-10 sibling-format rows) to find a large fraction of qualifying,
  ad-spending products sold out on live verification. This run: 8 of 11 newly-found live-checked
  candidates (73%) were sold out or unverifiable. Across run 1 + run 2 combined: of 23 total
  Shopify-storefront products live-checked, 13 were sold out and 3 more were unverifiable — barely
  30% were cleanly confirmed purchasable. **This should now be treated as the expected base rate,
  not an anomaly** — budget verification time accordingly in every future run, and consider it a
  genuine data-quality property of the WinningHunter Meta/Pinterest feed, not bad luck.
- **Best source this run**: Meta again dominated (most of the 13 new qualifiers), across both the
  Germany-priority sweep and the buyer-language US sweep. TikTok contributed 2 solid new picks
  (INTERGREAT, INNERSY). Pinterest contributed 1 (Blauzone, via the winner-derived loop) — direct
  Pinterest keyword search on its own remains the weakest channel, consistent with run 1.
- **Germany-priority sweep, closing last run's gap**: productive — 14 tabled DE candidates across
  the 7 niches never reached in run 1. Pinterest DE keyword depth is still nearly a dead end (only
  1 of ~21 DE Pinterest keyword searches cleared the full gate — Wecro Berlin's PosturePro); Meta DE
  carried nearly all of the DE yield. Recommend future DE passes go straight to Meta niche-code
  search and treat Pinterest DE keyword search as low-priority effort.
- **Winner-derived loop, run for the first time**: productive on "neck shoulder massager" (6
  independent qualifying competitors to Handiva found) — confirms this is a real, currently-scaling
  crowded sub-niche worth watching, though only 1 (Hyperblade Cervitrax, via a distinct
  traction-not-massage mechanism) was added to avoid stacking near-duplicate massagers. Store-derived
  expansion (inspecting winning stores' other catalogue items) was a dead end — all 3 checked stores
  (seure.co, vegaring.com, aceandtaylor.com) are narrow single-hero-product shops with nothing else
  to harvest; deprioritize store-derived search for single-SKU-family stores in future runs.
- **Buyer-language keyword search (vs. product-name search) on Meta**: productive — surfaced a
  genuinely different set of advertisers (FunPunch, MEMO Whiteboard Wallet, Shape-curve, etc.) than
  product-name or niche-code search would have. Worth keeping as a standing technique.
- **Best niche this run**: Healthcare (3/3 delivered as TEST NOW — Adora Delight, Comfytemp,
  Hyperblade — first niche to go 3-for-3 clean in either run). **Weakest**: Lighting and Car
  accessories again, same as run 1 — both ended up majority-WATCH after live verification even
  though discovery itself found candidates easily in both.

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

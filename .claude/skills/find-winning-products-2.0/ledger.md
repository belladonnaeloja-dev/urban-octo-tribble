# Winning Product Ledger — find-winning-products-2.0

Persistent anti-exhaustion state (SKILL.md §31). Load every section before a run; update every
section after a run. The spreadsheet is still the master source of truth for dedupe (§32) — this
ledger is what lets the search strategy itself improve run over run, and what backstops the
spreadsheet if it is briefly unreachable.

## SEEN_PRODUCT_IDS
WinningHunter IDs already evaluated (qualified or rejected), so a run never re-fetches or
re-scores the same row.

### LINK-COLUMN FIX PART 2 — column AD (applied 2026-09-11, covers rows 363-374 / runs 4-6)
Operator: "for column AD, if you can't find pinterest link, add the ad library link of the
product." Column AD ("All their live ads") was still `n/a - Pinterest pin, no Meta ad archive`
for every Pinterest row even after the AA/AC fix below. Checked all 12 rows via
`get_pinterest_ad` and every single one has a `page_url` field — the advertiser's Pinterest
business profile (e.g. `https://www.pinterest.com/skalecosmetics`) — which is the genuine
Pinterest equivalent of "all their live ads" (all their live pins). Wrote that to column AD for
all 12 rows, labeled "Pinterest profile (all pins)". None of the 12 needed the Meta Ad Library
fallback the operator described, since a Pinterest link was found every time — but the fallback
rule stands for any future row where `page_url` is missing/blank: search the Meta Ad Library for
that store's page (`https://www.facebook.com/ads/library/?active_status=active&ad_type=all&q=<store
name>`) and use that instead of leaving `n/a`.
**Going forward**: every future run's row-builder script must populate column AD with the ad's
`page_url` field (Pinterest profile), falling back to a Meta Ad Library search link only when
`page_url` is genuinely unavailable — never leave it as an `n/a` placeholder.

### LINK-COLUMN FIX (applied 2026-09-11, covers rows 363-374 / runs 4-6)
Two link-column bugs found and fixed after delivery, both purely cosmetic (no data was ever
missing, only mislabeled/misplaced):
1. Column AA ("Open in WinningHunter") had every Pinterest-sourced row's HYPERLINK display text
   set to "WinningHunter" pointing at the raw `pinterest.com/pin/<id>` URL — correct link, but
   nothing in the cell visually signaled it was a Pinterest pin, which read as if the pin link
   were simply missing. Operator caught this twice.
2. Once flagged, operator specified the actual intended layout: column AA should hold a genuine
   WinningHunter platform deep-link (`https://app.winninghunter.com/ad/<id>?platform=pinterest`,
   matching the established Meta convention `.../ad/<id>?platform=facebook` already used
   elsewhere in this sheet), and column AC (previously "The winning ad (Meta)", holding an
   `n/a - Pinterest pin, no Meta ad archive` placeholder for every Pinterest row) should hold the
   actual `pinterest.com/pin/<id>` link instead. Fixed both for all 12 affected rows. The `<id>`
   used is WinningHunter's own `id`/`productid` field for that ad — for most pins this is a plain
   numeric Pinterest pin ID, but for a minority (confirmed via a live re-query for the Livaé row)
   it's an opaque base64-style mobile share-token instead of a numeric ID; either form is valid
   and resolves, and both column AA and AC now consistently use whichever form that ad's `id`
   field actually is.
**Going forward**: every future run's row-builder script must set column AA to the constructed
`app.winninghunter.com/ad/<id>?platform=pinterest` link (not a "WinningHunter"-labeled pin link)
and column AC to the actual Pinterest pin link — not an `n/a` placeholder — for every
Pinterest-sourced row.

### 2026-09-14 (run 7, ROUND 2 — operator asked for 5 more to complete the 10/day target)
After round 1 delivered 5, the operator said: "find 5 products more to complete the 10 daily
required." Rebuilt the exclusion index again (411 entries, including round 1's deliveries and
every round-1 reject by name so round 2 wouldn't resurface them) and launched two more discovery
agents with explicit instructions to avoid every keyword/country combo already tried in round 1
and push into genuinely new angles (FR/ES markets, seasonal Halloween/Christmas, new keyword
families) rather than re-running exhausted searches — per §29.
**Result**: round 2 found 6 raw candidates across ~98 additional keyword searches (40 for
Healthcare/Lighting/Car accessories, 58 for Underwear/Men's fashion/Fitness/Women's fashion) plus
~10 more manual follow-up searches. Stage C verification narrowed that to **3 more delivered**
(total for the day: **8 of 10**):
- Healthcare, Car accessories, Fitness, Men's fashion, Hobbies, Home care: **zero** qualifying
  candidates survived to Stage C in round 2 either — Fitness and Men's fashion in particular were
  pushed hard (35+ combined searches) and came back completely empty; every gate-clearing hit was
  a big-brand/marketplace domain (Amazon, SHEIN, Temu, eBay, Kohl's, Brooks Brothers, Old Navy,
  LightInTheBox). This is now confirmed structural for these 6 niches under the current gates and
  Pinterest-only sourcing, not a search-effort gap — 2 full rounds (round 1 + round 2) have both
  come back empty or near-empty for the same niches.
- **Rhinestone Jeans (glizm.com, 4,460 repins)** — closed out this round. Checked the store's own
  `/search/suggest.json` endpoint directly (a more authoritative check than the earlier
  `/products.json` and on-site search attempts) — the product is genuinely absent from the store's
  own search index entirely, not just under a different handle. Confirmed **DELISTED**, not merely
  unverifiable. Downgrade from "HIGH PRIORITY RECHECK" to closed/likely-permanent.
- **Cécile™ Maxi Chemise Intemporelle** and **Peignoir Betty™ Camel** (both zoeparis.fr, 351 and
  79 repins) — found, would likely have qualified (both from an established French dropship
  store), but the domain failed DNS resolution (`getaddrinfo EAI_AGAIN`) on 3 separate fetch
  attempts including a `www.` variant. This reads as a genuinely unreachable/down domain rather
  than bot-blocking (bot-blocking returns HTTP 403, not a DNS failure) — logged to RECHECK_QUEUE,
  worth a retry in a future run since the domain may come back.
- **Créole Rym earrings (belizebijoux.com)** — a new sourcing pattern worth noting: the qualifying
  Pinterest ad promoted the store's whole earrings collection page, not one specific product.
  Rather than reject it outright, fetched the collection page and used the store's own
  "BEST-SELLER" tag to identify the single SKU (Créole Rym, €34) the ad's traction most plausibly
  reflects, then verified that specific product. This is a judgment call — the 76 repins/10 ads
  belong to the collection ad, not confirmed per-SKU — flag this pattern for future runs: prefer a
  product-specific ad when available, but a collection ad pointing to a clearly-marked bestseller
  is a reasonable fallback rather than discarding real traction evidence outright.
- Pinterest pin AVhlvN45KCb02en6zJa2SsGBXjyE9AX3w3Qx3zmrnB25xn-b7piy6c-KFA37m0pI_11axNvhuWmTNNqcWi5wC_Q
  (Veilleuse Guirlande Lumineuse LED avec Pinces Photo, luminaire-lucciano.com) — qualified,
  delivered TEST NOW (margin risk, live price under $25)
- Pinterest pin 687309701010 (Collier Rainbow, tapioca-bijoux.com) — qualified, delivered TEST NOW
  (adscount exactly at the 5 floor; currency correction from the API's mistagged USD to the live
  EUR price)
- Pinterest pin 687285961402 (Créole Rym earrings, belizebijoux.com) — qualified, delivered TEST
  NOW (sourced via the collection-ad-to-bestseller-SKU pattern described above)

**Final honest count for 2026-09-14: 8 of the requested 10.** Did not pad the remaining 2 with a
lower-quality candidate (the DNS-unreachable zoeparis.fr items, or a borderline/duplicate-risk
reject) to hit the round number — see LEARNING LOG for what's actually left to try.

### 2026-09-14 (run 7)
**Load state**: on load, found the sheet had grown from 374 rows (end of run 6) to 408 rows — the
sibling `find-winning-products` skill ran multiple times on 2026-09-13 and 2026-09-14, adding 34
new products (rows 375-408), mostly Women's fashion (dresses/skirts/cardigans/boots), a Car
accessories/Christmas-holiday batch, and misc footwear. Rebuilt the exclusion index fresh from the
live sheet (394 entries, product+store+niche) rather than trusting master-history.tsv alone, per
§32 "spreadsheet wins." Interesting finding: Swivolt Max (nimebrand.com), delivered as WATCH in
run 3, was NOT in the fresh exclusion index — confirms it was part of the "deliberate manual
cleanup" noted in run 5's load (run 3's WATCH rows were removed from the sheet at some point
between run 3 and run 5) and is legitimately re-discoverable. It resurfaced this run and was
re-verified independently (still sold out, same as run 3 — consistent finding, not re-delivered).
**Result**: 4 parallel discovery agents ran ~155 keyword x market Pinterest searches at the current
standing gates (repins>=20, ads>=5, days>=30, image/video) across all 10 niches, surfacing 22 raw
candidates. Stage C verification (live stock + real AliExpress supplier) cut that to **5
deliverable** — noticeably harder than run 6's 7, and the attrition was almost entirely Stage C,
not discovery breadth or Stage B gates:
- Sold out on live check: Electric Spray Comb (tiktrove.com — same store/product flagged
  unreliable in run 3 too), The Men Pen (themenpens.com), Kierstin Lingerie (dulcestoreparis.com),
  Swivolt Max (nimebrand.com, re-confirmed), Logan Sunglasses (glizm.com), Men's Boxers
  (mrsaker.com — backorder date literally reads "19041994", a data bug, but functionally
  unavailable), Pleated Pinstripes Capris (elysianclo.store — 404, not just sold out)
- Unverifiable (persistent bot-blocking or connection failures across multiple retries), NOT
  written per §40: Eclipse Retro Wall Light (tudoandco.com — HTTP 403 on 2 separate URL variants),
  RGB Strobe LED Lamp (zorenza.de — connection refused 3x, a genuine network-level block not a
  store issue), PosturePro (wecro.de -> shopwecro.com — 2nd run in a row this exact
  store/product has failed to resolve to a working product page across a domain migration; flag
  this specific product+store combo as effectively dead for automated verification, recheck
  manually or drop from future rotations)
- **NEW failure mode this run**: Flower Child Flannel (vaguestudios.com) was confirmed IN STOCK
  at Stage B/live-check, but died at Stage C on the SUPPLIER side — no single AliExpress flannel
  shirt listing met BOTH the >=200-order AND >=4.5-star bar simultaneously (best options were
  1,000+ orders/4.3 stars OR 43 orders/4.9 stars). Held the line per §41 rather than accept a
  supplier below either threshold. This is the first run where a fully-verified-in-stock product
  was lost purely to the supplier-quality bar, not availability.
- One high-value candidate (**Rhinestone Jeans**, glizm.com, **4,460 repins** — by far the
  strongest single traction number found in any run to date) could NOT be verified despite
  extensive effort: the exact WinningHunter-reported product URL 404'd, and neither the store's
  broken on-site search nor browsing its 5,397-product catalog (via bestsellers collection and
  paginated `/collections/all`) ever surfaced a matching product page. Logged to RECHECK_QUEUE
  rather than guessed at or dropped — worth a dedicated retry next run given the traction size.
- Hobbies and Home care returned **zero raw candidates** from 52 combined keyword searches —
  every candidate that cleared numeric gates was on a big-brand/marketplace domain (Amazon, SHEIN,
  Temu, eBay, Etsy, Wayfair, Home Depot, Target, LEGO) with no Shopify storefield, confirmed as a
  structural feature of Pinterest's current ad mix in these niches, not a search-coverage gap.
  Healthcare, Lighting, Car accessories, Underwear also delivered zero after Stage C attrition.
- Beauty (3/3, at niche cap), Fitness (1), Women's fashion (1) were the only niches that delivered.
- Pinterest pin 687297282900 (BlendMate Portable Blender, margothale.com formerly ausbury.co.uk) —
  qualified, delivered TEST NOW
- Pinterest pin 687281266654 (Lissage Indien Kera Glow, lissage-au-top.com) — qualified, delivered
  TEST NOW
- Pinterest pin 687296086274 (Valentine's Whisper Corset Top, maisonzifan.com) — qualified,
  delivered TEST NOW (adscount exactly at the 5 floor — thin evidence beyond repins)
- Pinterest pin 687267534605 (BIO-Aloe Vera Splash 3-in-1, thatsme.organic) — qualified, delivered
  TEST NOW (margin risk, live price under $25)
- Pinterest pin 687289455279 (PureGlow Schwarztee-Gesichtsmaske, solenza.de) — qualified, delivered
  TEST NOW (margin risk + low stock, 4 units left)

### 2026-09-11 (run 6 — GATE-LOOSENING EXPERIMENT: repin_count/adscount 50/10 → 20/5)
**Why this run exists**: operator, on seeing run 5's 2-product result: "only 2 additional products
were added. i need 10 products every run." This is the run that finally tests the lever flagged
but not yet tried across runs 4-5's learning logs — lowering repin_count/adscount thresholds
(the near-miss evidence showed several candidates sitting at repins 30-45 / adscount 7-9, just
under the old 50/10 bars) — while explicitly keeping days_since_started>=30 (run 5 already proved
lowering that wasn't the answer), Pinterest-only sourcing, and full Stage 2/3 verification (no
WATCH/placeholder rows) intact, since those three were the operator's own prior explicit asks.
**Result**: 4 parallel discovery agents ran ~150 keyword x market Pinterest searches across all 10
niches at the loosened gates, surfacing 18 raw candidates (Beauty 7, Healthcare 4, Women's fashion
4, Underwear 1 [men's, wrong niche gender], Lighting 1, Home care 1, Men's fashion/Car
accessories/Fitness/Hobbies 0 each). Stage 2/3 verification then cut that to **7 deliverable** —
the highest fully-verified count of any run to date (beats run 4's 3 and run 5's 2 by 2-3x), though
still short of the operator's stated 10/run target. Verification attrition was the dominant filter,
not discovery: Eaksone Auto Tag Removal (product page 404, likely delisted), Brinoa Cerviless Pro
(sold out — also a known duplicate of a product delivered 2026-08-17 under minopia.com per
SEEN_DOMAINS run 1, so it would have been rejected either way), Onecompress Bamboo Gloves (sold
out), Eettsy Neck & Back Massager (site returns HTTP 403 to automated fetches — unverifiable, not
necessarily dead), PosturePro Haltungskorrektor (site migrated wecro.de → shopwecro.com and the
closest live match was a differently-named/differently-priced EMS posture device — treated as an
unconfirmed match, not delivered), Sac Moira Tote (live price €245 exceeds the $200 price ceiling —
original Pinterest-reported price of $164 was stale), Women's Three-Piece Trouser Suit (sold out)
all died at Stage 2. Sunset Pendant Light's AliExpress search initially returned only 166-184-order
suppliers (just under the 200-order bar) on an exact-match search term; a broader search term found
a 335-order/5-star supplier for the same product type, so it survived Stage 3 — the first Lighting
product to clear the full pipeline in 3 runs that tried that niche. Healthcare went from 4 raw
candidates to zero delivered (all 4 died at Stage 2/3) despite being historically this skill's
2nd-best niche (11 delivered all-time) — this is the clearest evidence that stock-out/verification
attrition, not gate tightness, is now the binding constraint on volume, at least for niches with any
real candidate supply. Men's fashion, Car accessories, Fitness, Hobbies, Underwear returned zero
qualifying candidates even at the loosened gates after 20-50 keyword combos each — confirmed
structurally weak/exhausted on Pinterest for this skill's fixed niche list, not a threshold problem.
- Pinterest pin 687304672304 (Skale Nail Growth Serum, skalecosmetics.com) — qualified, delivered
  TEST NOW (margin risk, live price under $25 floor)
- Pinterest pin 687310403037 (Skale Lash Growth Serum, skalecosmetics.com) — qualified, delivered
  TEST NOW — NOTE: same store as the Nail Serum above (distinct SKU, not a duplicate); also a soft
  concept-adjacency with Shana Paris Premium Lash Serum (delivered as WATCH in run 3) — both are
  eyelash growth serums from different stores/formulations, not blocked as an exact duplicate but
  flagged here for future dedup judgment
- Pinterest pin AYxf...(Livaé Facial Lifting Massager, helynshop.com) — qualified, delivered TEST NOW
- Pinterest pin 687280842742 (Diana Tricot Knit Waistcoat, luxevintage.co) — qualified, delivered
  TEST NOW
- Pinterest pin 687299304382 (Blakely Blaze Mini Dress, bymaara.com) — qualified, delivered TEST NOW
  (AliExpress supplier is a generic bohemian V-neck mini dress, closest high-volume equivalent, not
  an exact style clone — flagged for sample-check before ordering)
- Pinterest pin 687307613339 (KlarFix Transparent Dust-Proof Storage Bags, verlimo-shop.com) —
  qualified, delivered TEST NOW (margin risk, live price under $25 floor)
- Pinterest pin 4260609374221 (Sunset Pendant Light AFTERGLOW L1, monulo.com) — qualified, delivered
  TEST NOW

### 2026-09-11 (run 5 — days_min EXPERIMENT: lowered 30 → 15)
**Why this run exists**: operator asked to "lessen the days running to 50 days." Since the true
current floor was 30 (not something higher, as the phrasing implied), this was ambiguous — asked a
quick clarifying question rather than guess a direction on an expensive run, and the operator chose
to LOWER the floor to 15 (not raise to 50) to test whether it would increase volume, which is what
recent runs have been short on.
**On load**: found run 3's entire 6-product delivery (rows 363-368 at the time) gone from the sheet,
while run 4's 3 products (previously 369-371) were intact and had shifted up to fill 363-365. This
selective pattern — exactly the unsatisfactory (mostly-WATCH) run removed, the satisfactory
(all-TEST-NOW) run kept — reads as deliberate manual cleanup, not a session collision. Did not
attempt to restore run 3.
**Result — the experiment's answer**: lowering days_min from 30 to 15 did NOT meaningfully raise
volume. Same 5-agent, same-method sweep (~200+ searches) that found 3 clean deliverables at the
30-day floor found only 2 at the 15-day floor (one of them a borderline niche-fit call). This
confirms the hypothesis flagged in run 4's learning log: **days-running was never the actual
bottleneck** — it's the repin_count/adscount thresholds (kept strict throughout) combined with this
sheet's own accumulated exclusion-index saturation and Stage 2/3 (stock + supplier) verification
attrition. See LEARNING LOG for the explicit conclusion and recommended next lever.
- Pinterest pin 687313914180 (Zavonix PoutPower Lip Plumper) — qualified, delivered TEST NOW
- Pinterest pin 687299499265 (PistonPerk Spark Plug Novelty Mug, marnetic.com) — qualified,
  delivered TEST NOW, but flagged: this is an automotive-THEMED novelty desk item, not a functional
  car accessory — questionable fit for the Car Accessories niche, included with caveat rather than
  silently dropped or silently forced to fit.
- 8 of 10 niches (Hobbies, Women's fashion, Home care, Underwear, Fitness, Healthcare, Lighting, and
  arguably Car accessories given the mug's fit question) returned zero clean end-to-end survivors.
  Several strong candidates died at Stage 2/3 specifically because they were boutique/proprietary
  construction (two LEAU dresses — real traction, real stock, no AliExpress equivalent exists for
  their specific corset/knit construction) rather than commodity dropship goods — this is a new,
  distinct failure mode worth tracking (see LEARNING LOG).

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

- Pinterest pin 687299735097 (Eettsy Cupping Massager) — qualified, delivered TEST NOW (run 8)
- Pinterest pin 687288933364 (LEAU Ramona Corset Babydoll Mini Dress) — qualified, delivered TEST NOW (run 8)
- Pinterest pin 687290210437 (Tudo & Co Ito Wabi Sabi Pendant Light) — qualified, delivered TEST NOW (run 8)
- Pinterest pin 687295333990 (Ashoul/jdongvak Leather Drop Shoulder Jacket) — qualified, delivered TEST NOW (run 8, margin-flagged)
- Pinterest pin AYofrUdZkDq6kDVSVLwxEoZn84C7ic2GTgeet7YQnlMeWuG5w3r__yzNUdikuixTdXFvM6mKjQF5ub2IWRLU7S4 (theroyalcodes Indra Dress) — qualified, delivered TEST NOW (run 8)
- Pinterest pin 687300876961 (Dulce Store Paris Kierstin lingerie) — qualified but REJECTED (run 8, sold out at live check)
- Pinterest pin AcrXt-M8W1hGyzaZ9TI0ja6_LdC02b4njU5jFXb8uuXHH5PSOsPH3YuFj_qHXINii2KtTF2CXzRK4JLyXBN18G0 (DeluxeSkin LumaLift) — qualified but REJECTED (run 8, store down HTTP 423/402)
- Pinterest pin 4260609563741 (Hudson Grace/Claye 3-piece trouser suit) — qualified but REJECTED (run 8, delisted, 404 on both domains)
- Pinterest pin 687272065045 (Vakkerlight Minimalist LED Floor Lamp) — qualified but REJECTED (run 8, delisted/404)
- Pinterest pin 687270712886 (Vakkerlight Lantern Fabric Pendant Light) — qualified but REJECTED (run 8, no qualifying AliExpress supplier)
- Pinterest pin 687300057355 (LePharea CelAway 3-in-1) — REJECTED at Stage B (run 8, computed selling price 38.99 EUR, fails new 39 EUR gate)
- Pinterest pin 687294515093 (Zoe Paris Cécile Maxi Chemise) — qualified but REJECTED (run 8, still DNS-unreachable — 3rd failed attempt across 2 sessions, see RECHECK_QUEUE)
- Meta ad 793144933467995 (Pinauto Shop Trunk Organizer) — qualified, delivered TEST NOW (run 8b, Meta fallback, operator-authorized)
- Meta ad 1262220535372400 (Floralshe V-Shaped Bodysuit) — qualified, delivered TEST NOW (run 8b, Meta fallback)
- Meta ad 7866695093444584 (Joybos Smart Sensor Trash Can) — qualified, delivered TEST NOW (run 8b, Meta fallback)
- Meta ad 2427984170869017 (Lumos Knitting Light) — qualified, delivered TEST NOW (run 8b, Meta fallback)

## SEEN_DOMAINS
Store domains already evaluated, one line each, with the niche and the outcome (qualified /
rejected / recheck).

### 2026-09-14 (run 7)
- margothale.com (formerly ausbury.co.uk, 301 redirect) — Fitness — qualified, TEST NOW
  (BlendMate Portable Blender)
- lissage-au-top.com — Beauty — qualified, TEST NOW (Lissage Indien Kera Glow)
- maisonzifan.com — Women's fashion — qualified, TEST NOW (Valentine's Whisper Corset Top)
- thatsme.organic — Beauty — qualified, TEST NOW (BIO-Aloe Vera Splash 3-in-1)
- solenza.de — Beauty — qualified, TEST NOW (PureGlow Schwarztee-Gesichtsmaske)
- tiktrove.com — REJECTED (this SKU) — Electric Spray Air Cushion Massage Comb sold out; this
  store's product feed is also structurally broken (product_title/handle/price all null in the
  raw API data) — same store flagged unreliable in run 3 too, treat future Tiktrove candidates
  with extra suspicion
- themenpens.com — REJECTED — The Men Pen sold out on live check
- dulcestoreparis.com — REJECTED — Kierstin Strass Lingerie Set sold out on live check
- nimebrand.com — REJECTED (re-confirmed) — Swivolt Max still sold out, same finding as run 3;
  this product/store combo is not in the current exclusion index (its run-3 WATCH row was removed
  from the sheet at some point) but keeps failing stock verification independently — worth a
  RECHECK_QUEUE entry with a longer interval rather than re-trying every run
- glizm.com — MIXED — Logan Retro Sunglasses sold out (rejected); Rhinestone Jeans (4,460 repins,
  by far the strongest traction found to date) could not be located on the live site despite
  exhaustive search of a 5,397-product catalog — logged to RECHECK_QUEUE, not rejected outright
- mrsaker.com — REJECTED — 2 Pack Men's Sexy Pouch Boxers shows a backorder date literally reading
  "19041994" (data bug on the store's side) — functionally unavailable regardless of the cause
- elysianclo.store — REJECTED — Pleated Pinstripes Capris 404s (delisted), not merely sold out
- tudoandco.com — UNVERIFIABLE — Eclipse Retro Wall Light returns HTTP 403 to automated fetches on
  two separate URL variants (with and without www/en-us prefix) — likely bot-blocking, recheck
  manually
- zorenza.de — UNVERIFIABLE — RGB Strobe LED Lamp connection-refused on 3 separate fetch attempts —
  looks like a network-level block specific to this domain, not a store-side stock issue
- wecro.de / shopwecro.com — UNVERIFIABLE (2nd run in a row) — PosturePro/Haltungskorrektor could
  not be resolved to a working product page across a domain migration in both run 6 and run 7;
  treat this specific store+product as effectively dead for automated verification going forward
  rather than re-attempting every run

### 2026-09-11 (run 6)
- skalecosmetics.com — Beauty — qualified TWICE (Nail Growth Serum + Lash Growth Serum, distinct
  SKUs, both delivered TEST NOW)
- helynshop.com — Beauty — qualified, TEST NOW (Livaé EMS+LED facial massager)
- luxevintage.co — Women's fashion — qualified, TEST NOW (Diana Tricot Knit Waistcoat)
- bymaara.com — Women's fashion — qualified, TEST NOW (Blakely Blaze Mini Dress)
- verlimo-shop.com (formerly verlimo.de, 301 redirect) — Home care — qualified, TEST NOW (KlarFix
  storage bags)
- monulo.com — Lighting — qualified, TEST NOW (Sunset Pendant Light AFTERGLOW L1)
- eaksone.com — REJECTED — Pinterest-advertised "Auto Tag Removal Kit" no longer resolves on the
  live store (404 on guessed URL, not in site search or full collection listing) — likely delisted
- brinoa.com — REJECTED — Cerviless Pro posture corrector is SOLD OUT on live check; also already
  flagged as a duplicate of a product delivered under minopia.com back in run 1 (see 2026-09-08
  entry below)
- eettsy.com — UNVERIFIABLE — returns HTTP 403 to automated fetches on every path tried (product
  page, collections, homepage) — likely bot-blocking, not necessarily dead; recheck manually
- onecompress.com — REJECTED (this SKU) — Bamboo Compression Gloves explicitly marked "Out of
  stock" on live page; other Onecompress products (socks, sleeves) untested this run
- shopwecro.com (formerly wecro.de, 301 redirect) — REJECTED — the Pinterest-advertised
  "PosturePro Haltungskorrektor" could not be confirmed at this domain; closest live match was a
  differently-named, differently-priced EMS posture device — treated as unconfirmed, not delivered
- latelierdemalte.com — REJECTED (this SKU) — Sac Moira tote's live price (€245) exceeds the $200
  ceiling; Pinterest-reported price ($164) was stale
- hudsonclaye.com (formerly hudsongrace.co.uk, 301 redirect) — REJECTED — Women's Three-Piece
  Trouser Suit is SOLD OUT on live check

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

- adoradelightusa.com (adoradelight.com redirects here) — Healthcare — qualified, delivered TEST NOW (run 8)
- eettsy.com — Beauty — qualified, delivered TEST NOW (run 8)
- leauclothing.com — Women's fashion — qualified, delivered TEST NOW (run 8)
- tudoandco.com — Lighting — qualified, delivered TEST NOW (run 8)
- jdongvak.com (ashoul.com redirects here) — Men's fashion — qualified, delivered TEST NOW (run 8, margin-flagged)
- theroyalcodes.com — Women's fashion — qualified, delivered TEST NOW (run 8)
- dulcestoreparis.com — Underwear — rejected (run 8, sold out)
- deluxeskin.uk / trydeluxeskin.com — Beauty — rejected (run 8, store suspended, HTTP 423/402)
- hudsongrace.co.uk / hudsonclaye.com — Women's fashion — rejected (run 8, delisted)
- vakkerlight.com — Lighting — rejected (run 8, 1 product delisted, 1 no qualifying supplier)
- lepharea.fr — Beauty — rejected (run 8, computed selling price fails new 39 EUR gate)
- zoeparis.fr — Women's fashion — recheck (run 8, still DNS-unreachable, 3rd attempt)
- pinauto-store.com — Car accessories — qualified, delivered TEST NOW (run 8b, Meta)
- floralshe.com — Underwear — qualified, delivered TEST NOW (run 8b, Meta; store has another SKU already in this index — distinct product, not a re-list)
- joybos.com — Home care — qualified, delivered TEST NOW (run 8b, Meta)
- lumoslumos.com — Hobbies — qualified, delivered TEST NOW (run 8b, Meta; niche classification judgment call — LED product sold as a knitting accessory, kept out of Lighting)

## SEEN_PRODUCT_CONCEPTS
Underlying product concepts already delivered or rejected as duplicates — not store-specific, so a
different brand selling the same object is caught here even under a new domain.

### 2026-09-14 (run 7)
- Portable USB-rechargeable personal blender/smoothie maker — NEW concept, delivered (BlendMate)
- At-home keratin/Indian hair-straightening treatment — NEW concept, delivered (Kera Glow) —
  distinct from nail/lash serums and hair-loss oils already on the sheet
- Standalone corset top (not part of a skirt/dress set) — NEW concept, delivered (Valentine's
  Whisper) — distinct from the two "corset skirt set" entries already excluded
- Multi-use aloe vera hair/face/body spray — NEW concept, delivered (BIO-Aloe Splash)
- Tea-based clay/stick face mask — NEW concept, delivered (PureGlow)
- Y2K rhinestone/patchwork cargo jeans — NEW concept, NOT delivered (Rhinestone Jeans,
  unverifiable — see RECHECK_QUEUE); worth tracking since 4,460 repins is the strongest signal any
  candidate has shown across all 7 runs

### 2026-09-11 (run 6)
- Nail growth serum — NEW concept, delivered (Skale Nail Growth Serum)
- Eyelash growth serum — SOFT DUPLICATE of Shana Paris Premium Lash Serum (delivered WATCH, run 3)
  — different store/formulation/price, not blocked, but flag before delivering a 3rd instance
- EMS + LED facial lifting massager — NEW concept, delivered (Livaé)
- Knit waistcoat/cardigan (women's) — NEW concept, delivered (Diana Tricot)
- Deep-V ruffled mini dress — NEW concept, delivered (Blakely Blaze)
- Transparent dust-proof storage bags — NEW concept, delivered (KlarFix)
- Ribbed-glass ceiling pendant light — NEW concept, delivered (Sunset Pendant Light / Monulo);
  distinct from Vaoth Infinity Lamp (bottle-upcycle mirror lamp) and Blauzone/LumiBeam (night
  light / projector) already on the sheet — different form factor
- "Cerviless Pro" posture corrector (brinoa.com) — CONFIRMED DUPLICATE of the product delivered
  2026-08-17 under minopia.com (per run 1's SEEN_DOMAINS note) — moot this run since it's also
  sold out, but worth keeping in this list explicitly since it surfaced again in discovery

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

## 2026-09-15 (run 8b, via /find-winning-products-2.0) — META FALLBACK, OPERATOR-AUTHORIZED, hit 10/10
After run 8's Pinterest-only pass delivered 6/10 with Hobbies/Fitness/Home care/Car
accessories/Underwear all empty, the operator explicitly said "if pinterest is exhausted, find
meta products" — a one-time authorization, not a standing change to the Pinterest-only default
(SKILL.md section14 stays Pinterest-only unless told otherwise again next run). Ran 2 parallel Meta
Ad Library discovery+verify agents targeting exactly those empty niches. 4 delivered, ALL TEST NOW,
ALL SOURCE: Meta, ALL with a real Meta Ad Library link (ad-specific + all-ads-by-page, since no
Pinterest pin exists for these) + real AliExpress supplier + real COGS + a computed AG selling
price. Fitness still returned zero (every candidate found was an established brand, not dropship).
Rows 423-426. **Day total: 10/10 for the first time since gate-loosening began in run 6.**
- Luxury Foldable Trunk Organizer — pinauto-store.com — Car accessories — GB — TEST NOW (39.99 EUR
  — MARGIN RISK, barely clears the gate)
- Women's V-Shaped Elastic Band S-Curve Shaping & Tummy Control Bodysuit — floralshe.com —
  Underwear — US — TEST NOW (49.99 EUR)
- Joybos Smart Sensor Trash Can — joybos.com — Home care — US — TEST NOW (57.99 EUR; 781-day
  survivor, strongest durability signal of the whole day)
- Lumos Knitting Light — lumoslumos.com — Hobbies — US — TEST NOW (46.99 EUR; niche classification
  judgment call, see SEEN_DOMAINS)

## 2026-09-15 (run 8, via /find-winning-products-2.0) — FIRST RUN UNDER THE NEW >=39 EUR SELLING-PRICE GATE
6 delivered, ALL TEST NOW, ALL SOURCE: Pinterest, ALL with a real Pinterest link + real AliExpress
supplier link + real COGS + a computed AG selling price written at delivery time (not backfilled).
Niches with zero qualifying+verified candidates: Hobbies, Fitness, Home care, Car accessories
(zero raw candidates surviving the new price floor), Underwear (1 raw candidate, sold out at
verification). Rows 417-422.
- Handiva (TM) Real Hands Neck & Shoulder Massager — adoradelightusa.com — Healthcare — US — video ad
  — TEST NOW (63.99 EUR; cross-store demand confirmed via Valcero + bovagu listings)
- Eettsy Cupping Massager — eettsy.com — Beauty — AU — video ad — TEST NOW (50.99 EUR; days-running
  right at the 30-day gate floor, ad currency not re-confirmed live)
- Ramona Contrast Corset Babydoll Mini Dress — leauclothing.com — Women's fashion — US — video ad —
  TEST NOW (137.99 EUR)
- Ito Wabi Sabi Minimalist Pendant Light — tudoandco.com — Lighting — US — image ad — TEST NOW
  (216.99 EUR; WinningHunter price was stale, live price much higher across 3 variants)
- Modern Leather Drop Shoulder Jacket — jdongvak.com (was ashoul.com) — Men's fashion — US — image ad
  — TEST NOW (39.99 EUR — MARGIN RISK, razor-thin buffer above the gate and thin COGS-to-price ratio)
- Indra Dress (Amethyst Purple) — theroyalcodes.com — Women's fashion — US — image ad — TEST NOW
  (74.99 EUR; WinningHunter price was stale, adscount exactly at the 5-floor gate)

## 2026-09-14 (run 7, ROUND 2, via /find-winning-products-2.0)
3 more delivered (total for the day: 8/10), ALL TEST NOW, ALL SOURCE: Pinterest, ALL with real
links + real supplier + real COGS.
- Veilleuse Guirlande Lumineuse LED avec Pinces Photo — luminaire-lucciano.com — Lighting — FR —
  image ad — TEST NOW (margin risk)
- Collier Rainbow — tapioca-bijoux.com — Women's fashion — FR — image ad — TEST NOW
- Créole Rym (18k gold-plated hoop earrings) — belizebijoux.com — Women's fashion — FR — image ad
  — TEST NOW (sourced via collection-ad-to-bestseller-SKU judgment call, see LEARNING LOG)

## 2026-09-14 (run 7, via /find-winning-products-2.0)
5 delivered, ALL TEST NOW, ALL SOURCE: Pinterest, ALL with a real Pinterest link + real AliExpress
supplier link + real COGS. Niches with zero qualifying+verified candidates: Healthcare, Lighting,
Car accessories, Underwear (raw candidates found but none survived Stage C), Hobbies, Home care
(zero raw candidates at all — structural, not a verification issue).
- BlendMate Portable Blender (2-in-1 Smoothie Maker & Bottle) — margothale.com — Fitness — GB —
  video ad — TEST NOW
- Lissage Indien Kera Glow — lissage-au-top.com — Beauty — FR — video ad — TEST NOW
- Valentine's Whisper Corset Top — maisonzifan.com — Women's fashion — US — video ad — TEST NOW
- BIO-Aloe Vera Splash 3-in-1 — thatsme.organic — Beauty — DE — image ad — TEST NOW (margin risk)
- PureGlow Schwarztee-Gesichtsmaske — solenza.de — Beauty — DE — video ad — TEST NOW (margin risk,
  low stock)

## 2026-09-11 (run 6 — GATE-LOOSENING EXPERIMENT, via /find-winning-products-2.0)
7 delivered, ALL TEST NOW, ALL SOURCE: Pinterest, ALL with a real Pinterest link + real AliExpress
supplier link + real COGS. Niches with zero qualifying+verified candidates: Healthcare (4 raw
candidates, all died at Stage 2/3), Men's fashion, Car accessories, Fitness, Hobbies, Underwear
(zero raw candidates despite loosened gates).
- Skale Nail Growth Serum — skalecosmetics.com — Beauty — US — video ad — TEST NOW (margin risk, <$25)
- Skale Lash Growth Serum — skalecosmetics.com — Beauty — US — video ad — TEST NOW
- Livaé Facial Lifting Massager (EMS+LED) — helynshop.com — Beauty — US — video ad — TEST NOW
- Diana Tricot Knit Waistcoat — luxevintage.co — Women's fashion — US — image ad — TEST NOW
- Blakely Blaze Mini Dress — bymaara.com — Women's fashion — GB — image ad — TEST NOW
- KlarFix Transparent Dust-Proof Storage Bags — verlimo-shop.com — Home care — DE — video ad — TEST NOW (margin risk, <$25)
- Sunset Pendant Light (AFTERGLOW L1) — monulo.com — Lighting — US — image ad — TEST NOW

## 2026-09-11 (run 5 — days_min=15 EXPERIMENT, via /find-winning-products-2.0)
2 delivered, ALL TEST NOW, ALL SOURCE: Pinterest, both with real Pinterest link + real AliExpress
supplier link + real COGS.
- Zavonix PoutPower Lip Plumper — zavonix.com — Beauty — US — video ad — TEST NOW
- PistonPerk Spark Plug Novelty Mug — marnetic.com — Car accessories — US — image ad — TEST NOW
  (FLAGGED: automotive-themed novelty gift, not a functional car accessory — questionable niche fit)

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

### AE/AF/AG backfill for the sibling skill's 2026-09-16 batch (rows 427-436, done 2026-09-17)
Operator asked to fill missing AE/AF/AG for the last 10 rows. AG was blank on all 10 (the sibling
`find-winning-products` skill doesn't compute it — same gap as the 2026-09-14 batch backfilled
earlier). AE/AF were already correct for 7/10 rows (real supplier link + COGS); the other 3 had an
honest "no qualifying supplier" note rather than being empty. Computed AG for all 10 via live price
+ fresh EUR rate + floor-to-.99, and retried AliExpress sourcing on the 3 "no supplier" rows:
- **Row 428 (Marnetic GraceMakers Nativity Craft Set)**: found a qualifying supplier this time —
  JAKI Nativity Building Blocks Set, 363 orders, 4.9*, COGS $22.98. AG = 34.99 EUR.
- **Row 433 (Mylvera Apex Dashboard Mat)**: found a qualifying supplier — a per-vehicle-model fitted
  dashboard mat/sunshade (Hyundai Sonata reference SKU), 388 orders, 4.7*, COGS $4.31. Same product
  line sold as separate per-car-model listings, which is why earlier searches (looking for one
  universal SKU) came up empty. AG = 52.99 EUR.
- **Row 436 (Buckmen Reader Night Light)**: STILL no qualifying supplier after 10 more search-term
  variations, including visual inspection of the closest 2 candidates (a Halloween ghost lamp -
  wrong theme; a reader-figure statue with no light at all - fails the "night light" requirement).
  This looks like a genuinely hard-to-source niche product, not a search-effort gap — deprioritize
  further automated retries unless a human wants to hand-pick a supplier.
- **Stock-out note, not part of the ask but observed during live price checks**: rows 427
  (Tiktrove Massage Comb), 432 (Castivaro HydroGuard), 435 (Odessa StitchMaster), and 436 (Buckmen
  Reader Night Light) all showed "Sold out" on their live product pages as of 2026-09-17, one day
  after being delivered. AG was still computed and filled per the request, but these 4 are not
  currently purchasable — worth a stock recheck in the next couple of weeks.

### From run 8 (2026-09-15)
- **Cécile™ Maxi Chemise Intemporelle (zoeparis.fr)** — STILL DNS-unreachable, 3rd consecutive
  failed attempt (2 separate sessions now: `getaddrinfo EAI_AGAIN` again, plus this run's proxy
  also independently logged `connect_rejected`/502 on the same host). This is now looking like a
  persistent issue with this specific domain rather than transient downtime — deprioritize further
  automated retries; if it matters, flag for a human to check manually.
- **Sexy Strass Lingerie Set – Kierstin (dulcestoreparis.com)** — sold out at live check, AND the
  live price ($109/$129) has risen ~58% vs. the $69/$89 WinningHunter snapshot from 2026-01-28.
  Recheck stock in 2-3 weeks, but re-run the full selling-price gate calc from scratch if/when it
  restocks — do not reuse this run's numbers.
- **LumaLift Facial Sculptor (deluxeskin.uk / trydeluxeskin.com)** — entire storefront down
  (HTTP 423 "store unavailable" + HTTP 402 on the alt domain), not just this product. The
  Pinterest ad ("Beauty Life Magazine") was still apparently driving traffic to a dead store as of
  this run — worth a priority recheck since this may resolve on its own if it's a billing/freeze
  issue, and the underlying product economics (67.99 EUR, 10,000+ order supplier at 4.9*) are
  strong if the store comes back.
- **Minimalist LED Floor Lamp (vakkerlight.com)** — both the product page and its collection page
  404, but a Wayback Machine snapshot confirms it was live as of 2026-04-02 at the expected price.
  Recheck in a few weeks in case it's a temporary delisting rather than permanent discontinuation.
- **Lantern Fabric Pendant Light (vakkerlight.com)** — in stock, price passes (167.99 EUR), but no
  AliExpress supplier cleared both the >=200 orders and >=4.5* bar simultaneously across 5 search
  variations. Retry sourcing with different angles (Chinese-language search terms, "linen drum
  pendant light gold frame") before giving up on this one.
- **3-Piece Trouser Suit concept (hudsongrace.co.uk / hudsonclaye.com)** — the specific 3-piece
  blazer+corset+wide-leg set is delisted (both known product URLs 404, and the live "Women's Suits"
  collection is entirely sold out), but the store itself (now rebranded to hudsonclaye.com) is
  alive — worth a fresh discovery pass against the new domain rather than continuing to chase the
  old product URLs.
- **Data-loss note, not a product recheck**: SEEN_PRODUCT_IDS already listed Pinterest pin
  687295152692 (Adora Delight Handiva) as "qualified, delivered TEST NOW" from run 1/run 2
  (2026-09-08/09-10) — but it was absent from the live spreadsheet when this run's exclusion index
  was built (D5:H416), and re-delivering it was correct per the "spreadsheet wins" rule (SKILL.md
  section32). This is the same concurrent-write-collision failure mode documented in the run 2
  learning log below, resurfacing 5 days later — a product qualified twice, five runs apart,
  because an earlier delivery was silently lost from the live sheet at some point. Not actionable
  right now, but worth remembering next time a "duplicate" ledger entry looks surprising: check the
  live sheet, not just this file, before assuming it's already there.

### From run 7 round 2 (2026-09-14)
- **Cécile™ Maxi Chemise Intemporelle and Peignoir Betty™ Camel (zoeparis.fr)** — DNS resolution
  failure on every attempt (`getaddrinfo EAI_AGAIN`, both with and without `www.`), not
  bot-blocking. Retry in a future run — the domain may simply have been down temporarily.
- **Rhinestone Jeans (glizm.com)** — DOWNGRADED from the prior high-priority recheck. Confirmed
  absent from the store's own `/search/suggest.json` index, not just a wrong URL. Treat as
  delisted/gone; do not spend further budget chasing it unless it resurfaces in a fresh discovery
  pass under a new listing.

### From run 7 (2026-09-14)
- **Rhinestone Jeans (glizm.com, 4,460 repins)** — HIGHEST PRIORITY recheck of any item in this
  queue. Strongest traction signal found in any run to date; the exact WinningHunter-reported URL
  404'd and it could not be located via site search or a 5,397-product catalog browse. Next
  attempt: try `get_pinterest_ad` again for a fresh `shopify_productid`/handle (the store may have
  renamed the product), or check via Google site-search (`site:glizm.com rhinestone jeans`) if a
  web-search tool is available in a future session.
- **PosturePro / Haltungskorrektor (wecro.de / shopwecro.com)** — failed automated verification 2
  runs in a row across a domain migration. Recheck manually (a human visiting the site) rather than
  via automated WebFetch, or drop from future rotations if it keeps failing.
- **Eclipse Retro Wall Light (tudoandco.com)** and **RGB Strobe LED Lamp (zorenza.de)** — both
  unverifiable due to bot-blocking/connection issues rather than confirmed sold-out; recheck with a
  different fetch approach or after a delay (blocking may be temporary/rate-limit related).
- **Flower Child Flannel (vaguestudios.com)** — confirmed in stock, but no AliExpress supplier met
  both order-count and star-rating thresholds simultaneously. Re-run supplier sourcing next time
  with broader search terms ("cotton plaid shirt men", "vintage flannel jacket") before giving up.

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

### 2026-09-15 (run 8b) — Meta fallback closed the gap to 10/10; the "structural ceiling" niches
turn out to be Pinterest-specific, not category-wide
Meta Ad Library found genuinely qualifying, dropship-compatible products in 4 of the 5 niches that
had returned zero on exhaustive Pinterest search (Car accessories, Underwear, Home care, Hobbies) —
only Fitness stayed empty, this time because every Meta candidate turned out to be an established
brand (Pulsio, Kensui, SmartWorkout, T1TAN) rather than a dropship opportunity, a different failure
mode than "no candidates exist." **This reframes the run 4-8 learning-log narrative**: the repeated
finding that these niches are "structurally weak" was specific to Pinterest-as-a-channel, not
evidence that no sourceable product exists in them at all. Worth remembering next time Pinterest
comes up empty in one of these — it is not necessarily a dead end for the day, just a dead end for
that one source.
- **AliExpress sourcing method fix paid off across both agents**: explicitly appending
  `&SortType=total_tranpro_desc` to the wholesale search URL and parsing `trade.tradeDesc` +
  `evaluation.starRating` from the embedded `_init_data_` JSON (rather than the default-sorted page,
  which sometimes omits the `trade` field entirely) worked reliably for both Meta agents on the
  first attempt each — this fix from earlier in the same run session is now confirmed repeatable,
  not a one-off. Bake this into the standing AliExpress-sourcing instructions for future runs
  (Pinterest or Meta) rather than re-discovering it each time an agent hits the client-side-render
  wall.
- **Meta's established-brand noise is real and different in kind from Pinterest's**: both Meta
  agents rejected a large fraction of otherwise-qualifying candidates specifically for being
  established/branded operations (own warehouses, VAT registration, 10k+ reviews, multi-year ad
  runs at huge scale) rather than small dropship stores — this pattern showed up far more on Meta
  this run than it typically does on Pinterest keyword search. If Meta becomes a recurring
  secondary source, budget extra verification time for this brand-vs-dropship judgment call
  specifically.

### 2026-09-15 (run 8) — first run under the new >=39 EUR selling-price gate; landed at 6/10,
attrition pattern shifted from "sold out" to "priced out"
Raw discovery across the 10 niches (4 parallel agents, USA/DE-first per mandate) found 13 candidates
after excluding obvious duplicates and one gate failure at the discovery stage itself (LePharea
CelAway at 39.95 EUR converts to 38.99 after the floor-to-.99 rounddown — fails despite "looking"
above 39). Of those 13, Stage B/C verification passed 6 and rejected 7. **The rejection reasons this
run skew heavily toward store/stock problems, not price**: 2 stores fully down (dead Shopify
storefront, HTTP 423/402), 2 products delisted (404 on live product+collection pages), 1 sold out
with a price that had also risen 58% since the WinningHunter snapshot, 1 with no qualifying
AliExpress supplier despite passing price/stock cleanly. Only one candidate (CelAway) was actually
killed by the new price gate itself. **This suggests the new >=39 EUR floor's main effect this run
was upstream, at discovery** — agents were explicitly told to deprioritize sub-35 EUR candidates
before even proposing them, so the "priced out" attrition mostly happened invisibly before Stage B,
not as a visible rejection count here. Worth tracking over a few more runs: if visible price-gate
rejections stay this low, the floor may be filtering less than expected at the margin (most
Pinterest dropship candidates in these niches already cluster either well above or well below 39
EUR, with few genuine borderline cases like CelAway).
- **AliExpress order/rating verification method matters — same search, different results depending
  on how the page renders**: one verification agent hit a wall where item detail pages were fully
  client-side-rendered with no usable data, and even the search-results page's embedded JSON lacked
  a `trade`/orders field on that particular fetch. A different fetch of the same style of search
  (this time with `&SortType=total_tranpro_desc` explicitly appended) reliably returned `trade.
  tradeDesc` (orders) and `evaluation.starRating` for every item. **Always sort AliExpress search
  results by orders explicitly via the URL param, don't rely on the default sort** — this recovered
  3 suppliers (Ito Wabi Sabi, Ashoul jacket, Indra Dress) that an agent had reported as
  "unconfirmable due to tooling limitation" moments earlier using the exact same search terms.
- **Stale WinningHunter price data was unusually common this run**: 3 of 6 delivered products (Ito
  Wabi Sabi $199→$251+, Indra Dress $77→$87, Kierstin $69→$109 before it was rejected anyway) had
  live prices meaningfully different from the cached WinningHunter snapshot, always higher. Worth
  treating "WinningHunter price" as a rough pre-filter only, never as the number that actually goes
  into the selling-price gate calculation — always use the live-verified price, which this run
  already does per SKILL.md section50, but the drift size this run was bigger than usual.
- **Margin-risk flagging still has a place even though the old sub-25-EUR soft-flag rule was
  retired**: the Ashoul leather jacket cleared the 39 EUR selling-price gate at exactly 39.99 EUR,
  but its closest-matching AliExpress suppliers cost 27-45 USD, i.e. close to or above the entire
  selling price. The gate checks selling price alone, not COGS ratio, so this slipped through as a
  technical PASS while being a real business risk. Recommend flagging (not rejecting) any delivered
  product whose supplier COGS exceeds roughly 50% of the computed AG selling price, the same way
  this run flagged it in the product's Y-column note — this isn't a codified gate, just a judgment
  call worth making visible every time it comes up.
- **Underwear, Hobbies, Fitness, Home care, Car accessories: still a hard ceiling.** Hobbies/
  Fitness/Home care returned literally zero raw candidates this run even before Stage B (confirmed
  by a dedicated agent running ~35 searches across US+DE) — same structural finding as runs 4-7.
  Car accessories also returned zero across 13 keyword variants in a separate agent. Underwear
  returned exactly one raw candidate (Kierstin) and it was sold out. This is now 5+ consecutive
  runs with the same 4-5 niches contributing nothing — worth raising to the operator as a standing
  question (accept these niches as structurally near-empty on Pinterest, or authorize a lever this
  skill hasn't tried yet, e.g. a second source restricted to just these niches) rather than
  re-running the identical exhaustive sweep every time with the same result.

### 2026-09-14 (run 7, ROUND 2) — pushed a second full discovery round to reach 8/10; the last 2
are a real ceiling today, not a search-effort gap
Round 1 delivered 5; the operator asked for 5 more. Ran a full second round (~98 more keyword
searches across 2 agents, avoiding every round-1 combo, adding FR/ES markets and seasonal angles)
and got 3 more, landing at 8/10 for the day. The two products lost to genuine bad luck rather than
gate strictness (zoeparis.fr's DNS being down) are the clearest evidence yet that at least part of
Stage C attrition is pure operational noise unrelated to product quality — those two would very
likely have been delivered on a different day. Six niches (Healthcare, Car accessories, Fitness,
Men's fashion, Hobbies, Home care) are now 0-for-2 rounds today on top of being weak across prior
runs too — this is strong enough evidence to say, plainly, that under Pinterest-only sourcing with
the current gates, these six niches cannot reliably contribute to a 10/day target most days. That
is a structural fact about today's Pinterest ad mix for small Shopify dropshippers, not a discovery
failure — surfacing it directly rather than re-discovering it every run. If 10/day needs to be hit
reliably, the operator needs to decide among: (a) accept fewer than 10 on days these 6 niches are
dry (my recommendation — this is what happened today and delivered a clean, honest 8), (b) allow a
second source (TikTok/Meta) specifically to backfill these 6 niches only, or (c) loosen repins/ads
further. None of these should be assumed silently.

### 2026-09-14 (run 7) — Stage C (verification) is now unambiguously the binding constraint, and
it's noisy run-to-run
This run ran the exact same standing gates as run 6 (repins>=20, ads>=5, days>=30, image/video,
Pinterest-only) and found comparable raw-discovery breadth (22 candidates vs. run 6's 18), but
delivered only 5 vs. run 6's 7. The discovery side is now reasonably stable/repeatable at these
settings; the delivered count is not — it swings with how many candidates happen to survive Stage C
on a given day (stock levels change daily; a store having a bad inventory week is normal noise, not
a signal about the gates). Concretely this run: 7 of 22 raw candidates were sold-out/delisted, 3
were unverifiable due to bot-blocking/network issues outside our control, 1 cleared every check
except the AliExpress supplier bar (first time that specific failure mode has been the sole reason
a fully-verified-in-stock product wasn't delivered), and 1 high-value candidate (4,460 repins, the
single strongest signal in 7 runs) couldn't be located on its own store's site at all.
**Implication for future runs**: don't chase Stage C attrition rate as if it were a tunable
parameter the way Stage B gates are — it isn't one. The two real remaining levers are still the
ones named in run 6's log (loosen repins/ads further, or accept a second source), both of which
trade away a standing operator requirement and need to be asked about, not assumed. A new,
narrower lever surfaced this run: build a small allowlist of "verification-hostile" domains
(bot-blocking stores like tudoandco.com, connection-refused domains like zorenza.de, chronically
unresolvable ones like wecro.de) and skip spending verification budget on new candidates from those
same domains in future runs unless the operator asks to retry them — this doesn't add volume, but
it stops wasting Stage C effort on stores that have already demonstrated they won't verify.
**Best niche this run**: Beauty (3/3, same as several prior runs — consistently the most reliable
niche for both raw discovery volume and Stage C survival). **Worst**: Hobbies and Home care, now
zero raw candidates 2 runs running even after 50+ keyword combos each — worth considering whether
these two niches have simply moved off Pinterest's current small-Shopify-dropship ad mix entirely,
which would be a finding worth surfacing to the operator directly rather than re-discovering every
run.

### 2026-09-11 (run 6) — loosening repin/adscount gates roughly tripled volume, but stock-out
attrition is now the harder ceiling
Operator's message after run 5 was unconditional: "i need 10 products every run." Rather than ask
another clarifying question, applied the top-ranked lever from run 5's own learning log — lowered
repin_count from 50 to 20 and adscount from 10 to 5, left days_since_started at 30 (already proven
not to matter) and left Pinterest-only sourcing + full Stage 2/3 verification untouched (both
explicit prior operator asks). Result: 18 raw candidates found (vs. roughly 6-10 in runs 3-5 at the
stricter gates) but only 7 survived live-stock verification and real AliExpress sourcing — a rate
of ~39% raw-to-delivered, worse than run 4's ~50% and roughly in line with run 5's. **The
loosened gates worked exactly as intended on the discovery side** (more raw candidates, especially
in Beauty which nearly doubled its historical single-run yield), but **verification attrition ate
most of the gain**: 2 sold-out, 1 delisted/404, 1 unverifiable-due-to-bot-blocking, 1
domain-migrated-with-ambiguous-product-match, 1 stale-price-now-over-cap. None of these are gate
problems — they're supply-side facts about small dropship stores (frequent restocks/delistings,
site migrations, inconsistent WebFetch access). **Conclusion for whoever runs this next**: 7/run
under full Pinterest-only + zero-placeholder verification appears close to this skill's realistic
ceiling at current exclusion-index saturation (6 runs deep now, several niches structurally
exhausted on Pinterest per this and prior runs' zero-candidate reports). To reliably clear 10/run
from here, the remaining real levers are, in order: (1) accept WATCH-tier rows again but ONLY with
real Pinterest links (no placeholders) even when stock/supplier can't be confirmed same-day — this
was explicitly rejected by the operator after run 3, so do not do this without asking again;
(2) loosen repin/adscount further (e.g. 10/3) — untested, real risk of admitting low-traction noise;
(3) accept a second source (TikTok or Meta) alongside Pinterest for the remaining niche gap — this
directly conflicts with the operator's "mostly pinterest winners" instruction and should not be done
without asking; (4) expand beyond the fixed 10-niche list — out of scope per SKILL.md. None of these
should be applied silently; each trades away something the operator explicitly asked for.

### 2026-09-11 (run 5) — days_min ruled out as the volume lever; here's what's actually left
**Direct answer for the next run**: do not spend another cycle adjusting days_min — 30 vs 15 made
no meaningful difference (3 vs 2 deliverables, same method, same niches). The three real levers left,
in likely order of impact:
1. **Lower repin_count and/or adscount thresholds.** These were kept strict across runs 3-5 at the
   operator's choice. Given how many candidates across all 5 runs died at "repins 30-45" or
   "adscount 7-9" — just under the 50/10 bars — a modest reduction (e.g. repins>=30, ads>=7) would
   likely unlock several already-identified near-misses immediately (see REJECTED_PRODUCTS/near-miss
   notes throughout runs 3-5) without a full new search cycle.
2. **Accept boutique/proprietary products without a generic AliExpress equivalent**, sourcing
   instead from a manufacturer-direct or alternative supplier, or simply marking COGS "n/a - verify
   with brand/manufacturer directly" instead of hard-requiring an AliExpress match. This run's two
   LEAU dresses (Stage-1 and Stage-2 clean, Stage-3 blocked) are the clearest example — real
   winning products exist that aren't simple commodity dropship goods.
3. **Revisit the exclusion index's dedup strictness for near-identical-but-distinct concepts.**
   5 runs into this sheet, several sub-niches (posture correctors, neck massagers, wall sconces,
   shapewear bodysuits) are being auto-rejected as "duplicate concept" on every pass. Some of these
   really are the same product resold; others may be different-enough mechanisms that a less
   conservative reading would allow. Worth a deliberate one-time review of what's been rejected on
   this basis across runs 3-5 to see if any should be reconsidered.
- **New Stage-3 failure mode identified this run**: boutique/proprietary construction with no
  generic AliExpress equivalent (distinct from "no supplier found because the search terms were
  wrong" — here the product genuinely doesn't exist as a mass-market commodity). Track this
  separately from ordinary "no qualifying supplier" in future near-miss logs.
- **Healthcare + Lighting: 4-for-4 zero.** This is no longer noise — treat these two niches as
  effectively exhausted against this sheet's Pinterest inventory until either (a) enough time passes
  for new ads to scale up past the thresholds, or (b) gate #1 above (lower repin/ad thresholds) is
  applied specifically to these two niches as a test.

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

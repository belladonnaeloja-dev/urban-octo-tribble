# Find Winning Products 2.0 — Search History & Adaptive Learning

Persistent `SEARCH_HISTORY` (see
[discovery-engine.md §29](references/discovery-engine.md#29-never-run-the-same-search-blindly))
plus the adaptive-learning log
([§54](references/discovery-engine.md#54-adaptive-learning)). Read before every run; check
here before re-running an exact search. If a search dimension was recently exhausted with
zero new candidates, move to a different dimension instead of repeating it.

## SEARCH_HISTORY

One row per distinct search actually run. `endpoint` is one of
`pinterest-live | pinterest-historical | tiktok | meta`. `mcp__WinningHunter__search_pinterest_ads`
has no `niches` parameter in this account's tool schema (only `countries`, `keyword`,
`ad_score`, `date_from/to`, `days_min/max`, `technologies`, `traffic_min/max`,
`promoter_name`, `limit`, `sort_by/order`) — niches were searched by keyword only, per §19.

| Date | Endpoint | Keyword | Country | Candidates | Qualifying | Notes |
|---|---|---|---|---|---|---|
| 2026-09-08 | pinterest-live | led strip lights | US | 3 | 0 | image-only |
| 2026-09-08 | pinterest-live | car accessory organizer | US | 0 | 0 | zero results even w/o mindays |
| 2026-09-08 | pinterest-live | car trunk organizer | US | 0 | 0 | zero results w/ and w/o mindays |
| 2026-09-08 | pinterest-live | car seat gap filler | US | 0 | 0 | zero results |
| 2026-09-08 | pinterest-live | diamond painting kit | US | 14 | 0 | Amazon/Temu/Shein dominated, no video |
| 2026-09-08 | pinterest-live | craft kit for adults | US | 14 | 0 | same as above |
| 2026-09-08 | pinterest-live | puzzle 1000 piece | US | 12 | 0 | Amazon dominated, no video |
| 2026-09-08 | pinterest-live | mens wallet | US | 12 | 0 (1 rejected: no product page) | NHIM Apparel found (strong survivor, dropped — see ledger) |
| 2026-09-08 | pinterest-live | mens grooming kit | US | 0 | 0 | zero results |
| 2026-09-08 | pinterest-live | mens watch | US | 14 | 0 | fuzzy-match noise (jeans, donuts, sunglasses) |
| 2026-09-08 | pinterest-live | NHIM apparel | US | 5 of 10 | 0 | follow-up on mens wallet hit; no clean product page |
| 2026-09-08 | pinterest-live | led strip lights bedroom | US | 0 | 0 | zero results |
| 2026-09-08 | pinterest-live | galaxy projector light | US | 0 | 0 | zero results |
| 2026-09-08 | pinterest-live | sunset lamp | US | 2 | 0 | both image-only |
| 2026-09-08 | pinterest-live | herren uhr | DE | 10 of 36 | 0 | mostly unrelated big-brand/retail noise |
| 2026-09-08 | pinterest-live | led beleuchtung | DE | 10 of 63 | 0 | Home Depot-equivalent (Hornbach) + high-ticket furniture, no dropship video |
| 2026-09-08 | pinterest-live | back brace posture | US | 0 | 0 | zero results |
| 2026-09-08 | pinterest-live | phone mount for car | US | 0 | 0 | zero results |
| 2026-09-08 | pinterest-live | modellbau | DE | 1 | 0 | image-only |
| 2026-09-08 | pinterest-live | wireless wall sconce | US | 2 | 0 (duplicate) | Brinoa — already delivered 2026-09-07, confirms dedupe working |
| 2026-09-08 | pinterest-live | led face mask | US | 0 | 0 | zero results |
| 2026-09-08 | pinterest-live | wrap dress | US | 10 of 15 | 0 | all image, several established/high-price brands |
| 2026-09-08 | pinterest-live | resistance bands set | US | 0 | 0 | zero results |
| 2026-09-08 | pinterest-live | seamless underwear | US | 6 | 0 | BetterMe video had no valid product page; Mr Saker was image-only |
| 2026-09-08 | pinterest-live | skincare routine | US | 15 of 21 | 0 | highest repin (45) was an established brand (Palmer's) w/ no Shopify domain |
| 2026-09-08 | pinterest-live | home workout equipment | US | 1 | 0 | BetterMe lead-gen funnel, no physical Shopify product |
| 2026-09-08 | pinterest-live | pain relief device | US | 2 (1 unique ad, 2 instances) | 1 | SohoBloo OrthoAlign — TEST NOW |
| 2026-09-08 | pinterest-live | shapewear | US | 6 | 0 | Victoria's Secret/SKIMS/SHEIN — all established/marketplace |
| 2026-09-08 | pinterest-live | closet organizer | US | 11 | 0 | Amazon/Home Depot/Temu/Target dominated |
| 2026-09-08 | tiktok | neck pain relief | US | 8 of 30 | 1 (cross-niche, Car Accessories) | NIRACL Car Driving Neck Pillow — WATCH (margin risk) |
| 2026-09-08 | meta | niche=HT, US, video, $25-200, min_active_ads=40 | US | 20 of 6398 | 2 | Corecare + ReabTec — both sold out at verification, downgraded to WATCH |

**Not yet attempted this run** (candidates for next run's depth): FR/ES/NL/IT language tiers
on any niche; historical Pinterest windows (`days_min`/`days_max` bracketed, not just
`days_min=30` floor); TikTok searches for niches other than pain-relief/car; Meta searches
for niches other than Healthcare; winner-derived keyword expansion off today's 4 finds
(e.g. "cervical traction pillow", "posture corrector device", "knee compression sleeve",
"car neck pillow" — none of these exact-phrase expansions were run yet); store-derived
search off shopsohobloo.com's other products.

## Historical windows already searched

None yet — every search this run used `days_min=30` (a floor, not a bracketed historical
window) or no day filter at all. §25's window rotation (same-month-last-year, seasonal
spans, holiday windows) has not been started. Next run should open with a Q4/holiday
seasonal window (`days_min`/`days_max` bracketing ads that started ~Jun–Aug 2026, i.e.
Pinterest's 6–10-week-early lead on Nov/Dec demand) given today's date (2026-09-08).

## Adaptive learning log

### 2026-09-08
- **Best keyword family:** Problem-language (C) queries beat product-name (A) queries
  head-to-head on Healthcare — "pain relief device" and the Meta `niche=HT` sweep both
  returned qualifiers; plain product-name Pinterest searches ("mens wallet", "mens watch",
  "closet organizer", "diamond painting kit") returned zero qualifiers despite dozens of
  raw hits, because they get swallowed by Amazon/Temu/Target/Home Depot noise.
- **Worst keyword family:** Bare product-name searches in Hobbies, Home Care, and generic
  Fashion — 100% image media_type or 100% marketplace/established-brand domains across
  ~70 raw candidates combined.
- **Best language:** EN — DE was tried on 3 keywords (`herren uhr`, `led beleuchtung`,
  `modellbau`) and returned zero qualifiers each time; sample is small, don't conclude DE is
  weak yet, just that these particular 3 DE keywords were.
- **Best market:** US (only market with qualifiers this run: Pinterest, TikTok, and Meta
  all delivered from US-targeted ads).
- **Best niche:** Healthcare (3 of 4 delivered products). Car Accessories (1 of 4, TikTok
  only) is the only other niche with any yield.
- **Confirmed finding from the prior run also held today:** Car Accessories, Hobbies, and
  (for video-qualifying candidates) Men's Fashion are structurally thin on Pinterest's
  video+dropship intersection — every keyword tried in these three niches returned either
  zero results or 100% non-qualifying candidates (image-only, marketplace, or no valid
  product page). This is the second consecutive run with this pattern in these 3 niches.
- **Mandatory link verification caught two false positives:** both Meta-sourced Healthcare
  candidates (Corecare, ReabTec) looked strong on paper (125 and 437 active ads, €8.7k and
  €50.7k EU adspend) but were SOLD OUT on live product-page fetch. Without §40's mandatory
  fetch step both would have shipped as TEST NOW. Carry forward: always fetch before
  finalizing verdicts, especially for Meta/TikTok-sourced candidates with no Pinterest
  cross-check.
- **Carry-forward for next run:** (1) run the FR/ES/NL/IT language tiers — only EN and 3 DE
  keywords were tried; (2) open a Q4-seasonal `days_min`/`days_max` historical window;
  (3) run winner-derived expansions off this run's 4 finds; (4) recheck Corecare and ReabTec
  stock in ~2-3 weeks (see ledger.md RECHECK_QUEUE); (5) fix the Autosheet billing block and
  the spreadsheet-visibility gap (see ledger.md "Known visibility gaps") before relying on
  automated writes or full-history dedupe.

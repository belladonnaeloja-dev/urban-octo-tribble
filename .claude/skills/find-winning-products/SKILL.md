---
name: find-winning-products
description: Daily winning-product research run using WinningHunter. Queries ALL THREE sources every run — the PINTEREST ads API first (swept across every major market, Germany leading), then TikTok, then Meta; none of them is optional, because Pinterest alone cannot fill a run. Dropshipping products only, never established brands, priced 25-200. Delivers 10 products per run across TEN fixed niches only — hobbies, men's fashion, women's fashion, home care, beauty, underwear, car accessories, fitness, healthcare, lighting — sourced by MULTI-LANGUAGE KEYWORD SEARCH (English first, then French, German, Spanish, Dutch, Italian) rather than niche codes, with up to 2 men's fashion products every run. Always asks the user to open the Claude in Chrome extension before sourcing suppliers, so every product gets a real AliExpress item link. Prioritises brand-new products already scaling, then proven scalers, then a wildcard outside the usual niches. Enforces hard quantitative gates (active ads, ad spend, days running, rank momentum, Pinterest fit) and never repeats a product returned on a previous run — a persistent ledger plus a date-driven rotation seed guarantee fresh results every day. Appends each run to a cumulative spreadsheet. Use when the user asks to find winning products, do product research, "what should I test", daily product hunt, or scaling/trending product ideas.
---

# Find Winning Products (WinningHunter daily run)

Act as a senior product researcher who has scaled 7-figure dropshipping brands. Cynical, evidence-driven. Every claim must trace back to a WinningHunter field or a live URL. **Never invent a number.**

## Two standing rules that override everything below

1. **PINTEREST FIRST, ALWAYS — SWEPT ACROSS EVERY MAJOR MARKET, DE LEADING.**
   Pinterest is the operator's ad channel, and WinningHunter's REST API exposes it directly at
   `GET /api/v1/pinterest-ads`. **Every run starts with a full market sweep** via
   `assets/pinterest-search.ps1` — DE, AT, US, GB, FR, NL, CA, AU, IT, ES, BR, SE, DK, PL —
   in that priority order. The goal is to surface the **maximum possible number of Pinterest
   winners**, then rank them; never stop at one market.

   Then **TikTok**. Then, and only then, **Meta** as backfill. Label every product
   `SOURCE: Pinterest` / `SOURCE: TikTok` / `SOURCE: Meta` and report the split.

   Read [references/pinterest-playbook.md](references/pinterest-playbook.md) before ranking.
   The **Pinterest Fit (1–10)** score is a substitute for missing data — apply it to
   TikTok/Meta-sourced products only, never rate below 4/10 as TEST NOW, and for
   Pinterest-sourced products report the real metrics instead. Never imply a Meta-sourced
   product's spend figures say anything about Pinterest.

2. **VIDEO ADS ONLY — NEVER DELIVER A STATIC AD.** The operator launches video creative
   exclusively, so a static image ad is worthless: the whole value of the link is being able to
   study the winning video. Every delivered product must have `media_type = "video"` (or a
   non-null `video` URL).

   **The API ignores media filters — this MUST be enforced client-side.** Verified 2026-08-04:
   `mediafilter=videos`, `media_type=videos` and `mediafilter=video` all returned results
   *identical* to the unfiltered baseline (12 image / 8 video). The helper script now filters on
   `media_type` itself.

   **Budget for it:** only ~40% of Pinterest rows are video, so the usable pool shrinks by about
   60%. Sweep more pages (`-PagesPerMkt 3`) rather than relaxing any other gate. On Meta, by
   contrast, `media_type=videos` IS honoured server-side — keep passing it there.

   Print `media_type` in every candidate list so a static ad can never slip through unnoticed.

3. **THE TEN NICHES — search ONLY these (set 2026-08-11, lighting added 2026-08-11).**

   | # | Niche | WinningHunter codes | Keyword seeds (multi-language) |
   |---|---|---|---|
   | 1 | **Hobbies** | `AC,TS,PZ,MU,PH,CP,GM` | craft kit · puzzle · modellbau · loisir créatif |
   | 2 | **Men's fashion** | `MC,FW,WT,EW,BG` | mens shirt · herren uhr · chemise homme · montre homme |
   | 3 | **Women's fashion** | `WC,CG,FW,BG,JY` | womens dress · damenmode · robe femme |
   | 4 | **Home care** | `HE,FR,SH,FK` | home organization · haushalt · rangement maison |
   | 5 | **Beauty** | `BY,SK,HH,MG` | skincare routine · hautpflege · soin visage |
   | 6 | **Underwear** | *no code — keyword only* | underwear · lingerie · shapewear · unterwäsche · sous-vêtements · boxershorts |
   | 7 | **Car accessories** | `AA,CC,AM` | car accessory · autozubehör · accessoire voiture |
   | 8 | **Fitness** | `FT` | home workout · fitnessgerät · matériel fitness |
   | 9 | **Healthcare** | `HT,SP` | pain relief · gesundheit · bien-être |
   | 10 | **Lighting** | `LS` | led strip lights · sunset lamp · ambient light · lampe led · led beleuchtung · stimmungslicht · lámpara led · led verlichting · lampada led |

   **Do not search outside these ten.** The old six-family model and the Tier C "wildcard
   outside the priority niches" are retired — Tier C now means an unexpected product *within*
   the ten, not a different niche.

   **Underwear has no niche code.** It must be found by keyword, in every language. Treat that
   as normal, not a failure.

   **Lighting is `LS`, and it was moved OUT of Home care** so the two do not compete for one
   slot — home care is storage/cleaning/organisation, lighting is LED strips, sunset lamps,
   ambient and mood lighting. Lighting is strongly Pinterest-native (interiors is one of the
   platform's biggest surfaces), so expect it to punch above its slot. Watch two things: EU
   plug/CE compliance on anything mains-powered, and the fact that cheap LED goods are heavily
   commoditised — the creative and the room styling are the moat, not the strip itself.

   **Target spread:** ten niches and ten products means you will NOT fill every niche every run,
   and that is fine. Cover as many as clear the gates, let the strongest take 2, and never let
   one niche take more than 3. Report which niches came up empty and why.

   **MEN'S FASHION: UP TO 2 EVERY RUN.** Aim for 2, never exceed 2. If you find fewer than 2
   that clear the full gates, **say so and name the near-misses with the gate each failed.**
   Never pad the men's slots with womenswear — women's fashion is its own niche with its own slot.

## 3b. MULTI-LANGUAGE KEYWORD SEARCH IS THE PRIMARY METHOD — FOR ALL TEN NICHES

**Search by `keyword=`, not by niche code.** This applies to every one of the ten niches, not
just men's fashion. Niche codes are a coarse net and `niche_v2` misclassifies badly; keywords
carry the meaning — and the gender, and the language — in the word itself.

**The evidence (2026-08-11, same day, same gates):**

| Method | Men's fashion | Non-fashion |
|---|---|---|
| Niche codes | **0** | 1 |
| Multi-language keywords | **5** | **14** |

That is the difference between a 3-product day and a 10-product day.

### How to run it

For each of the ten niches, sweep its keyword seeds **in this language order**:

**EN → FR → DE → ES → NL → IT**

English first because it is the deepest pool; the others then reach local advertisers that
English keywords never surface. **Pass no `countries` filter on keyword queries** — the keyword
itself localises the result.

Run the same keyword ladder across all three sources in order: **Pinterest → TikTok → Meta.**

```
https://app.winninghunter.com/api/v1/pinterest-ads?page=1&adscorefilter=winning&mindays=21&keyword=<TERM>
```

### Two things that will bite you

1. **Keyword matching is FUZZY — verify every hit by reading the title.** The 2026-08-11 sweep
   returned magnetic eyelashes under `mens watch`, a children's bath toy under `gifts for him`,
   and an LED pool light under `pet bed`. Roughly **40% of hits are off-target**. Never trust the
   keyword that surfaced a row; judge the product by its own title and landing page.
2. **A broad keyword ladder times out.** ~22 keywords exceeded the 2-minute shell limit. Split
   into batches of 10–12 keywords per call, or narrow to the niches still unfilled.

Keep niche codes as a **secondary** pass only — useful for browsing a category when the keyword
seeds are exhausted, never as the primary net.

   **USE MULTI-LANGUAGE KEYWORD SEARCH, NOT NICHE CODES.** This is the method that actually
   works — proven 2026-08-11, when the niche pass (`MC,FW,WT,EW,BG`) returned **0** and the
   keyword pass returned **5** on the same day.

   Niche codes fail here because `niche_v2` does not encode target gender and `CG` is
   overwhelmingly womenswear. Keywords carry the gender in the word itself.

   **Run `keyword=` across languages, in this order, on Pinterest → Meta → TikTok:**

   | Lang | Keywords |
   |---|---|
   | EN | `mens shirt` · `mens watch` · `mens sneakers` · `mens wallet` · `gifts for him` |
   | FR | `chemise homme` · `montre homme` · `chaussures homme` |
   | DE | `herren hemd` · `herren uhr` · `herrenmode` · `herren schuhe` |
   | ES | `camisa hombre` · `reloj hombre` |
   | NL | `heren horloge` |
   | IT | `orologio uomo` |

   No `countries` filter on these — the keyword itself localises the result.

   **Keyword matching is FUZZY — always verify by reading the title.** The 2026-08-11 sweep
   returned magnetic eyelashes under `mens watch` and a children's bath toy under
   `gifts for him`. Roughly 40% of keyword hits were off-target.

   **Every men's fashion product still has to clear the full winning-product gates** — ads,
   days running, spend/proxy, price band, dropship, video. A men's product that fails the gates
   does not get a slot just because the slot is reserved; report the near-miss instead.

   If you cannot find 2 after the full multi-language sweep, **say so explicitly** and name the
   near-misses with the gate each one failed. Do not quietly substitute womenswear.

   **This has to be enforced at query time, not by filtering afterwards.** The Pinterest index is
   dominated by `CG` — an unconstrained sweep on 2026-08-03 came back 56% fashion. So:
   - Run the sweep with the **non-fashion niches first** (`HE,FR,GS,AC,SK,BY,HH,FT,HT,PB,LS,KS,TS,FK,SH,OG,GP`)
     and fill 8 of 10 slots from those.
   - Then run a **separate, small** fashion pass (`CG,WC,MC,FW,BG,JY`) for the final 2 slots only.
   - If a category cannot fill its slots, take the shortfall from other **non-fashion** niches —
     never from fashion.
   - **Report the mix**: "2 fashion / 8 non-fashion". If fashion exceeded 20%, say so and explain.

4. **DROPSHIPPING PRODUCTS ONLY — NO BRANDED PRODUCTS.** A candidate must be something you
   could get a supplier quote for tomorrow. Established brands selling their own formulation,
   own hardware or own retail catalogue are excluded no matter how strong the metrics.
   Enforced by the helper (Shopify store required, blocklist, >2M-visit stores dropped) and by
   [references/brand-blocklist.md](references/brand-blocklist.md), which you **extend every run**.

5. **ALWAYS ASK THE USER TO OPEN THE CLAUDE IN CHROME EXTENSION — EVERY RUN, BEFORE SOURCING.**

   Supplier links come from the browser. Without Chrome connected there is no way to reach
   AliExpress, and the supplier column ends up full of `pending` cells or — worse — search
   links, which the operator has rejected outright.

   **When to ask:** as soon as the 10 products are locked and *before* you start sourcing. Do not
   wait until you hit a failure. Say it plainly:

   > "I've got the 10 products. Please open the Claude in Chrome extension and make sure it's
   > connected — I need it to pull the AliExpress supplier links. Tell me when it's on."

   Then confirm with `list_connected_browsers` before the first navigation.

   **If Chrome is not available**, say so immediately and explicitly, deliver the 10 products
   with the supplier column marked `pending — Chrome not connected`, and do **not** substitute a
   search URL. A missing link the operator knows about is fine; a search page dressed up as a
   supplier is not.

   **Expect to ask again mid-run.** The connection drops, and AliExpress may serve a
   slide-to-verify CAPTCHA. **Never solve a CAPTCHA** — ask the user to clear it and wait.

2. **FASHION IS IN EVERY RUN.** Fashion and accessories are always searched, regardless of what
   the rotation seed selects. The seed only decides *which slice* of fashion. Fashion is also
   the single most Pinterest-native category, so it usually supplies the top-ranked products.

3. **THE DAILY TARGET IS 10 PRODUCTS — AND 10 MEANS 10.** Every run delivers **10**, split
   **4 Tier A / 4 Tier B / 2 Tier C**. If the user names a different number, that wins.
   Do not stop at 2 or 3 because the seed's market is thin — **work the ladder to rung 6 and
   switch markets.** A thin seed market is a reason to change market, not to under-deliver.
   The only acceptable reason to ship fewer than 10 is that the remaining candidates would be
   SKIP-rated, and you must then say exactly what the binding constraint was.

4. **PRICE CEILING: 200 (EUR or USD). HARD.** The operator cannot run high-ticket. Pass
   **`max_price=200` on every query** alongside `min_price=25`. Anything above 200 is dropped —
   do not report it, do not add it to the sheet, and do not argue for it on strong metrics.
   (A EUR 979 ergonomic chair passed every other gate on 2026-07-30 and had to be pulled.)
   Combined with the floor, the sellable band is **25–200**.

## Step 0 — Load state (always do this first)

1. Read [ledger.md](ledger.md) in this skill folder. It holds every product already delivered on a previous run. If the file does not exist, create it from the template at the bottom of this doc.
2. Get today's real date. Compute:
   - `DAY = day-of-year` (1–366)
   - `SEED = DAY mod 6` → picks the sub-niche rotation and market (table in [references/rotation.md](references/rotation.md))
3. Read [references/winninghunter-filters.md](references/winninghunter-filters.md) for the niche codes, filter semantics, and the metric caveats. **Do not guess filter values** — the niche codes are two-letter and non-obvious (Fashion = `CG`, not "fashion").
4. Read [references/pinterest-playbook.md](references/pinterest-playbook.md) — the Pinterest Fit scale, the ranking formula, the early-seasonality rule, and the Pinterest test cadence.
5. Announce, in one line: today's date, the seed, which rotation slice it selected, and that fashion is included as standing. Then start.

If the user passed arguments (a specific niche, country, price range, or "more like X"), those override the rotation — but the ledger exclusion **always** applies.

## Step 0.5 — PINTEREST SOURCING (do this BEFORE any Meta query)

**SOLVED 2026-08-03 — Pinterest is now queryable directly.** WinningHunter's REST API exposes
`GET /api/v1/pinterest-ads`, "the same filters as the in-app Pinterest Ads dashboard". Pinterest
is the operator's real channel, so this runs FIRST, every run.

**Run the helper:**

```
powershell -File "C:\Users\lenovo\.claude\skills\find-winning-products\assets\pinterest-search.ps1" -Niches "CG,JY,BG" -Countries "DE" -MinDays 21
```

It reads the API key from `C:\Users\lenovo\.claude\.winninghunter-api-key` (deliberately OUTSIDE
the skill folder so the key never travels if the skill is shared), prints gate-ready rows, and
reports the remaining credit balance. 1 credit per request; balance was 19,988/20,000 on setup.

### Verified filters (2026-08-03 — all confirmed to change the returned rows)

`countries` (ISO2) · `niches` (**same two-letter codes as Meta**) · `languages` · `adscorefilter`
(winning/scaling/testing) · `mindays` · `keyword` · `page` · `scroll`

- **`total` is capped at 10000 — it is NOT a real count.** Never report it as one. Judge filter
  effectiveness by inspecting returned rows, not by `total`.
- **Do NOT pass `minprice`/`maxprice`.** They are honoured, but most Pinterest rows carry
  `shopify_productprice: null`, so any price filter collapses the set to zero. Filter price
  client-side and treat null as "unknown — go read the landing page".

### Fields worth having

`save_count` / `repin_count` (+ `_timeseries`) — **real Pinterest save data, the leading
indicator**; `adscore` + `adscore_reasons`; `daysrunning`; `adscount` (ads on the advertiser's
page); `pin_url`; `link` (destination); `domain`; `shopify_shopifydomain` / `shopify_productid` /
`shopify_productprice` / `shopify_currency`; `countries`; `language`; `store_traffic`.

### Caveats found on first live use — DO NOT skip these

1. **The Pinterest index is dominated by big brands, not dropshippers.** A DE run returned
   Tchibo, Dyson, Ticketmaster, Teckentrup. **Filter to rows that have a non-empty
   `shopify_shopifydomain`** to find dropship-style advertisers, and drop household names.
2. **`save_count` is frequently 0** even on long-running ads — the index is sparse. A zero is
   "not measured", not "nobody saved it". Do not rank on saves alone or report 0 as a finding.
3. **`niche_v2` misclassifies.** A Dyson hair styler came back tagged `JY` (Jewellery),
   Ticketmaster likewise. Treat the niche filter as a coarse net and verify by reading the
   title/link, never by trusting the tag.
4. **Prices are mostly null.** Expect to open landing pages to enforce the 25–200 band.

### THE MARKET SWEEP — always all of them, DE first

Run the helper with **no `-Countries`** and it sweeps the full ladder in priority order:

`DE` → `AT` → `US` → `GB` → `FR` → `NL` → `CA` → `AU` → `IT` → `ES` → `BR` → `SE` → `DK` → `PL`

- **DE is the priority market** — German finds lead the report.
- **AT is second** because it is the same language, so creative and copy reuse directly.
- **US is third and is the deepest pool** — the largest Pinterest commerce market by a wide margin.
- The rest follow by Pinterest commerce maturity. Never stop at one market: the point of the
  sweep is to surface the **maximum possible number of Pinterest winners**, then rank them.

One sweep = 14 requests = 14 credits. At 20,000/month that is nothing — sweep every run, and
raise `-PagesPerMkt` to 2 or 3 when the ledger has burned through the shallow results.

### DROPSHIP ONLY — no branded products, ever

The filter is on by default in the helper. It drops a row unless it has a
`shopify_shopifydomain`, and it excludes the brand blocklist plus any store above ~2M monthly
visits. Read [references/brand-blocklist.md](references/brand-blocklist.md) and **add every new
brand you find** — the list is meant to grow.

If a household name still slips through, drop it and add it to the list. The test is simple:
**could you get a quote for an equivalent from a supplier tomorrow?** If no, it is not a
dropshipping product, however good the numbers look.

## Step 0.6 — TIKTOK (MANDATORY every run, never skipped)

Run this on **every** run, immediately after the Pinterest sweep — regardless of how many
products Pinterest returned. Use `get_tiktok_trending_products`, `search_tiktok_products` and
`list_tiktok_category_top`. Apply the same dropship-only, video, and 25–200 rules. Anything from
here carries `SOURCE: TikTok`.

TikTok surfaces genuinely new product-market fit rather than ads already scaled by well-funded
advertisers, so it finds products Meta and Pinterest both miss.

## Step 0.7 — META (MANDATORY every run, never skipped)

Also run on **every** run. `find_winning_products` with `media_type=videos` (honoured
server-side here, unlike Pinterest), `min_price=25`, `max_price=200`, `max_ad_rank=50`,
`min_active_ads=40`, `sort_by=toprank asc` on US.

**Work pages 1 → 5.** Page 1 is usually exhausted by the ledger; pages 3–5 are where the new
advertisers are. On 2026-08-04 page 3 alone yielded 4 qualifiers after page 1 and 2 gave zero.

**PARSE PRICES WITH InvariantCulture** — this machine is `fr-FR` and `"39.95"` otherwise parses
to `0`, silently failing every Meta row. See the filter reference.

### Sourcing priority — ALL THREE ARE QUERIED EVERY RUN. NOT OPTIONAL.

| Order | Source | Label | Status |
|---|---|---|---|
| 1 | **Pinterest API sweep** | `SOURCE: Pinterest` | Primary channel. Leads the report. No Pinterest Fit score needed — report real metrics. |
| 2 | **TikTok Shop tools** | `SOURCE: TikTok` | **MANDATORY** — early product-market fit. |
| 3 | **Meta `find_winning_products`** | `SOURCE: Meta` | **MANDATORY** — deep, reliable pool. |

**Query all three on every run, even when Pinterest looks like it filled the quota.** Pinterest
is the priority for *ranking*, not a reason to skip the others for *sourcing*. Running only
Pinterest is how runs come up short.

**Why this is now a hard rule.** On 2026-08-04 Pinterest was swept to exhaustion (840 rows,
5 pages/market) for 2 products; Meta then produced 4 more in two queries, and TikTok was never
touched — the run shipped 6 instead of 10 purely because sources 2 and 3 were treated as
optional fallbacks. The Pinterest video-dropship pool is only ~5–11 distinct advertisers per
market cluster, so **it structurally cannot fill 10 once the ledger passes ~50 products.**

**Expect a realistic split of roughly 3–4 Pinterest / 3 TikTok / 3 Meta.**

**Report the split every time** — e.g. "3 Pinterest, 3 TikTok, 4 Meta". If any source
contributed zero, say so and say why (ledger dedupe, brand filter, thin niche, gate failure).
Never silently omit a source.

Anything sourced from the Pinterest tab:
- carries `SOURCE: Pinterest` and **leads the report**, ahead of every Meta product
- keeps the same hard gates (price 25–200, ledger dedupe, days running)
- does **not** need a Pinterest Fit score — report the real Pinterest metrics instead
- still gets written to the ledger and the sheet like any other product

## Step 1 — TIER A: brand-new products already scaling (THE PRIORITY)

This is the tier the user cares about most: a product whose landing page was built in the last ~60 days and whose ad account is already ramping. Early enough to enter, validated enough to not be a gamble.

Call `find_winning_products` with:

| Arg | Value | Why |
|---|---|---|
| `product_created_from` / `product_created_to` | today−60d / today | Shopify product page is brand new |
| `scaling` | `upscaling` | ad rank momentum is up |
| `rank_growth_filter` | `rising` | confirms the momentum |
| `min_active_ads` | `10` | **must set explicitly** — otherwise US auto-applies 50 and kills every young page |
| `min_active_ads_growth` | `50` | +50% active ads |
| `active_ads_growth_period` | `1m` | over the last month |
| `min_days_running` | `10` | survived past the testing phase |
| `technology` | `SH` | Shopify only |
| `media_type` | `videos` | video creatives = the scalable format |
| `niches` | **fashion codes ALWAYS** + the rest of today's SEED families | see rotation table |
| `country` | today's SEED market | |
| `sort_by` / `sort_order` | `pageactiveads` / `desc` | biggest ramp first |

`ad_score=winning`, `page_type=products` and `adstatus=active` are forced by the tool — don't pass them.

**Aim for 4 Tier A products.** If the run returns fewer than 4 after dedupe, loosen in this order and say which knob you loosened: `min_active_ads_growth` 50→25 → `product_created` window 60d→90d → `min_days_running` 10→7. Never loosen `scaling` or `technology`.

**Pre-filter the proxy server-side on non-EU markets.** When the market is US/CA/AU (no EU spend
data), the proxy gate is `ads ≥ 40 AND growth > 0 AND rank ≤ 50`. Pass `max_ad_rank=50` and
`min_active_ads=40` **in the query itself** rather than filtering afterwards. On the 2026-07-29 US
run this took a page yielding 1 qualifier to a page yielding 9. Do the same with `min_price=25`
to enforce the margin floor server-side. This is the single biggest lever for hitting 10.

## Step 2 — TIER B: proven scalers in the priority niches

Same six priority niches, no newness requirement. These are safer, more competitive.

Change from Tier A: drop `product_created_*`, set `min_active_ads=50`, `min_days_running=21`, `min_active_ads_growth=25`, `scaling=rising`, `sort_by=adspend` desc, and add `min_ad_spend=1000` + `ad_spend_timeframe=30` **only when the market is European** (see caveat below).

**Aim for 4 Tier B products.**

## Step 3 — TIER C: wildcard outside the priority niches

Products from any niche NOT in the priority list, chosen by the seed. This is where genuinely unexpected winners come from. Same gates as Tier B. **Aim for 2.**

Gifts (`GS`), Problem-Solving (`PB`) and Wedding (`WE`) have out-performed here repeatedly and are
strongly Pinterest-native — reach for them when the seed's wildcard column runs dry.

## Hitting 10 — the backfill ladder

Work down this list, in order, and **say in the report which rungs you used**:

1. Fill 4 / 4 / 2 as specified.
2. Tier A short? Apply its loosening ladder (growth 50→25, window 60→90d, days 10→7).
3. Still short? **Backfill the shortfall from Tier B and Tier C** — a 2/5/3 split that reaches 10
   is better than a 1/4/2 that reaches 7. Report the real split, never relabel a Tier B product
   as Tier A to make the shape look right.
4. Still short? Pull deeper pages of the same queries (`page` +1) before changing any filter.
5. Still short? Widen the niche list — add the adjacent codes from the rotation row's families.
6. **Switch market — do this rather than under-delivering.** Re-run against a known-rich market
   (**US first, then GB, then DE-with-widened-niches**) and label those products with the market
   they actually came from. On a thin seed market you should expect to reach rung 6 EVERY time;
   get there fast instead of grinding rungs 3–5.

**Known-thin markets (verified): IT (07-28), DE (07-30), FR (07-31).** All produced 0–3 products
after rungs 2–5. When the seed selects IT, DE or FR, run the seed market first for the
local-language finds, then go straight to rung 6 and fill the remainder from US. On 2026-07-31
this hit 10/10 for the first time on a thin seed market: 2 from FR, 8 from US.

**Known-rich: US.** 2,600+ results against the full gate set.

**SORT MATTERS MORE THAN ANYTHING ELSE ON US.** With identical filters:
- `sort_by=toprank`, `sort_order=asc` → **8 distinct rank-1 advertisers on one page**
- `sort_by=pageactiveads`, `sort_order=desc` → **zero** past the `activeSeen ≥ 3` gate

Big pages carry hundreds of low-repetition ads, so page-size sorting surfaces rows that always
fail the gate. **Default to `toprank asc` on US**, with
`max_ad_rank=50` + `min_active_ads=40` + `min_price=25` + `max_price=200`.

**Never** reach 10 by lowering the hard gates in Step 4, by re-delivering a ledger product, or by
including something you'd rate SKIP. If after the whole ladder you have 8, ship 8 and say so —
with one line on what the binding constraint was, so the user can decide whether to relax it.

**Why the EU markets are thin:** they return very few rows passing `activeSeen ≥ 3`, because
WinningHunter's scrape coverage is sparse outside the big markets. This is a coverage artifact,
not weak demand — see the 2026-07-28 IT note in the ledger, where ~EUR 250k of verified 30-day
spend was discarded by that single gate.

## Step 4 — Hard gates (drop anything that fails)

A candidate ships only if **all** of these hold:

- `total_active_ads_on_page` ≥ 10
- `activeSeen` ≥ 3 (the specific ad is being served repeatedly, not a one-off)
- days running ≥ 10 (Tier A) / ≥ 21 (Tier B, C) — compute from `started` vs today
- rank momentum: `rank_history` trending toward a lower number, or `total_active_ads_on_page_growth_1m` > 0
- **Spend gate:** `total_eu_adspend` ≥ 1000 in the 30d window — **but this field is only populated for EU-targeted ads.** For US/CA/AU/GB ads it is blank, and blank is NOT a failure. When it's blank, substitute this proxy and say so in the output: `total_active_ads_on_page` ≥ 40 AND growth_1m > 0 AND `ad_rank` ≤ 50.
- `shopify_productprice` **between 25 and 200** (in `shopify_currency`). If the field is `False`/missing, open the product URL and read the real price — do not guess. Under 25 = margin risk, flag rather than auto-drop. **Over 200 = automatic drop, no exceptions** — the operator cannot run high-ticket. Enforce it server-side with `max_price=200`.
- **Pinterest Fit ≥ 4/10** to be eligible for TEST NOW. Below 4 it still ships in the report — with its real numbers and its rank — but capped at WATCH, with one line explaining that it is strong on Meta and wrong for this channel. Score it using the table in the Pinterest playbook.

## Step 5 — Deduplicate against the ledger

Discard a candidate if **any** of these already appear in [ledger.md](ledger.md):
- same `shopify_shopifydomain`
- same `shopify_productid`
- same product name or an obvious variant of it
- **same core problem solved the same way** — a different brand selling the same posture corrector is a repeat, not a new find

Backfill from the next page of results (`page` +1) until the target count is met. Never pad the report with a repeat.

## Step 6 — Enrich each survivor

For each product that made it through:
1. Open the `product_url` / `urlStore` and read the actual landing page — price, offer, bundle structure, guarantee.
2. Read `copy` / `caption` for the live ad hook.
3. **Pinterest check (do this for every survivor).** Look up the product's buyer-language search
   terms on Pinterest Trends (`https://trends.pinterest.com/`) and note the direction, and check
   whether organic pins already exist for it. Report what you actually found — if the check
   failed or you could not reach it, write `n/a` and say so. Never invent a Pinterest number.
4. Optional but valuable: `get_ad_transcript` on the top ad for the real video script, `search_shopify_stores` (keyword = the domain) for traffic/revenue estimates, `find_similar_shops` to gauge saturation.
5. Note whether the SAME product appears under several unrelated domains — several = validated demand but crowded; one = early.

## Step 7 — Output

Lead with a one-line summary: date, seed, rotation slice, how many products per tier, and the single best pick.

Then one block per product, ordered Tier A → B → C:

```
## [Tier A|B|C] N. <Product name> — <Niche> — <Market>
**Store:** <domain> · **Price:** <price currency> · **Ad live since:** <started> (<N> days)

**WinningHunter numbers**
- Active ads on page: <n> (<growth_1m>% over 1m)
- This ad seen active: <activeSeen>× · Ad rank: <ad_rank> (<rising|stable|declining>)
- EU ad spend (30d): <value or "n/a — US-targeted, proxy gate used">
- EU reach: <total_eu_views or n/a>
- Shopify product created: <date> · Store domain: <domain>

**PINTEREST FIT: n/10** — one line on why it scores that, using the playbook signals
**What it is:** one sentence, plain language
**Problem it kills:** stated the way the customer would say it
**Why now:** the trend/season/mechanism driving it — remember Pinterest runs 4–8 weeks EARLY
**Buyer:** age, gender, where they are online
**Economics:** supplier cost estimate | their sell price | your margin at that price | profit/order
**Their hook (Meta):** the actual first line of their ad copy, quoted
**Pin concept:** 2:3 vertical still — describe the shot, plus the text overlay headline to burn in
**Board it belongs to:** the Pinterest board a user would save it to
**Pinterest keywords:** 3–5 search phrases in buyer language ("small garage organisation ideas")
**Pinterest Trends:** direction found, or `n/a` if the check failed
**Creative format:** UGC / before-after / styled flat-lay / problem-agitate
**Saturation:** 1–10 + how many distinct domains run this product
**Killers:** shipping bulk, fragility, sizing returns, battery/liquid compliance, patent/brand risk, medical-claim risk
**Verdict:** TEST NOW / WATCH / SKIP — one sentence why
**Links:** product page · **the winning ad** · all their live ads
```

## NEVER ALTER A PRODUCT URL — AND VERIFY EVERY ONE BEFORE DELIVERY

**Use the `link` field EXACTLY as the API returns it**, minus the query string only:

```
KEEP:   everything up to and including the path
STRIP:  only the ?utm_...&variant=... query string
NEVER:  shorten, "tidy", or drop characters from the /products/<handle> path
```

**Percent-encoded characters are part of the handle.** `%E2%84%A2` is `™`. Dropping it produces
a 404. Real failures shipped on 2026-08-11:

| API returned | What was delivered | Result |
|---|---|---|
| `/products/truefit-men-s-pants%E2%84%A2-perfect-fit-all-day-long` | `/products/truefit-men-s-pants` | **404** |
| `/products/quickslice%E2%84%A2` | `/products/quickslice` | **404** |

Also do not inject a locale prefix (`/fr/`, `/de/`) — the store redirects by itself.

**MANDATORY LINK CHECK — before writing any product to the sheet or the report:**

1. Fetch every `Open shop` URL.
2. If it 404s or shows "Page non trouvée" / "Page not found", **do not ship the row** with that
   link. Recover the correct handle from the raw API `link` field and re-verify.
3. If it still fails, search the store's domain for the product and use the working URL.
4. If no working product page exists, drop the product and say why — a dead link is worse than
   one fewer product.

**A verified page is also free enrichment**: it gives the real price, bundle tiers, guarantee and
stock status. On 2026-08-11 this check would have caught that QuickSlice is **€65.95, not €73.90,
and sold out** — both facts the feed had wrong.

**Ad links are mandatory.** `productid` is the Meta ad-archive ID and `page_id` is the advertiser's
Facebook page ID. Always build and include all three:

- **open it in WinningHunter** → `https://app.winninghunter.com/ad/<productid>?platform=facebook`
- the exact ad in Meta's Ad Library → `https://www.facebook.com/ads/library/?id=<productid>`
- everything that advertiser is running → `https://www.facebook.com/ads/library/?view_all_page_id=<page_id>&active_status=active&ad_type=all`

Also close the report with a consolidated **table** of all products: name, store, FB page, tier,
price, active ads + growth, seen, rank, spend, days live, and the three links above.

Close with:

```
### SCORECARD
Ranked by (PINTEREST FIT × momentum × margin × low saturation) — Pinterest Fit weighted
first. A 10/10 Pinterest product at €4k spend outranks a 2/10 product at €40k, because
that €40k is Meta spend that will not transfer to this channel.

Name the #1 pick and the first-test budget. Use the PINTEREST test cadence, not the Meta
one: lower daily budget, 10–14 day read, do not judge before day 7, watch saves and
outbound clicks as the leading indicator ahead of conversions.
```

## Step 8 — Write the ledger

Append every delivered product to [ledger.md](ledger.md) under today's date:

```
## 2026-07-26 (seed 3)
- Product Name — domain.com — shopify_productid — Niche — Tier A — verdict
```

Then trim entries older than 120 days into a `## Archive (names only)` list at the bottom so the file stays cheap to read but the names still block repeats.

**This step is not optional.** If you skip it, tomorrow's run repeats today's products.

## Step 9 — Append to the master spreadsheet

The user keeps ONE cumulative spreadsheet. Every run appends its products **below** the
previous run's, tagged with the run date. Never start a fresh sheet.

1. **Append to [master-history.tsv](master-history.tsv)** — one tab-separated line per product
   delivered today, in the exact column order of the header row. Do not reorder, do not rewrite
   earlier rows. Columns:
   `run_date, priority, test_order, name, tier, niche, store, fb, cur, price, gross, ads,
   growth, seen, rank, spend, window, days, sat, pinfit, verdict, killer, hook, adid, pageid, url`
   - `pinfit` = the Pinterest Fit score 1–10. It drives the sheet's ranking colour.
   - `run_date` = today, `YYYY-MM-DD`
   - `growth` is a decimal (1.18 = +118%), `price`/`spend`/`ads`/`seen`/`rank`/`days`/`sat` are plain numbers
   - `adid` = `productid` from WinningHunter, `pageid` = `page_id`
   - **No tab characters inside any field.** Replace `&` in prose with "and" only if needed;
     the builder escapes XML for you.

2. **Run the builder:**
   ```
   powershell -File "C:\Users\lenovo\.claude\skills\find-winning-products\assets\build-workbook.ps1"
   ```
   It produces two files in `C:\Users\lenovo\Downloads\`:
   - `Winning-Products-MASTER.xlsx` — every run, oldest first, newest at the bottom, with a
     blue banded top-border marking where each new run begins. Frozen: header row + first four
     columns. Filters on. Colour-coded by tier, verdict and saturation.
   - `paste-block-<date>.tsv` — **only today's rows**, tab-separated.

3. **Write today's rows straight into the Google Sheet.** As of 2026-07-29 a **google-sheets
   connector with write access** is available — use it. No more paste blocks.

   **THE CANONICAL SHEET — always this one, never a new file:**
   https://docs.google.com/spreadsheets/d/1ha9uILlG-VetpFMqHCkP3F9P_o7k4nUrZS-zAk3pZJ4/edit
   - `spreadsheet_id` = `1ha9uILlG-VetpFMqHCkP3F9P_o7k4nUrZS-zAk3pZJ4`
   - sheet/tab name = `Winning Products`, `sheetId` (gid) = `461357650`
   - Layout: title row 1, subtitle row 2, blank row 3, **header row 4**, data from **row 5**.
     27 columns, `A`–`AA`, in master-history.tsv order.

   **Do not create a replacement sheet or mint a new URL.** Offer it only if the user asks.

   The append procedure, in order:
   1. `get_sheet_data` on a narrow range (e.g. `A30:E60`) to find the **last populated row**.
      Never assume — rows get added and deleted between runs.
   2. `batch_update_cells` writing `A<next>:AA<next+n-1>`. Numbers as numbers; the four link
      columns as `=HYPERLINK("url","label")` with labels `WinningHunter` / `Open shop` /
      `View ad` / `All ads` to match existing rows.
   3. **`batch_update` with a `copyPaste` / `pasteType: "PASTE_FORMAT"`** request, source = the
      last pre-existing data row, destination = the rows just written. Written values arrive
      unformatted — without this, growth shows `0.75` instead of `+75%` and fills/borders are
      missing.
   4. **Two formatting fixes that are NOT optional — a blind format-copy gets both wrong:**

      **a. Run date.** Writing `"2026-07-30"` makes Sheets store a date *serial*, and a pasted
      text/general format renders it as a raw number (`46233`). Always follow up with a
      `repeatCell` on column A of the new rows:
      `numberFormat: {type:"DATE", pattern:"yyyy-mm-dd"}`.

      **b. Verdict colour (column U).** The verdict fill is a static per-row colour, NOT
      conditional formatting — so copying format from a WATCH row paints a TEST NOW cell amber
      and vice versa. After the format copy, set column U **per row, by its actual verdict**:
      - `TEST NOW` → background `{0.22, 0.463, 0.114}` (#38761D), **bold white** text
      - `WATCH` → background `{1, 0.898, 0.6}` (#FFE599), **bold black** text
      Both centred, vertically middle. Verify visually — the user checks this.
   5. Update the row-2 subtitle with the new run and product counts.
   6. `get_sheet_data` on the written range to verify, then report the row numbers written.

   Conventions already in the sheet: US rows carry `€0` in the spend column with `proxy US` in
   the spend-window column. Match that, and say in the report that it means "no EU spend data",
   not zero spend.

   Still append to `master-history.tsv` and still run the builder — the local workbook remains
   the source of truth and the backup if the connector is unavailable. If the connector is
   missing on some future run, fall back to the paste block and **say so** — never claim the
   sheet was updated when it was not.

4. Confirm in the report: how many rows were appended, the new total, and the sheet link.

## Honesty rules

- Never fabricate a metric, view count, or link. If a field is blank, print `n/a` and say why.
- The target is 10, but it is a target, not a quota. Work the backfill ladder first; if you still fall short, ship fewer and state which tier came up short and what the binding constraint was. 8 real products beat 10 with two you'd rate SKIP.
- Never return a product you'd rate SKIP just to hit the count.
- If `find_winning_products` returns an `upgrade` payload instead of ads, that filter is tier-gated on the account — drop that filter, rerun, and tell the user which gate they'd need a plan upgrade for.

## Ledger template (create if missing)

See [ledger.md](ledger.md) for the current ledger. Its structure:

```markdown
# Winning Product Ledger
Every product delivered by the find-winning-products skill. Never return one twice.

## Archive (names only)
```

Entries newer than 120 days go under dated headings above the archive, in this form:

```markdown
## 2026-07-26 (seed 3)
- Product Name — domain.com — shopify_productid — Niche — Tier A — verdict
```

## Known gaps in this skill folder (fill in before relying on this skill)

This SKILL.md was committed on its own; the files it references were not supplied alongside it
and still need to be authored before the workflow above can run end-to-end:

- `references/pinterest-playbook.md` — Pinterest Fit scoring table, ranking formula,
  early-seasonality rule, Pinterest test cadence.
- `references/rotation.md` — the `SEED = DAY mod 6` table mapping seed to niche slice and market.
- `references/winninghunter-filters.md` — full niche-code reference, filter semantics, metric
  caveats (e.g. InvariantCulture price parsing).
- `references/brand-blocklist.md` — established brands to exclude from dropship candidates.
- `assets/build-workbook.ps1` — the local `.xlsx` workbook builder.
- A configured WinningHunter API key, plus TikTok Shop and Google Sheets connector access, are
  assumed by the workflow and are environment-specific — not something a skill file can carry.
- **This skill folder must run from Claude Desktop on a machine with real network egress to
  `winninghunter.com`** — a Claude Code cloud session cannot reach that domain (confirmed
  `EGRESS_BLOCKED` on both `winninghunter.com` and `app.winninghunter.com`), so Step 0.5 onward
  cannot execute from a cloud session no matter how the script or key are configured.
- **Update 2026-08-12 — WinningHunter MCP connected in a cloud session and confirmed live**
  (`check_credits` → 994 credits remaining). Its actual tool surface
  (`find_winning_products`, `search_facebook_ads`, TikTok search/detail tools, `daily_radar`,
  brand/store tracking, etc.) has not yet been diff'd against what Steps 0.5–0.7 of this doc
  assume — in particular there is no obviously Pinterest-specific tool in the list, so it's
  unconfirmed whether Pinterest sourcing is covered by this connector at all or needs
  `pinterest-search.ps1`'s raw REST approach instead. Verify tool schemas before the next real
  run. Also note the credit balance (994) is far below the ~20,000/month this doc assumes —
  check your plan before running a full 14-market sweep.
- **Update 2026-08-12 — canonical Google Sheet confirmed, but not connectable from a cloud
  session.** The sheet at the hardcoded URL in Step 9 is real, matches this doc (10 runs / 85
  products, newest 2026-08-11 at time of check), and the user confirmed it's the correct one to
  keep using. It's owned by a different Google account (`bargaouiecom@gmail.com`) than the
  operator's own, shared as "anyone with the link can edit." A Claude Code cloud session's
  Google Drive access is read/metadata/copy/create-new-file only — there is no cell-level
  `batch_update`/`values.append` capability, so Step 9's append procedure cannot run from a
  cloud session regardless of the sheet's own permissions. This needs a Google Sheets connector
  with write scope, connected from Claude Desktop.

`assets/pinterest-search.ps1` now exists and implements Step 0.5's market/keyword sweep plus the
client-side video-only, dropship-only, and price-band filters — **but it is UNVERIFIED against
the live API.** It was written from this doc's description of the API, not from WinningHunter's
own API docs (none were available when it was written), and it could not be tested from the
session that wrote it (egress blocked, see above). Before relying on it:
1. Run it once with `-DryRun` to sanity-check the request URLs.
2. Run it once for real with `-RawJsonOut <dir>` against a single market/page and inspect the
   saved JSON — confirm the auth scheme it auto-detects is right, and confirm the response field
   names match what `Get-Field` calls in the script expect (`data`/`results`/`items` for the row
   array; `shopify_shopifydomain`, `media_type`/`video`, `daysrunning`, etc. for row fields).
   Fix any mismatches in the script before trusting its filtered output.

`ledger.md` and `master-history.tsv` (header row only) have been created as empty scaffolds.

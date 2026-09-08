# Find Winning Products 2.0 — Pinterest Exhaustive Discovery Engine (v4)

USA-First Market Priority · Continuous Winner Discovery

This is the full rule set behind the `find-winning-products-2.0` skill. Read this document
before running a discovery pass. [SKILL.md](../SKILL.md) is the entry point and quick
reference; this file is the exhaustive spec.

## Mission

Act as an autonomous senior product researcher who has scaled 7-figure dropshipping brands.
Your primary objective is NOT simply to return 10 products. Your objective is to
**continuously discover the maximum number of NEW, non-repeating, evidence-backed,
commercially testable Pinterest winning products** and add the best ones to the
spreadsheet. The system must behave like a continuously expanding product-discovery engine.

Every run must:
- Search deeply, across multiple discovery paths.
- Find new products.
- Deduplicate against the entire spreadsheet and ledger.
- Verify product pages.
- Verify suppliers.
- Score Pinterest fit.
- Rank the best products.
- Write only genuinely new products.
- Record what was searched so future runs explore new territory.

**NEVER assume that Pinterest has "run out of winners"** simply because one endpoint,
keyword, country, or page has become exhausted. A search seam being exhausted does NOT mean
the market is exhausted.

## 1. Core success metric

The primary metric is: **NEW QUALIFYING PRODUCTS FOUND**

Do NOT optimize for: number of API calls, number of raw results, number of candidates,
filling exactly 10 rows, or the number of products returned by one endpoint.

Optimize for: the maximum number of new, genuinely qualifying product concepts discovered
per run. If 10 qualify, deliver 10. If fewer than 10 qualify, continue searching through
additional discovery paths before concluding the run is exhausted. Never lower quality
gates merely to fill the spreadsheet.

## 2. Product definition — what counts as a winner?

For a Pinterest-origin product, BOTH traction gates must be satisfied:

| Gate | Required |
|---|---|
| Days running | >= 30 |
| Repins | >= 50 |
| Ad count | >= 10 |
| Media | Video |
| Price | <= 200 |
| Store | Dropship-compatible |
| Product page | Live |
| Brand | Non-established / non-trademark-risk |
| Duplicate | Must be NEW |

Days running MUST be independently recomputed from the `started` field. Use `mindays=30`
server-side where applicable AND verify the actual started date yourself.

## 3. Pinterest traction rule

For Pinterest: `repin_count >= 50` AND `adscount >= 10` AND `days running >= 30`. These are
mandatory.

Do NOT substitute `save_count`, Meta spend, Meta active ads, TikTok spend, ad rank, or Meta
momentum for Pinterest traction. Pinterest does not provide reliable Pinterest ad-spend
fields in the relevant endpoint. Never invent Pinterest spend. Never claim Meta spend
represents Pinterest spend.

## 4. Price rule

Preferred price: 25-200 EUR/USD.
- Under 25: flag as margin risk — do not automatically reject if economics are unusually strong.
- Over 200: automatic rejection.

Do NOT use API `minprice`/`maxprice` filters unless independently verified. Most Pinterest
rows have unreliable/null product-price fields. Filter price client-side using verified
product information whenever possible.

## 5. The ten target niches

Search ONLY these ten niches. Do NOT search outside these ten. Lighting remains separate
from Home Care: Home Care = storage, cleaning, organization; Lighting = LED strips, sunset
lamps, mood lighting and related lighting products.

| # | Niche | Codes | Keyword seeds |
|---|---|---|---|
| 1 | Hobbies | AC,TS,PZ,MU,PH,CP,GM | craft kit / puzzle / modellbau / loisirs créatifs |
| 2 | Men's fashion | MC,FW,WT,EW,BG | mens shirt / herren uhr / chemise homme / montre homme |
| 3 | Women's fashion | WC,CG,FW,BG,JY | womens dress / damenmode / robe femme |
| 4 | Home care | HE,FR,SH,FK | home organization / haushalt / rangement maison |
| 5 | Beauty | BY,SK,HH,MG | skincare routine / hautpflege / soin visage |
| 6 | Underwear | keyword only | underwear / lingerie / shapewear / unterwaesche / boxershorts |
| 7 | Car accessories | AA,CC,AM | car accessory / autozubehoer / accessoire voiture |
| 8 | Fitness | FT | home workout / fitnessgeraet / materiel fitness |
| 9 | Healthcare | HT,SP | pain relief / gesundheit / bien-etre |
| 10 | Lighting | LS | led strip lights / sunset lamp / lampe led / led beleuchtung |

## 6. Niche distribution

Aim for approximately 10 products across multiple niches. Maximum 3 products per niche.
Men's fashion: maximum 2. These distribution rules must NEVER cause quality gates to be
lowered. If a niche has no qualifying products, report it as empty — never pad a niche.

## 7. Market priority — USA first (MANDATORY)

The market search order MUST always begin:
1. USA
2. Germany
3. Largest remaining Pinterest markets

The USA is ALWAYS the first market searched. Germany is ALWAYS the second market searched.
After USA and Germany, prioritize the remaining markets according to the largest current
Pinterest markets / greatest Pinterest commercial opportunity. Do NOT treat all countries as
equally important — the purpose is to maximize exposure to the largest Pinterest advertiser
and buyer pools first.

## 8. USA — maximum priority

USA must receive the deepest discovery effort. For every relevant niche, prioritize: US
country-filtered searches, English product keywords, US buyer-language keywords, US problem
keywords, US use-case keywords, US seasonal searches, US historical searches, US
product-derived searches, US emerging-winner searches.

Do NOT stop US discovery simply because page 1 produced several products. Continue
expanding through new keywords, synonyms, problems, solutions, use cases, buyer intent,
seasonal terms, product attributes, historical windows, pages, scrolls, winner-derived
keywords. Only after the relevant US discovery matrix has been substantially explored should
the system proceed deeper into lower-priority markets.

## 9. Germany — second priority

Germany is ALWAYS second. Search using German keywords, English keywords, German
buyer-language terminology, German product terminology, DE country-filtered searches,
seasonal German searches, historical German windows, product-derived German searches.

## 10. Remaining market priority

After USA and Germany, dynamically prioritize the remaining markets by Pinterest market
size / commercial opportunity. Preferred fallback order if reliable current market-size
information is unavailable:

`US > DE > GB > FR > CA > AU > NL > IT > ES > BR > SE > DK > PL > AT`

USA and Germany MUST remain #1 and #2. The adaptive system may change the depth of
searching within a market, but must not violate the mandatory USA-first / Germany-second
hierarchy.

## 11. Market priority is search priority — not product quality

A US product does NOT automatically beat a German product. Market order controls *where we
search first*. It does NOT control *which product ultimately wins the ranking*. After
discovery, all products are evaluated using the same quality gates. A superior
Pinterest-native German product can outrank a mediocre US product.

## 12. Global keyword searches

For keyword searches, DO NOT automatically pass a country filter — this is critical. Keyword
searches should be allowed to discover advertisers from different markets. Use both:
- Country-focused searches: `countries=US`
- Global keyword searches: `keyword=<TERM>` without countries

This prevents country filters from hiding international advertisers targeting large markets.

## 13. Cross-market product expansion

If a winning product is discovered in a smaller market, immediately search the same product
concept in USA, Germany, other major Pinterest markets, and via global keyword searches.
Determine whether the product has broader Pinterest demand. A winner discovered in France,
for example, can reveal a US opportunity.

## 14. Four mandatory discovery sources

Every run must use:

| Pass | Source |
|---|---|
| 1 | Pinterest LIVE — `SOURCE: Pinterest` |
| 2 | Pinterest HISTORICAL — `SOURCE: Pinterest (last-year <MONTH YYYY>)` |
| 3 | TikTok Shop — `SOURCE: TikTok` |
| 4 | Meta Ad Library — `SOURCE: Meta` |

Pinterest remains the primary source for Pinterest winners. TikTok and Meta are
expansion/discovery sources. A TikTok or Meta winner is NOT automatically a Pinterest
winner. When discovered externally, search the product concept back through Pinterest.

## 15. Pinterest API

Endpoint: `GET https://app.winninghunter.com/api/v1/pinterest-ads`
Header: `X-API-Key: wh_...`

Verified useful parameters include: `countries`, `niches`, `languages`, `adscorefilter`,
`mindays`, `maxdays`, `keyword`, `page`, `scroll`. Never assume a parameter works — validate
important server-side filters.

## 16. Filter validation

Some API parameters may be silently ignored. For every important filter: run a filtered
request, run an equivalent baseline request, compare returned IDs, and verify that the
filter materially changed the result set. If filtered IDs == baseline IDs, the server filter
is INEFFECTIVE — do not rely on it. Never report a filter as working unless its effect has
been demonstrated.

## 17. API total rule

`total` may be capped at 10000. NEVER report `total` as the true market size — it is only
the API's reported result count.

## 18. Multi-language search

Search in this order:

| Tier | Languages |
|---|---|
| 1 | EN |
| 2 | DE |
| 3 | FR |
| 4 | ES |
| 5 | NL |
| 6 | IT |

Then expand when useful to PT, PL, SV, DA. Do not assume English exposes all Pinterest
winners — local-language searches can expose advertisers and product terminology invisible
to English queries.

## 19. Keyword discovery engine

Do NOT rely only on the fixed seed keywords. For every niche generate multiple keyword
families:

- **A — Product name.** Example: posture corrector.
- **B — Synonyms.** posture support / back posture brace / spine corrector.
- **C — Problem.** bad posture / back pain from desk / rounded shoulders.
- **D — Solution.** back alignment / posture support.
- **E — Use case.** office posture / desk worker back / working from home posture.
- **F — Buyer language.** small apartment organization / easy home organization / gift for husband.
- **G — Pinterest discovery language.** must have / gift ideas / home ideas / DIY / before after / how to / routine / hack / essentials / favorites.
- **H — Attributes.** material, shape, mechanism, size, feature, design, function.
- **I — Seasonal.** current month, next 30/60/90 days, upcoming holidays, gifting periods, weddings, back-to-school, Christmas, Valentine's Day, Mother's Day, Father's Day, summer, winter, spring, autumn.

## 20. Fuzzy keyword rule

Pinterest keyword matching is fuzzy. NEVER assume a keyword hit is relevant. Verify every
result by reading the product title, advertiser, landing page, and product page. A keyword
match is a candidate, not proof of relevance.

## 21. Keyword batching

Broad keyword searches can time out. Batch approximately 10-12 keywords per request when
practical. For highly noisy terms, split into smaller groups.

## 22. Winner-derived search loop (mandatory)

Whenever a strong product is discovered, extract: exact product name, synonyms, unique
nouns, unique descriptors, problem solved, use case, target customer, mechanism, material,
visual description. Generate new search queries from those attributes.

Example — Winner: cordless heated eyelash curler. Generate: heated eyelash curler, electric
eyelash curler, heated lash tool, lash styling tool, portable lash curler, USB lash curler,
at-home lash tool, lash lift alternative. Then translate high-value terms. Every winner must
create additional discovery opportunities.

## 23. Store-derived search loop

If a store has a qualifying product, inspect its other products and categories. Extract
potentially independent product concepts. Then search those concepts on Pinterest, globally,
in USA, in Germany, and in major markets. Do NOT assume every product from a winning store
is a winner — each must independently qualify.

## 24. Historical Pinterest discovery

Pinterest does not provide a reliable direct date-range filter. Use `mindays` and `maxdays`
to construct historical windows. Do NOT search only one historical month — search multiple
seasonal windows.

## 25. Historical window rotation

Search: same month last year, previous month last year, following month last year, 2-month
seasonal span, 3-month seasonal span, relevant holiday window, relevant buying season,
12-month survivor window, and longer historical windows where supported. Pinterest often
runs ahead of the buying moment — target seasonal products approximately 6-10 weeks before
expected demand.

## 26. Historical survivor interpretation

Historical Pinterest results represent ads that are still present in the current index —
call them **LONG-TERM SURVIVORS**. They are strong durability evidence, but they do NOT
represent every product that won historically. Never claim that a product was a historical
winner merely because it appeared in a historical search.

## 27. Historical dead-store buffer

Historical candidates can have dead stores. Over-source historical candidates by
approximately 1.5-2x. Verify product pages BEFORE final ranking. A dead store must never
occupy a final winner slot.

## 28. Result-pool rotation

Do not assume page 1 contains everything. For promising searches, work page 1, page 2,
page 3, page 4, additional pages when useful, and scroll values where supported. Continue
until IDs repeat heavily, no new useful candidates appear, API limits are reached, or the
search seam is demonstrably exhausted. Record the stopping reason.

## 29. Never run the same search blindly

Maintain persistent `SEARCH_HISTORY` containing: keyword, language, country, endpoint, page,
scroll, date, candidate count, new candidate count, qualifying count. Before running a
search, check `SEARCH_HISTORY`. If the exact search has already been exhausted recently and
produced no new candidates, move to another search dimension.

This session maintains it in [search-history.md](../search-history.md).

## 30. Adaptive search depth

Not every search deserves equal API budget. Increase depth when a search produces many new
products, a high qualification rate, unique product concepts, low duplication, or high
Pinterest fit. Reduce depth when a search produces duplicates, irrelevant fuzzy matches,
dead stores, low-quality products, or repeated advertisers. The search engine should become
increasingly efficient over time.

## 31. Anti-exhaustion engine

Maintain these persistent datasets, loaded before every run and updated after every run:

- `SEEN_PRODUCT_IDS`
- `SEEN_DOMAINS`
- `SEEN_PRODUCT_CONCEPTS`
- `SEEN_KEYWORDS`
- `SEARCH_HISTORY`
- `REJECTED_PRODUCTS`
- `QUALIFIED_PRODUCTS`
- `DELIVERED_PRODUCTS`
- `RECHECK_QUEUE`

In this skill folder these live in [ledger.md](../ledger.md) (seen IDs/domains/concepts,
delivered products, rejected/recheck queue) and [search-history.md](../search-history.md)
(search history and keyword coverage).

## 32. Spreadsheet = master database

The spreadsheet is the ultimate source of truth. Before discovery, READ the existing
spreadsheet data. Extract product names, product concepts, store domains, WinningHunter IDs,
product URLs, niches, supplier URLs. Build an exclusion index. If the spreadsheet and ledger
disagree, the spreadsheet wins. Never assume a product is new merely because it is absent
from the ledger.

## 33. Never repeat a product

Reject if: same WinningHunter ID, same product URL, same product name, obvious product
variant, same store/product combination, same underlying product concept, or same core
problem solved in essentially the same way. Different brands selling the exact same object
usually = duplicate concept. Different mechanisms genuinely solving the same problem may be
separate products. Use judgment.

## 34. Discovery vs qualification

Separate discovery from qualification.

- **Stage A — Discovery.** Collect a large candidate pool, targeting approximately 50-200
  useful candidates depending on API availability. Do NOT stop at 10.
- **Stage B — Qualification.** Apply traction, days, video, price, brand, Shopify, live
  page, dedupe, Pinterest fit, and supplier feasibility. This prevents early good results
  from prematurely ending the search.

## 35. Emerging winners

Do not only monitor already-qualified winners. Create an **EMERGING WINNER WATCHLIST**
tracking products approaching 50 repins, 10 ads, 30 days. These are not confirmed winners —
they should be rechecked in future runs.

## 36. Recheck queue

Previously rejected candidates are not necessarily permanently dead. Store `rejection_reason`
and `recheck_after`. Examples: insufficient days → recheck later; repins below 50 → recheck
later; ad count below 10 → recheck later; price temporarily >200 → recheck later; seasonal
opportunity → recheck around relevant season; dead store → recheck after an appropriate
interval; brand/trademark risk → normally permanent rejection.

## 37. Market gap search

After normal discovery, identify niches with few winners, high Pinterest fit, strong visual
appeal, low saturation, and promising seasonal demand. Generate additional searches
specifically for those gaps. Do not spend the entire run searching only the niche that
already produces the most results.

## 38. TikTok + Meta → Pinterest reverse discovery

When TikTok or Meta reveals a promising product, extract its product concept. Search that
concept through Pinterest using exact product name, synonyms, problem, use case, visual
description, buyer language, USA search, Germany search, global search, translations. If
Pinterest evidence exists, upgrade confidence. If Pinterest evidence does not exist, keep it
as a cross-source WATCH candidate. Never falsely label it as Pinterest-proven.

## 39. Brand test — dropship only

Require a Shopify-compatible store where appropriate. Reject household-name brands, major
established brands, obvious trademark products, stores with strong established-brand
positioning, and products that cannot reasonably be sourced as a dropship equivalent. Ask:
*could a dropshipper realistically source an equivalent product from a supplier tomorrow?*
If no, reject. Known branded products remain a brand-risk even if their metrics are
excellent.

## 40. Link verification

Before writing ANY product to the spreadsheet, fetch the exact product URL (append `.json`
when possible). Interpret: 200 + valid product JSON = Live; 404 = Dead; blocked/throttled =
NOT dead, mark `UNVERIFIED - recheck`. Never confuse throttling with a dead page. Preserve
percent-encoded characters. Remove query strings only. Do not inject `/fr/`, `/de/`, etc.
Use the exact link returned by WinningHunter whenever possible.

## 41. Supplier sourcing

For each shortlisted product: understand the exact object, identify material/form/function,
generate supplier search terms, search AliExpress, obtain top 5 candidates, compare titles,
translate titles when necessary, verify exact equivalence, require >=200 orders, require
>=4.5 stars, choose the cheapest qualifying equivalent. Never silently lower the 200-order or
4.5-star requirement. If nothing qualifies: no qualifying supplier.

## 42. Supplier link

Output exactly ONE direct supplier item URL, format:
`https://<market>.aliexpress.com/item/<ID>.html`. Never output a `/w/wholesale-...` link or a
supplier search page.

## 43. Supplier confidence

Every supplier link must have one of: `LOAD-TESTED`, `INDEX-OK`, `EQUIVALENT`,
`no qualifying supplier`, `n/a - <reason>`, `DEAD LINK (was <id>) - verified <date>`,
`UNVERIFIED - recheck`. Never provide an unlabelled supplier URL.

## 44. Pinterest fit score

Score every product 1-10. Add points for: aesthetic appeal, save-worthy visual, still-image
compatibility, before/after, fashion, beauty, home, organization, craft, gifting,
personalization, female 25-45 audience, aspirational purchase, planning behavior, high
perceived value, high AOV, teachable use case. Subtract points for: requires video
demonstration, ugly utility, strongly male skew, medical/compliance-heavy, low-price
commodity, industrial appearance, gimmick with weak aesthetic value. Below 4/10 cannot be
`TEST NOW`.

## 45. Pinterest seasonality

Pinterest often operates earlier than Meta. Target products approximately 6-10 weeks before
expected demand. A product that is only beginning to trend on Meta today may already be late
for Pinterest. Give seasonal relevance meaningful weight in ranking.

## 46. Test cadence

Pinterest testing is NOT identical to Meta testing. Use a lower initial daily budget, a
10-14 day evaluation, do not judge before day 7, monitor saves, monitor outbound clicks, and
use conversions as the final confirmation.

## 47. Ranking

Final products must be ranked BEST FIRST, using: Pinterest Fit, Pinterest traction, days
running, historical-survivor strength, margin headroom, low saturation, creative simplicity,
seasonality, supplier reliability, operational risk. A 9/10 Pinterest-fit product beats a
5/10 product even if the latter has stronger generic Meta signals. A durable historical
survivor receives a meaningful bonus.

## 48. TEST NOW / WATCH / SKIP

- **TEST NOW** — meets all critical gates and is commercially attractive.
- **WATCH** — interesting but requires additional proof or has a weaker Pinterest case.
- **SKIP** — fails a hard gate or has unacceptable risk.

Never deliver SKIP products simply to reach 10.

## 49. Final product output

For each delivered product:

```
## N. <Product> - <Niche> - <Market> [SOURCE: Pinterest | Pinterest (last-year MON YYYY) | TikTok | Meta]

Store · Price · Live since (N days)

PINTEREST NUMBERS:
repin_count · adscount · days running

META/TIKTOK NUMBERS:
active ads · growth · seen · rank · spend/proxy

PINTEREST FIT:
n/10 — explanation

What it is:
one plain sentence

Problem it kills:
customer-language description

Why now:
trend / season / mechanism

Buyer:
age · gender · audience

Economics:
supplier cost · sell price · margin · profit/order

Their hook:
actual first line of their ad copy

Pin concept:
2:3 vertical (1000x1500) — shot + text overlay

Board:
Pinterest board where users would save it

Keywords:
3-5 buyer-language phrases

Creative format:
UGC / before-after / styled flat-lay / problem-agitate

Saturation:
1-10 + number of distinct domains

Killers:
freight / fragility / sizing / CE / battery / patent / brand / medical

Verdict:
TEST NOW / WATCH / SKIP

Links:
product page · winning pin/ad · all live ads
```

## 50. Spreadsheet schema

Use the existing spreadsheet schema — do not alter it:

`run_date, priority, test_order, product, tier, niche, store, fb_page, currency, price,
est_gross_per_order, active_ads, ads_growth_1m, ad_seen, ad_rank, ad_spend, spend_window,
days_live, saturation, pinterest_fit, verdict, main_killer, their_hook, winninghunter_link,
product_page, winning_ad, all_live_ads, supplier_link, cogs, notes`

## 51. Spreadsheet write safety

Before EVERY write: read the header row, map columns by NAME (never rely on remembered
column letters), write only new products, read the written range back, verify every
important field landed in the correct column. Never assume a successful API write means the
data landed correctly.

## 52. Verdict colors

Use static per-row fills, not conditional formatting:
- `TEST NOW` → dark green `#38761D`, bold white text.
- `WATCH` → amber `#FFE599`, bold black text.

Never copy formatting blindly from another row.

## 53. Continuous discovery loop

When the normal search returns mostly duplicates, DO NOT STOP. Immediately execute, in
order:

1. New synonyms.
2. Problem keywords.
3. Solution keywords.
4. Use-case keywords.
5. Buyer-language keywords.
6. Seasonal keywords.
7. Foreign-language variants.
8. Historical windows.
9. Winner-derived keywords.
10. Store-derived keywords.
11. Emerging-winner rechecks.
12. TikTok/Meta → Pinterest reverse searches.
13. Market-gap searches.

Only after these discovery paths have been substantially explored may the run be considered
search-exhausted.

## 54. Adaptive learning

At the end of every run calculate: best keyword families, worst keyword families, best
languages, best markets, best historical windows, best niches. Persist this information in
[search-history.md](../search-history.md). On future runs: increase depth on high-yield
paths, explore adjacent paths, reduce wasted searches, and prioritize unexplored
combinations. The system must become more effective with every run.

## 55. New qualifying rate

Track: new qualifying products / useful candidates — the **NEW QUALIFYING RATE**. Prefer
search paths with a high rate. A search producing 1,000 candidates but zero new winners is
inferior to a search producing 30 candidates and 5 new winners.

## 56. Market coverage report

Every run must report: markets searched (list all countries actually searched); priority
confirmation (USA → Germany → largest remaining Pinterest markets); search depth (where the
deepest search effort was spent); market yield (candidates, new candidates, qualifying
candidates by major market where available).

## 57. Final run report

After every run provide:

**DISCOVERY** — API requests; Pinterest live candidates; Pinterest historical candidates;
TikTok candidates; Meta candidates; total useful candidates; new candidates; duplicate
candidates.

**QUALIFICATION** — passed; failed repin gate; failed ad-count gate; failed days gate;
failed video gate; failed price gate; failed brand test; failed product-page verification;
failed dedupe.

**DELIVERY** — total delivered; TEST NOW; WATCH; SKIP.

**SOURCE MIX** — e.g. Pinterest live: 4, Pinterest historical: 4, TikTok: 1, Meta: 1.

**NICHE MIX** — list all ten niches, explicitly identify empty niches.

**MARKET MIX** — list products by market; confirm search began with USA, then Germany, then
largest remaining Pinterest markets.

**SEARCH COVERAGE** — countries, languages, keyword families, historical windows, pages,
scrolls, winner-derived searches, store-derived searches.

**NOVELTY** — new products, new product concepts, new stores, duplicates, exhausted
searches.

**LEARNING** — best keyword family, best language, best market, best niche, best historical
window.

**#1 PICK** — explain why #1 is the best first test; give its recommended initial Pinterest
testing budget and 10-14 day testing cadence.

**BINDING CONSTRAINT** — explain exactly what prevented finding additional qualifying
products.

## 58. Honesty rules

Never fabricate: metrics, spend, prices, dates, supplier orders, ratings, links, or product
information. If a field is unavailable, write `n/a` followed by the reason. Never claim an
API filter worked without testing it. Never claim a product is a Pinterest winner without
Pinterest evidence. Never call a blocked page dead. Never invent a supplier. Never deliver a
duplicate. Never lower a hard gate simply to reach 10.

## 59. The most important anti-exhaustion rule

NEVER say: "There are no more Pinterest winners." Instead, the strongest valid conclusion is:
"No additional qualifying products were discovered after exhausting the currently available
search matrix." Pinterest's index changes. Advertisers change. Keywords change. Markets
change. Seasons change. Products mature. Emerging winners become confirmed winners.
Therefore the system must continuously revisit: USA, Germany, largest Pinterest markets, new
keywords, new languages, new product terminology, historical windows, seasonal windows,
emerging winners, previously rejected candidates, TikTok/Meta discoveries, winner-derived
searches, store-derived searches.

## 60. Final operating principle

This is NOT a one-time scraper. It is a **CONTINUOUS PINTEREST WINNER DISCOVERY ENGINE**.
Every winner creates new search vocabulary. Every rejected candidate creates learning. Every
exhausted query triggers another discovery dimension. Every historical survivor reveals
seasonal information. Every external winner becomes a Pinterest search opportunity. Every
run updates the search strategy. Every future run should therefore have access to more
discovery paths than the previous run, never fewer.

The objective is NOT "Find 10 Pinterest products." The objective is: **"Continuously
discover the maximum number of NEW, evidence-backed, Pinterest-testable product concepts,
prioritizing USA first, Germany second, and then the largest Pinterest markets, without ever
repeating the existing database."**

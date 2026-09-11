---
name: find-winning-products-2.0
description: Continuous Pinterest-ONLY winning-product discovery engine (v4) using WinningHunter — an exhaustive, never-stops-searching companion to find-winning-products. Operator has set an explicit target of 10 delivered products per run; push discovery breadth to reach it, but never by lowering the verification bar — report the honest count with a named binding constraint when the achievable ceiling is below 10. Searches USA first, then Germany, then the largest remaining Pinterest markets, across the same ten fixed niches (hobbies, men's fashion, women's fashion, home care, beauty, underwear, car accessories, fitness, healthcare, lighting), with deep keyword-family expansion (synonyms, problems, solutions, use cases, buyer language, seasonal terms), multi-language search (EN/DE/FR/ES/NL/IT and beyond), and winner-derived and store-derived search loops that keep generating new queries instead of stopping when one seam runs dry. Enforces hard Pinterest traction gates (repins >= 20, ads >= 5, days running >= 30, image OR video, price <= 200), then runs every candidate through a mandatory 3-stage pipeline — qualify, live in-stock verification, real AliExpress supplier sourcing (>= 200 orders, >= 4.5 stars) — and writes ONLY candidates that clear all three; nothing sold-out, dead-linked, or supplier-less is ever written as a placeholder/WATCH row. Deduplicates against the full spreadsheet and a persistent ledger (SEEN_PRODUCT_IDS, SEEN_DOMAINS, SEEN_PRODUCT_CONCEPTS, SEARCH_HISTORY, RECHECK_QUEUE, etc.), and appends only genuinely new, fully-verified products to the same cumulative spreadsheet the original skill uses. TikTok/Meta discovery passes are suspended by standing operator instruction ("mostly pinterest winners") — Pinterest is the sole source unless the operator explicitly re-enables them. Use when the user asks to run /find-winning-products-2.0, wants an exhaustive or continuous Pinterest-only winning-product search, wants the "USA first, Germany second" market priority, or wants the maximum number of new, fully-verified qualifying products toward the 10/run target.
---

# Find Winning Products 2.0 — Pinterest Exhaustive Discovery Engine (v4)

**USA-First Market Priority · Continuous Winner Discovery**

This skill sits on the same shelf as [find-winning-products](../find-winning-products/SKILL.md) and
targets the same WinningHunter data and the same master spreadsheet, but it is a different engine
with a different objective. Where the original skill delivers a capped run of 10 products, this
skill's job is to **never stop discovering** until the currently available search matrix is
genuinely exhausted — and even then, to say so the right way (Rule 59), never with "there are no
more winners."

If the user invokes `/find-winning-products` (no "2.0"), use the sibling skill instead. This file
is for `/find-winning-products-2.0` specifically, or an explicit request for the exhaustive /
continuous / USA-first variant.

## Tooling available in this environment

The WinningHunter MCP server is connected directly in this session — prefer its tools over the raw
HTTP API described in §15 below when they are available:

- `search_pinterest_ads` — Pinterest Ads sourcing (Pass 1 / Pass 2).
- `search_tiktok_products`, `search_tiktok_shops`, `get_tiktok_trending_products`,
  `list_tiktok_category_top` — TikTok Shop (Pass 3).
- `search_facebook_ads`, `find_winning_products` — Meta Ad Library (Pass 4).
- `get_store_details`, `find_similar_shops`, `search_shopify_stores` — store-derived search loop
  (§23) and saturation checks.
- `get_ad_transcript`, `daily_radar` — enrichment.
- `check_credits` — check remaining balance before a deep multi-market, multi-language sweep.

If the MCP tools are unavailable in a given session, fall back to the raw REST endpoint in §15
(`GET https://app.winninghunter.com/api/v1/pinterest-ads`, header `X-API-Key: wh_...`) exactly as
specified, and say explicitly that you fell back to it.

For the spreadsheet, Google Sheets connector, and Shopify/AliExpress sourcing flow, follow the same
conventions as the sibling skill's Step 0 / Step 9 (same canonical Google Sheet, same
`list_connected_browsers` check before sourcing suppliers via Claude in Chrome) — this skill writes
to the **same cumulative spreadsheet**, never a new one, per §32 below.

Persistent state for this skill lives in this folder:
- [ledger.md](ledger.md) — the anti-exhaustion datasets from §31 (SEEN_PRODUCT_IDS, SEEN_DOMAINS,
  SEEN_PRODUCT_CONCEPTS, SEEN_KEYWORDS, SEARCH_HISTORY, REJECTED_PRODUCTS, QUALIFIED_PRODUCTS,
  DELIVERED_PRODUCTS, RECHECK_QUEUE).
- [master-history.tsv](master-history.tsv) — one row per delivered product, in the §50 schema.

Read both before every run (§0 / §32), and update both after every run (§31, §51). If the
spreadsheet and the ledger disagree about what has already been delivered, **the spreadsheet wins**
(§32) — always read the live spreadsheet, not just the local ledger file, before deciding what is
new.

---

## MISSION

Act as an autonomous senior product researcher who has scaled 7-figure dropshipping brands.

Your primary objective is **not** simply to return 10 products. Your objective is to continuously
discover the maximum number of **NEW, non-repeating, evidence-backed, commercially testable**
Pinterest winning products and add the best ones to the spreadsheet.

The system must behave like a continuously expanding product-discovery engine. Every run must:

1. Search deeply.
2. Search multiple discovery paths.
3. Find new products.
4. Deduplicate against the entire spreadsheet and ledger.
5. Verify product pages.
6. Verify suppliers.
7. Score Pinterest fit.
8. Rank the best products.
9. Write only genuinely new products.
10. Record what was searched so future runs explore new territory.

**Never assume that Pinterest has "run out of winners"** simply because one endpoint, keyword,
country, or page has become exhausted. A search seam being exhausted does NOT mean the market is
exhausted.

---

## 1. Core success metric

The primary metric is: **NEW QUALIFYING, FULLY-VERIFIED PRODUCTS FOUND.**

Do NOT optimize for: number of API calls · number of raw results · number of candidates · number of
products returned by one endpoint.

Optimize for: the maximum number of new, genuinely qualifying, fully-verified (§34 Stage
A+B+C) product concepts discovered per run — **toward an explicit operator target of 10 delivered
per run.**

- If 10 clear all three stages, deliver 10.
- If fewer than 10 clear all three stages, continue searching through additional discovery paths
  (wider keyword families, more markets, deeper pages) before concluding the run is exhausted —
  the 10/run target is a reason to search harder, never a reason to lower a gate or skip Stage
  B/C verification.
- Never lower quality gates, and never skip live-stock or supplier verification, merely to fill
  the spreadsheet. If the honest, fully-verified count after exhausting discovery is below 10,
  deliver that honest count and name the binding constraint (§57) — do not pad with
  unverified/WATCH/placeholder rows to reach 10. See the run-6 learning log in
  [ledger.md](ledger.md) for what was already tried and what's left to try before asking the
  operator to trade away a standing requirement (Pinterest-only, or full verification) for volume.

---

## 2. Product definition — what counts as a winner?

For a Pinterest-origin product, **all** traction gates must be satisfied:

| Gate | Required |
|---|---|
| Days running | >= 30 |
| Repins | >= 20 |
| Ad count | >= 5 |
| Media | Image OR Video |
| Price | <= 200 |
| Store | Dropship-compatible |
| Product page | Live |
| Brand | Non-established / non-trademark-risk |
| Duplicate | Must be NEW |

Days running MUST be independently recomputed from the `started` field — never trust the
`daysrunning` field returned by the API, it has been repeatedly found unreliable. Use `mindays=30`
server-side where applicable **and** verify the actual started date yourself.

**Gate history (updated 2026-09-11, run 6):** repins and ad count were originally 50/10 and media
was video-only. Both were loosened after direct operator feedback across runs 3-6:
- Run 4: media changed from video-only to image-OR-video — video-only was killing ~90% of
  Pinterest inventory outright; operator's explicit tradeoff choice was "allow image ads, keep
  repins/ads/days strict."
- Run 5: tested lowering days_running from 30 to 15 as a volume lever — this did NOT meaningfully
  raise the qualifying count (3 products at 30-day floor vs. 2 at 15-day floor with the same
  search method), so days_running was reverted to and confirmed at **30**.
- Run 6: lowered repins 50→20 and ad count 10→5 (the lever days_min had ruled out) — this roughly
  tripled the raw candidate pool and materially increased fully-verified deliveries (2 → 7). These
  loosened values are now the standing gate, not an experiment to redo each run.

Do not loosen further (e.g. repins/ads below 20/5, or dropping the days≥30 or price≤200 gates)
without a fresh, explicit operator instruction — see [ledger.md](ledger.md)'s run 6 learning log
for the remaining untested levers and why each one trades away something the operator already
asked for.

---

## 3. Pinterest traction rule

For Pinterest: `repin_count >= 20` **AND** `adscount >= 5` **AND** days running `>= 30`. These are
mandatory (see §2 gate history for why the repin/ad-count numbers are lower than the skill's
original 50/10).

Do NOT substitute `save_count`, Meta spend, Meta active ads, TikTok spend, ad rank, or Meta
momentum for Pinterest traction. Pinterest does not provide reliable Pinterest ad-spend fields in
the relevant endpoint. Never invent Pinterest spend. Never claim Meta spend represents Pinterest
spend.

---

## 4. Price rule

- Preferred price: **25–200 EUR/USD**.
- Under 25: flag as margin risk — do not automatically reject if economics are unusually strong.
- Over 200: automatic rejection.

Do NOT use API `minprice` / `maxprice` filters unless independently verified. Most Pinterest rows
have unreliable/null product-price fields. Filter price **client-side** using verified product
information whenever possible.

---

## 5. The ten target niches

Search ONLY these ten niches — do NOT search outside them.

| # | Niche | Codes | Keyword seeds |
|---|---|---|---|
| 1 | Hobbies | `AC,TS,PZ,MU,PH,CP,GM` | craft kit / puzzle / modellbau / loisirs créatifs |
| 2 | Men's fashion | `MC,FW,WT,EW,BG` | mens shirt / herren uhr / chemise homme / montre homme |
| 3 | Women's fashion | `WC,CG,FW,BG,JY` | womens dress / damenmode / robe femme |
| 4 | Home care | `HE,FR,SH,FK` | home organization / haushalt / rangement maison |
| 5 | Beauty | `BY,SK,HH,MG` | skincare routine / hautpflege / soin visage |
| 6 | Underwear | keyword only | underwear / lingerie / shapewear / unterwaesche / boxershorts |
| 7 | Car accessories | `AA,CC,AM` | car accessory / autozubehoer / accessoire voiture |
| 8 | Fitness | `FT` | home workout / fitnessgeraet / materiel fitness |
| 9 | Healthcare | `HT,SP` | pain relief / gesundheit / bien-etre |
| 10 | Lighting | `LS` | led strip lights / sunset lamp / lampe led / led beleuchtung |

Lighting stays separate from Home Care: Home Care = storage, cleaning, organization. Lighting = LED
strips, sunset lamps, mood lighting and related lighting products.

---

## 6. Niche distribution

Aim for approximately 10 products across multiple niches.

- Maximum 3 products per niche.
- Men's fashion: maximum 2.

The distribution rules must NEVER cause quality gates to be lowered. If a niche has no qualifying
products, report it as empty. Never pad a niche.

---

## 7. Market priority — USA first

**This rule is mandatory.** The market search order must always begin:

1. USA
2. Germany
3. Largest remaining Pinterest markets

The USA is ALWAYS the first market searched. Germany is ALWAYS the second market searched. After
USA and Germany, prioritize the remaining markets according to the largest current Pinterest
markets / greatest Pinterest commercial opportunity. Do NOT treat all countries as equally
important — the purpose is to maximize exposure to the largest Pinterest advertiser and buyer pools
first.

---

## 8. USA — maximum priority

USA must receive the deepest discovery effort. For every relevant niche, prioritize:

- US country-filtered searches
- English product keywords
- US buyer-language keywords
- US problem keywords
- US use-case keywords
- US seasonal searches
- US historical searches
- US product-derived searches
- US emerging-winner searches

Do NOT stop US discovery simply because page 1 produced several products. Continue expanding
through new keywords, synonyms, problems, solutions, use cases, buyer intent, seasonal terms,
product attributes, historical windows, pages, scrolls, and winner-derived keywords. Only after the
relevant US discovery matrix has been substantially explored should the system proceed deeper into
lower-priority markets.

---

## 9. Germany — second priority

Germany is ALWAYS second. Search using: German keywords, English keywords, German buyer-language
terminology, German product terminology, DE country-filtered searches, seasonal German searches,
historical German windows, product-derived German searches. Germany receives the second-highest
discovery effort.

---

## 10. Remaining market priority

After USA and Germany, dynamically prioritize the remaining markets by Pinterest market size /
commercial opportunity. Preferred fallback order if reliable current market-size information is
unavailable:

`US > DE > GB > FR > CA > AU > NL > IT > ES > BR > SE > DK > PL > AT`

USA and Germany MUST remain #1 and #2. The adaptive system may change the depth of searching within
a market, but must not violate the mandatory USA-first / Germany-second hierarchy.

---

## 11. Market priority is search priority — not product quality

A US product does NOT automatically beat a German product. Market order controls **where we search
first**. It does NOT control **which product ultimately wins the ranking**. After discovery, all
products are evaluated using the same quality gates. A superior Pinterest-native German product can
outrank a mediocre US product.

---

## 12. Global keyword searches

For keyword searches: DO NOT automatically pass a country filter. This is critical — keyword
searches should be allowed to discover advertisers from different markets. Use both:

- Country-focused searches: `countries=US`
- Global keyword searches: `keyword=<TERM>` without countries

This prevents country filters from hiding international advertisers targeting large markets.

---

## 13. Cross-market product expansion

If a winning product is discovered in a smaller market, immediately search the same product concept
in USA, Germany, other major Pinterest markets, and global keyword searches. Determine whether the
product has broader Pinterest demand. A winner discovered in France, for example, can reveal a US
opportunity.

---

## 14. Discovery sources — Pinterest-ONLY by standing operator instruction

**UPDATED 2026-09-11.** This section originally mandated four passes every run (Pinterest live,
Pinterest historical, TikTok Shop, Meta Ad Library). After run 2 delivered a Meta/TikTok-heavy
mix, the operator said explicitly: *"results are still not expected. I want results to be mostly
pinterest winners."* Runs 3 through 6 ran Pinterest-only with no objection — that is now the
standing behavior, not a one-run experiment:

| Pass | Source | Label | Status |
|---|---|---|---|
| 1 | Pinterest LIVE | `SOURCE: Pinterest` | **Mandatory, every run** |
| 2 | Pinterest HISTORICAL | `SOURCE: Pinterest (last-year <MONTH YYYY>)` | **Mandatory, every run** |
| 3 | TikTok Shop | `SOURCE: TikTok` | **Suspended** — do not run unless the operator explicitly re-enables it |
| 4 | Meta Ad Library | `SOURCE: Meta` | **Suspended** — do not run unless the operator explicitly re-enables it |

Do not run TikTok or Meta discovery passes on your own initiative to make up volume toward the
10/run target (§1) — that trades away a standing operator requirement without asking, which is
exactly the mistake this rule exists to prevent. If Pinterest-only discovery, even after
loosened gates (§2) and exhaustive keyword/market sweeps, cannot reach 10 fully-verified products,
report the honest count and ask before adding another source back in.

The §38 TikTok/Meta → Pinterest reverse-discovery machinery stays available for the rare case the
operator asks for a mixed-source run again, but is dormant by default. A TikTok or Meta winner is
NOT automatically a Pinterest winner — when (if) that path is re-enabled, search the product
concept back through Pinterest (§38) before treating it as Pinterest-proven.

---

## 15. Pinterest API

Endpoint: `GET https://app.winninghunter.com/api/v1/pinterest-ads`
Header: `X-API-Key: wh_...`

Verified useful parameters: `countries`, `niches`, `languages`, `adscorefilter`, `mindays`,
`maxdays`, `keyword`, `page`, `scroll`.

Never assume a parameter works. Validate important server-side filters (§16).

*(In this environment, use the connected `WinningHunter` MCP tools — see "Tooling available in this
environment" above — instead of raw HTTP where possible.)*

---

## 16. Filter validation

Some API parameters may be silently ignored. For every important filter: run the filtered request,
run the equivalent baseline request, and compare the returned IDs.

- If `filtered IDs == baseline IDs` → **SERVER FILTER INEFFECTIVE.** Do not rely on it.

Never report a filter as working unless its effect has been demonstrated.

---

## 17. API total rule

`total` may be capped at 10000. Therefore: **never report `total` as the true market size.** It is
only the API's reported result count.

---

## 18. Multi-language search

Search in this order:

| Tier | Language |
|---|---|
| 1 | EN |
| 2 | DE |
| 3 | FR |
| 4 | ES |
| 5 | NL |
| 6 | IT |

Then expand, when useful, to PT, PL, SV, DA. Do not assume English exposes all Pinterest winners —
local-language searches can expose advertisers and product terminology invisible to English
queries.

---

## 19. Keyword discovery engine

Do NOT rely only on the fixed seed keywords. For every niche, generate multiple keyword families:

- **A — Product name.** e.g. `posture corrector`
- **B — Synonyms.** posture support, back posture brace, spine corrector
- **C — Problem.** bad posture, back pain from desk, rounded shoulders
- **D — Solution.** back alignment, posture support
- **E — Use case.** office posture, desk worker back, working from home posture
- **F — Buyer language.** small apartment organization, easy home organization, gift for husband
- **G — Pinterest discovery language.** must have, gift ideas, home ideas, DIY, before after, how
  to, routine, hack, essentials, favorites
- **H — Attributes.** material, shape, mechanism, size, feature, design, function
- **I — Seasonal.** current month, next 30/60/90 days, upcoming holidays, gifting periods,
  weddings, back-to-school, Christmas, Valentine's Day, Mother's Day, Father's Day, summer, winter,
  spring, autumn

---

## 20. Fuzzy keyword rule

Pinterest keyword matching is fuzzy. **Never** assume a keyword hit is relevant. Verify every
result by reading: product title, advertiser, landing page, product page. A keyword match is a
candidate, not proof of relevance.

---

## 21. Keyword batching

Broad keyword searches can time out. Batch approximately 10–12 keywords per request when
practical. For highly noisy terms, split into smaller groups.

---

## 22. Winner-derived search loop

**Mandatory.** Whenever a strong product is discovered, extract: exact product name, synonyms,
unique nouns, unique descriptors, problem solved, use case, target customer, mechanism, material,
visual description. Generate new search queries from those attributes.

Example — winner: `cordless heated eyelash curler`. Generate: heated eyelash curler, electric
eyelash curler, heated lash tool, lash styling tool, portable lash curler, USB lash curler,
at-home lash tool, lash lift alternative. Then translate high-value terms.

Every winner must create additional discovery opportunities.

---

## 23. Store-derived search loop

If a store has a qualifying product, inspect its other products and categories. Extract potentially
independent product concepts, then search those concepts on Pinterest globally, in the USA, in
Germany, and in major markets. Do NOT assume every product from a winning store is a winner — each
must independently qualify.

---

## 24. Historical Pinterest discovery

Pinterest does not provide a reliable direct date-range filter. Use `mindays` and `maxdays` to
construct historical windows. Do NOT search only one historical month — search multiple seasonal
windows.

---

## 25. Historical window rotation

Search: same month last year · previous month last year · following month last year · 2-month
seasonal span · 3-month seasonal span · relevant holiday window · relevant buying season ·
12-month survivor window · longer historical windows where supported.

Pinterest often runs ahead of the buying moment — target seasonal products approximately **6–10
weeks before expected demand**.

---

## 26. Historical survivor interpretation

Historical Pinterest results represent ads that are still present in the current index. Call them
**LONG-TERM SURVIVORS** — strong durability evidence. But they do NOT represent every product that
won historically. Never claim a product was a historical winner merely because it appeared in a
historical search.

---

## 27. Historical dead-store buffer

Historical candidates can have dead stores. Over-source historical candidates by approximately
**1.5–2x**. Verify product pages BEFORE final ranking. A dead store must never occupy a final
winner slot.

---

## 28. Result-pool rotation

Do not assume page 1 contains everything. For promising searches, work page 1, page 2, page 3,
page 4, additional pages, and scroll values where supported. Continue until:

- IDs repeat heavily, or
- no new useful candidates appear, or
- API limits are reached, or
- the search seam is demonstrably exhausted.

Record the stopping reason.

---

## 29. Never run the same search blindly

Maintain persistent **SEARCH_HISTORY** containing: keyword, language, country, endpoint, page,
scroll, date, candidate count, new-candidate count, qualifying count. Before running a search,
check SEARCH_HISTORY. If the exact search has already been exhausted recently and produced no new
candidates, move to another search dimension.

---

## 30. Adaptive search depth

Not every search deserves equal API budget.

- **Increase depth** when a search produces many new products, a high qualification rate, unique
  product concepts, low duplication, or high Pinterest fit.
- **Reduce depth** when a search produces duplicates, irrelevant fuzzy matches, dead stores,
  low-quality products, or repeated advertisers.

The search engine should become increasingly efficient over time.

---

## 31. Anti-exhaustion engine

Maintain these persistent datasets (in [ledger.md](ledger.md)):

- `SEEN_PRODUCT_IDS`
- `SEEN_DOMAINS`
- `SEEN_PRODUCT_CONCEPTS`
- `SEEN_KEYWORDS`
- `SEARCH_HISTORY`
- `REJECTED_PRODUCTS`
- `QUALIFIED_PRODUCTS`
- `DELIVERED_PRODUCTS`
- `RECHECK_QUEUE`

Load them before every run. Update them after every run.

---

## 32. Spreadsheet = master database

The spreadsheet is the ultimate source of truth. Before discovery, **read the existing spreadsheet
data.** Extract: product names, product concepts, store domains, WinningHunter IDs, product URLs,
niches, supplier URLs. Build an exclusion index. If the spreadsheet and ledger disagree, **the
spreadsheet wins.** Never assume a product is new merely because it is absent from `ledger.md`.

This skill writes to the **same cumulative Google Sheet** the sibling `find-winning-products` skill
uses — never a new sheet. Follow that skill's Step 9 procedure (header-by-name column mapping,
`HYPERLINK` formulas, static per-row verdict fills, date-serial fix) when writing rows.

---

## 33. Never repeat a product

Reject if: same WinningHunter ID · same product URL · same product name · obvious product variant ·
same store/product combination · same underlying product concept · same core problem solved in
essentially the same way.

Different brands selling the exact same object usually = duplicate concept. Different mechanisms
genuinely solving the same problem may be separate products. Use judgment.

---

## 34. Discovery, qualification, and mandatory verification — the 3-stage pipeline

Separate discovery from qualification from verification. **UPDATED 2026-09-11 (run 4):** Stage C
was added after the operator's direct feedback on run 3 — several delivered rows had no real
Pinterest link, no real AliExpress supplier link, and no real COGS (sold-out/unverified WATCH
items had been written with `pending`/`n/a` placeholders in those fields). That is no longer
allowed. A candidate is only ever written to the spreadsheet after clearing **all three** stages:

**Stage A — Discovery.** Collect a large candidate pool — target approximately **50–200 useful
candidates**, depending on API availability. Do NOT stop at 10.

**Stage B — Qualification.** Apply: traction gates (§2/§3), days, media type, price, brand,
Shopify, live product-page existence (§40), dedupe (§33), Pinterest fit (§44).

**Stage C — Verification (mandatory before any write).**
1. **Live in-stock verification** — fetch the exact product URL and confirm it is not sold out,
   not a dead link, and price-confirmed. A "found" product that is sold out, unverifiable
   (e.g. the store blocks automated fetches), or has a stale/wrong price is **not** written to the
   spreadsheet — log it in `ledger.md`'s RECHECK_QUEUE / SEEN_DOMAINS as "found but not
   deliverable," with the specific reason, and move on.
2. **Real AliExpress supplier sourcing** — per §41/§42, a direct item URL with >= 200 orders and
   >= 4.5 stars. No qualifying supplier → not written to the spreadsheet either, same
   RECHECK_QUEUE treatment.

Only candidates that clear Stage A + B + C get a row. This means, in practice, **every delivered
row now carries a real Pinterest pin link, a real live product-page link, a real AliExpress
supplier link, and a real COGS number** — never a placeholder. See §48 for how this changes the
TEST NOW / WATCH distinction, and §50 for the exact link-column layout to write.

This 3-stage design costs volume (Stage C verification is the dominant filter on delivered count,
per run 6's learning log — not Stage B's gates) but is non-negotiable per explicit operator
instruction. Do not skip Stage C to hit the 10/run target (§1).

---

## 35. Emerging winners

Do not only monitor already-qualified winners. Create an **EMERGING WINNER WATCHLIST** tracking
products approaching 50 repins, 10 ads, 30 days. These are not confirmed winners — recheck them in
future runs.

---

## 36. Recheck queue

Previously rejected candidates are not necessarily permanently dead. Store `rejection_reason` and
`recheck_after`. Examples:

- Insufficient days → recheck later.
- Repins below 50 → recheck later.
- Ad count below 10 → recheck later.
- Price temporarily > 200 → recheck later.
- Seasonal opportunity → recheck around relevant season.
- Dead store → recheck after an appropriate interval.
- Brand/trademark risk → normally permanent rejection.

---

## 37. Market gap search

After normal discovery, identify niches with few winners, high Pinterest fit, strong visual appeal,
low saturation, and promising seasonal demand. Generate additional searches specifically for those
gaps. Do not spend the entire run searching only the niche that already produces the most results.

---

## 38. TikTok + Meta → Pinterest reverse discovery

When TikTok or Meta reveals a promising product, extract its product concept and search that
concept through Pinterest using: exact product name, synonyms, problem, use case, visual
description, buyer language, USA search, Germany search, global search, translations.

- If Pinterest evidence exists → upgrade confidence.
- If Pinterest evidence does not exist → keep it as a cross-source **WATCH** candidate.

Never falsely label it as Pinterest-proven.

---

## 39. Brand test — dropship only

Require a Shopify-compatible store where appropriate. Reject: household-name brands, major
established brands, obvious trademark products, stores with strong established-brand positioning,
products that cannot reasonably be sourced as a dropship equivalent.

Ask: *could a dropshipper realistically source an equivalent product from a supplier tomorrow?* If
no, reject. Known branded products remain a brand-risk even if their metrics are excellent.

---

## 40. Link verification — now means in-stock verification, not just "not 404"

Before writing ANY product to the spreadsheet: fetch the exact product URL. **UPDATED 2026-09-11:**
"live" is not enough — confirm the product is actually purchasable (in stock), per §34 Stage C.
Interpret:

- `200` + page shows an active "Add to cart" (no "Sold out" state) → **Live and in stock.**
  Deliverable, pending Stage C's supplier check.
- `200` + page explicitly shows "Sold out" / "Out of stock" / "Notify me when available" →
  **Sold out.** Not deliverable this run — log to RECHECK_QUEUE, do not write to the spreadsheet.
- `404` → **Dead** (the guessed/reported URL is wrong, or the product was delisted). Try the
  store's own `/search?q=` or `/collections/all` page to find the real current URL before giving
  up — store domains and product handles both migrate (seen twice: a 301 domain redirect, and a
  product simply no longer listed anywhere on the store).
- Blocked/throttled (e.g. HTTP 403 to automated fetches) → **NOT dead** — mark
  `UNVERIFIED - recheck`, do not write to the spreadsheet this run (this is a Stage C failure, not
  a pass).
- Price shown on the live page differs materially from the price WinningHunter reported → use the
  **live price**, not the API's, and re-check the price <= 200 gate against it — a stale API price
  can put a product over the cap even though it looked fine at discovery time.

Never confuse throttling with a dead page, and never confuse "page loads" with "in stock." Preserve
percent-encoded characters. Remove query strings only. Do not inject `/fr/`, `/de/`, etc. Use the
exact link returned by WinningHunter whenever possible, but fall back to site search when it 404s.

---

## 41. Supplier sourcing

For each shortlisted product: understand the exact object, identify material/form/function,
generate supplier search terms, search AliExpress, obtain top 5 candidates, compare titles,
translate titles when necessary, verify exact equivalence, require **>= 200 orders**, require
**>= 4.5 stars**, choose the cheapest qualifying equivalent.

Never silently lower the 200-order or 4.5-star requirement. If nothing qualifies: **no qualifying
supplier.**

---

## 42. Supplier link

Output exactly ONE direct supplier item URL: `https://<market>.aliexpress.com/item/<ID>.html`.
Never output a `/w/wholesale-...` link or a supplier search page.

---

## 43. Supplier confidence

Every supplier link must carry one of: `LOAD-TESTED` · `INDEX-OK` · `EQUIVALENT` · `no qualifying
supplier` · `n/a - <reason>` · `DEAD LINK (was <id>) - verified <date>` · `UNVERIFIED - recheck`.
Never provide an unlabelled supplier URL.

---

## 44. Pinterest Fit Score

Score every product 1–10.

**Add points for:** aesthetic appeal, save-worthy visual, still-image compatibility, before/after,
fashion, beauty, home, organization, craft, gifting, personalization, female 25–45 audience,
aspirational purchase, planning behavior, high perceived value, high AOV, teachable use case.

**Subtract points for:** requires video demonstration, ugly utility, strongly male skew,
medical/compliance-heavy, low-price commodity, industrial appearance, gimmick with weak aesthetic
value.

Below 4/10 cannot be `TEST NOW`.

---

## 45. Pinterest seasonality

Pinterest often operates earlier than Meta. Target products approximately **6–10 weeks before
expected demand.** A product that is only beginning to trend on Meta today may already be late for
Pinterest. Give seasonal relevance meaningful weight in ranking.

---

## 46. Test cadence

Pinterest testing is NOT identical to Meta testing. Use: lower initial daily budget, 10–14 day
evaluation, do not judge before day 7, monitor saves, monitor outbound clicks, use conversions as
the final confirmation.

---

## 47. Ranking

Final products must be ranked **best first**, using: Pinterest Fit, Pinterest traction, days
running, historical-survivor strength, margin headroom, low saturation, creative simplicity,
seasonality, supplier reliability, operational risk.

A 9/10 Pinterest-fit product beats a 5/10 product even if the latter has stronger generic Meta
signals. A durable historical survivor receives a meaningful bonus.

---

## 48. TEST NOW / WATCH / SKIP

- **TEST NOW** — meets all critical gates AND has cleared Stage C verification (§34): confirmed
  in stock, real supplier sourced. This is the only verdict that should appear on a delivered row
  under the current (2026-09-11-onward) pipeline.
- **WATCH** — interesting, qualifies at Stage B, but has NOT cleared Stage C (sold out,
  unverifiable, or no qualifying supplier). **Do not write WATCH rows to the spreadsheet anymore**
  — this was the exact operator complaint after run 3 (WATCH rows with `pending`/`n/a` supplier
  and COGS placeholders). Keep WATCH candidates in `ledger.md`'s RECHECK_QUEUE instead, and
  recheck them on a future run once stock/verification might have changed.
- **SKIP** — fails a hard gate or has unacceptable risk.

Never deliver SKIP products simply to reach 10. Never deliver WATCH products to the spreadsheet
simply to reach 10 either — that is the same mistake in a different tier. If the fully-verified
(TEST NOW) count is below 10 after exhausting discovery, report the honest count (§1, §57).

---

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
product page · WinningHunter deep-link (`app.winninghunter.com/ad/<id>?platform=pinterest`) ·
Pinterest pin link (`pinterest.com/pin/<id>`) · AliExpress supplier link — see §50 for the exact
spreadsheet column mapping
```

---

## 50. Spreadsheet schema

Use the existing spreadsheet schema — do not alter it:

`run_date, priority, test_order, product, tier, niche, store, fb_page, currency, price,
est_gross_per_order, active_ads, ads_growth_1m, ad_seen, ad_rank, ad_spend, spend_window, days_live,
saturation, pinterest_fit, verdict, main_killer, their_hook, winninghunter_link, product_page,
winning_ad, all_live_ads, supplier_link, cogs, notes`

### Link-column convention for Pinterest-sourced rows (UPDATED 2026-09-11)

The live sheet's column headers are `winninghunter_link` = "Open in WinningHunter" and
`winning_ad` = "The winning ad (Meta)" — both named for the sibling skill's Meta-sourced rows.
Runs 4-6 initially got this wrong (put the raw Pinterest pin URL under a "WinningHunter"-labeled
hyperlink in the WinningHunter column, and left the Meta-ad column as an `n/a` placeholder), which
read as if the Pinterest link were simply missing. The operator corrected this explicitly. The
correct mapping for every Pinterest-sourced row, matching the existing Meta-row convention
(`https://app.winninghunter.com/ad/<id>?platform=facebook`) already used elsewhere in this sheet:

- **`winninghunter_link` column** → `=HYPERLINK("https://app.winninghunter.com/ad/<id>?platform=pinterest","WinningHunter")`
  — a genuine WinningHunter platform deep-link, not the raw Pinterest URL.
- **`winning_ad` column** → `=HYPERLINK("https://www.pinterest.com/pin/<id>","Pinterest pin")` —
  the actual Pinterest pin link goes here, replacing the old `n/a - Pinterest pin, no Meta ad
  archive` placeholder text.
- `<id>` is WinningHunter's own `id` / `productid` field for that ad (returned by
  `search_pinterest_ads`/`get_pinterest_ad`) — for most pins this is a plain numeric Pinterest pin
  ID matching the `pin_url` field exactly, but for some it is an opaque base64-style mobile
  share-token instead; use whichever form that ad's `id` field actually is in **both** columns
  consistently, don't try to "clean it up" into a numeric form.
- **`all_live_ads` column** → `=HYPERLINK("<page_url>","Pinterest profile (all pins)")` — use the
  ad's `page_url` field (the advertiser's Pinterest business profile, e.g.
  `https://www.pinterest.com/skalecosmetics`), returned by `search_pinterest_ads` /
  `get_pinterest_ad`. This is the genuine Pinterest equivalent of "all their live ads." Only if
  `page_url` is genuinely missing/blank for that ad, fall back to a Meta Ad Library search link
  for the store (`https://www.facebook.com/ads/library/?active_status=active&ad_type=all&q=<store
  name>`) instead of leaving `n/a`. Do not leave this column as a placeholder — every Pinterest ad
  fetched so far has carried a `page_url`, so the fallback should be rare.

---

## 51. Spreadsheet write safety

Before EVERY write: read the header row, map columns by NAME (never rely on remembered column
letters), write only new products, read the written range back, verify every important field
landed in the correct column. Never assume a successful API write means the data landed correctly.

---

## 52. Verdict colors

Use static per-row fills, never copied blindly from another row:

- **TEST NOW** → dark green `#38761D`, bold white text.
- **WATCH** → amber `#FFE599`, bold black text.

---

## 53. Continuous discovery loop

When the normal search returns mostly duplicates, **do not stop.** Immediately execute, in order:

1. New synonyms
2. Problem keywords
3. Solution keywords
4. Use-case keywords
5. Buyer-language keywords
6. Seasonal keywords
7. Foreign-language variants
8. Historical windows
9. Winner-derived keywords
10. Store-derived keywords
11. Emerging-winner rechecks
12. TikTok/Meta → Pinterest reverse searches
13. Market-gap searches

Only after these discovery paths have been substantially explored may the run be considered
search-exhausted.

---

## 54. Adaptive learning

At the end of every run, calculate: best keyword families (most new qualifying products), worst
keyword families (mostly duplicates/irrelevant), best languages, best markets, best historical
windows (most durable survivors), best niches (highest yield).

Persist this information. On future runs: increase depth on high-yield paths, explore adjacent
paths, reduce wasted searches, prioritize unexplored combinations. The system must become more
effective with every run.

---

## 55. New qualifying rate

Track `new qualifying products / useful candidates` — the **NEW QUALIFYING RATE.** Prefer search
paths with a high rate. A search producing 1,000 candidates but zero new winners is inferior to a
search producing 30 candidates and 5 new winners.

---

## 56. Market coverage report

Every run must report:

- **Markets searched** — list all countries actually searched.
- **Priority** — confirm USA → Germany → largest remaining Pinterest markets.
- **Search depth** — state where the deepest search effort was spent.
- **Market yield** — candidates / new candidates / qualifying candidates by major market where
  available.

---

## 57. Final run report

After every run, provide:

**DISCOVERY** — API requests · Pinterest live candidates · Pinterest historical candidates ·
TikTok candidates · Meta candidates · total useful candidates · new candidates · duplicate
candidates.

**QUALIFICATION** — passed Stage B · failed repin gate · failed ad-count gate · failed days gate ·
failed media gate · failed price gate · failed brand test · failed product-page verification ·
failed dedupe. Then **Stage C** — passed (both live-stock AND supplier) · failed live-stock check
(sold out / dead / unverifiable) · failed supplier sourcing (no qualifying AliExpress match).
Report Stage C attrition explicitly and separately from Stage B — per run 6, Stage C verification
is now the dominant filter on final delivered count, not the traction gates.

**DELIVERY** — total delivered (all TEST NOW under the current pipeline — see §48) · candidates
that reached Stage B but not Stage C, logged to RECHECK_QUEUE instead of delivered · SKIP.

**SOURCE MIX** — Pinterest live: N · Pinterest historical: N. (TikTok and Meta passes are
suspended per §14 — omit them from the mix unless the operator has explicitly re-enabled them for
this run, in which case report those counts too.)

**NICHE MIX** — list all ten niches, explicitly identify empty niches.

**MARKET MIX** — list products by market; confirm search began with USA, then Germany, then
largest remaining Pinterest markets.

**SEARCH COVERAGE** — countries · languages · keyword families · historical windows · pages ·
scrolls · winner-derived searches · store-derived searches.

**NOVELTY** — new products · new product concepts · new stores · duplicates · exhausted searches.

**LEARNING** — best keyword family · best language · best market · best niche · best historical
window.

**#1 PICK** — explain why #1 is the best first test; give its recommended initial Pinterest
testing budget and 10–14 day testing cadence.

**BINDING CONSTRAINT** — explain exactly what prevented finding additional qualifying products.

---

## 58. Honesty rules

Never fabricate: metrics, spend, prices, dates, supplier orders, ratings, links, product
information. If a field is unavailable: `n/a` followed by the reason.

Never claim an API filter worked without testing it. Never claim a product is a Pinterest winner
without Pinterest evidence. Never call a blocked page dead. Never invent a supplier. Never deliver
a duplicate. Never lower a hard gate simply to reach 10.

---

## 59. The most important anti-exhaustion rule

**Never say:** "There are no more Pinterest winners."

**Instead, the strongest valid conclusion is:** "No additional qualifying products were discovered
after exhausting the currently available search matrix."

Pinterest's index changes. Advertisers change. Keywords change. Markets change. Seasons change.
Products mature. Emerging winners become confirmed winners. Therefore the system must continuously
revisit: USA, Germany, largest Pinterest markets, new keywords, new languages, new product
terminology, historical windows, seasonal windows, emerging winners, previously rejected
candidates, TikTok/Meta discoveries, winner-derived searches, store-derived searches.

---

## 60. Final operating principle

This is NOT a one-time scraper. It is a **CONTINUOUS PINTEREST WINNER DISCOVERY ENGINE.**

Every winner creates new search vocabulary. Every rejected candidate creates learning. Every
exhausted query triggers another discovery dimension. Every historical survivor reveals seasonal
information. Every external winner becomes a Pinterest search opportunity. Every run updates the
search strategy. Every future run should therefore have access to **more** discovery paths than the
previous run, never fewer.

The objective is NOT "find 10 Pinterest products." The objective is:

> Continuously discover the maximum number of NEW, evidence-backed, Pinterest-testable product
> concepts, prioritizing USA first, Germany second, and then the largest Pinterest markets, without
> ever repeating the existing database.

---

## Ledger template (create if missing)

See [ledger.md](ledger.md) for the current ledger. Its structure mirrors §31's persistent datasets —
one section per dataset, updated at the end of every run.

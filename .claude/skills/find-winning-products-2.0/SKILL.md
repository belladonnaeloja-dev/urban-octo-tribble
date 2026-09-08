---
name: find-winning-products-2.0
description: >-
  Continuous Pinterest winning-product discovery engine (v4) with USA-first, Germany-second
  market priority, PLUS a bundled ad-variations extension that scales a confirmed winner into
  ~50 Pinterest ad creatives. The discovery half is NOT a "find 10 and stop" tool — it is an
  exhaustive, self-expanding search across four mandatory sources every run (Pinterest LIVE,
  Pinterest HISTORICAL, TikTok, Meta), covering exactly ten fixed niches (hobbies, men's
  fashion, women's fashion, home care, beauty, underwear, car accessories, fitness,
  healthcare, lighting), gated on hard Pinterest traction rules (repins >= 50, ad count >= 10,
  days running >= 30, video only, price <= 200, dropship-compatible, live product page,
  non-established brand, never a repeat). Market search order is always USA first, Germany
  second, then the largest remaining Pinterest markets — though ranking afterwards is by
  quality (Pinterest Fit score, traction, seasonality), not by which market a product came
  from. Runs a multi-language keyword-family engine (EN/DE/FR/ES/NL/IT+), historical-window
  rotation, winner-derived and store-derived search loops, and an anti-exhaustion engine that
  persists SEEN_PRODUCT_IDS/SEARCH_HISTORY/RECHECK_QUEUE so no run repeats a prior search or
  product. Verifies every product page and every AliExpress supplier link before writing to
  the spreadsheet (master source of truth), and produces a full discovery/qualification/
  delivery/market-coverage run report. Once the discovery engine (or the user) has a
  confirmed winning creative, this skill ALSO drives the five-stage ad-variations workflow —
  source pool + deconstruct + generate (cv2 recolors/PIL hooks/stitching/Higgsfield
  Marketing Studio) + audio remux + Pinterest bulk-upload sheet — to turn that one winner
  into a ~45-creative "Mixed P+" Pinterest campaign. Use this skill when the user asks to
  find winning products (2.0 / v4 / exhaustive / continuous mode), run the Pinterest
  discovery engine, do continuous product research prioritizing USA and Germany, or wants to
  scale a winning ad into dozens of variations / build a Pinterest creative-test campaign.
  This is a separate skill from the existing `find-winning-products` skill — use that one
  only if the user explicitly asks for the original/legacy version.
metadata:
  type: skill
---

# Find Winning Products 2.0 (Pinterest Exhaustive Discovery Engine)

This skill has two parts that chain together:

1. **Discovery** — a continuous, self-expanding Pinterest winner-discovery engine. Full rule
   set: [references/discovery-engine.md](references/discovery-engine.md). **Read it before
   every run** — it is the actual spec (60 sections) and this file only summarizes the parts
   you need to start correctly and stay oriented.
2. **Ad-Variations** — once a winner is confirmed (found by this engine, or handed to you
   directly by the user), scale it into ~45 Pinterest ad creatives + a bulk-upload campaign
   sheet. Full workflow: [references/ad-variations.md](references/ad-variations.md).

Trigger Ad-Variations when the user wants to scale a winning ad, "make ~50 creatives," build
ad variations, or produce a Pinterest creative-test campaign — whether or not that winner
came from a discovery run in this session.

## Non-negotiable framing (read this even if you skip everything else)

- The goal is **NEW QUALIFYING PRODUCTS FOUND**, not "return 10 rows." Ship 10 if 10 qualify;
  ship fewer and say why if fewer qualify. Never lower a gate to hit the count. See
  [discovery-engine.md §1](references/discovery-engine.md#1-core-success-metric).
- **NEVER conclude "there are no more Pinterest winners."** The correct sentence when a run
  comes up dry is "no additional qualifying products were discovered after exhausting the
  currently available search matrix" — see
  [§59](references/discovery-engine.md#59-the-most-important-anti-exhaustion-rule). A search
  seam going dry (one keyword, one page, one country) is never proof the market is exhausted;
  work the continuous-discovery-loop expansions in
  [§53](references/discovery-engine.md#53-continuous-discovery-loop) before calling a run done.
- **Market order is USA, then Germany, then the largest remaining Pinterest markets — always,
  every run.** This governs *where you search first*, not which product wins the final
  ranking (a strong German product can outrank a mediocre US one). See
  [§7–§11](references/discovery-engine.md#7-market-priority--usa-first-mandatory).
- **Four sources, every run, none optional:** Pinterest LIVE → Pinterest HISTORICAL
  (`mindays`/`maxdays` windows, not a real date filter) → TikTok → Meta. Label every product
  with its `SOURCE:`. TikTok/Meta winners are not Pinterest winners until searched back
  through Pinterest. See [§14](references/discovery-engine.md#14-four-mandatory-discovery-sources)
  and [§38](references/discovery-engine.md#38-tiktok--meta--pinterest-reverse-discovery).
- **Exactly ten niches, nothing else:** hobbies, men's fashion (max 2), women's fashion, home
  care, beauty, underwear, car accessories, fitness, healthcare, lighting. Max 3/niche. Empty
  niches get reported empty, never padded. See
  [§5–§6](references/discovery-engine.md#5-the-ten-target-niches).
- **Pinterest traction gate is fixed and cannot be substituted:** `repin_count >= 50` AND
  `adscount >= 10` AND days running >= 30 (recomputed from `started`, not trusted from
  `mindays`). Never substitute Meta spend, TikTok spend, or ad rank for Pinterest traction.
  See [§2–§3](references/discovery-engine.md#2-product-definition--what-counts-as-a-winner).
- Price band 25–200 (flag <25 as margin risk, don't auto-drop; auto-reject >200). Video only.
  Dropship-compatible, non-established brand. See
  [§4](references/discovery-engine.md#4-price-rule) and
  [§39](references/discovery-engine.md#39-brand-test--dropship-only).
- **Verify before writing:** fetch every product URL (404 = dead, throttled ≠ dead — mark
  `UNVERIFIED - recheck`), and every AliExpress supplier link must be a single direct
  `/item/<ID>.html` URL meeting ≥200 orders / ≥4.5 stars, never a search page. See
  [§40–§43](references/discovery-engine.md#40-link-verification).
- **The spreadsheet is the master database, not the ledger.** Read it before discovery; if it
  disagrees with the ledger, the spreadsheet wins. Schema in
  [§50](references/discovery-engine.md#50-spreadsheet-schema) is fixed — do not alter it.
  Write safety rules (map columns by name, read back after writing) are in
  [§51](references/discovery-engine.md#51-spreadsheet-write-safety).
- **Never fabricate** a metric, spend figure, price, date, supplier order count, rating, or
  link. Missing data is `n/a` plus the reason. See
  [§58](references/discovery-engine.md#58-honesty-rules).

## Run sequence

1. **Load state.** Read [ledger.md](ledger.md) (delivered products, seen IDs/domains/
   concepts, rejected + recheck queue) and [search-history.md](search-history.md) (every
   search already run, and the adaptive-learning notes from prior runs). Read the live
   spreadsheet if one is configured — it is the source of truth over the ledger (§32).
2. **Discover** (Stage A, §34): sweep Pinterest LIVE → Pinterest HISTORICAL → TikTok → Meta,
   USA first, Germany second, then the remaining market ladder, across the multi-language
   keyword-family engine (§18–§19), targeting a broad candidate pool (50–200 useful
   candidates) rather than stopping at 10.
3. **Qualify** (Stage B, §34): apply the hard gates (§2–§4, §39–§40), dedupe against the
   ledger/spreadsheet (§32–§33), verify product pages (§40) and suppliers (§41–§43), and score
   Pinterest Fit (§44).
4. **Exhaust before concluding.** If short of 10 qualifying products, run the continuous
   discovery loop's 13 expansions (§53) — synonyms, problem/solution/use-case/buyer-language
   keywords, seasonal terms, foreign-language variants, historical windows, winner-derived
   and store-derived searches, emerging-winner rechecks, TikTok/Meta reverse searches, and
   market-gap searches — before reporting the run exhausted.
5. **Rank** (§47) and assign verdicts (§48): TEST NOW / WATCH / SKIP, best first.
6. **Write** only genuinely new products to the spreadsheet, using the fixed schema (§50) and
   write-safety procedure (§51), with verdict colors per §52.
7. **Update state.** Append everything delivered, rejected, and searched this run into
   [ledger.md](ledger.md) and [search-history.md](search-history.md), including the
   adaptive-learning summary (§54) so the next run explores unexplored ground rather than
   repeating this one.
8. **Report** using the exact structure in §57 (Discovery / Qualification / Delivery / Source
   Mix / Niche Mix / Market Mix / Search Coverage / Novelty / Learning / #1 Pick / Binding
   Constraint) plus the market-coverage confirmation in §56.
9. **If the user wants a winner scaled into a creative-test campaign**, hand off to
   [references/ad-variations.md](references/ad-variations.md) — starting with its hard-stop
   winner-confirmation step. Do not infer the winner from the discovery run's own #1 pick
   without the user explicitly confirming it as the creative to scale.

## Per-product output format

Use the exact block format from
[discovery-engine.md §49](references/discovery-engine.md#49-final-product-output) for every
delivered product.

## State files in this skill folder

- [ledger.md](ledger.md) — `SEEN_PRODUCT_IDS` / `SEEN_DOMAINS` / `SEEN_PRODUCT_CONCEPTS` /
  `DELIVERED_PRODUCTS` / `REJECTED_PRODUCTS` / `RECHECK_QUEUE` / `EMERGING WINNER WATCHLIST`
  (§29, §31, §35–§36). Never repeat anything recorded here or in the live spreadsheet.
- [search-history.md](search-history.md) — `SEARCH_HISTORY` (§29) plus the adaptive-learning
  log (§54): best/worst keyword families, best languages, best markets, best historical
  windows, best niches, per run.
- [master-history.tsv](master-history.tsv) — local mirror of every row ever written to the
  spreadsheet, one line per product, columns matching §50 exactly. Append here whenever you
  append to the live spreadsheet, so the run has a durable local record even if the
  spreadsheet connector is unavailable on a future run (say so explicitly if it is).

## Known gaps to resolve before a first real run

- No WinningHunter API key / MCP connection, TikTok, Meta, or spreadsheet connector is wired
  into this skill folder yet — confirm live access to all four before promising a real run
  (do not fabricate results if a source is unreachable; say so and report it as a binding
  constraint per §57/§58).
- No live spreadsheet URL is recorded here yet. Ask the user for the canonical spreadsheet
  (or confirm one already exists) before Step 1 of the first run, and record it in this file
  once confirmed so future runs don't have to ask again.
- Ad-Variations needs Shopify MCP, Higgsfield MCP, and Vmake API (credentials via macOS
  Keychain, see [ad-variations.md](references/ad-variations.md)) connected before Stage 0.

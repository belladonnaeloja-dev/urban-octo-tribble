# Winning Product Ledger — find-winning-products-2.0

Persistent anti-exhaustion state (SKILL.md §31). Load every section before a run; update every
section after a run. The spreadsheet is still the master source of truth for dedupe (§32) — this
ledger is what lets the search strategy itself improve run over run, and what backstops the
spreadsheet if it is briefly unreachable.

## SEEN_PRODUCT_IDS
WinningHunter IDs already evaluated (qualified or rejected), so a run never re-fetches or
re-scores the same row.

- (none yet)

## SEEN_DOMAINS
Store domains already evaluated, one line each, with the niche and the outcome (qualified /
rejected / recheck).

- (none yet)

## SEEN_PRODUCT_CONCEPTS
Underlying product concepts already delivered or rejected as duplicates — not store-specific, so a
different brand selling the same object is caught here even under a new domain.

- (none yet)

## SEEN_KEYWORDS
Keywords already searched, with language, country (or "global"), and outcome, so §29's "before
running a search, check SEARCH_HISTORY" rule has something to check against.

- (none yet)

## SEARCH_HISTORY
One line per search actually run: `date | endpoint | keyword | language | country | page/scroll |
candidates | new_candidates | qualifying`.

- (none yet)

## REJECTED_PRODUCTS
`product | reason | rejected_date | recheck_after (or "permanent")` — per §36. Brand/trademark risk
is normally permanent; everything else gets a recheck date.

- (none yet)

## QUALIFIED_PRODUCTS
Products that cleared every gate in a given run, whether or not they were ultimately delivered
(niche cap, dedupe against a stronger duplicate, etc.) — kept so a near-miss isn't re-discovered
and re-scored from scratch next run.

- (none yet)

## DELIVERED_PRODUCTS
Products actually written to the spreadsheet, one dated block per run — mirrors the sibling skill's
ledger format so the two stay easy to cross-check:

```markdown
## 2026-MM-DD
- Product Name — domain.com — winninghunter_id — Niche — Market — SOURCE — Verdict
```

- (none yet)

## RECHECK_QUEUE
Emerging winners (§35) and recheckable rejects (§36) due for another look, with the date they
become worth rechecking.

- (none yet)

## LEARNING LOG (§54)
End-of-run notes on which keyword families, languages, markets, historical windows, and niches
produced the highest new-qualifying rate (§55) — read this before planning the next run's depth
allocation.

- (none yet)

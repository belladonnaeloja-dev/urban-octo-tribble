# Find Winning Products 2.0 — Ledger

Persistent anti-repeat state for the `find-winning-products-2.0` skill (see
[discovery-engine.md §29, §31–§36](references/discovery-engine.md)). Read this file in full
before every run. Update it at the end of every run — this step is not optional; skipping it
means tomorrow's run repeats today's products.

**The live spreadsheet is the master database (§32).** If it disagrees with this ledger, the
spreadsheet wins. This file is the local backstop for when the spreadsheet is unavailable or
to speed up dedupe without re-reading the whole sheet every time.

## SEEN_PRODUCT_IDS

WinningHunter IDs already delivered or rejected. One per line: `<id> — <product name> — <date first seen>`.

(none yet)

## SEEN_DOMAINS

Store domains already evaluated (delivered or rejected — rejected domains still count, a
domain isn't automatically safe to re-mine next run without a reason). One per line:
`<domain> — <status: delivered|rejected|watch> — <date>`.

(none yet)

## SEEN_PRODUCT_CONCEPTS

Underlying product concepts already covered, independent of brand/domain (§33 — "same core
problem solved the same way" is a duplicate even across different stores). One per line:
`<concept name> — <example product> — <date>`.

(none yet)

## DELIVERED_PRODUCTS

Every product actually written to the spreadsheet, newest run first.

<!-- ## 2026-09-08 (run 1)
- Product Name — domain.com — WH-id — Niche — Market — SOURCE: Pinterest — verdict
-->

(none yet — this is the first run)

## REJECTED_PRODUCTS

Products that failed a gate. Kept so they aren't silently re-discovered without a reason,
and so `recheck_after` can be honored.

| Product | Domain | Rejection reason | Rejected on | Recheck after |
|---|---|---|---|---|

(none yet)

## RECHECK_QUEUE

Rejected-but-not-permanently-dead candidates (§36): insufficient days, repins below 50, ad
count below 10, price temporarily >200, seasonal opportunity, dead store. Brand/trademark
risk is normally a permanent rejection and does not belong here.

| Product | Domain | Reason held back | Recheck after / season |
|---|---|---|---|

(none yet)

## EMERGING WINNER WATCHLIST

Products approaching but not yet meeting the traction gates (§35): closing in on 50 repins,
10 ads, or 30 days running.

| Product | Domain | Repins | Ad count | Days running | First noticed |
|---|---|---|---|---|---|

(none yet)

## Archive

Entries older than 120 days move here (names + domains only) so the file stays cheap to read
while still blocking repeats.

(none yet)

# Resolving multiple Shopify listings for one title

When you batch-search Shopify for a bestseller's title (see
`build_batch_queries.py`), each aliased field can return more than one
product. This happens because the same promo title sometimes exists as
several live listings — most commonly price-test duplicates or old copies.

Before writing `shopify_prices.json` for `match_and_build_sheet.py`, resolve
each title down to a price list:

1. Filter out obvious test/duplicate listings by title, case-insensitive:
   anything containing "TEST", "PRICE TEST", "PRICETEST", "(kopie)", "Kopie
   van", "(Copy)", or similar. These are internal experiments, not the
   listing customers actually buy from.
2. If exactly one candidate remains, use its minVariantPrice.amount
   as the single price for that title.
3. If more than one non-test candidate remains (genuinely ambiguous —
   e.g. two real listings under the same title), keep all of their prices
   in the list for that title. match_and_build_sheet.py will use the
   highest one and add a note flagging it, so it's visible in the output
   rather than silently picked.
4. If zero candidates remain (only test listings matched), treat the
   title as unmatched rather than using a test price — a discarded
   price-test is not what's actually charged.

This matters because the whole point of the sheet is to catch products
whose supplier cost eats too much of the selling price; a stale test price
(often lower than the real one, to see if demand holds) would understate
the ratio and hide a real problem.

# Matching xlsx rows to Shopify products

parse_quotation_xlsx.py gives you two lookup dicts:

- by_title: exact title match. Try this first — most rows match exactly,
  since analytics product_title and the xlsx Product name are usually
  pulled from the same underlying product.
- by_brand_key: fallback for when the promo prefix or trailing description
  text has drifted between when the quote was recorded and now (campaigns
  get relaunched in different languages, descriptions get rewritten, etc).
  brand_key() strips all of that down to the distinctive brand name after
  the last "|" and before the (TM) mark, which is stable across those changes.

If a title matches multiple xlsx rows (a product was re-quoted over time),
latest_row() picks the one with the most recent Quotation approval
date — that's the quote that's actually in effect now, not a stale one
from an earlier negotiation round.

Do not try to match on Product shopify ID in the xlsx — in practice this
ID does not correspond to any live Shopify product or variant ID (it looks
like it's sourced from the quotation platform's own internal reference,
not synced live to Shopify). Title matching is the reliable path.

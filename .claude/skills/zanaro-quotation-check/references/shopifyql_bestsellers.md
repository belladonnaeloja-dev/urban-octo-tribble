# Pulling best sellers by revenue

Use the Shopify MCP's `run-analytics-query` tool (ShopifyQL) to get the
ranked list of best sellers by revenue for the lookback window:

```
FROM sales SHOW total_sales, orders GROUP BY product_title ORDER BY total_sales DESC SINCE -90d UNTIL today LIMIT 100
```

- Swap `-90d` for the requested lookback window (`-30d`, `-180d`, etc.).
- `LIMIT` is the number of best sellers to check (default 100 — the ceiling
  the MCP tool accepts per call is high enough for this in one shot).
- `total_sales` is the revenue figure to rank by (gross - discounts -
  returns + shipping + tax — Shopify's "total sales"). `gross_sales` and
  `net_sales` are also available in the same query if the user specifically
  wants a different revenue definition; ask if they push back on which one
  is "the" revenue number, but default to `total_sales` without asking.
- The result's `product_title` column is the exact, current Shopify title —
  use it verbatim as the join key for the xlsx match and the Shopify price
  lookup (don't re-derive or reformat it).

Build the `titles.json` / `bestsellers.json` inputs the other scripts expect
directly from this query's rows:

- `titles.json`: `[row.product_title, ...]` — feed to `build_batch_queries.py`.
- `bestsellers.json`: `[[row.product_title, row.total_sales, row.orders], ...]` — feed to `match_and_build_sheet.py`.

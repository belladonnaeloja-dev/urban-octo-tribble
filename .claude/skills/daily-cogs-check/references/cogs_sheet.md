# The "Daily COGS" sheet

Spreadsheet: **not created yet.** On the first run, create it with the
Google Drive MCP `create_file` (`contentMimeType: "text/csv"`, the header
row below plus the run's rows as `textContent`, title "Daily COGS"), which
Drive converts to a Google Sheet. Then write its URL and ID here, commit
the change, and use it on every later run.

<!-- After the first run, replace the line above with:
Spreadsheet: "Daily COGS" (https://docs.google.com/spreadsheets/d/<ID>), tab "Log".
-->

## Tab layout

Header in row 1, one row per store per day, newest day at the bottom.

| Col | Header | Value |
|---|---|---|
| A | Date | order day, `YYYY-MM-DD` |
| B | Store | store name, or `ALL` for the all-stores row |
| C | Orders | non-canceled orders |
| D | Orders with COGS | orders with cost > 0 |
| E | Orders without COGS | C − D |
| F | COGS - Actual (USD) | sum of Zendrop costs |
| G | Avg COGS per Order (USD) | F ÷ D |
| H | COGS - Estimated Missing (USD) | sum of estimates, blank if not done |
| I | COGS - Total incl. Estimates (USD) | F + H |
| J | Canceled | canceled orders (excluded) |
| K | Notes | warnings, unpriced products, "Shopify revenue skipped" etc. |

`total_cogs.py --tsv` writes exactly these columns, without the header.

## Writing

1. Read `Log!A1:K2000` with `get_values` and find rows with the same
   Date + Store.
2. Existing rows: overwrite them with `update_values` at their row range.
3. New rows: `append_values` to `Log!A:K`.
4. Write money and counts as numbers, not text.
5. Read the written range back to verify before replying.

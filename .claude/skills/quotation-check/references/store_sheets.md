# Where each store's results go

Every mapped store lives in one spreadsheet, one tab per store:
"Zanaro Top Bestsellers by Quotation %"
(https://docs.google.com/spreadsheets/d/10oUKhWCvLNk-Y_HYNcdUayekezJXnPPXx88TPoTM_K8).

| Store (xlsx "Store name" / myshopify subdomain) | Storefront | Tab | sheetId (gid) |
|---|---|---|---|
| `bycheri` | Zanaro Berlin | DE | 171846471 |
| `solundi-com` | Solundi.com | NL | 754982655 |

The sheetIds were checked against the live spreadsheet on 2026-09-28. If
a Sheets call reports "No grid with id", look up the real IDs with
Google Sheets `get_spreadsheet` (fields `sheets.properties.sheetId`,
`sheets.properties.title`) and fix this table.

A store not listed here gets a new sheet (SKILL.md step 7), unless the
user names a tab for it — then add a row here.

## Tab layout

The header is row 1 and data starts at row 2 (A2). There are 13 columns:

Quotation Rank | Bestseller Rank (90d revenue) | Product | SKU | Supplier |
Selling Price (EUR) | Quotation - Lowest (EUR) | Quotation - Highest (EUR) |
Quotation % (Lowest / Selling Price) | Revenue - Last 90 Days (EUR) |
Orders - Last 90 Days | Supplier | Note

The second "Supplier" column (Zendrop / Service Points) and "Note" are
maintained by the user by hand. Never overwrite them for a product already
in the tab.

## Update rules (every run)

1. Read the tab first (Google Sheets `get_values`, range `<Tab>!A1:M200`).
2. For each product already in the tab, match it by brand name (the word
   before ™). If it is in this run's results, refresh columns A–K with the
   new figures and keep L and M as they are. If it has no current quote or is
   no longer in the top 100, keep its old quote figures. If it is still a best
   seller, refresh its bestseller rank, selling price, revenue and orders and
   recompute Quotation %. If it dropped out of the top 100, set its bestseller
   rank to `>100`. Mention these rows in the reply.
3. Add the **30 highest-quotation-% products not already in the tab**, with
   Note = `NEW <YYYY-MM-DD>` and Supplier (col L) left blank. On an empty
   tab, fill it with the default top 20 instead.
4. Check that no product appears twice, then re-sort everything by Quotation %
   descending and renumber Quotation Rank.
5. Format Quotation % with 2 decimals (e.g. `60.53%`).

## Writing to the tab

Use the Google Sheets MCP tools (load them with ToolSearch):

1. Column I holds a fraction with a `0.00%` number format, so write
   Quotation % as a number (e.g. `0.6053`), not as the text `60.53%`.
   Write prices, revenue, orders and ranks as numbers; `>100` stays text.
2. If the table grows, first call `insert_dimension` on the tab's sheetId
   (ROWS, `startIndex` = current last data row, 0-based = number of rows
   including the header, `endIndex` = start + added rows,
   `inheritFromBefore: true`) so the new rows pick up the table's
   formatting and anything below moves down.
3. Write all rows at once with `update_values`, range `<Tab>!A2:M<n+1>`.
4. Read the range back with `get_values` to verify before replying.

If the Sheets tools aren't available in the session, fall back to writing
the rows (no header, 13 tab-separated columns) to a `.tsv` file in the
scratchpad, sending it with SendUserFile, and telling the user to paste it
at A2 (inserting rows first if the table grows).

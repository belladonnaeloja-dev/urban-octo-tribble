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
2. Re-check **every** product already in the tab, not only the ones in this
   run's top 100. Match each one by brand name (the word before ™); where the
   title has no ™ in its last `|` segment, match on the exact title first so
   the description text isn't used as the key. Keep columns L and M as they
   are.
   - **Quote:** look the product up in this run's uploaded xlsx and use its
     latest row that has a price (`latest_row()` in
     `parse_quotation_xlsx.py`), even if that row's status is a pending
     requote or bid rather than an approved quote; say so in the reply when
     a pending bid changed a product's quote. If the xlsx has no priced row for
     it, keep the old quote figures and list it under "No quotation" in the
     reply with its xlsx status (e.g. `Stop fullfilment`,
     `Requote - Bidding`, or "not in file").
   - **Selling price:** look up the current Shopify price for every product
     in the tab, including ones outside the top 100, with the same batched
     queries as step 4 of SKILL.md (exact title, minVariantPrice, skip
     TEST/PRICE TEST/(Copy)/(kopie) and DRAFT listings, highest price if
     several live listings share the title). List every price that changed
     in the reply.
   - **Rank, revenue, orders:** refresh from this run's best-seller query.
     If it dropped out of the top 100, set its bestseller rank to `>100` and
     keep its old revenue and orders.
   - Recompute Quotation % from the refreshed quote and price.
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

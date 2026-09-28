# Where each store's results go

Every mapped store lives in one spreadsheet, one tab per store:
"Zanaro Top Bestsellers by Quotation %"
(https://docs.google.com/spreadsheets/d/10oUKhWCvLNk-Y_HYNcdUayekezJXnPPXx88TPoTM_K8).

| Store (xlsx "Store name" / myshopify subdomain) | Storefront | Tab | gid |
|---|---|---|---|
| `bycheri` | Zanaro Berlin | DE | 820189638 |
| `solundi-com` | Solundi.com | NL | 754982655 |

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

1. Read the tab first (Drive `read_file_content` on the spreadsheet).
2. For each product already in the tab, match it by brand name (the word
   before ™). If it is in this run's results, refresh columns A–K with the
   new figures and keep L and M as they are. If it has no current quote or is
   no longer in the top 100, keep its old quote figures. If it is still a best
   seller, refresh its bestseller rank, selling price, revenue and orders and
   recompute Quotation %. If it dropped out of the top 100, set its bestseller
   rank to `>100`. Mention these rows in the reply.
3. Add the **10 highest-quotation-% products not already in the tab**, with
   Note = `NEW <YYYY-MM-DD>` and Supplier (col L) left blank. On an empty
   tab, fill it with the default top 20 instead.
4. Check that no product appears twice, then re-sort everything by Quotation %
   descending and renumber Quotation Rank.
5. Format Quotation % with 2 decimals (e.g. `60.53%`).

## Writing to the tab

The Google Drive connector can read the sheet but cannot edit cells, and
there is currently no working Sheets-write tool. Write the final rows
(no header, 13 tab-separated columns) to a `.tsv` file in the scratchpad,
send it to the user with SendUserFile, and tell them to paste it at A2
(inserting rows first if the table grows, so any block below moves down).
If a Sheets-write tool becomes available, write the rows directly
instead and read the tab back to verify.

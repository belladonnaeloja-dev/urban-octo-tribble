---
name: zendrop-quote-check
description: 'Cross-check every order in a Zendrop orders CSV (Order Number, Total (USD), Country) for the Zanaro Berlin store against the quoted prices in the "Zendrop_quote_request" Google Sheet — the order total must equal the quoted USD price (column Q for DE, the matching country column for AT/CH/NL/BE/FR) times the quantity of each product. Line items come from Shopify. Every order that does not match is written to one persistent Google Sheet, "Zendrop Quotation Mismatches", with order #, product name, quoted price, CSV total and the difference. Use when the user asks to check/verify/cross-check Zendrop quotations, orders or order totals, run the weekly quotation check, or shares a Zendrop orders CSV plus the quote sheet.'
---

# Zendrop quotation check (orders CSV × Zendrop_quote_request)

Checks that Zendrop charged what it quoted. For each order in the CSV, the expected total is the
sum of `quoted USD price × quantity` for every product in the order, using the quote column for the
order's destination country. Orders that don't match go into the mismatch Google Sheet.

The check itself never changes the quote sheet, Shopify or the CSV. It only writes to the
mismatch sheet.

## Inputs (ask for whichever is missing)

1. **Orders CSV** (usually `zanaro_berlin_linked_product_orders_last_7_days.csv`, exported by
   the Zendrop bot). It needs `Order Number`, `Total (USD)` and `Country`. If it also has
   `Product`, `Variant` and `Quantity` columns, you can skip Step 2.
2. **Quote sheet**: default is `Zendrop_quote_request.xlsx`, Drive file ID
   `1SvNOGcVRPUv2DruK6yNZBneZm3WoLvxY`. If the user gives a different link, take the ID from the
   URL (`/d/<ID>/`).

Only use the files the user gives you for this run. Don't pick up other order exports or
example sheets from Drive on your own.

## Fixed IDs

- **Mismatch sheet and folder:** see `state.json` (`mismatch_sheet_id`, `folder_id`).
- **Shopify store:** the Zanaro Berlin store, whose orders are named `#BC…`. Verify it with
  `get-shop-info`, then `get-order` on the first order number in the CSV, before looking up
  the rest. If a different store is connected, don't switch on your own: tell the
  user. Switching logs the current store out, and they have to approve the new one in their
  claude.ai connector settings.

## Step 1: Read the quote sheet

Call Google Drive `read_file_content` with the quote sheet ID. Save the returned `fileContent`
string exactly as returned to `<scratchpad>/quotes.txt`, then check how it parsed:

```
python3 .claude/skills/zendrop-quote-check/scripts/check_quotes.py --quotes <scratchpad>/quotes.txt --dump-quotes
```

The first output line must be `USD quote columns: DE=Q, AT=S, CH=U, NL=W, BE=Y, FR=AA`.
**Column Q is the DE price in USD.** The script finds these columns from the header rows
("Zendrop Quotes" → country code → "USD ($)"). If DE isn't Q, or the script exits with a
layout error, the sheet has been restructured. Stop and tell the user rather than guessing.

How the sheet is laid out (the script handles this):
- Each product's first row has its name in column A. Rows below it with an empty column A are
  **variants** of that product, labelled in column D (details) or L (quality/inclusions),
  e.g. `1pc`/`2pc`, `4-Zahn`, `Kabellos`.
- Prices are written loosely (`$11.46`, `$$8.48`, `€24,40`). Blank means no quote.
- Products are matched by brand name, which is the word before `™`
  (`50% RABATT NUR HEUTE | SteamPress™ - …` → `SteamPress`). Rows for the Zanaro store are
  preferred (the store column sometimes says `Zabaro`).

## Step 2: Get each order's line items from Shopify

The CSV has no product names, so look them up. Use `graphql_query`, following the Shopify
GraphQL workflow (check the schema with `graphql_schema`, then run `validate_graphql_codeblocks`,
then execute). Fetch up to 50 orders per call:

```graphql
query ($q: String!) {
  orders(first: 50, query: $q) {
    nodes { name lineItems(first: 50) { nodes { title variantTitle quantity } } }
    pageInfo { hasNextPage endCursor }
  }
}
```

with `q` = `name:BC126162 OR name:BC126160 OR …` (order numbers without the `#`). Page through
until every order in the CSV is covered. For a single order that's missing, `get-order` with the
name as-is (`#BC126162`) also works. Write the results to `<scratchpad>/items.json`:

```json
{"#BC126162": [{"title": "50% RABATT NUR HEUTE | SteamPress™ - …", "variant": "50% RABATT", "qty": 1}]}
```

Drop line items that Zendrop doesn't fulfil (shipping protection, tips, digital add-ons). Keep
every physical product.

## Step 3: Run the check

```
python3 .claude/skills/zendrop-quote-check/scripts/check_quotes.py \
  --quotes <scratchpad>/quotes.txt --orders <path to CSV> --items <scratchpad>/items.json \
  --out <scratchpad>/mismatches.csv --checked-on <today YYYY-MM-DD>
```

Rules the script applies:
- **Expected total** = Σ (quoted USD price for the destination country × quantity).
  DE → Q, AT → S, CH → U, NL → W, BE → Y, FR → AA.
- **Match** if `|CSV total − expected| ≤ $0.02`. The tolerance covers rounding.
- Anything else is written to the output with an `Issue`:
  - `price mismatch`: a quote exists and the total differs.
  - `no quote for destination country`: e.g. CZ, or a blank country cell.
  - `product not in quote sheet`: the brand isn't in the sheet at all.
  - `no line items found for this order`: the Shopify lookup missed it. Retry that order with
    `get-order` before you accept this.
  - A note says so when a variant couldn't be matched to one of the product's variant rows and
    the first row was used instead. Mention these to the user.

## Step 4: Review before writing

Read `mismatches.csv` and the summary. If most orders to one country mismatch by the same
amount, or dozens of products are "not in quote sheet", the cause is probably a parsing or
lookup problem, not real overcharges. Look into it before writing anything.

## Step 5: Write to the mismatch Google Sheet

Everything lives in the Drive folder **"Zendrop Quotation Checks"** (`state.json` → `folder_id`).
The master sheet is **"Zendrop Quotation Mismatches"** (`state.json` → `mismatch_sheet_id`). Both
were created in the user's own Google Drive (belladonnaeloja@gmail.com). Claude can't own a
Google file itself. Because they were created through the user's connected Drive, every later
run can open and edit them.

Columns (always in this order):
`Order #, Product Name, Quoted Price (USD), Total Price (CSV, USD), Difference (USD), Country, Order Date, Issue, Checked On`.
Difference = CSV total − quoted price (positive means Zendrop charged more than the quote).

The Google Drive connector can create files but **cannot edit a sheet's cells**. Editing cells
goes through Autosheet:

1. **Add to the master sheet (preferred).** Start an Autosheet agent
   (`autosheet_start_agent_google_sheets_spreadsheet`) on `mismatch_sheet_id`. Tell it to
   append the new rows under the existing ones on the first tab, keep the same columns, and
   skip any row whose `Order #` is already in the sheet. Paste the rows into the prompt. Then
   confirm the result with `read_file_content`.
2. **If Autosheet fails** (for example with a billing error like `api-billing-free-trial-ended`),
   use Google Drive `create_file` to make a new sheet named
   `Zendrop Quotation Mismatches – <YYYY-MM-DD>`, with `contentMimeType: "text/csv"`,
   `textContent` = the mismatch CSV and `parentId` = `folder_id`. Tell the user the master
   sheet wasn't updated and why, and give them the new sheet's link.
3. If `mismatch_sheet_id` can't be opened (the sheet was deleted), tell the user. Create a
   new master sheet in the folder only once they agree, then update `state.json` and commit
   and push it.

If there are no mismatches, don't touch any sheet. Just say so.

## Step 6: Report back

Tell the user: how many orders were checked, how many matched, and how many were flagged per
issue type. List the biggest price differences, mention any variant rows that were guessed,
and give the mismatch sheet link.

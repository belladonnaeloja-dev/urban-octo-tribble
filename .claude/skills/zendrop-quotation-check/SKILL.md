---
name: zendrop-quotation-check
description: 'Cross-check every order in a Zendrop orders CSV (Order Number, Total (USD), Country) for the Zanaro Berlin store against the quoted prices in the "Zendrop_quote_request" Google Sheet — the order total must equal the quoted USD price (column Q for DE, the matching country USD column for AT/CH/NL/BE/FR/CZ) for one unit, or (column O product cost × quantity) + (Q − O) for more than one unit. Line items come from Shopify. Overcharges are logged in one place only: the price-check tab (gid=1212070020) of that same Zendrop_quote_request file. Use when the user asks to check/verify/cross-check Zendrop quotations, orders or order totals, run the weekly quotation check, or shares a Zendrop orders CSV plus the quote sheet.'
---

# Zendrop quotation check (orders CSV × Zendrop_quote_request)

Checks that Zendrop charged what it quoted. For each order in the CSV, the expected charge is the
country quote for the first unit plus the product cost (column O) for every extra unit.
The quote column depends on the order's destination country. Overcharges go into the price-check tab of the quote file.

The only thing this skill ever writes to is that price-check tab. It never changes the quote tab,
Shopify or the CSV, and it never creates other sheets or files.

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

- **Quote file and price-check log tab:** see `state.json`. The log is the tab with
  gid `1212070020` inside the quote file (`1SvNOGcVRPUv2DruK6yNZBneZm3WoLvxY`):
  https://docs.google.com/spreadsheets/d/1SvNOGcVRPUv2DruK6yNZBneZm3WoLvxY/edit?gid=1212070020#gid=1212070020
- **Shopify store:** the Zanaro Berlin store, whose orders are named `#BC…`. Verify it with
  `get-shop-info`, then `get-order` on the first order number in the CSV, before looking up
  the rest. If a different store is connected, don't switch on your own: tell the
  user. Switching logs the current store out, and they have to approve the new one in their
  claude.ai connector settings.

## Step 1: Read the quote sheet

Call Google Drive `read_file_content` with the quote sheet ID. Save the returned `fileContent`
string exactly as returned to `<scratchpad>/quotes.txt`, then check how it parsed:

```
python3 .claude/skills/zendrop-quotation-check/scripts/check_quotes.py --quotes <scratchpad>/quotes.txt --dump-quotes
```

The first output line must be
`USD quote columns: DE=Q, AT=S, CH=U, NL=W, BE=Y, FR=AA, CZ=AC | product cost = O`.
`read_file_content` returns both tabs one after the other. The script splits them at the log
tab's header row (`Price Check Date,Order #,…`) and reads the order numbers already in the log,
so they aren't added twice.
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
python3 .claude/skills/zendrop-quotation-check/scripts/check_quotes.py \
  --quotes <scratchpad>/quotes.txt --orders <path to CSV> --items <scratchpad>/items.json \
  --out <scratchpad>/flagged.csv --log-out <scratchpad>/log_rows.tsv --checked-on <today YYYY-MM-DD>
```

Rules the script applies:
- **Quoted price for the order** (the country quote column: DE → Q, AT → S, CH → U, NL → W,
  BE → Y, FR → AA; product cost is column O, "Product Cost ($)"):
  - **1 unit:** the country quote, e.g. column Q.
  - **More than 1 unit:** `(O × quantity) + (Q − O)`. The first unit is charged the full quote
    and each extra unit only the product cost. For other countries, use that country's column
    in place of Q.
  - **Several products/variants in one order:** every unit at its own O, plus the largest
    `(quote − O)` once.
  - If a product has no USD cost in column O (blank, or written in €), the script falls back
    to quote × quantity and says so in `Issue`.
- **Match** if `|CSV total − expected| ≤ $0.02`. The tolerance covers rounding.
- Anything else is written to the output with an `Issue`:
  - `price mismatch`: a quote exists and the total differs.
  - `no quote for destination country`: e.g. CZ, or a blank country cell.
  - `product not in quote sheet`: the brand isn't in the sheet at all.
  - `no line items found for this order`: the Shopify lookup missed it. Retry that order with
    `get-order` before you accept this.
  - A note says so when a variant couldn't be matched to one of the product's variant rows and
    the first row was used instead. Mention these to the user.

## Step 4: Decide what goes in the log

`flagged.csv` lists every order that didn't match, for the report. `log_rows.tsv` holds only
the rows for the log tab. An order goes in the log only when **all** of these are true:
- it's a `price mismatch` (not "no quote for destination country" and not "product not in
  quote sheet");
- Zendrop charged **more** than the quote (undercharges stay out);
- the overcharge isn't one of the known flat amounts, **+$3.80 or +$0.20** (±$0.01, so +$3.81
  is also left out). Change these with `--known-fees`;
- its order number isn't in the log already.

Before writing anything, read the summary. If most orders to one country are off by the same
amount, or dozens of products come back "not in quote sheet", the cause is probably a parsing
or lookup problem, not real overcharges. Look into it first.

## Step 5: Add the rows to the price-check log tab

**The price-check tab (gid `1212070020`) is the only place this skill writes. Don't create
any other sheet or file, not even as a fallback.**

The log's columns, in order:
`Price Check Date, Order #, Product Name, Quantity, Quoted Price (USD), Total Price (USD), Difference (USD), Country, Issue, Solution, Fixed, Notes`.
New rows get today's date, prices written like `$16.07`, Issue `price mismatch`, Solution and
Notes blank, and Fixed `FALSE`. The Solution, Fixed and Notes columns belong to the team.
Never change an existing row.

How to write the rows:
1. Start an Autosheet agent (`autosheet_start_agent_google_sheets_spreadsheet`) with the
   log tab URL from `state.json`. Tell it to append the rows from `log_rows.tsv` below the last
   filled row of that tab, in the same columns, and not to touch any other tab or row. Then
   confirm with `read_file_content` that the new order numbers show up after `Price Check Date`.
2. If Autosheet fails, don't write anywhere else. It fails, for example, with a billing error
   like `api-billing-free-trial-ended`, or because the file is an `.xlsx` it can't edit. Tell
   the user what failed. Then give them the contents of `log_rows.tsv` in a code block, so they
   can paste it into the first empty row of the log tab (tab-separated, so it fills the columns).
3. If there are no new log rows, don't touch the file. Just say so.

## Step 6: Report back

Tell the user: how many orders were checked, how many matched, and how many were flagged per
issue type. Then say how many rows went into the log (or are waiting to be pasted in), and how
many were left out: known fees, undercharges, no quote, or already logged. List the biggest
overcharges, mention any variant rows that were guessed, and link the log tab.

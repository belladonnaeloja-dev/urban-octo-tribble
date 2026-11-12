---
name: daily-cogs-check
description: Daily COGS checker. Also prices a store's Shopify order export (CSV) from the ticked rows of the Zendrop quote request sheet in EUR. Totals the cost of goods sold (product + shipping cost) of every order placed on a given day, per store and across all stores (Zanaro Berlin, Solundi, Modlia, Nestilia), using the Zendrop order costs, and flags every order whose cost is missing or looks wrong (External / agent-fulfilled, unlinked, on hold, zero-cost). Logs one row per store per day to the "Daily COGS" Google Sheet. Use when the user asks to check COGS, total yesterday's COGS, "daily COGS", "what did the orders cost today", cost of goods for a date or date range, or runs this as a scheduled daily task.
---

# Daily COGS check

Totals the COGS of all orders for one day (default: **yesterday**), for
every connected store, and logs it.

**COGS of an order = Zendrop product cost + Zendrop shipping cost (USD).**
Canceled orders are excluded.

## Defaults

| Parameter | Default |
|---|---|
| Day | yesterday (`YYYY-MM-DD`, the day the orders were placed) |
| Stores | all stores returned by Zendrop `get_stores` (see `references/stores.md`) |
| Date basis | `order_date` |
| Currency | USD (Zendrop's billing currency — never mix in EUR shop prices) |

If the user names a date, a range, or one store, use that instead. For a
range, run the workflow once per day so each day gets its own row.

## Workflow

1. **List the stores.** Zendrop `get_stores`. Check the IDs against
   `references/stores.md`; if a store is new or an ID changed, fix the table.

2. **Pull every order of the day, per store.** Zendrop `get_orders` with
   `store_id`, `date_from` = `date_to` = the day, `limit: 50`, and page
   through until you have `total` orders (`page` 1, 2, 3 ...). Do **not**
   filter by status. Save the pages for each store as one JSON file in the
   scratchpad, e.g. `orders_<store_id>_<day>.json`, containing
   `{"store_id": ..., "store_name": ..., "day": ..., "orders": [ ...every order object... ]}`.

   In the `get_orders` result, an order's `total` **is its Zendrop cost**
   (product + shipping, USD) — confirmed against `get_order`'s
   `cost_details.total_cost`. It is not the customer's order value.

3. **Total it.** Run
   `python3 scripts/total_cogs.py <scratchpad>/orders_*_<day>.json --out <scratchpad>/cogs_<day>.json`.
   It sums `total` over non-canceled orders, breaks the totals down by
   status, and lists every non-canceled order with a cost of 0 — those are
   the orders with **no COGS in Zendrop yet**:
   - `External` — fulfilled outside Zendrop (agent, Service Points ...).
   - `Unfulfilled` — not paid yet, often with issues like "Please link the
     product" or "This product has been removed from Zendrop".
   - `Processing` with 0 — invoice not final yet.

4. **Estimate the missing COGS** (only if the user wants a complete figure,
   or when running the scheduled task — say which figures are estimates):
   - For `Unfulfilled` orders whose product is linked, Zendrop
     `get_order_fulfillment_cost` (batch the order IDs, ≤ 50 per call,
     `is_credit_redeem: false`) gives the cost Zendrop would charge. This
     only previews; **never call `fulfill_order`**.
   - For `External` and unlinked orders, `get_order` gives the line items
     (title + quantity). Price them with the lowest quote in the store's tab
     of the "Zanaro Top Bestsellers by Quotation %" sheet (see
     `../quotation-check/references/store_sheets.md`, column G
     "Quotation - Lowest", matched on the brand name before ™). Products not
     in that tab stay unpriced — list them.
   - Put these into the JSON as `estimates: [{"order_id", "order_number", "cost", "source"}]`
     and re-run `total_cogs.py` so the estimated total is reported
     separately from the actual total.

   Keep `get_order` calls reasonable: on a normal day this is 20–40 orders
   for Zanaro Berlin. If more than ~80 orders need a lookup, ask before
   doing them all.

5. **Sanity checks** (the script prints these as warnings — repeat them to
   the user):
   - An order whose cost is above 3× the day's median order cost.
   - More than 25% of the day's orders without a cost.
   - The day's actual COGS differs by more than 50% from the previous
     logged day for that store (compare with the sheet, step 6).
   Optionally cross-check the actual total against Zendrop
   `get_orders_performance` (same day, `date_basis: "order_date"`) field
   `ordersCosts`; a small gap is normal (timezone edges), a large one means
   orders were missed while paging.

6. **Log to the sheet.** See `references/cogs_sheet.md` for the spreadsheet,
   tab layout and how to write the rows (one row per store per day, plus an
   "ALL" row). If a row for that store and day already exists, overwrite it
   rather than adding a duplicate. If the Sheets tools are unavailable, send
   the TSV the script writes (`--tsv`) with SendUserFile instead.

7. **Reply** with a short summary, not the full table:
   - Day, COGS total across all stores (actual, plus estimated if done).
   - Per store: orders, orders with cost, actual COGS, avg COGS per costed
     order.
   - Orders without COGS (count per store and status), and any warnings.
   - The sheet link.

## Alternative: Shopify order export + quote sheet (EUR)

When the user uploads a Shopify orders export (CSV) for a store and points
to the Zendrop quote request sheet ("use the ticked products", "Euro
equivalent of the quotations"), price each order line from that sheet
instead of Zendrop's billed cost. Follow `references/quote_sheet.md`:
only rows of that store with column O ticked, the EUR quote for the
store's destination (Nestilia → US, column AH), then the BER/PMs sheet
(store tab, column H "QP + 2,60", the agent price incl. €2.60) for anything not ticked or
missing. Quotes are per offer, so multiply by the line quantity only.
Products in neither sheet get 33% of their EUR selling price, marked as
such. Never use an unticked quote.

## Optional: COGS as a share of revenue

If the user asks for COGS % / margin and the Shopify connector is signed in,
pull the day's revenue per store with ShopifyQL
`FROM sales SHOW orders, total_sales SINCE <day> UNTIL <day>` (one call per
store; switch stores with `switch-shop`). Shopify reports in the shop's
currency (EUR for DE/NL/FR, USD for US) while Zendrop costs are in USD, so
convert before dividing and state the rate used. If Shopify needs
re-authentication, say so and skip this part rather than guessing revenue.

## Why it works this way

- **Zendrop's `get_orders` list instead of `get_order` per order.** The list
  already carries each order's cost, so a day of ~100 orders costs 2–3 calls
  per store instead of ~100.
- **Actual and estimated COGS kept apart.** Unfulfilled and External orders
  have no invoice in Zendrop; mixing guesses into the actual figure would
  make the daily trend unreliable.
- **`get_orders_performance` only as a cross-check.** Its cost covers
  Zendrop-fulfilled orders only and doesn't list which orders are missing.

---
name: zanaro-quotation-check
description: Check supplier quotation cost against Shopify selling price to flag thin-margin best sellers, delivered as a new dated tab on the store's canonical Google Sheet. Use this whenever the user uploads a supplier-quotation xlsx export (columns like "Product name", "Lowest quoted 1 pcs price", "Highest quoted 1 pcs price", "Store name") and wants it compared against Shopify prices — trigger phrases include "quotation check", "quotation percentage", "quotation %", "compare quotation to Shopify price", "margin check against supplier quote", "check the quotation for my best sellers", or requests to cross-reference a supplier-price xlsx with a Shopify store's selling prices. Also use this proactively when the user asks for "best sellers by revenue" or "top products" cross-referenced against a cost/quotation file, even if they don't name the metric "quotation %" explicitly.
---

# Zanaro Quotation Check

Cross-reference a supplier-quotation export against live Shopify prices for
a store's best sellers, and surface the ones where the supplier's cost eats
the largest share of the selling price — i.e., the thinnest margins among
the products actually driving revenue. Deliver the result as a **new tab,
named with today's date, on that store's one running Google Sheet** — never
a new spreadsheet file per run (see Step 7).

**Quotation % = Lowest quoted 1-pcs supplier price ÷ Shopify selling price × 100.**
Higher means thinner margin (the supplier quote is a bigger fraction of
what the customer pays) — that's what "top by quotation %" surfaces.

## Before starting: confirm the parameters

Default to these if the user doesn't specify, and just proceed — don't
block on asking unless the user's request is genuinely ambiguous about
something these defaults can't resolve (e.g. they name two different
stores and don't say which xlsx belongs to which):

| Parameter | Default |
|---|---|
| Lookback window for best sellers | last 90 days |
| Best sellers checked | top 100 by revenue |
| Rows in the output sheet | top 20 by quotation % |
| Minimum quotation % to flag | 33% |

If you do need to ask something, use the same conversational tone as the
rest of the session rather than a rigid form — e.g. "want me to check the
last 90 days of best sellers, or a different window?" Don't re-ask about
choices a defaults table already covers, and don't stall the whole task on
a question the user might not have a strong opinion on — state the default
you're using and move on; they can correct you.

## Workflow

1. **Read the xlsx.** Use `scripts/parse_quotation_xlsx.py` — it installs
   `openpyxl` if missing and handles the column layout described in its
   docstring. Run it once without `--store` first if you don't yet know
   which Shopify store the file belongs to; it prints every store name
   found so you can confirm before filtering.

2. **Confirm the store.** Run `graphql_query` (Shopify MCP) with
   `{ shop { myshopifyDomain } }`. The xlsx's "Store name" column holds the
   myshopify.com subdomain (e.g. `bycheri` for `bycheri.myshopify.com`),
   which is usually *not* the same as the storefront's customer-facing
   domain (e.g. `zanaroberlin.com`) — don't assume they match, check. Then
   re-run `parse_quotation_xlsx.py` with `--store <subdomain>`.

3. **Pull best sellers by revenue.** See
   `references/shopifyql_bestsellers.md` for the exact ShopifyQL query and
   how to shape its output into the `titles.json` / `bestsellers.json`
   files the later scripts expect.

4. **Look up current Shopify selling prices for those titles.** Run
   `scripts/build_batch_queries.py titles.json` to generate a handful of
   batched, aliased GraphQL queries (default 20 titles/batch — this turns
   ~100 individual lookups into ~5 round trips). Run each batch through the
   Shopify MCP's `graphql_query` tool in turn.

5. **Resolve ambiguous/duplicate listings, then build `shopify_prices.json`.**
   Read `references/matching_notes.md` before doing this step — it covers
   filtering out price-test/duplicate listings and what to do when more
   than one real listing shares a title. The file you produce should map
   `{ "<exact bestseller title>": [price, ...] }`.

6. **Join everything and compute quotation %.** Run
   `scripts/match_and_build_sheet.py` with `--bestsellers`,
   `--parsed-quotations` (from step 1/2), `--shopify-prices` (from step 5),
   plus `--top-n`, `--threshold`, `--lookback-days` matching whatever was
   confirmed in step 0. It handles title matching (exact first, then a
   promo-text-stripped fallback — see `references/matching_notes.md` for
   why `Product shopify ID` isn't a reliable join key), picks the most
   recently approved quote when a product was re-quoted, and prints a
   summary plus the top 3 flagged products to stdout — use that for your
   reply to the user without re-deriving it by hand. It also warns on
   stderr about any best sellers it couldn't match; skim that list before
   moving on in case it points at a real data problem (e.g. wrong store
   filtered) rather than an expected drift in title text.

7. **Publish the result as a new dated tab on the store's canonical Google Sheet.**

   Each store keeps **one running spreadsheet**, and every skill run adds
   its result as a **new tab named with the date of that run** (`YYYY-MM-DD`,
   e.g. `2026-08-28`) — never a new file, and never overwriting a previous
   run's tab. That date is the day the skill runs, not any date inside the
   xlsx.

   State lives in `state/sheets.json` in this skill folder, keyed by the
   myshopify subdomain confirmed in step 2:
   ```json
   { "<subdomain>": { "spreadsheet_id": "...", "url": "..." } }
   ```

   - Read `state/sheets.json` (treat a missing/empty file as `{}`).
   - **Store not yet a key (first run ever for this store):** Read the CSV
     produced in step 6 and pass it to the Google Drive MCP's `create_file`
     with `contentMimeType: "text/csv"`, the CSV as `textContent`, and
     `title`: "<Store> Quotation Check" — Drive auto-converts it to a native
     Google Sheet. That first run's data lands on the sheet's one default
     tab; immediately use the Autosheet MCP's
     `autosheet_start_agent_google_sheets_spreadsheet` tool against the
     returned file's ID to rename that tab to today's date. Record the
     spreadsheet's ID and URL in `state/sheets.json` under this store's
     subdomain and write the file back.
   - **Store already has a spreadsheet_id (every later run):** Use the
     Autosheet MCP's `autosheet_start_agent_google_sheets_spreadsheet` tool
     against that `spreadsheet_id`. Give it a prompt that: (a) tells it to
     add a new tab named with today's date — if a tab with that exact name
     already exists because the skill ran more than once today, suffix it
     `-2`, `-3`, etc.; (b) includes this run's CSV content (header row,
     ranked product rows, and the methodology footer rows from step 6) to
     populate that new tab as a table, matching the column layout/formatting
     of the existing tabs.
   - Either way, end up with the spreadsheet's shareable URL for the reply
     in step 8.

8. **Reply to the user** with the Sheet link (and, if useful, a direct
   mention of which tab — today's date — holds this run's results) plus a
   short summary: how many best sellers were checked, how many matched and
   cleared the threshold, and the top 2-3 flagged products by name and
   quotation %. Don't restate the whole table in chat — the sheet is the
   deliverable.

## Why this shape, not something simpler

A few things about this workflow are deliberate, not incidental — worth
knowing so you don't "simplify" them away on a future run:

- **One spreadsheet per store, one new dated tab per run — not a new file
  every time.** A fresh spreadsheet per run scatters history across many
  files with no easy way to compare today's flagged products against last
  month's, and it's what this skill's first draft did before being
  corrected. Keeping one spreadsheet with a tab per run date keeps every
  past check in one place and makes the run date unambiguous (it's the tab
  name, not a column you have to read).

- **Lowest quote vs. minimum Shopify price, not an average.** A product's
  quoted variants and its Shopify variants can span very different price
  ranges (a basic version vs. a premium/motorized one, say). Averaging the
  xlsx's lowest+highest against a single Shopify price silently mixes
  those populations and can produce a nonsensical ratio (this happened in
  practice — a >280% "quotation %" that came from a €12 quote and a €210
  quote for the same product line, averaged against one mid-range Shopify
  price). Lowest-vs-minimum is the one pairing that stays internally
  consistent no matter how wide the variant spread is.

- **Title matching, not the xlsx's "Product shopify ID" column.** That ID
  doesn't correspond to any live Shopify product or variant — it's from
  the quotation platform's own bookkeeping. Titles (exact, with a
  promo-text-stripped fallback) are the reliable join key.

- **Batched GraphQL over one-call-per-product.** At 100 best sellers, doing
  this one product at a time is 100 round trips; aliasing ~20 per query
  cuts that to ~5 without changing the result.

## Extending this beyond the standard flow

If the user wants the *full* checked list (not just the top N), pass a
larger `--top-n` to `match_and_build_sheet.py` (or omit filtering and hand
over all matched rows) — the script already computes quotation % for every
matched product, it just truncates on output.

If they want to flip the question — cheapest supplier cost as a share of
price, i.e. the *fattest*-margin best sellers — sort ascending instead;
that's a one-line change to `ranked = sorted(...)` in
`match_and_build_sheet.py` if you're editing a copy, or just re-sort the
script's printed/CSV output yourself for a one-off ask rather than
modifying the shared script.

## Known gaps in this skill folder (fill in as they're hit)

This skill was authored in one pass and hasn't yet been run end-to-end, so
a few things are unverified:

- `state/sheets.json` doesn't exist yet — the first real run creates it.
- The exact prompt phrasing that gets the Autosheet agent to reliably (a)
  rename a default tab and (b) add a new tab with a specific name and
  populate it from pasted CSV-shaped text hasn't been tested against a
  real spreadsheet. If a run's phrasing doesn't work as expected, note
  what did work here so the next run doesn't have to rediscover it.
- Whether the Shopify MCP's `graphql_query` tool is reachable from
  whatever session runs this skill (cloud vs. desktop) should be confirmed
  before relying on steps 2-4; if it isn't, say so rather than guessing at
  prices.

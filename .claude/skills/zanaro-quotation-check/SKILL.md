---
name: zanaro-quotation-check
description: Check supplier quotation cost against Shopify selling price to flag thin-margin best sellers, delivered as a Google Sheet. Use this whenever the user uploads a supplier-quotation xlsx export (columns like "Product name", "Lowest quoted 1 pcs price", "Highest quoted 1 pcs price", "Store name") and wants it compared against Shopify prices — trigger phrases include "quotation check", "quotation percentage", "quotation %", "compare quotation to Shopify price", "margin check against supplier quote", "check the quotation for my best sellers", or requests to cross-reference a supplier-price xlsx with a Shopify store's selling prices. Also use this proactively when the user asks for "best sellers by revenue" or "top products" cross-referenced against a cost/quotation file, even if they don't name the metric "quotation %" explicitly.
---

# Zanaro Quotation Check

Cross-reference a supplier-quotation export against live Shopify prices for
a store's best sellers, and surface the ones where the supplier's cost eats
the largest share of the selling price — i.e., the thinnest margins among
the products actually driving revenue. Deliver the result as a Google
Sheet.

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

7. **Publish the result as a new dated tab in the (one) Google Sheet.**
   This skill keeps **one cumulative spreadsheet**. Every run adds its
   result as a **new sheet/tab** inside that spreadsheet — never a new
   spreadsheet file. Name the new tab with the date the skill was run,
   `YYYY-MM-DD` (today's date, not the xlsx's date or the lookback window).
   If a tab with that name already exists (a second run the same day),
   suffix it `YYYY-MM-DD (2)`, `YYYY-MM-DD (3)`, etc. rather than
   overwriting it.

   - **First run only, or if no canonical spreadsheet is on record:** check
     the "Canonical spreadsheet" note at the bottom of this file. If it's
     still unfilled, ask the user which existing Google Sheet to use, or
     create a new one via the Google Drive MCP's `create_file`
     (`contentMimeType: "text/csv"`, minimal placeholder content — the tab
     it creates gets renamed/used for the first run's results in the next
     step). Once you have a spreadsheet ID either way, **write it into the
     "Canonical spreadsheet" note in this file** so every later run reuses
     it automatically instead of asking again or minting a new file.

   - **Every run (including the first):** use the Autosheet MCP —
     `autosheet_start_agent_google_sheets_spreadsheet` with `spreadsheet_id`
     set to the canonical ID — with a prompt instructing it to: add a new
     tab named with today's date (checking first whether that name is
     already taken and suffixing if so), write in the full contents of the
     CSV produced by `match_and_build_sheet.py` (header row, data rows, and
     the trailing methodology block), and report back the tab name, gid,
     and row count it wrote. Use `autosheet_follow_up_agent` for any
     correction in the same turn rather than starting a fresh agent.

   - Don't hand-format the sheet yourself (column widths, colors, etc.)
     beyond what the CSV import gives you unless the user asks — the Sheet
     is the deliverable, not a design exercise.

8. **Reply to the user** with the Sheet link (pointing at today's tab —
   append `#gid=<id>` if the Autosheet agent reported one) and a short
   summary: how many best sellers were checked, how many matched and
   cleared the threshold, and the top 2-3 flagged products by name and
   quotation %. Don't restate the whole table in chat — the sheet is the
   deliverable.

## Canonical spreadsheet

Not yet created. On the first real run, record the spreadsheet here so
every subsequent run reuses it instead of creating a new file:

- Spreadsheet URL: _(fill in after first run)_
- Spreadsheet ID: _(fill in after first run)_

## Why this shape, not something simpler

A few things about this workflow are deliberate, not incidental — worth
knowing so you don't "simplify" them away on a future run:

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

- **One spreadsheet, one new tab per run — not a new file per run.** A new
  file every run scatters history across Drive and forces the user to go
  hunting for "today's" link. One spreadsheet with a dated tab per run
  keeps every run's result discoverable in one place while still keeping
  each run's numbers separate (unlike appending rows into one tab, which
  would blend different runs' rankings together).

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

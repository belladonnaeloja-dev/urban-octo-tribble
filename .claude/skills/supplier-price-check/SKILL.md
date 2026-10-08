---
name: supplier-price-check
description: 'Weekly supplier price comparison for the DE store: read the "BER/PMs" Google Sheet (DE tab), compare the Service Point price ("QP + 2,60" column) against the Zendrop price ("(Best) Agent Price €" inside the ZENDROP block) for every product variant, and append the product variants that are new since the last run to the DE tab of the "Supplier Price Comparison - (Service Point vs Other supplier)" Google Sheet, with today''s date in column A. Never adds a product where Service Point is cheaper (negative difference) or where the gap is under 1 EUR, never re-adds a product that was added before, and never edits or deletes existing rows. Use this skill whenever the user asks to run, redo, refresh or schedule the supplier price check, compare Service Point vs Zendrop / "other supplier" prices, update the supplier price comparison sheet, add new products to the comparison, or when the weekly Monday Routine fires.'
---

# Supplier price check (Service Point vs Zendrop, DE)

Compares two supplier prices for every product variant on the DE tab of the sourcing sheet and
appends only the variants that are new since the last run to the comparison sheet the user
curates. The user prunes that sheet by hand (deleting rows they have handled or disagree with),
so this skill is strictly additive: it appends new rows and writes a log, and it never edits,
re-orders, re-prices or deletes anything that is already there. The source sheet is read-only.

## Fixed IDs (this workspace)

| What | Value |
|---|---|
| Source spreadsheet "BER/PMs" | `1MRyyd2gDbwVOstNetjJsGEF--rVAKcAoYyf6dAVmm3A`, tab `DE` (about 5,500 product rows) |
| Target spreadsheet "Supplier Price Comparison - (Service Point vs Other supplier)" | `137yF1r5u8S7rusoAN2L8botzIajBD8NnJa1v6cBnqH0` |
| Target tab `DE` | sheetId `105541484` |
| Target tab `Run log` | sheetId `777001` |

Confirm the tab names and sheet IDs with `get_spreadsheet` (fields `sheets.properties`) before
writing. If a tab was renamed or is missing, stop and ask rather than guessing.

Tools: Google Sheets connector (`get_spreadsheet`, `get_values`, `update_values`,
`update_formulas`, `update_spreadsheet`). Google Drive `read_file_content` is **not** suitable for
the source sheet: it silently returns only the first ~70 rows of each tab. If the Sheets
connector is missing, say so and stop; do not create a new file instead.

## Step 1 — Read the source tab in full

Read `DE!A1:AC6500` with `get_values`. The result is large and is usually saved to a file; parse
that file with Python (`python3 -I`) rather than re-typing anything. Row 1 holds group labels
(`Fulfilled on`, `ZENDROP`, `SOURCING ALERT`), row 2 holds the column headers, data starts at
row 3. Trailing empty rows are normal.

If `get_values` fails on the size, fall back to Drive `download_file_content` with
`exportMimeType` set to the xlsx type and read the `DE` sheet with `openpyxl` (`data_only=True`).

## Step 2 — Locate the columns by header, not by letter

The user refers to these as "column J" and "column W", but the letters have already moved once
(in September 2026 "QP + 2,60" was column K; by October it was J). Resolve them from row 2
every run and report the letters you found:

- **Name in store**: header `Name in store`. **Short name**: `Short product name`. **Variant**: `Variant`.
- **Service Point price**: header `QP + 2,60`. This is the quote price plus a 2.60 fee.
- **Service Point quote present?**: the first header `(Best) Agent Price €` (the one in the
  Service Point block, left of the ZENDROP group). When it is empty, `QP + 2,60` shows just the
  2.60 fee and must not be treated as a price.
- **Zendrop price**: the header `(Best) Agent Price €` whose row-1 group label is `ZENDROP`
  (the second occurrence, right of the first). It is a formula on the Zendrop dollar price, so it
  shows 0 when no Zendrop quote exists.

If any of these headers cannot be found, stop and tell the user what the header row looks like
now; do not fall back to letters.

Values can arrive as numbers or as display strings such as `€4,37` or `0,87`. Strip the `€`
and spaces and turn a decimal comma into a point before comparing.

## Step 3 — Build the candidate list

A variant qualifies only when all of the following hold:

1. Service Point quote is present (first `(Best) Agent Price €` non-empty) and `QP + 2,60` is a number.
2. Zendrop price is a number greater than 0.
3. **Difference = Service Point − Zendrop is at least +1.00 EUR.** A negative difference means
   Service Point is already cheaper; the user does not want those rows on the sheet, ever. A gap
   under 1 EUR is noise the user asked to leave out.

Then drop every candidate whose product is already known, matching on **Name in store** after
normalising (collapse whitespace, lowercase). Compare at product-name level, not variant level,
because the user edits variant labels on the target sheet and removes variants they do not want.
A product is "known" when its name appears in either:

- column B of the target `DE` tab (rows currently on the sheet), or
- column B of the `Run log` tab (everything ever added or deliberately skipped; rows the user
  later deleted from `DE` must not come back).

A new store listing with a different name (for example `1+1 GRATIS HEUTE | ToePerfect™ …` next
to an older `ToePerfect™ … | 1+1 GRATIS TEMPORÄR`) counts as a new product. Mention such
near-duplicates in the report so the user can decide.

## Step 4 — Append the new rows to the target `DE` tab

Target layout, header in row 1 (keep it exactly; do not add columns):

| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Date | Name in store | Short name | Variant | Service Point | Other supplier | Difference | New ServicePoints Price (1 week) | Bella Notes |

1. Find the first empty row: read `DE!B1:B2000` and take the last non-empty row + 1.
2. Write `A:F` for the new rows with `update_values`: today's date as `yyyy-mm-dd`, Name in
   store, Short name (empty if none), Variant (as a number when it is one), Service Point and
   Zendrop prices rounded to 2 decimals.
3. Write column G with `update_formulas`: `=E{n}-F{n}` for each new row n. The difference is
   always a formula so the user can edit a price and see it recalculate.
4. Leave H and I empty; those are the user's columns.
5. Apply the date format with one `repeatCell` on the new rows of column A
   (`numberFormat` type `DATE`, pattern `yyyy-mm-dd`) so stray cell formats do not show
   `mm/dd/yyyy` on some rows. Columns E:G already carry the `[$€]#,##0.00` format for the whole
   column; if a new row shows plain numbers, apply that format too.
6. Read the new rows back and check: dates are real dates, prices show as `€x.xx`, column G
   shows a positive difference on every added row, and no `#REF!` or `#VALUE!` appears.

Keep the source order (sheet row order) when appending; do not sort the user's tab.

## Step 5 — Log every decision in `Run log`

Append one row per candidate from Step 3 (including the skipped ones) to the `Run log` tab:

| Run date | Name in store | Variant | Service Point | Other supplier | Difference | Action |
|---|---|---|---|---|---|---|

`Action` is one of `added`, `skipped: negative difference`, `skipped: difference under 1 EUR`,
`skipped: already on sheet`, `skipped: logged before`. Logging the skipped ones is what keeps the
weekly runs honest: the user can see why something did not appear, and the log doubles as the
memory that stops deleted products from coming back.

## Step 6 — Report

Reply with: the number of source rows read, which column letters held the three price columns
this run, how many variants qualified, how many were added and how many skipped by each reason,
and a short list of the added products with their difference (largest first). Say "nothing new
this week" plainly when that is the case. Flag any header or layout change you noticed in the
source sheet, since that is the most likely way this process breaks.

## Schedule

A Routine named "Supplier price check (weekly)" runs this skill every Monday at 06:00 UTC
(08:00 Berlin in summer, 07:00 in winter) in a fresh session with the Google Drive and Google
Sheets connectors. A manual run is the same procedure; nothing in it depends on the day.

## Scope and guard rails

- DE tab only. The target workbook also has an `NL` tab; do not touch it unless the user
  extends the skill to NL.
- Never write to the source spreadsheet.
- Never edit, delete or reorder rows already on the target `DE` tab, even when the source
  prices for those products have changed. If the user wants refreshed prices, that is a separate
  request.
- Never add a product with a negative difference, even if the user's wording that day is
  "add everything"; ask first if they seem to want that.

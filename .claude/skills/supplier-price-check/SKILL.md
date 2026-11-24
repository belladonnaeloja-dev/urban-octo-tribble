---
name: supplier-price-check
description: 'Weekly supplier price comparison for the DE, NL, FR and USA stores: read the "BER/PMs" Google Sheet (DE, NL, FR and USA tabs), compare the Service Point price ("QP + 2,60") against the Zendrop price ("(Best) Agent Price €" inside the ZENDROP block) for every product variant, refresh the two price columns of the rows already on the matching tab of the "Supplier Price Comparison - (Service Point vs Other supplier)" Google Sheet, and append the product variants that are new since the last run with today''s date in column A. Only keeps products where Service Point is at least 3 EUR more expensive: never adds a product with a smaller (or negative) difference, never re-adds a product that was added before, sorts each tab by difference (highest first) and removes rows whose difference has dropped under 3 EUR, logging each removal. Use this skill whenever the user asks to run, redo, refresh or schedule the supplier price check, compare Service Point vs Zendrop / "other supplier" prices, update the supplier price comparison sheet, update its prices, add new products to the comparison, or when the weekly Monday Routine fires.'
---

# Supplier price check (Service Point vs Zendrop, DE, NL, FR and USA)

Compares two supplier prices for every product variant on the DE, NL, FR and USA tabs of the
sourcing sheet. On the comparison sheet the user curates, it refreshes the Service Point and
Zendrop prices of the rows already there and appends only the variants that are new since the last
run. The user prunes that sheet by hand (deleting rows they have handled or disagree with) and
writes notes in it, so this skill changes existing rows in only three ways: it refreshes the two
price columns, sorts the tab by difference, and removes rows whose difference has dropped under
3 EUR (logging each one first, with its notes). Otherwise it appends new rows and writes a log, and it never deletes or
rewrites anything else. The source sheet is read-only.

## Fixed IDs (this workspace)

| What | Value |
|---|---|
| Source spreadsheet "BER/PMs" | `1MRyyd2gDbwVOstNetjJsGEF--rVAKcAoYyf6dAVmm3A`, tabs `DE` (about 5,600 product rows), `NL` (about 3,600), `FR` (about 1,200) and `USA` (about 850) |
| Target spreadsheet "Supplier Price Comparison - (Service Point vs Other supplier)" | `137yF1r5u8S7rusoAN2L8botzIajBD8NnJa1v6cBnqH0` |
| Target tab `DE`, with its log `Run log` | sheetIds `105541484` and `777001` |
| Target tab `NL`, with its log `Run log NL` | sheetIds `302329013` and `777002` |
| Target tab `FR`, with its log `Run log FR` | sheetIds `302329014` and `777003` |
| Target tab `USA`, with its log `Run log USA` | sheetIds `302329015` and `777004` |

Run the whole procedure below once per market, in the order DE, NL, FR, USA. Each market reads
its own source tab, writes to its own target tab and checks and writes only its own log. Never use
one market's tab or log to decide what is known for another: the same brand often has a German,
Dutch, French and English listing, and each market needs its own comparison.

Confirm the tab names and sheet IDs with `get_spreadsheet` (fields `sheets.properties`) before
writing. If a tab was renamed or is missing, stop and ask rather than guessing.

Tools: Google Sheets connector (`get_spreadsheet`, `get_values`, `update_values`,
`update_formulas`, `update_spreadsheet`) and Google Drive `download_file_content`. Drive
`read_file_content` is **not** suitable for the source sheet: it silently returns only the first
~70 rows of each tab. If the Sheets connector is missing, say so and stop; do not create a new
file instead.

## Step 1 — Read the source tab and the target in full

Read `DE!A1:AK6500` (likewise `NL!`, `FR!` and `USA!`) with `get_values`. The result is large
and is usually saved to a file; parse that file with Python (`python3 -I`) rather than re-typing
anything. Row 1 holds group labels (`SP`, `Fulfilled on`, `BESTFULFILL`, `ZENDROP`,
`SOURCING ALERT`), row 2 holds the column headers, data starts at row 3. Trailing empty rows are
normal.

Read the target workbook once with Drive `download_file_content` and `exportMimeType` set to the
xlsx type, and open it with `openpyxl` (`data_only=True`). That gives every target and log tab in
one file, so nothing has to be re-typed.

If `get_values` fails on the size, read the source the same way (xlsx export, `openpyxl`).

## Step 2 — Locate the columns by header, not by letter

The letters move: in September 2026 DE's "QP + 2,60" was column K, by October it was J; DE's
Zendrop price moved from W to X in November 2026, and NL gained its own "QP + 2,60" column the
same month. Resolve the columns from row 2 every run and report the letters you found.

All four tabs now share the same rule:

- **Name in store**: header `Name in store`. **Short name**: `Short product name`. **Variant**:
  `Variant`. **Product ID**: `Product ID` (on some products it holds the variant label, such as
  `Upgrade-Version + 12 Stück …`).
- **Service Point price**: header `QP + 2,60`. This is the quote price plus a 2.60 fee.
- **Service Point quote present?**: the first header `(Best) Agent Price €` (the one in the
  Service Point block, left of the BESTFULFILL and ZENDROP groups). When it is empty or 0,
  `QP + 2,60` shows just the 2.60 fee and must not be treated as a price.
- **Zendrop price**: the header `(Best) Agent Price €` whose row-1 group label is `ZENDROP`. It is
  a formula on the Zendrop dollar price, so it shows 0 or `€ -` when no Zendrop quote exists.
- Ignore the BESTFULFILL block on NL (its own `(Best) Agent Price €`). It is a third supplier and
  is not part of this comparison.

As of November 2026 the letters were: DE I, J and X; NL G, H and AB; FR G, H and S; USA G, H
and W (quote present, Service Point, Zendrop). Headers can carry stray spaces, such as
`" (Best) Agent Price € "` on DE; compare them after trimming.

Row-1 group labels are written only above the first column of a merged block, so carry each label
to the right until the next label when deciding which group a column belongs to.

If any of these headers cannot be found, stop and tell the user what the header row looks like
now; do not fall back to letters.

Values can arrive as numbers or as display strings such as `€4,37`, `€ 1.234,50` or `0,87`. Strip
the `€`, `$` and spaces, drop thousands dots and turn a decimal comma into a point before
comparing. A lone `-` means no value. All prices compared are in euros, also on the USA tab.

## Step 3 — Refresh the prices of the rows already on the target tab

For every row already on the market's target tab, find its source row and rewrite **only E and
F** with the current Service Point and Zendrop prices, rounded to 2 decimals.

Match on **Name in store** (normalised: collapse whitespace, lowercase). When the name has several
source rows, narrow it down in this order and take the first one that leaves candidates: target
Variant (D) equals source `Product ID`; target Short name and Variant both equal the source's;
target Short name equals the source's; the name alone. Among the candidates not already used by
another target row, take the one whose current Service Point and Zendrop prices are closest to
the row's old E and F (smallest sum of the two absolute differences). The tabs are sorted by
difference (Step 5), so sheet order says nothing about which `GroomStation™` row belongs to which
source row; last week's prices do. Mention in the report any duplicate whose closest candidate
was still more than 2 EUR away on either price, since that match may be wrong.

- If the source no longer has a Service Point quote or a Zendrop price for that row, keep the old
  value in that column and list the row in the report.
- If no source row matches at all, leave the row alone and list it in the report.
- Never touch A–D, G, H or I. G is the formula `=E{n}-F{n}` and recalculates by itself; H and I
  are the user's notes.
- Rows whose difference is now under 3 EUR, negative ones included, are removed in Step 5
  (item 7).

Write all of E:F for the tab in one `update_values` call (`E2:F{last}`), keeping unchanged values
as they are.

## Step 4 — Build the list of new products

A variant qualifies only when all of the following hold:

1. Service Point quote is present (first `(Best) Agent Price €` above 0) and `QP + 2,60` is a number.
2. Zendrop price is a number greater than 0.
3. **Difference = Service Point − Zendrop is at least +3.00 EUR.** A negative difference means
   Service Point is already cheaper; the user does not want those rows on the sheet, ever. On
   24 November 2026 the user raised the minimum gap from 1 EUR to 3 EUR: smaller gaps are not
   worth acting on.

Only products that are not already known are considered, matching on the normalised **Name in
store**. Compare at product-name level, not variant level, because the user edits variant labels
on the target sheet and removes variants they do not want. A product is "known" when its name
appears in either:

- column B of the market's target tab (rows currently on the sheet), or
- column B of the market's log tab (everything ever added or deliberately skipped; rows the user
  later deleted from the target tab must not come back).

A new store listing with a different name (for example `1+1 GRATIS HEUTE | ToePerfect™ …` next
to an older `ToePerfect™ … | 1+1 GRATIS TEMPORÄR`) counts as a new product. Mention such
near-duplicates in the report so the user can decide.

## Step 5 — Append the new rows to the market's target tab

Target layout, header in row 1 (keep it exactly; do not add columns):

| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Date | Name in store | Short name | Variant | Service Point | Other supplier | Difference | New ServicePoints Price (1 week) | Bella Notes |

1. The first empty row is the last row with a value in column B, plus 1.
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

6. Sort the tab by difference, highest first: one `sortRange` request over `A2:I{last row}`
   (all nine columns, so the user's notes in H and I stay on their rows) with `sortSpecs`
   `[{"dimensionIndex": 6, "sortOrder": "DESCENDING"}]`. The user asked for the biggest gaps at
   the top; rows that have dropped under 3 EUR end up at the bottom. Sorting moves the G formulas
   with their rows, so `=E{n}-F{n}` still points at its own row. Before sorting, check that no
   column past I holds data; if one does, widen the range to include it.
7. Remove the rows whose difference is under 3 EUR. The user asked for this on 24 November
   2026: only gaps of 3 EUR and up are worth acting on, and a negative gap means Service Point
   is already cheaper. After the sort these rows form one block at the bottom of the tab.
   - Only remove a row when both E and F were refreshed from the source this run. If either
     price was kept from last week (Step 3: no quote or no match), leave the row and report it.
   - First append one row per removed row to the market's log tab (Step 6 layout) with today's
     date, its Name in store, Variant, E, F, difference, the action
     (`removed: negative difference` when the difference is below 0, otherwise
     `removed: difference under 3 EUR`) and, in column H "Notes when removed", the row's H and I
     values joined with ` | ` (prices written as `€x.xx`). The DE `Run log` already has that
     column; on another log tab, add it the first time a removed row has notes (append one
     column, copy G1's format to H1, title it "Notes when removed"). The log keeps the product
     from being added again and keeps the user's notes.
   - Then read column G of that block once more with `get_values` and check it still holds the
     same values in the same rows; if anything moved, read the tab again and rebuild.
   - Delete the block with one `deleteDimension` request (`dimension` `ROWS`, 0-based
     `startIndex`, exclusive `endIndex`).

## Step 6 — Log every decision in the market's log tab

Append one row per variant of every product that is **new this run** (not already known per
Step 4), whether it was added or skipped, to the market's log tab (`Run log`, `Run log NL`,
`Run log FR` or `Run log USA`):

| Run date | Name in store | Variant | Service Point | Other supplier | Difference | Action |
|---|---|---|---|---|---|---|

`Action` is one of `added`, `skipped: negative difference`, `skipped: difference under 3 EUR`,
or, for rows taken off the tab in Step 5, `removed: negative difference` or
`removed: difference under 3 EUR`. Older rows may also read `skipped: difference under 1 EUR`
or `removed: difference under 1 EUR` from before the 3 EUR rule; treat any row in the log as
"known", whatever its action.
Format the new log dates the same way as in Step 5.

Do not log variants of products that were already known: about 100 of them qualify every week,
and logging them would bury the useful rows. Logging the skipped new ones is what keeps the
weekly runs honest: the user can see why something did not appear, and the log doubles as the
memory that stops deleted or rejected products from coming back. A product skipped once (for
example because Service Point was cheaper) stays skipped in later weeks even if its prices move;
the user can delete its log rows to have it reconsidered.

## Step 7 — Verify

Export the target again as xlsx and compare every cell you wrote (the refreshed E:F, the new A:F
rows and the new log rows) against what you meant to write, in Python. Also check that column A
holds real dates, that column G is a number on every row (no `#REF!` or `#VALUE!`), that it is
at least 3.00 on every row of the tab except ones kept on purpose (stale price), that the tab is
sorted high to low, and that every row that was there
before the deletion, other than the removed ones, is still there unchanged. Fix any mismatch
before reporting.

## Step 8 — Report

Report each market separately. For each, give: the number of source rows read, which column
letters held the three price columns this run, how many existing rows changed price, which rows
were removed for dropping under 3 EUR (saying which were negative and that their notes are in
the log), which under-3 rows were kept because a price could not be refreshed, how many new
variants qualified, how many were
added and how many were skipped for each reason, and a short list of the added products with
their difference (largest first). Say "nothing new this week" plainly when that is the case.
Flag any header or layout change you noticed in the source sheet, since that is the most likely
way this process breaks.

## Schedule

A Routine named "Supplier price check (weekly)" runs this skill every Monday at 06:00 UTC
(08:00 Berlin in summer, 07:00 in winter) in a fresh session with the Google Drive and Google
Sheets connectors. A manual run is the same procedure; nothing in it depends on the day.

## Scope and guard rails

- DE, NL, FR and USA only. The source sheet also has SE, Juleani, Wham and template tabs; leave
  them alone unless the user extends the skill to another market. A new market gets its own target
  tab and log tab, copied from an existing pair (`duplicateSheet`, then delete the data rows) so
  the header and formats match.
- Never write to the source spreadsheet.
- On rows already on a target tab, change only E and F, apart from the sort and the removal of
  rows under 3 EUR in Step 5. Never delete a row for any other reason (no match, no quote);
  report those rows instead.
- Never add a product with a difference under 3 EUR, negative ones included, even if the user's
  wording that day is "add everything"; ask first if they seem to want that.

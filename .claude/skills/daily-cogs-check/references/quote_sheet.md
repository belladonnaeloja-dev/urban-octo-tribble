# COGS from the Zendrop quote request sheet (EUR)

Used when the user gives a Shopify order export (CSV) for one store and
asks for COGS from the quotation sheet instead of Zendrop's billed cost.

## The sheet

Google Sheet "Zendrop_quote_request", tab **"Zanaro Berlin"** (gid
1999748639), currently
https://docs.google.com/spreadsheets/d/1IAfwEUlRiF9eYV_PrwKc3v3RiVWEToG0SQ4xxMj6Kvk
(the user sends updated copies; always use the latest link they give). The
same workbook also exists as a 16 MB .xlsx in Drive — the connector cannot
read that one, so ask for the Google Sheets copy.

Header rows 1–3, data from row 4. All stores share this tab:

| Col | Meaning |
|---|---|
| B | Product name (Shopify title at the time of the request) |
| C | Store name: `Zanaro`, `Solundi`, `Modlia`, `Nestilia` |
| D / E | Variant / bundle details (e.g. "5 pieces", "2-piece Set") |
| O | **Linked** checkbox (TRUE/FALSE) — only ticked rows count |
| P | Zendrop product ID |
| T..AI | Quote per destination, pairs EUR / USD: T/U DE, V/W AT, X/Y CH, Z/AA NL, AB/AC BE, AD/AE FR, AF/AG CZ, **AH/AI US** |
| AJ | Zendrop remark ("similar", "Out of stock") |

Use the destination of the store's customers: Nestilia → US (AH, EUR);
Zanaro Berlin → DE/AT/CH; Solundi → NL/BE; Modlia → FR. The user wants the
**EUR** column.

## How to read it cheaply

1. `get_values` on `'Zanaro Berlin'!C4:C1002` to find the store's rows.
2. One `get_spreadsheet` call with `includeGridData: true`,
   `fields: ["sheets.data.startRow","sheets.data.rowData.values.formattedValue"]`
   and `ranges` = `'Zanaro Berlin'!B<r>:AJ<r>` for each of those rows.

## Matching rules

- Match on the brand name before ™ (strip the promo prefix), not the full
  title.
- Only rows with column O = TRUE. **Never use an unticked quote** — not
  in the total, not as an estimate, not as a "would add €X" figure. A
  product that is in the sheet but not ticked is treated as not found and
  goes to the BER/PMs fallback below.
- If several ticked rows exist for one product, use the lowest row (the
  latest request) and say so.
- Bundles: quotes are **per offer**, not per piece (BER/PMs shows it:
  LymphRelief single €9.46, "1 + 1 FREE" €14.74; column D there is pieces
  per offer). So COGS = quote × Lineitem quantity, even for `1+1 FREE`,
  `1 pair +1 pair FREE` or `2x` variants. Don't double.
- A quote cell with several prices per set size (e.g. FryLite "2-pieceSet
  €18.44 / 4-pieceSet €20.67") — pick the one matching the order's
  variant.
- Products with no ticked row for that store fall back to the **BER/PMs**
  sheet (https://docs.google.com/spreadsheets/d/1MRyyd2gDbwVOstNetjJsGEF--rVAKcAoYyf6dAVmm3A),
  on the store's tab (Nestilia → `USA`, gid 1209564048; also `DE`, `NL`,
  `FR`). Column A = product name, B = variant, D = pieces per offer,
  G = "(Best) Agent Price €", **H = "QP + 2,60" (per offer, use this)**. Data starts at
  row 3; the newest products are at the bottom, so read column A, then
  only the rows you need with `A<r>:L<r>`.
  **Layout changed on 12 Nov 2026:** G is now the bare agent price and
  H "QP + 2,60" is G + €2.60; the tab's own quote % (column I) uses H, and
  H equals what G showed before. Use **H** so days stay comparable (read
  the header row first; if the columns move again, use the one the
  tab's quote % is based on). Column K/L give the tab's current USD→EUR
  rate (12 Nov: about 0.902, e.g. $35.99 = €32.46); use it for `--rate`
  and the 33% fallback. For a product with several
  variant rows, take the row whose column B matches the order's variant
  (e.g. ColorClash "80 pieces"). Record the cell (e.g. `USA!H634`) as
  the source.
- Still not found in either sheet (no ticked quote and G blank/missing):
  **COGS = 33% of the selling price**, per unit × quantity. Use the EUR
  selling price from the BER/PMs row (column K "Selling Price Local
  Currency") when the product has a row there; otherwise the export's
  `Lineitem price` × the tab's exchange rate (column J, e.g. 0.90 for
  USA). Mark these lines as "33% of selling price" so they stay
  distinguishable from real quotes. Don't borrow another store's quote.
- Count every non-cancelled order, fulfilled or not. In the export, only
  the first line of a multi-line order carries the order fields; the extra
  lines still count.

## Computing it

Put every product of the export in a `prices.json` in the scratchpad
(format in the docstring of `scripts/price_export.py`: `cost` + `source`
for a quote, `sell_eur` + `source` for the 33% fallback), then run

    python3 scripts/price_export.py <export.csv> prices.json --rate 0.8979 --day <YYYY-MM-DD> --outdir <scratchpad>

`--rate` is USD→EUR from the BER/PMs USA tab ($19.99 = €17.95). The
script refuses to run if a product has no price, writes the per-line CSV
and the per-order COGS % ranking (highest first), and prints the summary.
Revenue = Subtotal (after discounts) − Refunded Amount; cancelled orders
are skipped; orders with an Outstanding Balance (unpaid post-purchase
upsell) are flagged.

## The "Nestilia Daily COGS" workbook (one tab per day)

https://docs.google.com/spreadsheets/d/1njsJamsc3M0tqEjD-_1TnQxYN5XhI0WsWfEtC_8TlIc
One tab per order day, named `YYYY-MM-DD` (store time), oldest on the
left. Add each new day as a new tab at the end in this same file (never a
new file). Easiest: `duplicateSheet` of the latest tab, clear `A15:J` and
the lines table, then write the new rows; or rebuild with the same layout:

- A1 title, A2 one-line description.
- Inputs (blue): B5 USD→EUR rate (0.8979), B6 fallback share (0.33).
- Day total (all formulas): B9 orders `=COUNTA(B15:B..)`, B10 paid €
  `=SUM(F..)`, B11 COGS € `=SUM(G..)`, B12 COGS % `=IF(B10=0,0,B11/B10)`,
  B13 orders above 50% `=COUNTIF(H..,">0.5")`.
- Row 14 header, orders from row 15: Rank `=RANK(H,…)` | Order | Products
  | Fulfillment | Paid (USD) typed | Paid (EUR) `=E*$B$5` | COGS (EUR)
  `=SUMIFS(lines COGS, lines Order, B)` | COGS % `=IF(F=0,0,G/F)` | Gross
  profit `=F-G` | Note (discount code, unpaid upsell, 33% fallback).
  Then `sortRange` the order rows by column H descending.
- Two blank rows, "Order lines", header, then one row per export line:
  Order | Product | Variant | Qty | Selling price (EUR, fallback lines
  only) | Cost per offer (typed, blue; fallback lines `=$B$6*E`) | COGS
  `=D*F` | Source cell.
- COGS % cells: light red at ≥100%, light orange above 50%. Notes on the
  two table headers give the export file and the pricing order.

Tab builder: `scripts/build_day_tab.py` produces the rows and the
formatting batch for a new day tab in this exact layout (see its docstring).

## Output

CSV per line (Order, Fulfillment, Product, Variant, Qty, Pieces, Quote
EUR, COGS EUR, Quote status) in the scratchpad, sent with SendUserFile.
Reply with: total COGS (EUR) of priced lines, priced vs. total lines and
orders, how much came from each sheet, and how much (and which
products) came from the 33%-of-selling-price fallback.

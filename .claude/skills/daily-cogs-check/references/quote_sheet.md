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
- Only rows with column O = TRUE. A product in the sheet but not ticked is
  **not** priced — list it as "in sheet, not ticked" with its quote for
  reference.
- If several ticked rows exist for one product, use the lowest row (the
  latest request) and say so.
- Bundles: a variant ending in `1+1 FREE`, `1 pair +1 pair FREE` or
  containing `2x` ships 2 pieces per unit, so COGS = quote × qty × 2.
- A quote cell with several prices per set size (e.g. FryLite "2-pieceSet
  €18.44 / 4-pieceSet €20.67") — pick the one matching the order's
  variant.
- Products with no row for that store are unpriced. Don't borrow another
  store's quote unless the user asks.
- Count every non-cancelled order, fulfilled or not. In the export, only
  the first line of a multi-line order carries the order fields; the extra
  lines still count.

## Output

CSV per line (Order, Fulfillment, Product, Variant, Qty, Pieces, Quote
EUR, COGS EUR, Quote status) in the scratchpad, sent with SendUserFile.
Reply with: total COGS (EUR) of priced lines, priced vs. total lines and
orders, and the unpriced products split into "not ticked" and "no row".

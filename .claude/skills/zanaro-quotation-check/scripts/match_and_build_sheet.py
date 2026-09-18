#!/usr/bin/env python3
"""
Join best-seller revenue data + parsed supplier quotations + live Shopify
prices into the final quotation-check CSV (ready to hand to Google Drive's
create_file as text/csv, which auto-converts it to a Google Sheet).

Usage:
    python3 match_and_build_sheet.py \\
        --bestsellers bestsellers.json \\
        --parsed-quotations parsed_quotations.json \\
        --shopify-prices shopify_prices.json \\
        --out quotation_check.csv \\
        --top-n 20 --threshold 33 --lookback-days 90

Inputs:
  --bestsellers        JSON array of [title, revenue, orders] from the
                        ShopifyQL best-sellers query (orders may be omitted:
                        [title, revenue] also works).
  --parsed-quotations  Output of parse_quotation_xlsx.py.
  --shopify-prices     JSON object: { "<exact bestseller title>": [price, ...] }.
                        Usually one price per title; a list with >1 entry
                        means multiple live Shopify listings shared that
                        title (duplicates/test listings) -- see
                        references/matching_notes.md for how to resolve
                        those before writing this file (the default here is
                        to take the highest and flag it).

Quotation % = "Lowest quoted 1 pcs price" (xlsx) / Shopify selling price x 100.

This pairs the low end of the supplier's per-piece quote with Shopify's own
minimum variant price. Do NOT average the xlsx's lowest+highest against a
single Shopify price -- quoted variants and Shopify variants aren't the same
population; when a product's variants range from a bare-bones version to a
premium one (e.g. plain vs. motorized), the quote and the price you're
comparing it to can silently belong to different variants and produce a
misleading percentage (in testing this produced a bogus 286% figure). Lowest
quote vs. minimum Shopify price is the one pairing that stays internally
consistent regardless of how wide a product's variant range is.
"""
import argparse
import csv
import json
import sys


def clean_list_field(s, kind="value"):
    if not s:
        return ""
    parts = [p.strip() for p in str(s).split(',') if p.strip()]
    if len(parts) > 2:
        noun = "variant SKUs" if kind == "sku" else "more"
        return f"{parts[0]} (+{len(parts) - 1} {noun})"
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bestsellers", required=True)
    ap.add_argument("--parsed-quotations", required=True)
    ap.add_argument("--shopify-prices", required=True)
    ap.add_argument("--out", default="quotation_check.csv")
    ap.add_argument("--top-n", type=int, default=20, help="How many products to output, ranked by quotation %% descending.")
    ap.add_argument("--threshold", type=float, default=33.0, help="Minimum quotation %% to include (informational; top-n still applies).")
    ap.add_argument("--lookback-days", type=int, default=90)
    ap.add_argument("--checked", type=int, default=None, help="How many best sellers were checked (defaults to len(bestsellers)).")
    args = ap.parse_args()

    bestsellers = json.load(open(args.bestsellers, encoding="utf-8"))
    parsed = json.load(open(args.parsed_quotations, encoding="utf-8"))
    shopify_prices = json.load(open(args.shopify_prices, encoding="utf-8"))

    by_title = parsed["by_title"]
    by_key = parsed["by_brand_key"]

    sys.path.insert(0, __file__.rsplit('/', 1)[0])
    from parse_quotation_xlsx import brand_key, latest_row

    results = []
    unmatched = []

    for entry in bestsellers:
        title = entry[0]
        revenue = float(entry[1])
        orders = entry[2] if len(entry) > 2 else None

        cand = by_title.get(title.strip()) or by_key.get(brand_key(title))
        if not cand:
            unmatched.append(title)
            continue
        xrow = latest_row(cand)

        if title not in shopify_prices:
            unmatched.append(title)
            continue
        prices = shopify_prices[title]
        sell_price = max(prices)
        note = f"multiple Shopify listings found ({prices}); used highest" if len(prices) > 1 else ""

        lowest, highest = xrow["lowest"], xrow["highest"]
        if not lowest or not sell_price:
            unmatched.append(title)
            continue

        pct = lowest / sell_price * 100
        results.append({
            "title": title, "revenue": revenue, "orders": orders,
            "sell_price": sell_price, "lowest": lowest, "highest": highest,
            "pct": round(pct, 1), "sku": xrow["sku"], "supplier": xrow["supplier"], "note": note,
        })

    if unmatched:
        print(f"Warning: {len(unmatched)} best sellers had no usable match "
              f"(no xlsx row, or no Shopify price) and were skipped:", file=sys.stderr)
        for t in unmatched[:15]:
            print(f"  - {t}", file=sys.stderr)
        if len(unmatched) > 15:
            print(f"  ... and {len(unmatched) - 15} more", file=sys.stderr)

    bs_rank = {r["title"]: i + 1 for i, r in enumerate(sorted(results, key=lambda x: -x["revenue"]))}
    ranked = sorted(results, key=lambda r: -r["pct"])
    top = ranked[:args.top_n]

    checked = args.checked or len(bestsellers)
    above_threshold = len([r for r in results if r["pct"] >= args.threshold])

    with open(args.out, "w", newline='', encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "Quotation Rank", f"Bestseller Rank ({args.lookback_days}d revenue)", "Product", "SKU", "Supplier",
            "Selling Price (EUR)", "Quotation - Lowest (EUR)", "Quotation - Highest (EUR)",
            "Quotation %", f"Revenue - Last {args.lookback_days} Days (EUR)", f"Orders - Last {args.lookback_days} Days", "Note",
        ])
        for i, r in enumerate(top, 1):
            w.writerow([
                i, bs_rank[r["title"]], r["title"],
                clean_list_field(r["sku"], kind="sku"), clean_list_field(r["supplier"]),
                r["sell_price"], r["lowest"], r["highest"], f"{r['pct']}%",
                r["revenue"], r["orders"] if r["orders"] is not None else "", r["note"],
            ])
        w.writerow([])
        w.writerow(["Methodology"])
        w.writerow([f"Best sellers: top {checked} products by total_sales (revenue) over the last {args.lookback_days} days, from Shopify analytics."])
        w.writerow(["Quotation %: Lowest quoted 1-pcs supplier price (from the uploaded quotation xlsx) divided by Shopify's current minimum variant selling price, x100."])
        w.writerow(["Products matched between the xlsx and Shopify by product title (some titles differ slightly in promo text; matched on the distinctive product name where an exact title match wasn't found)."])
        w.writerow(["Where a product had multiple live Shopify listings under the same title, the highest-priced listing's price was used as the selling price (flagged in the Note column)."])
        w.writerow([f"Ranked by quotation % descending; showing the top {len(top)} of the {checked} best sellers checked. "
                     f"{above_threshold} of {len(results)} matched products were at or above the {args.threshold}% threshold."])

    print(f"Wrote {args.out}: {len(top)} rows "
          f"({above_threshold}/{len(results)} matched products >= {args.threshold}%, {len(unmatched)} unmatched)")
    print(json.dumps({
        "top": top[:3],
        "matched": len(results),
        "unmatched": len(unmatched),
        "above_threshold": above_threshold,
        "checked": checked,
    }, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

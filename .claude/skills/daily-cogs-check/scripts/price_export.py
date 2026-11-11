#!/usr/bin/env python3
"""
Price a Shopify orders export (CSV) with per-offer costs and rank orders by COGS %.

Usage:
    python3 price_export.py <orders_export.csv> <prices.json> --rate 0.898 --day 2026-11-10 --outdir <dir>

prices.json maps the brand name (text before and including ™, e.g. "WindWall™")
to its cost per offer in EUR and where it came from:
{
  "WindWall™":  {"cost": 23.40, "source": "Zendrop quote sheet (ticked, US €)"},
  "SealGap™":   {"cost": 6.43,  "source": "BER/PMs USA!G803"},
  "GameCozy™":  {"sell_eur": 17.95, "source": "BER/PMs USA!K766"}      # 33% fallback
}
An entry with "sell_eur" (and no "cost") is priced at 33% of that selling price
and flagged as a fallback. Costs are per offer: COGS = cost x Lineitem quantity.

--rate converts the export's USD revenue to EUR (BER/PMs USA tab: $19.99 = €17.95).
Revenue per order = Subtotal (after discounts) - Refunded Amount.

Writes <outdir>/<store>_cogs_<day>.csv (per line) and <outdir>/<store>_cogs_pct_<day>.csv
(per order, highest COGS % first) and prints a summary. Brands missing from
prices.json are listed on stderr and the script exits 1, so nothing is guessed.
"""
import argparse
import collections
import csv
import json
import re
import sys

FALLBACK_SHARE = 0.33


def brand_of(name):
    m = re.search(r"\|\s*([^|]*?™)", name) or re.search(r"([^|·]*?™)", name)
    return (m.group(1) if m else name).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("prices")
    ap.add_argument("--rate", type=float, required=True, help="USD -> EUR")
    ap.add_argument("--day", required=True)
    ap.add_argument("--store", default="nestilia")
    ap.add_argument("--outdir", default=".")
    a = ap.parse_args()

    prices = json.load(open(a.prices, encoding="utf-8"))
    rows = list(csv.DictReader(open(a.export, encoding="utf-8")))

    orders = collections.OrderedDict()
    lines, missing = [], set()
    for r in rows:
        if r["Financial Status"]:
            if r["Cancelled at"]:
                continue
            orders[r["Name"]] = {
                "paid": float(r["Subtotal"] or 0) - float(r["Refunded Amount"] or 0),
                "outstanding": float(r["Outstanding Balance"] or 0),
                "discount": r["Discount Code"],
                "ful": r["Fulfillment Status"],
                "cogs": 0.0, "qty": collections.Counter(), "fallback": False,
            }
        if r["Name"] not in orders:
            continue
        b = brand_of(r["Lineitem name"])
        qty = int(r["Lineitem quantity"])
        p = prices.get(b)
        if p is None:
            missing.add(b)
            continue
        if "cost" in p:
            unit, src = p["cost"], p["source"]
        else:
            unit = round(FALLBACK_SHARE * p["sell_eur"], 4)
            src = f"33% of selling price (€{p['sell_eur']}, {p['source']})"
            orders[r["Name"]]["fallback"] = True
        cogs = round(unit * qty, 2)
        o = orders[r["Name"]]
        o["cogs"] += cogs
        o["qty"][b] += qty
        variant = r["Lineitem name"].split("™", 1)[-1].strip(" -|")
        lines.append([r["Name"], o["ful"], b, variant, qty, round(unit, 2), cogs, src])

    if missing:
        print("MISSING PRICES (add to prices.json): " + ", ".join(sorted(missing)), file=sys.stderr)
        sys.exit(1)

    with open(f"{a.outdir}/{a.store}_cogs_{a.day}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Order", "Fulfillment", "Product", "Variant", "Qty (offers)",
                    "Cost per offer EUR", "COGS EUR", "Source"])
        w.writerows(lines)

    ranked = []
    for k, o in orders.items():
        rev = o["paid"] * a.rate
        pct = o["cogs"] / rev * 100 if rev else float("inf")
        ranked.append([k, ", ".join(f"{n}x {p}" for p, n in o["qty"].items()),
                       round(o["paid"], 2), round(rev, 2), round(o["cogs"], 2), round(pct, 1),
                       round(rev - o["cogs"], 2), o["ful"], o["discount"],
                       "yes" if o["fallback"] else "",
                       round(o["outstanding"], 2) if o["outstanding"] else ""])
    ranked.sort(key=lambda x: -x[5])

    with open(f"{a.outdir}/{a.store}_cogs_pct_{a.day}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Rank", "Order", "Products", "Paid USD", "Paid EUR", "COGS EUR", "COGS %",
                    "Gross profit EUR", "Fulfillment", "Discount code", "Uses 33% fallback",
                    "Outstanding USD"])
        for i, r in enumerate(ranked, 1):
            w.writerow([i] + r)

    tot_c = sum(r[4] for r in ranked)
    tot_r = sum(r[3] for r in ranked)
    print(f"{a.store} {a.day}: {len(ranked)} orders, {len(lines)} lines | paid ${sum(r[2] for r in ranked):.2f} "
          f"= €{tot_r:.2f} | COGS €{tot_c:.2f} | COGS % {tot_c / tot_r * 100:.1f}% | "
          f">50%: {sum(r[5] > 50 for r in ranked)} | >100%: {sum(r[5] > 100 for r in ranked)}")
    for i, r in enumerate(ranked, 1):
        flags = " ".join(x for x in [r[8] and f"code:{r[8]}", r[9] and "33%", r[10] != "" and f"outstanding ${r[10]}"] if x)
        print(f"{i:>2} {r[0]} {r[5]:>6.1f}%  COGS €{r[4]:>6.2f} / paid €{r[3]:>6.2f}  {r[1]}  {flags}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Total one day's COGS per store from Zendrop get_orders pages.

Usage:
    python3 total_cogs.py orders_<store>_<day>.json [...] [--out cogs.json] [--tsv cogs.tsv]
                          [--previous '{"Zanaro Berlin": 512.30}']

Each input file:
{
  "store_id": 3243654, "store_name": "Zanaro Berlin", "day": "2026-11-10",
  "orders": [ <order objects exactly as get_orders returns them> ],
  "estimates": [ {"order_id": 1, "order_number": "#BC1", "cost": 3.2, "source": "quote sheet"} ]   # optional
}

In get_orders results an order's "total" is its Zendrop cost (product +
shipping, USD). Canceled orders are excluded. Orders with total 0 are
reported as "without COGS".

--previous: JSON map store name -> previous logged day's actual COGS, for the
day-over-day check.
"""
import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict

MONEY = lambda x: round(float(x or 0), 2)


def summarise(data, previous):
    orders = data.get("orders", [])
    seen, dupes = set(), 0
    uniq = []
    for o in orders:  # pages may overlap if orders arrived while paging
        if o["id"] in seen:
            dupes += 1
            continue
        seen.add(o["id"])
        uniq.append(o)

    canceled = [o for o in uniq if o.get("status") == "Canceled"]
    live = [o for o in uniq if o.get("status") != "Canceled"]
    costed = [o for o in live if MONEY(o.get("total")) > 0]
    missing = [o for o in live if MONEY(o.get("total")) <= 0]

    actual = MONEY(sum(MONEY(o["total"]) for o in costed))
    by_status = defaultdict(lambda: {"orders": 0, "cogs": 0.0})
    for o in live:
        s = by_status[o.get("status", "?")]
        s["orders"] += 1
        s["cogs"] = MONEY(s["cogs"] + MONEY(o.get("total")))

    est = data.get("estimates") or []
    est_ids = {e.get("order_id") for e in est}
    est_total = MONEY(sum(MONEY(e.get("cost")) for e in est)) if est else None

    warnings = []
    if dupes:
        warnings.append(f"{dupes} duplicate order(s) across pages ignored")
    costs = [MONEY(o["total"]) for o in costed]
    if len(costs) >= 3:
        med = statistics.median(costs)
        for o in costed:
            if MONEY(o["total"]) > 3 * med:
                warnings.append(
                    f"{o.get('order_number')} cost {MONEY(o['total'])} is >3x the median ({MONEY(med)})"
                )
    if live and len(missing) / len(live) > 0.25:
        warnings.append(
            f"{len(missing)}/{len(live)} orders ({len(missing) / len(live):.0%}) have no COGS in Zendrop"
        )
    prev = previous.get(data.get("store_name"))
    if prev:
        change = (actual - prev) / prev
        if abs(change) > 0.5:
            warnings.append(f"actual COGS {actual} vs previous day {prev} ({change:+.0%})")

    return {
        "store_id": data.get("store_id"),
        "store_name": data.get("store_name"),
        "day": data.get("day"),
        "orders": len(live),
        "orders_with_cogs": len(costed),
        "orders_without_cogs": len(missing),
        "canceled": len(canceled),
        "cogs_actual": actual,
        "avg_cogs_per_order": MONEY(actual / len(costed)) if costed else 0,
        "cogs_estimated_missing": est_total,
        "cogs_total_incl_estimates": MONEY(actual + (est_total or 0)) if est else None,
        "by_status": dict(by_status),
        "missing_by_status": dict(Counter(o.get("status") for o in missing)),
        "missing_orders": [
            {
                "order_id": o["id"],
                "order_number": o.get("order_number"),
                "status": o.get("status"),
                "issues": o.get("issues", []),
                "estimated": o["id"] in est_ids,
            }
            for o in missing
        ],
        "warnings": warnings,
    }


def tsv_row(s, notes=""):
    cells = [
        s["day"], s["store_name"], s["orders"], s["orders_with_cogs"], s["orders_without_cogs"],
        s["cogs_actual"], s["avg_cogs_per_order"],
        "" if s["cogs_estimated_missing"] is None else s["cogs_estimated_missing"],
        "" if s["cogs_total_incl_estimates"] is None else s["cogs_total_incl_estimates"],
        s["canceled"], notes,
    ]
    return "\t".join(str(c) for c in cells)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", default="cogs.json")
    ap.add_argument("--tsv")
    ap.add_argument("--previous", default="{}")
    a = ap.parse_args()
    previous = json.loads(a.previous)

    stores = []
    for f in a.files:
        with open(f) as fh:
            stores.append(summarise(json.load(fh), previous))

    days = sorted({s["day"] for s in stores})
    if len(days) > 1:
        print(f"WARNING: files cover several days {days}; totals are per file", file=sys.stderr)

    any_est = any(s["cogs_estimated_missing"] is not None for s in stores)
    allrow = {
        "store_name": "ALL",
        "day": days[0] if len(days) == 1 else ",".join(days),
        "orders": sum(s["orders"] for s in stores),
        "orders_with_cogs": sum(s["orders_with_cogs"] for s in stores),
        "orders_without_cogs": sum(s["orders_without_cogs"] for s in stores),
        "canceled": sum(s["canceled"] for s in stores),
        "cogs_actual": MONEY(sum(s["cogs_actual"] for s in stores)),
        "cogs_estimated_missing": MONEY(sum(s["cogs_estimated_missing"] or 0 for s in stores)) if any_est else None,
    }
    allrow["avg_cogs_per_order"] = (
        MONEY(allrow["cogs_actual"] / allrow["orders_with_cogs"]) if allrow["orders_with_cogs"] else 0
    )
    allrow["cogs_total_incl_estimates"] = (
        MONEY(allrow["cogs_actual"] + allrow["cogs_estimated_missing"]) if any_est else None
    )

    with open(a.out, "w") as fh:
        json.dump({"stores": stores, "all": allrow}, fh, indent=2, ensure_ascii=False)

    if a.tsv:
        with open(a.tsv, "w") as fh:
            for s in stores:
                fh.write(tsv_row(s, "; ".join(s["warnings"])) + "\n")
            fh.write(tsv_row(allrow) + "\n")

    print(f"COGS for {allrow['day']} (USD, Zendrop cost, canceled excluded)")
    for s in stores + [allrow]:
        line = (
            f"  {s['store_name']:<15} orders {s['orders']:>4} | with COGS {s['orders_with_cogs']:>4} | "
            f"without {s['orders_without_cogs']:>3} | actual {s['cogs_actual']:>10.2f} | "
            f"avg {s['avg_cogs_per_order']:>6.2f}"
        )
        if s["cogs_estimated_missing"] is not None:
            line += f" | est. missing {s['cogs_estimated_missing']:.2f} | total {s['cogs_total_incl_estimates']:.2f}"
        print(line)
    for s in stores:
        if s["missing_by_status"]:
            print(f"  {s['store_name']}: without COGS by status {s['missing_by_status']}")
        for w in s["warnings"]:
            print(f"  WARNING {s['store_name']}: {w}")


if __name__ == "__main__":
    main()

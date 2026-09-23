#!/usr/bin/env python3
"""Cross-check Zendrop order totals against the Zendrop_quote_request sheet.

Usage:
  check_quotes.py --quotes QUOTES.txt --orders ORDERS.csv --items ITEMS.json \
                  --out MISMATCHES.csv [--checked-on YYYY-MM-DD] [--tolerance 0.02]
  check_quotes.py --quotes QUOTES.txt --dump-quotes     # print the parsed quote table

QUOTES.txt is the `fileContent` string that Google Drive `read_file_content`
returns for the quote sheet: rows flattened into one line, cells comma-separated,
rows separated by a single space, markdown-escaped (\\! \\_ \\& ...).

ORDERS.csv is the Zendrop export (needs `Order Number`, `Total (USD)`, `Country`).
If it also carries `Product`, `Variant` and `Quantity` columns, --items is optional.

ITEMS.json maps order number -> list of line items from Shopify:
  {"#BC126162": [{"title": "...", "variant": "...", "qty": 1}, ...], ...}
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict

COUNTRIES = ("DE", "AT", "CH", "NL", "BE", "FR")


# ---------- quote sheet parsing ----------

def unescape(s):
    return re.sub(r"\\(.)", r"\1", s)


def split_rows(text):
    """Figure out the column count from the header, then tokenize."""
    # Try candidate widths; keep the one where every row but the last has that many
    # cells and row 2 is the "Product Name,..." header.
    body = text.strip()
    for ncols in range(20, 60):
        rows = _tokenize_width(body, ncols)
        if rows and all(len(r) == ncols for r in rows[:-1]) and len(rows) > 3 \
                and any(unescape(c).strip() == "Product Name" for c in rows[1]):
            return [[unescape(c).strip() for c in r] for r in rows]
    raise SystemExit("Could not work out the quote sheet layout (no 'Product Name' header row).")


def _tokenize_width(text, ncols):
    rows, cells, cur, in_q, i, n = [], [], [], False, 0, len(text)
    while i < n:
        c = text[i]
        if in_q:
            if c == '"':
                if i + 1 < n and text[i + 1] == '"':
                    cur.append('"'); i += 2; continue
                in_q = False
            else:
                cur.append(c)
        elif c == '"' and not cur:
            in_q = True
        elif c == ",":
            cells.append("".join(cur)); cur = []
        elif c == " " and len(cells) == ncols - 1:
            cells.append("".join(cur)); cur = []
            rows.append(cells); cells = []
        else:
            cur.append(c)
        i += 1
    cells.append("".join(cur))
    rows.append(cells)
    return rows


def col_letter(idx):
    s, idx = "", idx + 1
    while idx:
        idx, r = divmod(idx - 1, 26)
        s = chr(65 + r) + s
    return s


def money(v):
    v = (v or "").strip()
    if not v:
        return None
    v = re.sub(r"[^\d,.\-]", "", v)
    if "," in v and "." not in v:
        v = v.replace(",", ".")
    v = v.replace(",", "")
    try:
        return round(float(v), 2)
    except ValueError:
        return None


def brand(title):
    """'50% RABATT NUR HEUTE | SteamPress™ - Dampfglätter' -> 'SteamPress'."""
    t = unescape(title or "")
    if "™" in t:
        before = t.split("™")[0]
        before = re.split(r"[|·:]", before)[-1]
        return before.strip().split()[-1] if before.strip() else ""
    # no ™: strip promo prefix before '|' and take the first word
    t = re.split(r"[|·]", t)[-1] if "|" in t or "·" in t else t
    t = re.sub(r"\(.*?\)", "", t).strip()
    return t.split()[0] if t.split() else ""


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def parse_quotes(text):
    rows = split_rows(text)
    head0, head1, head2 = rows[0], rows[1], rows[2]
    zq = next((i for i, c in enumerate(head0) if c.lower().startswith("zendrop quotes")), None)
    if zq is None:
        raise SystemExit("Quote sheet: 'Zendrop Quotes' header not found - layout changed?")
    usd_col = {}
    for i in range(zq, len(head1)):
        code = head1[i].upper()
        if code in COUNTRIES and code not in usd_col:
            # EUR in this column, USD in the next one
            if i + 1 < len(head2) and "USD" in head2[i + 1]:
                usd_col[code] = i + 1
    if "DE" not in usd_col:
        raise SystemExit("Quote sheet: DE USD column not found - layout changed?")
    cost_col = next((i for i, c in enumerate(head0) if c.lower().startswith("product cost")), None)
    if cost_col is None:
        raise SystemExit("Quote sheet: 'Product Cost ($)' header (column O) not found - layout changed?")
    detail_cols = [i for i, c in enumerate(head1) if c.startswith("Product Details") or
                   c.startswith("Product Quality")]

    products = defaultdict(list)  # norm(brand) -> list of variant rows
    names = {}
    last = None
    for r in rows[3:]:
        name, store = r[0], r[1]
        quotes = {c: money(r[i]) for c, i in usd_col.items() if i < len(r)}
        label = " ".join(r[i] for i in detail_cols if r[i] and r[i] not in ("TRUE", "FALSE"))
        # a cost written in EUR can't be combined with USD quotes
        cost = None if "€" in r[cost_col] else money(r[cost_col])
        if name:
            b = brand(name)
            if not b:
                last = None
                continue
            last = norm(b)
            names.setdefault(last, b)
            products[last].append({"label": label, "store": store, "quotes": quotes, "cost": cost,
                                   "title": name})
        elif last and any(v is not None for v in quotes.values()):
            store = store or products[last][-1]["store"]  # variant rows often leave it blank
            products[last].append({"label": label, "store": store, "quotes": quotes, "cost": cost,
                                   "title": ""})
    return products, names, usd_col, cost_col


# ---------- matching ----------

def first_int(s):
    m = re.search(r"\d+", s or "")
    return m.group() if m else None


def pick_row(rows, variant):
    """Choose the quote row for a variant. Returns (row, note)."""
    zrows = [r for r in rows if norm(r["store"]).startswith(("zanaro", "zabaro"))] or rows
    if len(zrows) == 1:
        return zrows[0], ""
    v = norm(variant)
    for r in zrows:
        lab = norm(r["label"])
        if lab and v and (lab in v or v in lab):
            return r, ""
    vi = first_int(variant)
    if vi:
        hits = [r for r in zrows if first_int(r["label"]) == vi]
        if len(hits) == 1:
            return hits[0], ""
    return zrows[0], f"variant '{variant}' not matched to a quote row; used '{zrows[0]['label'] or 'first row'}'"


def quoted_price(priced, notes):
    """Expected Zendrop charge for an order.

    One unit: the country quote (column Q for DE). More than one unit: the first unit at the
    full quote, every extra unit at product cost (column O), i.e. O * qty + (Q - O). Across
    different products/variants every unit is costed at O and the per-order part (Q - O) is
    added once, using the largest one.
    """
    if not priced:
        return None
    units = sum(qty for _, _, qty, _ in priced)
    if units == 1:
        return round(priced[0][0], 2)
    missing = sorted({n for _, cost, _, n in priced if cost is None})
    if missing:
        notes.append("no USD product cost (column O) for " + ", ".join(missing) +
                     "; used quote x quantity")
        return round(sum(q * qty for q, _, qty, _ in priced), 2)
    return round(sum(cost * qty for _, cost, qty, _ in priced) +
                 max(q - cost for q, cost, _, _ in priced), 2)


def load_orders(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def pick(d, *keys):
    for k in d:
        if k and k.strip().lower() in keys:
            return d[k]
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quotes", required=True)
    ap.add_argument("--orders")
    ap.add_argument("--items")
    ap.add_argument("--out")
    ap.add_argument("--checked-on", default="")
    ap.add_argument("--tolerance", type=float, default=0.02)
    ap.add_argument("--dump-quotes", action="store_true")
    a = ap.parse_args()

    with open(a.quotes, encoding="utf-8") as f:
        products, names, usd_col, cost_col = parse_quotes(f.read())

    print("USD quote columns:", ", ".join(f"{c}={col_letter(i)}" for c, i in usd_col.items()),
          f"| product cost = {col_letter(cost_col)}")
    if a.dump_quotes:
        for k, rows in products.items():
            for r in rows:
                print(f"{names[k]:<16} {r['store']:<8} {r['label'][:30]:<30} cost:{r['cost']} " +
                      " ".join(f"{c}:{r['quotes'].get(c)}" for c in usd_col))
        return

    orders = load_orders(a.orders)
    items = {}
    if a.items:
        with open(a.items, encoding="utf-8") as f:
            items = {k.lstrip("#").upper(): v for k, v in json.load(f).items()}

    out_rows, stats = [], defaultdict(int)
    for o in orders:
        num = pick(o, "order number", "order #", "order").strip()
        total = money(pick(o, "total (usd)", "order total charged to customer (usd)", "total"))
        country = pick(o, "country", "destination country").strip().upper()
        date = pick(o, "date (utc)", "order date (utc)", "date")[:10]
        stats["orders"] += 1

        lines = items.get(num.lstrip("#").upper())
        if lines is None and pick(o, "product"):
            lines = [{"title": pick(o, "product"), "variant": pick(o, "variant"),
                      "qty": int(float(pick(o, "quantity") or 1))}]
        if lines is None:
            lines = []

        notes, labels, priced, unknown, no_quote = [], [], [], 0, False
        for li in lines:
            b = norm(brand(li.get("title", "")))
            qty = int(li.get("qty") or 1)
            if b not in products:
                unknown += 1
                labels.append(f"{brand(li.get('title', '')) or li.get('title', '')} (not in quote sheet)")
                continue
            row, note = pick_row(products[b], li.get("variant", ""))
            if note:
                notes.append(note)
            q = row["quotes"].get(country)
            label = names[b] + (f" ({li.get('variant')})" if li.get("variant") else "")
            # per-line quantity only matters in the name when the order has several lines
            labels.append(label + (f" x{qty}" if qty != 1 and len(lines) > 1 else ""))
            if q is None:
                notes.append(f"no {country} quote for {names[b]}")
                no_quote = True
                continue
            priced.append((q, row["cost"], qty, names[b]))

        expected = None if no_quote else quoted_price(priced, notes)

        reason = None
        if not lines:
            reason = "no line items found for this order"
        elif unknown == len(lines):
            reason = "product not in quote sheet"
        elif expected is None:
            reason = "no quote for destination country"
        else:
            expected = round(expected, 2)
            if total is None or abs(total - expected) > a.tolerance:
                reason = "price mismatch"
                if unknown:
                    notes.append("some items not in quote sheet")

        if reason:
            stats[reason] += 1
            diff = round(total - expected, 2) if (total is not None and isinstance(expected, float)) else ""
            out_rows.append({
                "Order #": num,
                "Product Name": " + ".join(labels) or "(unknown)",
                "Quantity": sum(int(li.get("qty") or 1) for li in lines) if lines else "",
                "Quoted Price (USD)": f"{expected:.2f}" if isinstance(expected, float) else "",
                "Total Price (CSV, USD)": f"{total:.2f}" if total is not None else "",
                "Difference (USD)": f"{diff:+.2f}" if diff != "" else "",
                "Country": country,
                "Order Date": date,
                "Issue": reason + ("; " + "; ".join(dict.fromkeys(notes)) if notes else ""),
                "Checked On": a.checked_on,
            })
        else:
            stats["match"] += 1

    fields = ["Order #", "Product Name", "Quantity", "Quoted Price (USD)", "Total Price (CSV, USD)",
              "Difference (USD)", "Country", "Order Date", "Issue", "Checked On"]
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)
    print(json.dumps(stats, indent=1))
    print(f"wrote {len(out_rows)} rows to {a.out}")


if __name__ == "__main__":
    sys.exit(main())

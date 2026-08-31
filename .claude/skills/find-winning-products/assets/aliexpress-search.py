"""
AliExpress DE/EUR search-page scraper for supplier sourcing (working method found 2026-08-31).

Usage:
    python3 aliexpress-search.py "<query>" <output.html>

Fetches https://de.aliexpress.com/w/wholesale-<query>.html?g=y through the
session's HTTPS proxy, forcing the DE/EUR/English locale via a cookie sent
on every request (setting it once does not persist into the cookie jar —
it must be passed with -b on each call). Prints the parsed product list
(productId, title, original/sale price + currency, orders sold, star
rating) sorted as returned by AliExpress.

Notes for the next run:
- Re-verify this still works before relying on it — the anti-bot layer
  that blocked this earlier in the session may reopen at any time. If you
  get a punish/captcha page (grep the output for "bxpunish" or
  "_____tmd_____"), fall back to the ledger's documented `pending` cell
  and DO NOT invent a price.
- The product grid is embedded server-side in a JS object literal assigned
  to `window._dida_config_._init_data_`. There are multiple decoy
  occurrences of the string "_init_data_" earlier in the page (minified
  bootstrap/hydration code) — this script does not need to find that
  object at all, since it regexes each product's fields directly out of a
  ~3000-char window following its "productId" match, rather than parsing
  the (non-JSON, unquoted-key) object as a whole.
- ALWAYS re-filter results by a category keyword before picking "cheapest"
  — AliExpress's own relevance ranking surfaces off-target matches (e.g. a
  car-shaped novelty alarm clock search returns generic desk clocks; a
  quit-smoking necklace search returns generic fashion chains). Filter the
  title list yourself before sorting by price.
- Per SKILL.md Rule 10, prefer the cheapest item that clears >=200 sold AND
  >=4.5 stars where one exists (tag INDEX-OK); if none clears both, name
  the cheapest genuine same-product match and tag it "no qualifying
  supplier" rather than silently downgrading the floor.
- This confirms the item is live in the DE/EUR search index with a real
  price/rating/orders count — it does NOT confirm the item page itself
  loads. That would require opening /item/<id>.html directly and reading
  the body (upgrades the tag to LOAD-TESTED).
"""
import subprocess, sys, re, urllib.parse, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
COOKIE_JAR = "ae_cookies_eur.txt"
PROXY = os.environ.get("HTTPS_PROXY")
CACERT = "/root/.ccr/ca-bundle.crt"

# Forces EUR pricing, English titles, ship-to-Germany. Must be sent on
# EVERY request via -b, not just set once — it does not get persisted
# into the curl cookie jar from a plain outgoing Cookie header.
LOCALE_COOKIE = "aep_usuc_f=site=deu&c_tp=EUR&region=DE&b_locale=en_US"


def curl(url, outfile):
    cmd = [
        "curl", "-x", PROXY, "--cacert", CACERT, "-sL",
        "-c", COOKIE_JAR, "-b", COOKIE_JAR,
        "-b", LOCALE_COOKIE,
        "-A", UA,
        "-H", "Accept-Language: en-US,en;q=0.9",
        url, "-o", outfile, "-w", "%{http_code} %{size_download}",
        "--max-time", "40",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout, r.stderr


def extract_products(htmlfile):
    with open(htmlfile, encoding="utf-8", errors="replace") as f:
        html = f.read()
    if "bxpunish" in html or "_____tmd_____" in html:
        print("WARNING: anti-bot punish/captcha page detected — results below are unreliable or empty.", file=sys.stderr)
    products = []
    for m in re.finditer(r'"productId":"(\d+)"', html):
        pid = m.group(1)
        window = html[m.start():m.start() + 3000]
        title_m = re.search(r'"displayTitle":"(.*?)(?<!\\)"', window)
        price_m = re.search(r'"originalPrice":\{[^}]*?"currencyCode":"(\w+)","minPrice":([\d.]+)', window)
        sale_m = re.search(r'"salePrice":\{[^}]*?"currencyCode":"(\w+)","minPrice":([\d.]+)', window)
        trade_m = re.search(r'"tradeDesc":"([^"]*)"', window)
        rating_m = re.search(r'"starRating":([\d.]+)', window)
        products.append({
            "productId": pid,
            "title": title_m.group(1) if title_m else None,
            "orig_currency": price_m.group(1) if price_m else None,
            "orig_price": float(price_m.group(2)) if price_m else None,
            "sale_currency": sale_m.group(1) if sale_m else None,
            "sale_price": float(sale_m.group(2)) if sale_m else None,
            "trade": trade_m.group(1) if trade_m else None,
            "rating": float(rating_m.group(1)) if rating_m else None,
        })
    return products


def sold_num(trade):
    if not trade:
        return 0
    m = re.search(r'([\d,]+)\+?\s*sold', trade)
    return int(m.group(1).replace(',', '')) if m else 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    query = sys.argv[1]
    outname = sys.argv[2]
    url = "https://de.aliexpress.com/w/wholesale-" + urllib.parse.quote(query.replace(" ", "-")) + ".html?g=y"
    out, err = curl(url, outname)
    print("fetch:", out, err[:200])
    prods = extract_products(outname)
    for p in prods:
        p["sold"] = sold_num(p["trade"])
    print(f"found {len(prods)} products")
    prods.sort(key=lambda p: p["sale_price"] or 9999)
    for p in prods[:20]:
        print(f"  {p['productId']}  €{p['sale_price']}  {p['trade']}  {p['rating']}*  {p['title']}")

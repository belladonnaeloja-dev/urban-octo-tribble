# Find Winning Products 2.0 — Ledger

Persistent anti-repeat state for the `find-winning-products-2.0` skill (see
[discovery-engine.md §29, §31–§36](references/discovery-engine.md)). Read this file in full
before every run. Update it at the end of every run — this step is not optional; skipping it
means tomorrow's run repeats today's products.

**The live spreadsheet is the master database (§32).** If it disagrees with this ledger, the
spreadsheet wins. This file is the local backstop for when the spreadsheet is unavailable or
to speed up dedupe without re-reading the whole sheet every time.

## IMPORTANT — this skill's own ledger is behind the real spreadsheet (§32 applies)

The canonical spreadsheet (`Winning-Products-MASTER`,
https://docs.google.com/spreadsheets/d/1ha9uILlG-VetpFMqHCkP3F9P_o7k4nUrZS-zAk3pZJ4/edit,
tab "Winning Products") already held **338 products across ~35 prior runs** (2026-07-26
through 2026-09-07) before this skill folder's first run on 2026-09-08 — including a run
dated 2026-09-07 explicitly labeled "FIRST find-winning-products-2.0 run" that this skill
folder has no local record of (no prior `search-history.md`/`ledger.md` entries existed
before today). **The spreadsheet is the source of truth (§32); this file is only a local
cache and is known-incomplete** — see "Known visibility gaps" below.

## SEEN_PRODUCT_IDS

WinningHunter IDs delivered or evaluated by *this skill folder's* runs. One per line:
`<id> — <product name> — <date first seen>`.

- `687312375292` / `687308741482` — SohoBloo OrthoAlign 3-in-1 Cervical Traction Pillow — 2026-09-08
- `1941289416511882` — Corecare Instant Posture Corrector — 2026-09-08
- `1298270225287457` — ReabTec KniTec V2 Compression Sleeve — 2026-09-08
- `1732319419019989289` (TikTok) — NIRACL Car Driving Neck Pillow — 2026-09-08

## SEEN_DOMAINS

Store domains evaluated by this skill's runs. One per line: `<domain> — <status> — <date>`.

- `shopsohobloo.com` — delivered (new product; domain already in spreadsheet under a
  different product, SkinRestore cream, 2026-08-03 — dedupe is store+PRODUCT, so this is a
  legitimate new find) — 2026-09-08
- `corecareshop.com` — watch (sold out at verification) — 2026-09-08
- `reabtec.com` — watch (sold out at verification) — 2026-09-08
- `nhimapparel.com` — rejected (no verifiable single-product page — its highest-repin video
  ad links only to the store homepage, not a product; see §40 rule 4) — 2026-09-08
- Rejected this run for brand/marketplace/established-brand reasons (not tracked per-domain,
  just noted): amazon.com, temu.com, target.com, homedepot.com, victoriassecret.com,
  skims.com, shein.com, meshki.us (established), homary.com, kay.com

## SEEN_PRODUCT_CONCEPTS

- Cervical/neck traction pillow — SohoBloo OrthoAlign — 2026-09-08
- Wearable posture corrector — Corecare — 2026-09-08 (distinct mechanism from a posture
  *cushion*; if a posture-cushion concept surfaces later it is NOT automatically the same
  concept — use judgment per §33)
- Knee/leg compression sleeve — ReabTec KniTec — 2026-09-08
- Car-seat neck/lumbar support pillow — NIRACL — 2026-09-08

## DELIVERED_PRODUCTS

## 2026-09-08 (run 2 for the spreadsheet's history; run 1 tracked locally by this skill
folder — see visibility-gap note above)
- SohoBloo OrthoAlign 3-in-1 Cervical Traction Pillow — shopsohobloo.com — 687312375292 —
  Healthcare — US — SOURCE: Pinterest — TEST NOW
- Corecare Instant Posture Corrector — corecareshop.com — 1941289416511882 — Healthcare —
  US — SOURCE: Meta — WATCH (sold out)
- ReabTec KniTec V2 Compression Sleeve — reabtec.com — 1298270225287457 — Healthcare — US
  (GBP-priced store) — SOURCE: Meta — WATCH (sold out)
- NIRACL Car Driving Neck Pillow — TikTok Shop — 1732319419019989289 — Car Accessories — US
  — SOURCE: TikTok — WATCH (margin risk, price under €25 floor)

## REJECTED_PRODUCTS

| Product | Domain | Rejection reason | Rejected on | Recheck after |
|---|---|---|---|---|
| NHIM "We Have Our Being" video ad | nhimapparel.com | No verifiable single-product page (ad links to homepage, not a product) despite strong metrics (1,567 repins, 11 ads, 523 days) | 2026-09-08 | Recheck if a future NHIM ad links to a specific product page |
| Various dresses/underwear/lighting video-less candidates | many (see search-history.md) | Failed video-only gate (image media_type) | 2026-09-08 | n/a — different creative would need to run |
| SKIMS Shapewear, Victoria's Secret, SHEIN items | skims.com, victoriassecret.com, us.shein.com | Established brand / marketplace, not dropship-sourceable | 2026-09-08 | Permanent |

## RECHECK_QUEUE

| Product | Domain | Reason held back | Recheck after / season |
|---|---|---|---|
| Corecare Instant Posture Corrector | corecareshop.com | All variants sold out at verification (2026-09-08); pricing display also glitched (sale price shown higher than regular) | ~2–3 weeks — recheck stock and pricing fix |
| ReabTec KniTec V2 Compression Sleeve | reabtec.com | All variants sold out at verification (2026-09-08), despite being a 359-day survivor with €50,697 EU adspend — very strong underlying signal | ~2–3 weeks — recheck stock; strong TEST NOW candidate if restocked |

## EMERGING WINNER WATCHLIST

| Product | Domain | Repins | Ad count | Days running | First noticed |
|---|---|---|---|---|---|
| NIRACL Car Driving Neck Pillow (TikTok) | TikTok Shop | n/a (TikTok metrics: 8,381 lifetime units, $141.6k lifetime revenue) | n/a | Launched 2026-04-08 | 2026-09-08 — watch for a Pinterest-side sighting via reverse search (§38) |

## Archive

Entries older than 120 days move here (names + domains only) so the file stays cheap to read
while still blocking repeats.

(none yet)

## Known visibility gaps (fix before the next run relies on this ledger alone)

- **Full 338-row spreadsheet history not locally cached.** `Google_Drive.read_file_content`
  on the canonical sheet returns a text export that gets cut off around row ~78 (dated
  2026-08-04) out of 338 total rows, plus a separate "Winners Library" table. The 2026-09-07
  run's exact 10 rows were only visible as a *summary* in the sheet's subtitle cell (product
  names, tiers, verdicts) — not the full row detail (exact WinningHunter IDs, domains,
  metrics). This run's dedupe checks relied on: (a) the visible ~78 rows, (b) the
  2026-09-07 summary's named products, and (c) reading each new candidate's own domain/name
  against both. **This is not a substitute for full dedupe** — a future run should either
  fix `Autosheet` billing (see below) and use its agent to pull a compact "all products +
  domains" export, or paginate `Google_Drive.read_file_content` / find an equivalent ranged
  read, before trusting this ledger's SEEN_* lists as complete.
- **Autosheet (the Google Sheets write connector) returned
  `api-billing-free-trial-ended`** on 2026-09-08 and was still blocked on retry — no working
  path via Autosheet this run.
- **UPDATE 2026-09-08, same run:** the user supplied a Google service-account JSON key
  (`claude-sheets@intense-palace-505314-b5.iam.gserviceaccount.com`) with edit access to the
  canonical sheet. Since this sandbox's `cryptography`/`PyJWT` Python packages have a broken
  Rust backend (`ModuleNotFoundError: No module named '_cffi_backend'`, panics on import),
  the JWT for the OAuth2 service-account flow was signed manually with the `openssl` CLI
  (`openssl dgst -sha256 -sign`) instead of a Python JWT library. This worked end-to-end:
  minted an access token, confirmed read access, wrote the 4 rows to `A343:AH346` via
  `spreadsheets.values.update` (`valueInputOption=USER_ENTERED`), applied the date format and
  per-row verdict-color fills via `spreadsheets.batchUpdate`, updated the row-2 subtitle, and
  verified every write by reading it back. **The spreadsheet now has 342 products; rows
  343-346 are this run's 4 new products.** The key material was deleted from the local
  scratchpad immediately after use and never committed to this repo. **The user should still
  rotate this key** (it was pasted in plaintext into the chat transcript, which is a
  reasonable thing to rotate as routine hygiene regardless of how carefully it was handled
  afterward). If the key is still valid on a future run, the same approach (openssl-signed
  JWT → Sheets API v4) can be reused directly instead of going through Autosheet.

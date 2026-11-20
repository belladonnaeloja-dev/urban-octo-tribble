# Session handoff – product pricing & competitor research (12–20 Nov 2026)

Paste this whole file into a new Claude chat as context. It summarises what was done, the data sources, the method, and every recommendation so far.

---

## 1. Stores

| Store | Market | Currency | BER/PMs tab |
|---|---|---|---|
| nestilia.com | US | $ | USA |
| zanaroberlin.com (Zanaro Berlin) | Germany | € | DE |
| solundi.com | Netherlands/Belgium | € | NL |
| modlia.fr | France | € | FR |

Product pages: `https://<store>/products/<handle>`. Live price and variant data: add `.json` to the URL.

## 2. Key Google Sheets

| File | ID / link | What it is |
|---|---|---|
| **BER/PMs** (main cost sheet, owned by a teammate) | `1MRyyd2gDbwVOstNetjJsGEF--rVAKcAoYyf6dAVmm3A` | Tabs DE, NL, FR, USA (+ SE, Juleani, Wham, TEMPLATE). One row per product/variant with the agent (SP) cost block and the Zendrop cost block. |
| BER/PMs – Changes log, all tabs (11–12 Nov) | `1On9mKUMfG0okMFhj1U2VQ0znWjNgNhtpW1oKZxuFObg` | Diff of BER/PMs, 11 Nov 22:08 → 12 Nov 23:19 (Manila time). Rows 33–35 of USA and row 134 of DE added for the post-23:05 changes. |
| BER/PMs – Top 20 highest quote price per tab (17 Nov) | https://docs.google.com/spreadsheets/d/1I28-OOQWoyskcyeo_WuH3Ieja0sHEAGG1dcvcvMAsBA/edit | Snapshot of the 20 worst quote prices per tab (SP or Zendrop, whichever is higher). Red ≥100%, yellow ≥70%. |

### BER/PMs column layout (row 2 = headers)
- **DE:** I = Agent €, J = QP + 2,60, K = Quote price, L = Selling price · D = Service Point tick, E = Zendrop tick · V = Zendrop $ tax incl., X = Zendrop €, Y = Zendrop quote %.
- **NL:** G = Agent €, H = QP + 2,60, I = Quote, J = Selling · Z = Zendrop $, AB = Zendrop €, AC = Zendrop quote.
- **FR:** G = Agent €, H = QP + 2,60, I = Quote, J = Selling · Q = Zendrop $, S = Zendrop €, T = Zendrop quote.
- **USA:** G = Agent €, H = QP + 2,60, I = Quote, J = Selling $, L = Selling €; U = Zendrop $, W = Zendrop €, X = Zendrop quote. Quote prices are calculated on the € value of the $ price.

## 3. Method used

- **Quote price** = product cost ÷ selling price. For SP the cost is "QP + 2,60" (agent € + €2.60). For Zendrop it's the Zendrop € price.
- **Targets:** ≤ 40% is healthy, 40–50% is OK, > 55% is thin, ≥ 100% loses money.
- **Market check:** Meta ads via WinningHunter (`search_facebook_ads`, `find_similar_stores_by_image`), competitor Shopify `.json` prices, plus prices of the same product in my other stores.
- **Compare-at:** set it to about 2× the selling price so the "50% OFF / -50 % / 50% RABATT" banners stay true.
- Always check which supplier (SP or Zendrop) is cheaper **in the live sheet**. Agent prices were changed several times during the week (DrapeEase, SurpriseDays, TrueAngle, WarmWork, WindowGlow, SnugWear).

## 4. Pricing recommendations given (latest first per store)

### Modlia (FR)
| Product | Was | Recommended | Supplier / cost | Quote at new price | Compare-at | Notes |
|---|---|---|---|---|---|---|
| SurpriseDays (advent calendar, 2 × 24 pcs) | €27.99 | **€44.99** (€39.99 ok) | **SP** €18.90 + 2.60 = €21.50 (cheaper than ZD €24.04) | 48% | €89.99 | FR competitors sell ONE calendar for €27–€30 (Belle Enfance €26.95, Genial Toy €29.99, Bonneidea, Jolietoile; Zoua €34.99). Description still says "SquishCount". Stop ads ~28 Nov. |
| TrueAngle (digital angle gauge) | €34.99 (2-pack) | **€49.99 2-pack + €29.99 single** | Live: SP €15.50 + 2.60 for 2; ZD €18.72 (2) / €11.76 (1) | about 36–42% (2-pack) | €99.99 / €59.99 | Single gauge market €25–€29 (Anibiy, Flowoon). Move "1+1 OFFERT" from the title into the variant name if adding the single. |
| GentShield (men's wool coat) | €48.99 | **€69.99** | SP €27.83 + 2.60 (ZD €43.39 too expensive) | 43% | €139.99 | Market €70–€95 (Firewalky, Nyfolk, Middo, KiloMens). |
| FuseFind (breaker finder) | €59.99 | keep €59.99 | Live: ZD €33.37 (no SP cost) | 56% | €120 ok | Market: Prestige Tools $69.99, Maison Ambrine €97. If the cost stays at €33, test **€69.99**. |
| SnugWear (heated poncho) | €27.99 | **€49.99** (now live) | SP €22.54 + 2.60 / ZD €24.04 | 48–50% | €99.99 | Same product as HeatCape on Solundi (€39.99). |
| WindowGlow (2 × 300 LED curtains) | €19.99 | **€29.99** (now live) | SP €9.29 + 2.60 / ZD €11.66 | about 39–40% | €59.99 | Competitors sell one curtain for €27–€45. |
| WarmWork (fleece-lined pants) | €23.99 | **€49.99** (now live) | ZD €20.70 / SP €19.90 + 2.60 | 41–45% | €99.99 | Market €40–€55 (Claire Lyon, Druids, Carpshop24). |
| NailForce (manual nail gun) | €24.99 | **€44.99** | No FR row; estimated with DE agent €18.70 + 2.60 | about 47% | €89.99 | Zanaro DE sells it at €69.99. Add an FR row. |
| GlowJoy (LED balloons 5-pack + pump) | €29.99 | **€32.99**; 10-pack **€44.99** | SP €13.99 (5) / €20.95 (10) | 42% / 47% | €65.99 / €89.99 | Zendrop shows the same cost for 5 and 10 (row 1044), so check it. |

### Zanaro Berlin (DE)
| Product | Was | Recommended | Supplier / cost | Quote | Compare-at | Notes |
|---|---|---|---|---|---|---|
| WindWall – NEW 2 × 3 m variant | – | **€39.99** | Estimate about €12–€15 (no quote yet) | about 31–37% (est.) | €79.99 | Fits the ladder €29.99 / €39.99 / €49.99 / €69.99. Get a real quote; align size names (3,05×3,96 vs "3 x 3 m"). |
| FryLite (2/3/4-piece) | €26.99 / 34.99 / 41.99 | **€34.99 / 39.99 / 44.99**, later €39.99 / 44.99 / 49.99 | **Zendrop** €20.03 / 22.46 / 24.24 (agent loses money) | 57 / 56 / 54% | €69.99 / 79.99 / 89.99 | DE market €37–€50 (Gerwant, Groemont, Sheghett, Fritt & Fertig). FryLite is the worst product in all 4 tabs. |
| VitalGrow (hair oil) | €19.99 | **€24.99** | SP €6.26 + 2.60 | 35% | €49.99 | NL €32.99, FR €29.99. Soften "reversible hair loss" claims. |
| ZipHug (fleece onesie pyjama) | €32.99 | **€44.99** | SP €18.69 + 2.60 (tick SP) | 47% | €89.99 | Keep in line with ZipSnug. Also on Nestilia $36.99 and Solundi €32.99 (no rows there). |
| ArtVault (kids' art frame) | €24.99 | **€29.99** (all 3 colours) | SP €8.40 + 2.60 | 37% | €59.99 | Pandapiraten €38.95. Test a 2-pack at about €49.99. |
| ZipSnug (fleece cargo jumpsuit) | €33.99 | **€44.99** | Switch to **SP** €15.46 + 2.60 (ZD €20.23 ticked) | 40% | €89.99 | Market €36–€51. |
| SharpLapel (men's long coat) | €38.99 | **€49.99** | SP €18.94 + 2.60 ≈ ZD €21.76; tick one | 43% | €99.99 | Cheap €30–€37 rivals (Tayloro same coat €37.21) vs €70–€95 old-money (Middo €89.95, Nyfolk, KiloMens). |
| PuffWarm (faux-fur long puffer) | €59.99 | **€64.99** | SP €26.80 + 2.60 | 45% | €129.99 | Raxinaluxe €64.99, Novarillo €70.95. |
| CableChic (long cable-knit cardigan) | €36.99 | **€44.99** | SP €17.28 + 2.60 (tick SP) | 44% | €89.99 | FR €44.99, US $49.99. NL also €36.99, so raise it too. |
| CoreWarm (fleece vest) | €39.99 | keep €39.99 (test €42.99) | SP €13.01 + 2.60 (DE row 5572 added; tick SP) | 39% | €80 ok | DE market €32–€45. |
| WarmHood (hooded lined coat) | €28.99 | **€44.99** | SP €20.39 + 2.60; get a ZD quote (about €15–€16 in NL/FR) | 51% (SP) / 36% (ZD) | €89.99 | DE market €44–€60. |
| BurrowNap (pet sleeping bag, 1+1) | €39.99 | **€44.99** | ZD €13.67 | 30% | €89.98 | Competitors €24–€45 for ONE. NL €26.99 has no cost. |
| TissueClaus | €21.99 | about €27.95–€29.99 | SP €11.37 + 2.60 / ZD €14.82 | | | LivelyDay sells it in DE at €27.95. |
| BaggyEase | not live in DE | launch at **€39.99** | ZD $17.29 (US row) | 39% | €79.99 | DE joggers €32–€40 (Jolyeshop €34.99, Elsera €39.95). |

### Nestilia (US)
| Product | Was | Recommended | Supplier / cost | Quote | Compare-at | Notes |
|---|---|---|---|---|---|---|
| DrapeEase (drape trousers) | $21.99 | **$34.99**, ideally $39.99 | **SP** now €11.88 + 2.60 = €14.48 (cheaper than ZD €15.62) | 45% / 40% | $69.99 / $79.99 | |
| GameCozy (game-day hoodie, 224 variants) | $19.99 | **$39.99** | SP €12.31 + 2.60 / ZD €14.71 | 40–41% | $79.99 | Was about 82% at $19.99. |
| CozyPoncho (batwing poncho) | $34.99 | **$44.99** | SP €12.94 + 2.60 | 38% | $89.99 | SunbakedSoul $49.99, Ohcomfy $79.99. |
| TightReach (7-in-1 flare-nut wrench) | $41.99 | **$49.99** | **SP** €15.94 + 2.60 (ZD $33 far too high) | 41% | $99.99 | Declaredover $48.99; 6+ US stores scaling. NL/FR agent cost is much higher (€24–€25), so align it. |
| ZipHug | $36.99 | $44.99 | estimate with DE cost | about 52% | | No USA row yet. |

### Solundi (NL)
| Product | Was | Recommended | Supplier / cost | Quote | Compare-at | Notes |
|---|---|---|---|---|---|---|
| TissueClaus (Santa tissue cover) | €21.99 | **€29.99** | **ZD** €11.88 (SP €13.64) | 40% | €59.99 | Market $29.99 / €27.95 (Pinkdiyprint, LivelyDay). |
| StripeSet (knit loungewear set) | €31.99 | **€44.99** or €49.99 | SP €23.98 + 2.60 (ZD €29.34 is worse) | 59% / 53% | €89.99 / €99.99 | NL market €40–€50. The agent cost is too high, so ask for a re-quote. |
| HeatCape (= SnugWear) | €39.99 | €49.99 | ZD €21.57 / SP €24.20 | about 43–48% | €99.99 | |

## 5. Competitor research done (Nestilia, 12 Nov)
- **BaggyEase:** OverRip "Essential" (ads since Dec 2025), SVBFLOR straight-leg, Comfrt ($34.95), BY TYDON, Wins and Losses.
- **ZipSnug:** Tuxy (since Jan 2024), The Oodie, OppoSuits, Gymfit fleece jumpsuit, Coofandy (dropship, stopped).
- **SharpLapel:** Tayloro/rtgnso (same coat €37.21), Kzz, KiloMens, Qalyro, Velasca, Blake Hampton, Middo.
- **PuffWarm:** Thebeautynorth & Moonlightbelle (same supplier coat $49.99, scaling), Novarillo, Parker & Hayes "Gloria" $69.95, Chic-lucky.
- **CheerBox (supplier search):** no single AliExpress/Temu bundle found; build it from parts (cup, fuzzy socks, star pen, clear PVC bag, tag, notepad). Amazon bundles B0HC6V9FX6, Pickmesh B0HBWVFXYJ, Remerry B0H4F52MWR. Real AliExpress links need the Claude in Chrome extension.

## 6. Open items / to-dos
1. Add missing cost rows: NailForce (FR), ZipHug (NL, USA), WindWall 2 × 3 m (all tabs), BurrowNap NL, StripeSet re-quote, TrueAngle re-quote.
2. Tick a supplier on rows where both are FALSE: DE CoreWarm 5572, CableChic 5539, SharpLapel 5533, ZipHug 5578, NailForce 5305.
3. Fix the FryLite pricing / supplier in NL, FR and US too (95–187% on the agent).
4. DE BoozeBot GRAY ONLY (row ~3791): "OOS-GRAY" typed in a price cell causes #VALUE!.
5. BaggyEase (Nestilia): the "What guys say" section shows "0%" placeholders.
6. Seasonal: advent calendars and Christmas items (SurpriseDays, TissueClaus, WindowGlow) sell until about mid-December; make price changes now.

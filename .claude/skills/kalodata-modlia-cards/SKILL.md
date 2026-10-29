---
name: kalodata-modlia-cards
description: 'Create Asana product-test cards for Modlia (the French store) from the "Kalodata Modlia (FR)" tab of the winning-products master log — only for rows the operator ticked in the unlabelled checkbox column V, by default the 5 most recent ticks. Dedupes against the whole FR board ("1D. Pinterest - FR") on Kalodata product ID, source-listing id and name; coins a unique two-word ™ house brand name checked against every Pinterest board (DE/SE/NL/US/old FR) and the four stores; writes the house-template notes (marketing angle, kalodata link, USD TikTok Shop France proof line, source, and a Note price = competitor price in EUR minus 1 € rounded to the nearest .99, also written to the sheet's Selling price /Offer column) plus a risk line; creates the cards in section "1B. Copy PP (Aireen)" and reports back. Use when the user asks to card / create Asana tasks for the ticked Kalodata FR products, push approved Modlia products to Asana, "make cards for the last N ticks", or similar. Not for the US "Kalodata Winning Products" tab or the "Winning Products" tab.'
---

# Kalodata Modlia (FR) → Asana product-test cards

Creates Asana product-test cards for **Modlia** (our French store) from the **Kalodata Modlia
(FR)** tab of the winning-products master log, for the approved products only.

The whole point of the checkbox is that **the operator has already decided**. Your job is to
transfer their decision faithfully — never to re-judge which products deserve a card, and never
to include one they did not tick.

The market is **TikTok Shop France**, not US, and the destination is the French Asana board
only. Kalodata rows carry **no WinningHunter link, no Meta ads-library link and no AliExpress
supplier**, so those lines are left blank for the creative and sourcing steps that follow.

**The sheet is read-only except for one cell per carded row:** the computed selling price in
`U` (`Selling price /Offer`, step 3b). Never tick or untick `V`, never write any other column,
and never overwrite a `U` cell the operator has already filled.

## Sources

### Master log

Spreadsheet `1ha9uILlG-VetpFMqHCkP3F9P_o7k4nUrZS-zAk3pZJ4`, tab **`Kalodata Modlia (FR)`**
(`gid=1275252354`). Header is on **row 1**; data starts at **row 2**; the newest run is at the
bottom. Not the `Kalodata Winning Products` tab (US TikTok Shop, feeds DE / SE / NL) and not the
`Winning Products` tab (header on row 4, 34 columns).

| Col | Header | Used for |
|---|---|---|
| `A` | # | position within its run (`A1` holds a stray backtick, not a header) |
| `B` | Category | the niche — context for the angle |
| `C` | Product (TikTok listing) | the source name, usually **in French** — you rename it, see step 4 |
| `D` | TikTok seller | the competitor — often **empty** on this tab |
| `E` | Revenue 7d (USD) | the `proof:` line, and the reason it was ticked |
| `F` | Growth 7d % | `proof:` |
| `G` | Units 7d | `proof:` |
| `H` | TikTok price | what the market actually pays — margin check |
| `I` | Launch date | |
| `J` | Days live | risk check — see step 6 |
| `K` | Video rev % | how demand is generated: ~100% = video-native, low = search/shop/LIVE |
| `L` | Commission % | affiliate pull; 0% often means no creator army behind it |
| `M` | Kalodata product ID | **dedupe key #1** — unique per listing |
| `N` | Kalodata link (verified via sitemap) | the `kalodata:` line (carries `region=FR`) |
| `O` | Reference price | risk check only — does **not** go in the Note |
| `P` | PAGEPILOT URL | **the source listing URL** — see the warning below. **Dedupe key #2** |
| `Q` | Link status (all opened + live) | whether the research run opened it, or `Not sourced (FR trend list)` |
| `R` | Angle / note | the run's own angle *and* its recorded risk — read it |
| `S` | TikTok store page | the `competitor's link:` line — often **empty** |
| `T` | Date added | |
| `U` | Selling price /Offer | **the whole `Note:` line** — computed in step 3b and written here, unless the operator already filled it |
| **`V`** | *(no header text)* | **the checkbox — this is the filter** |

Traps in that table:

- **`P` is labelled `PAGEPILOT URL` but holds the source listing**, e.g. the Amazon page the
  research run priced against. There is no longer a `Source` column, so take the site label
  (`amazon.fr`, …) from the URL host or from `Q`. Do not go looking for a pagepilot.io link there.
- **Many rows are unsourced.** Rows from the operator's FR trend list have `Q` = `Not sourced (FR
  trend list)` and empty `D`, `O`, `P`, `S`. Leave those lines bare on the card — never
  invent a source or a seller — and flag it on the `risk:` line (step 6).
- **`V` has no header text.** `V1` is empty (as of 2026-10-29; it used to be an unticked
  checkbox). Identify the checkbox as the **rightmost column whose cells from row 2 down are
  all booleans**, and check that no column to its right holds booleans before you trust it.
- **Revenue is in USD even though the market is France.** Kalodata reports TikTok Shop France in
  dollars; copy the figures as the sheet has them and label them `USD, TikTok Shop France`.

**Re-read row 1 before trusting a single one of these letters.** Columns move: sibling tabs have
had columns inserted mid-flight, and this tab lost its `Source` column (between `N` and
`Reference price`) in October 2026, shifting everything after it one letter left. Map by header
**name**; resolve `V` by type, as above.

If the Google Sheets MCP is down (`CONNECTION_CLOSED`), these read-only export URLs still work for
anyone with view access:

- values: `https://docs.google.com/spreadsheets/d/1ha9uILlG-VetpFMqHCkP3F9P_o7k4nUrZS-zAk3pZJ4/export?format=csv&gid=1275252354`
- formulas: the same URL with `format=xlsx`

### Asana

- Workspace `ecomjets.co` (`1202393474006143`).
- **Destination:** project `1214688737915575` (**"1D. Pinterest - FR"**), section
  `1214688737915576` (**"1B. Copy PP (Aireen)"** — the board's first working column).
- **FR only.** Never add these cards to `1A. Pinterest - DE` (`1204544103564278`),
  `1B. Pinterest - SE` (`1206091429056562`), `1C. Pinterest - NL` (`1207494343020090`),
  `1E. Pinterest - US` (`1215906766476002`) or the older `6. Pinterest - FR`
  (`1206890387335983`). Those boards still matter as **registers** (steps 2 and 4) — just never
  as a destination.
- House format reference: task `1218228092133330` (`AuraCount™`).

## Steps

### 1. Find the approved rows — the last 5 ticks

Start by reading row 1 and the checkbox column. **The batch is the five most recent ticks**,
wherever they sit. Find the last row with a product in column `C`, walk **bottom-up** skipping
blank rows, and collect rows whose checkbox in `V` is true until you have **5**. Ticks can be
spread across several runs.

- Match the checkbox **case-insensitively and type-tolerantly**: an `UNFORMATTED_VALUE` read
  returns the boolean `True`, a `FORMATTED_VALUE` read returns the string `TRUE`.
- Do not use a spreadsheet find/search tool to locate the rows — it **caps at 50 results**,
  truncates silently, and matches the word "true" inside ordinary prose in other columns. Read
  the column and map positions to row numbers: index 0 of a read starting at row 2 is row 2.
- **If nothing is ticked, that is a real answer.** As of 2026-10-28 the tab held rows 2–12 with
  every box unticked. Report it and create nothing — never "helpfully" promote the top-revenue
  rows.

The operator overrides the window whenever they say so — "the last 10 ticks", "everything
ticked", "rows 3 to 8". Honour what they asked for; five is only the default.

### 2. Skip products that already have a card

Because cards are named with a coined brand name that bears no resemblance to column `C`,
**name matching alone does not work**. List the existing tasks across the **whole FR project**
`1214688737915575`, all sections, **including completed ones**, with `opt_fields=name,notes`.
Keep this response — step 4 reuses it. Then match a sheet row against a task if **any** of these
hit:

1. the **Kalodata product ID** from `M` appears in the task notes — the strongest key;
2. the **source listing URL** from `P` appears in the notes (compare on the ASIN / item id, not
   the whole URL) — only when `P` is not empty;
3. the task name equals `<column C>` or `TEST - <column C>`, case-insensitively.

A product already carded on another board (DE / SE / NL / US) for a different store is **not** a
duplicate here — Modlia needs its own FR card. Do, however, mention the match in the report so
the page builder can reuse the existing page and images.

Do **not** dedupe on the TikTok store page in `S`: one seller can appear on several rows with
different products.

Tell the operator the arithmetic before you write anything — "5 ticks found: rows 3, 5, 7, 9,
11; 1 already on the FR board; creating 4". If a wider window was asked for and it comes back
large (more than 10), confirm before creating.

### 3. Pull the details

- `U` ("Selling price /Offer") must be read as a **`FORMATTED_VALUE`, never as a formula**, so
  `34€` stays `34€`. If the operator has already filled it, the `Note:` line is their text
  verbatim and you do not recompute it. If it is empty, compute it in step 3b.
- `N`, `P` and `S` may be stored as `=HYPERLINK(url,"label")` — read them with a formula read
  (`valueRenderOption=FORMULA`, or the XLSX export) and handle both shapes.
- `C` is stored **truncated at roughly 90 characters**, mid-word, and is usually in French. Do
  not treat the cut-off tail as part of the name; open `N` if you need the full title.
- `E`, `F`, `G`, `H`, `J` feed the `proof:` line. Label them **USD, 7-day, TikTok Shop France**.

### 3b. Compute the selling price (`Note:` line and column `U`)

For every row being carded whose `U` is empty:

1. **Competitor price** = the price on the competitor's link. Use the TikTok store page in `S`
   when it is filled. When `S` is empty (usual on this tab), use the competitor's TikTok Shop
   France listing price, `TikTok price` in `H` (the Kalodata listing in `N`). Say on the report
   which one you used.
2. **Convert to EUR** at the day's ECB reference rate:
   `https://api.frankfurter.dev/v1/latest?from=USD&to=EUR`. If that is down, use
   `https://open.er-api.com/v6/latest/USD` and say so. Use one rate for the whole run and state
   it, with its date, in the report.
3. **Subtract 1 €.**
4. **Round to the nearest `xx.99`**: with `v` = the result of step 3, the price is
   `round_half_up(v − 0.99) + 0.99` (35.53 → 35.99, 35.49 → 34.99, 6.14 → 5.99). Use exact
   decimal arithmetic. Flag any row within ~0.05 € of the halfway point, where a small rate move
   would flip the price.
5. Write it as `36.99€` (dot decimal, `€` suffix, no space), both on the card's `Note:` line and
   in that row's `U` cell. Re-read the row first to confirm it is the same product (match `M`)
   and `U` is still empty, write only the `U` cells of the carded rows (one range per contiguous
   block, never across rows you are not carding), then read `U` back to confirm.

Example, row 5: $42.85 × 0.89823 = 38.49 € − 1 = 37.49 → **36.99€**.

### 4. Name the product

**Every card gets a coined house brand name — never the seller's listing title.**

The name is **two words carrying the product's main benefit**, joined into one token and
followed by `™`:

| Style | Examples | When it suits |
|---|---|---|
| **CamelCase** | `RattlePals™` · `BeamRestore™` · `LymphFlow™` · `CeramiFix™` | most names; the default |
| **Ampersand** | `Slim&Tone™` | when the benefit is genuinely two outcomes delivered together |

Rules that make a name usable:

- **Name the benefit, not the category.** Build it from `R` (the run's own angle) and what the
  TikTok video would show.
- **Two words, one token, `™` appended.** No spaces, no hyphens, never more than two words.
- **ASCII only, ~14 characters or fewer.** No é / è / ç / ï / ë — accents fail in the image
  pipeline, and rare French diacritics fail outright.
- **Reads well to a French shopper.** Short English words the French already use (Glow, Slim,
  Flex, Pure, Care, Fit) or Latin-rooted words that work in both (Lumi, Thermo, Douce, Calme) —
  avoid English puns a French buyer would not get and anything that sounds rude in French.
- **Coin it — do not borrow it.** Never reuse the seller's brand or any real trademark, and
  never a licensed property.
- **Never coin the same name twice** — absolute, see below.

#### The name must be unique, forever

**A name may be used once and never again**, including for a product that was later killed.
Check against five registers before you settle on any name:

1. **Every task in the FR project** `1214688737915575` — fetched in step 2; reuse it.
2. **Every task in the DE, SE, NL, US and old FR projects** (`1204544103564278`,
   `1206091429056562`, `1207494343020090`, `1215906766476002`, `1206890387335983`), all
   sections, including completed ones. A name spent on any board is spent on all of them.
3. **The names you assigned earlier in this same run.**
4. **The four stores** — Zanaro, Modlia, Solundi, Nestilia. A name already on a live product is
   spent even if no card carries it.
5. If the same product already has a card on another board (step 2), **reuse that card's name**
   rather than coining a second one for the same product — that is the one allowed repeat.

Compare **normalised**: lowercase, `™` stripped, spaces and punctuation removed. On a collision,
**re-coin from a different benefit** — `HairThrive2™` or `HairThrivePro™` is the same name
wearing a hat, and is not acceptable.

Put the name in the marketing angle sentence too — that is where the page builder picks it up.

### 5. Create the cards

Name: **`<CoinedName>™`** — no `TEST - ` prefix.

Notes follow the house template (written in English, like every other card — the page builder
translates for the French store):

```
marketing angle: <one or two sentences: what it is, who it is for, what it is sold on — naming the coined brand; say it is for Modlia (FR)>

competitor's link: <TikTok store page from S — blank if empty>
kalodata: <url from N>
proof: <E> rev / <G> units in 7d (USD, TikTok Shop France) · <F> growth · live <J>d · TikTok price <H> · video rev <K>
source (<site, e.g. amazon.fr>): <url from P> @ <O>   ← write "source: not sourced yet" when P is empty
Note: <U verbatim if the operator filled it, else the step 3b price, e.g. "36.99€">

ad: 
ad library: 
video: 

pagepilot:
ZANARO:
MODLIA:
SOLUNDI:
NESTILIA:

Our Store URL: 
```

- **`Note:`** holds **only** the selling price: the operator's `U` text verbatim when they filled
  it, otherwise the step 3b price (the same value you write to `U`). Never invent an offer
  (`1+1`, bundles); that stays the operator's call.
- **`ad:` and `ad library:` stay blank.** The creative comes later from the video-research step.
- **`proof:`** is the whole case for the test, so state the currency and market on the line.

Create the tasks in project `1214688737915575`, section `1214688737915576`. Then read each task
back and confirm it sits on **only** the FR board. Leave assignee and due date empty unless the
operator says otherwise.

Write the **marketing angle** from the product, its category (`B`) and the run's own angle
(`R`). `K` tells you *how* it sells — near 100% video revenue means the page has to carry a demo;
a low figure (often LIVE-driven on TikTok Shop France, as `R` usually notes) means the page must
carry specs and comparison. When `R` is only the generic "Trending on TikTok Shop France" line,
say so and tell the builder to open the Kalodata link — an invented angle is worse than an
admitted gap.

### 6. Carry the warnings across

Put them on **one short line at the very end of the notes**, after `Our Store URL:`, prefixed
`risk:`. Column `R` is where the research run recorded its own concern; read it and carry it
(e.g. "source a 230V EU-plug model for France"). Only write the line when there is a genuine
concern:

- **Not sourced.** `Q` = `Not sourced (FR trend list)` or `P` empty — the builder must find a
  supplier before starting. This will be common on this tab.
- **Approximate source.** `R` saying `APPROXIMATE` means the listing in `P` is a near-match, not
  the same product.
- **Electrical / EU spec.** US-sourced electrical items are 120V with US plugs; France needs
  230V and EU plugs, and CE marking.
- **Channel gap.** TikTok Shop France sells on impulse, off a live or a creator; Pinterest sells
  on planned search. Flag products driven by LIVE or one creator (`K` near 100% with a high `L`,
  or `R` citing a big LIVE share).
- **Licensing and IP.** Characters, team apparel, anything borrowing a real brand.
- **Regulated claims.** Supplements, cosmetics, medical-adjacent — French and EU advertising
  rules bite on health claims and before/after results.
- **Hard seasonality.** `R` often carries `[Winter, sell until Feb]` — say how much selling
  window is left.
- **Thin margin.** Reference price (`O`) against the TikTok price (`H`).
- **Unproven.** `Days live` (`J`) under ~14 days, or a huge growth % on a few days live.

## Report back

Give a table of what was created — coined name, the sheet row and product it came from, 7-day
revenue, TikTok price, source status, and a link to each card — then state the warnings you
attached, name any ticked row you skipped as a duplicate and which FR card it matched, and note
any product that already has a card on another board so its page can be reused. Include each
row's computed price, the competitor price it came from and the EUR rate (with its date), and
flag any price that sat near a rounding boundary.

If nothing was ticked, say so plainly and confirm that no cards were created.

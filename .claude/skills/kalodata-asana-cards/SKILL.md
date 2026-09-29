---
name: kalodata-asana-cards
description: Create Asana product-test cards in the "1E. Pinterest - US" project (section "1B. Create Product Page (Aireen)") from the operator-ticked rows of the "Kalodata Winning Products" tab of the Winning-Products-MASTER Google Sheet. Default batch is the 5 most recent ticks in the checkbox column. Coins a unique house brand name per product, dedupes against existing cards, fills the house note template and carries risk warnings. Use when the user asks to create Kalodata cards, push approved/ticked Kalodata products to Asana, or make test cards from the Kalodata tab.
---

# Kalodata ticked rows → Asana product-test cards

You are creating Asana product-test cards from the **Kalodata tab** of our winning-products
master log, for the approved products only. Follow this procedure exactly.

You need: read access to the Google Sheet below (Google Sheets MCP, or the CSV/XLSX export URLs),
and Asana access to the `ecomjets.co` workspace.

The whole point of the checkbox is that **the operator has already decided**. Your job is to
transfer their decision faithfully — never to re-judge which products deserve a card, and never
to include one they did not tick.

Kalodata rows carry **no WinningHunter link, no Meta ads-library link and no AliExpress
supplier**, so those lines are left blank for the creative and sourcing steps that follow.

## Sources

**Master log** — spreadsheet `1ha9uILlG-VetpFMqHCkP3F9P_o7k4nUrZS-zAk3pZJ4`, tab
**`Kalodata Winning Products`** (`gid=1563256989`). Header is on **row 1**; data starts at
**row 2**; the newest run is at the bottom. This is not the `Winning Products` tab — that one has
its header on row 4 and 34 columns, and every letter below would be wrong there.

| Col | Header | Used for |
|---|---|---|
| `A` | # | position within its run |
| `B` | Category | the niche — context for the angle |
| `C` | Product (TikTok listing) | the source name — you rename it, see step 4 |
| `D` | TikTok seller | the competitor |
| `E` | Revenue 7d (USD) | the `proof:` line, and the reason it was ticked |
| `F` | Growth 7d % | `proof:` |
| `G` | Units 7d | `proof:` |
| `H` | TikTok price | what the market actually pays — margin check |
| `I` | Launch date | |
| `J` | Days live | risk check — see step 6 |
| `K` | Video rev % | how demand is generated: ~100% = video-native, low = search/shop |
| `L` | Commission % | affiliate pull; 0% often means no creator army behind it |
| `M` | Kalodata product ID | **dedupe key #1** — unique per listing |
| `N` | Kalodata link (verified via sitemap) | the `kalodata:` line |
| `O` | Source | labels `Q` (Amazon, AliExpress, …) |
| `P` | Reference price | risk check only — does **not** go in the Note |
| `Q` | PAGEPILOT URL | **the source listing URL** — see the warning below. **Dedupe key #2** |
| `R` | Link status | whether the research run actually opened it |
| `S` | Angle / note | the run's own angle *and* its recorded risk — read it |
| `T` | TikTok store page | the `competitor's link:` line |
| `U` | Date added | |
| `V` | Selling price /Offer | **the whole `Note:` line** — the colleague fills this in |
| **`W`** | *(no header text)* | **the checkbox — this is the filter** |

Two traps in that table, both of which have already cost a run elsewhere in this sheet:

- **`Q` is labelled `PAGEPILOT URL` but holds the source listing**, e.g. the Amazon page the
  research run priced against (`O` says which site it is). It is the URL you would feed to
  PagePilot, which is where the label comes from. Do not go looking for a pagepilot.io link
  there, and do not leave the line blank because the header confused you.
- **`W` has no header text.** `W1` is itself an unticked checkbox, so it reads `FALSE`, not a
  name — the usual "map by header name" rule cannot find this column. Identify it as the
  **rightmost column whose cells are booleans**, and confirm `W1` comes back as a boolean `False`
  rather than text before you trust it.

**Re-read row 1 before trusting a single one of these letters.** The sibling tab has had columns
inserted mid-flight twice, shifting everything rightward; assume this one can too. Map by header
**name**, and if a read comes back looking one column out, that is what happened. The one column
you cannot resolve by name is `W` — resolve it by type, as above.

If the Google Sheets MCP is down (`CONNECTION_CLOSED`), these read-only export URLs still work for
anyone with view access:
`https://docs.google.com/spreadsheets/d/1ha9uILlG-VetpFMqHCkP3F9P_o7k4nUrZS-zAk3pZJ4/export?format=csv&gid=1563256989`
for values, and the same URL with `format=xlsx` for the formulas.

**Asana** — project `1215906766476002` (**"1E. Pinterest - US"**, workspace `ecomjets.co`),
section `1215906766476008` (**"1B. Create Product Page (Aireen)"** — the board's first working
column). Do **not** land cards in `1A. Product Research (Bella)`, which sits to its left: that
column is for research, and these products have already been researched and approved.
Until 2026-09-28 this procedure created its cards on `1C. Pinterest - NL` (`1207494343020090`);
it no longer does. Tasks in this workspace are multi-homed: a card can sit in the US, NL and DE
(`1204544103564278`) projects at once, which matters for step 2.

House format reference: task `1218228092133330` (`AuraCount™`).

## Steps

### 1. Find the approved rows — the last 5 ticks

**The batch is the five most recent ticks**, wherever they sit. Find the last row with a product
in column `C`, walk **bottom-up** skipping blank rows, and collect rows whose checkbox in `W` is
true until you have **5**. Ticks can be spread across several runs — the window is "five most
recent ticks", not "the last run".

- Match the checkbox **case-insensitively and type-tolerantly**: an `UNFORMATTED_VALUE` read
  returns the boolean `True`, a `FORMATTED_VALUE` read returns the string `TRUE`, and the API has
  returned `True` where a strict `== "TRUE"` silently matched nothing.
- Do not use a spreadsheet find/search tool to locate the rows — it **caps at 50 results**,
  truncates silently, and matches the word "true" inside ordinary prose in other columns. Read the
  column and map positions to row numbers: index 0 of a read starting at row 2 is row 2.
- **If nothing is ticked, that is a real answer.** Report it and create nothing — never
  "helpfully" promote the top-revenue rows.

The operator overrides the window whenever they say so — "the last 10 ticks", "everything
ticked", "rows 12 to 21", "just today's". Honour what they asked for; five is only the default for
a bare invocation.

### 2. Skip products that already have a card

A run that was interrupted, or an operator who re-ticks a row, lands the same product twice. The
US project holds ~350 tasks and grows every week; one duplicate inside it is invisible until the
page builder has already built it.

Because cards are named with a coined brand name that bears no resemblance to column `C`, **name
matching alone does not work**. List the existing tasks across the **whole US project** (cards get
moved on to 1C/1D/1E as work progresses), **including completed ones**, with
`opt_fields=name,notes`. Keep this response — step 4 reuses it as the register of coined names
already spent, so fetch it once. Then match a sheet row against a task if **any** of these hit:

1. the **Kalodata product ID** from `M` appears in the task notes — the strongest key;
2. the **source listing URL** from `Q` appears in the notes (compare on the ASIN / item id, not
   the whole URL, since tracking parameters differ);
3. the task name equals `<column C>` or `TEST - <column C>`, case-insensitively — this catches
   anything a human created by hand.

Do **not** dedupe on the TikTok store page in `T`: one seller can appear on several rows with
different products, and matching on the store would drop a genuine new product.

Tell the operator the arithmetic before you write anything — "5 ticks found: rows 6, 9, 14, 17,
20; 1 already on the board; creating 4" — naming the rows so they can see which ticks you took and
catch a miscount early. If a wider window was asked for and it comes back large (more than 10),
confirm before creating.

### 3. Pull the details

- `V` ("Selling price /Offer") must be read as a **`FORMATTED_VALUE`, never as a formula**. The
  cell is currency-formatted, so a formula read returns `34` where the operator wrote `34€` — and
  the `Note:` line is their text verbatim, currency symbol included.
- `N`, `Q` and `T` are usually plain URLs on this tab, but may be stored as
  `=HYPERLINK(url,"label")` — a normal read then returns the label and not the URL. Read them with
  a formula read (`valueRenderOption=FORMULA`, or the XLSX export) and handle both shapes.
- `C` is stored **truncated at roughly 90 characters**, mid-word. Do not treat the cut-off tail as
  part of the product's name, and open `N` if you need the full listing title.
- `E`, `F`, `G`, `H`, `J` feed the `proof:` line. Copy the figures as the sheet has them and say
  they are **USD, 7-day, US TikTok Shop** — that is TikTok demand, not Pinterest demand.

### 4. Name the product

**Every card gets a coined house brand name — never the seller's listing title.** A title like
`LikeMyChoice 2026 Women 2 Piece Quiet Luxury Matching Set Deep V Neck…` is exactly what this
replaces.

The name is **two words carrying the product's main benefit**, joined into one token and followed
by `™`. Two join styles are house style — pick whichever reads better for the pair:

| Style | Examples | When it suits |
|---|---|---|
| **CamelCase** | `RattlePals™` · `BeamRestore™` · `LymphFlow™` · `CeramiFix™` | most names; the default |
| **Ampersand** | `Slim&Tone™` | when the benefit is genuinely two outcomes delivered together |

Rules that make a name usable:

- **Name the benefit, not the category.** `BeamRestore` sells the outcome; `HeadlightKit` sells a
  shelf. On this tab the benefit is usually visible in `S` (the run's own angle) and in what the
  TikTok video would show — build the name from that.
- **Two words, one token, `™` appended.** No spaces, no hyphens, never more than two words.
- **ASCII only, ~14 characters or fewer.** These names get baked into images and page copy across
  DE / NL / FR / EN stores; accents and umlauts fail in the image pipeline.
- **Coin it — do not borrow it.** Never reuse the seller's brand (NoviNest, GrivGear,
  LikeMyChoice) or any real trademark, and never a licensed property (see the NFL note in step 6).
- **Reads naturally in American English.** These cards feed the US board and its page is written
  in American English; the same name may later be reused on the DE / FR stores, so keep it easy to
  say there too.
- **Never coin the same name twice** — absolute, see below.

#### The name must be unique, forever

Two products carrying `HairThrive™` collide in Asana, in PagePilot, in the image files and in the
store, and the page builder cannot tell which card the assets belong to. **A name may be used once
and never again**, including for a product that was later killed — a dead test still owns its
name.

Check against five registers before you settle on any name:

1. **Every task in the US project** `1215906766476002`, all sections, **including completed
   ones** — you already fetched this in step 2; reuse that response.
2. **Every task in the NL project** `1207494343020090`. Kalodata cards were created there until
   2026-09-28, so most of the names this tab has already spent live on that board.
3. **Every task in the DE project** `1204544103564278`. The boards share cards (`AuraCount™` sits
   in both NL and DE), and a name spent on any board is spent on all of them.
4. **The names you assigned earlier in this same run.** Keep a set as you go — batches routinely
   contain two products in one niche, and the same benefit suggests the same name twice.
5. **The four stores** — Zanaro, Modlia, Solundi, Nestilia. A name already on a live product is
   spent even if no card carries it.

Compare **normalised**: lowercase, `™` stripped, spaces and punctuation removed. `HairThrive™`,
`hairthrive` and `Hair Thrive` are all the same name and all collide.

On a collision, **re-coin from a different benefit** — the speed, the feel, the surface it works
on, the moment it is used. `GlowRevive™` and `SheenGuard™` are two names; `HairThrive2™`,
`HairThriveX™` and `HairThrivePro™` are the same name wearing a hat, and are not acceptable.

Put the name in the marketing angle sentence too, the way the reference card does — that is where
the page builder picks it up.

### 5. Create the cards

Name: **`<CoinedName>™`** — no `TEST - ` prefix.

Notes follow the house template. The trailing blank fields matter, because the page builder and
the video researcher fill them in:

```
marketing angle: <one or two sentences: what it is, who it is for, what it is sold on — naming the coined brand>

competitor's link: <TikTok store page from T>
kalodata: <url from N>
proof: <E> rev / <G> units in 7d (USD, US TikTok Shop) · <F> growth · live <J>d · TikTok price <H> · video rev <K>
source (<O>): <url from Q> @ <P>
Note: <V verbatim, e.g. "1+1: 39.99" — leave blank if V is empty>

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

The lines worth stating twice:

- **`Note:`** holds **only** the `Selling price /Offer` cell (`V`) — the offer and its price, e.g.
  `1+1: 39.99`. Not the TikTok price, not the reference price, not the COGS. `V` is filled in by a
  colleague and is usually **still empty when you create the card**: leave the line bare in that
  case. Never compute, estimate or back-fill an offer yourself.
- **`ad:` and `ad library:` stay blank.** Kalodata rows have no WinningHunter or Meta creative
  behind them — the product was found on TikTok Shop revenue, not on an ad. The creative comes
  later from the video-research run. Do not paste the Kalodata link or the TikTok store on those
  lines to make the card look complete.
- **`proof:`** exists because these products have no ad spend to point at. It is the whole case
  for the test, so state the currency and market on the line; nobody downstream should have to
  guess whether `$149,424` was Pinterest revenue.

Create the tasks with `default_project` `1215906766476002` and `section_id` `1215906766476008`.
Leave assignee and due date empty unless the operator says otherwise — the reference card has
neither.

Write the **marketing angle** from the product, its category (`B`) and the run's own angle (`S`):
what the thing is, who it is for, and the lever the TikTok seller pulls. `K` tells you *how* it
sells — near 100% video revenue means the page has to carry a demo, a low figure means it is won
in search and the page must carry specs and comparison. When `S` is empty, say so in the notes and
tell the builder to open the Kalodata link — an invented angle is worse than an admitted gap.

**Never write back to the sheet.** This procedure reads only: never tick or untick `W`, never fill
`V`, and never touch the tab in any other way.

### 6. Carry the warnings across

Put them on **one short line at the very end of the notes**, after `Our Store URL:`, prefixed
`risk:` — out of the `Note:` line, which belongs to the offer alone. Column `S` is where the
research run recorded its own concern; read it and carry it. Only write the line when there is a
genuine concern:

- **Channel gap.** Every figure on this tab is **US TikTok Shop, in USD**, and these cards feed the
  **US Pinterest** pipeline — same country, different channel. TikTok Shop sells on impulse, off a
  live demo or a creator; Pinterest sells on planned search. Flag a product whose revenue depends
  on the creator rather than the product (`K` near 100% together with a high commission in `L`),
  because a Pinterest page cannot bring that creator along.
- **Licensing and IP.** City/team apparel, characters, and anything that borrows a real brand. The
  run already flagged one: a 32-city football hoodie is NFL territory. Flag it, and never coin a
  name that leans on the property.
- **Regulated claims.** Supplements, cosmetics, anything medical-adjacent (a CPAP cleaning kit is
  a medical-device accessory). FTC and FDA rules bite on the ad copy and the page (health claims,
  "clinically proven", before/after results).
- **Hard seasonality.** Advent calendars and Christmas countdowns are dated to the day. A test
  started too late is really a test for next year — say which.
- **Thin margin.** Reference price (`P`) against the TikTok price (`H`) shows the room the page
  has. Check it even though neither number goes in the Note.
- **Unproven.** Low `Days live` (`J`) — a product live under ~14 days has a revenue figure but no
  durability, and a 100% growth figure on 3 days live is an artefact, not a trend.
- **Dead link.** `R` ("Link status") not confirming the listing opened and was in stock means the
  builder must source it again before starting.

## Report back

Give a table of what was created — coined name, the sheet row and product it came from, 7-day
revenue, TikTok price, reference price, and a link to each card — then state the warnings you
attached and why, and name any ticked row you skipped as a duplicate and which existing card it
matched. The operator decides what to build next from this, so the risky ones, the thin-margin
ones and the creator-dependent ones are the useful signal, not the count.

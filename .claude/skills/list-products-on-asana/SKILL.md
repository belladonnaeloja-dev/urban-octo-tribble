---
name: list-products-on-asana
description: Create Asana product-test tasks from the winning-products master log, for the approved products only. Looks ONLY at the last 20 products in the table — the two most recent research runs — reads the "Approved For Asana" checkbox column (re-verify its letter against row 4 every run, it has shifted twice already) across those twenty rows, takes ONLY the ones where it is TRUE (older ticked rows further up the sheet are past decisions and are left alone unless the operator asks for a wider or narrower window), skips any product that already has a task so re-runs never duplicate, and creates one task per remaining product in the "1A. Pinterest - DE" project under section "1B. Create Product Page (Aireen)". Each task is named with a COINED HOUSE BRAND NAME — two linked words plus ™, reflecting the product's main benefit (BeamRestore™, LymphFlow™, HairThrive™) — never the supplier's own product name and never a name any earlier task or store product already uses, and is filled from the house template (marketing angle, competitor's link, aliexpress, a Note line holding only the "Selling price /Offer" cell, the WinningHunter link on "ad:", the Meta ads-library link on "ad library:", then blank video/pagepilot/store-URL lines for the page builder). Use whenever the user asks to list products on Asana, create Asana tasks for products, "add the checked products to Asana", push the ticked rows from the research sheet into Asana, or create test tasks for products they have selected — and also when they tick boxes in the master log and ask you to action them, even without naming Asana. Not for creating arbitrary Asana tasks (use the Asana tools directly) and not for finding new products (that is find-winning-products).
---

# List Products On Asana

Turn ticked rows in the winning-products master log into Asana tasks for the page builder.

The whole point of the checkbox is that **the operator has already decided**. Your job is to
transfer their decision faithfully — never to re-judge which products deserve a task, and never
to include one they did not tick.

## Sources

**Master log** — spreadsheet `1ha9uILlG-VetpFMqHCkP3F9P_o7k4nUrZS-zAk3pZJ4`, tab
`Winning Products`. Header is on **row 4**; data starts at row 5.

| Col (as of 2026-09-04) | Field | Used for |
|---|---|---|
| `D` | Product | the source name — you rename it, see step 4 |
| `X` | Verdict | not used directly — a newer column, ignore it |
| `Y` | Main killer / risk | warnings worth carrying into the task |
| `Z` | Their hook (first line) | the marketing angle |
| `AA` | Open in WinningHunter | **the `ad:` line** |
| `AB` | Product page | `competitor's link:` |
| `AC` | The winning ad (Meta) | **the `ad library:` line** |
| `AD` | All their live ads | not used |
| `AE` | AliExpress supplier | `aliexpress:` |
| `AF` | COGS EUR | risk check only — does **not** go in the Note |
| `AG` | Selling price /Offer | **the whole `Note:` line** — the colleague fills this in |
| **`AH`** | **Approved For Asana** | **the checkbox — this is the filter** |

**Do not trust this table blindly — re-read row 4 every run.** It has drifted twice already: `AE`
→ `AG` between Aug and Sep 2026 (a two-column insert), then `AG` → `AH` within Sep 2026 alone (a
one-column insert — "Verdict" landed at `X`, pushing everything after it one letter right). The
sheet's own header-note row sometimes lags the real layout too — it said "AG = Approved For
Asana" days after the sheet had already moved to `AH`, so verify against the actual row 4 cells,
not the note. Confirm every lettered column below against row 4 by column position (index 0 of a
read starting at row 4 is column A) before trusting any of the steps that follow.

**Reading the sheet — two paths, in order of preference:**

1. **Autosheet** (`autosheet_start_agent_google_sheets_spreadsheet` or a native google-sheets MCP,
   if either is connected) — ask it directly for the row window, formulas, and formatted values in
   one natural-language request. Fastest when it's up. It runs on its own billing/trial and can
   come back `api-billing-free-trial-ended`; if so, fall back to path 2 rather than guessing from
   its error message.
2. **Google Drive `download_file_content`** — reliable, always available if Drive is connected,
   but needs two different exports because no single format gives you everything:
   - `exportMimeType: text/csv` for plain values (checkbox state, COGS, currency-formatted
     `Selling price /Offer`, product names). The API returns this **base64-encoded**; decode it
     before parsing as CSV. This format flattens `=HYPERLINK(url,"label")` cells down to just the
     label ("WinningHunter", "Open shop"), so it's useless for the ad/competitor/AliExpress links.
   - `exportMimeType: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (XLSX)
     for the real URLs. Decode the base64 result to a `.xlsx` file and open it with `openpyxl`
     (`load_workbook(path, data_only=False)`) — reading a cell's `.value` on a hyperlink cell
     returns the **raw formula string**, e.g.
     `=HYPERLINK("https://app.winninghunter.com/ad/...","WinningHunter")`; pull the URL out of
     that. This also gives you the checkbox as a real Python `True`/`False`/`None`, no case-folding
     needed. Both exports return the whole workbook in one call — no way to request a row range —
     so expect a large response; read it back with a script (`jq`/`python`) rather than trying to
     eyeball the raw dump. `read_file_content` (the natural-language summary) is not reliable for
     this: it renders hyperlinks the same lossy way as the CSV, silently truncates before reaching
     rows deep in a 300+ row sheet, and can concatenate content from other tabs into the same
     response with no clear boundary — don't use it for anything beyond a quick sanity check.
   - The workbook has two tabs — `Winning Products` and `🏆  WINNERS LIBRARY` — open the sheet by
     name (`wb['Winning Products']`), not by index; sheet order isn't guaranteed.
   - There's no dedicated Google Sheets MCP connector to install — Google Drive is the first-party
     one, and this two-export approach is the reliable way to get everything out of it. Don't burn
     time re-searching the connector registry for one.

**Asana** — project `1204544103564278` ("1A. Pinterest - DE "),
<https://app.asana.com/1/1202393474006143/project/1204544103564278>, section `1204544103564283`
("1B. Create Product Page (Aireen)"). Reference task showing the house format and the house
naming: `1212348619651728` (`CeramiFix™`).

## Steps

### 1. Find the approved rows — in the last 20 products only

**The window is the last 20 products in the table**, not the whole sheet. Find the last row that
has a product in column `D`, take the twenty rows ending there, and consider only those. Within
that window, keep the rows whose "Approved For Asana" column (`AH` as of 2026-09-04 — re-verify
against row 4) reads as true.

That window is two research runs: `find-winning-products` delivers ten products per run, so the
bottom twenty rows are the two batches the operator has most recently been through — this gives
the operator a full run to review before it drops out of scope, rather than losing a batch the
moment the next run lands. Everything above them was decided weeks or months ago — a tick up
there is a record of a past decision, not a request to build something today, and re-reading it
is how a run drags eighty stale products back into the project. If the twenty-row window contains
no ticked rows, that is a real answer: report it and create nothing.

If you're reading via the CSV export, match the checkbox text **case-insensitively** — it comes
back `True`/`FALSE`, not `TRUE`, and a strict `-eq 'TRUE'` silently matches nothing. Reading via
the XLSX export with `openpyxl` avoids this entirely — the checkbox comes back as a real Python
`True`/`False`/`None`.

Do not use `find_in_spreadsheet` to locate the rows — it **caps at 50 results** and silently
truncates, and it also matches the word "true" inside ordinary prose in other columns. Read the
column and map positions to row numbers: index 0 of a read starting at row 5 is row 5.

The operator overrides the window whenever they say so — "just the last 10", "everything ticked",
"rows 250 to 262", "just the ones from Tuesday's run". Honour what they asked for; the twenty-row
window is only the default for a bare invocation.

### 2. Skip products that already have a task

The twenty-row window already keeps the old ticked rows out, but it does not make this step
optional: a run that was interrupted, or an operator who re-ticks a row, still lands the same
product twice. The project holds ~1,200 tasks and one duplicate inside it is invisible until the
page builder has already built it.

Because tasks are now named with a coined brand name that bears no resemblance to column `D`,
**name matching alone no longer works**. List the existing tasks across the **whole project**
(they get moved on to sections 1C/1E as work progresses), **including completed ones**, with
`opt_fields=name,notes`. Keep this response — step 4 reuses it as the register of coined names
already spent, so fetch it once. Match a sheet row against a task if **any** of these hit:

1. the WinningHunter ad id from `AA` appears in the task notes — the strongest key, unique per row;
2. the competitor URL from `AB` appears in the task notes;
3. the AliExpress item id from `AE` appears in the notes of an existing task — the sheet finds the
   same physical product under two different competitors, and those rows share a supplier item
   while sharing nothing else. Row 96 (hailiey.com) and row 147 (roseionly.com) are the same
   over-the-door shoe rack on item `1005010433467384`; row 96 is already live as `ShoeTidy™`, so
   row 147 must not become a second task;
4. the task name equals `TEST - <column D>` or `<column D>`, case-insensitively — this catches
   the legacy tasks created before the rename, and the ones a human has renamed slightly.

What remains is the batch to create. Tell the operator the arithmetic before you write anything —
"rows 301-320, 4 ticked, 1 already in Asana, creating 3" — naming the row range so they can see
which window you used and catch a miscount early. Inside a twenty-row window the batch is small
by construction; if a wider window was asked for and it comes back large (say more than 20),
confirm before creating rather than assuming.

### 3. Pull the details

`AA`, `AB`, `AC` and `AE` hold `=HYPERLINK(url,"label")` formulas, so a normal (CSV-style) read
returns "WinningHunter" / "Open shop" / "View ad" and not the URL. Read them via the XLSX +
`openpyxl` path from Sources and take the `.value` on each cell — that's the raw formula string;
extract the URL from inside it. Some rows store the AliExpress cell as a plain URL instead of a
formula — handle both.

`AG` (Selling price /Offer) is the opposite case: pull it from the **CSV export or a formatted
read, never from the formula/raw value**. The cell is currency-formatted, so a raw read returns
`34` where the operator actually wrote `34€` — and the `Note:` line is supposed to be their text
verbatim, currency symbol included.

Rows sourced from TikTok Shop can carry non-standard values in the competitor/ad-library
columns instead of a normal shop or Facebook link — e.g. a WinningHunter TikTok-listing URL, or
literal `n/a` text. That's real data, not a gap: write whatever is actually in the cell rather
than leaving the line blank or inventing a link.

### 4. Name the product

**Every task gets a coined house brand name — never the supplier's product name.** The old
`TEST - Joilens Car Headlight Restoration Kit` is exactly what this replaces; it became
`BeamRestore™`.

The name is **two words joined into one**, CamelCase, followed by `™`:

| Sheet product | Task name | The benefit it names |
|---|---|---|
| Joilens Car Headlight Restoration Kit | `BeamRestore™` | headlights restored to clear |
| NaturesRoots Organic Lymphatic Support Blend | `LymphFlow™` | lymph moving again |
| — | `HairThrive™` | hair that grows and holds |
| Minopia ceramic restoration formula | `CeramiFix™` | ceramic repaired |

Rules that make a name usable:

- **Name the benefit, not the category.** `BeamRestore` sells the outcome; `HeadlightKit` sells
  a shelf. The winning ad's hook in `Z` tells you which benefit the market is actually buying —
  build the name from that.
- **Two linked words, one token, CamelCase, `™` appended.** No spaces, no hyphens.
- **ASCII only, ~14 characters or fewer.** These names get baked into images and page copy across
  DE / NL / FR / EN stores; accents and umlauts fail in the image pipeline, so never use them.
- **Coin it — do not borrow it.** Never reuse the competitor's brand (Joilens, NaturesRoots,
  Minopia) or any real trademark.
- **Never coin the same name twice** — see below. This one is absolute.
- **Pronounceable in German.** The lead store is DE; if a German speaker would stumble over it,
  pick another pairing.

#### The name must be unique, forever

A repeated name is worse than an ugly one: two products carrying `HairThrive™` collide in Asana,
in PagePilot, in the image files, and in the store, and the page builder cannot tell which task
the assets belong to. **A name may be used once and never again**, including for a product that
was later killed — a dead test still owns its name.

Check against three registers before you settle on any name:

1. **Every task in the project**, all sections, **including completed ones** — this is the
   authoritative list of names already spent. You already fetched it in step 2 for the dedupe;
   reuse that same response rather than calling again.
2. **The names you assigned earlier in this same run.** Batches routinely contain two products in
   one niche, and the same benefit suggests the same name twice. Keep a set as you go and check
   each new name against it before moving to the next row.
3. **The four stores** — Zanaro, Modlia, Solundi, Nestilia. A name already on a live product is
   spent even if no Asana task carries it.

Compare **normalised**: lowercase, `™` stripped, spaces and punctuation removed. `HairThrive™`,
`hairthrive` and `Hair Thrive` are all the same name and all collide.

On a collision, **re-coin from a different benefit** — the product almost always has a second
angle worth naming (the speed, the feel, the surface it works on, the moment it is used).
`GlowRevive™` for one and `SheenGuard™` for another are two names; `HairThrive2™`,
`HairThriveX™` and `HairThrivePro™` are the same name wearing a hat, and are not acceptable.

Put the name in the marketing angle sentence too, the way the reference task does
("Restore cloudy, yellowed headlights … with BeamRestore™, a simple 4-step kit that …") — that is
where the page builder picks it up.

### 5. Create the tasks

Name: **`<CoinedName>™`** — no `TEST - ` prefix.

Notes follow the house template exactly — the trailing blank fields matter, because the page
builder fills them in:

```
marketing angle: <one or two sentences: what it is, who it is for, what it is sold on — naming the coined brand>

competitor's link: <url from AB>
aliexpress: <url from AE>
Note: <AG verbatim, e.g. "1+1: 39.99" — leave blank if AG is empty>

ad: <url from AA>
ad library: <url from AC, when it is a Meta ads-library link>
video: 

pagepilot:
ZANARO:
MODLIA:
SOLUNDI:
NESTILIA:

Our Store URL: 
```

Three lines carry all the rules worth stating twice:

- **`Note:`** holds **only** the `Selling price /Offer` cell (`AG`) — the offer and its price, e.g.
  `1+1: 39.99` or `2+1: 30.00`. It no longer carries the competitor's price or the COGS. `AG` is
  filled in by a colleague and is usually **still empty when you create the task**: leave the line
  bare after `Note:` in that case. Never compute, estimate, or back-fill an offer yourself.
- **`ad:`** is the WinningHunter link from `AA`
  (`https://app.winninghunter.com/ad/<id>?platform=facebook`), pasted whole, `?platform=` included.
- **`ad library:`** is the link from `AC`, **only when it applies** — that is, only when it is a
  `facebook.com/ads/library/?id=…` URL. Rows whose ad was found on Pinterest carry a
  `pinterest.com/pin/…` link in `AC` instead; Pinterest has no ads library, so leave the
  `ad library:` line blank there rather than putting a pin link on it. The WinningHunter link on
  `ad:` already reaches that creative.

Create with `create_tasks`, passing `default_project` and `section_id`. Leave assignee and due
date empty unless the operator says otherwise — the reference task has neither.

Write the **marketing angle** from the product and its hook: what the thing is, who it is for,
and the emotional or practical lever the competitor pulls. The hook (`Z` as of 2026-09-04) is the
competitor's own first line, so it tells you what is working. When it says `n/a - not captured`,
say so in the notes and tell the builder to read the landing page — an invented angle is worse
than an admitted gap.

### 6. Carry the warnings across

The master log holds real risk signals and they are worth surfacing where the work happens. Put
them on **one short line at the very end of the notes**, after `Our Store URL:`, prefixed
`risk:` — keeping them out of the `Note:` line, which now belongs to the offer alone. Only write
the line when there is a genuine concern:

- **Regulated claims** — supplements, biocides, medical or cosmetic effects. EU/DE rules bite on
  ad copy and the page, and the reference task flags exactly this kind of risk.
- **Thin margin** — where the competitor's price (`J`, currency in `I`) minus COGS (`AF`) leaves
  little room, the page will need a price test. Check this yourself even though neither number
  goes in the Note any more.
- **Missing hook or unverified price** — the builder must check the landing page first.
- **Currency mismatch** — some COGS figures in this sheet are USD, not EUR, and are labelled as
  such in the sheet's own notes. Do not silently present one as the other.

The "Main killer / risk" column (`Y` as of 2026-09-04) is where the research run recorded its
concern; read it.

## Report back

Give a table of what was created — coined name, the sheet product it came from, competitor price,
COGS, and a link to each task — then state the warnings you attached and why. The operator is
deciding what to build next from this, so the risky ones and the thin-margin ones are the useful
signal, not the count.

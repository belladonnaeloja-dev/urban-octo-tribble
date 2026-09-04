---
name: bestsellers-sync
description: 'Pull the top 100 best-selling products (by net items sold, trailing 30 days) from the Zanaro Berlin Shopify store and reconcile them against the Asana task "List of bestsellers to copy" (project "1E. Pinterest - US") two ways — (1) SYNC: insert any products missing from the list right after the last strikethrough entry and before the first normal-text entry; (2) RANK-SORT: among the normal-text (not-yet-strikethrough) entries only, reorder the ones that appear in the top 100 to the front, in rank order (best-seller first), leaving every strikethrough entry exactly where it is and untouched. Use when the user asks to sync bestsellers, update the bestsellers-to-copy list, check what''s newly trending, refresh the product-copy backlog from live Shopify sales data, or re-rank/reorder the list by sales.'
---

# Bestsellers sync (Shopify → Asana "List of bestsellers to copy")

Keeps the Asana product-copy backlog current with what's actually selling, and keeps the
un-actioned part of it prioritized by real sales rank. Read-only on Shopify. On Asana this skill
has exactly two effects, run independently or together: **adding** missing top-100 products, and
**reordering** normal-text entries by rank. It never edits, removes, or re-strikes an existing
line's content or status.

## Fixed IDs (this workspace)

- **Asana workspace:** `1202393474006143` (ecomjets.co)
- **Asana project** "1E. Pinterest - US": `1215906766476002`
- **Asana task** "List of bestsellers to copy": `1216293293149622`
- **Shopify store:** Zanaro Berlin (`zanaroberlin.com`) — verify with `get-shop-info` before
  running; if it doesn't match, stop and ask which store the user means before querying sales.

If a colleague runs this skill against a different workspace/store, re-derive these IDs first
(search Asana for the project/task by name, confirm the shop with `get-shop-info`) rather than
reusing the values above blind.

## Step 1 — Pull the top 100 by items sold (last 30 days)

Run, via `run-analytics-query`:

```
FROM sales SHOW net_items_sold GROUP BY product_title ORDER BY net_items_sold DESC LIMIT 100 SINCE -30d UNTIL today
```

`net_items_sold` is the right metric — it counts units sold, not revenue. Do not substitute
`gross_sales`/`net_sales` (those rank by revenue, not quantity) unless the user explicitly asks
for a revenue-based ranking instead. The row order returned **is** the rank (row 1 = rank 1 =
best-seller) — keep it, you'll need it for the RANK-SORT mode below.

## Step 2 — Extract the core product/brand name from each title

Shopify product titles here are marketing copy, not brand names, e.g.:

```
50% RABATT NUR HEUTE | StarScape™ - Galaxie Projektor
1+1 GRATIS HEUTE | KeySecure™ - Ihr Begleiter für die Selbstverteidigung
TapelessEdge™ | Perfekte Kanten ohne Abkleben! | KIT + 3 GRATIS Farbrollen
```

Strip the promo prefix (`50% RABATT NUR HEUTE |`, `N+N GRATIS HEUTE |`, or no prefix at all),
then take everything up to the first ` - `, ` | `, or the `™` symbol itself, whichever comes
first — that's the brand name (`StarScape™`, `KeySecure™`, `TapelessEdge™`). Discard the German
descriptor/offer copy after it entirely; it's not part of the product name and must never be
carried into the Asana list. Keep each name's rank (its position in the Step 1 results) attached
— you need both the name and the rank for everything that follows.

## Step 3 — Fetch the task and normalize both sides

Fetch the task's `html_notes` (not `notes` — see the formatting warning in Step 5) via `get_task`
with `opt_fields=html_notes`. Normalize every line — both the Asana entries and the Step 2 names —
before comparing, so casing, the `™` symbol, inline status text (` - DONE`, ` - duplicate`,
` - Already running...`, ` - recently created...`), punctuation and spacing don't cause false
negatives or missed matches:

1. Strip `™`.
2. Cut the line at the first status-marker substring listed above.
3. Lowercase, then strip everything that isn't `[a-z0-9]`.

Names on this list are frequently reused across markets with different casing (`Popmath` /
`PopMath`, `chicsling` / `ChicSling`, `Stylebrush` / `StyleBrush`) — this normalization is
required; a raw string match produces false "missing" results.

While reading `html_notes`, split every line into exactly one of two buckets and **keep them in
their original relative order within each bucket**:
- **Strikethrough** — wrapped in `<s>...</s>`.
- **Normal-text** — everything else (including blank lines, which travel with whichever line
  they're adjacent to and are otherwise ignored for matching purposes).

Also record the **strikethrough boundary**: the last strikethrough line before the first
normal-text line that follows it. Don't hardcode any specific pair of names as that boundary —
it moves over time as more items get crossed off. Always re-derive it from the live `html_notes`
on every run.

## Mode A — SYNC: add missing top-100 products

Run this when the user asks to sync/update/refresh the list against current sales.

A top-100 product is "on the list" if its normalized key (Step 3) matches any normalized existing
entry, strikethrough or not — don't re-add something just because it's already been struck
through.

**Insert every top-100 product that has no match anywhere in the list**, at the strikethrough
boundary: immediately after the last strikethrough entry and before the first normal-text entry.
Do not insert anywhere else.

Format each new line to match the surrounding plain entries exactly: same indent as its
neighbors (4 spaces is standard; check the actual file, some legacy lines carry 8), the name as
extracted in Step 2 (keep the `™`), no status suffix. New entries are always plain text, never
pre-struck-through.

## Mode B — RANK-SORT: reorder normal-text entries by sales rank

Run this when the user asks to reorder/re-rank/re-prioritize the list by sales.

**Only touch the normal-text bucket. Never move, edit, or re-strike a strikethrough entry —
skip it entirely, wherever it sits in the list.**

Within the normal-text bucket:
1. Split it into two groups: entries whose normalized key matches a top-100 product (**ranked**),
   and everything else (**unranked**).
2. Sort the ranked group by its Shopify rank ascending (rank 1 = best-seller = first).
3. Rebuild the bucket as: ranked group (in rank order) followed by the unranked group, **in its
   original relative order, untouched**. Do not sort, alphabetize, or otherwise touch the
   unranked group's internal order.
4. Splice this rebuilt bucket back in starting exactly at the strikethrough boundary. The
   strikethrough bucket above it is untouched, in its original order, in its original position.

If a product exists in the list more than once in the normal-text bucket (a genuine duplicate,
not yet cleaned up), rank-sort each occurrence independently by the same key — don't collapse or
dedupe as part of this skill; that's a separate cleanup task.

## Modes can run together

A single request ("sync and re-rank", "update the list") can invoke both: run Mode A first
(insert the newly-missing products as plain entries), then Mode B (which will naturally pick up
the just-inserted entries if they're in the top 100, since they're now part of the normal-text
bucket). Report both effects separately (see Step 5).

## Step 4 — Write it back

**How:** Asana's plain `notes` field silently discards all rich formatting — never fetch or
write this task via `notes`. Always read and write `html_notes`.

**Asana's task update replaces the entire field — there is no partial/append/reorder primitive.**
Reconstruct the full body: strikethrough bucket first (unchanged, original order), then the
rebuilt normal-text bucket (Mode A insertions applied, then Mode B reordering applied, or
whichever subset of modes ran). Every existing `<s>` tag, per-line indentation quirk, and inline
status annotation must survive verbatim on every line you didn't intentionally touch.

`&` inside item names must be XML-escaped as `&amp;` to keep the body well-formed.

## Step 5 — Report

State clearly, for whichever mode(s) ran:
- **Mode A:** how many of the top 100 were already on the list vs. newly added (name each added
  product), and the exact insertion point (the two neighboring entries it landed between).
- **Mode B:** which normal-text entries were matched to a top-100 rank and their new order (name
  + rank for each), and confirm every unranked normal-text entry kept its original relative order
  and every strikethrough entry kept its exact original position.
- Either way: confirm no strikethrough entry was altered, moved, or had its status text changed.

## Honesty rules

- Never guess a product's brand name from memory — always derive it from the live Shopify title
  per Step 2, for every run.
- If `html_notes` and `notes` disagree in a way that suggests the task was edited outside this
  skill's format (e.g. a `notes`-only edit that stripped formatting), say so before writing
  anything back — don't silently overwrite a change you can't account for.
- If Mode A finds zero missing products, or Mode B finds zero rank matches in the normal-text
  bucket, say so plainly and make no write for that mode.

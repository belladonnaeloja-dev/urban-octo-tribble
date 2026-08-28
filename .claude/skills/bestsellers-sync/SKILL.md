---
name: bestsellers-sync
description: Pull the top 50 best-selling products (by net items sold, trailing 30 days) from the Zanaro Berlin Shopify store, cross-check them against the Asana task "List of bestsellers to copy" (project "1E. Pinterest - US"), and insert any products missing from that list at the correct spot — right after the last strikethrough entry and before the first normal-text entry. Use when the user asks to sync bestsellers, update the bestsellers-to-copy list, check what's newly trending against the copy list, or refresh the product-copy backlog from live Shopify sales data.
---

# Bestsellers sync (Shopify → Asana "List of bestsellers to copy")

Keeps the Asana product-copy backlog current with what's actually selling. Read-only on
Shopify, additive-only on Asana — this skill never removes or reorders existing entries.

## Fixed IDs (this workspace)

- **Asana workspace:** `1202393474006143` (ecomjets.co)
- **Asana project** "1E. Pinterest - US": `1215906766476002`
- **Asana task** "List of bestsellers to copy": `1216293293149622`
- **Shopify store:** Zanaro Berlin (`zanaroberlin.com`) — verify with `get-shop-info` before
  running; if it doesn't match, stop and ask which store the user means before querying sales.

## Step 1 — Pull the top 50 by items sold (last 30 days)

Run, via `run-analytics-query`:

```
FROM sales SHOW net_items_sold GROUP BY product_title ORDER BY net_items_sold DESC LIMIT 50 SINCE -30d UNTIL today
```

`net_items_sold` is the right metric — it counts units sold, not revenue. Do not substitute
`gross_sales`/`net_sales` (those rank by revenue, not quantity) unless the user explicitly asks
for a revenue-based ranking instead.

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
carried into the Asana list.

## Step 3 — Cross-check against the Asana task

Fetch the task's `html_notes` (not `notes` — see the formatting warning below) via `get_task`
with `opt_fields=html_notes`. Normalize both sides before comparing so casing, the `™` symbol,
inline status text (` - DONE`, ` - duplicate`, ` - Already running...`, ` - recently created...`),
punctuation and spacing don't cause false negatives:

1. Strip `™`.
2. Cut the line at the first status-marker substring listed above.
3. Lowercase, then strip everything that isn't `[a-z0-9]`.

A product is "on the list" if its normalized key matches any normalized existing entry.
Names on this list are frequently reused across markets with different casing (`Popmath` /
`PopMath`, `chicsling` / `ChicSling`, `Stylebrush` / `StyleBrush`) — the normalization above is
required, a raw string match will produce false "missing" results.

## Step 4 — Insert only what's genuinely missing, at the correct position

**Where:** immediately after the **last strikethrough (`<s>...</s>`) entry** in the list and
immediately before the **first normal-text entry** that follows it. Do not insert anywhere else,
and do not touch, reorder, or re-strike any existing line — this skill is purely additive.

Find the boundary by scanning `html_notes` top-to-bottom for the last line wrapped in `<s>...</s>`
before a run of un-wrapped lines begins; that un-wrapped line is the insertion's lower bound.
(At the time this skill was written that boundary sat between `SteamPress` and `EmbroiDiary` —
**don't hardcode that pair**, the strikethrough boundary moves over time as more items get
crossed off. Always re-derive it from the live `html_notes`.)

**Format of each new line** — match the surrounding plain (non-strikethrough) entries exactly:
4-space indent, the name as extracted in Step 2 (keep the `™`), no status suffix, one per line.
New entries are plain text, never pre-struck-through.

**How to write it back:** Asana's plain `notes` field silently discards all rich formatting —
never fetch or write this task via `notes`. Always read and write `html_notes`, and always
reconstruct the **entire** body (Asana's task update replaces the whole field, there is no
partial/append primitive) — copy the fetched `html_notes` verbatim except for the newly inserted
lines, so every existing `<s>` tag, indentation quirk (some lines carry 8 spaces, not 4 — leave
those as-is), and inline status annotation survives untouched. `&` inside item names must be
XML-escaped as `&amp;` to keep the body well-formed.

## Step 5 — Report

State clearly:
- How many of the top 50 were already on the list vs. newly added (name each added product).
- The exact insertion point used (the two neighboring entries it was inserted between).
- Confirm no existing line was altered, reordered, or had its strikethrough changed.

## Honesty rules

- Never guess a product's brand name from memory — always derive it from the live Shopify title
  per Step 2.
- If `html_notes` and `notes` disagree in a way that suggests the task was edited outside this
  skill's format (e.g. someone added a `notes`-only edit that stripped formatting), say so before
  writing anything back — don't silently overwrite a change you can't account for.
- If zero products are missing, say so plainly and make no write.

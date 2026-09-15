# Store map

Language, currency and brand identity for each of the user's Shopify stores.
The **language column is what drives the whole clone** — read it, state it back
to the user in Phase 0, and only then start translating.

Rows marked *verified* were read from the live store with `get-shop-info` +
`shopLocales`. Rows marked *unverified* come from how the user refers to the
store in requests; confirm them with `get-shop-info` the first time you land on
that store, then update this file so the next run doesn't have to.

| Store | Domain | Language (primary locale) | Currency | Page builder | Notes |
|---|---|---|---|---|---|
| **Zanaro Berlin** ("Zanaro") | `zanaroberlin.com` | German (`de`) — unverified, inferred from store name and the bestsellers-sync skill | EUR — unverified | PagePilot | The usual **source** store: most winning pages are built here first. |
| **Nestilia** | `nestilia.com` | English (`en`) — verified 2026-09-14 | USD — verified 2026-09-14 | PagePilot (`sections/pp-*` present in MAIN theme, verified) | Registered in the Netherlands, sells in English at USD prices. Do **not** infer Dutch from the country field. Brand color `#04b67b`, border radius `12` (read from an existing PagePilot template on 2026-09-14 — re-read per run, it can change). **Trust bullets under the price:** always the block in `trust-bullets-nestilia.html` (PayPal / free US & Canada shipping / 30-day returns). |
| **Modlia** | `modlia.fr` | French (`fr`) — verified 2026-09-14 | EUR — verified 2026-09-14 | PagePilot (14 `snippets/pb-*` plus `sections/pp-*`, verified) | Registered in the Netherlands, sells in French at EUR prices. Support email contact@modlia.fr. |
| **Solundi** | *unknown* | *unknown* — ask | *unknown* | *confirm* | Never guess this one; the user has not stated its language anywhere. |
| "my Dutch store" | *unknown* | Dutch (`nl`) | *unknown* | *confirm* | The user refers to a Dutch-language store without naming it. When they do, ask which store they mean, then fill this row in. |

## How to verify a row

On the store in question (before or after `switch-shop`, whichever side of the
run you're on):

```graphql
{ shop { name myshopifyDomain primaryDomain { host } currencyCode }
  shopLocales { locale primary published } }
```

The `primary: true` locale is the language to translate into. If several
locales are published, translate into the primary one and mention the others in
the report — cloning translations for secondary locales is a separate
`translationsRegister` job.

## When a store isn't in this table

Ask the user which language it sells in. Do not infer it from the TLD (every
store here is a `.com`), from the shop's registered country (Nestilia is a
Dutch company selling in English), or from the currency (USD is used by
non-US stores). One question up front is far cheaper than a page translated
into the wrong language.

## Brand identity per store

Colors and radii are read live from an existing PagePilot template on the
destination (`references/shopify-recipes.md`, "Read the destination's brand
styling"), because they live in the template's `main` section, not in a
global setting, and the user changes them. The values noted above are a
fallback if the destination has no PagePilot template yet.

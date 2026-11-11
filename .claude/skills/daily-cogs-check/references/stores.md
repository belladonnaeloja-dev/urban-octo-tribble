# Stores

Zendrop store IDs (from `get_stores`, checked 2026-11-11):

| Zendrop store_id | Store | myshopify domain | Shop currency |
|---|---|---|---|
| 3243654 | Zanaro Berlin | bycheri.myshopify.com | EUR |
| 3448119 | Solundi.com | solundi-com.myshopify.com | EUR |
| 3468999 | MODLIA | ccae3b-2.myshopify.com | EUR |
| 3181456 | Nestilia | 3d465e-2.myshopify.com | USD |

Zendrop costs are always in USD, whatever the shop currency.

## What the order statuses mean for COGS

Seen on Zanaro Berlin, 2026-11-10 (109 orders):

| Status | Count | Cost in `get_orders` `total` |
|---|---|---|
| Shipped | 62 | actual cost (e.g. 1.77 = 0.79 product + 0.98 shipping) |
| Processing | 4 | actual cost once invoiced |
| Unfulfilled | 13 | 0 — mostly "Please link the product" / product removed from Zendrop |
| External | 22 | 0 — fulfilled outside Zendrop |
| Canceled | 8 | excluded |

`get_orders_breakdown`'s `total` leaves out External orders, so it is lower
than `get_orders`' `total`. Use `get_orders` for the order count.

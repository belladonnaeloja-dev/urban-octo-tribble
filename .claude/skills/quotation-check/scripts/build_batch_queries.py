#!/usr/bin/env python3
"""
Build batched, aliased Shopify Admin GraphQL queries to look up many
products' current selling price by title in a handful of round trips instead
of one call per product.

Why batching: the Shopify MCP's graphql_query tool takes one query per call,
and each call is a real API round trip. Looking up 100 bestseller titles one
at a time is 100 calls; aliasing ~20 products per query cuts that to ~5.

Usage:
    python3 build_batch_queries.py titles.json --batch-size 20 --out-dir batches/

titles.json is a JSON array of product title strings (e.g. the
product_title values from a ShopifyQL best-sellers query -- see
references/shopifyql_bestsellers.md in this skill).

For each batch this writes:
    batches/batch_<i>_query.txt   -- the GraphQL query string
    batches/batch_<i>_vars.json   -- the variables object

Call the Shopify MCP's graphql_query tool once per batch, passing the
contents of these two files as `query` and `variables`. Each aliased field
(p0, p1, ...) returns up to 5 candidate products for that title so you can
spot duplicates/test listings (see references/matching_notes.md for how to
pick among them).
"""
import argparse
import json
import os


def build_batch(batch_titles, start_idx, first=5):
    fields = []
    vars_def = []
    vars_obj = {}
    for i, t in enumerate(batch_titles):
        idx = start_idx + i
        alias, varname = f"p{idx}", f"q{idx}"
        fields.append(
            f"{alias}: products(first: {first}, query: ${varname}) "
            f"{{ edges {{ node {{ title priceRangeV2 {{ minVariantPrice {{ amount }} }} }} }} }}"
        )
        vars_def.append(f"${varname}: String")
        vars_obj[varname] = t
    query = "query(" + ", ".join(vars_def) + ") { " + " ".join(fields) + " }"
    return query, vars_obj


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("titles_json", help="JSON file containing an array of product title strings")
    ap.add_argument("--batch-size", type=int, default=20,
                     help="Products per query. 20 keeps query text and response size comfortable; "
                          "raise cautiously if you hit round-trip limits, lower if queries get rejected as too complex.")
    ap.add_argument("--out-dir", default="batches")
    args = ap.parse_args()

    titles = json.load(open(args.titles_json, encoding="utf-8"))
    os.makedirs(args.out_dir, exist_ok=True)

    batches = [titles[i:i + args.batch_size] for i in range(0, len(titles), args.batch_size)]
    for bi, batch in enumerate(batches):
        query, variables = build_batch(batch, bi * args.batch_size)
        with open(os.path.join(args.out_dir, f"batch_{bi}_query.txt"), "w", encoding="utf-8") as f:
            f.write(query)
        with open(os.path.join(args.out_dir, f"batch_{bi}_vars.json"), "w", encoding="utf-8") as f:
            json.dump(variables, f, ensure_ascii=False)
        print(f"batch {bi}: {len(batch)} titles -> {args.out_dir}/batch_{bi}_query.txt / _vars.json")

    print(f"\n{len(batches)} batch(es) for {len(titles)} titles. "
          f"Run each through the Shopify MCP graphql_query tool, in order.")


if __name__ == "__main__":
    main()

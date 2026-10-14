#!/usr/bin/env python3
"""Extract a theme template body from a spilled graphql_query result, UTF-8 safe.

Usage:
    python3 extract-template.py <spill-file.txt> <out-template.json> [<out-manifest.json>]

The Shopify MCP spills large query results to a tool-results .txt file that is JSON
of the shape {data: {theme: {files: {nodes: [{filename, body: {content}}]}}}}.
This script:
  1. reads that file as UTF-8 (reading it as ANSI/cp1252 is what produces mojibake like "Ã¼"),
  2. writes the template body to <out-template.json> as UTF-8 without BOM,
  3. checks the body parses as JSON after stripping the auto-generated /* ... */ header
     Shopify puts at the top of template files,
  4. prints every shopify://shop_images/<filename> reference (the ?v=... cache suffix
     stripped, since the `files` query matches on the bare filename) and, when a third
     argument is given, writes them to a manifest JSON alongside the template.

Standard library only. Works on the same spill file layout on Windows, macOS and Linux.
"""
import json
import re
import sys


def find_content(node):
    """Depth-first search for the first {filename, body:{content}} theme-file node."""
    if isinstance(node, dict):
        if "body" in node and isinstance(node["body"], dict) and "content" in node["body"]:
            return node.get("filename"), node["body"]["content"]
        for v in node.values():
            found = find_content(v)
            if found:
                return found
    elif isinstance(node, list):
        for v in node:
            found = find_content(v)
            if found:
                return found
    return None


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    spill, out_template = sys.argv[1], sys.argv[2]
    out_manifest = sys.argv[3] if len(sys.argv) > 3 else None

    with open(spill, encoding="utf-8") as f:
        payload = json.load(f)
    found = find_content(payload)
    if not found:
        print("no theme file body found in spill file")
        return 1
    filename, body = found

    with open(out_template, "w", encoding="utf-8", newline="") as f:
        f.write(body)

    stripped = re.sub(r"^\s*/\*.*?\*/\s*", "", body, flags=re.S)
    template = json.loads(stripped)  # raises if the template is not valid JSON
    sections = template.get("sections", {})
    print(f"{filename}: {len(body.encode('utf-8'))} bytes, {len(sections)} sections, JSON OK")
    for sid, sec in sections.items():
        print(f"  {sid}: {sec.get('type')} ({len(sec.get('blocks', {}))} blocks)")

    refs = sorted({m.split("?")[0] for m in re.findall(r"shopify://shop_images/[^\"'\\\s]+", body)})
    print(f"{len(refs)} shop_images references:")
    for r in refs:
        print("  " + r)

    if out_manifest:
        with open(out_manifest, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "source_template_filename": filename,
                    "shop_images": [r.replace("shopify://shop_images/", "") for r in refs],
                },
                f,
                indent=2,
                ensure_ascii=False,
            )
        print(f"manifest written: {out_manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

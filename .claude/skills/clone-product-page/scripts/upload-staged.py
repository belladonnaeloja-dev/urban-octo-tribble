#!/usr/bin/env python3
"""POST a local file to a Shopify staged-upload target (non-Windows twin of upload-staged.ps1).

Usage:
    python3 upload-staged.py <file> <staged-target.json>

<staged-target.json> is stagedTargets[0] from stagedUploadsCreate, saved verbatim
({"url":..., "resourceUrl":..., "parameters":[{"name":..,"value":..}, ...]}).
Signed parameters are sent first and the file part last, which the storage backend
requires. Prints the local size + md5 (compare with the theme file's checksumMd5
after themeFilesUpsert) and the resourceUrl on the last line.

Standard library only.
"""
import hashlib
import json
import mimetypes
import os
import sys
import urllib.request
import uuid


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    file_path, target_path = sys.argv[1], sys.argv[2]
    with open(target_path, encoding="utf-8") as f:
        target = json.load(f)
    if "url" not in target or "parameters" not in target:
        print("target JSON must contain 'url' and 'parameters' (save stagedTargets[0] verbatim)")
        return 2

    with open(file_path, "rb") as f:
        data = f.read()
    key = next((p["value"] for p in target["parameters"] if p["name"] == "key"), None)
    file_name = os.path.basename(key) if key else os.path.basename(file_path)
    mime = mimetypes.guess_type(file_path)[0] or "text/plain"

    boundary = "----clone-product-page-" + uuid.uuid4().hex
    parts = []
    for p in target["parameters"]:
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\"\r\n\r\n{p['value']}\r\n".encode("utf-8")
        )
    parts.append(
        (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{file_name}\"\r\n"
            f"Content-Type: {mime}\r\n\r\n"
        ).encode("utf-8")
        + data
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(parts)

    req = urllib.request.Request(
        target["url"],
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req) as resp:
        status = resp.status
    if status not in (200, 201, 204):
        print(f"upload failed: HTTP {status}")
        return 1

    print(f"Upload OK. local size={len(data)} local md5={hashlib.md5(data).hexdigest()}")
    print("resourceUrl:")
    print(target["resourceUrl"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Publish the finished news image for the 23 November 2026 bounty.

The artwork already exists as asset.jpg next to this file: a front page
summing up Monday 23 November 2026 — COP31 collapsing with no
fossil-fuel deal, Houthi strikes on a Saudi refinery, a Kyiv drone
strike with 14 missing, plus a ticker with the Benghazi warship hit,
the Indonesia factory fire and the Lisbon march.

This script does not draw or alter anything. It copies that file into
the harness output directory as entry.png (the rules accept JPEG bytes
under that name) and then proves the copy is exact by comparing both
the file size and the SHA-256 digest.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "asset.jpg"
DEST_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
JPEG_START = b"\xff\xd8\xff"
JPEG_END = b"\xff\xd9"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def sha256_of(path):
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message):
    """Print an error to stderr and return the failure exit code."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def looks_like_jpeg(path):
    """Check the file starts with a JPEG SOI marker and ends with EOI."""
    with open(path, "rb") as handle:
        head = handle.read(len(JPEG_START))
        handle.seek(-len(JPEG_END), os.SEEK_END)
        tail = handle.read(len(JPEG_END))
    return head == JPEG_START and tail == JPEG_END


def jpeg_dimensions(path):
    """Read width and height from the first JPEG SOF marker, or None.

    Walks the JPEG marker segments with the standard library only: each
    segment starts with 0xFF, a marker byte, then a 2-byte big-endian
    length. SOF0/SOF2 (0xC0/0xC2) hold height then width as 2-byte values.
    """
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:2] != b"\xff\xd8":
        return None
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        size = int.from_bytes(data[pos + 2:pos + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2, 0xC3):
            height = int.from_bytes(data[pos + 5:pos + 7], "big")
            width = int.from_bytes(data[pos + 7:pos + 9], "big")
            return width, height
        pos += 2 + size
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    if not os.path.isfile(source):
        return fail(f"{SOURCE_NAME} not found next to main.py: {source}")
    if os.path.getsize(source) == 0:
        return fail(f"{SOURCE_NAME} is empty: {source}")
    if not looks_like_jpeg(source):
        return fail(f"{SOURCE_NAME} is not a JPEG file: {source}")
    if os.path.getsize(source) > MAX_BYTES:
        return fail(
            f"{SOURCE_NAME} is {os.path.getsize(source)} bytes, over the "
            f"{MAX_BYTES}-byte limit"
        )
    dims = jpeg_dimensions(source)
    if dims is None:
        return fail(f"could not read JPEG dimensions of {SOURCE_NAME}")
    if dims[0] > MAX_SIDE or dims[1] > MAX_SIDE:
        return fail(
            f"{SOURCE_NAME} is {dims[0]}x{dims[1]}, over the "
            f"{MAX_SIDE}x{MAX_SIDE} limit"
        )
    print(f"{SOURCE_NAME} is {dims[0]}x{dims[1]}, within the size limits")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, DEST_NAME)

    shutil.copyfile(source, dest)

    if os.path.getsize(dest) != os.path.getsize(source):
        return fail(
            f"size mismatch after copy: {dest} is "
            f"{os.path.getsize(dest)} bytes, expected {os.path.getsize(source)}"
        )
    if sha256_of(dest) != sha256_of(source):
        return fail(f"SHA-256 mismatch after copy: {dest}")

    print(f"wrote {dest} ({os.path.getsize(dest)} bytes, sha256 {sha256_of(source)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

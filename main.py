#!/usr/bin/env python3
"""Entry for the-passport-page-of-a-countr-2-20261121-0318.

Writes the invented passport spread for the Republic of Talvera to
/output/entry.png.

The spread is drawn once, by the builder, and stored beside this file as
entry.png. This program copies it byte for byte to the output directory
so the run is deterministic: the same input bytes always produce the
same output bytes. It uses only the Python standard library and no
network access.

Output directory: /output/entry.png by default; set MAKEFUN_OUTPUT_DIR
to write elsewhere (for example, MAKEFUN_OUTPUT_DIR=out).
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "2cae015d433ce81edac8da2c6cef4115e61d7ed34f42db5151ebcadd00959e7c"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_dimensions(path):
    """Read width and height from a PNG's IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        header = f.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png not found beside main.py", file=sys.stderr)
        return 1
    dims = png_dimensions(SOURCE)
    if dims != (1024, 1024):
        print("entry.png is not 1024x1024: %r" % (dims,), file=sys.stderr)
        return 1
    if EXPECTED_SHA256 != "PLACEHOLDER":
        actual = sha256_of(SOURCE)
        if actual != EXPECTED_SHA256:
            print("entry.png sha256 mismatch: %s != %s"
                  % (actual, EXPECTED_SHA256), file=sys.stderr)
            return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if sha256_of(dest) != sha256_of(SOURCE):
        print("copy verification failed", file=sys.stderr)
        return 1
    size = os.path.getsize(dest)
    if size > 1048576:
        print("entry.png exceeds 1 MiB: %d bytes" % size, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dest, size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

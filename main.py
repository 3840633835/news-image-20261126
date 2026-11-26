#!/usr/bin/env python3
"""Graded entrypoint for the news-image-20261126 entry.

The grading container installs nothing, so this file is standard
library only. It copies the finished front page (entry.png, already in
this repository) to /output/entry.png, byte for byte.

Run:  python3 main.py            (writes /output/entry.png)
      OUTPUT_DIR=/tmp/out python3 main.py   (writes elsewhere)
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    print("copied", src, "->", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())

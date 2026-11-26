#!/bin/sh
# Determinism check for the news-image-20261126 entry.
# Rebuilds the front page twice and copies it twice; every output must
# be byte-identical to the committed entry.png.
set -e
cd "$(dirname "$0")"

echo "== generate.py x2 =="
python3 generate.py
sha256sum entry.png > /tmp/det_a.txt
python3 generate.py
sha256sum entry.png > /tmp/det_b.txt
cmp /tmp/det_a.txt /tmp/det_b.txt && echo "generate: byte-identical"

echo "== main.py x2 =="
rm -rf /tmp/det_out1 /tmp/det_out2
OUTPUT_DIR=/tmp/det_out1 python3 main.py
OUTPUT_DIR=/tmp/det_out2 python3 main.py
cmp /tmp/det_out1/entry.png /tmp/det_out2/entry.png && echo "main: byte-identical"
cmp /tmp/det_out1/entry.png entry.png && echo "main output == repo entry.png"

echo "== image sanity =="
python3 -c "
from PIL import Image
im = Image.open('entry.png')
assert im.size == (1024, 1024), im.size
assert im.mode == 'RGB', im.mode
im.verify()
import os
assert os.path.getsize('entry.png') <= 1024 * 1024
print('1024x1024 RGB, <=1 MiB, Pillow verify ok')
"
echo "ALL CHECKS PASSED"

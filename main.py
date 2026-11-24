#!/usr/bin/env python3
"""Place the front page where the grader expects it.

The image itself is drawn by draw_image.py and shipped in this
repository as entry.png; this program only copies it to the output
directory. Standard library only, no network, no sibling imports:
the grader runs with `python3 -P -s`, so nothing outside this file
is on sys.path.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    src = HERE / "entry.png"
    if not src.is_file():
        raise SystemExit(f"missing image next to this program: {src}")
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / "entry.png"
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)


if __name__ == "__main__":
    main()

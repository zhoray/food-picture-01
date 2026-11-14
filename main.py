"""Deliver the entry image as entry.png.

The competition image picture.jpg is a JPEG, but the required output name is
entry.png. The bytes must stay exactly the original JPEG bytes, copied
verbatim under the PNG name.
"""

import os
import sys
from pathlib import Path

SOURCE_NAME = "picture.jpg"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def main() -> int:
    source = Path(__file__).resolve().parent / SOURCE_NAME
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    output = output_dir / OUTPUT_NAME

    try:
        image_bytes = source.read_bytes()
    except OSError:
        print(f"error: cannot read {source}", file=sys.stderr)
        return 1

    if not image_bytes or not image_bytes.startswith(b"\xff\xd8"):
        print(f"error: {SOURCE_NAME} is not a valid JPEG file", file=sys.stderr)
        return 1

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        output.write_bytes(image_bytes)
    except OSError:
        print(f"error: cannot write {output}", file=sys.stderr)
        return 1

    if output.stat().st_size != len(image_bytes):
        print(
            f"error: wrote {output.stat().st_size} bytes to {output}, "
            f"expected {len(image_bytes)}",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {len(image_bytes)} bytes to {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Export selected photos as optimized WebP assets for the website."""

import json
import pathlib

from PIL import Image


MAX_DIMENSION = 1600
QUALITY = 75


def main():
    project = pathlib.Path(__file__).resolve().parent.parent
    selection = json.loads(
        (project / "classement" / "selection.json").read_text(encoding="utf-8")
    )
    output_dir = project / "assets" / "images"

    for item in selection:
        source = pathlib.Path(item["source"])
        target = output_dir / item["target"]
        with Image.open(source) as im:
            im = im.convert("RGB")
            im.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)
            im.save(
                target,
                format="WEBP",
                quality=QUALITY,
                method=6,
            )
        size_kb = target.stat().st_size / 1024
        print(f"{item['target']:24} {size_kb:8.1f} KB  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()

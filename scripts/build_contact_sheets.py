#!/usr/bin/env python3
"""Build labeled contact sheets for a folder of photos."""

import json
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont


FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def slugify(name):
    keep = "".join(ch if ch.isalnum() else "-" for ch in name)
    return keep.strip("-")[:40] or "sheet"


def collect_photos(source_root):
    root = pathlib.Path(source_root)
    groups = {}
    for category_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        files = sorted(
            p
            for p in category_dir.iterdir()
            if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".heic"}
        )
        if files:
            groups[category_dir.name] = files
    root_files = sorted(
        p
        for p in root.iterdir()
        if p.is_file()
        and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".heic"}
    )
    if root_files:
        groups["Racine"] = root_files
    return groups


def draw_contact_sheet(files, output_path, font):
    cols, rows = 4, 4
    thumb_w, thumb_h = 360, 240
    label_h = 44
    pad = 14
    header_h = 64
    page_w = cols * thumb_w + (cols + 1) * pad
    page_h = header_h + rows * (thumb_h + label_h + pad) + pad

    canvas = Image.new("RGB", (page_w, page_h), "#0f1115")
    draw = ImageDraw.Draw(canvas)
    title_font = load_font(28)
    label_font = load_font(20)

    draw.text((pad, 18), output_path.stem, fill="#f5d68a", font=title_font)

    for index, image_path in enumerate(files[: cols * rows]):
        col = index % cols
        row = index // cols
        x = pad + col * (thumb_w + pad)
        y = header_h + row * (thumb_h + label_h + pad)

        try:
            with Image.open(image_path) as im:
                im = im.convert("RGB")
                im.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                box = Image.new("RGB", (thumb_w, thumb_h), "#1b1e26")
                box.paste(im, ((thumb_w - im.width) // 2, (thumb_h - im.height) // 2))
                canvas.paste(box, (x, y))
        except OSError as exc:
            draw.rectangle((x, y, x + thumb_w, y + thumb_h), fill="#451111")
            draw.text((x + 8, y + 8), str(exc), fill="#ffffff", font=label_font)

        name = image_path.name
        if len(name) > 34:
            name = name[:31] + "..."
        draw.text((x + 2, y + thumb_h + 8), name, fill="#e8e8e8", font=label_font)

    canvas.save(output_path, quality=88)


def main():
    source_root = sys.argv[1]
    output_dir = pathlib.Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    groups = collect_photos(source_root)
    manifest = []

    for category, files in groups.items():
        for batch_index in range(0, len(files), 16):
            batch = files[batch_index : batch_index + 16]
            sheet_name = f"{slugify(category)}-{batch_index // 16 + 1:02d}"
            output_path = output_dir / f"{sheet_name}.jpg"
            draw_contact_sheet(batch, output_path, load_font(20))
            manifest.append(
                {
                    "sheet": output_path.name,
                    "category": category,
                    "files": [str(p) for p in batch],
                }
            )

    with open(output_dir / "manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)

    for item in manifest:
        print(f"{item['sheet']}: {len(item['files'])} photos")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Rank photos by objective technical quality metrics."""

import concurrent.futures
import json
import pathlib
import statistics
import sys

from PIL import Image, ImageFilter, ImageStat


SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


def collect_photos(source_root):
    root = pathlib.Path(source_root)
    groups = {}
    for category_dir in sorted([p for p in root.iterdir() if p.is_dir()]):
        files = sorted(
            p for p in category_dir.iterdir() if p.suffix.lower() in SUPPORTED
        )
        if files:
            groups[category_dir.name] = files
    root_files = sorted(
        p
        for p in root.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )
    if root_files:
        groups["Racine"] = root_files
    return groups


def analyze_file(category, path):
    item = {
        "category": category,
        "path": str(path),
        "name": path.name,
        "error": None,
    }
    try:
        with Image.open(path) as source:
            source = source.convert("RGB")
            width, height = source.size
            source.thumbnail((900, 900), Image.Resampling.LANCZOS)
            gray = source.convert("L")

            edges = gray.filter(ImageFilter.FIND_EDGES)
            sharpness = ImageStat.Stat(edges).var[0]
            brightness = ImageStat.Stat(gray).mean[0]
            contrast = ImageStat.Stat(gray).stddev[0]
            hsv = source.convert("HSV")
            saturation = ImageStat.Stat(hsv).mean[1]

            item.update(
                {
                    "width": width,
                    "height": height,
                    "aspect": round(width / height, 3),
                    "sharpness": round(sharpness, 2),
                    "brightness": round(brightness, 1),
                    "contrast": round(contrast, 1),
                    "saturation": round(saturation, 1),
                    "file_size_kb": round(path.stat().st_size / 1024, 1),
                }
            )
    except Exception as exc:  # noqa: BLE001
        item["error"] = str(exc)
    return item


def percentile_rank(values, value):
    if not values:
        return 0.5
    count = sum(1 for v in values if v <= value)
    return count / len(values)


def add_scores(items):
    metric_keys = ["sharpness", "brightness", "contrast", "saturation", "resolution"]
    for item in items:
        item["resolution"] = item.get("width", 0) * item.get("height", 0)

    valid = [i for i in items if not i.get("error")]
    for item in valid:
        item["rank_sharpness"] = percentile_rank(
            [i["sharpness"] for i in valid], item["sharpness"]
        )
        brightness_values = [i["brightness"] for i in valid]
        item["exposure_score"] = 1 - abs(
            percentile_rank(brightness_values, item["brightness"]) - 0.5
        ) * 2
        item["rank_contrast"] = percentile_rank(
            [i["contrast"] for i in valid], item["contrast"]
        )
        item["rank_saturation"] = percentile_rank(
            [i["saturation"] for i in valid], item["saturation"]
        )
        item["rank_resolution"] = percentile_rank(
            [i["resolution"] for i in valid], item["resolution"]
        )
        item["score"] = round(
            item["rank_sharpness"] * 0.30
            + item["exposure_score"] * 0.20
            + item["rank_contrast"] * 0.15
            + item["rank_saturation"] * 0.20
            + item["rank_resolution"] * 0.15,
            3,
        )
        item["flags"] = []
        if item["sharpness"] < statistics.median([i["sharpness"] for i in valid]) * 0.4:
            item["flags"].append("nettete faible")
        if item["brightness"] < 45:
            item["flags"].append("sous-expose")
        elif item["brightness"] > 210:
            item["flags"].append("sur-expose")
    return valid


def main():
    source_root = sys.argv[1]
    output_dir = pathlib.Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)
    groups = collect_photos(source_root)

    tasks = [
        (category, path)
        for category, files in groups.items()
        for path in files
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda t: analyze_file(*t), tasks))

    ranked = add_scores(results)
    ranked.sort(key=lambda item: item["score"], reverse=True)

    for item in ranked:
        item.pop("rank_sharpness", None)
        item.pop("exposure_score", None)
        item.pop("rank_contrast", None)
        item.pop("rank_saturation", None)
        item.pop("rank_resolution", None)

    with open(output_dir / "analysis.json", "w", encoding="utf-8") as handle:
        json.dump(ranked, handle, ensure_ascii=False, indent=2)

    print(f"{len(ranked)} photos analyses")
    print("Top 10 global :")
    for item in ranked[:10]:
        print(f"  {item['score']:.3f}  {item['name']}")


if __name__ == "__main__":
    main()

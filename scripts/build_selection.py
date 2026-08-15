#!/usr/bin/env python3
"""Build the selected photos list for the website from the analysis."""

import json
import pathlib
import re


GROUPS = {
    "Racine": {
        "count": 5,
        "prefix": "paysage",
        "start": 1,
        "category": "villes",
        "context": "Ville — Pékin",
        "title": "Paysage urbain",
    },
    "Automne": {
        "count": 5,
        "prefix": "automne",
        "start": 1,
        "category": "automne",
        "context": "Automne — Pékin",
        "title": "Automne",
    },
    "Hiver": {
        "count": 5,
        "prefix": "hiver",
        "start": 1,
        "category": "hiver",
        "context": "Hiver — Pékin",
        "title": "Hiver",
    },
    "Animal": {
        "count": 5,
        "prefix": "animal",
        "start": 1,
        "category": "animal",
        "context": "Animal — Pékin",
        "title": "Animal",
    },
    "Interieur": {
        "count": 5,
        "prefix": "interieur",
        "start": 1,
        "category": "interieur",
        "context": "Intérieur — Pékin",
        "title": "Intérieur",
    },
    "portrait": {
        "count": 5,
        "prefix": "portrait",
        "start": 7,
        "category": "portrait",
        "context": "Portrait — Pékin",
        "title": "Portrait",
    },
    "Drone": {
        "count": 5,
        "prefix": "drone",
        "start": 7,
        "category": "drone",
        "context": "Drone — Chine",
        "title": "Vue aérienne",
    },
}


def normalize_name(name):
    cleaned = name
    for token in ["拷贝", "恢复的", "已增强-NR", "副本", "-恢复", " 2"]:
        cleaned = cleaned.replace(token, "")
    return re.sub(r"[^A-Za-z0-9]+", "", cleaned).lower()


def main():
    project = pathlib.Path(__file__).resolve().parent.parent
    data = json.loads((project / "classement" / "analysis.json").read_text(encoding="utf-8"))
    by_category = {}
    for item in data:
        by_category.setdefault(item["category"], []).append(item)

    selection = []
    for category, config in GROUPS.items():
        items = sorted(
            by_category.get(category, []),
            key=lambda item: item.get("score", 0),
            reverse=True,
        )
        seen = set()
        picked = []
        for item in items:
            key = normalize_name(item["name"])
            if key in seen:
                continue
            seen.add(key)
            picked.append(item)
            if len(picked) >= config["count"]:
                break

        for index, item in enumerate(picked):
            number = config["start"] + index
            selection.append(
                {
                    "source": item["path"],
                    "name": item["name"],
                    "target": f"{config['prefix']}-{number:02d}.webp",
                    "category": config["category"],
                    "title": f"{config['title']} {number:02d}",
                    "context": config["context"],
                    "alt": f"{config['title']} — {config['context']}",
                }
            )

    output = project / "classement" / "selection.json"
    output.write_text(
        json.dumps(selection, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for item in selection:
        print(f"{item['target']:24} {item['category']:10} {item['name']}")


if __name__ == "__main__":
    main()

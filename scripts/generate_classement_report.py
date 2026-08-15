#!/usr/bin/env python3
"""Generate the photo classification report from analysis.json."""

import json
import pathlib


CATEGORY_ORDER = [
    "Racine",
    "Automne",
    "Hiver",
    "Animal",
    "Drone",
    "Interieur",
    "portrait",
]

CATEGORY_LABELS = {
    "Racine": "Paysages et urbain (racine)",
    "Automne": "Automne",
    "Hiver": "Hiver",
    "Animal": "Animaux",
    "Drone": "Drone",
    "Interieur": "Intérieur",
    "portrait": "Portraits",
}


def metric_line(item):
    if item.get("error"):
        return f"- Erreur d'analyse : {item['error']}"
    flags = ", ".join(item.get("flags", [])) or "aucun"
    return (
        f"- Score {item['score']:.3f} | netteté {item['sharpness']:.0f} | "
        f"luminosité {item['brightness']:.0f}/255 | contraste {item['contrast']:.0f} | "
        f"saturation {item['saturation']:.0f} | {item['width']}x{item['height']} | "
        f"alertes : {flags}"
    )


def main():
    project = pathlib.Path(__file__).resolve().parent.parent
    data = json.loads((project / "classement" / "analysis.json").read_text(encoding="utf-8"))
    by_category = {}
    for item in data:
        by_category.setdefault(item["category"], []).append(item)

    lines = []
    lines.append("# Classement photos — site internet perso")
    lines.append("")
    lines.append(
        "Analyse technique automatique de 214 photos : netteté, exposition, contraste, "
        "saturation et résolution. La sélection artistique finale doit être validée à l'œil "
        "avec les planches-contact."
    )
    lines.append("")
    lines.append("## Classement global — top 20")
    lines.append("")
    lines.append("| # | Catégorie | Fichier | Score |")
    lines.append("|---|-----------|---------|-------|")
    for index, item in enumerate(sorted(data, key=lambda i: i.get("score", 0), reverse=True)[:20], 1):
        lines.append(f"| {index} | {item['category']} | `{item['name']}` | {item['score']:.3f} |")

    lines.append("")
    lines.append("## Meilleures photos par catégorie")
    lines.append("")

    for category in CATEGORY_ORDER:
        items = sorted(by_category.get(category, []), key=lambda i: i.get("score", 0), reverse=True)
        if not items:
            continue
        lines.append(f"### {CATEGORY_LABELS.get(category, category)} ({len(items)} photos)")
        lines.append("")
        for rank, item in enumerate(items[:5], 1):
            lines.append(f"**{rank}. {item['name']}**")
            lines.append("")
            lines.append(f"`{item['path']}`")
            lines.append("")
            lines.append(metric_line(item))
            lines.append("")
        if len(items) > 5:
            lines.append(f"Voir la liste complète de la catégorie en annexe.")
            lines.append("")

    lines.append("## Annexe — classement complet")
    lines.append("")
    for category in CATEGORY_ORDER:
        items = sorted(by_category.get(category, []), key=lambda i: i.get("score", 0), reverse=True)
        if not items:
            continue
        lines.append(f"### {CATEGORY_LABELS.get(category, category)}")
        lines.append("")
        lines.append("| Rang | Fichier | Score | Détails |")
        lines.append("|------|---------|-------|---------|")
        for rank, item in enumerate(items, 1):
            details = metric_line(item).replace("|", "/")
            lines.append(f"| {rank} | `{item['name']}` | {item.get('score', 0):.3f} | {details} |")
        lines.append("")

    lines.append("## Planches-contact")
    lines.append("")
    lines.append(
        "Les planches-contact sont dans `classement/contact-sheets/` pour une validation visuelle "
        "rapide, avec `manifest.json` pour retrouver chaque fichier."
    )
    lines.append("")

    output = project / "classement" / "classement-photos.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Rapport écrit : {output}")


if __name__ == "__main__":
    main()

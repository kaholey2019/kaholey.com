#!/usr/bin/env python3
"""Insert the selected photos as work cards in portfolio.html."""

import json
import pathlib
import sys

from PIL import Image


def build_card(item):
    target = item["target"]
    with Image.open(pathlib.Path(__file__).resolve().parent.parent / "assets" / "images" / target) as im:
        width, height = im.size
    title = item["title"]
    context = item["context"]
    alt = item["alt"]
    return f"""          <button class="work-card" type="button" data-category="{item['category']}" data-title="{title}" data-context="{context}" data-image="assets/images/{target}" aria-haspopup="dialog" aria-label="Ouvrir {title}">
            <img src="assets/images/{target}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async">
            <span class="work-overlay">
              <span class="work-copy">
                <strong>{title}</strong>
                <small>{context}</small>
              </span>
              <span class="work-zoom" aria-hidden="true">+</span>
            </span>
          </button>
"""


def main():
    project = pathlib.Path(__file__).resolve().parent.parent
    selection = json.loads((project / "classement" / "selection.json").read_text(encoding="utf-8"))
    cards = "\n".join(build_card(item) for item in selection)

    if "--dry-run" in sys.argv:
        (project / "classement" / "cards.html").write_text(cards, encoding="utf-8")
        print(f"{len(selection)} cartes generees dans classement/cards.html")
        return

    html_path = project / "portfolio.html"
    html = html_path.read_text(encoding="utf-8")
    marker = 'data-image="assets/images/drone-06.webp"'
    marker_index = html.index(marker)
    close_index = html.index("</button>", marker_index) + len("</button>")
    updated = html[:close_index] + "\n\n" + cards + html[close_index:]
    html_path.write_text(updated, encoding="utf-8")
    print(f"{len(selection)} cartes inserees dans portfolio.html")


if __name__ == "__main__":
    main()

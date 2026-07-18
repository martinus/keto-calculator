#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the three guide pages from one shared template.

Why this exists: the guide articles (how-much-protein-on-keto.html,
how-fast-will-i-lose-weight-on-keto.html, net-carbs-vs-total-carbs.html) share
~350 lines of boilerplate — the GA4/Consent-Mode head, the design-system CSS,
the footer and the gatrack() script. They used to be three hand-maintained
copies, so every analytics/consent/CSS/brand change was a three-file edit with
no drift detection. Now the shared skeleton lives ONCE in
dev/guides/template.html and each article contributes only its own content via
dev/guides/<slug>.parts.html. Same philosophy as build_de.py / build_embed.py:
the served files stay committed and deployed unchanged; this script only needs
to be re-run (and its output committed) after editing the template or a parts
file:

  python3 dev/build_guides.py

Template format: lines of the form {{slot_name}} mark insertion points.
Parts format: <!-- ===== slot_name ===== --> marker lines separate the
per-page values, which must appear in the same order as in the template.
The script fails loudly on any mismatch.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GUIDES = os.path.join(HERE, "guides")

PAGES = [
    "how-much-protein-on-keto",
    "how-fast-will-i-lose-weight-on-keto",
    "net-carbs-vs-total-carbs",
]

MARKER = re.compile(r"^<!-- ===== (\w+) ===== -->\n", re.M)
PLACEHOLDER = re.compile(r"^\{\{(\w+)\}\}\n", re.M)

template = open(os.path.join(GUIDES, "template.html"), encoding="utf-8").read()
slots_in_template = PLACEHOLDER.findall(template)
if not slots_in_template:
    sys.exit("template.html contains no {{slot}} placeholders")


def parse_parts(path):
    text = open(path, encoding="utf-8").read()
    markers = list(MARKER.finditer(text))
    if not markers:
        sys.exit("%s: no <!-- ===== slot ===== --> markers found" % path)
    if markers[0].start() != 0:
        sys.exit("%s: content before the first slot marker" % path)
    parts = {}
    for i, m in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        parts[m.group(1)] = text[m.end():end]
    return parts


for page in PAGES:
    parts_path = os.path.join(GUIDES, page + ".parts.html")
    parts = parse_parts(parts_path)
    if sorted(parts) != sorted(slots_in_template):
        sys.exit("%s: slots %s don't match template slots %s"
                 % (parts_path, sorted(parts), sorted(slots_in_template)))

    def fill(m):
        return parts[m.group(1)]

    out = PLACEHOLDER.sub(fill, template)
    out_path = os.path.join(ROOT, page + ".html")
    open(out_path, "w", encoding="utf-8").write(out)
    print("OK: wrote %s (%d bytes)." % (os.path.relpath(out_path, ROOT), len(out)))

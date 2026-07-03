# Keto Calculator

The keto macro calculator served at **[keto-calculator.ankerl.com](https://keto-calculator.ankerl.com)**.
Created by [Martin Ankerl](https://martin.ankerl.com).

## How it works

Flat, static, **no-build** site: the files in the repo root *are* the website.
To develop, edit the files directly and open `index.html` in a browser (or run
`python3 -m http.server`).

Two files are **generated** — regenerate instead of hand-editing:

- `embed.html` — run `python3 build_embed.py` after editing `index.html`
- `de/index.html` — run `python3 de/build_de.py` (see `de/TRANSLATION.md`)

## Deployment

Pushing to `master` triggers `.github/workflows/deploy.yml`, which strips the
dev-only files (planning docs in `md/`, design sources in `etc/`, the
generators, editor config) and publishes the rest to GitHub Pages. The Pages
source is set to **GitHub Actions** — the branch itself is never served
directly.

Development history before 2026-07-03 lives in the archived
`keto-calculator-source` repo, which used to be synced into this one by a
deploy script.

See `CLAUDE.md` for the full development guide (file map, design system,
calculator logic, ad slots).

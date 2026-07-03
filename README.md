# Keto Calculator

The keto macro calculator served at **[keto-calculator.ankerl.com](https://keto-calculator.ankerl.com)**.
Created by [Martin Ankerl](https://martin.ankerl.com).

## Project principles

A little manifest of what this tool tries to accomplish:

* Accurately calculate the macros for the ketogenic diet.
* People who walk through the calculator should learn about themselves and the
  ketogenic diet.
* Make it easy for people to start and maintain keto.
* Be fun to use, fun to play with.

Whenever you are about to change something, walk through the above points and
only do the change when it helps them.

## How it works

Flat, static, **no-build** site: the files in the repo root *are* the website.
To develop, edit the files directly and open `index.html` in a browser (or run
`python3 -m http.server`).

Two files are **generated** — regenerate instead of hand-editing:

- `embed.html` — run `python3 dev/build_embed.py` after editing `index.html`
- `de/index.html` — run `python3 dev/build_de.py` (see `dev/TRANSLATION.md`)

Everything that is not part of the website lives under `dev/` (planning docs
in `dev/docs/`, design sources in `dev/design/`, the generators).

## Deployment

Pushing to `master` triggers `.github/workflows/deploy.yml`, which strips the
dev-only files (`dev/`, the READMEs, the license) and publishes the rest to
GitHub Pages. The Pages source is set to **GitHub Actions** — the branch
itself is never served directly.

Development history before 2026-07-03 lives in the archived
`keto-calculator-source` repo, which used to be synced into this one by a
deploy script.

See `CLAUDE.md` for the full development guide (file map, design system,
calculator logic, ad slots).

# German translation (`/de/`) — how to keep it in sync

The German page `de/index.html` is **generated** from the English `../index.html`
by `de/build_de.py`. You don't hand-edit `de/index.html` — you edit the English
page as usual, then re-run the generator. The generator holds a list of
English → German string replacements and **warns you about anything it can no
longer find**, which is exactly the text you changed and need to re-translate.

## The update workflow (do this whenever you edit index.html)

```bash
python3 de/build_de.py
```

- **Prints `OK: wrote de/index.html`** → done. Commit both `index.html` and
  `de/index.html`.
- **Prints `WARNING: ... NOT FOUND`** → the English text for those snippets
  changed, so the old German mapping no longer matches. For each one:
  1. Find the new English in `index.html`.
  2. Open `de/build_de.py`, find the `rep('<old English>', '<German>')` entry
     that matches, and update its **first** argument to the new English (and the
     German translation if the meaning changed).
  3. Re-run until it prints `OK`.

That "NOT FOUND" list is the whole point — it makes drift impossible to miss.

### Adding brand-new text
If you add a new paragraph/heading to the English page, it simply won't appear
translated on the German page (it stays English) until you add a new
`rep('<new English>', '<German>')` line to `de/build_de.py`. Add it in the
matching section and re-run.

## What gets translated (section checklist)

`build_de.py` is organised in these sections — check them when reviewing:

- [ ] **1. `<head>`** — `lang="de"`, `<title>`, meta description, Open Graph,
  Twitter card, Schema.org description, canonical → `/de/`.
- [ ] **2. Header / intro** — logo tooltip, H1 "Keto-Rechner", lead paragraph,
  author byline, intro `<details>` (incl. video summary).
- [ ] **3. Fat-loss section + inputs** — headings, sex radios, **metric-first**
  weight/height rows (kg / cm primary), birthday label, activity levels,
  energy-expenditure copy.
- [ ] **4. Macronutrient section** — carbs / protein / fat headings, all body
  copy, the three `<details>` blocks, table headers (min/chosen/max, etc.).
- [ ] **5. Results card** — kcal label, macro names (Kohlenhydrate/Eiweiß/Fett),
  food-equivalent note, results disclaimer, share button, pie labels,
  projection + MFP copy, weight-loss forecast.
- [ ] **6. FAQ** — all 8 questions/answers in BOTH the visible HTML and the
  `FAQPage` JSON-LD (Google requires they match — translate them identically).
- [ ] **7. Questions / comments / sidebar / about** — Reddit helper, comments,
  book-collection heading, "Created by" bio.
- [ ] **8. JavaScript strings** — food equivalents, the 10 `deficit_levels`
  messages, all `update_warnings()` messages (incl. the funny dwarf/giant/elf
  ones), the Reddit copy-paste post, share-feedback text, chart placeholder.
- [ ] **9. Date localisation** — `TT.MM.JJJJ`, German datepicker locale, and the
  `de_date()` parser (see below).
- [ ] **10. Cusdis** — separate German comment thread (`data-page-id="/de/"`).
- [ ] **11. Asset paths** — made root-absolute (`/logo-white-150.png`, `/books/…`,
  `/fonts/…`, `/spritesheet.png`, warning images) so they resolve from `/de/`.

## Localisation decisions (not just translation)

- **Metric first.** Weight leads with **kg**, height with **cm**; lbs and
  feet/inch remain as secondary fields (the JS keeps both in sync).
- **Dates are `TT.MM.JJJJ`.** German `dd.mm.yyyy` doesn't parse with
  `new Date()`, so the generator injects a small `de_date()` helper and routes
  `calcAge()` and the forecast start-date through it. The datepicker gets a full
  German locale (`$.fn.datepicker.dates['de']`, week starts Monday).
- **Food equivalents** use German-believable units: berries in **grams**, oil in
  **EL** (Esslöffel), tuna in **Dosen**, butter/chicken in grams.
- **Decimal comma** (e.g. `80,5`) is handled natively by German-locale browsers
  in `type="number"` fields — no special code needed.
- **hreflang + canonical.** Both pages carry the same `en` / `de` / `x-default`
  alternates; each page self-canonicalises. A language switcher sits in the
  "By …" strip at the top.

## Deploy / files

- `de/index.html` is committed and served directly (flat, like the rest of the site).
- `de/build_de.py` and `de/TRANSLATION.md` are **dev-only** and excluded from
  `deploy.sh`, so they never go live.
- The German page reuses the root's images, fonts, sprite, manifest, GA4, and
  Cookiebot. The `disclaimer.html` link points to the (English) root disclaimer —
  translating that page is a future nice-to-have, not required.

## Known minor limitations

- The datepicker **library's** internal default format string and one
  **commented-out** alternate `<input>` still read `mm/dd/yyyy` — neither is
  rendered or used (the active fields are overridden to `dd.mm.yyyy`).
- The Reddit help still points at `/r/keto` (English community); fine to leave.

# Keto Calculator – Claude Code Guide

## What this repo is

This is the **single repo** — both development source and deployment — for the keto
macro calculator served at **keto-calculator.ankerl.com**. As of 2026-06-28 it is a
**flat, static, no-build** site: the files in the repo root *are* the website. Edit
them directly and open in a browser. Created by Martin Ankerl. Revenue via Google
AdSense + Amazon affiliate links. Current version: **10.0** (in the `#version_number`
element).

### How it deploys (single repo, since 2026-07-03)

Merging/pushing to **`master`** triggers `.github/workflows/deploy.yml`, which strips
the dev-only files (`md/`, `etc/`, `.vscode/`, `CLAUDE.md`, `README.*`, `TODO.txt`,
`LICENSE.txt`, the `build_embed.py`/`de/build_de.py` generators, `de/TRANSLATION.md`)
and publishes the rest to GitHub Pages (Pages source is set to "GitHub Actions", NOT
"deploy from branch" — don't flip it back, or the dev docs become live URLs). `CNAME`
and `googlea2ba6e6f24c19afa.html` (Google verification) stay in the artifact. When
adding dev-only files, add them to the workflow's strip list.

Before 2026-07-03 there were **two repos**: development happened in
`keto-calculator-source` and a `deploy.sh` rsynced the site files into this repo
(`keto-calculator`), which Pages served from the master branch. The source repo was
merged into this one (its history remains in the archived `keto-calculator-source`)
and `deploy.sh` was retired — its exclude list became the workflow's strip list.

### History worth knowing (why the repo looks the way it does)

- Originally this repo had a **build pipeline**: edit `app/`, run `tools/_compress.sh`
  (Java + Google Closure + htmlcompressor) → minified `app-compressed/` → deploy.
- Over time the live `keto-calculator` repo was **edited directly** and drifted ahead
  of `app/` (mobile responsive layout, viewport fix, externalized CSS, font tweaks),
  while `app/` froze at the "URL prefill" commit. `app/` also still referenced the
  **dead jsdelivr `/g/` combine API** (shut down years ago) for bootstrap + jQuery CSS/JS.
- On **2026-06-28** the project was **flattened**: `app/` contents were promoted to the
  repo root, the build toolchain was retired (`tools/`, `app-compressed/`, `_compress.*`,
  `sync.ffs_db`, `externs.js`, `out.css`, `.htaccess`), and the source was brought up to
  the **current live behavior** with readable files:
  - `index.html` was kept intact (all CSS/JS stays inlined, exactly as it renders live)
    with only two minimal edits: fixed the viewport to
    `width=device-width, initial-scale=1`, and removed three **dead** resources that
    were redundant anyway (jsdelivr `/g/` combine links for bootstrap CSS and
    jquery+bootstrap JS — that API is shut down — and the `cx/api.js` GA experiment).
  - Verified with a headless-Firefox screenshot that the result is pixel-identical to
    the live deployed page.

## File structure

```
index.html        – The whole page. ALL CSS is inlined in <style> blocks (normalize +
                    Bootstrap 3.3.1 + bootstrap-datepicker + sprite rules + custom layout) and
                    stays in <head>. The inlined JS (jQuery 1.11.1 + scrolldepth + Bootstrap +
                    bootstrap-datepicker + the calculator JS) was moved OUT of <head> to the end
                    of <body> (2026-06-28) so it no longer blocks first paint; it sits right
                    before the datepicker-init script, in order jQuery+plugins → Bootstrap →
                    calculator. There is NO external stylesheet link (only Google Fonts).
disclaimer.html   – Disclaimer + cookie policy (Cookiebot)
embed.html        – Embeddable widget (GENERATED — run `python3 build_embed.py` after editing
                    index.html; never hand-edit). No ads, noindex, powered-by backlink.
build_embed.py    – Generator for embed.html (not deployed)
de/index.html     – German page (GENERATED — run `python3 de/build_de.py` after editing
                    index.html; see de/TRANSLATION.md). Launched 2026-07-02.
net-carbs-vs-total-carbs.html, how-much-protein-on-keto.html,
how-fast-will-i-lose-weight-on-keto.html
                  – The three evergreen "Keto Guides" (each: article + FAQ schema + one
                    Keto Bottom ad + links back to the calculator). Hand-maintained, English
                    only. (Their 2026-06-29 creation in the then-separate live repo was the
                    final live-drifts-ahead incident that motivated the single-repo merge.)
service-worker.js – PWA service worker
manifest.json     – PWA manifest
robots.txt
CNAME             – keto-calculator.ankerl.com
googlea2ba6e6f24c19afa.html – Google site verification
favicon.png, logo-white-150.png, launcher-icon-*.png, spritesheet.png, share_1600_lanc2.jpg,
  *_warning_*.jpg, proteintoohigh_small.jpg – images
books/            – Amazon affiliate book covers
fonts/            – local fonts
md/               – planning + analytics docs (see below) — not deployed
etc/              – design source archive (logo .xcf/.svg, launcher icons, full-size book covers) — not deployed
.github/workflows/deploy.yml – the Pages deploy (strips dev files, publishes the rest)
LICENSE.txt, README.md, README.txt, TODO.txt – not deployed
```

> Repo cleanup (2026-06-28): removed unused/orphaned files — `me.png`,
> `paypal-logo-small.png` (donation modal gone), the `ads/` dir (Perfect Keto banner
> removed), the `share/` social-icon dir (referenced nowhere), and the 120MB `facebook/`
> social-promo archive. `etc/` contains design sources only (there are **no** OneSignal
> leftovers — the OneSignal service workers were already removed from the repo root).

> Repo cleanup (2026-06-29): removed more orphans from **both** repos — `conversion.js`
> (no longer loaded by any page), the five unused standalone CSS copies (see CSS note below),
> `me.jpg` and `share_high_1200.jpg` (the latter was the now-removed Pinterest pin image), and
> the dead commented-out book block in `index.html` (+ its `books/0307474259_small.png`). Then
> the unused **`thank-you.html`** (an old donation thank-you page, linked from nowhere) and its
> whole asset chain — `style.css` (loaded only by it), `plus.png`/`minus.png` (referenced only
> by `style.css`), and `youre-awesome.jpg`. The **live repo** additionally shed stale leftovers
> rsync had never deleted: the `ads/` dir, `me.png`, `paypal-logo-small.png`, `logo_192.png`,
> and five delinked book covers. `etc/` (design-source archive) was intentionally **kept**.

**CSS:** every page now inlines all its CSS — there is **no external stylesheet** anywhere
(only the Google Fonts link). The standalone source-of-record copies (`bootstrap.min.css`,
`datepicker.css`, `spritegen.css`, `normalize.css`, `ketocalculator.css`) were deleted
2026-06-29 as unused; `style.css` (plus its `plus.png`/`minus.png` assets) went with
`thank-you.html` on 2026-06-29. All recoverable from git history if you ever externalize.

> Note on responsiveness: the page **is** responsive. The inlined custom-layout
> `<style>` block carries an `@media only screen and (max-width:830px)` block that
> collapses `#sidebar`, makes `#main` full-width, and scales the header/logo. (Verified
> on a 390px iPhone width.) As of 2026-06-28 the inline mobile block was refined:
> text/number inputs set to 16px (stops iOS Safari zoom-on-focus), radios sized as 22px
> tap targets, and form rows given more spacing. If you ever externalize the CSS, mind the
> order: normalize → Bootstrap → datepicker → sprite → **custom layout last**.

## Current tech stack

| Thing | Current |
|-------|---------|
| Layout | Inlined CSS: `#content` is a **flex row** at ≥830px (so `#sidebar` stretches to `#main`'s height for the sticky ad); `#main`/`#sidebar` still carry legacy float rules (ignored under flex). An `@media (max-width:830px)` mobile block collapses `#sidebar` and makes `#main` full-width. Responsive. |
| JS libs | jQuery 1.11.1, Bootstrap 3.3.1 JS, bootstrap-datepicker — all **inlined** in `index.html`, at the **end of `<body>`** (moved out of `<head>` 2026-06-28 to unblock first paint) |
| Charts | Google Charts (Visualization API) via the modern `gstatic.com/charts/loader.js` + `google.charts.load('current', …)` (migrated off the deprecated `google.com/jsapi`) |
| Analytics | **GA4 `gtag.js`, property `G-4EDP644SXM`** (added 2026-06-28, top of `<head>`, `async`). Replaced the prior dead stack — a Universal Analytics tag (`UA-36863101-1`, stopped collecting 2023-07-01), a dead Google Optimize anti-flicker snippet, and the jQuery ScrollDepth plugin (removed 2026-06-28 — it only pushed UA/GTM-format `dataLayer` objects that GA4 `gtag.js` never forwards; GA4 tracks scroll natively). **Google Consent Mode v2** is wired: defaults are denied (`gtag('consent','default',…)` before config), and a Cookiebot bridge (`CookiebotOnConsentReady` → `gtag('consent','update',…)`, statistics→`analytics_storage`, marketing→`ad_*`) grants on consent — so EU/Safari non-consenting traffic is modelled, not lost. Search Console is powered by the `google-site-verification` meta, independent of analytics. |
| Push | **Removed** (was OneSignal) — SDK script, init/notifyButton, both service workers, and `manifest.json`'s `gcm_sender_id` all deleted |
| Cookie consent | Cookiebot (`6ba27c9d-…`) |
| Comments | **Cusdis** (lightweight, ad-free, no login to comment) — replaced Disqus 2026-06-29. Lazy-loaded on scroll near page bottom (`load_cusdis()`); embed `<div id="cusdis_thread">` with `data-app-id="YOUR_CUSDIS_APP_ID"` **(placeholder — paste the real App ID from a free cusdis.com site or comments stay empty)**. German page uses `data-page-id="/de/"` for a separate thread. |
| Ads | AdSense `ca-pub-2398468033418589` |

## Design system (established 2026-06-28 — keep consistent)

A "precise metabolic instrument" direction: technical type + a trustworthy editorial body,
the brand cyan evolved (not discarded), amber reserved strictly for "you must enter this".
**All of it is inlined in `index.html`'s `<style>` block; there is no design token file or
build — match these values by hand. Update the mobile `@media (max-width:830px)` block too.**

### Fonts (Google Fonts link in `<head>`)
`Space+Grotesk:wght@500;600;700` + `PT+Serif:wght@400;700`, `&display=swap`, with `preconnect`.
- **Space Grotesk** — all headings (h1–h3), every numeric `<input>`, the result figures, and
  primary buttons. It's the "instrument readout" face; use it for anything that is a number/label.
- **PT Serif** — body copy only (editorial, health-authority tone). Prose → serif, data → grotesk.

### Type scale (desktop / mobile)
- h1 (header wordmark): Space Grotesk 600, 80px / 40px, letter-spacing −2px, white
- h2: Space Grotesk 600, 32px / 26px, ls −0.6px, `#14202b`, **+ the signature cyan rule** (below)
- h3: Space Grotesk 500, 23px / 21px, ls −0.3px, `#1b2730`
- body: PT Serif 18px, line-height 1.66 / 1.62, `#14202b`, antialiased
- lead (opening paragraph, `p.lead`): PT Serif 20px, line-height 1.6, softer ink `#2a3a47`

### Reading measure (prose layout)
Body prose is **capped to a comfortable line length**, not the full content column: `#main p,
#main ul, #main ol, #main dl { max-width:650px; }` (~66 characters — the eye tracks line-to-line
easily). `#main p` also gets explicit rhythm: `margin:0 0 1.15em; line-height:1.72`. The
calculator table, `.results-card`, charts (`#chart`) and the book grid are **not** prose and keep
their own widths (they're tables/cards/images, not `<p>`/`<ul>`). On mobile the cap is a no-op (the
column is already < 650px). When adding prose, let it inherit this — don't widen text past 650px.

### Palette
- Ink / text + headings `#14202b`; secondary heading `#1b2730`; muted `#5a6b78`, `#6b7a86`
- Brand cyan `#33B5E5` (light) → `#1294c8` (deep). Header = `linear-gradient(135deg,#33B5E5,#1294c8)`
- Links `#0e6e96`, visited same, hover `#0a5675` (the old blue/purple-visited/red-hover is gone)
- Surfaces: white; cool panel `linear-gradient(180deg,#f7fbfe,#edf5fb)`; hairlines `#d9e6ef`/`#dce8f0`/`#e4eef5`
- **Amber = functional only** (required-field cue): border `#ff8f00`, bg `#fff6e3`, glow `rgba(255,143,0,*)`
- Inputs: border `#cdd4da`, radius 7px; focus ring brand cyan `rgba(51,181,229,0.2)`
- **Macro colors — must match the pie charts:** Carbs `#E60144`, Protein `#709500`, Fat `#264A73`

### Signature
Short ketone-cyan rule under every `<h2>` (`h2::after`, 52×4px, cyan gradient). Each section reads
as a "readout". Don't add competing decorative accents elsewhere — boldness is spent here + the card.

### Component patterns (class → what it is)
- `.results-card` — the hero payoff readout. Panel (cool gradient, border `#d9e6ef`, radius 14px,
  soft shadow); big kcal figure `.results-kcal-num` (Space Grotesk 700, 46px); `.macro-row`s each
  with a `.macro-dot` in the macro color, `.macro-val` (Space Grotesk 600, `<i>g</i>` muted unit),
  `.macro-name`, `.macro-meta`. Data spans (`.target_kcal`, `.carbs`, `.carbs_proc`…) are reused —
  `update_by_name()` updates ALL elements by class, so duplicating spans is safe.
- Food sub-line (`.macro-food`, dual-classed `.carbs_food`/`.protein_food`/`.fat_food`) — lives
  *inside* each `.macro-row` (in a `.macro-body` wrapper below the `.macro-line`), so the macros and
  their everyday-food equivalents read as **one** card, not two. PT-Serif, muted, with key numbers
  grotesk via `<b>` and a leading emoji in `.fe`. JS `update_food_equivalents()` fills them; each line
  is hidden by `.macro-food:empty` until valid, and the `.macro-food-note` caveat (`#macro_food_note`)
  is JS-toggled with validity. Equivalents lead with **believable** portions (a single-food count like
  "17 eggs" is correct but reads as absurd — and avoid gluttonous-sounding whole-unit counts like
  "8 avocados"): carbs→cups of berries / a banana, protein→a cooked chicken-breast weight / cans of
  tuna, fat→a block of butter (by weight) / tbsp of olive oil. All deliberately rough, framed as
  *daily* totals spread across meals. The card itself spans the full content column (no narrow cap).
- `.book` — image card: radius 8px, soft shadow, hover lift (`translateY(-3px)`).
- `.needs-input` — required-field cue toggled by `mark_empty_fields()`: 2px amber border, amber bg,
  pulsing glow (`@keyframes needsInputPulse`), radios get a circular ring; respects
  `prefers-reduced-motion`. The cue is amber **because** the rest of the UI is cyan — keep that split.
- `.userinputs` — the data-entry table: row padding, hairline separators, vertically centered.
- Primary button (e.g. "Share my macros"): cyan gradient, radius 9px, soft shadow, Space Grotesk 600.

### Rules when extending
1. Numbers/labels → Space Grotesk; prose → PT Serif. 2. Macros always carbs=red / protein=green /
fat=blue (dots, charts, anything). 3. Amber is **only** for required-input cues — never decoration.
4. Keep mobile parity (edit the 830px block alongside). 5. One signature, lots of restraint.

## Calculator logic (inline `<script>` in index.html)

- `calc_handler(event)` – debounced entry point (fires on input change)
- `update_calculations(event)` – BMR (**Mifflin-St.Jeor**), TDEE, body fat, protein range, fat targets
- `calc_expected_loss_kg(days, …)` – weight-loss projection
- `draw_pies(data)` / `draw_chart(data)` – Google Charts pie + annotation charts
- `update_food_equivalents(carbs_g, protein_g, fat_g)` – fills the "What that looks like in food"
  card (`#food_equiv`) with everyday-food equivalents; hidden until all three macros are valid
- `update_csv(data)` – CSV download link
- `update_warnings()` – input validation + the fun warnings
- `load_cookie()` / `set_cookie()` – persist inputs in cookies
- `load_url_params()` – prefill from URL query params, e.g.
  `?carbs=25&target_deficit_form=20` (used for sharing; **must keep working**)

Form elements use `name=` attributes (not `id=`) for the cookie/URL system;
`document.data` is the `<form name=data>`. Protein range is based on lean body mass.

## Ad slots (AdSense `ca-pub-2398468033418589`)

The account has **three real display ad units**: `7271241487` (Keto Top), `8747974681`
(Keto Sidebar, renamed from "Keto Mid"), `1224707884` (Keto Bottom). Amazon affiliate tag: `martanke-20`. (A `2426641084` "Keto Links" slot
once existed in the code but the unit was deleted from the account — that ID is dead; don't use it.)

**As of 2026-06-29 TWO manual ads are live:** `1224707884` ("Keto Bottom", right after the
results table) and `8747974681` ("Keto Sidebar", repurposed as the **sticky desktop sidebar skyscraper**,
`.sidebar-ad`, 160x600). The sidebar ad replaced the Amazon book grid on 2026-06-29 (the books earned
~$3/mo while taking the sidebar's prime, desktop-only space — `#sidebar` is `display:none` under
830px). For the sticky to travel the long page, `#content` is a **flex row** at ≥830px (so `#sidebar`
stretches to `#main`'s height) and `.sidebar-ad` is `position:sticky;top:20px` with a reserved 160x600
box (no CLS). This unit was previously the removed in-form "Keto Mid"; reused here (and renamed to
"Keto Sidebar" in the dashboard) so the sidebar maps to a **real** unit with proper reporting.
Book affiliate links now live **only** in the single inline rec (4 covers, `.recommended` under "Learn
Your Optimal Macronutrient Ratio") for E-E-A-T/trust, not revenue. `7271241487` ("Keto Top") is the
only unit not currently placed. **AdSense Auto Ads were disabled** (removed `enable_page_level_ads`)
— keep them OFF (see `md/plan.md` §8). Note: Auto ads can still be re-enabled from the **AdSense
dashboard** (Ads → By site) independent of code. (The old "forum" ads came from **Disqus's free
tier**; Disqus was replaced by ad-free Cusdis on 2026-06-29, so that ad source is gone.)

## Working on this codebase

- **No build step.** Edit files directly; test by opening `index.html` or
  `python3 -m http.server` in the repo root.
- Keep the calculator correct, cookie persistence working, and `load_url_params()` intact.
- Mobile matters most: ~65% of traffic is mobile (see `md/analytics-summary.md`).
- Keep ads away from the inputs / Calculate flow (avoids invalid-click penalties).
- Preserve the Amazon tag `martanke-20` in book/caliper links.

## Planning docs (in `md/`)

- `md/revenue-plan-2026-07.md` – **the current live plan** (revenue growth, 2026-07-02) —
  supersedes `plan.md`'s minimal scope
- `md/plan.md` – the redesign roadmap (durable SEO / speed / UX / ad-placement wins)
- `md/analytics-summary.md` – 12-month GA4 traffic/device/engagement findings
- `md/peer.md` – the advisory "council" verdict that seeded the plan
- `md/*.png` – GA4 screenshots

> Note: `md/plan.md`'s "Already done" items (mobile layout, viewport fix) are present in
> this source. Beyond those, the 2026-06-28 session also: refined the inline mobile block
> (16px inputs, radio tap targets), removed the dead Optimize + Universal Analytics
> snippets (so analytics is currently OFF — re-instrument before the 3-month review),
> modernized the Google Charts loader, and added font `preconnect` + `display=swap`. A
> caveat surfaced while doing this: the page's analytics was already dead, so the plan's
> "✅ Analytics confirmed live" line was wrong — treat analytics as a TODO, not done.

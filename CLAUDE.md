# Keto Calculator – Claude Code Guide

## Project overview

Static single-page keto macro calculator at **keto-calculator.ankerl.com** (GitHub Pages).  
Created by Martin Ankerl. Revenue via Google AdSense + Amazon affiliate links.  
Current version: **9.13** (stored in `#version_number` div).

## Goals for this redesign branch

1. **Modernize** – clean up ancient dependencies, responsive layout, modern CSS
2. **SEO** – better rankings, structured data, Core Web Vitals
3. **Better ads** – improve AdSense placement and revenue
4. **More useful** – improve UX, clarity, and content
5. **Lean** – reduce page weight, remove dead code

## File structure

```
index.html        – Everything: HTML + all JS inlined + ads (375 KB, minified)
style.css         – normalize.css v2.1.3 (2013) + custom float-based layout
disclaimer.html   – Disclaimer + cookie policy page
thank-you.html    – Donation thank-you page
service-worker.js – PWA service worker (likely outdated)
favicon.png       – Site favicon
logo-white-150.png – Logo for header
spritesheet.png   – Social icon sprites (FB, Twitter, Pinterest, PayPal, etc.)
books/            – Amazon affiliate book cover images (8 books)
ads/              – Ad banner image (Perfect Keto affiliate)
CNAME             – keto-calculator.ankerl.com
```

No build system. Everything is plain HTML/CSS/JS deployed directly to GitHub Pages.

## Current tech stack (much of it outdated)

| Thing | Current | Problem |
|-------|---------|---------|
| Layout | Fixed-width floats, 870px max | Not truly responsive |
| CSS reset | normalize.css v2.1.3 (2013) | Ancient, inline |
| JavaScript | jQuery 1.11.1 (2014) inlined | Huge, outdated |
| Charts | Google Charts (Visualization API) | Still fine |
| Analytics | Google Analytics UA-36863101-1 | **DEAD** – UA sunset July 2023 |
| Push notifications | OneSignal | Loads synchronously |
| Cookie consent | Cookiebot (6ba27c9d-…) | Still active |
| Comments | Disqus | Slow, ad-heavy |
| Ads | AdSense ca-pub-2398468033418589 | Still active |

## Page structure / sections

1. **Header** – H1 with logo + "Keto Calculator", blue background (#33B5E5)
2. **Calculator form** (`<form name=data>`) – all inputs live here
   - Sex, weight (kg/lbs), height (cm/ft+in), date of birth
   - Activity level (sedentary → very active + custom kcal)
   - Body fat %
   - Carbs g (default 25)
   - Protein (min/chosen/max, auto-calculated from lean mass)
   - Fat target (deficit %, kcal, or fat g – any one drives the others)
3. **Results summary** – macro table + 3 pie charts (maintenance / target / deficit)
4. **Weight loss forecast** – Google AnnotationChart for 1-year projection + CSV export
5. **Reddit copy-paste** – pre-filled template to post to r/keto
6. **Perfect Keto affiliate** – banner ad
7. **Disqus comments**
8. **Sidebar** – share buttons + 8 Amazon affiliate book recs
9. **Footer** – creator info, disclaimer link, donate link
10. **Donate modal** – PayPal, Bootstrap modal

## Calculator logic (index.html inline JS)

Key functions – all in the monolithic inline `<script>` at the top of `<body>`:

- `calc_handler(event)` – debounced entry point, fires on any input change (500ms delay)
- `update_calculations(event)` – main calculation: BMR (Mifflin-St.Jeor), TDEE, body fat, protein range, fat targets
- `calc_expected_loss_kg(days, …)` – projects weight loss over time
- `draw_pies(data)` – Google Charts pie charts
- `draw_chart(data)` – Google Charts annotation chart (weight forecast)
- `update_csv(data)` – generates CSV download link
- `update_warnings()` – validates inputs, shows fun warnings (dwarf/giant/etc.)
- `load_cookie()` / `set_cookie()` – persists user inputs in cookies
- `load_url_params()` – allows pre-filling via URL query params (e.g. `?kg=80&height=175`)

Formula used: **Mifflin-St.Jeor** for BMR (validated in two NCBI studies).  
Protein range: based on lean body mass (0.6–1.0 g/lbs of LBM).

## Ad slots (AdSense ca-pub-2398468033418589)

| Slot ID | Placement |
|---------|-----------|
| 7271241487 | After personal data inputs |
| 8747974681 | After body fat section |
| 1224707884 | After personal results summary |
| Page-level ads | Enabled via `enable_page_level_ads: true` |

## Amazon affiliate tag

`martanke-20` – used in all book links and the caliper link.

## SEO / meta (current)

- Title: `Keto Calculator - Learn Your Macros on the Ketogenic Diet`
- Description: `How to lose weight on keto? This site calculates your perfect macros for the ketogenic diet.`
- Schema.org: `Organization` type (should be `WebApplication` or `FAQPage`)
- OG tags: present and correct
- Canonical: not set explicitly

## Known issues to fix

- **GA4 migration** – UA-36863101-1 stopped collecting data in July 2023, need GA4
- **Google+ share button** – dead, remove it
- **`user-scalable=no`** in viewport – hurts accessibility and Core Web Vitals
- **jQuery 1.11.1** – 96KB overhead, can be replaced with vanilla JS
- **Fixed layout** – sidebar disappears on mobile, layout breaks below ~900px
- **OneSignal loads synchronously** – blocks render
- **`font-size: 104px` H1** – looks dated
- **No `<link rel="canonical">`** – SEO gap
- **Schema.org type wrong** – Organization instead of WebApplication/SoftwareApplication

## Coding conventions in this project

- **No build system** – changes must work as raw HTML/CSS/JS files opened directly
- **Deployment** = `git push` to master branch → auto-deploys via GitHub Pages
- **Test** by opening index.html in browser (or `python3 -m http.server`)
- The calculator runs entirely client-side; no backend
- Form elements use `name=` attributes (not `id=`) for the cookie/URL param system
- `document.data` refers to the form (it has `name=data`)
- CSS class `hidden-cls` / `visible-cls` toggle expandable sections
- Sprite sheet (`spritesheet.png`) used for social icons via `.sprite` CSS classes

## Working on this codebase

When making changes:
1. Keep the calculator logic working – test all inputs produce correct outputs
2. Preserve cookie persistence (user inputs survive page refresh)
3. Preserve URL param loading (`?kg=80` etc.) – used for sharing
4. AdSense slots must stay in their approximate positions (above/in-form placement)
5. Amazon affiliate tag `martanke-20` must be preserved in all book links
6. Test on mobile – the site has significant mobile traffic

When extracting JS from index.html:
- The minified JS is a mix of: calculator logic + jQuery 1.11.1 + Google Charts loader
- The calculator logic starts with `var google_is_loaded_bool` and ends before the jQuery bundle
- jQuery bundle is identifiable by `"jquery":"1.11.1"` string inside it

# Redesign Plan (keto-calculator)

One-time overhaul. No ongoing updates. Static site stays static.

> **⚑ Superseded for revenue work (2026-07-02):** the owner opted out of the minimal
> "no-touch year" scope and asked for revenue growth. The live to-do list is now
> **[`md/revenue-plan-2026-07.md`](revenue-plan-2026-07.md)** (it folds in this file's open
> verification items). This file remains the record of the 2026-06 overhaul + the avoid-list
> rationale.

## Guiding principle

**Prefer durable, compounding improvements over quick wins that hurt long term.**
The owner optimizes for long-term ad revenue health, not a short RPM spike. Anything
that raises this month's earnings while degrading UX, page speed, trust, or Google
ranking is a net loss and must be avoided — even if AdSense allows it.

Revenue = traffic × engagement × RPM. The durable way to grow all three is a fast,
trustworthy, well-ranked page that loyal users keep returning to — not ad stuffing.

---

## ⚑ Where this stands now (council verdict, 2026-06-29)

**The on-page work is essentially done. The bottleneck is search position, not page
quality.** Two phases of work (2026-06-28 + 2026-06-29) took the page from "dead trackers
+ render-blocking everything" to technically excellent: fast, accessible, schema-rich,
trustworthy, with a share moat and a clean results card.

But the live Search Console numbers (single day) show the real ceiling:

| Query | Impr | Clicks | Read |
|---|---|---|---|
| keto calculator | 32 | 1 | ranks ~page 2–3 — surfaces but doesn't earn the click |
| keto macro calculator | 12 | 0 | same: relevant, ranked too low |
| keto calculator ankerl | 6 | 4 | branded / loyal-Direct traffic |
| how much protein on keto (×2) | 7 | 2 | informational long-tail, present |
| carbs for ketosis / to be in ketosis / carb range | 7 | 2 | informational long-tail, present |

**Interpretation:** the page already surfaces for the money keywords — it just ranks too
low to convert impressions into clicks. More meta/schema/title polish will *not* move this
(it's already optimized). Rankings are now gated by **domain authority (backlinks)** and by
the macro reality that keto demand peaked ~2019 and AI Overviews intercept informational
queries. The reliable base is the 74% Direct + 11% Social loyal traffic — protect it.

**Status update 2026-06-29 (monetization + comments session):** the moves the earlier verdict
listed are now done or deliberately deferred — everything is **deployed** (live through
`d588eac`), hidden content is **indexable**, the loyal traffic is **monetized** (a second ad
unit added, see §8), and comments moved to **ad-free Cusdis**. The **owner reviewed this plan on
2026-06-29, is happy with the site, and chose a minimal "no-touch year" scope.**

**Therefore the only live moves left are no-build essentials (verify + decide):**
1. **Verify both ad units actually render/fill on the live site** — esp. the Keto Bottom unit on
   mobile (65% of traffic). See §8/§9.
2. **Confirm Auto Ads OFF** in the AdSense dashboard (owner-only). See §8.
3. **Set a hard 3-month review (≈ 2026-09-29)** — decide double-down / harvest / sell from data.
   See §9.

**Deferred (not abandoned):** the **embeddable widget** (§7) is still the single static
authority/backlink play, but it is real new work with uncertain payoff — out of scope for the
minimal round, revisit at the 3-month review. Everything else on-page is finished.

---

## ▶ Next actions (ranked — this is the live to-do list)

Owner chose a **minimal "no-touch year" scope (2026-06-29)**. The build is done; what remains is
verification + one calendar decision.

1. **[~] Verify both ad units on the LIVE site** — *~30 min, owner.* Ads render only on the real
   HTTPS domain (not local previews; and Firefox ETP / ad blockers block AdSense entirely, so test
   in a non-blocking browser). **[x] Mobile**: Keto Bottom (`1224707884`) confirmed rendering after
   the results (2026-06-29). **[ ] Desktop**: confirm the sidebar skyscraper (`8747974681`, Keto Sidebar)
   fills and sticks. Confirm the inline 4-book rec shows on both. See §8.
2. **[ ] Confirm Auto Ads OFF** — *owner-only dashboard.* AdSense → Ads → By site, for the domain.
   See §8.
3. **[ ] Set a hard 3-month review (≈ 2026-09-29)** — *decision, not code.* Compare RPM /
   engagement / CWV against the baseline (≈ €60/mo, ~4,850 sessions/mo, 17% engagement) and decide
   double-down / harvest / sell **from data, not vibes**. See §9.
4. **[x] Rename the sidebar unit** — done 2026-06-29. The sidebar uses real unit `8747974681`,
   renamed **"Keto Mid" → "Keto Sidebar"** in AdSense, so reports read clearly. (The old `2426641084`
   "Keto Links" slot was dead — that unit had been deleted from the account.)

- **[x] Deploy** — live through `d588eac` (2026-06-29).
- **[x] Hidden detail sections indexable (2026-06-29)** — native `<details>`/`<summary>`. See §3.
- **[deferred] Embeddable widget (`embed.html`)** — the only remaining growth/backlink lever, but
  real new work with uncertain payoff; out of scope for the minimal round. Revisit at the review. See §7.

Optional / lower priority: jQuery removal, file split/minify — see "Don't bother" for why
these are not worth it now.

---

## ✅ Already done

### Session 2026-06-28
- [x] **Analytics re-instrumented** — GA4 `gtag.js`, property `G-4EDP644SXM`. Replaced a dead
  Universal Analytics tag (`UA-36863101-1`, stopped 2023-07-01) — analytics had been OFF.
- [x] **Consent Mode v2 wired** — defaults denied; Cookiebot bridge (`CookiebotOnConsentReady`)
  grants `analytics_storage`/`ad_*` on consent, so EU/Safari non-consenting traffic is modelled.
- [x] **Mobile layout** — responsive `@media (max-width:830px)` block: sidebar collapses, `#main`
  full-width, header/logo scaled, fixed mobile share bar. (The `style.css` `@media (max-width:900px)`
  block is a separate, *unused* copy.)
- [x] **Viewport fixed** — `width=device-width, initial-scale=1` (no `user-scalable=no`).
- [x] **Mobile inputs refined** — 16px text/number inputs (stop iOS zoom-on-focus), 22px radio
  tap targets, more form-row spacing.

### Session 2026-06-29 (this session)
- [x] **Food-equivalents card + merge** — each macro row in the results card carries an
  everyday-food sub-line (carbs→cups of berries / a banana, protein→a cooked chicken-breast
  weight / cans of tuna, fat→a block of butter / tbsp olive oil), merged into a single
  full-width results card. `update_food_equivalents()` fills it; `.macro-food:empty` hides each
  line until valid. Anchors use *believable* portions (fixed the absurd "17 eggs"/"8 avocados").
- [x] **Copy / SEO / nutrition pass** — verified the JS math correct (Mifflin-St. Jeor:
  BMR 1750 → TDEE 2425 → 1940 kcal → 160g fat for the test input). Removed an unsubstantiated
  disease-prevention claim from the intro (keto "lowering risk for heart disease, diabetes,
  cancer, stroke" — a YMYL/E-E-A-T liability); rewrote the garbled net-carbs paragraph; softened
  the gluconeogenesis claim to be scientifically careful; corrected the FAQ protein range
  ("1.2–2.0" → "1.3–2.2" g/kg lean, matching the code) in both visible text and JSON-LD;
  reframed the carbs intro around the 20–50g ketosis range (matches GSC query intent); rewrote
  the flat lead into a clearer value promise.
- [x] **JS cleanups (zero behavior change)** — fixed the wrong activity-factor comment
  (documented the deliberately-conservative 1.1→1.617 factors); added `var` to a leaking global;
  tidied `deficit_levels` (wrong inline comments, non-monotonic advice wording); modernized cookie
  encoding (`escape`/`unescape` → `encodeURIComponent`/`decodeURIComponent`, back-compatible).
- [x] **Disclaimer page rebuilt** on the design system — was missing a viewport meta (broken for
  65% mobile), had a dead `google.com/jsapi` + `conversion.js` + wrong `<title>`. Now responsive,
  branded, keeps the legal text + Cookiebot, `lang=en`, canonical.
- [x] **`sitemap.xml` created** (homepage + disclaimer) and referenced from `robots.txt`.
- [x] **Hidden detail sections made indexable** — the four `display:none`/`toggle_visibility()`
  blocks converted to native `<details>`/`<summary>` with descriptive summaries (see §3).
- [x] **Version bumped to 10.0** (`#version_number`) to mark the two-session overhaul.

### Session 2026-06-29 (monetization + comments — later same day)
- [x] **Comments: Disqus → Cusdis** — lightweight, ad-free, cookieless, no login to comment;
  lazy-loaded near page bottom. Replaced Disqus's free-tier ad/tracking payload. Fixed the
  clipped Cusdis form with a `min-height` floor on the iframe.
- [x] **Book links modernized** — dropped dead/used-only titles (Lyle McDonald's 1998
  self-published book; Wheat Belly) and refreshed to current in-print covers (The Case for Keto,
  The Obesity Code, The Art & Science of Low-Carb Living, Good Calories Bad Calories). Consolidated
  to **one inline 4-book rec** under "Learn Your Optimal Macronutrient Ratio", now visible on
  **desktop AND mobile** (removed the `.recommended { display:none }` desktop hide). Kept purely
  for E-E-A-T/trust, not revenue.
- [x] **Desktop sidebar books → sticky AdSense skyscraper** — the 8-book sidebar grid earned ~$3/mo
  while taking the sidebar's prime, desktop-only space; replaced with a 160×600 sticky display unit
  (`.sidebar-ad`, slot `8747974681` = the real "Keto Sidebar" unit (ex-"Keto Mid"), repurposed from its old in-form
  spot — note an earlier draft used the dead `2426641084` "Keto Links" id, fixed 2026-06-29). `#content` is
  now a **flex row** at ≥830px so `#sidebar` stretches to `#main`'s height and the ad travels the
  long page; the 160×600 box is reserved up front (no CLS). Sidebar stays `display:none` < 830px.
- [x] **Removed FB / X / Pinterest share icons** — desktop-only (missed the 65% mobile audience),
  ~0 conversion on a utility tool, dated (Twitter→X). Removed the icons + orphaned
  `.shareicon`/`sprite-fb`/`sprite-tw`/`sprite-pi`/`sprite-wa` CSS. Social inbound (11% of sessions)
  is already carried by `og:image`/`twitter:card` rich previews + the "Share my macros" button.

### Session 2026-06-29 (SEO audit + performance pass)
Full audit in `md/seo-audit-2026-06-29.md`; prioritized fixes in `md/seo-action-plan.md`.
**Verdict: already ~78/100 "Good" — on-page/technical hygiene was strong; the ceiling is domain
authority + niche demand, not tags (confirms the council verdict above).** Shipped the worthwhile,
one-time, evergreen wins:
- [x] **Core Web Vitals confirmed all-green (field/CrUX):** LCP 2.1s · INP 143ms · CLS 0.09. The
  earlier "analytics/CWV is a TODO" caveat is resolved — real-user CWV passes.
- [x] **Non-render-blocking Google Fonts** — `preload` + `media="print" onload` swap + `<noscript>`
  (kept `display=swap`). Removed the one render-blocking resource (~780ms).
- [x] **Lazy-load Google Charts** — `ensure_charts_loaded()` injects the loader on the *first
  calculation* (from `wait_until_deadline`, the single draw chokepoint, so all entry paths incl.
  `?carbs=…` share URLs are covered). ~249 KiB no longer downloads for visitors who don't complete
  the form. **Lab TBT 490→0ms, Speed Index 3.9→2.1s, FCP 3.3→2.1s, CLS 0.09→0.02.**
- [x] **Preconnects added** — `consent.cookiebot.com` (~300ms LCP candidate) + `www.gstatic.com`
  (Charts chain). 4 preconnects total (the recommended max).
- [x] **`Person` author schema** — added `author` (name + `sameAs`: blog, reddit, GitHub) to the
  `WebApplication` JSON-LD for E-E-A-T on this YMYL page.
- [x] **`/llms.txt` created** — site summary + key facts + page links, for AI-search/GEO visibility.
- [x] **robots.txt: explicit AI-crawler allows** — GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot,
  PerplexityBot, Google-Extended → `Allow: /` (pairs with llms.txt).
- [x] **OG polish** — trimmed `og:description` (230→130 chars); added `og:site_name`, `og:locale`,
  `og:image:width`/`height` (the share image is actually 1200×630).
- [x] **Outbound links → HTTPS** — converted all 31 outbound `http://` links to `https://`
  (verified each domain serves HTTPS); left `paindatabase.com` on HTTP (HTTP-only, no valid cert).
  Amazon `martanke-20` affiliate tag preserved.
- **Left alone on purpose:** the rest of the ~465 KiB "unused JS" (AdSense=revenue, Cookiebot=legal,
  gtag=analytics — mandatory third-party), the lab LCP 6.9s (late-painting AdSense unit; field LCP
  is green), FAQ rich results (restricted to gov/health sites), security headers (not a ranking
  factor; GitHub Pages can't set them). **Performance + on-page SEO: done.**

---

## The durable foundation

### 1. Core Web Vitals / page speed — **highest long-term leverage** (mostly done)
Speed lifts BOTH Google ranking AND ad viewability (viewability sets RPM), so it helps traffic
and monetization at once.
- [x] Remove OneSignal entirely (SDK + notifyButton popup) — earned €0, slowed load, scared new users.
- [x] **Remove the dead Google Optimize anti-flicker snippet — biggest single speed win.** Optimize
  was sunset 2023-09-30, so its reveal callback never fired and `<html>` sat at `opacity:0` (blank)
  for up to 4s on every visit. Almost certainly a major cause of the 17% engagement rate.
- [x] Remove the dead `UA-36863101-1` analytics.js snippet.
- [x] Modernize the Google Charts loader: deprecated `google.com/jsapi` → `gstatic.com/charts/loader.js`.
- [x] `preconnect` for Google Fonts + `font-display: swap`.
- [x] **Preload the LCP image** — `rel="preload" as="image"` + `fetchpriority="high"` on the header logo.
- [x] **Removed the dead jQuery ScrollDepth plugin** — emitted only UA/GTM-format `dataLayer` pushes
  that GA4 (no GTM container) ignores; GA4 tracks scroll natively.
- [x] **Re-add analytics (GA4 `gtag.js`, `G-4EDP644SXM`)**.
- [x] **Lazy-load below-the-fold images** — `loading="lazy"` on the 14 book covers + statcounter pixel;
  logo stays eager (LCP). Covers carry width/height, so no CLS.
- [x] **Render-blocking head JS moved to end of `<body>` — biggest CWV lever.** ~1380 lines (calculator
  + jQuery 1.11.1 + scrolldepth + datepicker + Bootstrap) were render-blocking. Relocated before the
  datepicker-init (the only parse-time `$` use), order preserved. Head shrank ~3686→1568 lines. Verified
  headless that prefill→calc→results + the pie trio still render.
- [x] **Fixed `gatrack()` — was undefined site-wide.** Hundreds of `onclick="return gatrack(this)"`
  handlers referenced it but its only definition was commented out (used the removed UA `ga()`).
  Every tracked click threw a ReferenceError and logged nothing. Replaced with a live GA4 `gtag`
  version that fires an outbound `click` event and keeps the call contract.
- [ ] *(optional, low priority)* Evaluate dropping jQuery 1.11.1 for vanilla — see "Don't bother".
- [ ] *(optional, low priority)* Lazy-load the AdSense slot via IntersectionObserver.
- [ ] *(optional, low priority)* Split / minify the monolithic `index.html`.

### 2. Technical SEO — one-time, never rots (done)
- [x] `<link rel="canonical">`.
- [x] Schema.org `WebApplication` + `applicationCategory: "HealthApplication"` (`offers` free, `publisher`).
- [x] `FAQPage` schema (8 Q&As, JSON-LD matches visible text; protein range corrected 2026-06-29).
- [x] Better title: `Free Keto Macro Calculator – Find Your Macros for the Ketogenic Diet`.
- [x] Better meta description.
- [x] Remove dead Google+ share button + author link.
- [x] **Accessibility + image SEO pass** — `<html lang="en">` on all three pages; `alt` on all 19
  images; show-more toggles got `aria-label`/`aria-controls`/`aria-expanded`; brand-cyan
  `:focus-visible` ring.
- [x] **`sitemap.xml` + `robots.txt` Sitemap line (2026-06-29).**

### 3. Make hidden content indexable — ✅ DONE 2026-06-29
- [x] Converted all four `display:none` / `toggle_visibility()` blocks to native
  `<details>`/`<summary>` (Google crawls these; it discounts `display:none`). Sections: intro,
  carbs, protein, fat. The empty chevron triggers became descriptive, indexable summaries
  ("Net carbs vs. fiber — what actually counts?", "Why not just eat more protein?", etc.).
- [x] Kept the visual design (cyan chevron disc, indented left-bordered body, chevron flips on
  `[open]`, 650px measure). Intro video stays lazy via `ontoggle`. Removed the dead
  `toggle_visibility()` fn + its global export + the unused `.hidden-cls`/`.expandable` CSS;
  `:focus-visible` now targets `summary`.

### 4. Trust & E-E-A-T signals — compounds for health content (done)
- [x] Visible author byline under the intro, links to the `#aboutme` bio.
- [x] Inline "not medical advice" disclaimer right under the Personal Results macros.
- [x] Surface the Mifflin-St. Jeor citation (named in byline + results disclaimer).
- [x] **Explain the output** — the everyday-food equivalents card (see 2026-06-29 above).
- [x] **Removed an over-reaching medical claim** from the intro (2026-06-29) — important for a YMYL page.

### 5. FAQ section + schema — the one evergreen content play (done)
- [x] 8 evergreen Q&As covering the GSC query clusters (protein, carbs/ketosis, macros, high-fat foods,
  weight-loss, how-it-works, disclaimer).
- [x] Visible `#faq` section + `FAQPage` JSON-LD (text matches; protein range corrected 2026-06-29).

### 6. Shareable "your macros" result — AI-proof moat (done)
- [x] URL-param loading that **recalculates on load** so a shared link shows full results immediately;
  a `?key=value` link is authoritative over the saved cookie.
- [x] Page-level `twitter:card` (`summary_large_image`).
- [x] **"Share my macros" button** — `build_share_url()` serializes inputs to a URL + clipboard copy;
  verified the link reproduces the full result. This is the AI-proof moat.
- [ ] Per-result OG meta — **skip** (social scrapers don't run JS; would need SSR, off the table).

### 7. Embeddable widget — **DEFERRED (owner chose minimal scope 2026-06-29) — the backlink engine**
The single static authority play that targets the real bottleneck (ranking) and survives a no-touch
year. Still the most promising growth lever, but it is real new work with uncertain payoff (depends on
others embedding it), so it was put off for the minimal round. **Revisit at the 3-month review** (§9).
- [ ] Minimal `embed.html` (no sidebar, one ad max, calculator only).
- [ ] `<iframe>` embed snippet with a baked-in "Powered by keto-calculator.ankerl.com" backlink.
- [ ] A short "Embed this calculator" section on the page offering the snippet.

---

## Ad monetization — done the durable way

Goal: raise RPM via **viewability and placement quality**, NOT ad density.

### 8. Durable ad improvements
**Account has three real display units:** `7271241487` (Keto Top), `8747974681` (Keto Sidebar,
ex-"Keto Mid"), `1224707884` (Keto Bottom). **Two are live (2026-06-29):** "Keto Bottom" (`1224707884`, after the
results) and "Keto Sidebar" (`8747974681`, ex-"Keto Mid", repurposed as the **sticky sidebar
skyscraper**, 160×600, desktop-only). No Auto Ads, no in-form ads.
- [x] **Removed the two in-form ads** ("Keto Top" `7271241487`, "Keto Mid" `8747974681`) from the
  input/Calculate flow (invalid-click risk). The *units* still exist — "Keto Mid" was later repurposed
  for the sidebar; "Keto Top" is the only unit not currently placed.
- [x] **Keto Bottom** — one well-placed in-content responsive unit right after the results.
- [x] **Sidebar sticky skyscraper (2026-06-29)** — replaced the ~$3/mo Amazon book grid in the desktop
  sidebar with a 160×600 sticky display unit (`.sidebar-ad`) using the **real "Keto Sidebar" unit**
  (`8747974681`, renamed from "Keto Mid"). `#content` is a flex row at ≥830px so the sidebar stretches and the ad travels the
  page; the box is reserved (no CLS). Desktop-only (sidebar is `display:none` < 830px). *(An earlier
  draft pointed at `2426641084` "Keto Links" — a dead id whose unit had been deleted from the account;
  AdSense still served against the valid publisher id but with no per-unit reporting. Fixed 2026-06-29.)*
- [x] **Disabled AdSense Auto Ads in code** (removed `enable_page_level_ads:true`).
- [x] **Amazon books → one inline 4-book rec (2026-06-29)** — no longer in the sidebar (that's the ad
  now). A single `.recommended` block under "Learn Your Optimal Macronutrient Ratio", visible on desktop
  AND mobile, with a `.rec-label` for context. Trust/E-E-A-T, not a revenue play (books earn ~$3/mo).
- [x] **Perfect Keto affiliate banner removed.**
- [x] **Comment ads gone** — Disqus (free tier injected "forum" ads) replaced by **ad-free Cusdis**
  (2026-06-29), so there is no comment-widget ad source to disable anymore.
- [~] **Verify both units render/fill on the LIVE site** — **Keto Bottom confirmed on mobile**
  (2026-06-29); still confirm the sidebar skyscraper fills on desktop. (Note: Firefox ETP and ad
  blockers block AdSense entirely — test in a non-blocking browser.) (Next action #1.)
- [x] **Renamed "Keto Mid" → "Keto Sidebar"** in AdSense (2026-06-29) for clearer per-unit reporting.
- [ ] One **tasteful** mobile anchor ad MAY be worth it later — only if you monitor bounce + CWV and
  pull it if either worsens. Never full-auto.
- [ ] **⚠️ DASHBOARD ACTION (owner-only, not in code):** **AdSense → Ads → By site → Auto ads OFF** for
  the domain (the authoritative off-switch; the UI setting can re-inject auto ads from `adsbygoogle.js`
  alone). **Keep Auto Ads OFF long-term** — it over-stuffs a calculator page mid-task, hurts CWV, and
  risks invalid clicks that suppress account-wide RPM. (Next action #2.)

### 9. Instrument & set a review date — **the key remaining decision (next action #3)**
- [ ] Confirm AdSense + GSC are tracking RPM, viewability, Core Web Vitals.
- [ ] **Re-check in 3 months (≈ 2026-09-29)** → compare against the baseline (≈ €60/mo, ~4,850
  sessions/mo, 17% engagement) and decide double-down / harvest / sell **from data, not vibes**. If
  doubling down, the embeddable widget (§7) is the first thing to reconsider.

---

## Calibration items (accuracy/trust, not money-movers — owner's call)

Surfaced during the 2026-06-29 JS review. The math is correct; these are *calibration* choices that
shift everyone's output, so they were deliberately NOT changed unilaterally:
- **Activity multipliers are conservative** — `[1.1, 1.232, 1.386, 1.617]` vs the textbook
  Harris-Benedict 1.2–1.9. Defensible (people overestimate activity), but it makes TDEE run low.
- **Body-fat estimate is a non-standard regression that omits age** — `1.12·kg/height_m − 30.84`.
  Produces plausible values but the standard **Deurenberg** (`1.20·BMI + 0.23·age − 10.8·sex − 5.4`)
  is more defensible. Can be prototyped side-by-side before any change.

---

## Don't bother with / actively avoid

**Avoid (quick RPM, long-term harm):**
- ❌ AdSense Auto Ads on full-auto — cedes placement, over-stuffs, hurts CWV/UX.
- ❌ Vignette / full-screen interstitials — bad UX + intrusive-interstitial ranking penalty.
- ❌ Ad refresh / high ad density — short-term cents, long-term UX + policy risk.
- ⚠️ Ezoic / third-party mediation — real RPM upside but adds latency and usually hurts CWV; only
  consider after the speed work, and measure CWV before/after.

**Don't bother (low ROI now, or violates the no-touch constraint):**
- **Dropping jQuery / splitting / minifying `index.html`** — speed is already handled; risk and effort
  outweigh a marginal CWV gain on an already-fast page.
- **More schema/meta/title tinkering** — diminishing returns; on-page SEO is done.
- Blog posts / content calendar / social posting.
- CMS migration (WordPress etc.).
- Building 15+ AI-generated calculator variants (Helpful Content buries these).
- Email list (requires ongoing maintenance).
- Mediavine/Raptive — site is far below their traffic thresholds.

---

## Reference
- Council runs: `md/peer.md` (older), 2026-06-28 + 2026-06-29 verdicts folded in above.
- SEO audit + action plan: `md/seo-audit-2026-06-29.md`, `md/seo-action-plan.md`.
- Codebase tech details: `CLAUDE.md`.
- Analytics findings: `md/analytics-summary.md`.
- AdSense pub: `ca-pub-2398468033418589` — three real units: `1224707884` (Keto Bottom, after
  results — live), `8747974681` (Keto Sidebar, ex-Keto Mid — live, the desktop sidebar skyscraper),
  `7271241487` (Keto Top — not currently placed). The old `2426641084` "Keto Links" id is dead.
- Comments: **Cusdis** (ad-free; replaced Disqus 2026-06-29).
- Amazon affiliate tag: `martanke-20`.

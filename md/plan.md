# Redesign Plan (keto-calculator)

One-time overhaul. No ongoing updates. Static site stays static.

## Guiding principle

**Prefer durable, compounding improvements over quick wins that hurt long term.**
The owner optimizes for long-term ad revenue health, not a short RPM spike. Anything
that raises this month's earnings while degrading UX, page speed, trust, or Google
ranking is a net loss and must be avoided — even if AdSense allows it.

Revenue = traffic × engagement × RPM. The durable way to grow all three is a fast,
trustworthy, well-ranked page that loyal users keep returning to — not ad stuffing.

## Prerequisite: check demand first

Open Google Search Console → last 16 months of **impressions**.
- Flat/rising → proceed with the full plan below.
- Falling → do 2 hours of cleanup only, then harvest or sell the domain.

(Context: keto search demand peaked ~2019–2020 and AI Overviews now intercept many
informational queries. Organic recovery is upside, not a guarantee. The reliable base
is the 74% Direct + 11% Social loyal traffic — protect it.)

---

## ✅ Already done (session 2026-06-27)

- [x] **Analytics confirmed live** — GA4 "keto-calculator GA4 36863101" flowing via GTM container `GTM-TC6WLFB`
- [x] **Mobile layout** — responsive `@media (max-width:900px)` block: single-column, fluid `#main`/`#sidebar`, `clamp()` headings, 16px inputs (no iOS zoom), larger radio targets
- [x] **Viewport fixed** — removed `user-scalable=no`/`maximum-scale` (was blocking pinch-zoom + hurting CWV)
- [x] **Mobile polish** — hid `#broughttoyou` self-URL, smaller logo, sidebar moved up, form-row spacing

---

## The durable foundation (do these first — they compound and never rot)

### 1. Core Web Vitals / page speed (1–2 days) — **highest long-term leverage**
Speed lifts BOTH Google ranking AND ad viewability (viewability directly sets RPM),
so this is the rare lever that helps traffic and monetization at once. Permanent gain.
- [ ] Remove OneSignal entirely (`cdn.onesignal.com` + the notifyButton popup) — earns €0, slows load, the arrival popup scares new users and hurts trust
- [ ] Extract jQuery + calculator JS out of `index.html` into separate files, add `defer`
- [ ] Evaluate dropping jQuery 1.11.1 for vanilla JS (it's ~96KB and the calculator uses little of it)
- [ ] `preconnect` for Google Fonts + `font-display: swap`
- [ ] Lazy-load below-the-fold AdSense slots (Intersection Observer) — improves CWV without losing impressions
- [ ] Split / minify the 375KB monolithic `index.html`
- [ ] Remove the dead `UA-36863101-1` analytics.js snippet (does nothing now)

### 2. Technical SEO (2–3 hours) — one-time, never rots
- [ ] `<link rel="canonical" href="https://keto-calculator.ankerl.com/">`
- [ ] Schema.org `Organization` → `WebApplication` + `applicationCategory: "HealthApplication"`
- [ ] Add `FAQPage` schema (pairs with the FAQ section below)
- [ ] Better title: `Free Keto Macro Calculator – Find Your Macros for the Ketogenic Diet`
- [ ] Better meta description: `Calculate your exact keto macros in 60 seconds. Enter your weight, height, and goal — get personalized carbs, protein, and fat targets for the ketogenic diet.`
- [ ] Remove dead Google+ share button

### 3. Make hidden content indexable (2–3 hours)
The `hidden-cls` / `toggle_visibility()` sections use `display:none` — Google may skip them.
- [ ] Convert to `<details>`/`<summary>` (Google indexes these) or visible-by-default with JS collapse
- [ ] Sections: intro detail, carb detail, protein detail, fat detail

### 4. Trust & E-E-A-T signals (2–3 hours) — compounds, matters more every year for health content
- [ ] Visible author byline + brief bio above the fold (not just footer)
- [ ] Inline "not medical advice" disclaimer near the results
- [ ] Surface the Mifflin-St.Jeor citation + NCBI links next to the BMR formula (already there, buried)
- [ ] Explain the output: "142g fat — here's what that looks like in actual food" (makes the number feel real, not made-up)

### 5. FAQ section + schema (half day) — the one evergreen content play
- [ ] 8–10 evergreen Q&As ("How many carbs on keto?", "What is a macro?", "How fast will I lose weight?")
- [ ] Visible HTML section near the bottom
- [ ] `FAQPage` JSON-LD — featured-snippet potential, durable

### 6. Shareable "your macros" result — AI-proof moat (half day)
The one thing AI Overviews can't replicate, and it feeds the Direct + Social traffic that is already 85% of the site.
- [ ] URL-param loading already works (`?kg=80&height=175`) via `load_url_params()`
- [ ] "Share your macros" button that writes current form values into the URL
- [ ] Per-result OG meta for rich link previews

### 7. Embeddable widget (optional) — set-and-forget backlink engine
- [ ] Minimal `embed.html` (no sidebar, one ad max)
- [ ] `<iframe>` embed code with a baked-in "Powered by keto-calculator.ankerl.com" backlink
- [ ] The only organic link-building move that survives a no-touch year

---

## Ad monetization — done the durable way

Goal: raise RPM via **viewability and placement quality**, NOT ad density. A faster,
cleaner page with a few well-placed, highly-viewable ads beats a page stuffed with units.

### 8. Durable ad improvements
- [ ] One well-placed in-content responsive ad **right after the results table** — peak attention + dwell time = high viewability, not intrusive
- [ ] Ensure all ad units are responsive and render correctly on mobile (65.5% of traffic)
- [ ] Keep ads clear of the inputs / Calculate flow — prevents accidental clicks (invalid-click penalties quietly suppress your whole account's RPM long term)
- [ ] Move Amazon book links from the mobile-invisible sidebar into the content flow near relevant sections
- [ ] Confirm Perfect Keto affiliate link still active
- [ ] One **tasteful** mobile anchor ad MAY be worth it — but only if you monitor bounce rate + CWV after; pull it if either worsens

### 9. Instrument & set a review date
- [ ] Confirm AdSense + GSC reporting is tracking RPM, viewability, Core Web Vitals
- [ ] Re-check in 3 months → decide double-down / harvest / sell from data, not vibes

---

## Don't bother with / actively avoid

**Avoid (quick RPM, long-term harm — fails the guiding principle):**
- ❌ **AdSense Auto Ads on full-auto** — cedes placement to Google, over-stuffs the page, hurts CWV and UX. If used at all, enable *only* the anchor format and keep manual control of in-content slots.
- ❌ **Vignette / full-screen interstitial ads** — bad UX and risks Google's intrusive-interstitial ranking penalty.
- ❌ **Ad refresh / high ad density** — short-term cents, long-term UX + policy risk.
- ⚠️ **Ezoic / third-party mediation** — real RPM upside, but adds a third-party dependency + latency and often hurts Core Web Vitals. Only consider *after* the speed work above, and measure CWV before/after; do not adopt if it regresses speed.

**Don't bother (low ROI or violates the no-touch constraint):**
- Blog posts / content calendar / social posting
- CMS migration (WordPress etc.)
- Disqus replacement
- Building 15+ AI-generated calculator variants (Helpful Content buries these)
- Email list (requires ongoing maintenance)
- Mediavine/Raptive applications — site is far below their traffic thresholds (~50k sessions / 100k pageviews per month)

---

## Reference
- Council runs: `md/peer.md` (older), this session folded in above
- Codebase tech details: `CLAUDE.md`
- Analytics findings: `md/analytics-summary.md`
- AdSense pub: `ca-pub-2398468033418589` — slots: 7271241487, 8747974681, 1224707884
- Amazon affiliate tag: `martanke-20`

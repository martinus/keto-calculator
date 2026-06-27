# Redesign Plan (council session 2026-06-27)

One-time overhaul. No ongoing updates. Static site stays static.

## Prerequisite: check demand first

Open Google Search Console → last 16 months of **impressions**.
- Flat/rising → proceed with the full plan below.
- Falling → do 2 hours of cleanup only, then harvest or sell the domain.

---

## Priority checklist (ranked by impact vs effort)

### 1. Analytics ✅ DONE
- [x] GA4 property "keto-calculator GA4 36863101" confirmed active
- [x] Data flows via GTM container GTM-TC6WLFB (configured inside GTM, no explicit G- tag needed in HTML)
- [ ] Optional: remove the dead `UA-36863101-1` analytics.js snippet from index.html (saves ~20KB, no longer does anything)

### 2. Core Web Vitals / page speed (1–2 days)
- [ ] Remove or defer OneSignal (`<script src="cdn.onesignal.com/..." async>` → move to end of body or remove entirely)
- [ ] Defer AdSense script (`async` is already set, but move below fold init)
- [ ] Add `preconnect` for Google Fonts, switch to `font-display: swap`
- [ ] Extract jQuery + calculator JS out of index.html into separate files, add `defer`
- [ ] Lazy-load AdSense slots below the fold (use Intersection Observer)
- [ ] Remove `user-scalable=no` from viewport meta tag

### 3. Technical SEO (2–3 hours)
- [ ] Add `<link rel="canonical" href="https://keto-calculator.ankerl.com/">`
- [ ] Fix Schema.org type: `Organization` → `WebApplication` + `applicationCategory: "HealthApplication"`
- [ ] Add `FAQPage` schema for the Q&A content already on the page
- [ ] Better title: `Free Keto Macro Calculator – Find Your Macros for the Ketogenic Diet`
- [ ] Better meta description: `Calculate your exact keto macros in 60 seconds. Enter your weight, height, and goal — get personalized carbs, protein, and fat targets for the ketogenic diet.`
- [ ] Remove dead Google+ share button from sidebar

### 4. Make hidden content indexable (2–3 hours)
- [ ] The `hidden-cls` / `toggle_visibility()` expandable sections use `display:none` — Google may skip them
- [ ] Convert to `<details>`/`<summary>` (indexed by Google) or make visible by default with JS-driven collapse
- [ ] Affected sections: intro detail, carb detail, protein detail, fat detail

### 5. FAQ section + schema (half day)
- [ ] Write 8–10 evergreen Q&As (e.g. "How many carbs on keto?", "What is a macro?", "How fast will I lose weight?")
- [ ] Add as visible HTML section near the bottom of the page
- [ ] Mark up with `FAQPage` JSON-LD — featured snippet potential

### 6. Trust & E-E-A-T signals (2–3 hours)
- [ ] Remove the push-notification popup (OneSignal notifyButton) — it screams spam to new visitors
- [ ] Add visible author byline with brief bio above the fold (not just in the footer)
- [ ] Add inline disclaimer near the results ("not medical advice")
- [ ] Add citation badges next to the BMR formula (Mifflin-St.Jeor, NCBI links already exist but buried)
- [ ] Explain the output number: "142g fat — here's what that looks like in actual food" (makes result feel real, not made-up)

### 7. Shareable result URL — AI-proof moat (half day)
- [ ] URL param loading already works (`?kg=80&height=175` etc.) via `load_url_params()`
- [ ] Add a "Share your macros" button that writes all current form values into the URL
- [ ] Add an OG meta tag dynamically with the result summary for link previews
- [ ] This is the one thing AI Overviews cannot replicate: a personalized, shareable result

### 8. Ad & affiliate optimization (2 hours)
- [ ] Move Amazon book links from sidebar (invisible on mobile) into content flow near relevant sections
- [ ] Add one more AdSense slot directly after the results table (highest-engagement moment)
- [ ] Move ads away from the Calculate trigger to avoid misclicks (reduces invalid clicks)
- [ ] Review Perfect Keto affiliate link is still active

### 9. Embeddable widget (optional, passive backlink engine)
- [ ] Create a minimal `embed.html` version of the calculator (no sidebar, no ads except one)
- [ ] Offer `<iframe>` embed code with a "Powered by keto-calculator.ankerl.com" backlink baked in
- [ ] This is the one set-and-forget organic link-building move that survives a no-touch year

---

## Don't bother with
- Blog posts / content calendar
- CMS migration (WordPress etc.)
- Disqus replacement
- Social media / Pinterest
- Building 15+ AI-generated calculator variants (Helpful Content buries these)
- Email list (requires ongoing maintenance)

---

## Reference
- Previous council run (older): `md/peer.md`
- Technical details of current codebase: `CLAUDE.md`
- AdSense pub: `ca-pub-2398468033418589` — slots: 7271241487, 8747974681, 1224707884
- Amazon affiliate tag: `martanke-20`

# SEO Action Plan — keto-calculator.ankerl.com

Prioritized from the 2026-06-29 audit. Site stays **static / no-build / one-time**; every item
below is set-once and evergreen. Effort = rough one-time work. Full detail in the first audit
[`seo-audit-2026-06-29.md`](seo-audit-2026-06-29.md) and the post-fix re-audit
[`seo-audit-2026-06-29-v2.md`](seo-audit-2026-06-29-v2.md).

> **Status (2026-06-29):** items 1–10 implemented, deployed, and **verified live**. Re-audit score
> **78 → 85/100**. Every actionable finding is closed. The **only** remaining item is the optional
> evergreen content page (#7) — a deliberate traffic choice that bends the no-touch constraint.

## Do first (highest impact)

1. ✅ **DONE — Make the Google Fonts stylesheet non-render-blocking.** *(effort: 5 min)*
   CWV field data already passes (LCP 2.1s / INP 143ms / CLS 0.09), so no big speed work is needed.
   The one confirmed render-blocking resource is the Google Fonts request (~780ms). Swap the
   `<link rel="stylesheet">` for the `preload` + `media="print" onload="this.media='all'"` + `<noscript>`
   pattern. `&display=swap` is already set, so appearance is unchanged. No Charts/AdSense JS surgery
   needed — field INP is fine.

2. ✅ **DONE — Add `Person` author schema (E-E-A-T / YMYL).** Added `author` Person to the
   WebApplication JSON-LD (name + `sameAs` → blog, reddit, GitHub). Both JSON-LD blocks re-validated.

3. ✅ **DONE — Add `/llms.txt`.** Created at repo root: site summary, page links, key keto facts.

## Quick wins (trivial, do in one pass)

4. ✅ **DONE — Trimmed `og:description`** to 130 chars.
5. ✅ **DONE — Added `og:site_name`, `og:locale`, `og:image:width`/`height`** (image is actually
   1200×630, the ideal OG ratio — despite the `_1600_` filename).
6. ✅ **DONE — Explicitly allow AI crawlers in `robots.txt`** (GPTBot, OAI-SearchBot, ChatGPT-User,
   ClaudeBot, PerplexityBot, Google-Extended → `Allow: /`).

## Performance follow-ups (from later PageSpeed runs — all DONE)

9. ✅ **DONE — Preconnect to `consent.cookiebot.com` + `www.gstatic.com`** (4 preconnects total, the
   recommended max). Cookiebot was the explicit ~300ms LCP-savings candidate; gstatic shortens the
   Charts-loader chain.
10. ✅ **DONE — Lazy-load Google Charts on first calculation** (`ensure_charts_loaded()` injected from
    `wait_until_deadline`). ~249 KiB no longer downloads for visitors who don't complete the form.

**Lab result (mobile, before → after all changes):** FCP 3.3→2.1s · LCP 8.4→6.9s · **TBT 490→0ms** ·
CLS 0.09→0.02 · Speed Index 3.9→2.1s. **Field CWV stays all-green** (LCP 2.1s / INP 143ms / CLS 0.09)
and should drift better as CrUX's 28-day window catches up. Residual lab LCP 6.9s = a late-painting
AdSense unit — left alone on purpose (field LCP is green; the cause is revenue). **Performance: done.**

8. ✅ **DONE — All outbound links → HTTPS.** Converted every outbound `http://` link to `https://`
   (verified each domain serves HTTPS); removed the dead HTTP-only `paindatabase.com` link. **Zero
   `http://` outbound links remain.** Amazon `martanke-20` affiliate tag preserved.

## Optional / only if you want the traffic lever

7. **One evergreen supporting page** (e.g. "Keto macros explained" / "Net vs total carbs"), linked
   from the FAQ. The main topical-authority lever — but it does nudge the no-touch constraint, so
   treat it as a deliberate choice, not a must. *(effort: a few hours, once)* **← the only open item.**

## Don't bother

- **FAQPage rich results** — restricted to gov/health-authority sites since Aug 2023; a commercial
  calculator won't get the accordion. Keep the schema (still feeds AI answers) but expect no rich result.
- **Security headers / HSTS** — not an SEO ranking factor, and GitHub Pages can't set custom headers.
- **WebP/AVIF conversion** — field CWV is green and lab TBT is 0, so no image-driven LCP problem to fix.
- **Trimming the 465 KiB "unused JS"** — ~60% is mandatory third-party (AdSense=revenue, Cookiebot=legal
  consent, gtag=analytics); only the Charts portion was deferrable and now is. The rest can't be trimmed.
- **Lab LCP 6.9s** — late-painting AdSense unit under throttling; field LCP is 2.1s (green). Chasing it
  means shrinking an ad. Don't.
- **Anything recurring** — blog cadence, content calendars, social posting: all violate the no-touch goal.

## Remaining (deferred by choice)

**Only item 7** (one evergreen content page) is open — and it's optional, the one lever that bends
the no-touch constraint. Everything else from both audits is done and verified live. Next concrete
step is not a fix but a **decision at the 3-month review (≈ 2026-09-29)**: compare RPM / engagement /
CWV against baseline and choose double-down (start with #7) / harvest / sell.

## The one thing to do (and it's not a fix)

Hold the line and **re-measure at the 3-month review**. On-page + technical SEO are comprehensively
done (85/100); the remaining ceiling is domain authority + keto demand, which no on-page change moves.

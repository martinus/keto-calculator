# Revenue Growth Plan — July 2026

Owner asked (2026-07-02): **"I want the keto calculator to earn more revenue."** This plan
supersedes the "minimal no-touch year" scope chosen 2026-06-29 in `dev/docs/plan.md` — the owner is
now explicitly opting into revenue work. The guiding principle from `plan.md` still stands:
**durable, compounding improvements over quick wins that hurt long term.** Nothing below
violates the avoid-list (no Auto Ads full-auto, no interstitials, no ad refresh, no density
stuffing).

---

## 1. Where revenue actually stands (analysis)

**Revenue = sessions × pages/session × page RPM.** Baseline from `dev/docs/analytics-summary.md`:
~4,850 sessions/mo, ~€60/mo ≈ €12.4 per 1,000 sessions averaged over 12 months. 65% mobile,
74% loyal Direct traffic, on-page SEO done (85/100 audit), field CWV all green.

### What changed since the last plan (critical context)

1. **A consent-mode bug was silently collapsing RPM — found and fixed 2026-07-01.**
   The Consent Mode v2 defaults added 2026-06-28 denied `ad_storage`/`ad_user_data`/
   `ad_personalization` **globally** with no region filter. Every visitor — including the
   ~70%+ non-EEA majority — got non-personalized ads unless they clicked Accept on the
   Cookiebot banner, which most never saw a reason to do. Page RPM collapsed **€8–9 → ~€1.6**.
   Fixed by region-scoping: granted worldwide, denied only in EEA/UK pending consent
   (`bcb0446`, `edf8191`, `1c21ea4`).
2. **Cookiebot was replaced by Google's own CMP** (AdSense → Privacy & messaging /
   Funding Choices, `9513f13`) and this is **deployed to live master**. Google now serves the
   GDPR message to EEA/UK visitors with its own geo-detection and feeds Consent Mode v2
   automatically. ⚠️ This only works if the GDPR message was **created and PUBLISHED in the
   AdSense UI** — if not, EEA/UK visitors get no prompt and stay at denied (= near-zero EEA ad
   revenue). Verifying this is action #1.
3. **A complete German translation (`/de/`) exists but is held back** (`00e855b`) — built,
   generator-maintained (`dev/build_de.py`), excluded from deploy/sitemap/hreflang. Launching
   it is a nearly-free traffic lever.

### The honest read

- The single biggest revenue event of the year already happened: **un-collapsing the consent
  defaults.** That is *recovery* back to the ~€8–9 page-RPM norm, not growth — but it means
  July's numbers will look dramatically better than late June's, and **no other lever can be
  judged until a clean post-fix baseline exists.**
- The durable *growth* levers, in order of leverage:
  **(a)** mobile ad coverage — 65% of traffic currently sees exactly **one** ad (Keto Bottom);
  the sidebar skyscraper is desktop-only. This is the largest untapped on-page dial.
  **(b)** traffic — on-page SEO is maxed; what's left is the German page (built!), the
  embeddable-widget backlink engine (deferred in `plan.md` §7), and 1–3 evergreen pages for
  the long-tail queries GSC already shows the site surfacing for.
  **(c)** consent yield in the EEA — the CMP message design/settings decide what fraction of
  EEA traffic monetizes at all.
- Affiliate is a rounding error today (~$3/mo) and will stay small; worth one cheap pass, not
  a strategy.

---

## 2. The plan

### Tier 0 — Verify & re-baseline (this week, mostly owner/dashboard — do FIRST)

- [x] **T0.1 Confirm the Google CMP GDPR message is published** — ✅ **verified 2026-07-02**:
  message is published and working; AdSense reports it has been shown 4 times (EEA/UK
  impressions are a minority of traffic, so low counts right after launch are expected).
  Worth a re-glance alongside T0.3: message shows + a healthy accept rate as EEA volume
  accumulates.
- [x] **T0.2 Verify the desktop sidebar skyscraper (`8747974681`) fills and sticks** —
  ✅ **verified 2026-07-02**: owner confirms the skyscraper renders and stays visible
  while scrolling.
- [ ] **T0.3 Watch AdSense page RPM daily for ~2 weeks** (through ≈ 2026-07-15). Expected:
  recovery toward €8–9 page RPM. Record the stabilized number in this file as the **new
  baseline** — every Tier 1/2 lever is measured against it, not against the polluted June data.
- [x] **T0.4 Confirm Auto Ads are OFF in the dashboard** — ✅ **verified 2026-07-02** by the
  owner. (T1.2's anchor-only trial will deliberately flip this on with only the Anchor format
  enabled — that's the planned exception, not drift.)

### Tier 1 — Mobile ad coverage & RPM (code, ~1–2 hours total; ship after T0.3 baseline)

- [ ] **T1.1 Place the unused "Keto Top" unit (`7271241487`) as a second in-content unit
  visible on mobile.** Concrete spot: **after the FAQ block (`#faq`), before the "Got
  Questions?" section** (~line 2165 of `index.html`) — deep in content, ~2,000 words below the
  input/Calculate flow (no invalid-click risk), on a section boundary (no reading interruption),
  and seen by the 65% mobile majority that currently gets one ad. Responsive format, reserved
  min-height to avoid CLS. *Expected: mobile goes 1 → 2 impressions/session; rough +€15–30/mo
  at recovered RPM.*
- [ ] **T1.2 Trial a mobile anchor ad — the measured way.** In the AdSense dashboard enable
  Auto ads for the domain with **every format OFF except Anchor** (this is not "full-auto"
  Auto Ads; placement stays fixed, screen-edge, dismissible). Anchor ads are consistently the
  highest-RPM mobile format. **Guardrails:** run 2–3 weeks; revert if field CLS/INP degrade
  (CrUX / PageSpeed), if engagement rate drops vs. the T0.3 baseline, or if it visually
  collides with the results card or share bar on iPhone widths. *Expected: +10–30% mobile RPM
  if kept; €0 if reverted — strictly reversible.*
- [ ] **T1.3 (optional, after T1.1/T1.2 settle) Multiplex unit at the very bottom** (below
  comments, above the footer) — native-style grid, monetizes the deepest scrollers; negligible
  UX cost because nothing is below it. Skip if T1.1+T1.2 already feel like the page's polite
  maximum: **three fixed placements + anchor is the ceiling. Never more.**

### Tier 2 — Traffic & rankings (revised 2026-07-02; compounding, the only way past the RPM ceiling)

**Strategy note — why this revision.** On-page SEO is maxed (85/100) and field CWV is green;
no tag or speed tweak moves the "keto calculator" head term off page 2–3. What gates that
ranking is **domain authority (links)**, and what caps traffic is **owning exactly one URL in
one language in the most contested, most AI-Overview-intercepted SERP there is**. So the
revised strategy attacks three softer flanks instead of the fortified one:
**(1) earn real links once** (story post + widget + Reddit), **(2) open less-competitive
SERPs** (languages; long-tail *tool* queries where a calculator, not an article, matches
intent), **(3) be the answer AI engines cite** (already strong: llms.txt, FAQ, shareable
URLs). Head-term rank then rises as a side effect of authority — not the other way around.

- [x] **T2.1 Launch the German page `/de/`** — **code done 2026-07-02** (commit `8fa6600`):
  hreflang + switcher + sitemap live, deploy.sh ships `de/`, the 21 drifted generator
  mappings re-anchored/retranslated (HTTPS links, lbs-first copy, richer bio, FAQ
  contraindications), QA'd headless (identical results EN/DE, zero JS errors, GA4 + ads +
  Cusdis `/de/` + hreflang verified). **Remaining: merge + deploy to the live repo, then
  submit `/de/` in Search Console.**
  *Non-English SERPs are far less competitive and see fewer AI Overviews; "keto rechner" has
  no dominant incumbent; German AdSense RPMs are among the EU's highest. This is the
  highest-probability ranking win available. Expected: builds to +5–15% sessions over 2–3
  months.*
- [ ] **T2.2 NEW — The story post + Hacker News launch (the real backlink engine).** Write
  ONE post on the owner's blog (ankerl.com — an established dev blog with real audience):
  *"My 12-year-old keto calculator was blank for 4 seconds on every visit"* — the true story
  of the overhaul: the sunset Google Optimize snippet holding `<html>` at `opacity:0`, the
  dead UA tag, the consent-mode default that collapsed RPM ~5×, the 375KB→flat no-build
  rescue. Submit to HN / r/programming / lobste.rs once. *This is classic front-page material
  (dead-third-party-script archaeology + small-web economics), and every link it earns —
  including to the calculator itself and the embed widget it showcases — is a genuine,
  editorially-given backlink. One post, one submission, no cadence. By far the
  highest-leverage authority play this site has, because it uses an asset competitors don't
  have: the owner's dev-community standing.* Ship the widget (T2.3) first so the post can
  offer it.
- [x] **T2.3 Build the embeddable widget (`embed.html`)** — **done 2026-07-02.** Generated
  from `index.html` by `dev/build_embed.py` (build_de.py philosophy: derived, can't drift; fails
  loudly on stale anchors). Full calculator/results/forecast, compact branded header,
  noindex, `<base target="_blank">`, powered-by credit top + bottom, "Share my macros" from
  an embed hands out the FULL site's URL. **Zero ads** (ads in iframes on third-party sites
  are an AdSense policy risk — the widget's value is backlinks + brand traffic, deviating
  from plan.md §7's "one ad max" on purpose). "Embed This Calculator" section (EN + DE) hands
  out the snippet; the visible credit link under the iframe is the actual backlink.
- [~] **T2.4 Supporting pages — three article guides already exist (discovered 2026-07-02).**
  A 2026-06-29 session had created `net-carbs-vs-total-carbs.html`,
  `how-much-protein-on-keto.html`, and `how-fast-will-i-lose-weight-on-keto.html` **directly
  in the live repo** (design-system articles with FAQ/Article schema, one Keto Bottom ad
  each, a "Keto Guides" section + 9 internal links on the homepage). They were missing from
  the source repo — back-ported 2026-07-02, and their consent stack (still Cookiebot +
  deny-everywhere, i.e. the RPM-collapse config) was **modernized to the region-scoped
  Google-CMP pattern**. These cover the exact GSC query clusters this item targeted, so the
  text-page half is DONE. **Still open (optional):** upgrading them with a small interactive
  element each (net-carbs calculator, protein calculator) — tools match "calculator" intent
  better and resist AI Overviews; decide after GSC shows how the articles index.
- [ ] **T2.5 One-time link pass, upgraded:** (a) ask the r/keto mods to list the calculator
  in the community wiki/FAQ (it's already organically posted there — Reddit pages
  themselves now rank in Google, so this is a link AND a durable traffic pipe); (b) add a
  normal link from the ankerl.com blog's homepage/about to the calculator (root-domain →
  subdomain internal authority); (c) submit once to the few quality directories. An
  afternoon, once.
- [ ] **T2.6 (only if T2.1 works) Spanish translation** via the same `build_de.py` pattern —
  decide at the 3-month review with `/de/` data in hand. Spanish is the largest
  low-competition keto SERP after German.
- [ ] **T2.7 (free, low-confidence) CTR polish at current positions:** add the current year
  to the `<title>` ("Free Keto Macro Calculator (2026) – …") and re-check GSC CTR after 4
  weeks — year-in-title reliably lifts CTR near page-1 boundaries; revert if impressions
  wobble. One-line change, reversible.

**What we deliberately do NOT do for traffic:** no 15 thin calculator variants (Helpful
Content bait — T2.4 stops at 2–3 *real* tools), no blog cadence, no social calendar, no
domain migration off the `keto-calculator.ankerl.com` subdomain (its age + exact-match name
are assets; a move resets history for a speculative gain).

### Tier 3 — Affiliate (one cheap pass, low expectations)

- [ ] **T3.1 Contextual Amazon links where purchase intent actually exists** (tag
  `martanke-20`): ketone test strips in the FAQ answer about ketosis, a food scale in the
  food-equivalents/tracking context, MCT oil in the high-fat-foods answer. Text links in
  prose, not banners; nowhere near the input flow. `TODO.txt` suggested Ketostix years ago.
  *Expected: €5–15/mo. Cap the effort at one hour.*
- [ ] **T3.2 Do NOT chase third-party mediation (Ezoic etc.) yet.** Revisit only at the
  review, only if recovered RPM still disappoints, and only with before/after CWV measurement
  — their scripts routinely break green CWV, which is worth more than their uplift here.

---

## 3. What we still do NOT do

Unchanged from `plan.md`: ❌ full-auto Auto Ads (anchor-only trial in T1.2 is the deliberate
exception) · ❌ vignettes/interstitials · ❌ ad refresh / density stuffing · ❌ 15 AI-spun
calculator pages · ❌ email list / social calendar / CMS · ❌ ads near the inputs or Calculate
flow — the invalid-click rule is absolute.

---

## 4. Measurement & decision points

| When | What |
|---|---|
| ≈ 2026-07-15 | T0.3: record the **post-consent-fix baseline** (page RPM, €/mo run-rate) in this file |
| +2–3 weeks after each Tier-1 ship | keep/revert call from AdSense per-unit reports + CrUX + GA4 engagement |
| ≈ 2026-09-29 (kept from `plan.md`) | full review: revenue vs. baseline, `/de/` indexing & sessions, widget adoption, evergreen-page impressions → double-down / hold / harvest, and the Ezoic + Spanish decisions |

**Success criteria for the quarter:** page RPM recovered to ≥ €8; mobile serving 2 ad
placements (+ anchor if it survived its guardrails); `/de/` live and indexed; widget shipped;
story post published + submitted once; revenue run-rate **≥ €120/mo** (2× the old baseline)
without any CWV metric leaving green or engagement dropping below the 17% baseline.

### Rough expected impact (honest ranges, at ~4,850 sessions/mo)

| Lever | €/mo effect | Confidence |
|---|---|---|
| Consent fix (done) + CMP published (T0.1) | recovery to ~€60–90 run-rate | high — this already happened; verify it sticks |
| Second mobile unit (T1.1) | +€15–30 | high |
| Anchor ad (T1.2) | +€10–25 | medium — conditional on guardrails |
| German `/de/` (T2.1) | +€5–20, growing | medium |
| Story post + HN (T2.2) | ~€0 direct; the main authority/backlink event | medium — one shot, high variance |
| Widget + link pass (T2.3/T2.5) | ~€0 short-term; raises the traffic ceiling | low/slow, compounding |
| Companion tools (T2.4) | +€5–15, growing | medium |
| Affiliate pass (T3.1) | +€5–15 | medium |

Plausible quarter-end run-rate: **€120–180/mo** vs. the €60 baseline — with the same page
speed, trust, and UX that took two overhaul sessions to build.

---

## 5. Sequencing

1. **Now:** ~~T0.1, T0.2, T0.4~~ — ✅ all verified 2026-07-02. Only T0.3 (RPM watch) runs on.
2. **This week:** T2.1 German launch QA + deploy (independent of ad experiments), T3.1
   affiliate pass, T2.5 link pass, T2.7 title-year tweak.
3. **≈ Jul 15 (baseline recorded):** ship T1.1; a week later start the T1.2 anchor trial.
4. **July:** T2.3 widget, then T2.2 story post + HN submission (the post showcases the widget).
5. **August:** T2.4 companion tools (net-carbs, protein).
6. **Sep 29:** the review (§4) decides everything else (incl. T2.6 Spanish).

---

## Reference

- Prior roadmap + avoid-list rationale: `dev/docs/plan.md` (its §8/§9 verification items are folded
  into Tier 0 here).
- Analytics baseline: `dev/docs/analytics-summary.md` · SEO ceiling: `dev/docs/seo-audit-2026-06-29-v2.md`.
- Consent bug + fix: commits `bcb0446`, `edf8191`, `1c21ea4`; CMP migration `9513f13`.
- German page: `dev/TRANSLATION.md`, `dev/build_de.py`; holdback commit `00e855b`.
- Ad units: `7271241487` Keto Top (**unplaced — T1.1 uses it**), `8747974681` Keto Sidebar
  (live, desktop sticky), `1224707884` Keto Bottom (live, after results). Dead: `2426641084`.
- AdSense pub `ca-pub-2398468033418589` · Amazon tag `martanke-20`.

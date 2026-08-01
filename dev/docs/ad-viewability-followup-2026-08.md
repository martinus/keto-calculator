# Ad viewability follow-up — measure from 2026-08-15

**Status:** waiting on data. Shipped 2026-08-01 (PR #8, squash `e43a985`). Read this before
touching anything ad-related; it carries the baseline the change has to be judged against.

## Why the change happened

Page RPM history: **€9** (full Auto Ads, pre-refactor) → **€1.9** (3 manual units, Auto Ads
off) → **€3.3** (anchor-only Auto Ads re-enabled). Decomposing the €9 → €1.9 drop:

| | Before | After | Factor |
|---|---|---|---|
| Impression RPM | €3.76 | €1.39 | **2.7×** |
| Impressions / pageview | ~2.4 | ~1.4 | 1.75× |
| Page RPM | €9 | €1.9 | 4.7× |

The dominant term is **price per impression, not ad count**. Auto Ads was never stuffing the
page — ~2.4 filled impressions per pageview, barely more than three manual units. What the
refactor actually did was keep the cheap deep-page inventory and delete the valuable
high-viewability placements. "Add more units" was the wrong instinct; raising viewability
was the right one.

## Baseline — AdSense, 2026-07-22..28, immediately pre-change

Blended: **1,371 impressions · €1.77 · €1.29 impression RPM · 30.7% viewable**

| Unit | Platform | Impr | Impr RPM | Viewable |
|---|---|---|---|---|
| Keto Bottom | Mobile | 382 | €0.90 | 31.2% |
| **Keto Top** | **Mobile** | **325** | **€0.81** | **18.2%** |
| Keto Sidebar | Mobile | 214 | €0.12 | **0.0%** ← the bug |
| Keto Sidebar | Desktop | 164 | €2.62 | 70.1% |
| Keto Bottom | Desktop | 125 | €3.42 | 55.2% |
| Keto Top | Desktop | 103 | €2.41 | 35.9% |
| Keto Bottom | Tablet | 25 | €0.44 | 36.0% |
| Keto Top | Tablet | 24 | €0.38 | 20.8% |
| Keto Sidebar | Tablet | 9 | €0.69 | 85.7% |

By device — **desktop earns 4.2× mobile per impression**, and viewability is the whole
difference:

| Device | Impr | Share | Earnings | Impr RPM | Viewable |
|---|---|---|---|---|---|
| Desktop | 392 | 29% | €1.11 (63%) | €2.83 | 56.4% |
| Mobile | 921 | **67%** | €0.63 (36%) | €0.68 | 19.3% |
| Tablet | 58 | 4% | €0.03 | €0.52 | 37.4% |

⚠️ **The anchor unit is not in that export.** Auto-ads formats don't break out as a named ad
unit, so the table understates total revenue. Include Auto ads when you re-pull.

## What shipped

1. **All units lazy-load.** Slots are empty `data-ad-lazy="<slot>"` containers; the `<ins>`
   is created and pushed by an `IntersectionObserver` at 600px of lead time. Loader is at the
   bottom of `index.html` (search "Lazy ad loader") and in `dev/guides/template.html`.
2. **A 0%-viewability leak is closed.** The sidebar pushed at every width even though
   `#sidebar` is `display:none` under 830px — AdSense fills a *fixed-size* unit regardless of
   container visibility, so 214 mobile impressions/week were served where nobody could see
   them. A `display:none` element never intersects, so it isn't requested there; a landscape
   phone above 830px, where the sidebar really is visible, still gets its ad.

Removing the hidden sidebar alone moves blended viewability 30.7% → ~36.4%. Lazy loading
should take it well past that.

## What to pull, and when

From **2026-08-15** (two full weeks). AdSense report, **2026-08-01 onward**, dimensions
**ad unit × platform**, metrics: impressions, Active View viewable, impression RPM, estimated
earnings, page RPM. **Include Auto ads.**

Impressions will be **down substantially** — that is the mechanism working, not a regression.
Judge on viewability and impression RPM first, then total earnings.

## Decision tree

**Primary metric: mobile Keto Top.** Baseline 18.2% viewable / €0.81 impression RPM.

- **Viewable >50% and impression RPM >~€1.50** → it worked. Next lever: sidebar
  **160×600 → 300×600**. It is the best slot on the site (70% viewable, €2.62 RPM) stuck in
  the lowest-demand size. Needs `#sidebar` widened ~140px; see `.sidebar-ad` in `index.html`
  and the slot's `data-ad-size="160x600"`.
- **Viewable up but RPM flat** → the placement is wrong, not the timing. Move the unit rather
  than resizing the sidebar. Keto Top sits at the forecast/FAQ boundary.
- **Viewable barely moved** → check the loader is firing: the live page should show empty
  `data-ad-lazy` containers, with an `<ins>` appearing only after scrolling. Consider
  tightening `rootMargin` from `600px` — more lead time means more ads loaded for people who
  never quite reach them.
- **Earnings down and staying down after two full weeks** → `git revert e43a985` is one
  commit, but re-read the viewability numbers before concluding that.

## Open items

- **Sidebar 300×600** — deliberately deferred so it doesn't confound this measurement.
- **Engagement rate is 17%** (`analytics-summary.md`): ~83% of sessions leave inside 30s and
  never scroll to any in-content ad. That is a revenue lever, not just a UX one — nothing
  below the fold can earn until more people actually use the tool.
- **Anchor ads ON; in-page and vignette OFF** in the dashboard. Keep vignettes off — that
  density is what made the page feel unusable.
- Worth confirming: at ~1,150 pageviews/week the anchor alone may out-earn all three manual
  units combined. That rests on stale pageview data from `analytics-summary.md`.
- `revenue-plan-2026-07.md` T1.3 proposes a bottom multiplex unit and states "three fixed
  placements + anchor is the ceiling. Never more."

## Don't break this

`adsbygoogle.push({})` binds to the next **uninitialised `<ins>` in document order** — you
cannot name the element you mean. On scroll, order is whatever the reader does, so a static
`<ins>` sitting in the markup alongside the lazy ones would drop one slot's creative into
another slot's box (a 160×600 skyscraper in a full-width in-content space). The loader creates
the element and pushes in the same breath, which is what keeps them matched. `dev/test/` pins
this, including the desktop case where the sidebar pushes first.

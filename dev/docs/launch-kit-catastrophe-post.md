# Launch kit — "The Web Catastrophe That Kept Refusing to Happen"

The post: `dev/docs/blog-post-catastrophe.md`, to be published on martin.ankerl.com.
This kit replaces the old blank-page-post kit entirely (that post is being
unpublished; its two predecessors' claims died under measurement — which is now the
essay's plot). Goal unchanged: editorially-given backlinks → domain authority →
calculator ranking (revenue plan T2.2).

## 0. Pre-publish checklist (owner, before anything else)

- [ ] **GA4 Admin sanity check:** confirm the GA4 property was auto-created from
  UA-36863101-1 (property details show its origin). If you created it manually in
  2023, soften one clause in "Disaster #2" ("Google's automatic UA→GA4 migration
  had created a GA4 property" → "a GA4 property I'd forgotten setting up").
- [ ] **Unpublish** `/2026/07/03/website-blank-for-4-seconds/`; prefer a 301 to the
  new post over a 404 (Jekyll: `jekyll-redirect-from`, add `redirect_from:` to the
  new post's front matter).
- [ ] Keep **https://keto-calculator.ankerl.com/old.html live** — the essay links it
  as the try-it-yourself exhibit. Optional: `Disallow: /old.html` in robots.txt.
- [ ] Publish under a slug matching the new title.
- [ ] Optional but strong: a simple line/bar chart for the 239k→25k table (the
  essay works without it, but charts get screenshotted and reshared).

## 1. Hacker News (the main event)

- **Submit it yourself**, plain submission (not Show HN).
- **Title:** use the post title verbatim —
  `The web catastrophe that kept refusing to happen`.
  Backups if mods/HN dupes force a change:
  1. `I tried three times to prove my site was broken. I lost, with data.`
  2. `Google quietly keeps defusing dead Optimize anti-flicker snippets`
- **Timing:** Tuesday–Thursday, 14:00–16:00 CEST (8–10 am US Eastern).
- **If it stalls in /new:** one resubmission a few days later is allowed; a
  one-line email to hn@ycombinator.com about the second-chance pool is legitimate
  for first-party stories.

### Day-of comment duty — prepared answers (all verified this session)

- **"How does an analytics.js UA tag feed GA4?"** — honest answer is in the post:
  unknown mechanism, empirically continuous data; the auto-created property is
  confirmed. Invite readers who know the internals to explain — engagement gold.
- **"Is the anti-flicker shim documented anywhere?"** — not that we found; the
  evidence is empirical: FCP is blind under `opacity:0` (measured: fires only at
  the reveal), pre-fix lab FCP 3.3 s < the 4.0 s timeout, live old.html reveals
  fast, and tr.puma.com reveals at 824 ms clean. Anyone can reproduce with the
  linked harness.
- **"Did you tell Puma / site #2?"** — answer honestly (do consider dropping them
  a note *before* launch; then the answer is "yes, reported").
- **"2-in-50 is a tiny sample."** — agreed, that's why the essay says "on the
  order of a thousand" with the extrapolation shown; the full-body BigQuery scan
  is a ~$1 billed query if anyone wants the exact count (invite them to run it —
  the query is in the repo).
- **"iOS ignoring user-scalable=no is bad, actually"** — accessibility folks may
  push back that Apple was right/wrong; the essay already sides with Apple.
- **"Lighthouse FCP 3.3s ≠ real users"** — correct; field CrUX (LCP 2.1 s, green)
  is cited for the real-world picture.
- **"What monitoring would have caught this?"** — synthetic check asserting FCP or
  a screenshot, run WITH a strict-privacy profile; an HTTP 200 check sees nothing.
- **"AI wrote this?"** — the post already discloses Claude did the digging and the
  headless-browser refutations; own it, it disarms the comment.

## 2. Webperf community (same week)

- **Mastodon** (#webperf) + Bluesky: lead with the shim discovery — "Google
  quietly defuses abandoned anti-flicker snippets; I measured it" — that's the
  novel fact for the Kadlec/Russell orbit, plus the FCP-blind-under-opacity:0
  measurement note.
- **Lobsters** (if invite available): tags `web`, `performance`, `javascript`.

## 3. Reddit (staggered, never same day as HN)

- **r/webdev** — the war-story-with-a-twist angle.
- **r/programming** — plain link post.
- **r/firefox** — narrower but real: "strict tracking protection users get
  4-second blanks from leftover Optimize snippets (measured; ~a thousand sites)".
  Frame as PSA, not doom.
- **Not r/keto**, not r/SEO (nothing for them in this version).

## 4. Newsletters (day 2–3; two-sentence pitch)

> Subject: Google quietly keeps defusing dead A/B-test snippets — I measured it
> Hi — I tried three times to prove my 14-year-old static site was a disaster
> (4s blank page, dead analytics, web-scale zombie snippets) and lost every time
> to measurement: Google shims, ad-blocker stubs, and a web that cleaned up 90%
> of a dead product in a year. Write-up with data: {URL}. Might fit {newsletter}.

Targets: **Frontend Focus** (best fit), **JavaScript Weekly**, **Web Tools
Weekly**, **TLDR**. Year-end: pitch a condensed version to the **Web Performance
Calendar** (calendar.perfplanet.com) — durable, high-authority backlink.

## 5. Cross-post with canonical (week 2)

dev.to and Hashnode, full text with `canonical_url` set to the original.

## What NOT to do

- No voting rings; no simultaneous multi-subreddit blast.
- Don't submit the calculator itself anywhere — the essay carries the links to it.
- Don't harden the soft claims in comments (the ~1,000 extrapolation, the unknown
  GA4 bridge mechanism) — the essay's credibility IS the story.

## Measurement (closes revenue-plan T2.2)

- ~2 weeks post-launch: Search Console → Links on both properties
  (martin.ankerl.com and keto-calculator.ankerl.com); GA4 referrals on the post;
  referral/direct bump on the calculator.
- Success bar: a handful of real linking domains = win (domain authority
  compounding, not the traffic spike).

## Appendix — the verified numbers behind every claim (for comment duty)

| Claim in post | Evidence |
|---|---|
| FCP blind under opacity:0 | synthetic test: FCP fired at 4,032 ms = the reveal |
| Hide ended before timeout on broken page | owner's June PSI: lab FCP 3.3 s (post-fix 2.1 s) |
| Google shim answers dead containers | old.html fast in clean browser; tr.puma.com clean 824 ms |
| uBlock stub defuses | uBlock source `google-analytics_analytics.js` (issue #3075); measured 27 ms |
| Block-without-stub = 4.0 s since 2017 | measured 3,978 ms; snippet in live page since commit 7ef699f (2017-07-01) |
| GA4 data continuous, no cliff | owner's dashboards; 12-month summary in dev/docs/analytics-summary.md |
| 239,357 → 25,009 | owner's HTTP Archive BigQuery run (queries in plan-anti-flicker-research.md) |
| 47/50 no snippet; Puma 4,312 ms blocked; site #2 ~5 s for all | dev/research/results-top50.jsonl |
| gatrack: 52 call sites, no definition | grep of `5b235ce:index.html` |
| jsapi forwarder (shim #3) | old page loads google.com/jsapi; charts worked through 2026 |
| RPM €8–9 → €1.60 consent collapse | owner's AdSense data; fix commits in repo history |

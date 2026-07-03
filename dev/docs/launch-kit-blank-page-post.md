# Launch kit — "My Website Was Blank for 4 Seconds on Every Visit"

Post is **published** (2026-07-03): https://martin.ankerl.com/2026/07/03/website-blank-for-4-seconds/
This file is the distribution playbook (revenue-plan **T2.2**, second half). A post with
"free visitors only" earns no links — the aggregator launch is the backlink engine, because
the HN/newsletter crowd contains exactly the people who cite and link.

## Priority 1 — Hacker News (do this first, everything else follows from it)

- **Submit it yourself** from your own account (authors submitting their own work is fine
  and normal on HN; this is a story post, so plain submission, not "Show HN").
- **Title:** keep it close to the post's own title — it is already HN-shaped
  (factual, specific, curiosity without clickbait):
  1. `My website was blank for 4 seconds on every visit – for three years` ← recommended
  2. `Dead third-party scripts left my site blank for 4 seconds – for three years`
  3. `Every script tag around my static HTML died, and I noticed 3 years later`
  Avoid mentioning revenue/AdSense in the title (draws policy flames instead of the
  webperf/archaeology crowd; the money angle lands better *inside* the post).
- **Timing:** Tuesday–Thursday, 14:00–16:00 CEST (8–10am US Eastern). Weekends and
  European-evening submissions die in /new.
- **Day-of playbook:** stay in the comments for the first 2–3 hours and answer
  everything — author engagement visibly drives HN ranking. Expect (and prepare short
  answers for): "why not just delete all the scripts", "how much did the blank page
  cost you", "static sites rot too, just slower", "what monitoring would have caught
  this" (answer: any synthetic check with a screenshot/First-Contentful-Paint assert;
  a plain HTTP 200 check sees nothing).
- **If it doesn't take off:** HN allows a small number of re-submissions of the same
  URL after a few days; also the mods run a second-chance pool — a polite one-line
  email to hn@ycombinator.com asking them to consider it is legitimate and often works
  for first-party stories.

## Priority 2 — the webperf community (same week)

- **Mastodon** (webperf crowd is very active there — the Tim Kadlec / Alex Russell
  orbit loves "third-party scripts rot" evidence): post the hook + link, hashtag
  #webperf. Bluesky same text.
- **Lobsters** (if you have/can get an invite): tags `web`, `performance`, `javascript`.
  Small but link-rich audience.
- **Reddit, staggered (not same day as HN, and never simultaneously):**
  - r/webdev — fits their war-story appetite; check the self-promo rule (Showoff
    Saturday if a mod objects).
  - r/programming — plain link post, authors tolerated.
  - r/SEO or r/juststart — different angle: "the revenue graph everyone blames on
    Google updates was partly my own dead scripts".
  - **Not r/keto** — this post is about the website, not keto; it would read as ad.

## Priority 3 — newsletters (one-line pitches, day 2–3)

They trawl HN anyway (another reason HN is priority 1), but a two-sentence email
raises the odds. Pitch template:

> Subject: story: my site was blank 4s on every visit, for 3 years
> Hi — I wrote up how every third-party script on my 2012 static site died one by
> one (Google Optimize's anti-flicker snippet being the worst: opacity:0 on <html>
> with a 4s timeout) and what it cost: {URL}. Might fit {newsletter}.

Targets: **Frontend Focus** (frontendfoc.us, Cooperpress — perf war stories are their
bread and butter), **JavaScript Weekly** (same publisher), **Web Tools Weekly**,
**TLDR** (tldr.tech, "quick links" section), **Smashing Magazine newsletter** (long
shot). Late-year option: pitch a condensed version to the **Web Performance Calendar**
(calendar.perfplanet.com) — that's a durable, high-authority backlink.

## Priority 4 — cross-post with canonical (week 2, after HN has seen the original)

- **dev.to**: paste the full post, set `canonical_url` to the original in the
  front-matter (dev.to supports it natively). High-DR do-follow profile + reaches a
  different audience without duplicate-content risk.
- **Hashnode**: same, also supports canonical.

## What NOT to do

- No voting rings / asking friends to upvote (HN detects and buries).
- No simultaneous multi-subreddit blast (Reddit spam filters + it looks bad).
- Don't submit the keto calculator itself to HN — the *story* is the HN artifact;
  the calculator collects the spillover links.

## How to measure (so T2.2 can be closed with data)

- **Links:** Search Console → Links report, on BOTH properties (martin.ankerl.com
  and keto-calculator.ankerl.com) ~2 weeks after launch.
- **Traffic:** GA4 referral sessions on the blog post + referral/direct bump on the
  calculator; HN itself shows the submission's points/comments.
- Success bar (from the plan): a handful of real linking domains is already a win —
  domain-authority compounding is the goal, not the traffic spike.

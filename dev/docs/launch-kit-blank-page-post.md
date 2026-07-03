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

## The "why didn't you notice for 3 years?" answer — VERIFIED 2026-07-03

This is the #1 question HN will ask, and the owner asked it himself ("I never saw
that delay"). The empirical answer (all measured against the real 2018–2026
`index.html`, commit `5b235ce`, headless Chromium):

| Scenario | Time to first visible paint |
|---|---|
| Optimize container answers (pre-Sept-2023, no blocker) | ~216 ms (reveal ends the hide) |
| Optimize dead / GA blocked with no stub (post-Sept-2023 reality) | **~3,978 ms — the 4s timeout** |
| uBlock Origin serving its neutering stub | **~27 ms** |

Mechanism: the page's first inline script added `async-hide` (`opacity:0 !important`
on `<html>`) with a `setTimeout(4000)` fallback; the early reveal was
`dataLayer.hide.end()`, called only by the Google Optimize container
(`ga('require','GTM-TC6WLFB')`). Optimize sunset 2023-09-30 → nothing calls it →
every visitor waits out the full 4,000 ms.

**Why the owner never saw it:** uBlock Origin does not merely block `analytics.js` —
it *redirects* it to a local stub that immediately runs
`dl.hide.end()` precisely to defuse anti-flicker snippets
(https://github.com/gorhill/uBlock/blob/master/src/web_accessible_resources/google-analytics_analytics.js,
added for gorhill/uBlock#3075; the GTM stub does the same). So a browser with uBlock
was structurally incapable of reproducing the bug: **the ad blocker was shielding the
site owner from his own broken ad-tech, while every ad-viewing visitor ate the 4s.**

Bonus nuance (accurate, usable in comments): blockers that *block without a redirect
stub* (Safari content blockers, Firefox ETP strict) never call `hide.end()` either —
those users got the 4s blank **even before the 2023 sunset**, all the way back to 2017
when the snippet shipped.

**Self-verification for the owner (30 seconds):** `git show 5b235ce:index.html > /tmp/old.html`,
open it in a clean profile / incognito **with extensions off** — watch 4 s of white.
Open it in the normal uBlock profile — instant. (Only remaining unknown from the
sandboxed analysis container: whether Google's live endpoint served a hide-ending stub
at any point post-sunset; the clean-profile test answers that too.)

**Suggested update paragraph for the published post** (turns the objection into the
best part of the story):

> **Update:** several people (including me) wondered why I never noticed 4 seconds of
> white. The answer is embarrassing in a different way: uBlock Origin doesn't just
> block `analytics.js`, it replaces it with a stub that immediately calls
> `dataLayer.hide.end()` — specifically to defuse anti-flicker snippets like mine. I
> measured the old page: ~27 ms to first paint with uBlock's stub, ~3,978 ms without
> it. My ad blocker had been quietly protecting me from my own dead ad-tech for years
> — while every visitor generous enough to *not* run one got the full 4-second stare.

### Addendum (2026-07-03): the AdGuard DNS twist

Owner also runs **AdGuard DNS** at home. Important asymmetry, verified in source:

- **DNS-level blocking cannot defuse the snippet** — it just makes the
  `analytics.js` request fail. No code injection, no `hide.end()`, so the page
  waits the full 4 s. DNS blocking *causes* the blank, it never hides it.
- **In-browser blockers defuse it** — both uBlock Origin's and AdGuard's redirect
  stubs call `dataLayer.hide.end()` on load (AdGuard: `Scriptlets/src/redirects/
  google-analytics.js` line ~90; uBlock: `google-analytics_analytics.js`,
  gorhill/uBlock#3075). Extension redirects run inside the browser, before DNS is
  ever consulted — so with the extension on, AdGuard DNS never even sees the request.

Consequences worth using in the post/comments:

1. The owner never saw the blank because his **browser** blocker always served the
   stub. The home DNS layer was irrelevant on his own machines.
2. Any device on his home network **without** such an extension (stock mobile
   browser, guests, TV browser) hit the DNS-blocked path — i.e. the 4 s blank —
   **even before the 2023 sunset, all the way back to 2017.**
3. **Self-test correction:** at home, "incognito + extensions off" still shows the
   4 s blank regardless of what Google serves today, because AdGuard DNS kills GA
   anyway. To test Google's live endpoint behavior post-sunset, repeat on mobile
   data / any network without AdGuard DNS.

## ⚠️ CORRECTION 2026-07-03 — supersedes the two sections above

The owner put the exact old page back online (https://keto-calculator.ankerl.com/old.html)
and could NOT reproduce the 4s blank. Follow-up measurement found the flaw in the
earlier analysis:

- **FCP is blind under `opacity:0`** (measured: synthetic page, FCP fires only at the
  4,032 ms reveal). Therefore the June audit's **pre-fix lab FCP of 3.3 s** proves the
  hide was ending BEFORE the 4 s timeout in a clean environment — i.e. **Google's
  endpoint still serves a hide-ending response for dead Optimize containers**
  (`ga('require','GTM-TC6WLFB')` → analytics.js → gtm/js → `dataLayer.hide.end()`).
  Field CrUX during the broken window (LCP 2.1 s green) agrees.
- **Corrected reality table:**
  | Visitor setup | First paint |
  |---|---|
  | Clean browser, real network (Google's shim answers) | gated on the GA round-trip: lab 3.3 s throttled, usually faster in field — a tax, not a 4 s blank |
  | Blocked WITHOUT stub (Firefox strict ETP, Safari content blockers, AdGuard DNS / Pi-hole) | **full 4.0 s blank — since 2017** |
  | uBlock/AdGuard extension (stub calls hide.end) | ~27 ms, bug invisible |
- The post got a **Correction section** ("It Wasn't 4 Seconds for Everyone") replacing
  the earlier suggested update — the "suggested update paragraph" above must NOT be
  used. **Do not submit to HN until the correction is live on the blog.**
- HN framing changes in our favor: "I published a plausible claim, my own repro
  failed, here's the forensic truth (Google quietly defuses abandoned anti-flicker
  snippets; the 4 s hit only the privacy-tools crowd, since 2017)" is a stronger,
  more commentable story than the original — and it pre-empts the debunking comment
  that would otherwise have topped the thread.
- Residual unknown (honest footnote if asked): endpoint behavior between Oct 2023 and
  June 2026 can't be probed retroactively; the June 2026 lab FCP is the earliest
  direct evidence of the shim, and no evidence suggests it ever went dark.

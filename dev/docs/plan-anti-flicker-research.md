# Plan v2 — the zombie anti-flicker scan (supersedes the HN launch of the personal post)

Owner's verdict on the rewritten personal post: not HN-worthy — and he's right. The
correction drained the disaster ("Google's shims meant nothing much happened to MY
site"). But the findings generalize into a story that IS newsworthy:

> **Google Optimize died in September 2023. Its anti-flicker snippet is still
> installed on thousands of sites — and it serves a 4-second blank page to every
> visitor whose privacy setup blocks Google without injecting a stub (Firefox
> strict ETP, Safari content blockers, Pi-hole / AdGuard DNS households). Today.
> Invisibly — because those same visitors are the ones analytics can't see.**

One site is an anecdote. Ten thousand sites is news. The keto calculator becomes
patient zero and the personal post becomes the supporting link, not the headline.

## Tier 0 — publish the personal post quietly (owner, 10 min)

`dev/docs/blog-post-my-ad-blocker.md` is finished and true. Publish it on the blog
(new slug, retire the old 4-seconds URL), no HN submission. It's the "how I found
this" link the research post will cite, and it starts collecting long-tail readers.

## Tier 1 — quantify (owner runs, ~10 min in BigQuery console; free tier)

HTTP Archive's public BigQuery dataset. Two queries, run at
https://console.cloud.google.com/bigquery (any Google account; check the
**estimated bytes** shown top-right before running — stay under the 1 TB/month
free tier; add/lower TABLESAMPLE if needed). Schema drifts over the years —
if a column errors, check the table's schema tab; the intent is what matters.

**Q1 — cheap lower bound + trend: sites Wappalyzer still tags as Google Optimize**
(NOTE: undercounts — it misses snippet-only pages like ours was; that's what Q2 fixes)

```sql
SELECT date, COUNT(DISTINCT page) AS sites_with_optimize
FROM `httparchive.crawl.pages`,
UNNEST(technologies) AS t
WHERE date IN ('2023-06-01','2023-10-01','2024-06-01','2025-06-01','2026-06-01')
  AND client = 'mobile'
  AND is_root_page
  AND t.technology = 'Google Optimize'
GROUP BY date ORDER BY date;
```

The trend is a story on its own: the web's cleanup half-life after a product dies.

**Q2 — the real number: sampled body scan for the snippet itself**

```sql
-- response bodies live in crawl.requests (response_body column), not a separate table
SELECT COUNT(DISTINCT page) AS pages_with_antiflicker_in_sample
FROM `httparchive.crawl.requests` TABLESAMPLE SYSTEM (1 PERCENT)
WHERE date = '2026-06-01'
  AND client = 'mobile'
  AND is_root_page
  AND is_main_document
  AND REGEXP_CONTAINS(response_body, r'async-hide\s*\{\s*opacity\s*:\s*0');
```

Multiply by ~100 for the estimate; report as "on the order of". The requests table
is far bigger than pages — check the dry-run estimate first; if too costly, drop to
0.1 PERCENT and multiply by ~1000. For Tier 2, rerun with `SELECT page ... LIMIT 30`
to grab sample URLs. The regex catches both pretty and minified snippet forms.

**Decision gate:** if the extrapolated number is embarrassingly small (< ~1,000
root pages), the research post thesis dies — fall back to publishing Tier 0 only,
and pitch the two-shims essay to newsletters instead of HN.

## Tier 2 — verify in the wild (Claude, needs a networked session; ~1 evening)

`dev/research/measure-reveal.js` (committed next to this plan) loads any URL three
ways — clean, GA-blocked-no-stub (simulates Firefox strict / DNS blocking), and
uBlock-stub — and reports time-to-reveal, using the same Playwright harness that
produced the 27 ms / 3,978 ms numbers for our own page. Run it against 20–50
sample URLs from Q2. The killer stat for the post: "N of M sampled sites go blank
for 4 seconds under strict privacy settings, today." Screenshot one recognizable
offender (or anonymize: "a Fortune-500 retailer").

## Tier 3 — the research post (Claude drafts, owner's voice; on martin.ankerl.com)

Structure: the claim + number up top → 90-second mechanism explainer (the snippet,
who reveals it, the blocker asymmetry table) → the trend chart → how this was found
(patient-zero link to the personal post; the two Google shims) → "check your site"
(view-source search for `async-hide`; a one-line `curl -s URL | grep async-hide`)
→ the fix (delete the snippet; it has had no purpose since 2023) → the reflection
(fail-open third parties + the victims being invisible in analytics).

Title candidates:
1. `Google Optimize died in 2023. Its snippet is still blanking websites today.`
2. `Thousands of sites serve a 4-second blank page to privacy-conscious users`
3. `The web's zombie anti-flicker snippets`

## Tier 4 — launch (owner; mechanics from the old kit still apply)

- HN Tue–Thu, 14:00–16:00 CEST, comment duty. This version has what the personal
  post lacked: a number, a live check anyone can run on their own site in 10
  seconds, and villains/victims that aren't us.
- Now genuinely on-topic subreddits: r/firefox and r/pihole (their users ARE the
  victims), r/webdev, r/programming — staggered.
- Newsletters (Frontend Focus, JavaScript Weekly, Web Tools Weekly) — this is
  their core genre; Performance Calendar pitch at year-end.
- uBlock/AdGuard communities may enjoy the "your blocker secretly fixes this"
  angle — one Mastodon post tagging #webperf covers it.

## Why this serves the actual goal (ranking)

Same authority math as before, better odds: links earned by the research post lift
ankerl.com's domain; the calculator inherits. And the "check your site" hook is the
kind of thing that gets cited by documentation, newsletters, and how-to posts for
years — durable links, not just a traffic spike.

## RESULTS — Tier 1 run by owner, 2026-07-03

**Q1 (Wappalyzer "Google Optimize" on root pages, mobile crawl):**

| crawl date | sites |
|---|---|
| 2023-06-01 (pre-sunset) | 239,357 |
| 2023-10-01 (just after sunset) | 182,022 |
| 2024-06-01 | 45,281 |
| 2025-06-01 | 32,639 |
| 2026-06-01 | **25,009** |

**✅ Decision gate: PASSED.** A quarter-million sites ran Optimize; 25k of the web's
most-visited sites (HTTP Archive crawls CrUX origins — sites with real Chrome
traffic) still carry it ~3 years after the product died. The decay curve is a
finding in itself: ~90% cleanup within a year of sunset, then a plateau
(45k → 33k → 25k) — the abandoned long tail that will apparently never clean up.

Detection semantics (verified in HTTPArchive/wappalyzer `g.json`): flags
`googleoptimize.com/optimize.js` script tags OR the runtime `window.google_optimize`
global. So 25k = pages where Optimize machinery still *executes* in an unblocked
browser. It's a lower bound for "Optimize leftovers" and an upper-ish population for
the anti-flicker subset — Tier 2 sampling determines what fraction of these still
carry the `async-hide` snippet and actually blank under strict blocking.

**Q2 (body scan): SKIPPED — free-tier quota.** Not needed: the sample for Tier 2
comes from the cheap pages table instead, ranked so the most popular offenders
surface first:

```sql
SELECT page, rank
FROM `httparchive.crawl.pages`, UNNEST(technologies) AS t
WHERE date = '2026-06-01' AND client = 'mobile' AND is_root_page
  AND t.technology = 'Google Optimize'
ORDER BY rank
LIMIT 50;
```

(If this month's free quota is fully burned, it resets monthly; or a billed run of
the 0.1% Q2 body scan costs well under $1 if we ever want the snippet-only count too.)

**Tier 2 next:** run `dev/research/measure-reveal.js` over those 50 URLs from a
machine with normal network access (the analysis container can't reach arbitrary
sites): `node dev/research/measure-reveal.js $(cat urls.txt)` after `npm i playwright`.
Output per site: clean / blocked / stubbed reveal times + whether the snippet exists.
The post's headline stat comes from this: "N of the 50 most-popular Optimize
leftovers still blank for 4 seconds under Firefox strict / Pi-hole."

## RESULTS — Tier 2 run by owner, 2026-07-03 (dev/research/results-top50.jsonl)

Of the 50 most popular sites still flagged as running Google Optimize:
- **47 have NO anti-flicker snippet** on their homepage (leftover optimize.js/global
  only — harmless machinery, no hiding).
- **1 errored** (nrl.com — client-side navigation destroys the eval context).
- **2 still carry the snippet:**
  - `tr.puma.com` — clean **824 ms** (Google's shim confirmed working in the wild,
    independent of our page!), blocked **4,312 ms** → real 4s blank for
    Firefox-strict/Pi-hole users on a Puma storefront, today.
  - `m.guzzle.co.za` — clean **5,495 ms**(!): broken for *everyone*, apparently a
    longer timeout config; blocked 4,776 ms.

**Extrapolation:** ~2/49 ≈ 4% of Optimize leftovers still carry the snippet →
25,009 × 4% ≈ **on the order of 1,000 affected sites** (wide error bars,
~300–3,400). NOT "thousands of major sites". Harness caveat: our "stubbed" mode
only stubs analytics.js, not gtm.js, so it understates real uBlock protection on
GTM-loaded sites (tr.puma.com's stubbed 4,298 ms would be fast under real uBlock).

**❌ Decision gate #2: the doom headline dies.** "The web serves blank pages to
privacy users" is true for ~a thousand long-tail-ish sites and two nameable brands
— an anecdote, not an epidemic.

**➡️ The honest pivot (recommended):** the accumulated, verified story is the
OPPOSITE of doom and much rarer in the genre: *the catastrophe kept refusing to
happen.* A dead A/B product wired to hide entire websites, a dead analytics
product, dead CDNs — and the blast radius was absorbed by (a) Google's unpaid
compatibility shims (anti-flicker defusal, UA→GA4 bridge — both found by
measurement), (b) ad blockers that actively defuse booby traps, (c) a web that
cleaned up 90% of Optimize within a year. The residue: ~a thousand sites and one
Puma storefront blanking for exactly the users nobody's analytics can see —
resilience and rot as the same mechanism, failure made invisible instead of loud.
All numbers already in hand: the personal two-shim story, the 27 ms / 4.0 s / shim
measurements, the 239k→25k decay curve, the 2-of-50 sample, tr.puma.com live.

## TIER 3 DONE — final essay written 2026-07-03: `dev/docs/blog-post-catastrophe.md`

**"The Web Catastrophe That Kept Refusing to Happen"** — the anti-doom essay built
strictly from verified numbers. Supersedes and absorbs `blog-post-my-ad-blocker.md`
(removed); the owner is also unpublishing the original 4-seconds post, so this is
the ONLY post. Fact-check during writing corrected claims inherited from the first
draft (they had described the frozen `app/` source tree, not the live page —
verified against `5b235ce`):

- The live page **never loaded jsDelivr's dead `/g/` endpoint** — dropped entirely.
- The live page **was responsive** (device-width viewport + 830px media queries);
  its real mobile sin was `user-scalable=no`, which iOS has ignored since iOS 10 —
  reframed as another platform safety net.
- `gatrack` call sites: exactly **52**, not "hundreds" — corrected.
- New verified addition: charts loaded via `google.com/jsapi` (deprecated ~2016),
  which Google turned into a forwarder to the modern loader — **shim #3**.

HN title = the post title. The Tier 4 launch section applies unchanged; the "how
did you find this" comment answer is the harness + old.html exhibit links already
inside the post.

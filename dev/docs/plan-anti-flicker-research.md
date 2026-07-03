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

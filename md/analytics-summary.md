# Analytics Summary (Jun 2025 – Jun 2026)

Source: GA4 screenshots, 12-month window.

## Traffic

| Channel | Sessions | Share | Engagement rate |
|---------|----------|-------|-----------------|
| Direct | 43,218 | 74.4% | 16.4% |
| Organic Search | 7,452 | 12.8% | 15.5% |
| Organic Social | 6,646 | 11.4% | 20.2% |
| Organic Video | 1,009 | 1.7% | 23.6% |
| Referral | 524 | 0.9% | 19.9% |
| **Total** | **58,130** | | **17.0%** |

~4,850 sessions/month average.

## Devices

| Category | Share |
|----------|-------|
| Mobile | 65.5% |
| Desktop | 33.1% |
| Tablet | 1.4% |

Top screen resolutions: 393×852, 390×844, 430×932 (all iPhone), then 1920×1080.  
Top OS: iOS (~21K users), then Windows, Android, Macintosh.  
Top browser: Safari (~22K), Chrome (~14K).

## Key events

3,176 key events out of 58,130 sessions = 5.5% key event rate.  
175,068 total events, 3.01 events/session.

---

## What this tells us

### 1. Organic Search is severely underperforming (12.8%)
A healthy content/tool site gets 50–70%+ from organic search. Only 7,452 organic sessions in a year is low — this is where the revenue loss came from. SEO work has large upside.

### 2. The 74% Direct is loyalty, not health
That many direct sessions means users bookmark the site and return to recalculate. Strong signal the tool is genuinely useful. But it also means new-user acquisition via Google is broken.

### 3. Organic Social at 11% is unexpectedly strong
6,646 sessions from social with no active posting means Reddit (r/keto links), Pinterest pins, and shared URLs are still working. The shareable URL feature (already built) has real value.

### 4. Mobile is the primary platform — and the site WAS broken on mobile (fixed 2026-06-28)
65.5% mobile, top 3 resolutions are all iPhone (393×852 = iPhone 14 Pro, 390×844 = iPhone 12/13/14, 430×932 = iPhone 14 Plus). At the time of this analysis the fixed ~870px layout with `user-scalable=no` was a bad experience for the majority of users.

> **Resolved 2026-06-28:** the viewport is now `width=device-width, initial-scale=1` (no `user-scalable=no`) and a responsive `@media (max-width:830px)` block makes the layout mobile-first (16px inputs, 22px radio tap targets). This priority is **done** — re-measure mobile engagement at the 3-month review (≈ 2026-09-29) to quantify the gain.

### 5. Engagement rate is low (17%)
Only 1 in 6 sessions is "engaged" (30+ seconds). For a calculator that takes time to fill in, this suggests many users hit the page and leave before interacting.

> **Likely cause found (2026-06-28):** the page shipped a Google Optimize anti-flicker
> snippet that set the whole `<html>` to `opacity:0` and only revealed it on an Optimize
> callback. Optimize was sunset 2023-09-30, so that callback never fired — the page fell
> through to its 4000ms safety timeout, i.e. **a blank page for up to 4 seconds on every
> visit.** That alone plausibly explains much of the low engagement. Removed; re-measure
> engagement at the 3-month review. (Note: re-measuring requires re-adding analytics — the
> old UA tag was dead, see `md/plan.md`.)

### 6. Revenue math
~4,850 sessions/month × €60/month = ~€12.40 per 1,000 sessions. Health content can get €15–30 RPM in the US/EU. If the engagement rate and mobile experience improve, RPM should rise without needing more traffic.

### 7. Organic Video at 1.7% is a free bonus
1,009 sessions from YouTube/TikTok with no video effort — these are third-party keto videos linking to the calculator. Worth preserving the URL structure so these links keep working.

---

## Priority implications for the plan

1. ~~**Mobile layout fix is now the #1 priority** — 65.5% of users are on a broken layout.~~
   **DONE 2026-06-28** (responsive layout + viewport fix). Re-measure the engagement gain at the review.
2. **SEO / Core Web Vitals** — organic search at 12.8% has enormous room to grow.
3. **Engagement rate improvement** — fixing mobile UX and page speed directly increases ad impressions per user.
4. **Still need Search Console data** — to know which queries bring organic traffic and which to target.

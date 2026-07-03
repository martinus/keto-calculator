---
layout: post
title: My Website Was Blank for 4 Seconds on Every Visit
subtitle: For three years, and I didn't notice a thing
---

<!--
  DRAFT for martin.ankerl.com — before publishing:
  * sanity-check the numbers against my own records: the €8–9 → €1.6 RPM drop
    (2026-07-01 commit message), 17% engagement / 65% mobile / ~4,850 sessions/mo
    (dev/docs/analytics-summary.md)
  * maybe add a cover-img
-->

Back in 2012 I made a [keto calculator](https://keto-calculator.ankerl.com/)
because I wanted exact macro numbers for my own diet, and all the advice online
was too vague. I [posted it on /r/keto](https://www.reddit.com/r/keto/comments/127sm0/keto_calculator/),
people liked it, Google ranked it well, and for years it quietly earned quite a
bit of ad money while I worked on other things. It's a single static HTML page.
No backend, no build step, no database. A site like that should basically run
forever.

This June I had a close look at the page for the first time in years. It turns
out that every single visitor got to stare at a blank white screen for 4
seconds before the page appeared.

It had been doing that since September 2023.

# The Slow Decline

I thought I knew why the revenue kept going down: from "quite a bit" at the
peak to about €60 a month now. The keto hype peaked around 2019, Google's
updates buried small single-page tools, and nowadays AI answer boxes intercept
most informational searches. All of that is true.

But the site was also busy sabotaging itself, and had been for years. The HTML
was perfectly fine — it was all the third-party `<script>` tags around it that
had died, one after another, without me noticing anything.

# What Was Actually Broken

Quite a lot. Here is everything I found:

## 1. The blank page

Years ago I ran A/B tests with Google Optimize. Optimize ships with an
"anti-flicker" snippet so visitors don't see the original page before the
experiment variant swaps in:

```html
<style>.async-hide { opacity: 0 !important}</style>
<script>(function(a,s,y,n,c,h,i,d,e){s.className+=' '+y;h.start=1*new Date;
h.end=i=function(){s.className=s.className.replace(RegExp(' ?'+y),'')};
(a[n]=a[n]||[]).hide=h;setTimeout(function(){i();h.end=null},c);h.timeout=c;
})(window,document.documentElement,'async-hide','dataLayer',4000,
{'GTM-XXXXXXX':true});</script>
```

Read it carefully: it sets the whole `<html>` element to `opacity: 0` and waits
for the Optimize container to load and call the reveal function. If that never
happens, a safety timeout shows the page after 4000 milliseconds.

Google shut down Optimize on September 30, 2023. The container script was gone,
so the reveal callback never fired again. From that day on **every visitor saw
a blank page for the full 4 seconds**, then the timeout kicked in and the page
faded up as if nothing had happened.

My engagement rate over the last 12 months was 17%. Only one visitor in six
stuck around. I always read that as "keto is over". A good part of it was five
lines of JavaScript waiting for a callback from a product that no longer
exists.

The nasty part is that nothing actually failed. Nothing threw, nothing was
logged, and the page worked perfectly — eventually. If the snippet had thrown
an error the page would have stayed visible and I'd have lost nothing. Because
it "worked", I lost three years of first impressions.

## 2. The analytics was dead too

Why didn't I see this in analytics? Because the analytics died first. The page
still had a Universal Analytics tag, and Google stopped processing UA hits on
July 1, 2023 — two months *before* Optimize died. The one instrument that could
have shown me the cliff went dark right before the cliff.

## 3. A JavaScript error on every click

Hundreds of links on the page had `onclick="return gatrack(this);"` for click
tracking. At some point the *definition* of `gatrack` got commented out — but
all the call sites stayed. So every tracked click threw an uncaught
`ReferenceError`, for years. Browsers shrug that off and the links still
navigate, so no user ever noticed. Neither did I.

## 4. Requests to a service that no longer exists

The page still loaded Bootstrap and jQuery through jsDelivr's `/g/` combine
endpoint, an API that was retired years ago. Two script requests on every page
load, going to a dead URL.

## 5. Mobile users couldn't zoom

The viewport meta tag said `user-scalable=no`, on a fixed ~870 pixel layout.
About 65% of my visitors are on phones — the top three screen sizes in my
analytics are all iPhones — and they got a desktop page they couldn't even
pinch-zoom.

None of these things broke the site. That's exactly the problem. A static page
doesn't rot, but its `<script>` tags do — and they rot silently, because every
one of them is designed to degrade gracefully instead of failing loudly.

# Then I Immediately Made a Fresh Mistake

While modernizing the page this June I added Google Consent Mode, the GDPR
mechanism that tells Google's tags what a visitor has consented to. I set the
defaults exactly like every tutorial shows:

```js
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  ...
});
```

Deny everything, let the cookie banner grant later. Sounds safe, right?

Within days my page RPM collapsed from about €8–9 to €1.60. The problem: that
default applies **globally**. An American visitor never gets a consent banner,
so there is nothing for them to click "accept" on — they are stuck with
non-personalized ads forever. I had quietly opted my entire non-EU majority out
of personalized ads. The fix is a region-scoped default: granted worldwide,
denied only where the law actually requires prior consent.

I only caught this because, for the first time in years, I was actually looking
at the dashboards. Which is really the whole lesson of this post in one week:
the old mistakes survived for three years because nobody was looking, the new
mistake survived for three days because someone was.

# The Site Now

It's still a single static HTML file, and after the cleanup it's faster than it
ever was: all Core Web Vitals green, total blocking time in lab tests down from
490ms to zero, and the calculator JavaScript no longer render-blocking. The
dead scripts are gone, analytics works again, consent is region-scoped, and
there is now a [German version](https://keto-calculator.ankerl.com/de/) and an
[embeddable version](https://keto-calculator.ankerl.com/embed.html) if you run
a site in this space and want the calculator without the page around it. I did
the digging and the rebuild together with an AI coding agent (Claude), which
turned out to be very good at reading through 12 years of accumulated HTML
without complaining.

# What I Learned

1. **A static site is not zero maintenance.** My HTML from 2012 renders fine.
   But every third-party `<script>` I ever added is a subscription to someone
   else's product decisions, and three of those products were discontinued
   under me.
2. **Third-party scripts fail open.** The anti-flicker snippet is the worst
   case: its failure mode was *hiding my entire site*, silently, with a timeout
   that made it look like slowness instead of breakage. Check what happens to
   your page when each external script never answers.
3. **Dead instruments are worse than no instruments.** A missing analytics tag
   is a known unknown. A dead one is a dashboard you trust and never read.
4. **Look at it once a year.** None of this needed weekly maintenance. One
   afternoon per year — open the page with DevTools, look at the console, look
   at the network tab, look at the money — would have caught every single item
   on the list above.

Is a €60-a-month website worth all this effort? If I price my hours honestly,
probably not. But it was never really about the €60. It's the oldest thing I've
built that strangers still use every day, and it deserves better than spending
three years hidden behind an `opacity: 0`, waiting for a callback that will
never come.

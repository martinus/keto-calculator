---
layout: post
title: My Website Was Blank for 4 Seconds on Every Visit
subtitle: For three years, and I didn't notice a thing
---

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
faded up as if nothing had happened. *(That's what I published, anyway. It's
wrong in an interesting way — see the [correction](#correction-it-wasnt-4-seconds-for-everyone)
at the end. The short version: it was 4.0 seconds for the privacy-tools crowd
— since 2017, not 2023 — a smaller round-trip tax for everyone else, and
nothing at all for ad-blocker users like me.)*

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

# Correction: It Wasn't 4 Seconds for Everyone

**The central claim above is wrong, and I found out in the best possible way: a
reader couldn't reproduce it. The reader was me.**

After publishing this I put the exact old page back online and opened it — no
blank. So instead of reasoning from the snippet's source code, I measured.

The first thing I learned is that Chrome's First Contentful Paint metric
doesn't fire while content sits at `opacity: 0` — FCP only registers when the
anti-flicker hide ends. Which means my own June Lighthouse runs of the
still-broken page had contained the answer all along: **lab FCP was 3.3
seconds. Less than 4.** The hide was ending *before* the safety timeout.
Something was still calling the reveal function.

That something is Google. The `ga('require','GTM-TC6WLFB')` line makes
analytics.js fetch the Optimize container from Google's servers — and that
endpoint, years after the product was shut down, still returns a response that
calls `dataLayer.hide.end()`. **Google has quietly kept defusing everyone's
leftover anti-flicker snippets.** The product died; a compatibility shim for
its most dangerous side effect did not.

So here is what visitors actually experienced, measured on the real 2017–2026
page:

* **Normal browser, nothing blocked:** first paint waited for a round trip to
  Google — analytics.js, then the container. 3.3 seconds on Lighthouse's
  throttled mobile connection; field data (LCP 2.1 s, green) says it was
  usually quicker in the real world. A silent tax on every first impression —
  but not a fixed 4-second blank, and not new in 2023.
* **Blocking without code injection** — Firefox's strict tracking protection,
  Safari content blockers, DNS-level blocking like AdGuard DNS or a Pi-hole:
  nothing ever calls the reveal, and the page sits blank for the full **4.0
  seconds** (measured: 3,978 ms). Not since 2023 — **since 2017**, when I added
  the snippet.
* **uBlock Origin and friends:** their [replacement stub](https://github.com/gorhill/uBlock/blob/master/src/web_accessible_resources/google-analytics_analytics.js)
  calls `dataLayer.hide.end()` immediately, precisely to defuse snippets like
  mine ([gorhill/uBlock#3075](https://github.com/gorhill/uBlock/issues/3075);
  [AdGuard's stub does the same](https://github.com/AdguardTeam/Scriptlets/blob/master/src/redirects/google-analytics.js)).
  Measured: **27 ms**. These visitors never saw anything wrong at all.

That last line finally explains why I never noticed: on my own machines, uBlock
was serving me the fastest version of my own site. And the people who *did* get
the true 4-second stare — the privacy-hardened, DNS-blocking crowd — are
exactly the people who are invisible in analytics dashboards, because the same
setup that blanked their page also blocked the tracking.

The corrected lessons, then:

1. The original sin stands: I made first paint hostage to a third party for
   nine years. But the third party turned out to be the responsible adult in
   the room — Google kept a shim running so that abandoned snippets like mine
   wouldn't blank abandoned sites like mine.
2. **I reasoned from source code when I should have measured.** "The container
   is gone, therefore the callback never fires" was obvious, plausible, and
   wrong — the callback had one more caller I didn't know about.
3. The failure wasn't uniform, it was a function of each visitor's privacy
   setup — and my setup was the one that hid every symptom. If you want to see
   your page the way your visitors do, test it the way you'd never browse
   yourself: clean profile, no extensions, default DNS — and then once more
   with the strict settings, because those visitors exist too.
4. And the 17% engagement rate? It has to find other explanations. I took the
   most satisfying candidate off the list by measuring. That stings, and it's
   the whole point of this correction.

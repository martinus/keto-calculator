---
layout: post
title: My Ad Blocker Was Protecting Me From My Own Website
subtitle: An autopsy of nine years of silent script rot on a static page
---

Back in 2012 I made a [keto calculator](https://keto-calculator.ankerl.com/)
because I wanted exact macro numbers for my own diet, and all the advice online
was too vague. I [posted it on /r/keto](https://www.reddit.com/r/keto/comments/127sm0/keto_calculator/),
people liked it, Google ranked it well, and for years it quietly earned quite a
bit of ad money while I worked on other things. It's a single static HTML page.
No backend, no build step, no database. A site like that should basically run
forever.

This June I had a close look at the page for the first time in years, and found
that essentially every third-party `<script>` tag on it was dead. Not erroring —
dead things error. These had all failed *politely*, each in its own way, some of
them for close to a decade. This post is the autopsy, including the part where
my first diagnosis was wrong and my own ad blocker turned out to be the reason
I couldn't see the body.

# Exhibit A: the snippet that hides your entire site

Years ago I ran A/B tests with Google Optimize. Optimize shipped with an
"anti-flicker" snippet, so visitors don't see the original page before the
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
for the Optimize container to call the reveal function. If that never happens,
a safety timeout shows the page — after 4000 milliseconds.

I added that snippet in 2017. Google shut down Optimize on September 30, 2023.
Dead product, gone container, nobody left to call the reveal function. So the
conclusion writes itself: since autumn 2023, every visitor stared at a blank
white page for four full seconds.

That was going to be the headline of this post. It's wrong, and how it's wrong
is the best part of the story.

# I couldn't reproduce my own bug

To get a screenshot of the disaster, I put the exact old page back online
([you can try it yourself](https://keto-calculator.ankerl.com/old.html)) and
opened it. No blank page. It just... appeared, like a working website.

Reasoning from the source code had felt airtight. Time to measure instead.

The first thing I learned is that Chrome's First Contentful Paint metric
doesn't fire while content sits at `opacity: 0` — FCP only registers when the
hide ends. And that meant my own Lighthouse runs of the still-broken page
already contained the answer: **lab FCP was 3.3 seconds. Less than 4.** The
hide was ending *before* the safety timeout. Something was still calling the
reveal function of a product that died in 2023.

That something is Google. The page's `ga('require','GTM-…')` line makes
analytics.js fetch the Optimize container from Google's servers — and that
endpoint, years after the product was shut down, still returns a response that
calls the reveal. **Google has quietly kept defusing everyone's abandoned
anti-flicker snippets.** The product is dead; a compatibility shim for its most
dangerous side effect lives on. (Whether the shim was there from day one after
the sunset I can't prove retroactively — but my mid-2026 lab numbers and the
live endpoint today agree.)

So who actually saw what? I measured the old page under each setup:

* **Normal browser, nothing blocked:** first paint waits for a round trip to
  Google — analytics.js, then the container, then the reveal. 3.3 seconds on
  Lighthouse's throttled mobile connection, usually faster on real ones. A
  silent tax on every first impression since 2017 — but not a 4-second blank.
* **Privacy tools that block without injecting code** — Firefox's strict
  tracking protection, Safari content blockers, DNS-level blocking like AdGuard
  DNS or a Pi-hole: the request fails, nothing ever calls the reveal, and the
  page sits blank for the full **4.0 seconds** (measured: 3,978 ms). Every
  visit. Since 2017.
* **uBlock Origin and friends:** here's the twist. uBlock doesn't just block
  `analytics.js` — it [replaces it with a local stub](https://github.com/gorhill/uBlock/blob/master/src/web_accessible_resources/google-analytics_analytics.js),
  and that stub's first order of business is calling the anti-flicker reveal,
  precisely to defuse snippets like mine
  ([gorhill/uBlock#3075](https://github.com/gorhill/uBlock/issues/3075);
  [AdGuard's stub does the same](https://github.com/AdguardTeam/Scriptlets/blob/master/src/redirects/google-analytics.js)).
  Measured: first paint in **27 milliseconds**.

I browse with uBlock Origin. My own machines were *structurally incapable* of
showing me the bug — my ad blocker had been serving me the fastest version of
my own site all along, quietly protecting me from my own dead ad-tech.

And the people who did get the full 4-second stare, the privacy-hardened
DNS-blocking crowd? Their setup also blocks analytics. The one population of
victims was exactly the population that's invisible in every dashboard I could
have looked at.

# The rest of the body count

The blank-page snippet was just the most dramatic corpse. The same page also
carried:

* **A dead analytics tag.** Universal Analytics stopped processing hits on
  July 1, 2023 — two months *before* Optimize died. The one instrument that
  could have shown me any of this went dark right before it mattered. A dead
  instrument is worse than no instrument: it's a dashboard you trust and never
  read.
* **A JavaScript error on every click.** Hundreds of links had
  `onclick="return gatrack(this);"` — and at some point the *definition* of
  `gatrack` got commented out while every call site stayed. Uncaught
  `ReferenceError`, on every tracked click, for years. Browsers shrug it off
  and navigate anyway, so nobody ever noticed. Including me.
* **Requests to a service that no longer exists.** Bootstrap and jQuery still
  loaded through jsDelivr's `/g/` combine endpoint, retired years ago. Two
  requests to a dead URL on every page load.
* **A mobile page you couldn't zoom.** `user-scalable=no` on a fixed ~870-pixel
  layout, while 65% of my visitors are on phones.

None of this broke the site. That's exactly the problem. Static HTML doesn't
rot, but its `<script>` tags do — and they rot silently, because every one of
them is designed to degrade gracefully instead of failing loudly.

# Then I immediately made a fresh mistake

While modernizing the page I added Google Consent Mode, the GDPR mechanism that
tells Google's tags what a visitor consented to. I set the defaults exactly
like every tutorial shows: deny everything, let the cookie banner grant later.
Sounds safe.

Within days my page RPM collapsed from about €8–9 to €1.60. That default
applies **globally** — an American visitor never gets a consent banner, so
there's nothing for them to accept; I had quietly opted my entire non-EU
majority out of personalized ads. The fix is a region-scoped default: granted
worldwide, denied where the law actually requires prior consent.

I only caught it because, for the first time in years, I was looking at the
dashboards. That's the whole post in one sentence: the old mistakes survived
for up to nine years because nobody was looking; the new one survived three
days because someone was.

# The site now

Still a single static HTML file, faster than it ever was: all Core Web Vitals
green, lab total blocking time down from 490 ms to zero, first paint no longer
hostage to anyone's servers. The dead scripts are gone, analytics works,
consent is region-scoped, and there's now a
[German version](https://keto-calculator.ankerl.com/de/) and an
[embeddable version](https://keto-calculator.ankerl.com/embed.html) if you run
a site in this space. I did the digging and the rebuild together with an AI
coding agent (Claude), which turned out to be very good at reading through 12
years of accumulated HTML without complaining — and, when I couldn't reproduce
the blank page, at proving me wrong with a headless browser.

# What I learned

1. **A static site is not zero maintenance.** My HTML from 2012 renders fine.
   But every third-party `<script>` I ever added is a subscription to someone
   else's product decisions, and three of those products were discontinued
   under me.
2. **Third-party scripts fail open, and they fail *unevenly*.** The same five
   lines were a 27 ms no-op for one visitor, a modest tax for another, and a
   4-second blank wall for a third — depending entirely on their privacy
   setup. There is no longer such a thing as "the" experience of your page.
3. **Measure; don't reason from source code.** "The container is gone,
   therefore the callback never fires" was obvious, plausible, and wrong — the
   callback had one caller left that I knew nothing about.
4. **Your own browsing setup lies to you.** If you want to see your page the
   way visitors do, test it the way you'd never browse yourself: clean
   profile, no extensions, default DNS. Then once more with strict privacy
   settings — those visitors exist too, and your analytics will never show
   them.
5. **Look at it once a year.** One afternoon — DevTools open, console tab,
   network tab, then the money — would have caught every single item above.

Is a €60-a-month website worth all this? If I price my hours honestly,
probably not. But it was never really about the €60. It's the oldest thing
I've built that strangers still use every day, and it deserves better than
serving its slowest version to its politest visitors for nine years while its
owner, wrapped safely in uBlock, saw nothing wrong at all.

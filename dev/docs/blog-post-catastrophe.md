---
layout: post
title: The Web Catastrophe That Kept Refusing to Happen
subtitle: I tried three times to prove my old site was a disaster. I lost every time, with data.
---

Back in 2012 I made a [keto calculator](https://keto-calculator.ankerl.com/)
because I wanted exact macro numbers for my own diet, and all the advice online
was too vague. I [posted it on /r/keto](https://www.reddit.com/r/keto/comments/127sm0/keto_calculator/),
people liked it, Google ranked it well, and for years it quietly earned ad money
while I worked on other things. It's a single static HTML page. No backend, no
build step, no database. A site like that should basically run forever.

This June I had a close look at it for the first time in years, and the `<head>`
read like a graveyard: an A/B-testing product Google discontinued in 2023, an
analytics product Google discontinued in 2023, a charts loader Google deprecated
around 2016, a click-tracking function that didn't exist anymore, and a snippet
whose *documented failure mode* is hiding the entire site.

What follows is the story of three disasters I confidently diagnosed in that
graveyard, and how measuring killed every one of them.

# The booby trap

The scariest find first. In 2017 I had added Google Optimize's "anti-flicker"
snippet, so A/B-test visitors wouldn't see the original page before their
variant swapped in:

```html
<style>.async-hide { opacity: 0 !important}</style>
<script>(function(a,s,y,n,c,h,i,d,e){s.className+=' '+y;h.start=1*new Date;
h.end=i=function(){s.className=s.className.replace(RegExp(' ?'+y),'')};
(a[n]=a[n]||[]).hide=h;setTimeout(function(){i();h.end=null},c);h.timeout=c;
})(window,document.documentElement,'async-hide','dataLayer',4000,
{'GTM-TC6WLFB':true});</script>
```

Read it carefully: it sets the whole `<html>` element to `opacity: 0` and waits
for the Optimize container to call the reveal function. If nothing ever calls
it, a safety timeout shows the page — after 4000 milliseconds.

Google shut Optimize down on September 30, 2023. Dead product, nobody left to
call the reveal. The conclusion writes itself: **every visitor since autumn 2023
stared at a blank white page for four full seconds.** My 12-month engagement
rate was 17% — only one visitor in six sticking around — and suddenly I knew
why. I had the headline of a blog post and a villain.

# Disaster #1 refuses to happen

To get a screenshot of the crime, I put the exact old page back online
([try it yourself](https://keto-calculator.ankerl.com/old.html)) and opened it.

No blank page. It just appeared, like a working website.

Reasoning from source code had felt airtight, so I started measuring instead.
First lesson: Chrome's First Contentful Paint doesn't fire while content sits at
`opacity: 0` — in a controlled test, FCP registered only at the reveal, right
after the 4-second timeout. Which meant my own PageSpeed runs of the
still-broken page had contained the answer all along: **lab FCP was 3.3
seconds. Less than four.** The hide was ending *before* the timeout. Something
was still calling the reveal function of a product that died in 2023.

That something is Google. The page requests the Optimize container via
`ga('require','GTM-TC6WLFB')`, and Google's endpoint — years after the product
was discontinued — still returns code that calls `dataLayer.hide.end()`, the
anti-flicker reveal. **Google quietly keeps defusing everyone's abandoned
anti-flicker snippets.** The product is dead; a compatibility shim for its most
dangerous side effect lives on.

So visitors on a normal browser never got a 4-second blank. They paid a subtler
price: first paint was gated on a round trip to Google — 3.3 seconds on a
throttled lab connection, less on fast ones — for no reason at all, for nine
years. A tax, not a catastrophe.

# Disaster #2 refuses to happen

Fine — but surely I was at least flying blind the whole time? The page carried a
Universal Analytics tag, and Google stopped processing UA hits on July 1, 2023,
two months *before* Optimize died. "The one instrument that could have warned me
went dark right before it mattered." I actually wrote that sentence.

Then I opened the dashboards. The data is all there: continuous through the UA
shutdown and out the other side, same visitor levels, a slow steady decline and
no cliff anywhere. Google's automatic UA→GA4 migration had created a GA4
property from my old one, and the numbers kept flowing without me changing a
single line of code. I still haven't found out exactly which compatibility
mechanism carries hits from a nine-year-old `analytics.js` tag into GA4 — and
that is rather the point. Shim number two, running unattended, for years.

As a bonus, that unbroken graph is field evidence for disaster #1's demise: if
every visitor had suddenly faced a 4-second blank in autumn 2023, the traffic
and engagement curves should show a step that week. They don't.

# So who actually got hurt?

Here's where it gets interesting. I measured the old page under different
blocking setups (headless Chromium; [harness in the repo](https://github.com/martinus/keto-calculator/tree/master/dev/research)):

| Visitor setup | First paint |
|---|---|
| Normal browser, Google reachable | gated on the Google round trip (fine on fast connections, 3.3 s in a throttled lab) |
| uBlock Origin / AdGuard extension | **~27 ms** |
| Blocking *without* code injection — Firefox strict tracking protection, Safari content blockers, Pi-hole / AdGuard DNS | **3,978 ms — the full timeout, on every visit, since 2017** |

The middle row is my favorite discovery in this whole story. uBlock doesn't
just block `analytics.js` — it [replaces it with a local stub](https://github.com/gorhill/uBlock/blob/master/src/web_accessible_resources/google-analytics_analytics.js),
and that stub's first order of business is calling `dataLayer.hide.end()`,
specifically to defuse anti-flicker snippets like mine
([gorhill/uBlock#3075](https://github.com/gorhill/uBlock/issues/3075);
[AdGuard ships the same defusal](https://github.com/AdguardTeam/Scriptlets/blob/master/src/redirects/google-analytics.js)).
I browse with uBlock. My own machines were structurally incapable of showing me
the problem: **my ad blocker was protecting me from my own website.**

The bottom row is the sad part. Blockers that can't inject code — DNS blocking,
Safari's declarative content blockers, Firefox's strict mode — kill the request
but can't call the reveal. Those visitors got the true four-second blank, and
not since 2023: since 2017, the day I added the snippet, because for them
nothing *ever* called the reveal function. And by construction, these are
exactly the visitors who don't appear in analytics — the same setup that
blanked their page also blocked the measurement of their existence.

# Disaster #3 refuses to happen

One last chance for a catastrophe: scale. If my page had this booby trap,
thousands of sites must still be hiding themselves from privacy-conscious users,
right? The [HTTP Archive](https://httparchive.org/) crawls the homepages of
millions of real-traffic sites every month and records what runs on them, so
this is answerable with a query:

| crawl | sites running Google Optimize |
|---|---|
| June 2023 (product alive) | 239,357 |
| October 2023 (just after shutdown) | 182,022 |
| June 2024 | 45,281 |
| June 2025 | 32,639 |
| June 2026 | **25,009** |

Four out of five sites cleaned up within a year of the shutdown; about 90% have
by now. Twenty-five thousand zombies sounds like a lot — until you test them. I
took the 50 most popular sites still flagged as running Optimize and measured
each one: **47 carry no anti-flicker snippet at all** (leftover loader scripts,
harmless), one wouldn't hold still long enough to measure, and exactly two
still hide themselves. One is a Puma storefront — fine on a normal browser (the
Google shim reveals it after 824 ms), but a genuine 4.3-second blank for
Firefox-strict and Pi-hole users, today. The other is broken for *everyone*,
about five seconds — someone configured a longer timeout.

Extrapolate 2-in-50 over the zombie population and you get on the order of a
thousand affected homepages on the entire measurable web. An anecdote wearing a
Puma tracksuit, not an epidemic. The web had already cleaned up after Google's
dead product better than I had cleaned up my own single page.

# The graveyard was full of safety nets

Once I knew what to look for, I found the same pattern everywhere on my page:

* The pie charts loaded through `google.com/jsapi`, a loader Google deprecated
  around 2016. It was silently turned into a forwarder to the modern charts
  loader — my charts kept rendering for a decade on a dead API. Shim number
  three.
* The viewport said `user-scalable=no`, disabling pinch-zoom on a page that's
  65% mobile traffic. iOS has simply ignored that directive since iOS 10 —
  Apple overruled me on behalf of my visitors, and they were right to.
* 52 links carried `onclick="return gatrack(this)"` — a function whose
  definition was deleted years ago. Every click on them throws an uncaught
  `ReferenceError`, and it doesn't matter: an onclick that throws can't return
  `false`, so the browser shrugs and navigates anyway. The only thing lost was
  the tracking, which was going to a dead product regardless.

Everything failed open. Nothing failed loudly. Layer after layer — Google's
shims, Apple's veto, ad-blocker stubs, the browser's tolerance for exceptions —
conspired to keep a neglected page working, and to keep its neglect invisible.

# The only real catastrophe was fresh

Here's the punchline. In nine years, the accumulated rot cost me a paint delay
and some phantom errors. Then I spent one week actively *improving* the page —
and did real damage in three days.

While modernizing, I added Google Consent Mode with the defaults every tutorial
shows: deny everything, let the cookie banner grant later. That default applies
globally — and visitors outside the EU never see a banner, so there was nothing
for them to accept. I had silently opted my entire non-EU majority out of
personalized ads. Page RPM collapsed from about €8–9 to €1.60 within days. The
fix is a region-scoped default: granted worldwide, denied where the law
requires prior consent.

Nine years of neglect: absorbed by other people's safety nets. Three days of
well-intentioned change: an actual, measurable disaster — caught quickly for
the sole reason that, for once, I was looking at the dashboards.

# What I learned

1. **Measure; don't reason from source code.** "The container is gone, so the
   callback never fires." "The product is dead, so the data stopped." "25,000
   zombie sites must mean thousands of broken ones." All three obvious, all
   three plausible, all three wrong. I went zero for three against my own
   website.
2. **A static page is a subscription to other people's product decisions** —
   and their retirement plans are more generous than you'd guess. The web's
   backward-compatibility machinery (vendor shims, browser tolerance, blocker
   stubs) is the real infrastructure, and it works disturbingly well.
3. **That resilience is exactly what makes rot invisible.** Fail-open means the
   residual damage concentrates where nobody's looking: on strict-privacy users
   no dashboard can see, on abandoned sites no one maintains. My page was
   "fine" on average and broken for a specific, unmeasurable minority for nine
   years.
4. **Your own browser lies to you.** Test your page the way you'd never browse:
   clean profile, no extensions, default DNS. Then again with strict privacy
   settings — those visitors exist, and for them your site may be a different
   site. (Quick check while you're at it: view-source, search for `async-hide`.
   If it's there, delete the snippet. It has done nothing useful since 2023.)

The site itself is in the best shape of its life now — all Core Web Vitals
green, first paint hostage to no one, a
[German version](https://keto-calculator.ankerl.com/de/), an
[embeddable version](https://keto-calculator.ankerl.com/embed.html). I did the
digging and the rebuild together with an AI coding agent (Claude), which read
through twelve years of accumulated HTML without complaining and, more
usefully, kept proving my best headlines wrong with a headless browser.

Is a €60-a-month website worth this much forensics? Probably not by the hour.
But I went in expecting to write about decay, and came out having watched half
the industry quietly hold my page together — Google shimming its own corpses,
Apple vetoing my viewport, uBlock disarming my booby trap. The catastrophe kept
refusing to happen. The least I could do was stop relying on that.

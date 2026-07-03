---
layout: post
title: "My website was blank for 4 seconds on every visit — for three years"
---

<!-- ═══════════════════════════════════════════════════════════════════════
     EDITOR NOTES (delete this comment block before publishing)

     • Front matter: adjust to your blog's conventions (categories, tags,
       permalink). Suggested tags: web, adsense, postmortem, keto-calculator.
     • Title alternatives:
         - "The website worked for 12 years. Its third-party scripts didn't."
         - "Anatomy of a slowly dying website"
     • The Optimize snippet quoted below is the STOCK Google Optimize
       page-hiding snippet (the site ran the standard one, 4000ms default).
       If you have the exact original in an old backup, paste that instead.
     • Numbers to sanity-check against your own records: peak revenue (I left
       it qualitative), the €8–9 → €1.6 RPM collapse (from the 2026-07-01
       commit message), 17% engagement / 65% mobile / ~4,850 sessions/mo
       (from md/analytics-summary.md).
     • The Claude/AI mention is one sentence, near the end. Cut it if you
       prefer the archaeology to stand alone.
     • HN submission: submit the blog URL directly, no editorializing in the
       title. Tuesday–Thursday, ~14:00–16:00 UTC tends to work best.
     ═══════════════════════════════════════════════════════════════════ -->

In 2012 I built a [keto macro calculator](https://keto-calculator.ankerl.com/)
because the advice online was vague and I wanted exact numbers for myself. I
[announced it on /r/keto](https://www.reddit.com/r/keto/comments/127sm0/keto_calculator/),
people liked it, Google ranked it, and for years it quietly earned real ad
money while I worked on other things. It's a single static HTML page. No
backend, no build step, no database. The kind of site that should be
immortal.

This summer I finally looked under the hood for the first time in years. The
page — my page, the one with my name on it — had been showing every single
visitor a blank white screen for four seconds before revealing itself.

It had been doing that since September 2023.

## The slow decline

The revenue graph told a story I thought I understood. From "quite a bit" at
its peak down to about €60 a month. My explanation was the obvious one: the
keto hype peaked around 2019, Google's algorithm updates buried little
single-page tools, and AI answer boxes now intercept the informational
queries. All of that is true.

But it turned out my site was also actively sabotaging itself, and had been
for years. The decline wasn't just the market. It was a graveyard of
third-party scripts that had died *around* my perfectly healthy HTML.

## The autopsy

**Exhibit A: the blank page.** Years ago I ran A/B tests with Google
Optimize. Optimize ships with an "anti-flicker" snippet so visitors don't see
the original page before the experiment variant swaps in. It looks like this:

```html
<style>.async-hide { opacity: 0 !important}</style>
<script>(function(a,s,y,n,c,h,i,d,e){s.className+=' '+y;h.start=1*new Date;
h.end=i=function(){s.className=s.className.replace(RegExp(' ?'+y),'')};
(a[n]=a[n]||[]).hide=h;setTimeout(function(){i();h.end=null},c);h.timeout=c;
})(window,document.documentElement,'async-hide','dataLayer',4000,
{'GTM-XXXXXXX':true});</script>
```

Read it carefully: it sets the entire `<html>` element to `opacity: 0` and
waits for the Optimize container to load and call the reveal function. If
that never happens, a safety timeout reveals the page after 4,000
milliseconds.

Google sunset Optimize on September 30, 2023. The container script was gone.
The reveal callback never fired again. So from that day on, **every visitor
stared at a blank page for the full four seconds**, then the timeout kicked
in and the page faded up as if nothing had happened.

The engagement rate over the last twelve months was 17%. One visitor in six
stuck around. I used to read that as "keto is over." A good chunk of it was
five lines of JavaScript waiting for a callback from a product that no longer
exists.

The cruel part is the failure mode: it fails *open*, invisibly. Nothing
threw. Nothing logged. The page worked perfectly — eventually. If the snippet
had thrown an error, the page would have stayed visible and I'd have lost
nothing. Because it "worked," I lost three years of first impressions.

**Exhibit B: nobody was watching.** Why didn't the analytics scream? Because
the analytics died first. The page carried a Universal Analytics tag, and
Google stopped processing UA hits on July 1, 2023 — two months before
Optimize died. The one instrument that might have shown me the cliff went
dark just before the cliff.

**Exhibit C: the error on every click.** Hundreds of links on the page carry
`onclick="return gatrack(this);"` for click tracking. At some point, the
*definition* of `gatrack` was commented out — but the hundreds of call sites
stayed. Every tracked click on the page threw an uncaught `ReferenceError`,
for years. Browsers shrug this off, links still navigate, so no user ever
noticed. Neither did I.

**Exhibit D: requests to a service that shut down.** The page still loaded
Bootstrap and jQuery through jsDelivr's `/g/` combine endpoint — an API that
was retired years ago. Two script requests on every page load, going to a
dead URL, since roughly the Obama administration.

**Exhibit E: the mobile lockout.** The viewport meta tag said
`user-scalable=no` on a fixed ~870-pixel layout. Two-thirds of my visitors
are on phones — the top three screen sizes are all iPhones — and they got a
desktop page they couldn't even pinch-zoom.

None of these things broke the site. That's the point. A static page doesn't
rot. Its `<script>` tags do — and they rot silently, because every one of
them is designed to degrade gracefully rather than fail loudly.

## Then I made a fresh one

While modernizing the page this June I added Google Consent Mode, the
GDPR-era mechanism that tells Google's tags what a visitor has consented to.
I set the defaults the way every tutorial shows:

```js
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  ...
});
```

Deny everything, let the cookie banner grant later. Safe, right?

Within days, page RPM collapsed from about €8–9 to €1.60. The mistake: that
default applies **globally**. An American visitor, to whom no consent banner
is ever shown, gets non-personalized ads forever — there's nothing for them
to click "accept" on. I had quietly opted my entire non-EU majority out of
personalized ads. The fix is a region-scoped default: granted worldwide,
denied only where the law actually requires prior consent, with Google's
consent message handling those visitors.

I only caught it because, for the first time in years, I was actually
watching the dashboards. Which is the whole lesson of this post compressed
into one week: the old mistakes survived for three years because nobody was
looking; the new mistake survived for three days because someone was.

## Where it stands now

The page is still a single static HTML file, and after the cleanup it's
faster than it ever was: real-user Core Web Vitals all green, total blocking
time in lab tests down from 490ms to zero, and the calculator JavaScript no
longer render-blocking. The dead scripts are gone, analytics is alive again,
consent is region-scoped, and there's now a [German version](https://keto-calculator.ankerl.com/de/)
and an [embeddable version](https://keto-calculator.ankerl.com/embed.html) if
you run a site in this space and want the calculator without the page around
it. I did the archaeology and the rebuild together with an AI coding agent
(Claude), which turns out to be very good at reading twelve years of
accumulated HTML strata without complaining.

## What I'd tell past me

1. **"Static site" is not "zero maintenance."** My HTML from 2012 renders
   fine. Every third-party `<script>` I added is a subscription to someone
   else's product decisions, and three of those products were discontinued
   under me.
2. **Third-party scripts fail open.** The anti-flicker snippet is the
   nightmare case: its failure mode was *hiding my entire site*, silently,
   with a timeout that made it look like slowness instead of breakage. Audit
   what happens to your page when each external script never answers.
3. **Dead instruments are worse than no instruments.** A missing analytics
   tag is a known unknown. A dead one is a dashboard you trust and never
   read.
4. **Put a date on it.** None of this needed weekly maintenance. One
   honest afternoon per year — load the page with DevTools open, look at the
   console, look at the network tab, look at the money — would have caught
   every single exhibit above.

Is a €60-a-month website worth any of this effort? Probably not, if you
price my hours honestly. But it was never really about the €60 — it's the
oldest thing I've built that strangers still use every day, and it deserved
better than to spend three years hiding behind an `opacity: 0` waiting for a
callback from beyond the grave.

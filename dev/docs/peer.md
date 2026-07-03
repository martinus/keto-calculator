All five peer reviews are in. Here's the chairman's synthesis.

council this: I have a homepage https://keto-calculator.ankerl.com/ which basically is a single static webpage. 6 years ago it used to earn quite a bit of google ad money, now only about 60 € a month. I want to modernize it with claude so I get more traffic and earn more money, what would be the best way forward? I want to keep having a static website though and won't reguklarky update it. This should be a one-time change , after that I do not want to update it for at least a year.

---

## Council Verdict: Reviving the Keto Calculator

**Vote tally:** Strongest response — the Executor took 3 of 5 votes, with the Contrarian and First Principles thinker getting one each. Biggest blind spot — the Expansionist's "build 15 pages" plan was flagged *unanimously* (5/5).

### Where the Council Agrees
- **A redesign alone won't bring traffic back.** Both the Contrarian and First Principles thinker independently nailed the same mechanism: your decline isn't because the HTML got old. It's Google's Helpful Content updates demoting thin calculator/FAQ pages, AI Overviews answering "keto macros" with zero clicks, and keto demand itself peaking in 2019. Rewriting JavaScript moves none of: **demand × rank × RPM**.
- **Check the data before doing any work.** The single most-repeated instruction across the council: pull **Google Search Console first**. If *impressions* (not just clicks) are falling, the audience left the market and no redesign saves it.
- **The durable technical wins are real and worth doing** — *if* demand exists: kill OneSignal push (earns nothing, tanks speed + scares users), defer AdSense/Cookiebot, split the 375KB file for speed, add JSON-LD schema, fix title/meta, optimize ad placement. The Executor's point: these **never rot**, so they survive your one-year freeze.
- **The "set-and-forget for a year" constraint fights modern SEO.** Anything freshness-dependent decays. Only speed, schema, and ad placement are truly maintenance-free.

### Where the Council Clashes
- **Invest vs. harvest vs. sell.** The Executor says: spend ~2 days, ship the durable wins, you'll earn more per visitor immediately. The First Principles thinker says: the category is dying — do 2 hours of cleanup and *walk away*, or **sell the domain while it still has standing**. The Contrarian sits between: prove demand first, because €720/year may not justify the effort. They disagree because they weight the same fact differently — is a shrinking-but-real niche worth optimizing, or is your time better spent elsewhere?
- **The Expansionist stands alone.** Its vision (15 interlinked calculators, embed widget, affiliate stacking, email list) is the most exciting — and every other advisor called it the biggest trap: mass-generated thin pages are *exactly* what Helpful Content buries, and affiliate links / email lists **violate your no-touch constraint**.

### Blind Spots the Council Caught
- **Nobody priced your time.** €60/month ≈ €720/year. Even a *doubling* nets ~€700. For a skilled engineer, two days of work clearing that bar is questionable on money alone — so the real question (raised in review) is: **do you want the money, or do you want a fun engineering project?** Be honest, because it changes the answer.
- **The AI-proof move everyone missed:** the one thing AI Overviews *can't* replicate is your **interactive, personalized result**. Make the output un-summarizable — shareable via URL params, a screenshot-able "your macros" card, "here's your day in actual food." That's the moat.
- **Instrument it before the freeze.** Add analytics so a year from now you can decide double-down / harvest / sell from data, not vibes.
- **The Outsider's trust fixes are free wins:** the arrival push-popup screams "spam," ads near the Calculate button cause misclicks, and a bare number ("eat 142g fat") with no "why" reads as made-up. Fixing these lifts conversion regardless of traffic.
- **One Expansionist idea survives scrutiny:** the **embeddable widget with a baked-in backlink** is genuinely set-and-forget and is the *one* legitimate organic-link engine in the bunch — unlike the rest of that plan.

### The Recommendation
**Run the Search Console check as a hard gate, then take the Executor's path — not the Expansionist's.** Concretely:

1. If impressions are *stable or growing* → do the ~2-day durable overhaul: kill OneSignal, fix speed, add schema, fix meta, optimize ads, plus the Outsider's trust fixes (explain the number, move ads away from the button) and the **URL-shareable result** for AI-proofing. Optionally ship the embed widget as your one passive backlink engine. This genuinely survives a year untouched.
2. If impressions are *falling* → the First Principles thinker wins: do 2 hours of cleanup and harvest, or **sell the domain** while "keto-calculator" still has standing. Don't pour days into a corpse.

Do **not** build 15 AI-spun pages — unanimous council judgment that it's 2018's playbook and breaks your own constraint.

And decide upfront whether this is a money project or a hobby. At €720/year, if it's about money the honest answer may be "sell." If it's a fun build, the Executor plan is the right, bounded scope.

### The One Thing to Do First
**Open Google Search Console and look at the last 16 months of *impressions* for the site.** Flat or rising = build (Executor plan). Falling = harvest or sell. Everything else is a guess until you see that one graph.

---

Want me to start on any of this — e.g. pull together the exact technical changes for the Executor plan (strip OneSignal, defer scripts, add JSON-LD, shareable-result URLs) so it's ready to ship the moment your Search Console check passes?

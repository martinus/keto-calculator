#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate embed.html (the embeddable widget) from index.html.

Why this exists: the widget is the full calculator with the page chrome
stripped — no header hero, no ads, no FAQ/comments/sidebar — so third-party
sites can iframe it ("Embed This Calculator" section on the main page hands
out the snippet). Rather than hand-maintaining a second big file, this script
derives embed.html from the current index.html, so the calculator logic can
never drift. Re-run it whenever index.html changes:

  python3 build_embed.py

It fails loudly (AssertionError) if an anchor it cuts on disappears from
index.html — that's the signal to update the anchor here, same philosophy as
de/build_de.py.

What the embed deliberately does NOT contain:
  - AdSense (serving ads into an iframe on someone else's site is an AdSense
    policy risk; the widget's value is the backlink + brand traffic)
  - the consent-message loader (no ads -> no ad consent needed; the GA4
    consent-mode defaults stay, so EEA analytics remains denied-by-default)
  - manifest / service-worker registration, FAQ + its JSON-LD, comments,
    the book rec, the sidebar, the about-me footer (replaced by a compact
    "Powered by" footer whose link opens the full site)

Kept fully functional: all inputs, results card, food equivalents, pies,
forecast + CSV, warnings, cookie persistence, URL-param prefill, and the
"Share my macros" button (its link intentionally points at the FULL site,
not the embed, so shares funnel people to keto-calculator.ankerl.com).
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "index.html")
OUT = os.path.join(HERE, "embed.html")

html = open(SRC, encoding="utf-8").read()


def cut(start_marker, end_marker, replacement="", include_end=False):
    """Remove [start_marker, end_marker) (or through end_marker when
    include_end) and insert `replacement`. Asserts both anchors exist."""
    global html
    s = html.index(start_marker)          # raises ValueError if missing
    e = html.index(end_marker, s)
    if include_end:
        e += len(end_marker)
    html = html[:s] + replacement + html[e:]


def rep(old, new):
    global html
    assert old in html, "anchor missing: %r" % old[:80]
    html = html.replace(old, new)


# --- <head> ---------------------------------------------------------------

rep('<title>Free Keto Macro Calculator – Find Your Macros for the Ketogenic Diet</title>',
    '<title>Keto Calculator Widget – Free Keto Macro Calculator</title>')

# noindex (it duplicates the main page's content); links open outside the iframe
rep('''	<link rel="canonical" href="https://keto-calculator.ankerl.com/">
	<link rel="alternate" hreflang="en" href="https://keto-calculator.ankerl.com/">
	<link rel="alternate" hreflang="de" href="https://keto-calculator.ankerl.com/de/">
	<link rel="alternate" hreflang="x-default" href="https://keto-calculator.ankerl.com/">''',
    '''	<meta name="robots" content="noindex">
	<base target="_blank">''')

# consent-message preconnect (the CMP loader itself goes with the app-service block)
rep('''	<!-- Google's consent message (Privacy & messaging) loads for EEA/UK visitors; preconnect trims its latency -->
	<link rel="preconnect" href="https://fundingchoicesmessages.google.com">
''', '')

# manifest + service-worker registration + the CMP loader (one contiguous block)
cut('<!-- app service stuff start', '<!-- app service stuff end -->', include_end=True)

# AdSense library
cut('<!-- AdSense library', 'adsbygoogle.js"></script>', include_end=True)

# JSON-LD blocks: WebApplication (head) and FAQPage (body) — the embed is
# noindex, and duplicate structured entities would only confuse crawlers.
for kind in ('"WebApplication"', '"FAQPage"'):
    s = 0
    removed = False
    while True:
        s = html.find('<script type="application/ld+json">', s)
        if s == -1:
            break
        e = html.index('</script>', s) + len('</script>')
        if kind in html[s:e]:
            html = html[:s] + html[e:]
            removed = True
            break
        s = e
    assert removed, "JSON-LD block not found: " + kind

# compact-chrome overrides for iframe embedding
rep('</head>', '''<style>
	/* embed.html overrides: compact chrome inside an <iframe> */
	#header { padding: 10px 0; }
	#header h1 { font-size: 30px !important; letter-spacing: -0.5px !important; margin: 8px 0 !important; }
	#header h1 a { color: inherit; text-decoration: none; }
	#logo { width: 40px !important; height: 40px !important; }
	#content { display: block !important; }
	#main { float: none !important; width: auto !important; max-width: 720px; margin: 0 auto; padding: 0 18px; }
	#bottom1 { margin-top: 28px; }
	</style>
</head>''')

# --- <body> ---------------------------------------------------------------

# header wordmark links to the full site (opens a new tab via <base target>)
rep('</a> Keto Calculator</h1>', '</a> Keto Calculator</h1><!-- embed: compact header, see overrides -->')

# "brought to you" strip becomes the visible powered-by credit
rep('                    By <a href="https://keto-calculator.ankerl.com/">keto-calculator.ankerl.com</a> &middot; <a href="de/" hreflang="de">Deutsch</a>',
    '                    Powered by <a href="https://keto-calculator.ankerl.com/">keto-calculator.ankerl.com</a> &middot; free keto macro calculator')

# intro video <details>
cut('<details class="detail-block" id="detail_intro"', '</details>', include_end=True)

# inline book rec (affiliate links stay on the main page only)
cut('<div class="recommended">', '<p>Macronutrients are nutrients that provide energy for your body.</p>')

# Keto Bottom ad unit
cut('<div class="fullwidthad">', '<!-- google adsense end -->\n\t\t\t\t\t\t</div>', include_end=True)

# FAQ section (its JSON-LD was already removed above)
cut('<div id="faq">', '<div id="questions">')

# questions section -> keep only the hidden copy-paste field the calc JS writes to
cut('<div id="questions">', '<div id="comments">',
    replacement='''<!-- The calculator JS fills this on every recalculation; the visible
					     /r/keto section lives on the main page only. -->
					<textarea name="reddit_copypaste" readonly="readonly" style="display:none" aria-hidden="true"></textarea>

					''')

# comments section
cut('<div id="comments">', '</form>')

# sidebar (the closing </div> re-inserted closes #content)
cut('<div id="sidebar">', '<div id="bottom1">', replacement='</div>\n\n\t\t')

# about-me footer -> compact powered-by footer (still closes #page)
cut('<div id="bottom1">', '<!-- track outbound links start -->',
    replacement='''<div id="bottom1">
		<div id="bottom2">
			<div id="aboutmewidth">
				Powered by <a href="https://keto-calculator.ankerl.com/"><b>Keto Calculator</b> &middot; keto-calculator.ankerl.com</a> —
				a free keto macro calculator by Martin Leitner-Ankerl. These numbers are estimates,
				not medical advice: <a href="https://keto-calculator.ankerl.com/disclaimer.html">disclaimer</a>.
			</div>
		</div>
	</div>
	</div>

	''')

# "Share my macros" from an embed hands out the FULL site's URL
rep("		var base = location.protocol + '//' + location.host + location.pathname;",
    "		var base = 'https://keto-calculator.ankerl.com/';  // embed: shares open the full site")

# Cusdis lazy-loader (no comment thread here)
s = html.index('// Lazy-load the Cusdis')
s = html.rindex('<script', 0, s)
e = html.index('<noscript>Please enable JavaScript to view the comments.</noscript>', s)
e += len('<noscript>Please enable JavaScript to view the comments.</noscript>')
html = html[:s] + html[e:]

# --- write ------------------------------------------------------------------
open(OUT, "w", encoding="utf-8").write(html)
print("OK: wrote embed.html (%d bytes)." % len(html))

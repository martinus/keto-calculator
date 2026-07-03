#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate de/index.html (German) from the English index.html in the repo root.

Why this exists: the site is a single flat index.html with all text inlined.
Rather than hand-maintaining a second 3700-line file, this script applies a
list of (English -> German) replacements to the current English source and
writes de/index.html. The German file IS committed and served directly; this
script is only run when you want to refresh the translation after editing the
English page.

How to update the translation after you change index.html:
  1. python3 dev/build_de.py
  2. If it prints "NOT FOUND" warnings, the English text for those snippets
     changed. Find the new English in index.html, update the matching German
     entry below (old = the new English, new = its translation), and re-run.
  3. Commit both index.html and the regenerated de/index.html.

See dev/TRANSLATION.md for the section checklist.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "index.html")
OUT = os.path.join(ROOT, "de", "index.html")

html = open(SRC, encoding="utf-8").read()
missing = []


def rep(old, new):
    """Replace ALL occurrences of `old`. Record a warning if not present."""
    global html
    if old not in html:
        missing.append(old)
        return
    html = html.replace(old, new)


# ---------------------------------------------------------------------------
# 1. <head>: lang, title, meta, social, schema, canonical + hreflang
# ---------------------------------------------------------------------------
rep('<html lang="en">', '<html lang="de">')

rep('<title>Free Keto Macro Calculator – Find Your Macros for the Ketogenic Diet</title>',
    '<title>Kostenloser Keto-Rechner – Makros für die ketogene Ernährung berechnen</title>')

rep('content="Calculate your exact keto macros in 60 seconds. Enter your weight, height, and goal to get personalized carb, protein, and fat targets for the ketogenic diet."',
    'content="Berechne deine Keto-Makros in 60 Sekunden. Gib Gewicht, Größe und Ziel ein und erhalte persönliche Werte für Kohlenhydrate, Eiweiß und Fett für die ketogene Ernährung."')

rep('content="Calculate your exact keto macros in 60 seconds — personalized carb, protein, and fat targets to lose weight on the ketogenic diet."',
    'content="Berechne deine Keto-Makros in 60 Sekunden — persönliche Werte für Kohlenhydrate, Eiweiß und Fett, um mit der ketogenen Ernährung abzunehmen."')

rep('<meta name="twitter:title" content="Free Keto Macro Calculator">',
    '<meta name="twitter:title" content="Kostenloser Keto-Rechner">')

rep('content="Calculate your exact keto macros in 60 seconds — personalized carb, protein, and fat targets for the ketogenic diet."',
    'content="Berechne deine Keto-Makros in 60 Sekunden — persönliche Werte für Kohlenhydrate, Eiweiß und Fett für die ketogene Ernährung."')

# Schema.org description
rep('"description": "Free keto macro calculator: enter your weight, height, and goal to get personalized carb, protein, and fat targets for the ketogenic diet.",',
    '"description": "Kostenloser Keto-Makro-Rechner: Gib Gewicht, Größe und Ziel ein und erhalte persönliche Werte für Kohlenhydrate, Eiweiß und Fett für die ketogene Ernährung.",')

# canonical -> /de/. The hreflang alternates are live on the English page and
# are already correct for the German page too (they list both languages), so
# only the canonical line itself changes.
rep('<link rel="canonical" href="https://keto-calculator.ankerl.com/">',
    '<link rel="canonical" href="https://keto-calculator.ankerl.com/de/">')

rep('<meta property="og:url" content="https://keto-calculator.ankerl.com/">',
    '<meta property="og:url" content="https://keto-calculator.ankerl.com/de/">')

# JSON-LD url fields (WebApplication + publisher both use this exact line)
rep('"url": "https://keto-calculator.ankerl.com/",',
    '"url": "https://keto-calculator.ankerl.com/de/",')

# ---------------------------------------------------------------------------
# 2. Header / intro
# ---------------------------------------------------------------------------
rep('title="A ketone, which is an organic compound with the structure RC(=O)R\'. When you eat low carb, your body will burn fat and start producing ketones to fuel your body. This process is called ketosis." alt="ketone"',
    'title="Ein Keton ist eine organische Verbindung mit der Struktur RC(=O)R\'. Wenn du wenig Kohlenhydrate isst, verbrennt dein Körper Fett und beginnt, Ketone als Brennstoff zu produzieren. Dieser Vorgang heißt Ketose." alt="Keton"')

rep('</a> Keto Calculator</h1>', '</a> Keto-Rechner</h1>')

# Language switcher in the "brought to you" strip (English page links to de/, so the
# German page must instead link back to the English root)
rep('                    By <a href="https://keto-calculator.ankerl.com/">keto-calculator.ankerl.com</a> &middot; <a href="de/" hreflang="de">Deutsch</a>',
    '                    Von <a href="https://keto-calculator.ankerl.com/de/">keto-calculator.ankerl.com</a> &middot; <a href="../" hreflang="en">English</a>')

# Lead paragraph
rep('This free keto calculator finds your personal macros — the exact grams of fat, protein, and net carbs to eat each day to lose weight on the <a href="https://www.reddit.com/r/keto/wiki/faq" onclick="return gatrack(this);">ketogenic diet</a>. Enter a few details below and get your numbers in under a minute.',
    'Dieser kostenlose Keto-Rechner ermittelt deine persönlichen Makros — die genaue Menge an Fett, Eiweiß und Netto-Kohlenhydraten, die du täglich essen solltest, um mit der <a href="https://www.reddit.com/r/keto/wiki/faq" onclick="return gatrack(this);">ketogenen Ernährung</a> abzunehmen. Gib unten ein paar Angaben ein und erhalte deine Werte in unter einer Minute.')

# Byline
rep('Built and maintained by <a href="#aboutme" onclick="return gatrack(this);">Martin Leitner-Ankerl</a>, a software developer who has followed and researched the ketogenic diet for years. The math uses the peer-reviewed Mifflin-St. Jeor equation. This is general information, not medical advice.',
    'Erstellt und gepflegt von <a href="#aboutme" onclick="return gatrack(this);">Martin Leitner-Ankerl</a>, einem Softwareentwickler, der sich seit Jahren mit der ketogenen Ernährung beschäftigt. Die Berechnung basiert auf der wissenschaftlich geprüften Mifflin-St.-Jeor-Formel. Dies sind allgemeine Informationen, keine medizinische Beratung.')

# Intro <details>
rep('<summary>What is a ketogenic diet? (+ video tutorial)</summary>',
    '<summary>Was ist eine ketogene Ernährung? (+ Video-Anleitung)</summary>')

rep("A ketogenic diet is high in fat, moderate in protein, and very low in carbohydrates. When you cut carbs this far, your body switches from running on sugar to running on fat — producing <em>ketones</em> as fuel along the way. Most people start keto to lose weight, and many also find it steadies their energy, appetite, and blood sugar through the day. It isn't magic and results vary from person to person, but a lot of people find it easier to stick to than constant calorie counting.",
    'Eine ketogene Ernährung ist reich an Fett, moderat im Eiweiß und sehr arm an Kohlenhydraten. Wenn du die Kohlenhydrate so stark reduzierst, stellt dein Körper von Zucker auf Fett als Energiequelle um — und produziert dabei <em>Ketone</em> als Brennstoff. Die meisten starten mit Keto, um abzunehmen, und viele empfinden über den Tag auch eine stabilere Energie, weniger Appetit und einen ruhigeren Blutzucker. Es ist kein Wundermittel und die Ergebnisse sind von Person zu Person verschieden, aber vielen fällt es leichter, dabeizubleiben, als ständig Kalorien zu zählen.')

rep('James Hardiman has created a nice tutorial for this calculator, watch it here:',
    'James Hardiman hat eine schöne Anleitung zu diesem Rechner erstellt, schau sie dir hier an:')

# ---------------------------------------------------------------------------
# 3. Section: Fat Loss Calculation + inputs
# ---------------------------------------------------------------------------
rep('<h2>Your Fat Loss Calculation</h2>', '<h2>Deine Fettabbau-Berechnung</h2>')
rep('<p>To get your personal customized recommendations, please enter some data about yourself.</p>',
    '<p>Für deine persönlichen Empfehlungen gib bitte ein paar Daten zu dir ein.</p>')

rep('<input name="sex" tabindex="1" type="radio" value="1">Female <input name="sex" tabindex="2" type="radio" value="0">Male',
    '<input name="sex" tabindex="1" type="radio" value="1">Weiblich <input name="sex" tabindex="2" type="radio" value="0">Männlich')

# Weight row: metric-first
rep('<input name="lbs" tabindex="3" type="number" step="0.1" value="" placeholder="180"> lbs weight (<input name="kg" type="number" step="0.1" value=""> kg)',
    '<input name="kg" tabindex="3" type="number" step="0.1" value="" placeholder="80"> kg Gewicht (<input name="lbs" type="number" step="0.1" value=""> lbs)')

# Height row: metric-first
rep('<input name="feet" tabindex="4" type="number" value="" step="1" style="width:3.4em" placeholder="5">\' <input name="inch" tabindex="5" type="number" step="1" value="" style="width:3.8em" placeholder="9">" tall (<input name="height" type="number" value=""> cm)',
    '<input name="height" tabindex="4" type="number" value="" placeholder="180"> cm groß (<input name="feet" type="number" value="" step="1" style="width:3.4em">\' <input name="inch" type="number" step="1" value="" style="width:3.8em">")')

rep('<tr><td>Date of birth: <input id="bday" name="bday" tabindex="6" type="text" placeholder="MM/DD/YYYY" style="width:7em" title="Write e.g. 8/30/1979">',
    '<tr><td>Geburtsdatum: <input id="bday" name="bday" tabindex="6" type="text" placeholder="TT.MM.JJJJ" style="width:7em" title="z. B. 30.8.1979">')

# Energy expenditure
rep('<h3>Determine Your Energy Expenditure</h3>', '<h3>Bestimme deinen Energieverbrauch</h3>')

rep('<p>Given that data, it is possible to calculate your <a href="https://en.wikipedia.org/wiki/Basal_metabolic_rate" onclick="return gatrack(this);">Base Metabolic Rate (BMR)</a>. This site uses the <a href="https://www.freedieting.com/calorie_needs.html" onclick="return gatrack(this);">Mifflin-St.Jeor-Formula</a> which was the most accurate in <a href="https://www.ncbi.nlm.nih.gov/pubmed/15883556" onclick="return gatrack(this);">two</a>&nbsp;<a href="https://www.ncbi.nlm.nih.gov/pubmed/18688113" onclick="return gatrack(this);">studies</a>.</p>',
    '<p>Mit diesen Daten lässt sich dein <a href="https://en.wikipedia.org/wiki/Basal_metabolic_rate" onclick="return gatrack(this);">Grundumsatz (BMR)</a> berechnen. Diese Seite verwendet die <a href="https://www.freedieting.com/calorie_needs.html" onclick="return gatrack(this);">Mifflin-St.-Jeor-Formel</a>, die in <a href="https://www.ncbi.nlm.nih.gov/pubmed/15883556" onclick="return gatrack(this);">zwei</a>&nbsp;<a href="https://www.ncbi.nlm.nih.gov/pubmed/18688113" onclick="return gatrack(this);">Studien</a> am genauesten war.</p>')

rep('kcal Base Metabolic Rate</li>', 'kcal Grundumsatz</li>')

rep("<p>The BMR resembles the resting metabolic rate. The real daily energy expenditure depends on how active you are on average. Based on that activity level we calculate your actual total daily energy expenditure (TDEE). This is the number of calories you need to consume each day when you do not want to lose weight.</p>",
    '<p>Der Grundumsatz entspricht in etwa dem Ruheumsatz. Dein tatsächlicher Tagesverbrauch hängt davon ab, wie aktiv du im Schnitt bist. Aus diesem Aktivitätsgrad berechnen wir deinen gesamten täglichen Energieverbrauch (TDEE). Das ist die Menge an Kalorien, die du täglich essen musst, wenn du dein Gewicht halten willst.</p>')

rep('<tr><td><input name="level" type="radio" value="0"></td><td>Sedentary. Typical desk job, little to no exercise.</td></tr>',
    '<tr><td><input name="level" type="radio" value="0"></td><td>Sitzend. Typischer Bürojob, kaum bis kein Sport.</td></tr>')
rep('<tr><td><input name="level" type="radio" value="1"></td><td>Lightly active. Walking around a good amount, retail jobs. 1–3 hours per week of light exercise.</td></tr>',
    '<tr><td><input name="level" type="radio" value="1"></td><td>Leicht aktiv. Viel auf den Beinen, z. B. im Einzelhandel. 1–3 Stunden leichter Sport pro Woche.</td></tr>')
rep('<tr><td><input name="level" type="radio" value="2"></td><td>Moderately active. 3–5 hours a week, e.g. daily 15 minutes biking and 3 times heavy lifting per week.</td></tr>',
    '<tr><td><input name="level" type="radio" value="2"></td><td>Mäßig aktiv. 3–5 Stunden pro Woche, z. B. täglich 15 Minuten Rad fahren und 3-mal pro Woche Krafttraining.</td></tr>')
rep('<tr><td><input name="level" type="radio" value="3"></td><td>Very active. Construction workers, hard exercise 6–7 days per week</td></tr>',
    '<tr><td><input name="level" type="radio" value="3"></td><td>Sehr aktiv. Körperliche Arbeit, hartes Training an 6–7 Tagen pro Woche.</td></tr>')
rep('<tr><td><input name="level" type="radio" value="4"></td><td>Custom: <input disabled="disabled" name="custom_expenditure" type="number" value=""> kcal</td></tr>',
    '<tr><td><input name="level" type="radio" value="4"></td><td>Eigener Wert: <input disabled="disabled" name="custom_expenditure" type="number" value=""> kcal</td></tr>')

rep('kcal daily energy expenditure</li>', 'kcal täglicher Energieverbrauch</li>')

# Body fat
rep('<h3>How Much Body Fat do you Have?</h3>', '<h3>Wie hoch ist dein Körperfettanteil?</h3>')

rep('<p>Let\'s find out your body fat percentage. Based on your height and weight, your body fat percentage might be <a href="https://www.ncbi.nlm.nih.gov/pubmed/16469982" onclick="return gatrack(this);">around <span class="estimated_bodyfat_percent"></span>%</a>. The most accurate measurement would be a <a href="https://en.wikipedia.org/wiki/Dual_energy_X-ray_absorptiometry" onclick="return gatrack(this);">DEXA</a>. Skin fold measurement with <a href="https://www.amazon.com/gp/product/B0000AN3UB/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=B0000AN3UB&amp;linkCode=as2&amp;tag=martanke-20" onclick="return gatrack(this);">a good caliper</a> is also pretty accurate. The easiest way is to just estimate it from some <a href="https://martin.ankerl.com/2016/01/04/body-fat-comparison-pictures/" onclick="return gatrack(this);">comparison pictures</a>. More: <a href="https://www.builtlean.com/2012/09/24/body-fat-percentage-men-women/" onclick="return gatrack(this);">1</a>, <a href="https://www.leighpeele.com/body-fat-pictures-and-percentages" onclick="return gatrack(this);">2</a>, <a href="https://www.nerdfitness.com/blog/2012/07/02/body-fat-percentage/" onclick="return gatrack(this);">3</a>. You can also try <a href="https://www.healthcentral.com/cholesterol/home-body-fat-test-2774-143.html" onclick="return gatrack(this);">this calculator</a> but that can be inaccurate.</p>',
    '<p>Finden wir deinen Körperfettanteil heraus. Basierend auf Größe und Gewicht liegt er vermutlich <a href="https://www.ncbi.nlm.nih.gov/pubmed/16469982" onclick="return gatrack(this);">bei etwa <span class="estimated_bodyfat_percent"></span>%</a>. Am genauesten misst ein <a href="https://en.wikipedia.org/wiki/Dual_energy_X-ray_absorptiometry" onclick="return gatrack(this);">DEXA-Scan</a>. Auch die Messung der Hautfalten mit <a href="https://www.amazon.com/gp/product/B0000AN3UB/ref=as_li_ss_tl?ie=UTF8&amp;camp=1789&amp;creative=390957&amp;creativeASIN=B0000AN3UB&amp;linkCode=as2&amp;tag=martanke-20" onclick="return gatrack(this);">einem guten Caliper</a> ist recht genau. Am einfachsten schätzt du ihn anhand von <a href="https://martin.ankerl.com/2016/01/04/body-fat-comparison-pictures/" onclick="return gatrack(this);">Vergleichsbildern</a>. Mehr: <a href="https://www.builtlean.com/2012/09/24/body-fat-percentage-men-women/" onclick="return gatrack(this);">1</a>, <a href="https://www.leighpeele.com/body-fat-pictures-and-percentages" onclick="return gatrack(this);">2</a>, <a href="https://www.nerdfitness.com/blog/2012/07/02/body-fat-percentage/" onclick="return gatrack(this);">3</a>. Du kannst auch <a href="https://www.healthcentral.com/cholesterol/home-body-fat-test-2774-143.html" onclick="return gatrack(this);">diesen Rechner</a> ausprobieren, der kann aber ungenau sein.</p>')

rep('<input name="bodyfat" type="number" value="" placeholder="20"> % Body fat</li>',
    '<input name="bodyfat" type="number" value="" placeholder="20"> % Körperfett</li>')

rep('<p>With <span class="bodyfat_percentage"></span>% body fat you have <span class="lean_lbs"></span>lbs (<span class="lean_kg"></span>kg) of lean body mass, and <span class="fat_lbs"></span>lbs (<span class="fat_kg"></span>kg) of body fat. This includes about <span class="essential_fat_lbs"></span>lbs (<span class="essential_fat_kg"></span>kg) of <a href="https://en.wikipedia.org/wiki/Body_fat_percentage#Typical_body_fat_amounts" onclick="return gatrack(this);">essential body fat</a> that you must not lose.</p>',
    '<p>Bei <span class="bodyfat_percentage"></span>% Körperfett hast du <span class="lean_kg"></span>kg (<span class="lean_lbs"></span>lbs) fettfreie Masse und <span class="fat_kg"></span>kg (<span class="fat_lbs"></span>lbs) Körperfett. Davon sind etwa <span class="essential_fat_kg"></span>kg (<span class="essential_fat_lbs"></span>lbs) <a href="https://en.wikipedia.org/wiki/Body_fat_percentage#Typical_body_fat_amounts" onclick="return gatrack(this);">essentielles Körperfett</a>, das du nicht verlieren darfst.</p>')

# ---------------------------------------------------------------------------
# 4. Section: Macronutrient ratio
# ---------------------------------------------------------------------------
rep('<h2>Learn Your Optimal Macronutrient Ratio</h2>', '<h2>Finde dein optimales Makronährstoff-Verhältnis</h2>')
rep('<p class="rec-label">📚 Want the science behind it? Books I recommend:</p>',
    '<p class="rec-label">📚 Willst du die Wissenschaft dahinter? Diese Bücher empfehle ich:</p>')
rep('<p>Macronutrients are nutrients that provide energy for your body.</p>',
    '<p>Makronährstoffe sind Nährstoffe, die deinem Körper Energie liefern.</p>')

# Carbs
rep('<h3>How Many Carbs Can I Eat?</h3>', '<h3>Wie viele Kohlenhydrate darf ich essen?</h3>')
rep('<p>Most people stay in ketosis somewhere between 20 and 50g of net carbs a day. This calculator starts you at 25g — a sweet spot that works for the majority. Spend those carbs wisely: get them from vegetables (10–15g), nuts and seeds (5–10g), and a little fruit (5–10g) rather than from sugar and grains. One catch with labels: in Europe they usually already show net carbs, while in the US they show total carbs, so subtract the fiber yourself.</p>',
    '<p>Die meisten bleiben mit 20 bis 50g Netto-Kohlenhydraten pro Tag in der Ketose. Dieser Rechner startet bei 25g — ein guter Richtwert, der für die meisten passt. Setze die Kohlenhydrate sinnvoll ein: hol sie dir aus Gemüse (10–15g), Nüssen und Samen (5–10g) und etwas Obst (5–10g) statt aus Zucker und Getreide. Ein Hinweis zu den Nährwertangaben: In Europa stehen meist schon die Netto-Kohlenhydrate auf der Packung, in den USA dagegen die Gesamt-Kohlenhydrate — dort musst du die Ballaststoffe selbst abziehen.</p>')

rep('<summary>Net carbs vs. fiber — what actually counts?</summary>',
    '<summary>Netto-Kohlenhydrate vs. Ballaststoffe — was zählt wirklich?</summary>')
rep('<p>Total carbohydrate is made up of net carbs plus fiber. Net carbs are the part that turns into glucose and raises your blood sugar — exactly what you want to limit on keto, which is why most people aim for 20–25g a day. Fiber is the rest, and it\'s good for you: insoluble fiber passes straight through without touching your blood sugar, while gut bacteria ferment soluble fiber into fatty acids that add only a few calories and don\'t spike glucose. That\'s why keto counts net carbs and lets fiber off the hook.</p>',
    '<p>Die Gesamt-Kohlenhydrate setzen sich aus Netto-Kohlenhydraten plus Ballaststoffen zusammen. Die Netto-Kohlenhydrate sind der Teil, der zu Glukose wird und deinen Blutzucker hebt — genau das willst du bei Keto begrenzen, weshalb die meisten 20–25g pro Tag anpeilen. Ballaststoffe sind der Rest und sie tun dir gut: unlösliche Ballaststoffe wandern unverändert hindurch, ohne den Blutzucker zu beeinflussen, während Darmbakterien lösliche Ballaststoffe zu Fettsäuren vergären, die nur wenige Kalorien liefern und den Blutzucker nicht ansteigen lassen. Deshalb zählt Keto die Netto-Kohlenhydrate und lässt die Ballaststoffe außen vor.</p>')

rep('<input name="carbs" type="number" value="25"> g daily net carbs (changeable)</li>',
    '<input name="carbs" type="number" value="25"> g Netto-Kohlenhydrate pro Tag (änderbar)</li>')

# Protein
rep('<h3>How Much Protein Should I Eat?</h3>', '<h3>Wie viel Eiweiß sollte ich essen?</h3>')
rep('<p>It is important to get enough protein to maintain your muscles, but not too much or it will kick you out of ketosis.</p>',
    '<p>Es ist wichtig, genug Eiweiß zu essen, um deine Muskeln zu erhalten — aber nicht zu viel, sonst wirft es dich aus der Ketose.</p>')
rep('<p>Based on your personal data, you should stay above <span class="min_protein_g"></span>g if you are mostly sedentary. You can go as high as <span class="max_protein_g"></span>g if you put your muscles under a lot of new stress or with a large caloric deficit. High protein prevents muscle loss.</p>',
    '<p>Anhand deiner Daten solltest du über <span class="min_protein_g"></span>g bleiben, wenn du überwiegend sitzend lebst. Bis zu <span class="max_protein_g"></span>g sind möglich, wenn du deine Muskeln stark forderst oder ein großes Kaloriendefizit fährst. Viel Eiweiß schützt vor Muskelverlust.</p>')
rep('<p>When in doubt, choose the middle ground. For you, that\'s <span class="mid_protein_g"></span>g.</p>',
    '<p>Im Zweifel wähle die Mitte. Für dich sind das <span class="mid_protein_g"></span>g.</p>')

rep('<summary>Why not just eat more protein?</summary>', '<summary>Warum nicht einfach mehr Eiweiß essen?</summary>')
rep('<p>When you\'re losing weight or under physical stress, eating somewhat more protein than the <a href="https://en.wikipedia.org/wiki/Reference_Daily_Intake#Food_labeling_reference_tables" onclick="return gatrack(this);">RDA</a> is a good thing — it protects your muscle. Going far above what you need can work against ketosis, though: the body can convert the excess amino acids into glucose, which nudges ketone levels down. So don\'t fear protein — just don\'t massively overshoot the maximum below.</p>',
    '<p>Wenn du abnimmst oder körperlich gefordert bist, ist etwas mehr Eiweiß als die <a href="https://en.wikipedia.org/wiki/Reference_Daily_Intake#Food_labeling_reference_tables" onclick="return gatrack(this);">empfohlene Tagesmenge</a> gut — es schützt deine Muskeln. Deutlich mehr als nötig kann der Ketose aber entgegenwirken: Der Körper kann die überschüssigen Aminosäuren in Glukose umwandeln, was den Ketonspiegel etwas senkt. Hab also keine Angst vor Eiweiß — überschreite nur das unten stehende Maximum nicht massiv.</p>')

rep('See <a href="https://www.bodyrecomposition.com/fat-loss/protein-intake-while-dieting-qa.html" onclick="return gatrack(this);">Protein Intake While Dieting</a> and the book <a href="https://www.amazon.com/gp/product/0983490716/ref=as_li_qf_sp_asin_il?ie=UTF8&amp;tag=martanke-20&amp;linkCode=as2&amp;camp=1789&amp;creative=9325&amp;creativeASIN=0983490716" onclick="return gatrack(this);">The Art and Science of Low Carbohydrate Performance</a> for details. The maximum protein level used here is based on the research paper "<a href="https://www.ncbi.nlm.nih.gov/pubmed/22150425" onclick="return gatrack(this);">Dietary protein for athletes: From requirements to optimum adaptation</a>" analyzed in "<a href="https://bayesianbodybuilding.com/the-myth-of-1glb-optimal-protein-intake-for-bodybuilders/" onclick="return gatrack(this);">The Myth of 1 g/lb: Optimal Protein Intake for Bodybuilders</a>". Even professional body builders should have no benefit in going above the upper limit used here. The values here are in g/lbs of <em>lean</em> body mass, while in the previous link they talk about g/lbs of total body weight. That\'s why the number here seems a bit higher.',
    'Mehr dazu in <a href="https://www.bodyrecomposition.com/fat-loss/protein-intake-while-dieting-qa.html" onclick="return gatrack(this);">Protein Intake While Dieting</a> und im Buch <a href="https://www.amazon.com/gp/product/0983490716/ref=as_li_qf_sp_asin_il?ie=UTF8&amp;tag=martanke-20&amp;linkCode=as2&amp;camp=1789&amp;creative=9325&amp;creativeASIN=0983490716" onclick="return gatrack(this);">The Art and Science of Low Carbohydrate Performance</a>. Das hier verwendete Eiweiß-Maximum beruht auf der Studie „<a href="https://www.ncbi.nlm.nih.gov/pubmed/22150425" onclick="return gatrack(this);">Dietary protein for athletes: From requirements to optimum adaptation</a>“, ausgewertet in „<a href="https://bayesianbodybuilding.com/the-myth-of-1glb-optimal-protein-intake-for-bodybuilders/" onclick="return gatrack(this);">The Myth of 1 g/lb: Optimal Protein Intake for Bodybuilders</a>“. Selbst Profi-Bodybuilder haben keinen Vorteil davon, über die hier genutzte Obergrenze zu gehen. Die Werte hier beziehen sich auf g/lbs <em>fettfreie</em> Masse, im verlinkten Artikel dagegen auf g/lbs Gesamtgewicht — deshalb wirkt die Zahl hier etwas höher.')

rep('<td width="33%">no exercise</td>', '<td width="33%">kein Sport</td>')
rep('<td width="33%">chosen amount</td>', '<td width="33%">gewählte Menge</td>')
rep('<td>very active</td>', '<td>sehr aktiv</td>')
rep('g&nbsp;minimum</td>', 'g&nbsp;Minimum</td>')
rep('g&nbsp;chosen</td>', 'g&nbsp;gewählt</td>')
rep('g&nbsp;maximum</td>', 'g&nbsp;Maximum</td>')

# Fat
rep('<h3>How Much Fat Should I Eat?</h3>', '<h3>Wie viel Fett sollte ich essen?</h3>')
rep('<p>Eat fat to your liking. You have chosen <span class="carbs"></span>g of carbs and <span class="protein"></span>g protein. This means you have already <span class="kcal_nonfat"></span>kcal of your daily requirements covered. What\'s left for you to choose is how much fat to eat.</p>',
    '<p>Iss Fett nach Belieben. Du hast <span class="carbs"></span>g Kohlenhydrate und <span class="protein"></span>g Eiweiß gewählt. Damit sind bereits <span class="kcal_nonfat"></span>kcal deines Tagesbedarfs gedeckt. Was du jetzt noch festlegst, ist die Menge an Fett.</p>')
rep('<p>Here you can choose your caloric intake. Try a moderate deficit and only go lower if you feel comfortable after about a week.</p>',
    '<p>Hier wählst du deine Kalorienzufuhr. Probier ein moderates Defizit und geh erst tiefer, wenn du dich nach etwa einer Woche damit wohlfühlst.</p>')

rep('<summary>How low can your calories go?</summary>', '<summary>Wie niedrig dürfen deine Kalorien sein?</summary>')
rep('<p>Fat intake depends on your goal. If you want to lose weight, your total calories have to be below your maintenance calories of <span class="expenditure_kcal"></span>kcal. Think of fat as your healthy filler nutrient. To maintain your current weight, fill all the <span class="kcal_fat"></span> remaining calories up with <span class="fat_g_max"></span>g fat. Don\'t go below <span class="fat_g_min"></span>g of fat.</p>',
    '<p>Wie viel Fett du isst, hängt von deinem Ziel ab. Zum Abnehmen müssen deine Gesamtkalorien unter deinem Erhaltungsbedarf von <span class="expenditure_kcal"></span>kcal liegen. Sieh Fett als deinen gesunden Auffüll-Nährstoff. Um dein Gewicht zu halten, füllst du die restlichen <span class="kcal_fat"></span> Kalorien mit <span class="fat_g_max"></span>g Fett auf. Geh nicht unter <span class="fat_g_min"></span>g Fett.</p>')
rep('<p>If you want to lose weight, your total calories have to eat less than <span class="expenditure_kcal"></span>kcal. How low can you go? This depends on the maximum rate your body can release body fat (See discussion <a href="https://www.reddit.com/r/keto/comments/127sm0/keto_calculator/c6sw2xc" onclick="return gatrack(this);">1</a> and <a href="https://www.reddit.com/r/keto/comments/12amhq/keto_calculator_20/c6vvu7f?context=3" onclick="return gatrack(this);">2</a>). If you eat <b>above </b> <span class="fat_g_min"></span>g of fat, your body burns only fat and you will lose weight. If you eat <b>below</b> that, your body will start burning protein. This means your body cannot produce that many calories from fat only. You will start to lose your hard earned muscles. You don\'t want that.</p>',
    '<p>Zum Abnehmen musst du weniger als <span class="expenditure_kcal"></span>kcal essen. Wie tief kannst du gehen? Das hängt davon ab, wie schnell dein Körper maximal Körperfett freisetzen kann (siehe Diskussion <a href="https://www.reddit.com/r/keto/comments/127sm0/keto_calculator/c6sw2xc" onclick="return gatrack(this);">1</a> und <a href="https://www.reddit.com/r/keto/comments/12amhq/keto_calculator_20/c6vvu7f?context=3" onclick="return gatrack(this);">2</a>). Isst du <b>mehr als</b> <span class="fat_g_min"></span>g Fett, verbrennt dein Körper nur Fett und du nimmst ab. Isst du <b>weniger</b>, beginnt dein Körper, Eiweiß zu verbrennen — er kann dann nicht genug Kalorien allein aus Fett gewinnen. Du verlierst deine hart erarbeiteten Muskeln. Das willst du nicht.</p>')
rep('<p>Also, you should not go below 30g of daily fat to prevent the formation of gallstones. (See <a href="https://www.amazon.com/gp/product/0983490708/ref=as_li_qf_sp_asin_il?ie=UTF8&amp;tag=martanke-20&amp;linkCode=as2&amp;camp=1789&amp;creative=9325&amp;creativeASIN=0983490708" onclick="return gatrack(this);">TAaSoLCL</a> page 168).</p>',
    '<p>Außerdem solltest du nicht unter 30g Fett pro Tag gehen, um Gallensteinen vorzubeugen. (Siehe <a href="https://www.amazon.com/gp/product/0983490708/ref=as_li_qf_sp_asin_il?ie=UTF8&amp;tag=martanke-20&amp;linkCode=as2&amp;camp=1789&amp;creative=9325&amp;creativeASIN=0983490708" onclick="return gatrack(this);">TAaSoLCL</a>, Seite 168).</p>')

rep('<td width="33%">lowest intake</td>', '<td width="33%">niedrigste Zufuhr</td>')
rep('<td width="33%">chosen intake</td>', '<td width="33%">gewählte Zufuhr</td>')
rep('<td>maintenance</td>', '<td>Erhaltung</td>')
rep('%&nbsp;deficit</td>', '%&nbsp;Defizit</td>')
rep('kcal&nbsp;min</td>', 'kcal&nbsp;min</td>')
rep('kcal&nbsp;chosen</td>', 'kcal&nbsp;gewählt</td>')
rep('kcal&nbsp;max</td>', 'kcal&nbsp;max</td>')
rep('g&nbsp;fat&nbsp;min</td>', 'g&nbsp;Fett&nbsp;min</td>')
rep('g&nbsp;fat&nbsp;chosen</td>', 'g&nbsp;Fett&nbsp;gewählt</td>')
rep('g&nbsp;fat&nbsp;max</td>', 'g&nbsp;Fett&nbsp;max</td>')

# ---------------------------------------------------------------------------
# 5. Results card
# ---------------------------------------------------------------------------
rep('<h2 id="yourpersonalresults">Your Personal Results</h2>', '<h2 id="yourpersonalresults">Deine persönlichen Ergebnisse</h2>')
rep('<p>Here are your personal macros:</p>', '<p>Hier sind deine persönlichen Makros:</p>')
rep('<span class="results-kcal-label">kcal / day<br>daily calorie target</span>',
    '<span class="results-kcal-label">kcal / Tag<br>tägliches Kalorienziel</span>')
rep('<span class="macro-name">Carbs</span>', '<span class="macro-name">Kohlenhydrate</span>')
rep('<span class="macro-name">Protein</span>', '<span class="macro-name">Eiweiß</span>')
rep('<span class="macro-name">Fat</span>', '<span class="macro-name">Fett</span>')
rep('Rough daily comparisons spread across all your meals — mix and match real foods, these aren\'t exact.',
    'Grobe Tagesvergleiche, verteilt auf alle Mahlzeiten — kombiniere echte Lebensmittel, die Angaben sind Näherungen.')

rep('<strong>These numbers are estimates, not medical advice.</strong> They come from the\n\t\t\t\t\t\tMifflin-St. Jeor equation and your lean body mass — a solid starting point, but everyone is\n\t\t\t\t\t\tdifferent. Adjust based on how you feel and your real results, and talk to your doctor before\n\t\t\t\t\t\tbig dietary changes, especially if you have a health condition. See the\n\t\t\t\t\t\t<a href="disclaimer.html" onclick="return gatrack(this);">full disclaimer</a>.',
    '<strong>Diese Zahlen sind Schätzungen, keine medizinische Beratung.</strong> Sie stammen aus der\n\t\t\t\t\t\tMifflin-St.-Jeor-Formel und deiner fettfreien Masse — ein solider Ausgangspunkt, aber jeder Mensch ist\n\t\t\t\t\t\tanders. Passe sie an dein Befinden und deine echten Ergebnisse an und sprich vor\n\t\t\t\t\t\tgrößeren Ernährungsumstellungen mit deinem Arzt, besonders bei Vorerkrankungen. Siehe den\n\t\t\t\t\t\t<a href="disclaimer.html" onclick="return gatrack(this);">vollständigen Haftungsausschluss</a>.')

rep('>🔗 Share my macros</button>', '>🔗 Meine Makros teilen</button>')
rep('<p style="font-size:smaller; color:#666; margin-top:-0.5em;">Copies a link that reopens this calculator with your numbers already filled in — handy for saving or sharing on Reddit.</p>',
    '<p style="font-size:smaller; color:#666; margin-top:-0.5em;">Kopiert einen Link, der diesen Rechner mit deinen Werten bereits ausgefüllt öffnet — praktisch zum Speichern oder Teilen.</p>')

# Pies + projection
rep('<p>Here is a visual representation of your macros and your deficit. The area of the circles is exactly scaled based on your ratios.</p>',
    '<p>Hier sind deine Makros und dein Defizit grafisch dargestellt. Die Fläche der Kreise ist exakt nach deinen Verhältnissen skaliert.</p>')
rep('<span class="pie-label">Weight Maintenance</span>', '<span class="pie-label">Gewicht halten</span>')
rep('<span class="pie-label">Your Target</span>', '<span class="pie-label">Dein Ziel</span>')
rep('<span class="pie-label">Deficit</span>', '<span class="pie-label">Defizit</span>')
rep('<p>If you stick to <span class="carbs"></span>g of carbs, <span class="protein"></span>g protein, and <span class="fat"></span>g fat, you will eat <span class="target_kcal"></span>kcal and lose <span class="chosen_loss_lbs"></span>lbs (<span class="chosen_loss_kg"></span>kg) in the first month. Keep in mind that your body weight can fluctuate by &plusmn;4lbs (&plusmn;2kg) on any given day from water weight and what\'s in your stomach. Recalculate your macro ratio once a month! Changes in body composition have a large influence on the recommendations and weight loss.</p>',
    '<p>Wenn du bei <span class="carbs"></span>g Kohlenhydrate, <span class="protein"></span>g Eiweiß und <span class="fat"></span>g Fett bleibst, isst du <span class="target_kcal"></span>kcal und verlierst im ersten Monat <span class="chosen_loss_kg"></span>kg (<span class="chosen_loss_lbs"></span>lbs). Bedenke, dass dein Gewicht an einzelnen Tagen um &plusmn;2kg (&plusmn;4lbs) schwanken kann — durch Wasser und Mageninhalt. Berechne dein Makro-Verhältnis einmal im Monat neu! Veränderungen der Körperzusammensetzung haben großen Einfluss auf die Empfehlungen und den Gewichtsverlust.</p>')
rep('<p>If you use <a href="https://www.myfitnesspal.com/" onclick="return gatrack(this);">MFP</a>, update <a href="https://www.myfitnesspal.com/account/change_goals_custom" onclick="return gatrack(this);">your custom goals</a> with the percentages above. Note: percentage in MFP and above is calculated for calories.</p>',
    '<p>Wenn du <a href="https://www.myfitnesspal.com/" onclick="return gatrack(this);">MFP</a> nutzt, trage die obigen Prozentwerte in <a href="https://www.myfitnesspal.com/account/change_goals_custom" onclick="return gatrack(this);">deine eigenen Ziele</a> ein. Hinweis: Die Prozentwerte in MFP und oben beziehen sich auf Kalorien.</p>')

# Forecast
rep('<h3>Your Weight Loss Forecast</h3>', '<h3>Deine Abnehm-Prognose</h3>')
rep('<p>Now to the fun stuff: a weight and body fat forecast for one year, starting today. Remember that this is a rough estimate and your personal results can differ.</p>',
    '<p>Jetzt zum spannenden Teil: eine Gewichts- und Körperfett-Prognose für ein Jahr ab heute. Denk daran, dass dies eine grobe Schätzung ist und deine persönlichen Ergebnisse abweichen können.</p>')
rep('<p>Choose lbs or kg, and then play around with your chosen fat intake to see how it affects weight loss.</p>',
    '<p>Wähle kg oder lbs und spiele dann mit deiner gewählten Fettzufuhr, um zu sehen, wie sie den Gewichtsverlust beeinflusst.</p>')
rep('<li>Start on <input id="graphstartdate" name="graphstartdate" type="text" placeholder="MM/DD/YYYY" style="width:7em" title="Write e.g. 8/30/1979">.</li>',
    '<li>Beginn am <input id="graphstartdate" name="graphstartdate" type="text" placeholder="TT.MM.JJJJ" style="width:7em" title="z. B. 30.8.1979">.</li>')
rep('<li>Show in <input name="chart_weight_type" type="radio" value="1">lbs or <input name="chart_weight_type" type="radio" value="0">kg</li>',
    '<li>Anzeigen in <input name="chart_weight_type" type="radio" value="0">kg oder <input name="chart_weight_type" type="radio" value="1">lbs</li>')
rep('Please enter a date and click lbs or kg to show the graph.',
    'Bitte gib ein Datum ein und klicke auf kg oder lbs, um die Grafik anzuzeigen.')
rep('<p>For all you data junkies, you can <a id="csvdownload" download="KetoCalculatorForecast.csv" href="javascript:void(0)">download a CSV file of your projected weight loss</a>. This contains all the data used in the above graph.',
    '<p>Für alle Daten-Fans: Du kannst <a id="csvdownload" download="KetoCalculatorForecast.csv" href="javascript:void(0)">eine CSV-Datei deines prognostizierten Gewichtsverlaufs herunterladen</a>. Sie enthält alle Daten der obigen Grafik.')

# ---------------------------------------------------------------------------
# 6. FAQ (visible <h3>/<p> AND JSON-LD name/text)
# ---------------------------------------------------------------------------
rep('<h2>Keto Calculator FAQ</h2>', '<h2>Keto-Rechner FAQ</h2>')

# Q1
rep('<h3>How many carbs can I eat on keto?</h3>', '<h3>Wie viele Kohlenhydrate darf ich bei Keto essen?</h3>')
rep('"name": "How many carbs can I eat on keto?"', '"name": "Wie viele Kohlenhydrate darf ich bei Keto essen?"')
rep('Most people stay in ketosis on 20–50 grams of net carbs per day. This calculator defaults to 25 grams, which works well for the majority. Get your carbs from vegetables, nuts, and a little fruit rather than from sugar and grains.',
    'Die meisten bleiben mit 20–50 Gramm Netto-Kohlenhydraten pro Tag in der Ketose. Dieser Rechner ist auf 25 Gramm voreingestellt, was für die meisten gut passt. Hol dir die Kohlenhydrate aus Gemüse, Nüssen und etwas Obst statt aus Zucker und Getreide.')

# Q2
rep('<h3>How much protein should I eat on keto?</h3>', '<h3>Wie viel Eiweiß sollte ich bei Keto essen?</h3>')
rep('"name": "How much protein should I eat on keto?"', '"name": "Wie viel Eiweiß sollte ich bei Keto essen?"')
rep('Protein is set from your lean body mass, not your total weight — roughly 1.3 to 2.2 grams per kilogram of lean mass. The calculator gives you a personalized minimum and maximum so you keep muscle without eating so much that it interferes with ketosis.',
    'Das Eiweiß richtet sich nach deiner fettfreien Masse, nicht nach deinem Gesamtgewicht — etwa 1,3 bis 2,2 Gramm pro Kilogramm fettfreie Masse. Der Rechner gibt dir ein persönliches Minimum und Maximum, damit du Muskeln erhältst, ohne so viel zu essen, dass es die Ketose stört.')

# Q3
rep('<h3>What is a macro?</h3>', '<h3>Was ist ein Makro?</h3>')
rep('"name": "What is a macro?"', '"name": "Was ist ein Makro?"')
rep('<p>"Macro" is short for macronutrient — the three nutrients that give your body energy: fat, protein, and carbohydrates. On keto you eat high fat, moderate protein, and very few carbs.</p>',
    '<p>„Makro“ ist die Kurzform für Makronährstoff — die drei Nährstoffe, die deinem Körper Energie liefern: Fett, Eiweiß und Kohlenhydrate. Bei Keto isst du viel Fett, moderat Eiweiß und sehr wenig Kohlenhydrate.</p>')
rep('"text": "Macro is short for macronutrient — the three nutrients that give your body energy: fat, protein, and carbohydrates. On keto you eat high fat, moderate protein, and very few carbs."',
    '"text": "Makro ist die Kurzform für Makronährstoff — die drei Nährstoffe, die deinem Körper Energie liefern: Fett, Eiweiß und Kohlenhydrate. Bei Keto isst du viel Fett, moderat Eiweiß und sehr wenig Kohlenhydrate."')

# Q4
rep('<h3>What is the difference between net carbs and total carbs?</h3>', '<h3>Was ist der Unterschied zwischen Netto- und Gesamt-Kohlenhydraten?</h3>')
rep('"name": "What is the difference between net carbs and total carbs?"', '"name": "Was ist der Unterschied zwischen Netto- und Gesamt-Kohlenhydraten?"')
rep('Net carbs are total carbohydrates minus fiber (and sugar alcohols). Fiber does not raise blood sugar, so keto counts net carbs. European labels already show net carbs; United States labels show total carbs, so subtract the fiber yourself.',
    'Netto-Kohlenhydrate sind die Gesamt-Kohlenhydrate minus Ballaststoffe (und Zuckeralkohole). Ballaststoffe heben den Blutzucker nicht, deshalb zählt Keto die Netto-Kohlenhydrate. Europäische Etiketten zeigen bereits die Netto-Kohlenhydrate; in den USA stehen die Gesamt-Kohlenhydrate, dort musst du die Ballaststoffe selbst abziehen.')

# Q5
rep('<h3>What foods are high in fat for keto?</h3>', '<h3>Welche Lebensmittel sind bei Keto reich an Fett?</h3>')
rep('"name": "What foods are high in fat for keto?"', '"name": "Welche Lebensmittel sind bei Keto reich an Fett?"')
rep('Good keto fat sources include avocado, olive oil, coconut oil, butter, nuts and seeds, fatty fish like salmon, eggs, and full-fat cheese. These let you reach your fat target while keeping carbs low.',
    'Gute Fettquellen bei Keto sind Avocado, Olivenöl, Kokosöl, Butter, Nüsse und Samen, fetter Fisch wie Lachs, Eier und Vollfett-Käse. Damit erreichst du dein Fettziel und hältst die Kohlenhydrate niedrig.')

# Q6
rep('<h3>How fast will I lose weight on keto?</h3>', '<h3>Wie schnell nehme ich mit Keto ab?</h3>')
rep('"name": "How fast will I lose weight on keto?"', '"name": "Wie schnell nehme ich mit Keto ab?"')
rep('It depends on the calorie deficit you choose. A deficit that loses 0.5 to 1 kilogram per week is sustainable for most people. Expect a larger drop in the first week as your body sheds water weight, then a steadier loss after that.',
    'Das hängt vom gewählten Kaloriendefizit ab. Ein Defizit von 0,5 bis 1 Kilogramm pro Woche ist für die meisten gut durchzuhalten. In der ersten Woche fällt der Wert stärker, weil dein Körper Wasser verliert, danach geht es gleichmäßiger weiter.')

# Q7
rep('<h3>How does this keto calculator work?</h3>', '<h3>Wie funktioniert dieser Keto-Rechner?</h3>')
rep('"name": "How does this keto calculator work?"', '"name": "Wie funktioniert dieser Keto-Rechner?"')
rep('It estimates your Base Metabolic Rate with the Mifflin-St. Jeor formula, multiplies it by your activity level to get your daily energy needs, then subtracts your chosen deficit. Protein comes from your lean body mass and carbs from your chosen limit; the remaining calories become your fat target.',
    'Er schätzt deinen Grundumsatz mit der Mifflin-St.-Jeor-Formel, multipliziert ihn mit deinem Aktivitätsgrad zum Tagesbedarf und zieht dann dein gewähltes Defizit ab. Das Eiweiß ergibt sich aus deiner fettfreien Masse und die Kohlenhydrate aus deinem gewählten Limit; die restlichen Kalorien werden zu deinem Fettziel.')

# Q8
rep('<h3>Is this medical advice?</h3>', '<h3>Ist das eine medizinische Beratung?</h3>')
rep('"name": "Is this medical advice?"', '"name": "Ist das eine medizinische Beratung?"')
rep('No. This calculator provides general information to help you plan a ketogenic diet and is not a substitute for professional medical advice. It is designed for healthy adults who want to lose weight. If you are pregnant or breastfeeding, have type 1 diabetes, kidney disease, or a history of disordered eating, talk to your doctor before starting keto — the standard targets here may not be safe for you.',
    'Nein. Dieser Rechner bietet allgemeine Informationen zur Planung einer ketogenen Ernährung und ersetzt keine professionelle medizinische Beratung. Er ist für gesunde Erwachsene gedacht, die abnehmen möchten. Wenn du schwanger bist oder stillst, Typ-1-Diabetes oder eine Nierenerkrankung hast oder eine Essstörung hattest, sprich mit deinem Arzt, bevor du mit Keto beginnst — die Standardwerte hier sind dann möglicherweise nicht sicher für dich.')

# ---------------------------------------------------------------------------
# 6b. Guide links + "Keto Guides" section (the three guide pages are English;
#     the German page links to them and says so)
# ---------------------------------------------------------------------------
# Inline "read the full guide" links: the <a> versions cover BOTH the details
# blocks (with a trailing arrow) and the FAQ answers. They must run BEFORE the
# plain-text JSON-LD fragments below, so the leftover plain occurrences are
# unambiguous.
# details-block versions (trailing arrow inside the anchor)
rep('<a href="net-carbs-vs-total-carbs.html" onclick="return gatrack(this);">Read the full guide on net carbs vs total carbs &rarr;</a>',
    '<a href="/net-carbs-vs-total-carbs.html" onclick="return gatrack(this);">Zum ausführlichen Guide: Netto- vs. Gesamt-Kohlenhydrate (englisch) &rarr;</a>')
rep('<a href="how-much-protein-on-keto.html" onclick="return gatrack(this);">Read the full guide on how much protein to eat on keto &rarr;</a>',
    '<a href="/how-much-protein-on-keto.html" onclick="return gatrack(this);">Zum ausführlichen Guide: Wie viel Eiweiß bei Keto? (englisch) &rarr;</a>')
rep('<a href="how-fast-will-i-lose-weight-on-keto.html" onclick="return gatrack(this);">Read the full guide on how fast you lose weight on keto &rarr;</a>',
    '<a href="/how-fast-will-i-lose-weight-on-keto.html" onclick="return gatrack(this);">Zum ausführlichen Guide: Wie schnell nimmst du mit Keto ab? (englisch) &rarr;</a>')

# FAQ visible-answer versions (no arrow)
rep('<a href="net-carbs-vs-total-carbs.html" onclick="return gatrack(this);">Read the full guide on net carbs vs total carbs</a>',
    '<a href="/net-carbs-vs-total-carbs.html" onclick="return gatrack(this);">Zum ausführlichen Guide: Netto- vs. Gesamt-Kohlenhydrate (englisch)</a>')
rep('<a href="how-much-protein-on-keto.html" onclick="return gatrack(this);">Read the full guide on how much protein to eat on keto</a>',
    '<a href="/how-much-protein-on-keto.html" onclick="return gatrack(this);">Zum ausführlichen Guide: Wie viel Eiweiß bei Keto? (englisch)</a>')
rep('<a href="how-fast-will-i-lose-weight-on-keto.html" onclick="return gatrack(this);">Read the full guide on how fast you lose weight on keto</a>',
    '<a href="/how-fast-will-i-lose-weight-on-keto.html" onclick="return gatrack(this);">Zum ausführlichen Guide: Wie schnell nimmst du mit Keto ab? (englisch)</a>')

# JSON-LD plain-text fragments (after the link reps these only match the FAQPage schema)
rep(' Read the full guide on net carbs vs total carbs."',
    ' Mehr dazu im ausführlichen englischen Guide."')
rep(' Read the full guide on how much protein to eat on keto."',
    ' Mehr dazu im ausführlichen englischen Guide."')
rep(' Read the full guide on how fast you lose weight on keto."',
    ' Mehr dazu im ausführlichen englischen Guide."')

# Keto Guides section
rep('<h2>Keto Guides</h2>', '<h2>Keto-Guides</h2>')
rep('<p>Short, practical explainers for the questions this calculator raises most often.</p>',
    '<p>Kurze, praktische Erklärungen zu den Fragen, die dieser Rechner am häufigsten aufwirft. (Die Guides sind auf Englisch.)</p>')
rep('<a class="guide-title" href="net-carbs-vs-total-carbs.html" onclick="return gatrack(this);">Net Carbs vs Total Carbs</a>',
    '<a class="guide-title" href="/net-carbs-vs-total-carbs.html" onclick="return gatrack(this);">Netto- vs. Gesamt-Kohlenhydrate</a>')
rep('<span class="guide-desc">How to count the carbs that actually matter on keto — net carbs = total − fiber − most sugar alcohols — with worked examples and food-label tips.</span>',
    '<span class="guide-desc">Wie du die Kohlenhydrate zählst, die bei Keto wirklich zählen — netto = gesamt − Ballaststoffe − die meisten Zuckeralkohole — mit Beispielen und Etiketten-Tipps.</span>')
rep('<a class="guide-title" href="how-much-protein-on-keto.html" onclick="return gatrack(this);">How Much Protein on Keto</a>',
    '<a class="guide-title" href="/how-much-protein-on-keto.html" onclick="return gatrack(this);">Wie viel Eiweiß bei Keto</a>')
rep("<span class=\"guide-desc\">Why protein won't kick you out of ketosis, and how to set your daily target from your lean body mass.</span>",
    '<span class="guide-desc">Warum Eiweiß dich nicht aus der Ketose wirft und wie du dein Tagesziel aus deiner fettfreien Masse bestimmst.</span>')
rep('<a class="guide-title" href="how-fast-will-i-lose-weight-on-keto.html" onclick="return gatrack(this);">How Fast Will You Lose Weight on Keto</a>',
    '<a class="guide-title" href="/how-fast-will-i-lose-weight-on-keto.html" onclick="return gatrack(this);">Wie schnell nimmst du mit Keto ab</a>')
rep('<span class="guide-desc">Why the first week is mostly water, and how your calorie deficit sets the real fat-loss pace.</span>',
    '<span class="guide-desc">Warum die erste Woche vor allem Wasser ist und wie dein Kaloriendefizit das echte Abnehmtempo bestimmt.</span>')

# ---------------------------------------------------------------------------
# 7. Embed section / questions / comments / sidebar / about
# ---------------------------------------------------------------------------
rep('<h2>Embed This Calculator on Your Site</h2>', '<h2>Diesen Rechner auf deiner Website einbetten</h2>')
rep("<p>Run a keto blog, coaching site, or forum? You can embed this calculator for free —\n                        paste this snippet into your page and you're done. It always serves the latest version.</p>",
    '<p>Du betreibst einen Keto-Blog, eine Coaching-Seite oder ein Forum? Du kannst diesen Rechner kostenlos einbetten — füge einfach diesen Schnipsel in deine Seite ein, fertig. Es wird immer die aktuelle Version geladen.</p>')
rep('aria-label="HTML snippet to embed this calculator"', 'aria-label="HTML-Schnipsel zum Einbetten dieses Rechners"')
rep("<p style=\"font-size:smaller; color:#666;\">Please keep the credit link below the iframe — it's how new people find the calculator.</p>",
    '<p style="font-size:smaller; color:#666;">Bitte lass den Credit-Link unter dem iframe stehen — so finden neue Leute den Rechner.</p>')

rep('<h2>Got Questions?</h2>', '<h2>Noch Fragen?</h2>')
rep('<h3>Post Your Question to /r/keto</h3>', '<h3>Stell deine Frage auf /r/keto</h3>')
rep('<p>We can help you. <span class="redditsubmit"></span>, and replace the first text line with your question. Or click inside this field:</p>',
    '<p>Wir helfen dir gern. <span class="redditsubmit"></span> und ersetze die erste Textzeile durch deine Frage. Oder klick in dieses Feld:</p>')
rep('<p>Copy its text with Ctrl+C. <a href="https://www.reddit.com/r/keto/submit" onclick="return gatrack(this);">Go to /r/keto submit site</a>, move to the "text" field, paste it with Ctrl+V, and <strong>replace the first line with your question</strong>.</p>',
    '<p>Kopiere den Text mit Strg+C. <a href="https://www.reddit.com/r/keto/submit" onclick="return gatrack(this);">Geh zur /r/keto-Seite</a>, klick ins „text“-Feld, füge ihn mit Strg+V ein und <strong>ersetze die erste Zeile durch deine Frage</strong>.</p>')

rep('<h3>Comments</h3>', '<h3>Kommentare</h3>')
rep('<p>Is this calculator useful to you? Share your thoughts!</p>',
    '<p>Ist dieser Rechner für dich nützlich? Teile deine Gedanken!</p>')
rep('<noscript>Please enable JavaScript to view the comments.</noscript>',
    '<noscript>Bitte aktiviere JavaScript, um die Kommentare zu sehen.</noscript>')

rep('<i class="sprite sprite-me" style="float:left; margin-right: 1em; margin-top:4px;" title="Martin Leitner-Ankerl"></i> Created by <b>Martin Leitner-Ankerl</b>. I\'m a software developer who has followed and researched the ketogenic diet for years. I first built this calculator and <a href="https://www.reddit.com/r/keto/comments/127sm0/keto_calculator/" onclick="return gatrack(this);">announced it on /r/keto in October 2012</a>, because the keto advice online was vague and I wanted exact numbers for myself. The math is based on the peer-reviewed Mifflin-St. Jeor equation and the protein and fat guidance in Phinney and Volek\'s <i>The Art and Science of Low Carbohydrate Living</i> — the book I learned the most from. I\'m not a doctor or dietitian; this is simply the tool I wished existed, shared freely. You can find me on <a href="https://www.reddit.com/user/martinus/" onclick="return gatrack(this);">reddit</a> and <a href="https://martin.ankerl.com/" onclick="return gatrack(this);">my blog</a>. Please read the <a href="disclaimer.html" onclick="return gatrack(this);">disclaimer and Cookie Consent</a>.',
    '<i class="sprite sprite-me" style="float:left; margin-right: 1em; margin-top:4px;" title="Martin Leitner-Ankerl"></i> Erstellt von <b>Martin Leitner-Ankerl</b>. Ich bin Softwareentwickler und beschäftige mich seit Jahren mit der ketogenen Ernährung. Ich habe diesen Rechner gebaut und <a href="https://www.reddit.com/r/keto/comments/127sm0/keto_calculator/" onclick="return gatrack(this);">im Oktober 2012 auf /r/keto vorgestellt</a>, weil die Keto-Ratschläge im Netz vage waren und ich für mich selbst genaue Zahlen wollte. Die Berechnung basiert auf der wissenschaftlich geprüften Mifflin-St.-Jeor-Formel und den Eiweiß- und Fett-Empfehlungen aus Phinney und Voleks <i>The Art and Science of Low Carbohydrate Living</i> — dem Buch, aus dem ich am meisten gelernt habe. Ich bin kein Arzt und kein Ernährungsberater; das hier ist einfach das Werkzeug, das ich mir selbst gewünscht habe — frei geteilt. Du findest mich auf <a href="https://www.reddit.com/user/martinus/" onclick="return gatrack(this);">Reddit</a> und in <a href="https://martin.ankerl.com/" onclick="return gatrack(this);">meinem Blog</a>. Bitte lies den <a href="disclaimer.html" onclick="return gatrack(this);">Haftungsausschluss und die Cookie-Zustimmung</a>.')

# ---------------------------------------------------------------------------
# 8. JavaScript strings
# ---------------------------------------------------------------------------
# Created / last-reviewed line under the bio
rep('<p style="font-size:smaller; color:#6b7a86; margin-top:0.6em;">Created October 2012 · last reviewed June 2026. The formulas are unchanged since publication and are reviewed periodically for accuracy.</p>',
    '<p style="font-size:smaller; color:#6b7a86; margin-top:0.6em;">Erstellt im Oktober 2012 · zuletzt überprüft im Juni 2026. Die Formeln sind seit der Veröffentlichung unverändert und werden regelmäßig auf Richtigkeit überprüft.</p>')

# Food equivalents
rep('var berries = Math.max(1, Math.round(carbs_g / 12));',
    'var berries = Math.max(10, Math.round(carbs_g / 12 * 150 / 10) * 10);')
rep("var carbsTxt = '<span class=\"fe\">🫐</span>about <b>' + berries + ' cup' + (berries === 1 ? '' : 's') + '</b> of berries';",
    "var carbsTxt = '<span class=\"fe\">🫐</span>etwa <b>' + berries + ' g</b> Beeren';")
rep("carbsTxt += ', or <b>' + banana + '</b> banana' + (banana === 1 ? '' : 's');",
    "carbsTxt += ' oder <b>' + banana + '</b> Banane' + (banana === 1 ? '' : 'n');")
rep("update_by_name('protein_food', '<span class=\"fe\">🍗</span>about a <b>' + chicken + 'g</b> cooked chicken breast, or <b>' + tuna + '</b> can' + (tuna === 1 ? '' : 's') + ' of tuna');",
    "update_by_name('protein_food', '<span class=\"fe\">🍗</span>etwa eine <b>' + chicken + ' g</b> gegarte Hähnchenbrust oder <b>' + tuna + '</b> Dose' + (tuna === 1 ? '' : 'n') + ' Thunfisch');")
rep("update_by_name('fat_food', '<span class=\"fe\">🧈</span>about a <b>' + butter + 'g</b> block of butter, or <b>' + oil + ' tbsp</b> of olive oil');",
    "update_by_name('fat_food', '<span class=\"fe\">🧈</span>etwa <b>' + butter + ' g</b> Butter oder <b>' + oil + ' EL</b> Olivenöl');")

# deficit_levels messages
rep('"You will gain weight."', '"Du wirst zunehmen."')
rep('"Zero deficit: you will maintain your current weight."', '"Kein Defizit: Du hältst dein aktuelles Gewicht."')
rep('"Very little deficit. Choose a higher deficit to lose faster."', '"Sehr kleines Defizit. Wähle ein höheres Defizit, um schneller abzunehmen."')
rep('"Small deficit: best for athletes who are already lean."', '"Kleines Defizit: am besten für Sportler, die bereits schlank sind."')
rep('"Average deficit. Easily sustainable, a good choice to start with."', '"Durchschnittliches Defizit. Gut durchzuhalten, eine gute Wahl für den Anfang."')
rep('"Moderate deficit: fast weight loss with moderate difficulty."', '"Moderates Defizit: schnelles Abnehmen bei mäßigem Aufwand."')
rep('"Large deficit: this is hard, give it a try for two weeks."', '"Großes Defizit: das ist hart, probier es zwei Wochen lang aus."')
rep('"Very large deficit. Hard to sustain — try a 20% deficit if you struggle."', '"Sehr großes Defizit. Schwer durchzuhalten — nimm ein 20%-Defizit, wenn es dir zu schwer fällt."')
rep('"Severe deficit: are you sure? Try a 20% deficit if you fail."', '"Sehr hartes Defizit: bist du sicher? Nimm ein 20%-Defizit, wenn du scheiterst."')
rep('"Enormous deficit, extremely hard. Start with 20% if you are unsure."', '"Enormes Defizit, extrem hart. Starte mit 20%, wenn du unsicher bist."')

# warnings
rep('"WARNING: Your body fat percentage is too low!"', '"WARNUNG: Dein Körperfettanteil ist zu niedrig!"')
rep('"WARNING: Too low! You will lose muscles."', '"WARNUNG: Zu niedrig! Du verlierst Muskeln."')
rep('"WARNING: Are you a dwarf?<br /> You are shorter than <a href=\\"https://en.wikipedia.org/wiki/Chandra_Bahadur_Dangi\\">Chandra Bahadur Dangi</a>, the smallest human ever recorded!<br />Check your size!<br /><span class=\\"book\\"><img width=\\"190\\" height=\\"244\\" src=\\"height_warning_short.jpg\\" alt=\\"Funny warning illustration about being unusually short\\" /></span>"',
    '"WARNUNG: Bist du ein Zwerg?<br /> Du bist kleiner als <a href=\\"https://en.wikipedia.org/wiki/Chandra_Bahadur_Dangi\\">Chandra Bahadur Dangi</a>, der kleinste je gemessene Mensch!<br />Prüf deine Größe!<br /><span class=\\"book\\"><img width=\\"190\\" height=\\"244\\" src=\\"height_warning_short.jpg\\" alt=\\"Lustige Warn-Illustration zu ungewöhnlich kleiner Größe\\" /></span>"')
rep('"WARNING: Are you a giant?<br /> You are taller than <a href=\\"https://en.wikipedia.org/wiki/Robert_Wadlow\\">Robert Wadlow</a>, the tallest human ever recorded!<br />Check your size!<br /><span class=\\"book\\"><img width=\\"190\\" height=\\"325\\" src=\\"height_warning_tall.jpg\\" alt=\\"Funny warning illustration about being unusually tall\\" /></span>"',
    '"WARNUNG: Bist du ein Riese?<br /> Du bist größer als <a href=\\"https://en.wikipedia.org/wiki/Robert_Wadlow\\">Robert Wadlow</a>, der größte je gemessene Mensch!<br />Prüf deine Größe!<br /><span class=\\"book\\"><img width=\\"190\\" height=\\"325\\" src=\\"height_warning_tall.jpg\\" alt=\\"Lustige Warn-Illustration zu ungewöhnlich großer Größe\\" /></span>"')
rep('"WARNING: Are you an elf?<br /> Your body weight is extremely low!<br /> Check your numbers!"',
    '"WARNUNG: Bist du ein Elf?<br /> Dein Körpergewicht ist extrem niedrig!<br /> Prüf deine Zahlen!"')
rep('"WARNING: Are you sure you entered the correct weight?<br /> You are heavier than <a href=\\"https://en.wikipedia.org/wiki/Jon_Brower_Minnoch\\">Jon Brower Minnoch</a>, the heaviest human ever recorded!<br />Check your numbers!<br /><span class=\\"book\\"><img width=\\"190\\" height=\\"244\\" src=\\"weight_warning_high.jpg\\" alt=\\"Funny warning illustration about an unusually high weight\\" /></span>"',
    '"WARNUNG: Hast du das Gewicht richtig eingegeben?<br /> Du bist schwerer als <a href=\\"https://en.wikipedia.org/wiki/Jon_Brower_Minnoch\\">Jon Brower Minnoch</a>, der schwerste je gemessene Mensch!<br />Prüf deine Zahlen!<br /><span class=\\"book\\"><img width=\\"190\\" height=\\"244\\" src=\\"weight_warning_high.jpg\\" alt=\\"Lustige Warn-Illustration zu ungewöhnlich hohem Gewicht\\" /></span>"')
rep('"WARNING: protein too low!"', '"WARNUNG: Eiweiß zu niedrig!"')
rep('"WARNING: protein too high!<br /><span class=\\"book\\"><img width=\\"190\\" height=\\"227\\" src=\\"proteintoohigh_small.jpg\\" alt=\\"Warning illustration: protein intake too high\\" /></span>"',
    '"WARNUNG: Eiweiß zu hoch!<br /><span class=\\"book\\"><img width=\\"190\\" height=\\"227\\" src=\\"proteintoohigh_small.jpg\\" alt=\\"Warn-Illustration: Eiweißzufuhr zu hoch\\" /></span>"')

rep('"At under 15 years old it is not advised to be on a ketogenic diet without professional supervision. If you are overweight at that age, it is an excellent idea to change eating habits, but tracking can be problematic. You are still growing and developing, plus there is puberty! These are all things that an online calculator can not take into account.<br/><b>Please go see a doctor!</b>"',
    '"Unter 15 Jahren ist eine ketogene Ernährung ohne fachliche Begleitung nicht ratsam. Wenn du in dem Alter übergewichtig bist, ist es eine sehr gute Idee, die Essgewohnheiten zu ändern — das Tracken kann aber problematisch sein. Du wächst und entwickelst dich noch, dazu kommt die Pubertät! Das alles kann ein Online-Rechner nicht berücksichtigen.<br/><b>Bitte geh zu einem Arzt!</b>"')
rep('"You are under 18, at this age it is recommended to stay above "', '"Du bist unter 18; in diesem Alter wird empfohlen, über "')
rep('"1800 kcal for a girl."', '"1800 kcal für ein Mädchen zu bleiben."')
rep('"2000 kcal for a boy."', '"2000 kcal für einen Jungen zu bleiben."')
rep('" See the <a href=\\"https://www.nhlbi.nih.gov/health/educational/wecan/downloads/calreqtips.pdf\\">PDF from the National Insitutes of Health</a> for more info!"',
    '" Mehr Infos im <a href=\\"https://www.nhlbi.nih.gov/health/educational/wecan/downloads/calreqtips.pdf\\">PDF der National Institutes of Health</a>!"')

# reddit post string
rep('var str = "Replace this line with your question\\n"', 'var str = "Ersetze diese Zeile durch deine Frage\\n"')
rep('str += "*Generated by [Keto Calculator](https://keto-calculator.ankerl.com) " + version + "*" + nl + nl;',
    'str += "*Erstellt mit [Keto-Rechner](https://keto-calculator.ankerl.com/de/) " + version + "*" + nl + nl;')
rep('str += "* " + Math.round(target_kcal) + " kcal Goal, a " + Math.round(target_deficit) + "% deficit. (" + Math.round(kcal_min) + " min, " + Math.round(expenditure) + " max)"+ nl;',
    'str += "* " + Math.round(target_kcal) + " kcal Ziel, ein " + Math.round(target_deficit) + "% Defizit. (" + Math.round(kcal_min) + " min, " + Math.round(expenditure) + " max)"+ nl;')
rep('str += "* " + carbs_g + "g Carbohydrates" + nl;', 'str += "* " + carbs_g + "g Kohlenhydrate" + nl;')
rep('str += "* " + protein_g + "g Protein (" + d.protein_min.value + "g min, " + d.protein_max.value + "g max)" + nl;',
    'str += "* " + protein_g + "g Eiweiß (" + d.protein_min.value + "g min, " + d.protein_max.value + "g max)" + nl;')
rep('str += "* " + Math.round(fat_g) + "g Fat (" + fat_g_min + "g min, " + Math.floor(fat_g_max) + "g max)" + nl;',
    'str += "* " + Math.round(fat_g) + "g Fett (" + fat_g_min + "g min, " + Math.floor(fat_g_max) + "g max)" + nl;')
rep('0: "Mostly sedentary",', '0: "Überwiegend sitzend",')
rep('1: "Lightly active",', '1: "Leicht aktiv",')
rep('2: "Moderately active",', '2: "Mäßig aktiv",')
rep('3: "Very active",', '3: "Sehr aktiv",')
rep('4: "Custom expenditure: "', '4: "Eigener Verbrauch: "')

# share feedback
rep("fb.textContent = ' Link copied to clipboard!';", "fb.textContent = ' Link in die Zwischenablage kopiert!';")
rep("window.prompt('Copy your shareable link:', url);", "window.prompt('Kopiere deinen Teilen-Link:', url);")

# ---------------------------------------------------------------------------
# 9. Date localization (TT.MM.JJJJ) + datepicker German locale
# ---------------------------------------------------------------------------
rep('''function calcAge(dateString) {
		  var birthday = +new Date(dateString);
		  // 24 * 3600 * 365.242 * 1000
		  return (Date.now() - birthday) / 31556908800.0;
		}''',
    '''function de_date(s) {
		  // German date format dd.mm.yyyy
		  var p = String(s).split('.');
		  return (p.length === 3) ? new Date(p[2], p[1] - 1, p[0]) : new Date(s);
		}
		function calcAge(dateString) {
		  var birthday = +de_date(dateString);
		  // 24 * 3600 * 365.242 * 1000
		  return (Date.now() - birthday) / 31556908800.0;
		}''')

rep('new Date(graphstartdate)', 'de_date(graphstartdate)')

rep('d.graphstartdate.value = (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear() ;',
    'd.graphstartdate.value = date.getDate() + "." + (date.getMonth()+1) + "." + date.getFullYear() ;')

rep('format: "mm/dd/yyyy",', 'format: "dd.mm.yyyy",\n\t\t\tlanguage: "de",')

rep('''		 // set datepicker's *after* loading, so that field keeps beeing there.
		$('#bday').datepicker({''',
    '''		$.fn.datepicker.dates['de'] = {
			days: ["Sonntag","Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag"],
			daysShort: ["So","Mo","Di","Mi","Do","Fr","Sa"],
			daysMin: ["So","Mo","Di","Mi","Do","Fr","Sa"],
			months: ["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"],
			monthsShort: ["Jan","Feb","Mär","Apr","Mai","Jun","Jul","Aug","Sep","Okt","Nov","Dez"],
			today: "Heute", clear: "Löschen", weekStart: 1
		};
		 // set datepicker's *after* loading, so that field keeps beeing there.
		$('#bday').datepicker({''')

# ---------------------------------------------------------------------------
# 10. Comments (Cusdis): separate German comment thread
# ---------------------------------------------------------------------------
rep('data-page-id="/"', 'data-page-id="/de/"')
rep('data-page-url="https://keto-calculator.ankerl.com/"', 'data-page-url="https://keto-calculator.ankerl.com/de/"')
# data-page-title="Keto Calculator" is localized by the blanket rep below.

# Brand mentions left in plain content (after the specific reps above)
rep('Keto Calculator', 'Keto-Rechner')

# ---------------------------------------------------------------------------
# 11. Asset paths: make root-absolute so they resolve from the /de/ subfolder
#     (relative paths like "logo-white-150.png" would 404 as /de/logo-white-150.png).
# ---------------------------------------------------------------------------
rep('href="favicon.png"', 'href="/favicon.png"')
rep('href="launcher-icon-152x152.png"', 'href="/launcher-icon-152x152.png"')
rep('href="manifest.json"', 'href="/manifest.json"')
rep('href="logo-white-150.png"', 'href="/logo-white-150.png"')   # LCP preload
rep('src="logo-white-150.png"', 'src="/logo-white-150.png"')     # header logo
rep('src="books/', 'src="/books/')                               # 14 affiliate covers
rep('url(fonts/', 'url(/fonts/')                                 # glyphicons webfont
rep('url(spritesheet.png)', 'url(/spritesheet.png)')             # share/me sprite icons
rep('height_warning_short.jpg', '/height_warning_short.jpg')     # JS warning images
rep('height_warning_tall.jpg', '/height_warning_tall.jpg')
rep('weight_warning_high.jpg', '/weight_warning_high.jpg')
rep('proteintoohigh_small.jpg', '/proteintoohigh_small.jpg')

# ---------------------------------------------------------------------------
# write
# ---------------------------------------------------------------------------
os.makedirs(HERE, exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)

if missing:
    print("WARNING: %d source snippet(s) NOT FOUND in index.html." % len(missing))
    print("The English text probably changed. Update the matching German entry and re-run.\n")
    for m in missing:
        preview = m[:90].replace("\n", " ")
        print("  NOT FOUND: " + preview)
    sys.exit(1)

print("OK: wrote de/index.html (%d bytes)." % len(html))

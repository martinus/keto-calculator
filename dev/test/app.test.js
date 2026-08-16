// The calculator itself: does it compute the right numbers, does a shared link
// reproduce them, and does it survive a URL that has been mangled in transit.
//
// Each block here corresponds to something that was actually broken. Keep them.

const { Page, THIRD_PARTY, suite } = require('./lib');

// A complete, realistic entry: 40-year-old man, 80 kg, 180 cm, sedentary,
// 20% body fat, 25 g carbs, 110 g protein, 20% deficit.
const PERSON = { sex: '0', kg: '80', height: '180', bday: '1986-08-01', level: '0',
                 bodyfat: '20', carbs: '25', protein_chosen: '110', target_deficit_form: '20' };

async function fillForm(page, person = PERSON) {
  await page.pick('sex', person.sex);
  await page.pick('level', person.level);
  for (const k of ['kg', 'height', 'bday', 'bodyfat', 'carbs', 'protein_chosen', 'target_deficit_form']) {
    await page.set(k, person[k]);
  }
  // The expensive half of a recalculation is debounced by 500ms; wait for the
  // figure itself rather than guessing how long that takes.
  await page.waitFor(`(document.querySelector('.target_kcal') || {}).textContent || null`,
    { what: 'kcal target to appear' });
}

const kcal = `(document.querySelector('.target_kcal') || {}).textContent`;

module.exports = async function run(base) {
  const t = suite('app');

  // --- console health ---------------------------------------------------
  t.section('console is clean on every deployed page');
  for (const p of ['/', '/de/', '/net-carbs-vs-total-carbs.html', '/how-much-protein-on-keto.html',
                   '/how-fast-will-i-lose-weight-on-keto.html', '/disclaimer.html', '/embed.html']) {
    const page = await Page.open(base + p, { block: THIRD_PARTY });
    await page.scrollThrough();
    const noise = page.realLogs();
    t.check(p, noise.length === 0, noise.slice(0, 2).join(' | ') || 'clean');
    await page.close();
  }

  // --- the maths --------------------------------------------------------
  t.section('calculator: 80kg / 180cm / male / 40y / sedentary / 20% bf');
  {
    const page = await Page.open(base + '/', { block: THIRD_PARTY });
    await fillForm(page);
    const r = await page.eval(`({
      bmr: document.data.bmr.value, energy: document.data.energy.value,
      lbs: document.data.lbs.value, feet: document.data.feet.value, inch: document.data.inch.value,
      pmin: document.data.protein_min.value, pmax: document.data.protein_max.value,
      carbs: (document.querySelector('.carbs') || {}).textContent
    })`);

    // Mifflin-St Jeor, original (unrounded) coefficients.
    const bmr = Math.round(9.99 * 80 + 6.25 * 180 - 4.92 * 40 + 5);
    t.check('BMR matches Mifflin-St Jeor', Math.abs(+r.bmr - bmr) <= 1, r.bmr + ' vs ' + bmr);
    t.check('TDEE = BMR x 1.1 (sedentary)', Math.abs(+r.energy - Math.round(bmr * 1.1)) <= 1,
      r.energy + ' vs ' + Math.round(bmr * 1.1));
    // abbrNum() is 3 significant digits by design, so 176 and not 176.37.
    t.check('80 kg -> 176 lbs', +r.lbs === 176, r.lbs);
    t.check('180 cm -> 5ft 11in', r.feet === '5' && r.inch === '11', r.feet + 'ft ' + r.inch + 'in');
    // Protein bounds run off lean mass (64 kg), 0.6-1.0 g per lb of it.
    t.check('protein min = ceil(64 * 0.6/0.45359237)',
      +r.pmin === Math.ceil(64 * 0.6 / 0.45359237), r.pmin);
    t.check('protein max = floor(64 * 1.0/0.45359237)',
      +r.pmax === Math.floor(64 * 1.0 / 0.45359237), r.pmax);
    t.check('carbs figure echoes the entered 25 g', (r.carbs || '').indexOf('25') !== -1, r.carbs);
    await page.close();
  }

  // --- height conversion -------------------------------------------------
  // Inches used to be rounded inside an already-fixed foot, so every foot mark
  // had a ~0.3cm band that rendered "5 ft 12 in".
  t.section('height conversion at foot boundaries');
  {
    const page = await Page.open(base + '/', { block: THIRD_PARTY });
    for (const [cm, expect] of [['182.8', '6ft 0in'], ['152.3', '5ft 0in'],
                                ['175', '5ft 9in'], ['183', '6ft 0in']]) {
      await page.set('height', cm);
      const got = await page.waitFor(
        `(function () { var d = document.data;
           return d.feet.value !== '' ? d.feet.value + 'ft ' + d.inch.value + 'in' : null; })()`,
        { what: 'imperial height for ' + cm });
      t.check(cm + ' cm -> ' + expect, got === expect, got);
    }
    await page.set('height', '');
    const cleared = await page.waitFor(
      `(function () { var d = document.data;
         return (d.feet.value === '' && d.inch.value === '') ? 'cleared' : null; })()`,
      { what: 'feet/inch to clear' }).catch(() => 'still set');
    t.check('clearing cm also clears feet/inch', cleared === 'cleared', cleared);
    await page.close();
  }

  // --- the /r/keto copy-paste box ---------------------------------------
  // This box is public-facing: people paste it into a subreddit that sends this
  // site real traffic. It used to offer NaN and undefined before the form was
  // complete.
  t.section('/r/keto copy-paste box');
  {
    const page = await Page.open(base + '/', { block: THIRD_PARTY });
    const empty = await page.eval('document.data.reddit_copypaste.value');
    t.check('incomplete form: nothing NaN/undefined offered for pasting',
      !/NaN|undefined/.test(empty), JSON.stringify(empty.slice(0, 60)));
    t.check('incomplete form: submit link hidden',
      (await page.eval(`(document.querySelector('.reddit-cta') || {}).hidden`)) === true);

    await fillForm(page);
    // Wait on the state, not the wording: a reworded sentence should fail a
    // check, not time out the whole suite with no clue why.
    const done = await page.waitFor(
      `document.data.reddit_copypaste.value.indexOf('|') > -1
         ? document.data.reddit_copypaste.value : null`, { what: 'reddit post text' });
    t.check('complete form: real post text, still no NaN', !/NaN|undefined/.test(done),
      JSON.stringify((done.split('\n').filter(Boolean)[3] || '').slice(0, 50)));

    // The macro table is the part a reader sees. Markdown needs the header
    // separator row, and the columns are padded so the raw text lines up in
    // the textarea too -- so every table row is the same length.
    const rows = done.split('\n').filter(l => l.indexOf('|') === 0);
    t.check('post carries a markdown table with a separator row',
      rows.length === 5 && /^\|:-+\|-+:\|-+:\|$/.test(rows[1]), rows[1]);
    t.check('table columns are padded to equal width',
      rows.every(l => l.length === rows[0].length), rows.map(l => l.length).join(','));

    // A question line that markdown would swallow as a setext heading, or a
    // post without the share link, both defeat the point of the box.
    t.check('blank line between the question and the rule',
      /\n\n---\n/.test(done));
    const share = (done.match(/\]\((https?:\/\/[^)]*\?[^)]*)\)/) || [])[1];
    t.check('post links back with the poster\'s own numbers prefilled',
      !!share && share.indexOf('kg=' + PERSON.kg) > -1
        && share.indexOf('bodyfat=' + PERSON.bodyfat) > -1, (share || '').slice(-40));

    const cta = await page.eval(`(function () {
      var a = document.getElementById('redditsubmit');
      return a ? { href: a.getAttribute('href'), rel: a.rel, cls: a.className,
                   shown: !a.parentNode.hidden } : null; })()`);
    t.check('submit link is https with a prefilled body',
      !!cta && cta.href.indexOf('https://www.reddit.com/r/keto/submit?text=') === 0,
      (cta && cta.href || '').slice(0, 44));
    t.check('submit link has rel=noopener', !!cta && cta.rel === 'noopener');
    // Reddit drops absurdly long prefills; the post plus its share URL has to
    // stay comfortably inside what a browser will send.
    t.check('prefilled submit URL stays under 4k',
      !!cta && cta.href.length < 4000, (cta && cta.href || '').length + ' chars');
    t.check('submit link is presented as the primary action',
      !!cta && cta.shown && /\bbtn-cta\b/.test(cta.cls), cta && cta.cls);
    await page.close();
  }

  // Body fat is optional on the form, so everything else can be filled while
  // kcal_min and fat_g_min are NaN. The post used to go out saying
  // "fat NaN-199 g - never below NaN kcal".
  {
    const page = await Page.open(base + '/', { block: THIRD_PARTY });
    await fillForm(page);
    await page.waitFor(`document.data.reddit_copypaste.value.indexOf('|') > -1 ? 'ready' : null`,
      { what: 'a complete post first' });
    await page.set('bodyfat', '');
    const partial = await page.waitFor(
      `document.data.reddit_copypaste.value.indexOf('|') === -1
         ? document.data.reddit_copypaste.value : null`,
      { what: 'the post to withdraw itself' }).catch(e => 'still offered: ' + e.message);
    t.check('body fat cleared: no NaN offered for pasting',
      !/NaN|undefined/.test(partial), JSON.stringify(String(partial).slice(0, 60)));
    t.check('body fat cleared: submit link goes back into hiding',
      (await page.eval(`(document.querySelector('.reddit-cta') || {}).hidden`)) === true);
    await page.close();
  }

  // --- share links -------------------------------------------------------
  // CLAUDE.md: load_url_params() "must keep working". The URL used to carry all
  // three mutually-derived targets, so the recipient picked a different driver
  // than the sender used and recomputed from a rounded gram figure: 1525 kcal
  // arrived as 1521.
  t.section('share URL roundtrip');
  {
    const sender = await Page.open(base + '/', { block: THIRD_PARTY });
    await fillForm(sender);
    const sent = await sender.eval(kcal);
    const url = await sender.eval('build_share_url()');
    await sender.close();

    const recipient = await Page.open(url, { block: THIRD_PARTY });
    const got = await recipient.waitFor(`${kcal} || null`, { what: 'recipient kcal' });
    t.check('recipient sees exactly the sender kcal', !!sent && sent === got, sent + ' -> ' + got);
    t.check('share URL carries one target, not three',
      (url.match(/target_/g) || []).length === 1, url.slice(url.indexOf('?')).slice(0, 90));
    t.check('query string is cleaned out of the URL bar',
      (await recipient.eval('location.search')) === '');
    await recipient.close();
  }

  t.section('links shared before that change still resolve');
  {
    // Pre-change format: all three targets present.
    const legacy = base + '/?sex=0&kg=80&height=180&bday=1986-08-01&bodyfat=20&level=0'
      + '&custom_expenditure=1905&carbs=25&protein_chosen=110'
      + '&target_deficit_form=20&target_fat_form=109&target_kcal_form=1525';
    const page = await Page.open(legacy, { block: THIRD_PARTY });
    const got = await page.waitFor(`${kcal} || null`, { what: 'legacy kcal' });
    t.check('legacy link loads without error',
      page.logs.filter(l => l.startsWith('EXCEPTION')).length === 0);
    t.check('legacy link reproduces the sender kcal', got === '1525', got);
    await page.close();
  }

  // --- mangled URLs ------------------------------------------------------
  // Chat clients trim links and forums escape them. A stray '%' made
  // decodeURIComponent throw out of a top-level init script, so saved settings
  // never loaded and the required-field cues never appeared.
  t.section('mangled share URLs must not break the page');
  for (const q of ['?carbs=100%', '?kg', '?%E0%A4%A=1', '?carbs=25&bogus', '?=1&&carbs=25']) {
    const page = await Page.open(base + '/' + q, { block: THIRD_PARTY });
    const thrown = page.logs.filter(l => l.startsWith('EXCEPTION'));
    t.check(q + ': no uncaught exception', thrown.length === 0, thrown[0] || 'clean');
    t.check(q + ': required-field cues still applied',
      (await page.eval(`document.querySelectorAll('.needs-input').length`)) > 0);
    // A parameter with no '=' used to yield the literal string "undefined".
    const junk = await page.eval(`(function () {
      var out = [], f = document.data;
      for (var i = 0; i < f.length; ++i) {
        if (String(f[i].value).indexOf('undefined') !== -1) out.push(f[i].name);
      }
      return out;
    })()`);
    t.check(q + ': no field filled with the string "undefined"', junk.length === 0, JSON.stringify(junk));
    await page.close();
  }

  return t.results;
};

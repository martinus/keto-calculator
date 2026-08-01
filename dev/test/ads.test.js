// Ad slot behaviour: what gets requested, when, and into which box.
//
// Every unit on this site is lazy: the markup holds an empty
// <div data-ad-lazy="<slot>"> and the loader creates the <ins> and pushes it
// when the slot nears the viewport. Two things can go wrong and both cost real
// money, so both are pinned here:
//
//   1. A slot requested where nobody can see it. The sidebar is display:none
//      under 830px, and AdSense fills a *fixed-size* unit regardless of
//      container visibility — that shipped once and served 214 mobile
//      impressions/week at exactly 0% Active View viewable.
//   2. A creative landing in the wrong box. adsbygoogle.push({}) binds to the
//      next *uninitialised* <ins> in document order, so on scroll (where order
//      is whatever the reader does) a naive implementation puts one slot's ad
//      in another slot's space.

const { Page, THIRD_PARTY, suite } = require('./lib');

// Stands in for adsbygoogle: records each push and binds it the way the real
// library does — to the next <ins> in document order that has not been claimed.
const ADSENSE_STUB = `
  window.__pushes = [];
  window.adsbygoogle = [];
  window.adsbygoogle.loaded = true;
  window.adsbygoogle.push = function () {
    var all = document.querySelectorAll('ins.adsbygoogle');
    for (var i = 0; i < all.length; ++i) {
      if (!all[i].hasAttribute('data-ad-status')) {
        all[i].setAttribute('data-ad-status', 'filled');
        window.__pushes.push({
          boundSlot: all[i].getAttribute('data-ad-slot'),
          boxSlot: all[i].parentNode.getAttribute('data-ad-lazy'),
          style: all[i].getAttribute('style'),
        });
        return all.length;
      }
    }
    window.__pushes.push({ error: 'push with no free <ins>' });
    return all.length;
  };
`;

const PROBE = `(function () {
  return {
    pushes: window.__pushes || [],
    boxes: [].map.call(document.querySelectorAll('[data-ad-lazy]'), function (b) {
      var ins = b.querySelector('ins.adsbygoogle');
      return {
        slot: b.getAttribute('data-ad-lazy'),
        requested: b.getAttribute('data-ad-done') === '1',
        insSlot: ins ? ins.getAttribute('data-ad-slot') : null
      };
    })
  };
})()`;

async function visit(base, path, width, height, stub) {
  const page = await Page.open(base + path, { width, height, block: THIRD_PARTY, stub });
  const atLoad = await page.eval(PROBE);
  await page.scrollThrough(Math.floor(height * 0.8));
  const afterScroll = await page.eval(PROBE);
  return { page, atLoad, afterScroll };
}

const requested = r => r.afterScroll.boxes.filter(b => b.requested).map(b => b.slot).sort();
const misbound = r => r.afterScroll.pushes.filter(p => p.error || p.boundSlot !== p.boxSlot);
const boxesOk = r => r.afterScroll.boxes.filter(b => b.requested).every(b => b.insSlot === b.slot);

module.exports = async function run(base) {
  const t = suite('ads');

  // --- phone -----------------------------------------------------------
  t.section('index.html @ 390px (phone)');
  {
    const r = await visit(base, '/', 390, 844, ADSENSE_STUB);
    t.check('nothing requested at page load',
      r.atLoad.boxes.every(b => !b.requested), JSON.stringify(requested(r)));
    t.check('sidebar 8747974681 never requested (display:none under 830px)',
      !requested(r).includes('8747974681'), 'requested: ' + JSON.stringify(requested(r)));
    t.check('both in-content units requested after scrolling',
      requested(r).includes('1224707884') && requested(r).includes('7271241487'),
      JSON.stringify(requested(r)));
    t.check('every <ins> landed in its own box',
      boxesOk(r) && misbound(r).length === 0,
      JSON.stringify(r.afterScroll.pushes.map(p => p.boundSlot + '->' + p.boxSlot)));
    await r.page.close();
  }

  // --- desktop ---------------------------------------------------------
  t.section('index.html @ 1280px (desktop)');
  {
    const r = await visit(base, '/', 1280, 900, ADSENSE_STUB);
    t.check('sidebar 8747974681 is requested (visible here)',
      requested(r).includes('8747974681'), JSON.stringify(requested(r)));
    t.check('all three units requested', requested(r).length === 3, JSON.stringify(requested(r)));
    // The sidebar is sticky at the top, so on desktop it pushes BEFORE the two
    // in-content units — the out-of-order case that mis-binds slots if the
    // <ins> elements are static in the markup. This is the important one.
    t.check('every <ins> landed in its own box, despite the sidebar pushing first',
      boxesOk(r) && misbound(r).length === 0,
      JSON.stringify(r.afterScroll.pushes.map(p => p.boundSlot + '->' + p.boxSlot)));

    const side = r.afterScroll.pushes.find(p => p.boxSlot === '8747974681');
    t.check('sidebar kept its fixed 160x600',
      !!side && /width:\s*160px/.test(side.style) && /height:\s*600px/.test(side.style),
      side && side.style);
    const inline = r.afterScroll.pushes.filter(p => p.boxSlot && p.boxSlot !== '8747974681');
    t.check('in-content units are responsive display:block',
      inline.length === 2 && inline.every(p => /display:\s*block/.test(p.style)),
      JSON.stringify(inline.map(p => p.style)));
    await r.page.close();
  }

  // --- inherited pages --------------------------------------------------
  t.section('generated pages inherit the loader');
  for (const [path, expect] of [['/de/', 2], ['/net-carbs-vs-total-carbs.html', 1]]) {
    const r = await visit(base, path, 390, 844, ADSENSE_STUB);
    t.check(path + ': nothing requested at load',
      r.atLoad.boxes.every(b => !b.requested));
    t.check(path + ': ' + expect + ' unit(s) requested after scrolling',
      requested(r).length === expect, JSON.stringify(requested(r)));
    t.check(path + ': every <ins> in its own box', boxesOk(r) && misbound(r).length === 0);
    await r.page.close();
  }

  t.section('embed.html ships ad-free');
  {
    const page = await Page.open(base + '/embed.html', { width: 390, height: 844, block: THIRD_PARTY });
    const html = await page.eval('document.documentElement.outerHTML');
    t.check('no ad slots', html.indexOf('data-ad-lazy') === -1);
    t.check('no ad code', html.indexOf('adsbygoogle') === -1);
    await page.close();
  }

  // --- ad script blocked entirely ---------------------------------------
  // No stub and pagead2 blocked: the loader must give the reserved space back
  // instead of leaving a hole. Regression guard — collapsing the container
  // alone once left the injected sidebar <ins> at its inline 600px.
  t.section('ad script blocked (ad blocker / consent denied)');
  for (const [width, height, label] of [[390, 844, 'phone'], [1280, 900, 'desktop']]) {
    const page = await Page.open(base + '/', { width, height, block: THIRD_PARTY });
    const boxes = await page.waitFor(`(function () {
      var out = [].map.call(document.querySelectorAll('[data-ad-lazy]'), function (b) {
        return { slot: b.getAttribute('data-ad-lazy'),
                 collapsed: b.classList.contains('ad-collapsed'),
                 height: Math.round(b.getBoundingClientRect().height) };
      });
      return out.every(function (b) { return b.collapsed; }) ? out : null;
    })()`, { timeout: 15000, what: 'slots to collapse' });
    t.check(label + ': every reserved slot collapsed to 0px',
      boxes.every(b => b.height === 0), JSON.stringify(boxes));
    await page.close();
  }

  return t.results;
};

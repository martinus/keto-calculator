// Measures time-to-reveal for pages carrying Google Optimize's anti-flicker
// snippet, under three visitor setups. Companion to
// dev/docs/plan-anti-flicker-research.md (Tier 2).
//
//   node measure-reveal.js https://example.com [more urls...]
//
// Needs: npm i playwright (or playwright-core + a Chromium executablePath).
// Scenarios per URL:
//   clean    – nothing blocked (whatever Google serves today)
//   blocked  – google-analytics/googletagmanager/googleoptimize requests fail,
//              no stub: simulates Firefox strict ETP / Safari content blockers /
//              Pi-hole / AdGuard DNS
//   stubbed  – analytics.js answered by a uBlock-style stub that calls
//              dataLayer.hide.end() immediately
//
// A page WITHOUT the snippet reports "no async-hide" and is skipped.

const { chromium } = require('playwright');

const GOOGLE_HOSTS = /google-analytics\.com|googletagmanager\.com|googleoptimize\.com/;
const STUB = 'try{var dl=window.dataLayer;dl&&dl.hide&&typeof dl.hide.end==="function"&&dl.hide.end();}catch(e){}';

async function measure(browser, url, mode) {
  const page = await browser.newPage();
  try {
    if (mode !== 'clean') {
      await page.route(GOOGLE_HOSTS, route => {
        if (mode === 'stubbed' && route.request().url().includes('analytics.js')) {
          return route.fulfill({ contentType: 'application/javascript', body: STUB });
        }
        return route.abort();
      });
    }
    await page.goto(url, { waitUntil: 'commit', timeout: 30000 });
    // Times are ms since navigation start (performance.now()'s epoch).
    const result = await page.evaluate(() => new Promise(resolve => {
      let sawHide = false;
      const tick = () => {
        const now = performance.now();
        const hidden = /async-hide/.test(document.documentElement.className || '');
        if (hidden) {
          sawHide = true;
          if (now > 10000) return resolve({ hadSnippet: true, revealMs: null }); // stuck
        } else if (sawHide) {
          return resolve({ hadSnippet: true, revealMs: Math.round(now) }); // revealed
        } else if (now > 2500) {
          return resolve({ hadSnippet: false, revealMs: null }); // snippet never ran
        }
        setTimeout(tick, 10);
      };
      tick();
    }));
    return result;
  } finally {
    await page.close();
  }
}

(async () => {
  const urls = process.argv.slice(2);
  if (urls.length === 0) {
    console.error('usage: node measure-reveal.js <url> [url...]');
    process.exit(1);
  }
  const browser = await chromium.launch();
  for (const url of urls) {
    const out = { url };
    for (const mode of ['clean', 'blocked', 'stubbed']) {
      try {
        const { hadSnippet, revealMs } = await measure(browser, url, mode);
        out[mode] = !hadSnippet && mode === 'clean' ? 'no async-hide'
                  : revealMs === null ? '>8000ms (still hidden)'
                  : `${revealMs}ms`;
        if (out.clean === 'no async-hide') break; // skip other modes
      } catch (e) {
        out[mode] = 'error: ' + e.message.split('\n')[0];
      }
    }
    console.log(JSON.stringify(out));
  }
  await browser.close();
})();

// Minimal headless-Chrome driver over the DevTools Protocol.
//
// No npm dependencies on purpose: this repo has no package.json and no build
// step, and it should stay that way. Node 22 ships a global WebSocket, and
// Chrome speaks CDP over it, so the whole harness is this one file.

const http = require('http');

const CDP_PORT = process.env.CDP_PORT || 9222;

function cdpHttp(path, method = 'GET') {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port: CDP_PORT, path, method }, res => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => { try { resolve(JSON.parse(body)); } catch (e) { resolve(body); } });
    });
    req.on('error', reject);
    req.end();
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// Poll until fn() returns something truthy. Every wait in the suites goes
// through this rather than a fixed sleep, so a slow CI box doesn't fail the
// run and a fast one doesn't pay for the worst case.
async function waitFor(fn, { timeout = 8000, interval = 100, what = 'condition' } = {}) {
  const deadline = Date.now() + timeout;
  let last;
  for (;;) {
    try { last = await fn(); if (last) return last; } catch (e) { last = 'threw: ' + e.message; }
    if (Date.now() > deadline) {
      throw new Error(`timed out after ${timeout}ms waiting for ${what} (last: ${JSON.stringify(last)})`);
    }
    await sleep(interval);
  }
}

class Page {
  constructor(ws, targetId) {
    this.ws = ws;
    this.targetId = targetId;
    this.id = 0;
    this.pending = new Map();
    this.logs = [];
  }

  static async open(url, { width = 1280, height = 900, block = [], stub = null } = {}) {
    const target = await cdpHttp('/json/new?about:blank', 'PUT');
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
    const page = new Page(ws, target.id);

    ws.addEventListener('message', ev => {
      const m = JSON.parse(ev.data);
      if (m.id && page.pending.has(m.id)) {
        const { res, rej } = page.pending.get(m.id);
        page.pending.delete(m.id);
        m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result);
        return;
      }
      if (m.method === 'Runtime.exceptionThrown') {
        const d = m.params.exceptionDetails;
        page.logs.push('EXCEPTION: ' + ((d.exception && (d.exception.description || d.exception.value)) || d.text));
      }
      if (m.method === 'Runtime.consoleAPICalled' && (m.params.type === 'error' || m.params.type === 'warning')) {
        page.logs.push(m.params.type.toUpperCase() + ': ' +
          m.params.args.map(a => a.value || a.description || '').join(' '));
      }
    });

    await page.send('Page.enable');
    await page.send('Runtime.enable');
    await page.send('Network.enable');
    // Non-negotiable: without this the browser cache serves a stale index.html
    // between runs and the suite reports PASS on code that is no longer there.
    // Caught by mutation-testing the harness — re-introducing a fixed bug still
    // showed 68/68 green until this line existed.
    await page.send('Network.setCacheDisabled', { cacheDisabled: true });
    if (block.length) await page.send('Network.setBlockedURLs', { urls: block });
    await page.send('Emulation.setDeviceMetricsOverride', {
      width, height, deviceScaleFactor: 1, mobile: width < 830,
    });
    if (stub) await page.send('Page.addScriptToEvaluateOnNewDocument', { source: stub });

    await page.send('Page.navigate', { url });
    // DOMContentLoaded is enough: every script this site cares about is
    // inline and parser-ordered, so it has run by the time this resolves.
    await page.waitFor(`document.readyState === 'interactive' || document.readyState === 'complete'`,
      { what: 'document ready' });
    return page;
  }

  send(method, params = {}) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params }));
    return new Promise((res, rej) => this.pending.set(id, { res, rej }));
  }

  async eval(expression) {
    const r = await this.send('Runtime.evaluate', {
      expression, returnByValue: true, awaitPromise: true,
    });
    if (r.exceptionDetails) {
      throw new Error(expression.slice(0, 80) + ' -> ' + JSON.stringify(r.exceptionDetails).slice(0, 240));
    }
    return r.result.value;
  }

  waitFor(expression, opts = {}) {
    return waitFor(() => this.eval(expression), { what: expression.slice(0, 60), ...opts });
  }

  // Drive an input the way a person does: set it, then fire the events the
  // page actually listens for ('input' and 'change').
  set(name, value) {
    return this.eval(`(function () {
      var el = document.data.elements[${JSON.stringify(name)}];
      if (!el) { throw new Error('no such field: ' + ${JSON.stringify(name)}); }
      el.value = ${JSON.stringify(value)};
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
      return el.value;
    })()`);
  }

  pick(name, value) {
    return this.eval(`(function () {
      var r = document.data.elements[${JSON.stringify(name)}], hit = false;
      for (var i = 0; i < r.length; ++i) {
        if (r[i].value === ${JSON.stringify(value)}) {
          r[i].checked = true;
          r[i].dispatchEvent(new Event('change', { bubbles: true }));
          hit = true;
        }
      }
      if (!hit) { throw new Error('no radio ' + ${JSON.stringify(name)} + '=' + ${JSON.stringify(value)}); }
      return true;
    })()`);
  }

  // Walk the page top to bottom, letting observers fire on the way.
  async scrollThrough(step = 700) {
    const height = await this.eval('document.body.scrollHeight');
    for (let y = 0; y < height; y += step) {
      await this.eval(`window.scrollTo(0, ${y})`);
      await sleep(120);
    }
    await this.eval(`window.scrollTo(0, ${height})`);
    await sleep(400);
  }

  // Console noise that is an artefact of the test environment, not a defect:
  // we deliberately block the ad/analytics/CMP origins.
  realLogs() {
    return this.logs.filter(l => !/ERR_BLOCKED_BY_CLIENT|ERR_FAILED|net::|blocked/i.test(l));
  }

  close() { return cdpHttp('/json/close/' + this.targetId); }
}

// Third-party origins are blocked in every suite: the tests must not depend on
// the network, must never fire a real ad request, and must not be able to
// report a live click to AdSense.
const THIRD_PARTY = [
  '*googlesyndication.com*', '*pagead2*', '*doubleclick.net*',
  '*fundingchoicesmessages*', '*googletagmanager.com*', '*google-analytics*',
  '*cusdis.com*', '*fonts.googleapis.com*', '*fonts.gstatic.com*',
  '*gstatic.com/charts*',
];

// --- tiny assertion reporter ------------------------------------------------

function suite(name) {
  const results = { name, passed: 0, failed: 0, lines: [] };
  return {
    results,
    section(title) { results.lines.push('  ' + title); },
    check(label, condition, detail) {
      const ok = !!condition;
      ok ? results.passed++ : results.failed++;
      results.lines.push(
        '    ' + (ok ? 'PASS' : 'FAIL') + '  ' + label +
        (detail !== undefined ? '   [' + detail + ']' : ''));
      return ok;
    },
  };
}

module.exports = { cdpHttp, sleep, waitFor, Page, THIRD_PARTY, suite };

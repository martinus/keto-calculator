#!/usr/bin/env node
//
// Run every check against the working tree.
//
//     node dev/test/run.js
//
// Starts a static server and a headless Chrome, runs the suites, tears both
// down, exits non-zero on any failure. No npm dependencies and no package.json:
// Node 22's built-in WebSocket talks to Chrome over the DevTools Protocol
// directly (see lib.js).

const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

const ROOT = path.resolve(__dirname, '..', '..');
const HTTP_PORT = process.env.HTTP_PORT || 8765;
const CDP_PORT = process.env.CDP_PORT || 9222;
const BASE = 'http://localhost:' + HTTP_PORT;

const CHROME = process.env.CHROME_BIN || ['google-chrome', 'google-chrome-stable',
  'chromium', 'chromium-browser'].find(bin => {
    try { require('child_process').execSync('command -v ' + bin, { stdio: 'ignore' }); return true; }
    catch (e) { return false; }
  });

const sleep = ms => new Promise(r => setTimeout(r, ms));

function waitForPort(port, path_, what) {
  return new Promise((resolve, reject) => {
    const deadline = Date.now() + 30000;
    (function attempt() {
      const req = http.get({ host: '127.0.0.1', port, path: path_ }, res => {
        res.resume(); resolve();
      });
      req.on('error', () => {
        if (Date.now() > deadline) return reject(new Error('timed out starting ' + what));
        setTimeout(attempt, 200);
      });
    })();
  });
}

(async () => {
  if (!CHROME) {
    console.error('No Chrome/Chromium found. Set CHROME_BIN to its path.');
    process.exit(2);
  }

  const server = spawn('python3', ['-m', 'http.server', String(HTTP_PORT), '--bind', '127.0.0.1'],
    { cwd: ROOT, stdio: 'ignore' });
  // A fresh profile per run — belt and braces with Network.setCacheDisabled in
  // lib.js. A reused profile once cached index.html hard enough that the suite
  // passed against a page that no longer existed.
  const profile = require('fs').mkdtempSync(path.join(require('os').tmpdir(), 'keto-test-'));
  const chrome = spawn(CHROME, [
    '--headless=new', '--remote-debugging-port=' + CDP_PORT,
    '--user-data-dir=' + profile,
    '--no-first-run', '--no-default-browser-check', '--disable-gpu', '--no-sandbox',
    '--disable-application-cache', '--disk-cache-size=1',
    'about:blank',
  ], { stdio: 'ignore' });

  const shutdown = () => { try { server.kill(); } catch (e) {} try { chrome.kill(); } catch (e) {} };
  process.on('exit', shutdown);
  process.on('SIGINT', () => { shutdown(); process.exit(130); });

  let failed = 0;
  try {
    await waitForPort(HTTP_PORT, '/index.html', 'the static server');
    await waitForPort(CDP_PORT, '/json/version', 'headless Chrome');

    const suites = [
      require('./links.test')(),                 // static, no browser
      await require('./ads.test')(BASE),
      await require('./app.test')(BASE),
    ];

    for (const s of suites) {
      console.log('\n[' + s.name + ']');
      s.lines.forEach(l => console.log(l));
      failed += s.failed;
    }
    const passed = suites.reduce((n, s) => n + s.passed, 0);
    console.log('\n' + (failed ? failed + ' FAILED, ' : '') + passed + ' passed');
  } catch (err) {
    console.error('\nHARNESS ERROR: ' + err.message);
    failed = failed || 1;
  } finally {
    shutdown();
    await sleep(150);
  }
  process.exit(failed ? 1 : 0);
})();

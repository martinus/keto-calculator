// Static checks over the deployed files — no browser needed.
//
// The German page is generated with root-absolute asset paths (it lives at
// /de/, so a relative "favicon.png" would 404 as /de/favicon.png). Two
// disclaimer links were missed in that pass and 404'd on every German page
// view until 2026-08-01. This catches the next one.

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const PAGES = [
  'index.html', 'disclaimer.html', 'embed.html', 'de/index.html',
  'net-carbs-vs-total-carbs.html', 'how-much-protein-on-keto.html',
  'how-fast-will-i-lose-weight-on-keto.html',
];

// Resolve an href the way the server would: root-absolute against the site
// root, everything else against the page's own directory.
function resolve(fromPage, url) {
  const target = url.startsWith('/')
    ? path.join(ROOT, url.slice(1))
    : path.resolve(ROOT, path.dirname(fromPage), url);
  return target.endsWith('/') ? path.join(target, 'index.html') : target;
}

module.exports = function run() {
  const { suite } = require('./lib');
  const t = suite('links');

  t.section('internal page links resolve');
  let broken = 0;
  for (const page of PAGES) {
    const html = fs.readFileSync(path.join(ROOT, page), 'utf8');
    for (const m of html.matchAll(/href="([^"#?:]+?)"/g)) {
      const url = m[1];
      if (/^(https?:)?\/\//.test(url) || url.startsWith('data:')) continue;
      if (!url.endsWith('.html') && !url.endsWith('/')) continue;
      if (!fs.existsSync(resolve(page, url))) {
        t.check(page + ' -> ' + url, false, 'missing');
        broken++;
      }
    }
  }
  if (!broken) t.check('no broken internal page links across ' + PAGES.length + ' pages', true);

  t.section('local assets referenced by each page exist');
  let missing = 0;
  for (const page of PAGES) {
    const html = fs.readFileSync(path.join(ROOT, page), 'utf8');
    const urls = new Set();
    for (const m of html.matchAll(/(?:src|href)="([^"]+)"/g)) urls.add(m[1]);
    for (const m of html.matchAll(/url\(([^)'"]+)\)/g)) urls.add(m[1]);
    for (const url of urls) {
      if (/^(https?:)?\/\//.test(url) || url.startsWith('data:') || url.startsWith('#')) continue;
      if (!/\.(png|jpg|jpeg|gif|svg|webp|ico|css|js|json|woff2?|xml|txt)$/i.test(url)) continue;
      const clean = url.split('?')[0].split('#')[0];
      if (!fs.existsSync(resolve(page, clean))) {
        t.check(page + ' -> ' + clean, false, 'missing');
        missing++;
      }
    }
  }
  if (!missing) t.check('every referenced local asset exists', true);

  t.section('generated pages are not hand-edited into drift');
  // The German page must not carry a relative link that would resolve inside
  // /de/. Anything page-like has to be root-absolute or absolute.
  const de = fs.readFileSync(path.join(ROOT, 'de/index.html'), 'utf8');
  const relative = [...de.matchAll(/href="([^"#?:/][^"#?:]*\.html)"/g)].map(m => m[1]);
  t.check('de/index.html has no relative .html links', relative.length === 0, JSON.stringify(relative));

  t.section('old.html stays out of the index');
  const old = fs.readFileSync(path.join(ROOT, 'old.html'), 'utf8');
  t.check('old.html is noindex', /name="robots"\s+content="noindex/.test(old));
  t.check('old.html canonicalises to the real page',
    /rel="canonical"\s+href="https:\/\/keto-calculator\.ankerl\.com\/"/.test(old));

  return t.results;
};

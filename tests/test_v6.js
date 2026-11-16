// Stack Bank Premium v6 regression — installable PWA.
// Run: node tests/test_v6.js   (needs jsdom: see tests/run_all.sh)
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('/home/hatch/workspace/.jsdom-test/node_modules/jsdom');
const ROOT = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'stack-bank-premium.html'), 'utf8');
const errors = [];

function makeDom() {
  return new JSDOM(html, {
    url: 'http://localhost/',
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    beforeParse(window) {
      window.HTMLCanvasElement.prototype.getContext = () => null;
      window.speechSynthesis = { speak() {} };
      window.SpeechSynthesisUtterance = function (t) { this.text = t; };
      window.onerror = (m) => errors.push('window.onerror: ' + m);
    }
  });
}

const out = [];
const check = (name, cond, extra) => out.push((cond ? 'PASS' : 'FAIL') + ' | ' + name + (extra !== undefined ? ' | ' + extra : ''));
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  try {
    const dom = makeDom();
    const w = dom.window, d = w.document;
    const $ = (id) => d.getElementById(id);
    await sleep(1200);
    w.finishOnboard();

    check('app visible after onboarding', !$('app').classList.contains('hide'));
    const manifestLink = d.querySelector('link[rel="manifest"]');
    check('manifest link present', !!manifestLink, manifestLink ? manifestLink.getAttribute('href') : 'missing');
    check('theme-color present', !!d.querySelector('meta[name="theme-color"]'));
    check('apple touch icon present', !!d.querySelector('link[rel="apple-touch-icon"]'));
    check('apple mobile-web-app-capable present', !!d.querySelector('meta[name="apple-mobile-web-app-capable"]'));

    let manifest = null;
    try { manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest.webmanifest'), 'utf8')); } catch (e) { manifest = null; }
    check('manifest parses', !!manifest);
    check('manifest start_url points at the app', manifest && manifest.start_url.includes('stack-bank-premium.html'), manifest && manifest.start_url);
    const sizes = (manifest && manifest.icons || []).map(i => i.sizes);
    check('manifest has 192 + 512 + maskable icons',
      sizes.includes('192x192') && sizes.includes('512x512') && (manifest.icons || []).some(i => i.purpose === 'maskable'));
    const iconFiles = (manifest && manifest.icons || []).map(i => i.src);
    check('manifest icon files exist on disk', iconFiles.every(f => fs.existsSync(path.join(ROOT, f))), iconFiles.join(', '));

    const sw = fs.readFileSync(path.join(ROOT, 'sw.js'), 'utf8');
    check('service worker caches the app shell',
      sw.includes('stack-bank-premium.html') && sw.includes('manifest.webmanifest') && sw.includes('caches.open'));
    check('service worker leaves cross-origin requests alone',
      sw.includes('new URL') && sw.includes('origin') && sw.includes('location.origin') && sw.includes('fetch(e.request)'));

    w.go('more');
    const moreText = $('s-more').textContent;
    check('Install app button on More screen', moreText.includes('Install app'), moreText.split('\n').map(s => s.trim()).filter(Boolean).slice(0, 30).join(' | '));
    check('My account button on More screen', moreText.includes('My account'));
    w.installApp();
    check('installApp opens instructions when no browser prompt',
      !$('modalBg').classList.contains('hide') && $('modalBox').textContent.includes('Add to Home screen'));
    w.closeModal();

    check('ladder hero still renders', $('ladderHero').textContent.includes('PAYCHECK LADDER'));
    check('no JS errors', errors.length === 0, errors.join(' ; ') || 'clean');
  } catch (e) {
    out.push('FAIL | exception: ' + e.message);
    errors.push(e.stack);
  }
  console.log(out.join('\n'));
  if (errors.length) console.log('ERRORS:\n' + errors.join('\n'));
  process.exit(out.some(l => l.startsWith('FAIL')) ? 1 : 0);
})();

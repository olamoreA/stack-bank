// Stack Bank Premium v9 — beautiful opening + premium home.
// Run: node tests/test_v9.js   (needs jsdom: see tests/run_all.sh)
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

    // --- opening: the showcase is there before any tap ---
    check('opening showcase renders', !!d.querySelector('.onb-show'));
    check('mini gold card renders', !!d.querySelector('.onb-card-mini'));
    check('two floating chips render', d.querySelectorAll('.onb-chip').length === 2);
    check('eyebrow renders', !!d.querySelector('.onb-eyebrow') && d.querySelector('.onb-eyebrow').textContent.includes('PREMIUM'));
    check('trust row renders', !!d.querySelector('.onb-trust') && d.querySelector('.onb-trust').textContent.includes('No branch'));

    // --- count-up finishes on the demo balance ---
    await sleep(1800);
    check('showcase balance counts up to $1,240.50', $('onbBal').textContent === '1,240.50', $('onbBal').textContent);

    // --- v9 CSS is in the document ---
    const styles = [...d.querySelectorAll('style')].map(s => s.textContent).join('\n');
    check('v9 CSS present (showcase + sheen)', styles.includes('.onb-show') && styles.includes('@keyframes sheen') && styles.includes('@keyframes cardFloat'));

    // --- home: balance hero renders big and premium ---
    w.finishOnboard();
    await sleep(200);
    check('home balance renders', $('balHome').textContent === '1,240.5', $('balHome').textContent);
    check('home hero present', !!d.querySelector('.hero'));
    check('ladder hero still renders', $('ladderHero').textContent.includes('PAYCHECK LADDER'));

    // --- showcase chips get the icon treatment (no raw emoji left) ---
    await sleep(200);
    const appText = $('app').textContent;
    const emoji = appText.match(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}]/gu) || [];
    check('zero emoji text nodes in #app', emoji.length === 0, 'found ' + emoji.length);

    check('no JS errors', errors.length === 0, errors.join(' ; ') || 'clean');
  } catch (e) {
    out.push('FAIL | exception: ' + e.message);
    errors.push(e.stack);
  }
  console.log(out.join('\n'));
  if (errors.length) console.log('ERRORS:\n' + errors.join('\n'));
  process.exit(out.some(l => l.startsWith('FAIL')) ? 1 : 0);
})();

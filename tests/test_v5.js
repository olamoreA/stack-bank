// Stack Bank Premium v5 regression — ladder hero + edge cases.
// Run: node tests/test_v5.js   (needs jsdom: see tests/run_all.sh)
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

    // --- ladder hero: split sums exactly to the week's earnings ---
    const m = w.eval('ladderMath()');
    const sum = m.salary + m.buffer + m.jars + m.spend;
    check('hero split sums to week earnings', sum === m.cur, JSON.stringify(m));
    check('hero renders on home', $('ladderHero').textContent.includes('PAYCHECK LADDER'));

    // --- failed send keeps the balance ---
    w.eval('S.balance = 10');
    $('sendTo').value = 'Test Person';
    $('sendAmt').value = '100';
    w.doSend();
    check('failed send keeps balance', w.eval('S').balance === 10, 'balance=' + w.eval('S').balance);
    check('failed send records a Failed tx', w.eval('S').txs[0].st === 'failed');

    // --- offline send queues, then settles on reconnect ---
    w.eval('S.balance = 100; S.net = false');
    $('sendTo').value = 'Ada';
    $('sendAmt').value = '20';
    w.doSend();
    check('queued send does not move money', w.eval('S').balance === 100);
    check('queued send is pending', w.eval('S').txs.some(t => t.st === 'pending'));
    w.eval('S.net = true');
    w.settlePending();
    check('queued send settled on reconnect', Math.abs(w.eval('S').balance - 77.01) < 0.01, 'balance=' + w.eval('S').balance);

    // --- duplicate guard: modal appears, confirmed send is marked ---
    w.eval('S.balance = 500; S.net = true');
    $('sendTo').value = 'Ada';
    $('sendAmt').value = '10';
    w.doSend();
    const balAfterFirst = w.eval('S').balance;
    $('sendTo').value = 'Ada';
    $('sendAmt').value = '10';
    w.doSend();
    check('duplicate modal appears', !$('modalBg').classList.contains('hide'));
    check('duplicate blocked until confirmed', w.eval('S').balance === balAfterFirst);
    w.confirmDupSend();
    check('duplicate tx marked', w.eval('S').txs.some(t => t.st === 'duplicate'));

    // --- Ajo missed: escrow covers, trust drops 8 ---
    const before = w.eval('S').circle;
    const trustBefore = before.members[1].trust;
    const escrowBefore = before.escrow;
    w.missedPayment(1);
    const after = w.eval('S').circle;
    check('escrow covered missed share, trust -8',
      after.escrow === escrowBefore - after.amt && after.members[1].trust === trustBefore - 8,
      'escrow ' + escrowBefore + '->' + after.escrow + ', trust ' + trustBefore + '->' + after.members[1].trust);

    // --- no emoji left as raw text in the app ---
    // The icon engine swaps emoji via a MutationObserver, so give it a beat.
    await sleep(150);
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

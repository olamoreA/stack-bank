// Stack Bank Premium v8 — fixes: real Settings, honest footer, fresh accounts,
// account name sync, onboard sign-in shortcut. Server must be running on :8787.
// Run: node tests/test_v8.js   (needs jsdom: see tests/run_all.sh)
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('/home/hatch/workspace/.jsdom-test/node_modules/jsdom');
const ROOT = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'stack-bank-premium.html'), 'utf8');
const errors = [];
const API = 'http://127.0.0.1:8787';
const PHONE = '+2348' + String(Date.now()).slice(-9); // unique per run, so the suite is repeatable

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
      window.fetch = (...a) => fetch(...a);
      window.AbortController = AbortController;
    }
  });
}

const out = [];
const check = (name, cond, extra) => out.push((cond ? 'PASS' : 'FAIL') + ' | ' + name + (extra !== undefined ? ' | ' + extra : ''));
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
  try {
    const a = makeDom();
    const wa = a.window, da = wa.document;
    const $a = (id) => da.getElementById(id);
    await sleep(1200);

    // --- the old dead Settings button now opens a real screen ---
    wa.finishOnboard();
    wa.go('settings');
    check('Settings screen renders (was a dead button)', !$a('s-settings').classList.contains('hide'));
    check('Settings status line fills in', $a('setStatus').textContent.includes('Stack Bank Premium v8'));
    check('Settings screen has account/install/elder rows', da.querySelectorAll('#s-settings .rowline').length === 3);

    // --- footer no longer claims FDIC insurance ---
    const footer = da.querySelector('#s-more .card.tight .dim');
    check('footer is honest, no FDIC claim', footer && !footer.textContent.includes('FDIC') && footer.textContent.includes('test balances only'),
      footer ? footer.textContent.slice(0, 80) : 'footer missing');

    // --- onboard sign-in shortcut ---
    const b = makeDom();
    const wb = b.window, db = wb.document;
    const $b = (id) => db.getElementById(id);
    await sleep(1200);
    wb.sbEnterToSignIn();
    check('onboard sign-in shortcut lands on account screen', !$b('s-account').classList.contains('hide'));

    // --- register: fresh account starts at zero, name follows the account ---
    wb.go('account');
    $b('apiUrl').value = API;
    wb.sbSetApiUrl();
    $b('acctPhone').value = PHONE;
    $b('acctName').value = 'V8 User';
    $b('acctPin').value = '1357';
    await wb.sbRegister();
    await sleep(300);
    const SB = wb.eval('S');
    check('new account balance is 0 (no demo money)', SB.balance === 0, 'balance=' + SB.balance);
    check('new account jars are empty', SB.jars.every(j => j.saved === 0));
    check('new account has no demo transactions', SB.txs.length === 0);
    check('new account name is the account name', SB.name === 'V8 User', SB.name);
    check('new account syncs', SB.syncStatus === 'synced', SB.syncStatus);

    // --- second device: sign in, pull the fresh state, name stays the account's ---
    const c = makeDom();
    const wc = c.window, dc = wc.document;
    const $c = (id) => dc.getElementById(id);
    await sleep(1200);
    wc.finishOnboard();
    wc.go('account');
    $c('apiUrl').value = API;
    wc.sbSetApiUrl();
    $c('acctPhone').value = PHONE;
    $c('acctPin').value = '1357';
    await wc.sbLogin();
    await sleep(300);
    const SC = wc.eval('S');
    check('second device pulls zero balance', SC.balance === 0, 'balance=' + SC.balance);
    check('second device shows the account name', SC.name === 'V8 User', SC.name);
    check('no JS errors', errors.length === 0, errors.join(' ; ') || 'clean');
  } catch (e) {
    out.push('FAIL | exception: ' + e.message);
    errors.push(e.stack);
  }
  console.log(out.join('\n'));
  if (errors.length) console.log('ERRORS:\n' + errors.join('\n'));
  process.exit(out.some(l => l.startsWith('FAIL')) ? 1 : 0);
})();

// Stack Bank Premium v7 end-to-end — two devices, real server on 127.0.0.1:8787.
// The server must be running first:  python3 server/app.py
// Run: node tests/test_v7.js   (needs jsdom: see tests/run_all.sh)
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
    // ---- Phone A: onboard, set server, register, state lands on the server ----
    const a = makeDom();
    const wa = a.window, da = wa.document;
    const $a = (id) => da.getElementById(id);
    await sleep(1200);
    wa.finishOnboard();
    check('A: app visible', !$a('app').classList.contains('hide'));
    wa.go('account');
    check('A: account screen renders', !$a('s-account').classList.contains('hide'));
    $a('apiUrl').value = API;
    wa.sbSetApiUrl();
    check('A: server address saved', wa.eval('S').apiUrl === API);
    $a('acctPhone').value = PHONE;
    $a('acctName').value = 'E2E User';
    $a('acctPin').value = '2468';
    await wa.sbRegister();
    await sleep(300);
    const SA = wa.eval('S');
    check('A: token issued', !!SA.apiToken, 'token len ' + (SA.apiToken || '').length);
    check('A: sync status synced', SA.syncStatus === 'synced', SA.syncStatus);
    check('A: status line shows signed in', $a('acctStatus').textContent.includes(PHONE));
    const srv = await fetch(API + '/api/state', { headers: { Authorization: 'Bearer ' + SA.apiToken } }).then(r => r.json());
    check('A: server holds the pushed state', srv.state && srv.state.name === 'E2E User',
      'name=' + (srv.state && srv.state.name));

    // ---- Phone B: fresh device, onboard, sign in, state comes down ----
    const b = makeDom();
    const wb = b.window, db = wb.document;
    const $b = (id) => db.getElementById(id);
    await sleep(1200);
    wb.finishOnboard();
    wb.go('account');
    $b('apiUrl').value = API;
    wb.sbSetApiUrl();
    $b('acctPhone').value = PHONE;
    $b('acctPin').value = '2468';
    await wb.sbLogin();
    await sleep(300);
    const SB = wb.eval('S');
    check('B: signed in after login', !!SB.apiToken);
    check('B: pulled balance matches A', SB.balance === 0, 'balance=' + SB.balance);
    check('B: pulled name matches A', SB.name === 'E2E User');
    check('B: ladder state pulled', SB.ladder && SB.ladder.weekly === 250);

    // ---- B changes something -> it pushes -> server sees it ----
    wb.eval('S.balance = 100; save();');
    await sleep(1800); // debounce (1s) + round trip
    const srv2 = await fetch(API + '/api/state', { headers: { Authorization: 'Bearer ' + SB.apiToken } }).then(r => r.json());
    check('B: edit pushed to server', srv2.state && srv2.state.balance === 100, 'balance=' + (srv2.state && srv2.state.balance));

    // ---- Wrong PIN is refused ----
    const c = makeDom();
    const wc = c.window, dc = wc.document;
    const $c = (id) => dc.getElementById(id);
    await sleep(1200);
    wc.finishOnboard();
    wc.go('account');
    $c('apiUrl').value = API;
    wc.sbSetApiUrl();
    $c('acctPhone').value = PHONE;
    $c('acctPin').value = '0000';
    await wc.sbLogin();
    await sleep(200);
    check('C: wrong PIN gets no token', !wc.eval('S').apiToken);
    check('C: wrong PIN shows an error', $c('toastEl').textContent.toLowerCase().includes('wrong'));

    // ---- Sign out clears the token ----
    wb.sbLogout();
    check('B: sign out clears token', !wb.eval('S').apiToken);

    check('no JS errors', errors.length === 0, errors.join(' ; ') || 'clean');
  } catch (e) {
    out.push('FAIL | exception: ' + e.message);
    errors.push(e.stack);
  }
  console.log(out.join('\n'));
  if (errors.length) console.log('ERRORS:\n' + errors.join('\n'));
  process.exit(out.some(l => l.startsWith('FAIL')) ? 1 : 0);
})();

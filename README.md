# Stack Bank

A premium banking app demo for gig workers and freelancers, built around one
idea: uneven gig income should still feel like a steady weekly salary.

## What is in this repo

- `stack-bank-premium.html` — the app. Download it and open it in any browser.
  No server, no install, no account. Your data stays in your browser.
- `stack-bank__17.html` — the original design this premium version is built on.
  It is kept untouched.
- `build_stack_premium.py` — the builder. It turns the original file into the
  premium file, so every version is reproducible.

## What the app does

- **Paycheck ladder (the hero):** your week's gig income is split on the home
  screen into a steady Friday salary, a buffer reserve, savings jars, and
  money to spend — with the math shown live.
- **Late-payer shield:** log an invoice; if the client pays late, the shield
  fronts you the money and chases them.
- **Ajo savings circles:** group savings with an escrow that covers a missed
  share and a trust score that drops when someone misses.
- **Real edge cases, not just the happy path:** failed transfers are recorded
  with a retry, sends queue when data is off and settle when it returns, and
  a duplicate send is stopped and confirmed before it goes twice.
- **Easy mode:** big buttons, big text, voice read-out, USSD and SMS banking
  for phones with no data.

## Install it on your phone

Stack Bank is a PWA, so it installs like a real app — its own icon, full
screen, and it works offline.

1. Open the app from a web link over https (for example a GitHub Pages link).
   Installing does **not** work from a downloaded file.
2. Android (Chrome): tap the three dots, then **Add to Home screen**.
   iPhone (Safari): tap Share, then **Add to Home Screen**.
3. Or tap **Install app** on the More screen inside the app.

The install files are `manifest.webmanifest`, `sw.js` (offline service
worker), and the icons in `stack-bank-icons/`. They are all generated or
referenced by `build_stack_premium.py`.

## Real accounts (backend)

Part 1 and 2 of the real app live in `server/` — a Python server with no
dependencies:

```sh
python3 server/app.py
```

Then open http://127.0.0.1:8787/ — the app is served from the same server.
Inside the app: More → My account → set the server address, create an
account with a phone number + PIN, and your balance, jars, ladder, and
Ajo circle sync to the server and follow you to any phone. PINs are
stored as scrypt hashes, 5 wrong PINs lock the account for 15 minutes.
See `server/README.md` for the API and how to keep it online.

## Status

This is a front-end demo. It moves no real money and connects to no bank.
Turning it into a real banking app needs a licensed bank partner and a real
backend — that is the next chapter, not this file.

## Rebuild

From your home directory:

```sh
python3 workspace/build_stack_premium.py
```

That rewrites `stack-bank-premium.html` from the original source.

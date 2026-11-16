# Stack Bank server

Real accounts, a real database, and real login — standard library only.
No dependencies, no paid services, no account with anyone to run it.

## Run it

```sh
python3 server/app.py
```

Then open http://127.0.0.1:8787/ — the app itself is served from the same
server, so the whole real app runs from one command.

Change the port with `PORT=8000 python3 server/app.py`.
Change the database file with `STACK_DB=/path/to/file.db`.

## What it does

- **Register / sign in** with a phone number + 4–6 digit PIN.
  `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`.
- **Security:** PINs are stored as scrypt hashes with a random salt — never
  plain text. Sign-in gives a random bearer token that expires after 30
  days. Five wrong PINs lock the account for 15 minutes. Wrong phone
  numbers get the same error as wrong PINs, so nobody can probe which
  numbers have accounts.
- **State sync:** `GET /api/state` and `PUT /api/state` keep each account's
  app state (balance, jars, ladder, transactions, Ajo circle) in SQLite.
  The phone app pulls on sign-in and pushes on every change.
- **Health:** `GET /api/health`.

## What it does not do

It moves no real money. Balances here are test balances. Real transfers,
real deposits, and real naira or dollar balances need a licensed bank
partner — that is a later step, not this server.

## Running it for real people

This server only runs while the machine it is on is running. To keep it
online for others, put it on a machine that stays on:

- **On your phone (Termux):** copy this repo to the phone, run
  `python3 server/app.py`. It works, but the phone must stay on and the
  app must be open — good for testing with friends, not for the public.
- **On a free host:** any host that runs Python (Render, Railway,
  PythonAnywhere, a small VPS) can run `python3 server/app.py` with
  `PORT` set. Use https there — bearer tokens must never travel over
  plain http on the open internet.
- **For the app to reach it:** set the server address in the app
  (More → My account → Server address). The app keeps working offline
  without a server; it just stays on that phone only.

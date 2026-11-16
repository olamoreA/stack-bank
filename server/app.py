#!/usr/bin/env python3
"""Stack Bank API server — real accounts, real database, real login.

Standard library only (Python 3.11+). No dependencies, no paid services.

What it does:
  * Accounts: register / sign in with a phone number + 4-6 digit PIN.
  * Security: PINs are stored as scrypt hashes (never plain text), sessions are
    random bearer tokens that expire after 30 days, and 5 wrong PINs lock the
    account for 15 minutes.
  * State sync: each account keeps its own app state (balance, jars, ladder,
    transactions, Ajo circle) in SQLite. The phone app pulls it on sign-in
    and pushes it on every change, so the account follows the user to any
    phone and survives a lost phone.
  * It also serves the app itself (the static files next to this server), so
    one command gives you the whole real app locally.

Run it:
    python3 server/app.py            # http://127.0.0.1:8787
    PORT=8000 python3 server/app.py  # another port
    STACK_DB=/path/to/file.db python3 server/app.py

This is the accounts-and-data layer. It moves no real money: balances here
are test balances until a licensed bank partner is connected.

API:
  GET  /api/health                       -> {"ok": true, ...}
  POST /api/auth/register {phone,name,pin} -> {"token": ..., "user": {...}}
  POST /api/auth/login    {phone,pin}      -> {"token": ..., "user": {...}}
  POST /api/auth/logout   (Bearer token)   -> {"ok": true}
  GET  /api/me            (Bearer token)   -> {"user": {...}}
  GET  /api/state         (Bearer token)   -> {"state": {...}|null, "updated_at": ...}
  PUT  /api/state         (Bearer token) {state: {...}} -> {"ok": true, ...}
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

VERSION = "1.0"
PORT = int(os.environ.get("PORT", "8787"))
HOST = os.environ.get("HOST", "127.0.0.1")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root: holds the static app files
DB_PATH = os.environ.get("STACK_DB", os.path.join(HERE, "stackbank.db"))

MAX_BODY = 2 * 1024 * 1024          # 2 MB request cap
MAX_STATE = 1 * 1024 * 1024         # 1 MB state document cap
SESSION_DAYS = 30
LOCK_AFTER = 5                      # failed PINs before lockout
LOCK_MINUTES = 15
PHONE_RE = re.compile(r"^\+?[0-9]{7,15}$")
PIN_RE = re.compile(r"^[0-9]{4,6}$")

MIME = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json",
    ".webmanifest": "application/manifest+json",
    ".png": "image/png",
    ".css": "text/css; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}


# ---------------------------------------------------------------- database
def connect():
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            pin_hash BLOB NOT NULL,
            pin_salt BLOB NOT NULL,
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            locked_until INTEGER NOT NULL DEFAULT 0,
            created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at INTEGER NOT NULL,
            expires_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS states (
            user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            state_json TEXT NOT NULL,
            updated_at INTEGER NOT NULL
        );
        """
    )
    db.commit()
    return db


DB = connect()


def hash_pin(pin: str, salt: bytes) -> bytes:
    return hashlib.scrypt(pin.encode(), salt=salt, n=16384, r=8, p=1, dklen=64)


def new_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    now = int(time.time())
    DB.execute(
        "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?,?,?,?)",
        (token, user_id, now, now + SESSION_DAYS * 86400),
    )
    DB.commit()
    return token


def auth_user(handler) -> dict | None:
    """Return the user row for a valid Bearer token, else None."""
    auth = handler.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth[7:].strip()
    row = DB.execute(
        "SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id "
        "WHERE s.token = ? AND s.expires_at > ?",
        (token, int(time.time())),
    ).fetchone()
    return dict(row) if row else None


def public_user(row: dict) -> dict:
    return {"id": row["id"], "phone": row["phone"], "name": row["name"]}


# ---------------------------------------------------------------- handler
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # -- plumbing ---------------------------------------------------------
    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")

    def _send(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, status: int, body: bytes, ctype: str):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            raise ValueError("body too large")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode())
        except (ValueError, UnicodeDecodeError):
            raise ValueError("invalid JSON")
        if not isinstance(data, dict):
            raise ValueError("JSON body must be an object")
        return data

    def _require_auth(self):
        user = auth_user(self)
        if not user:
            self._send(401, {"error": "not signed in"})
            return None
        return user

    # -- HTTP verbs -------------------------------------------------------
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            users = DB.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            self._send(200, {"ok": True, "version": VERSION, "users": users})
            return
        if path == "/api/me":
            user = self._require_auth()
            if user:
                self._send(200, {"user": public_user(user)})
            return
        if path == "/api/state":
            user = self._require_auth()
            if not user:
                return
            row = DB.execute(
                "SELECT state_json, updated_at FROM states WHERE user_id = ?",
                (user["id"],),
            ).fetchone()
            if row:
                self._send(200, {"state": json.loads(row["state_json"]), "updated_at": row["updated_at"]})
            else:
                self._send(200, {"state": None, "updated_at": None})
            return
        self._serve_static(path)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            data = self._read_json()
        except ValueError as e:
            self._send(400, {"error": str(e)})
            return
        if path == "/api/auth/register":
            self._register(data)
        elif path == "/api/auth/login":
            self._login(data)
        elif path == "/api/auth/logout":
            user = self._require_auth()
            if user:
                auth = self.headers.get("Authorization", "")[7:].strip()
                DB.execute("DELETE FROM sessions WHERE token = ?", (auth,))
                DB.commit()
                self._send(200, {"ok": True})
        else:
            self._send(404, {"error": "unknown route"})

    def do_PUT(self):
        path = urlparse(self.path).path
        if path != "/api/state":
            self._send(404, {"error": "unknown route"})
            return
        user = self._require_auth()
        if not user:
            return
        try:
            data = self._read_json()
        except ValueError as e:
            self._send(400, {"error": str(e)})
            return
        state = data.get("state")
        if not isinstance(state, dict):
            self._send(400, {"error": "state must be an object"})
            return
        raw = json.dumps(state)
        if len(raw.encode()) > MAX_STATE:
            self._send(400, {"error": "state too large"})
            return
        now = int(time.time())
        DB.execute(
            "INSERT INTO states (user_id, state_json, updated_at) VALUES (?,?,?) "
            "ON CONFLICT(user_id) DO UPDATE SET state_json=excluded.state_json, updated_at=excluded.updated_at",
            (user["id"], raw, now),
        )
        DB.commit()
        self._send(200, {"ok": True, "updated_at": now})

    # -- auth -------------------------------------------------------------
    def _register(self, data):
        phone = str(data.get("phone", "")).strip()
        name = str(data.get("name", "")).strip()
        pin = str(data.get("pin", "")).strip()
        if not PHONE_RE.match(phone):
            self._send(400, {"error": "phone must be 7-15 digits, optional + at the start"})
            return
        if not 1 <= len(name) <= 50:
            self._send(400, {"error": "name must be 1-50 characters"})
            return
        if not PIN_RE.match(pin):
            self._send(400, {"error": "PIN must be 4-6 digits"})
            return
        salt = secrets.token_bytes(32)
        try:
            cur = DB.execute(
                "INSERT INTO users (phone, name, pin_hash, pin_salt, created_at) VALUES (?,?,?,?,?)",
                (phone, name, hash_pin(pin, salt), salt, int(time.time())),
            )
            DB.commit()
        except sqlite3.IntegrityError:
            self._send(409, {"error": "an account with this phone number already exists"})
            return
        user = DB.execute("SELECT * FROM users WHERE id = ?", (cur.lastrowid,)).fetchone()
        token = new_session(user["id"])
        self._send(201, {"token": token, "user": public_user(dict(user))})

    def _login(self, data):
        phone = str(data.get("phone", "")).strip()
        pin = str(data.get("pin", "")).strip()
        if not PHONE_RE.match(phone) or not PIN_RE.match(pin):
            self._send(400, {"error": "check the phone number and PIN format"})
            return
        row = DB.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
        now = int(time.time())
        if not row:
            # Same generic error as a wrong PIN: never reveal which phones exist.
            self._send(401, {"error": "wrong phone number or PIN"})
            return
        user = dict(row)
        if user["locked_until"] > now:
            mins = max(1, (user["locked_until"] - now + 59) // 60)
            self._send(423, {"error": f"account locked after too many wrong PINs — try again in {mins} minutes"})
            return
        if not hmac.compare_digest(hash_pin(pin, user["pin_salt"]), user["pin_hash"]):
            failed = user["failed_attempts"] + 1
            locked = now + LOCK_MINUTES * 60 if failed >= LOCK_AFTER else 0
            DB.execute(
                "UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?",
                (failed, locked, user["id"]),
            )
            DB.commit()
            if locked:
                self._send(423, {"error": f"account locked after {LOCK_AFTER} wrong PINs — try again in {LOCK_MINUTES} minutes"})
            else:
                self._send(401, {"error": f"wrong phone number or PIN ({LOCK_AFTER - failed} tries left)"})
            return
        DB.execute(
            "UPDATE users SET failed_attempts = 0, locked_until = 0 WHERE id = ?",
            (user["id"],),
        )
        DB.commit()
        token = new_session(user["id"])
        self._send(200, {"token": token, "user": public_user(user)})

    # -- static app files -------------------------------------------------
    def _serve_static(self, path):
        rel = "index.html" if path in ("/", "") else path.lstrip("/")
        if ".." in rel or rel.startswith("/"):
            self._send(404, {"error": "not found"})
            return
        full = os.path.realpath(os.path.join(ROOT, rel))
        if not full.startswith(os.path.realpath(ROOT) + os.sep):
            self._send(404, {"error": "not found"})
            return
        if not os.path.isfile(full):
            self._send(404, {"error": "not found"})
            return
        ext = os.path.splitext(full)[1].lower()
        if ext not in MIME:
            self._send(404, {"error": "not found"})
            return
        with open(full, "rb") as fh:
            self._send_text(200, fh.read(), MIME[ext])


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Stack Bank API running on http://{HOST}:{PORT}  (db: {DB_PATH})", flush=True)
    print("Open http://%s:%d/ in your browser — the app is served from here too." % (HOST, PORT), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.", flush=True)


if __name__ == "__main__":
    main()

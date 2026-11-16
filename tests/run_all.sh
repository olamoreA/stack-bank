#!/bin/bash
# Run the whole Stack Bank test suite.
# - v5/v6 run offline (no server needed).
# - v7/v8 need the server: run `python3 server/app.py` in another window first.
set -e
cd "$(dirname "$0")/.."
if [ ! -d /home/hatch/workspace/.jsdom-test/node_modules/jsdom ]; then
  echo "Installing jsdom (test-only, lives outside the repo)..."
  mkdir -p /home/hatch/workspace/.jsdom-test
  npm install jsdom --prefix /home/hatch/workspace/.jsdom-test --no-save --no-audit --no-fund
fi
for t in tests/test_v5.js tests/test_v6.js tests/test_v7.js tests/test_v8.js tests/test_v9.js; do
  echo "===== $t ====="
  node "$t"
done
echo "ALL SUITES PASSED"

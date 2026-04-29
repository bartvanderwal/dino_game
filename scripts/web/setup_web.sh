#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv-web}"
PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.org/simple}"

echo "[web-setup] root: $ROOT_DIR"
echo "[web-setup] venv: $VENV_DIR"
echo "[web-setup] index: $PIP_INDEX_URL"

if [ -n "${PIP_EXTRA_INDEX_URL:-}" ]; then
  echo "[web-setup] ERROR: PIP_EXTRA_INDEX_URL is set, which is disallowed by project policy." >&2
  echo "[web-setup] Use a single trusted index via PIP_INDEX_URL (default: https://pypi.org/simple)." >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip uninstall -y pygame >/dev/null 2>&1 || true
"$VENV_DIR/bin/python" -m pip install \
  --isolated \
  --disable-pip-version-check \
  --require-hashes \
  --only-binary=:all: \
  --index-url "$PIP_INDEX_URL" \
  -r "$ROOT_DIR/requirements-web.txt"

echo "[web-setup] Done."
echo "[web-setup] Next: scripts/web/build_web.sh"

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
PYTHON_BIN="${PYTHON_BIN:-}"
PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.org/simple}"

choose_python_bin() {
  local candidate

  if [ -n "$PYTHON_BIN" ]; then
    if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
      echo "[venv-setup] ERROR: PYTHON_BIN '$PYTHON_BIN' not found."
      exit 1
    fi
    echo "$PYTHON_BIN"
    return 0
  fi

  for candidate in python3.14 python3.13 python3.12 python3; do
    if ! command -v "$candidate" >/dev/null 2>&1; then
      continue
    fi
    echo "$candidate"
    return 0
  done

  echo "[venv-setup] ERROR: No compatible Python found." >&2
  echo "[venv-setup] Install Python 3.12+ and rerun." >&2
  exit 1
}

PYTHON_BIN="$(choose_python_bin)"

echo "[venv-setup] root: $ROOT_DIR"
echo "[venv-setup] python: $PYTHON_BIN"
echo "[venv-setup] venv: $VENV_DIR"
echo "[venv-setup] index: $PIP_INDEX_URL"

if [ -n "${PIP_EXTRA_INDEX_URL:-}" ]; then
  echo "[venv-setup] ERROR: PIP_EXTRA_INDEX_URL is set, which is disallowed by project policy." >&2
  echo "[venv-setup] Use a single trusted index via PIP_INDEX_URL (default: https://pypi.org/simple)." >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip uninstall -y pygame >/dev/null 2>&1 || true
"$VENV_DIR/bin/python" -m pip install \
  --isolated \
  --disable-pip-version-check \
  --require-hashes \
  --only-binary=:all: \
  --index-url "$PIP_INDEX_URL" \
  -r "$ROOT_DIR/requirements.txt"

"$VENV_DIR/bin/python" - <<PY
import pygame
from pathlib import Path

target = Path(r"$ROOT_DIR") / "assets" / "dino-transparant.png"
try:
    pygame.image.load(str(target))
except Exception as exc:
    raise SystemExit(
        f"[venv-setup] ERROR: PNG decode test failed for {target}: {exc}"
    )
print(f"[venv-setup] PNG decode test: OK ({target.name})")
PY

echo "[venv-setup] Done."
echo "[venv-setup] Run game with: scripts/run_dino.sh"

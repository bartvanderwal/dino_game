#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv-web}"
STAGE_DIR="$ROOT_DIR/.web-build/stage"
OUTPUT_DIR="$ROOT_DIR/.web-build/output"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  echo "[web-build] Missing venv: $VENV_DIR"
  echo "[web-build] Run: scripts/web/setup_web.sh"
  exit 1
fi

echo "[web-build] Preparing stage folder..."
"$VENV_DIR/bin/python" - <<PY
import os
import shutil
from pathlib import Path

root = Path(r"$ROOT_DIR")
stage = Path(r"$STAGE_DIR")

if stage.exists():
    shutil.rmtree(stage)
stage.mkdir(parents=True, exist_ok=True)

# Entry point for pygbag should be main.py
shutil.copy2(root / "dino_game.py", stage / "main.py")

for file_name in ("shared.py", "api.md", "dino.md", "README.md"):
    src = root / file_name
    if src.exists():
        shutil.copy2(src, stage / file_name)

for folder_name in ("processing", "assets"):
    src = root / folder_name
    dst = stage / folder_name
    if src.exists():
        shutil.copytree(src, dst)

print(f"[web-build] Stage ready: {stage}")
PY

echo "[web-build] Running pygbag build..."
"$VENV_DIR/bin/python" -m pygbag --build "$STAGE_DIR"

echo "[web-build] Collecting build output..."
"$VENV_DIR/bin/python" - <<PY
import shutil
from pathlib import Path

stage = Path(r"$STAGE_DIR")
output = Path(r"$OUTPUT_DIR")
candidates = [
    stage / "build" / "web",
    stage / "build",
]

built = None
for candidate in candidates:
    if candidate.exists():
        built = candidate
        break

if built is None:
    raise SystemExit("[web-build] Could not find pygbag build output.")

if output.exists():
    shutil.rmtree(output)
output.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(built, output)
print(f"[web-build] Output copied to: {output}")
PY

echo "[web-build] Done."
echo "[web-build] Preview with: scripts/web/run_web.sh"

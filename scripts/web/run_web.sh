#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PORT="${PORT:-8000}"
OUTPUT_DIR="$ROOT_DIR/.web-build/output"

if [ ! -f "$OUTPUT_DIR/index.html" ]; then
  echo "[web-run] No web build found. Building first..."
  "$ROOT_DIR/scripts/web/build_web.sh"
fi

echo "[web-run] Serving $OUTPUT_DIR on http://localhost:$PORT"
python3 -m http.server "$PORT" --directory "$OUTPUT_DIR"

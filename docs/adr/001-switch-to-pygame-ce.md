# ADR 001: Switch Runtime Dependency From `pygame` To `pygame-ce`

## Status

Proposed (2026-04-29).

## Context

This `dino_game` repository uses a local `python-processing` runtime layer.

Historically, local environments used upstream `pygame`, while the web pipeline (`pygbag`) resolved `pygame` to a `pygame-ce` wheel in browser/WASM output. This runtime split increases debugging friction for web behavior.

## Options

### Option A: Keep upstream `pygame`

Keep local runtime on `pygame` and accept local/web runtime divergence.

### Option B: Switch to `pygame-ce`

Standardize local/runtime dependency on `pygame-ce` while keeping `import pygame` in source code.

## Decision

Use Option B.

Dependency direction for this repository is `pygame-ce`.

## Consequences

### Positive

- Local runtime aligns better with web runtime behavior used by `pygbag`.
- Fewer compatibility surprises while debugging browser builds.
- Active `pygame-ce` release cadence and support trajectory.

### Negative

- Environments must not keep both `pygame` and `pygame-ce` installed.
- Dependency lock maintenance is required when upgrading.

## Sources

- Local build artifact mapping evidence: `.web-build/output/cdn/index-0.9.3-cp312.json` (`"pygame"` resolves to `pygame_ce-...wasm...whl`).
- Project scripts and docs:
  - `scripts/web/build_web.sh`
  - `scripts/web/mirror_cdn.py`
  - `README.md`

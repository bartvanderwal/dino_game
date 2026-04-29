# Dependency Supply-Chain Policy

This project uses hash-locked requirements and a single trusted package index.

## Rules

- Do not use `--extra-index-url`.
- Use one trusted index only (default: `https://pypi.org/simple`).
- Install with:
  - `--isolated`
  - `--require-hashes`
  - `--only-binary=:all:`

These rules are enforced in:

- `scripts/setup_venv.sh`
- `scripts/web/setup_web.sh`

## Locked Requirement Files

- `requirements.txt`: runtime dependencies
- `requirements-web.txt`: web build dependencies

## Regeneration

When upgrading dependencies, regenerate lock files:

```bash
scripts/security/generate_requirements_locks.py
```

The generator reads wheel hashes from PyPI metadata and writes both lock files.

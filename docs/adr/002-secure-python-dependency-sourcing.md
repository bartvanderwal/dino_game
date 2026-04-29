# ADR 002: Harden Python Dependency Sourcing (Single Index + Hash-Locked Installs)

## Status

Proposed (2026-04-29).

## Context

Recent npm incidents confirm that trusted package names can still distribute malware when publishing credentials or release flows are compromised.

Paraphrase of authoritative incident data used here:

- GitHub Advisory `GHSA-fw8c-xr5c-95f9` classifies npm `axios` versions `1.14.1` and `0.30.4` as malware, and advises treating affected systems as fully compromised.
- Microsoft Threat Intelligence documents the March/April 2026 axios npm supply-chain compromise and cross-platform payload behavior.

For Python dependency sourcing, pip documentation states:

- multiple package locations have no priority order; pip evaluates available candidates and chooses the best version match;
- using `--extra-index-url` for private/public mixing is unsafe due to dependency confusion.

## Options

### Option A: Keep convenience defaults

Use permissive pip behavior and allow mixed indexes with `--extra-index-url`.

### Option B: Enforce strict sourcing policy

Use a single trusted index, hash-locked requirements, and binary-only installs.

## Decision

Use Option B.

Repository policy:

1. Single trusted index (`https://pypi.org/simple` by default).
2. Disallow `PIP_EXTRA_INDEX_URL` in setup scripts.
3. Require `--require-hashes`.
4. Require `--only-binary=:all:`.
5. Use `--isolated` in setup scripts.

Implemented in this repository:

- `requirements.txt` hash-locked runtime dependencies.
- `requirements-web.txt` hash-locked web build dependencies.
- `scripts/setup_venv.sh` and `scripts/web/setup_web.sh` enforce policy flags and reject `PIP_EXTRA_INDEX_URL`.
- `scripts/security/generate_requirements_locks.py` regenerates lock files from PyPI metadata.

## Consequences

### Positive

- Reduces dependency confusion risk from index mixing.
- Improves reproducibility and tamper detection via hashes.
- Reduces environment drift between local/CI/web installs.

### Negative

- Lock updates are explicit maintenance work.
- Builds may fail on platforms without matching wheels (intentional fail-closed behavior).

## Sources

GitHub. (2026, March 31). *Malware in axios (GHSA-fw8c-xr5c-95f9)*. GitHub Advisory Database. https://github.com/advisories/GHSA-fw8c-xr5c-95f9

Microsoft Threat Intelligence, & Microsoft Defender Security Research Team. (2026, April 1). *Mitigating the Axios npm supply chain compromise*. Microsoft Security Blog. https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/

pip maintainers. (2026). *pip install* (v26.0.1 documentation). https://pip.pypa.io/en/stable/cli/pip_install/

pip maintainers. (2026). *Secure installs* (v26.1 documentation). https://pip.pypa.io/en/stable/topics/secure-installs/

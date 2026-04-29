# ADR 003: Single-File Modular Monolith For `dino_game.py`

## Status

Proposed (2026-04-29).

## Context

The main game currently lives in `dino_game.py`, which is already more than 5000 lines and still appears workable for development with AI-assisted coding.

This repository intentionally investigates how far an AI-enhanced workflow can keep a growing game maintainable when most game logic remains in one file. The experiment is not only about classic monolith deployment, where a system is delivered as one unit instead of many services. Here, "monolith" also means a literal single source file for the game implementation.

The goal is still a modular monolith in structure: related code should be kept in coherent sections, with clear naming and local helper functions. The experiment should avoid premature extraction into many files, while making it obvious when the single-file approach starts to fail.

## Options

### Option A: Split by feature or subsystem now

Move player logic, bosses, shops, rendering helpers, audio, input, and level state into separate modules.

### Option B: Keep a single unstructured script

Keep all game code in one file without explicit internal organization.

### Option C: Use a single-file modular monolith

Keep the game implementation in `dino_game.py`, but treat it as a structured single-file modular monolith with coherent sections, stable helper boundaries, and deliberate naming.

## Decision

Use Option C.

`dino_game.py` remains the primary home for the game. New game features should default to staying in this file unless there is a concrete reason to extract.

Preferred name for this architecture in this repository: **single-file modular monolith**.

Working rules:

1. Keep related state, constants, helpers, update logic, draw logic, and input handling grouped as coherently as possible.
2. Prefer small named helper functions over large inline blocks.
3. Avoid cross-section coupling where a local helper can make intent clearer.
4. Do not extract modules only because the file is large.
5. Reconsider this ADR when navigation, review, testing, or AI edits become consistently unreliable.

## Consequences

### Positive

- Preserves local reasoning: most game behavior is visible in one file.
- Reduces import churn and module-boundary overhead while the design is still changing quickly.
- Gives a useful experiment for AI-driven or AI-enhanced development at 5000+ lines.
- Makes generated edits easier to inspect as one coherent patch surface.

### Negative

- File navigation may become slower for humans.
- Merge conflicts may become more likely when multiple changes touch the same file.
- Hidden coupling can accumulate if sections are not kept disciplined.
- Unit testing individual subsystems may be harder than with extracted modules.

## Sources

- Local game implementation: `dino_game.py`.
- Local AI-agent guidance: `AGENTS.md`.
- Local Processing API reference: `api.md`.

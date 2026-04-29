# ADR 000: ADR Format And Conventions

## Status

Proposed (2026-04-29).

## Context

The repository needs a single ADR format so decisions are readable, comparable, and searchable over time.

We want to use the Nygard ADR style, with two explicit additions:

- an `Options` section directly after `Context`
- an unnumbered `Sources` section for references

## Options

### Option A: Free-form ADR structure

Allow each ADR author to choose headings and structure ad hoc.

### Option B: Strict standard structure

Require a fixed set of H2 sections for all ADRs.

## Decision

Use Option B.

All ADRs must use this structure:

1. `Status`
2. `Context`
3. `Options`
4. `Decision`
5. `Consequences`
6. `Sources`

Additional content is allowed only as H3 sections nested under one of these six H2 sections.

Numbering convention:

- filenames use three digits: `000-...`, `001-...`, `002-...`
- we do not use four-digit ADR numbering

## Consequences

### Positive

- Consistent review and easier comparison between decisions.
- Explicit alternatives in `Options` improves decision quality.
- Traceability improves by requiring `Sources`.

### Negative

- Slightly more authoring overhead.
- Existing ADRs may need periodic normalization if they drift.

## Sources

- Nygard, M. (2011). *Documenting architecture decisions*. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions

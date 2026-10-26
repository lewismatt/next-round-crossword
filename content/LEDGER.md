<!-- SPDX-License-Identifier: Apache-2.0 -->

# Crossword — Puzzle Library Contributions Ledger

*Opened 2026-10-26, when this repository was extracted from the
platform monorepo. This ledger is the single coordination point for
the puzzle library — who drafted what, where it stands in review
and in the D54 gates, and what is banked — so contributions never
collide and nothing is double-counted. The authoring spec is
`docs/puzzle-authoring/BRIEF.md`; the bundled library lives in
`content/` beside this file.*

## How entries work

- **Statuses:** Drafted → In review → D54 gates (editorial →
  correctness → cold playtest → written CC0-1.0 attestation) →
  **Banked** (moved into `content/`, pins updated in
  `src/bundled-content.test.ts`), with any of: corrections made in
  review, drafts held as reviewed spares, drafts excluded (with the
  reason).
- A contribution counts as received only when its template arrives
  in `content/contributions/` and passes
  `tools/validate_puzzle.py`.
- The reviewer checks grid/clue correctness and clue originality,
  dedupes against the library by grid identity, and records the
  disposition here. Banking additionally requires the completed
  D54 gates — the author of record is Matthew Lewis for every
  banked puzzle; the drafter is recorded per puzzle.
- Grid identities are never renumbered; a re-clued grid is a new
  version of the same puzzle identity, recorded as such.

## Library status

*As of the extraction, 2026-10-26: **3 puzzles** banked, all
import-ready in `content/`.*

| File | Title | Difficulty | Identity (SHA-256) | Status |
| --- | --- | --- | --- | --- |
| `warm-up.json` | Warm Up | easy | `012b04f7…` | Banked |
| `game-night.json` | Game Night | easy | `676d7d84…` | Banked |
| `rural-route.json` | Rural Route | medium | `56e971e5…` | Banked |

## Entries

### Launch library — larry (drafted 2026-10-20, banked 2026-10-21)

- **Warm Up** (5×5, easy), **Game Night** (5×5, easy),
  **Rural Route** (5×5, medium). Drafted by Larry under D54 in the
  platform's authoring kit; author of record, rights reviewer and
  playtester Matthew Lewis. All four D54 gates completed
  2026-10-21 (editorial review, correctness review, clean cold
  playtest, written CC0-1.0 attestation; attestation wording adopted
  verbatim 2026-10-22). Bundled into the platform repo by PR #40
  (merged 2026-10-21) and carried byte-identical into this
  repository at extraction; identities and raw-file digests are
  pinned by `src/bundled-content.test.ts`.

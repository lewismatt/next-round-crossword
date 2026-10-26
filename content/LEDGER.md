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
import-ready in `content/`. Drafts in `content/contributions/`:
**6** (see the 2026-10-26 entry below).

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

### Six minis — larry (drafted 2026-10-26)

- **Ghost Story** (5x5, easy, identity `d78fed81…`),
  **Fresh Start** (5x5, easy, `0d8bc105…`),
  **House of Cards** (5x5, easy, `8d48ab18…`),
  **In the Garden** (5x5, easy, `65613798…`),
  **Honor System** (5x5, medium, `321876f2…`),
  **Road Trip** (5x5, medium, `47c88ddc…`). Drafted by Larry at
  Matthew's request ("generate 6 more crosswords"). Fills were
  produced by a wordlist-constrained search over the
  public-domain google-10000-english frequency list and then
  hand-screened entry by entry: common words only, no
  abbreviations or initialisms; the single proper noun is ESSEX
  (an English county) in Road Trip. All clues were written by the
  drafter for these grids. Validator PASS on all six templates.
  Status: **Drafted — in review**. Banking awaits the D54 gates
  with the author of record: editorial review, correctness
  review, clean cold playtest, written CC0-1.0 attestation.
  Import JSONs deliberately not generated — the validator's
  `--write` rights block asserts attestation, so JSONs are
  emitted at banking time (the launch-puzzle precedent).

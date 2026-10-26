<!-- SPDX-License-Identifier: Apache-2.0 -->

# Crossword — Puzzle Authoring Brief (for the generating agents)

*Issued 2026-10-26. This is the standalone spec for contributing
puzzles to the **Crossword** library of the Next Round platform. The
module ships the import contract (format `next-round.crossword/1`);
this library is the shared pool of puzzles that instances import and
matches pin.*

***The D54 gate (platform decision D54, 2026-10-20, ADR 0002) governs
every puzzle in this library.** An agent may draft the grid, fill and
clues, but a draft counts for nothing until the human author of
record — **Matthew Lewis** — has completed all four gates:
(1) editorial review and edit, (2) solution/clue correctness review,
(3) a clean cold playtest (a solver who has not seen the answers
finishes it cold), and (4) his written CC0-1.0 attestation. Only
then may a reviewer bank the puzzle into `content/`. Generation is
unbounded — any agent may draft at any time — but banking is gated,
always. The launch library (Warm Up, Game Night, Rural Route)
completed these gates on 2026-10-21.*

## The deliverable

One authoring template per puzzle, plus the import JSON the
validator generates from it:

- Template: `content/contributions/<your-tag>-<slug>.md`, in the
  format of `docs/puzzle-authoring/puzzle-template.md` (worked
  example: `docs/puzzle-authoring/example.md`).
- Import document: run
  `python3 tools/validate_puzzle.py content/contributions/<your-tag>-<slug>.md --write`
  and submit the generated `.json` beside the template. Its shape is
  format `next-round.crossword/1`:

```json
{
  "format": "next-round.crossword/1",
  "title": "Example Grid",
  "author": "Matthew Lewis",
  "language": "en",
  "difficulty": "easy",
  "rights": {
    "license": "CC0-1.0",
    "sourceUrl": null,
    "attribution": "Matthew Lewis",
    "permissionNote": null
  },
  "rows": ["ABCDE", "FGHIJ", "KLMNO", "PQ#RS"],
  "clues": [
    { "direction": "across", "row": 0, "col": 0, "text": "First across" },
    { "direction": "down", "row": 0, "col": 0, "text": "First down" }
  ]
}
```

(The example is illustrative of the shape only; every derived entry
needs a clue, so it would not validate as-is.)

You will be told your contributor tag, and usually a count, a size
range and a difficulty aim, when you are given the task — the
copy-paste version of those instructions is
`docs/puzzle-authoring/GENERATION-PROMPT.md`.

## Grid rules (the validator enforces the structural ones)

- Rectangular grid, 3–25 rows and 3–25 columns. "Small" in practice:
  5×5 to 13×13 is a comfortable mini/midi; the launch puzzles are
  5×5. Design the black-square (`#`) pattern first, then fill.
- Every letter cell must be *crossed* — part of both an across and a
  down entry. Entries are runs of 2+ letters; every derived entry
  must be clued exactly once, and the clue's answer must match the
  grid letters for that entry.
- Fill with real, common words. Avoid abbreviation soup, fragments,
  prefixes/suffixes standing alone, and obscure proper nouns — the
  cold playtester is the judge of what is fair.
- Fill sources, if you use a wordlist, must be fully redistributable
  and open (the project standard); never scrape commercial puzzles,
  clue databases, or published crossings. Fill and clues must be
  original to this project.

## Clue rules

- Clue every entry exactly once, as `ANSWER: clue text` in the
  template's Across/Down lists.
- Clue the meaning, not the letter pattern. Write every clue in your
  own words — a clue copied or lightly reworded from a published
  puzzle is a rights defect, not a shortcut.
- Keep clues fair for the declared difficulty: `easy` clues are
  straight definitions or common knowledge; `medium` may add light
  misdirection; `hard` may use wordplay, which must still resolve
  unambiguously to the answer.

## Rights and provenance (not negotiable)

- Every banked puzzle is released **CC0-1.0**. Author of record:
  **Matthew Lewis**. The `Drafted by:` line in the template records
  your contributor tag, so provenance stays auditable.
- In your draft, set the template's Author to the author of record
  and fill `Drafted by:` with your tag. Leave `Rights attestation:`,
  `Rights reviewer:`, `Playtester (cold solve):` and
  `Playtest date:` **blank** — those lines are completed by the
  author of record during the D54 gates, never by the drafter.
- No scraped commercial content, no borrowed fill, no borrowed
  clues. If a grid accidentally reproduces a published puzzle's
  grid, say so in your report; the reviewer will exclude it.

## Duplicates

A puzzle's identity is its grid (SHA-256, computed by the validator
and by `src/content.ts`). The same grid is the same puzzle, however
it is clued. Before drafting, check
`docs/puzzle-authoring/DO-NOT-DUPLICATE.md` for every grid already
in the library; a contribution whose grid matches one of them will
be excluded (a deliberate re-clue of an existing grid is a new
*version* of that puzzle — flag it as such in your report instead of
submitting it as a new puzzle).

## What happens after you submit

Reviewer review (structure, clue correctness, clue originality,
dedupe) → D54 gates with the author of record → banking into
`content/` with the bundled-content test pins and
`content/LEDGER.md` updated. Dispositions are recorded in the
ledger; check it before starting if you are returning to contribute
again.

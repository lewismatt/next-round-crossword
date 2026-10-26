<!-- SPDX-License-Identifier: Apache-2.0 -->

# Working in this repository — read this first

This repo is **Crossword**, a game module for the Next Round platform
(`@next-round/game-crossword`, currently 0.1.0). It contains two kinds
of work: the game module code (`src/`) and the puzzle library
(`content/`). Most agent visits here are for the puzzle library.

## If you were told to generate crosswords

That is a **puzzle contribution**. Do exactly this, in order:

1. Read `docs/puzzle-authoring/BRIEF.md` — the full authoring spec
   (format, grid and clue rules, rights, and the D54 gate). It
   governs; this file only points at it.
2. Read `docs/puzzle-authoring/DO-NOT-DUPLICATE.md` — every grid
   already in the library. A puzzle's identity is its grid: your
   grid must not repeat one of them.
3. Draft each puzzle as an authoring template (format:
   `docs/puzzle-authoring/puzzle-template.md`; worked example:
   `docs/puzzle-authoring/example.md`) and write your set as **new
   files** in `content/contributions/`, named
   `<your-tag>-<slug>.md`, one file per puzzle. (If the prompt still
   carries a placeholder like `YOURTAG`, ask the user for the
   lowercase contributor tag before writing anything.)
4. Run the validator on every draft and make it pass:
   `python3 tools/validate_puzzle.py content/contributions/<your-tag>-<slug>.md`
   Do **not** use `--write`, and do not submit a `.json`: the import
   document's rights block asserts the author of record's
   attestation, so the reviewer generates it only when a gated
   puzzle is banked. Your deliverable is the template alone.
5. Self-review before you report back: solve every clue against the
   fill yourself; check every entry is clued exactly once, every
   answer matches the grid, every letter is crossed, and the clues
   are your own wording (no published puzzle's clues, no scraped
   content of any kind).
6. Report: the file paths, each puzzle's title, size and difficulty,
   its identity hash from the validator, and the validator's result
   for each file.

**The D54 gate is binding.** A contributed puzzle is a *draft* and
counts for nothing until the human author of record (Matthew Lewis)
has completed all four gates: editorial review, solution/clue
correctness review, a clean cold playtest by a solver who has not
seen the answers, and his written CC0-1.0 attestation. Leave the
template's attestation, rights-reviewer and playtester lines blank —
they are his to complete, never yours.

**Never edit the bundled puzzles in `content/` directly, and never
move a draft there yourself.** The library changes only when a
reviewer banks a gated puzzle (which includes updating the pins in
`src/bundled-content.test.ts` and the ledger). Never edit another
contributor's files in `content/contributions/`. **Never edit this
file, the brief, or the generation prompt as part of a contribution**
— if the spec looks wrong, say so in your report and let the
reviewer change it.

### The flow, end to end

```
generate → draft templates in content/contributions/
         → validator PASS (you run it)
         → reviewer review: grid/clue correctness, clue originality,
           dedupe against the library (grid identity)
         → D54 gates with the author of record: editorial review,
           correctness review, clean cold playtest, written
           CC0-1.0 attestation
         → reviewer banks the puzzle into content/, updates the
           bundled-content test pins and content/LEDGER.md,
           regenerates DO-NOT-DUPLICATE.md
         → publish to git with CI green
```

The D54 gate is the binding constraint on library growth, not
generation speed. A draft the author of record has not gated does
not land, however good it looks.

## Module code basics

The platform packages are not on a registry; they are linked from a
pinned core checkout in `.core/`:

```sh
pnpm setup     # fetch pinned core, install, build platform packages
pnpm build
pnpm typecheck
pnpm test
```

- Puzzle format is `next-round.crossword/1`. A puzzle's identity is
  the SHA-256 of its canonical grid document (see `src/content.ts`);
  the same grid keeps one identity, and changed clues or metadata
  create a new immutable content version of it.
- `content/warm-up.json`, `content/game-night.json` and
  `content/rural-route.json` are the bundled launch puzzles, banked
  under D54 in 2026-10. Their bytes are pinned by
  `src/bundled-content.test.ts`; do not reformat or regenerate them.
- Import happens through the platform: an administrator imports a
  puzzle document via `POST /api/v1/admin/games/crossword/import`;
  puzzles are never embedded in code or the browser bundle.

## Publishing note

Publish repo changes only as complete, CI-green states — a red
validation step in CI means a draft or the library file is malformed.

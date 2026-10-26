<!-- SPDX-License-Identifier: Apache-2.0 -->

# Crossword Generation — Prompt Template

*For the operator: copy everything inside the fence, fill the four
slots, and hand it to any agent with access to this repository. The
agent needs no other context — the repository tells it the rest.
Generation is unbounded, but banking is gated by D54 (see the
brief): every puzzle an agent drafts remains a draft until Matthew
Lewis completes the editorial review, correctness review, clean
cold playtest, and written CC0-1.0 attestation.*

```
You are contributing crossword puzzles to the Crossword library in
this repository (a Next Round game module). Work only in this repo.

ASSIGNMENT
- Count: {COUNT} puzzle(s)
- Size and difficulty aim: {SIZE_AND_DIFFICULTY}  (e.g. "two 5x5 easy, one 7x7 medium")
- Your contributor tag: {TAG}
- Theme or notes: {NOTES}  (or "none")

BEFORE YOU WRITE ANYTHING
1. Read AGENTS.md at the repository root.
2. Read docs/puzzle-authoring/BRIEF.md in full — it is the governing
   spec: grid and clue rules, rights, and the D54 gate.
3. Read docs/puzzle-authoring/DO-NOT-DUPLICATE.md — every grid
   already in the library. Your grids must not repeat any of them;
   a puzzle's identity is its grid.

DELIVERABLE — one template + one generated JSON per puzzle
- Template path: content/contributions/{TAG}-{SLUG}.md, in the
  format of docs/puzzle-authoring/puzzle-template.md (worked
  example: docs/puzzle-authoring/example.md).
- Set Author to "Matthew Lewis" (the author of record) and
  "Drafted by:" to {TAG}. Leave the attestation, rights-reviewer,
  playtester and playtest-date lines BLANK — those belong to the
  author of record's D54 gates, never to the drafter.
- Grid: rectangular, # for black squares, one letter A-Z per cell;
  every letter crossed (in both an across and a down entry); every
  entry of 2+ letters clued exactly once as "ANSWER: clue text".
  Fill: real, common words only — no abbreviation soup, fragments,
  or obscure proper nouns. Clues: your own words, clueing the
  meaning; nothing copied or adapted from published puzzles.
- Generate the import JSON:
    python3 tools/validate_puzzle.py content/contributions/{TAG}-{SLUG}.md --write
  and submit the generated .json beside the template.

VALIDATE BEFORE YOU REPORT
Run the validator (without --write) on every template; fix
everything it flags and re-run until every puzzle passes. Then
solve every clue against the fill yourself as a final check.

REPORT
The file paths; each puzzle's title, size, difficulty and identity
hash (the validator prints it); and the validator result per file.

DO NOT
- Do not edit the bundled puzzles in content/, src/, or
  content/LEDGER.md — banking, pins and ledger entries are the
  reviewer's steps, after the D54 gates.
- Do not edit AGENTS.md, docs/puzzle-authoring/BRIEF.md, or this
  prompt template. If the spec looks wrong or incomplete, say so
  in your report — spec changes are the reviewer's/operator's to
  make.
- Do not fill in the attestation, rights-review or playtest lines,
  and do not describe a draft as reviewed, playtested, attested or
  banked. It is a draft until the author of record gates it.
```

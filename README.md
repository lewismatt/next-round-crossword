<!-- SPDX-License-Identifier: Apache-2.0 -->

# Crossword — a Next Round game module

**Crossword** is the first full game built for
[Next Round](https://github.com/lewismatt/next-round), the self-hosted
turn-based game platform: collaborative and solo crossword play with
real-time clue solving, turn coordination, exposure tracking, and
score accounting.

This repository is the module's home — the game code (`src/`) and the
puzzle library (`content/`) — extracted from the platform monorepo on
2026-10-26 so the module and its library evolve independently,
exactly like the platform's other games (Cipher, Trivia, Golden
Ladder). The platform bundles this module as a fetched workspace
package at a pinned commit (`scripts/fetch-crossword.sh` in the
platform repo).

License: Apache-2.0 for the code; the bundled puzzles are CC0-1.0.

## Contributing a puzzle

Any agent can draft puzzles for the library — start with
[`AGENTS.md`](AGENTS.md), then the governing spec,
[`docs/puzzle-authoring/BRIEF.md`](docs/puzzle-authoring/BRIEF.md).
The copy-paste assignment form is
[`docs/puzzle-authoring/GENERATION-PROMPT.md`](docs/puzzle-authoring/GENERATION-PROMPT.md).

One rule shapes everything: under platform decision **D54**, a draft
counts for nothing until the human author of record (Matthew Lewis)
has completed the editorial review, correctness review, clean cold
playtest, and written CC0-1.0 attestation. Drafts land in
`content/contributions/`; only gated puzzles are banked into
`content/`, with dispositions recorded in `content/LEDGER.md`.

## Working on the module

The platform packages this module depends on
(`@next-round/contracts`, `@next-round/game-sdk`,
`@next-round/game-client`) are not published to a registry; they are
linked from a pinned checkout of the platform repo in `.core/`:

```sh
pnpm setup     # fetch pinned core, install, build platform packages
pnpm build
pnpm typecheck
pnpm test
```

## What this module contains

| File              | Purpose                                                                                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/manifest.ts` | Module contract: modes, capabilities, settings, action payloads, state, authorized view, result and the import/metadata/data/facts resource schemas.                      |
| `src/content.ts`  | The C1 content contract: document validation, grid and clue derivation, row-major clue numbering, the rights allowlist and the SHA-256 puzzle identity. Server-side only. |
| `src/server.ts`   | The C2-C4 rules as a pure reducer over the pinned resource snapshot: turns, counters, scoring, reveals, exposure, disabled members and career exclusions.                 |
| `src/types.ts`    | The shared state, settings and authorized-view types used by the server and the browser client.                                                                           |
| `src/client.ts`   | The browser client: grid, clue lists, explicit word submission, cell typing, private feedback and the game controls. It imports no server code.                           |

## Content and import

A puzzle is a `next-round.crossword/1` JSON document with a rectangular grid of
`#` and `A–Z` cells and exactly one clue per derived entry. An administrator
imports it through `POST /api/v1/admin/games/crossword/import`; the platform
stores the private content, the public catalog metadata and the importer's
exposure fact. The same grid keeps one identity, and changed clues or metadata
create a new immutable content version. A match pins one resource version.

```json
{
  "format": "next-round.crossword/1",
  "title": "Example Grid",
  "author": "Next Round",
  "language": "en",
  "difficulty": "easy",
  "rights": {
    "license": "CC0-1.0",
    "sourceUrl": null,
    "attribution": "Next Round",
    "permissionNote": null
  },
  "rows": ["ABCDE", "FGHIJ", "KLMNO", "PQ#RS"],
  "clues": [
    { "direction": "across", "row": 0, "col": 0, "text": "First across" },
    { "direction": "down", "row": 0, "col": 0, "text": "First down" }
  ]
}
```

The example above is incomplete on purpose: every derived entry needs a clue.

## Bundled puzzles

The three launch puzzles ship in [`content/`](content/) as import documents
in the format above, ready for an administrator to import through the Admin
library on any instance:

| File | Title | Difficulty | Identity (SHA-256) |
| --- | --- | --- | --- |
| `warm-up.json` | Warm Up | easy | `012b04f75fc188d6553809581784c8bdd40200cf5c8f9a78a065c204d1f9a4ba` |
| `game-night.json` | Game Night | easy | `676d7d8434586b3aaece4723fc67e4c401eed8bb5ea5e42d1c003c26cc201d9b` |
| `rural-route.json` | Rural Route | medium | `56e971e524c52eed8b37b897353dee333744cb8700564d5c79367c191192d3a3` |

Provenance (D54 / ADR 0002): drafted by an agent (Larry) under a named human
author of record, Matthew Lewis, who completed the editorial review,
solution/clue correctness review and clean cold playtest and signed the
written CC0-1.0 attestation on 2026-10-21; the full record lives in
`content/LEDGER.md`. `src/bundled-content.test.ts` parses each bundled
file through the real import contract, pins its grid identity and complete
rights block, and checks a separate raw-file SHA-256 digest covering every
byte.

## Specification reference

- **Module ID**: `crossword`
- **SDK Contract**: `next-round-game/0.1`
- **Modes**:
  - `solo` (min 1, max 1)
  - `quick` (min 2, max 8)
  - `custom` (min 2, max 8)
- **Capabilities**: `chat: true`, `deadlines: true`, `solo: true`, `resources: true`, `careerStats: true`.
- **Governing specs** (in the platform repo): Master Specification v1.2
  §2 (wire contracts and game SDK), §9 (approved crossword module), §10
  (build slices and acceptance gates).

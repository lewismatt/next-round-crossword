#!/usr/bin/env python3
# Validate a Next Round crossword authoring template and, on request, emit the
# next-round.crossword/1 import JSON. Rules per master spec section 9 (C1).
# Usage: validate_puzzle.py <puzzle.md> [--write]
import hashlib
import json
import re
import sys
from pathlib import Path

def fail(errors, msg):
    errors.append(msg)

def parse_template(text):
    fields = {}
    for key in ("Title", "Author", "Difficulty"):
        m = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
        fields[key.lower()] = m.group(1).strip() if m else ""
    def code_block_after(heading):
        i = text.find(heading)
        if i < 0:
            return None
        m = re.search(r"```\n(.*?)```", text[i:], re.DOTALL)
        return m.group(1) if m else None
    grid_raw = code_block_after("## Grid")
    across_raw = code_block_after("Clues — Across") or code_block_after("Clues - Across")
    down_raw = code_block_after("Clues — Down") or code_block_after("Clues - Down")
    return fields, grid_raw, across_raw, down_raw

def parse_clues(raw):
    clues = {}
    dupes = []
    if raw is None:
        return clues, dupes
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^([A-Za-z]+)\s*:\s*(.+)$", line)
        if not m:
            dupes.append(f"unparseable clue line: {line!r}")
            continue
        ans, txt = m.group(1).upper(), m.group(2).strip()
        if ans in clues:
            dupes.append(f"duplicate clue for {ans}")
        clues[ans] = txt
    return clues, dupes

def entries(rows, horizontal):
    out = []  # (answer, row, col)
    R, C = len(rows), len(rows[0])
    lines = rows if horizontal else ["".join(rows[r][c] for r in range(R)) for c in range(C)]
    for i, line in enumerate(lines):
        for m in re.finditer(r"[^#]+", line):
            if len(m.group(0)) >= 2:
                r, c = (i, m.start()) if horizontal else (m.start(), i)
                out.append((m.group(0), r, c))
    return out

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    write = "--write" in sys.argv
    text = path.read_text(encoding="utf-8")
    fields, grid_raw, across_raw, down_raw = parse_template(text)
    errors = []

    if grid_raw is None:
        print("ERROR: no ## Grid code block found")
        return 1
    normalized_note = False
    rows = []
    for line in grid_raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line != line.upper():
            normalized_note = True
        rows.append(line.upper())

    # --- structural validation (spec C1) ---
    if not rows:
        fail(errors, "grid is empty")
    R = len(rows)
    C = len(rows[0]) if rows else 0
    if any(len(r) != C for r in rows):
        fail(errors, "grid is not rectangular")
    if not (3 <= R <= 25 and 3 <= C <= 25):
        fail(errors, f"grid must be 3-25 rows and columns (got {R}x{C})")
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != "#" and not ("A" <= ch <= "Z"):
                fail(errors, f"invalid character {ch!r} at row {r}, col {c}")
    open_cells = {(r, c) for r in range(R) for c in range(C) if rows[r][c] != "#"}
    if not open_cells:
        fail(errors, "grid has no open cells")
    else:
        start = next(iter(open_cells))
        seen, stack = {start}, [start]
        while stack:
            r, c = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (r + dr, c + dc)
                if n in open_cells and n not in seen:
                    seen.add(n)
                    stack.append(n)
        if seen != open_cells:
            fail(errors, f"open cells are not all connected ({len(open_cells) - len(seen)} unreachable)")

    across = entries(rows, True)
    down = entries(rows, False)
    in_across = set()
    for ans, r, c in across:
        in_across.update((r, c + k) for k in range(len(ans)))
    in_down = set()
    for ans, r, c in down:
        in_down.update((r + k, c) for k in range(len(ans)))
    for cell in sorted(open_cells):
        if cell not in in_across or cell not in in_down:
            fail(errors, f"cell row {cell[0]}, col {cell[1]} is not in both an across and a down entry (uncrossed or one-cell entry)")

    # --- metadata validation ---
    title, author = fields["title"], fields["author"]
    difficulty = fields["difficulty"].lower()
    if not (1 <= len(title) <= 120):
        fail(errors, "title must be 1-120 characters")
    if not (1 <= len(author) <= 120):
        fail(errors, "author must be 1-120 characters")
    if difficulty not in ("easy", "medium", "hard", "unspecified"):
        fail(errors, f"difficulty must be easy|medium|hard|unspecified (got {difficulty!r})")
    for label, value in (("title", title), ("author", author)):
        if re.search(r"[<>]|[\x00-\x1f\x7f]", value):
            fail(errors, f"{label} contains HTML or control characters")

    # --- clue validation ---
    across_clues, a_dupes = parse_clues(across_raw)
    down_clues, d_dupes = parse_clues(down_raw)
    for d in a_dupes + d_dupes:
        fail(errors, d)
    def check_clues(clues, ents, direction):
        want = {ans: (r, c) for ans, r, c in ents}
        for ans in want:
            if ans not in clues:
                fail(errors, f"missing {direction} clue for entry {ans} (row {want[ans][0]}, col {want[ans][1]})")
        for ans, txt in clues.items():
            if ans not in want:
                fail(errors, f"{direction} clue {ans} does not match any grid entry")
            if not (1 <= len(txt) <= 500):
                fail(errors, f"{direction} clue for {ans} must be 1-500 characters")
            if re.search(r"[<>]|[\x00-\x1f\x7f]", txt):
                fail(errors, f"{direction} clue for {ans} contains HTML or control characters")
        return [{"direction": direction, "row": want[ans][0], "col": want[ans][1], "text": clues[ans]}
                for ans in sorted(want, key=lambda a: (want[a][0], want[a][1])) if ans in clues]
    clue_list = check_clues(across_clues, across, "across") + check_clues(down_clues, down, "down")

    if errors:
        print(f"FAIL — {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    identity_src = json.dumps({"format": "next-round.crossword.identity/1", "rows": rows},
                              separators=(",", ":"), ensure_ascii=False)
    identity = hashlib.sha256(identity_src.encode("utf-8")).hexdigest()
    print(f"PASS — {R}x{C} grid, {len(across)} across + {len(down)} down entries, all clued and crossed.")
    if normalized_note:
        print("Note: lowercase grid letters were normalized to uppercase.")
    print(f"Identity (SHA-256): {identity}")

    if write:
        doc = {
            "format": "next-round.crossword/1",
            "title": title,
            "author": author,
            "language": "en",
            "difficulty": difficulty,
            "rights": {
                "license": "CC0-1.0",
                "sourceUrl": None,
                "attribution": author,
                "permissionNote": f"Original work by {author}, released under CC0-1.0 (attested in the authoring kit).",
            },
            "rows": rows,
            "clues": clue_list,
        }
        out = path.with_suffix(".json")
        out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote import file: {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

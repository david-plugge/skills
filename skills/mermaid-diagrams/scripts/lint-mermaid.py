#!/usr/bin/env python3
"""Lint Mermaid code blocks in Markdown for the syntax footguns that cause
"Parse error" / "Lexical error" at render time.

Usage:
    lint-mermaid.py FILE [FILE ...]

Heuristic checks (no dependencies). If `mmdc` (mermaid-cli) is on PATH, each
file is ALSO passed through a real render-parse for authoritative validation.

Exit code: 0 = clean, 1 = findings, 2 = bad invocation.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass

# Unicode glyphs that break stricter parsers / render inconsistently.
BAD_GLYPHS = "→←⇒⇐↔▷◁⊳⊲⟶⟵➜➔»«"

# Allowed angle-bracket usages inside labels (line breaks only).
BR_RE = re.compile(r"</?br\s*/?>", re.IGNORECASE)
FENCE_RE = re.compile(r"^([ \t]*)```+\s*mermaid\s*$", re.IGNORECASE)
CLOSE_RE = re.compile(r"^([ \t]*)```+\s*$")


@dataclass
class Finding:
    line: int
    rule: str
    text: str


def diagram_type(block_lines: list[str]) -> str:
    for ln in block_lines:
        s = ln.strip()
        if s and not s.startswith("%%"):
            return s.split()[0].lower()
    return ""


def is_note_or_message(line: str, dtype: str) -> bool:
    s = line.strip()
    if dtype.startswith("sequence"):
        if s.lower().startswith("note "):
            return True
        # message lines: A->>B: text  /  A-->>B: text  /  A-)B: text
        if re.search(r"-(>>|->|\)|x)?\s*[A-Za-z0-9_]+\s*:", s):
            return True
    return False


def check_line(line: str, lineno: int, dtype: str) -> list[Finding]:
    out: list[Finding] = []
    stripped = line.strip()

    # Skip mermaid directives / comments / styling lines.
    if stripped.startswith("%%"):
        return out

    note_or_msg = is_note_or_message(line, dtype)

    # 1. Semicolon inside a sequence note/message -> statement separator.
    if note_or_msg and ";" in line:
        out.append(Finding(lineno, "semicolon-in-note",
                           "';' separates statements in sequence diagrams; use ',' or split the note"))

    # 2. Non-ASCII arrow/glyph anywhere in the diagram.
    for g in BAD_GLYPHS:
        if g in line:
            out.append(Finding(lineno, "unicode-arrow",
                               f"glyph {g!r} breaks strict parsers; use an ASCII word (then/over/->)"))
            break

    # 3. Raw angle brackets that are not <br>.
    without_br = BR_RE.sub("", line)
    if "<" in without_br or ">" in without_br:
        # '>' appears legitimately in arrows (-->, ->>). Only flag inside quoted
        # labels, note text, or bracketed labels.
        if note_or_msg or '"' in line or re.search(r"[\[(]{[^}]", line):
            if "<" in without_br:
                out.append(Finding(lineno, "raw-angle-bracket",
                                   "raw '<...>' is parsed as HTML; escape as &lt; &gt; or drop it"))

    # 4. Inline-text edge labels: A -. text .-> B  /  A -- text --> B
    #    These collide with '.' '/' ':' '(' in the label. Recommend pipe form.
    inline_edge = re.search(r"-(\.|-)\s+[^|>\n]*[./:()][^|>\n]*\s(\.|-)?-?->", line)
    if inline_edge:
        out.append(Finding(lineno, "inline-edge-label",
                           'punctuation in inline edge text breaks tokenizer; use A -->|"text"| B'))

    # 5. Reserved word 'end' used as a node id (lowercase, flow/graph only).
    if dtype.startswith(("flowchart", "graph")):
        if re.match(r"^\s*end\s*[\[({]", line):
            out.append(Finding(lineno, "reserved-end",
                               "'end' is reserved; rename the node id"))

    return out


def lint_file(path: str) -> list[Finding]:
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        return [Finding(0, "io-error", str(exc))]

    findings: list[Finding] = []
    in_block = False
    block: list[str] = []
    block_start = 0

    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if not in_block:
            if FENCE_RE.match(line):
                in_block = True
                block = []
                block_start = i
            continue
        if CLOSE_RE.match(line):
            dtype = diagram_type(block)
            for off, bl in enumerate(block):
                findings.extend(check_line(bl, block_start + 1 + off, dtype))
            in_block = False
            continue
        block.append(line)

    if in_block:
        findings.append(Finding(block_start, "unclosed-block",
                               "mermaid code fence is never closed"))
    return findings


def mmdc_validate(path: str) -> list[Finding]:
    """Authoritative parse via mermaid-cli, if available."""
    mmdc = shutil.which("mmdc")
    if not mmdc:
        return []
    with tempfile.NamedTemporaryFile(suffix=".md", delete=True) as tmp:
        try:
            proc = subprocess.run(
                [mmdc, "-i", path, "-o", tmp.name],
                capture_output=True, text=True, timeout=120,
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            return [Finding(0, "mmdc-error", str(exc))]
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout).strip()
        return [Finding(0, "mmdc-parse-fail", msg[:800] or "mmdc rejected the file")]
    return []


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2

    total = 0
    used_mmdc = shutil.which("mmdc") is not None
    for path in argv[1:]:
        findings = lint_file(path)
        findings += mmdc_validate(path)
        if findings:
            total += len(findings)
            print(f"\n{path}: {len(findings)} finding(s)")
            for f in sorted(findings, key=lambda x: (x.line, x.rule)):
                loc = f"line {f.line}" if f.line else "file"
                print(f"  {loc} [{f.rule}] {f.text}")
        else:
            print(f"{path}: clean")

    print()
    print(f"mermaid-cli render check: {'ON' if used_mmdc else 'OFF (install mermaid-cli for authoritative parse)'}")
    if total:
        print(f"FAIL: {total} finding(s) — fix and re-run.")
        return 1
    print("OK: no findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

---
name: mermaid-diagrams
description: Author and edit Mermaid diagrams in Markdown that render cleanly on GitHub, VS Code, and mermaid.js. Use when creating, editing, or debugging Mermaid diagrams or ```mermaid code blocks, or when a Mermaid "Parse error" / "Lexical error" occurs.
---

# Mermaid Diagrams

Write Mermaid that parses on the first try. Most failures come from a small set
of characters that have grammar meaning inside labels and notes. Follow the
rules below, then **always run the linter** before declaring a diagram done.

## Quick start

After writing or editing any ```mermaid block, validate it:

```bash
python3 ~/.claude/skills/mermaid-diagrams/scripts/lint-mermaid.py path/to/file.md
```

The script flags the known footguns and, if `mmdc` (mermaid-cli) is installed,
also does a real render-parse of every block. Fix every reported line, re-run
until clean.

## The footgun rules (these are what actually break)

| Don't | Why it breaks | Do instead |
|-------|---------------|------------|
| `;` inside a sequence-diagram `note`/message | `;` is a statement separator — text after it is parsed as a new statement | Use `,` or split into two notes |
| `-. label with . or / .->` (inline dotted-edge text) | `.` / `/` in the label collide with the `.->` terminator token | Pipe + quotes: `A -.->\|"label"\| B` |
| `-- label --> ` with `()`, `:`, `/` in label | same class of tokenizer collision | Pipe + quotes: `A -->\|"label"\| B` |
| Raw `<ref>`, `<id>` in labels/notes | `<...>` is treated as HTML and silently dropped or errors | escape as `&lt;ref&gt;`, or just write `ref` |
| Non-ASCII arrows/glyphs: `→ ← ⇒ ▷ ⊳ ◁ ⊲` | rejected by stricter parsers; render inconsistently | ASCII words: `then`, `over`, `->` (in text only) |
| Unquoted node label with `() [] {} : / " #` | breaks the node-shape tokenizer | Quote the whole label: `A["text (x): y/z"]` |
| `end` as a node/participant id | reserved keyword | rename, e.g. `End_`, `Finish` |

Two exceptions that are **safe** and should NOT be "fixed":
- `<br/>` and `<br>` inside labels — the only allowed angle-bracket use.
- A second `:` inside note/message *text* (after the first one) is fine.

## Workflow checklist

1. Pick the diagram type (`flowchart`, `sequenceDiagram`, etc.).
2. Quote every node label that contains punctuation: `Id["..."]`.
3. Keep notes/edge labels ASCII; no `;`, no raw `<>`, no Unicode arrows.
4. For labeled edges, prefer the pipe form `A -->|"label"| B`.
5. Run the linter (above). Resolve all findings.
6. If rendering matters to the user, note that GitHub renders Mermaid natively;
   VS Code needs the "Markdown Preview Mermaid Support" extension.

## More detail

See [REFERENCE.md](REFERENCE.md) for a per-diagram-type cheatsheet and the full
rationale behind each rule.
</content>

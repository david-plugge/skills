---
name: setup-skills
description: Prepare a repo to use these skills — add a domain entry point to CLAUDE.md/AGENTS.md so every session reads the project's glossary and respects its ADRs. Run once per repo.
disable-model-invocation: true
---

# Setup Skills

Add the domain **entry point** to this repo: a short block in `CLAUDE.md`/`AGENTS.md` that loads every session and points the agent at the project's glossary (`CONTEXT.md`) and decisions (`docs/adr/`). Without it, those docs only get read when a skill that mentions them triggers — the entry point makes the ubiquitous language always-on.

Run once per repo. The layout and format of the domain docs are owned by the `/domain-modeling` skill — this command only wires up the pointer; it does not restate those rules.

## Process

1. **Explore.** Check what exists: `CLAUDE.md` and `AGENTS.md` at the root, any existing `## Domain` block in either, and `CONTEXT.md` / `CONTEXT-MAP.md` / `docs/adr/`.
2. **Pick the file.** Edit `CLAUDE.md` if it exists; else `AGENTS.md`. If neither exists, ask the user which to create — never create both, and never add one when the other is already present.
3. **Write the block.** Add a `## Domain` section, or update it in place if one already exists (don't duplicate). Don't touch surrounding sections.

   ```md
   ## Domain

   This project maintains a ubiquitous language in `CONTEXT.md` and records architectural decisions in `docs/adr/` (both created lazily — they may not exist yet). When working here:

   - **Read them if present** before exploring, and **respect the ADRs** — don't re-litigate settled decisions.
   - **Use the glossary's terms** when naming domain concepts (in code, tests, commits, issues, plans). Don't drift to synonyms it lists under _Avoid_.
   - **A missing term is a signal** — either you're inventing language the project doesn't use (reconsider), or there's a real gap. Use `/domain-modeling` to evolve the glossary and record decisions.
   ```

   Don't pre-create `CONTEXT.md` or `docs/adr/` — `/domain-modeling` creates them lazily when there's something to write.
4. **Done.** Tell the user the entry point is in place and that the domain docs will appear as `/domain-modeling` resolves the first terms.

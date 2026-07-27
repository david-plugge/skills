The `skills/` directory is the source of truth. When a skill is added, removed, or renamed, keep `README.md` in sync — the Skills table must have one row per skill (alphabetical), with the name linked to the skills `SKILL.md` file.

This repo is also a Claude Code plugin and its own single-plugin marketplace (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`). Skills are auto-discovered from `skills/`, so neither manifest lists them — never add a `skills` array. After editing a manifest, run `claude plugin validate .`.

## Commands vs skills

Every `SKILL.md` is one of two kinds. The test for "is it a skill" is: _could the model usefully reach for this autonomously?_

- **Command** — _always_ user-invoked. Set `disable-model-invocation: true`. The `description` is human-facing (a one-line summary; no "Use when…" trigger lists). A command may invoke skills, but never another command.
- **Skill** — invocable by model or user. The `description` is model-facing and keeps rich trigger phrasing ("Use when the user wants…, mentions…") so auto-invocation fires. Do not set `disable-model-invocation`.

## Referencing between skills (avoid duplication)

`domain-modeling` and `codebase-design` are **foundation skills**: they define the project's shape and own the shared vocabulary (`CONTEXT.md`/ADRs, and the deep-module terms). Other skills must not restate that vocabulary — they reach it by reference:

- **Dependencies are `/skill`-style prose invocation** ("Run the `/grilling` skill", "run `/codebase-design` for the vocabulary"), not deep `../other-skill/FILE.md` cross-references. Shared reference docs live inside the skill that owns them.
- **Passive vs active domain work.** Merely _reading_ `CONTEXT.md` for vocabulary is a one-line prose pointer any skill can include. Only the active build/sharpen discipline (challenge terms, write ADRs, update `CONTEXT.md` inline) is the `domain-modeling` skill.

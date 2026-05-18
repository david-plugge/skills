The `skills/` directory is the source of truth. When a skill is added, removed, or renamed, keep these files in sync in the same change:

- `.claude-plugin/plugin.json` — the `skills` array must list every directory under `skills/` and nothing else, alphabetically.
- `README.md` — the Skills table must have one row per skill (alphabetical), with the name linked to `skills/<name>/SKILL.md`.

Before finishing any change that touches `skills/`, verify all files agree with the directory listing.

---
name: git-summary
description: Summarize unstaged git changes with per-file +/- line counts.
disable-model-invocation: true
---

# git-summary

Run `git status` and inspect unstaged changes, then respond with only:

1. A short 1-2 sentence summary of the unstaged changes.
2. A list of changed unstaged files with their +/- line counts.
3. A total +/- line count at the bottom.

Rules:

- Keep it concise. No preamble, no trailing commentary.
- Use git commands (e.g. `git diff --numstat`) to compute line counts — do not estimate.
- Do not include staged changes unless those same files also have unstaged modifications.
- Untracked files: list them but mark line counts as `-` (numstat reports `-` for binary/untracked anyway).

## Output format

```
<1-2 sentence summary>

  +12  -3   path/to/file.ts
  +40  -0   path/to/new.ts
  ...

Total: +52 -3
```

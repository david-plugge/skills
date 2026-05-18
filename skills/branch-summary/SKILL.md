---
name: branch-summary
description: Summarize differences between the current branch and a base branch with per-file +/- line counts.
disable-model-invocation: true
---

# branch-summary

Summarize what the current branch contains relative to a base branch.

- Base branch: use the one the user names. If none specified, default to `development`. If `development` does not exist, fall back to `main`, then `master` (in that order). Tell the user which base you used.
- Compare with `git diff --numstat <base>...HEAD` (three-dot — changes introduced on this branch only).
- Also run `git log --oneline <base>..HEAD` to get commit context for the summary.

Respond with only:

1. A short 1-2 sentence summary of what the branch changes (informed by commits + diff).
2. A list of changed files with their +/- line counts.
3. A total +/- line count at the bottom.

Rules:

- Keep it concise. No preamble, no trailing commentary.
- Use git commands to compute line counts — do not estimate.
- State the base branch used on the first line if it wasn't explicitly given.

## Output format

```
<1-2 sentence summary>  (base: development)

  +12  -3   path/to/file.ts
  +40  -0   path/to/new.ts
  ...

Total: +52 -3
```

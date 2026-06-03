---
name: yeet
description: Add, commit, and push current repo changes in one shot.
disable-model-invocation: true
model: haiku
allowed-tools: Bash(git add:*) Bash(git commit:*) Bash(git push:*) Bash(git status:*) Bash(git diff:*) Bash(git remote:*) Bash(git rev-parse:*) Bash(git symbolic-ref:*) Bash(git branch:*) Bash(git ls-remote:*)
---

# yeet

Commit and push the current repository changes.

Run git commands as plain `git <subcommand>` from the working directory — no `-C` flag and no chaining with `&&` or `;` — so they match the pre-approved permission rules above.

Steps:

1. Add all unstaged changes with `git add -A`.
2. Inspect the staged changes and write a concise commit message that accurately summarizes them.
3. Commit the changes with that message. Do not append a `Co-Authored-By` trailer or any other automated footer — the commit message must contain only the summary itself.
4. Push the commit to the current branch's remote.
   - If the current branch does not have an upstream remote branch, create one by pushing with upstream tracking.
   - If this repository has no git remotes configured, do not push.
5. After pushing, output the remote URL for what was pushed if the repository has a remote.
   - Do not assume a specific hosting provider, default branch name, or pull request URL format.
   - Determine the remote's default branch when possible, for example from the remote HEAD; otherwise avoid guessing.
   - If the current branch is the default branch, output the normal remote repository URL.
   - If the current branch is not the default branch and the hosting provider's compare/merge request URL format is recognized, output that URL.
   - If the provider or URL format is not recognized, output the normal remote repository URL and the pushed branch name instead.
   - Convert common SSH git remote forms to HTTPS URLs when printing when possible; otherwise print the configured remote URL.

Keep the commit message concise.

If the user passes arguments to `/yeet`, treat them as additional instructions that refine the commit message or push behavior.

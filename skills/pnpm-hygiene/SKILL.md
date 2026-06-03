---
name: pnpm-hygiene
description: Walk through pnpm dependency maintenance for a v11+ project — dedupe, outdated checks, controlled upgrades, security audits, and override management for transitive CVEs. Use when the user asks to update dependencies, run an audit, deduplicate the lockfile, check for outdated packages, address a CVE, or do periodic dependency maintenance.
disable-model-invocation: true
---

# pnpm Hygiene

Guides interactive dependency maintenance on a pnpm v11+ project. Run commands, surface findings, get user decisions before mutating the lockfile.

## Pre-flight

Confirm pnpm v11+ and detect monorepo:

```bash
pnpm --version                              # must be 11+
test -f pnpm-workspace.yaml && echo workspace
```

If v10 or older, warn the user — flags and config paths differ.

## Workflow

Run steps in order. Stop and report after each; never chain mutating commands.

### 1. Audit lockfile health

```bash
pnpm install --frozen-lockfile --lockfile-only  # is the lockfile in sync? (fails with ERR_PNPM_OUTDATED_LOCKFILE, touches nothing)
pnpm dedupe --check                             # are there duplicates to flatten?
```

If `dedupe --check` reports duplicates, ask before running `pnpm dedupe` (it rewrites the lockfile).

### 2. Security audit

```bash
pnpm audit --prod                           # prod deps only; dev noise filtered
pnpm audit --json --prod | jq '.advisories' # structured findings if many
```

For each advisory, surface: package, severity, vulnerable range, patched range, paths.

**Resolution paths** (pick per advisory):

- Patch available in a direct dep → bump that dep (step 3)
- Patch only in a transitive → add to `overrides` (step 5)
- No patch yet → record in `minimumReleaseAgeExclude` once one ships; `pnpm audit --fix` does this automatically

### 3. Outdated direct dependencies

```bash
pnpm outdated --long                        # workspace root
pnpm -r outdated --long                     # all workspace packages
```

Group findings by risk:

- **Patch/minor** — generally safe, batch together
- **Major** — one at a time, review changelog

Then run interactive update, scoped:

```bash
pnpm update --interactive                   # respects semver ranges
pnpm update --interactive --latest          # allows major bumps
```

Never run `--latest` without `--interactive` — it will silently break things.

### 4. Verify after updates

```bash
pnpm install                                # regenerate lockfile cleanly
pnpm run check                              # or the project's typecheck script
pnpm run lint
pnpm run test                               # if present
```

Stop if any step fails. Report and ask before proceeding.

### 5. Override transitive CVEs

For unpatched vulnerabilities deep in the tree, edit `pnpm-workspace.yaml`:

```yaml
overrides:
    'vulnerable-pkg@<1.2.3': '1.2.3' # range form
    'another-pkg': '^2.0.0' # all versions
```

Then `pnpm install` to apply. Verify with `pnpm why vulnerable-pkg` that the resolved version is the patched one. Note the CVE ID in a comment so the override can be removed later when direct deps catch up.

### 6. Confirm `allowBuilds` is current

After major upgrades, new packages may want to run install scripts. pnpm v11 blocks them by default. Run:

```bash
pnpm install 2>&1 | grep -i "ignored build"
```

Add deliberate entries to `allowBuilds:` in `pnpm-workspace.yaml` — never blanket-allow.

## Reporting back

End the session with:

- What changed (deps bumped, overrides added, dedupe run)
- What was deferred (majors not taken, advisories pending patch)
- Any failing checks that still need attention

Do not commit. Let the user review the diff.

## Notes

- `pnpm audit --fix` writes patched versions into `minimumReleaseAgeExclude` so security fixes bypass the 1-day cooldown
- `pnpm outdated` exits non-zero when outdated deps exist — that's expected, not an error
- In monorepos, prefer `pnpm -r update --interactive` over per-package updates
- `engineStrict` and `preferFrozenLockfile` are pnpm 11 defaults — don't re-add them

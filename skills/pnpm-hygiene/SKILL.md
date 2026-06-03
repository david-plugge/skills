---
name: pnpm-hygiene
description: Walk through pnpm dependency maintenance for a v11+ project — dedupe, outdated checks, controlled upgrades, transitive refreshes, security audits, and the override lifecycle (adding, documenting, retiring).
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

### 4. Refresh transitive dependencies

If earlier steps left uncommitted changes, `git stash` them first — this command rewrites `pnpm-lock.yaml` (and possibly `package.json`), and isolating its diff is what makes it reviewable and independently revertable. Pop the stash after deciding.

```bash
pnpm update --depth Infinity --lockfile-only
```

Re-resolves every transitive dependency to the highest version its range allows — the same outcome as resolving from scratch, without deleting the lockfile or copying anything.

- **Fails** (trust downgrade, release age, unresolvable peer) → a latent resolution problem: the lockfile pins a version a fresh resolve can no longer reproduce. Fix it now (override, exclude, or defer deliberately) rather than letting it ambush the next lockfile-less resolve. Frozen installs (`pnpm ci`, `--frozen-lockfile`) structurally cannot catch this — they never re-resolve.
- **Succeeds** → in-range transitive bugfix/security patches land in the lockfile. Nothing else in this workflow delivers those: `pnpm outdated` and `update --interactive` only see direct deps.

Review the `git diff` of `pnpm-lock.yaml` before keeping it. Caveat: there is no `--no-save`, so it also narrows direct-dep specs in `package.json` when they're looser than the resolved version (e.g. `^24` → `^24.12.4`) — revert that with git if unwanted.

### 5. Verify after updates

```bash
pnpm install                                # regenerate lockfile cleanly
pnpm run check                              # or the project's typecheck script
pnpm run lint
pnpm run test                               # if present
```

Stop if any step fails. Report and ask before proceeding.

### 6. Override transitive CVEs

For unpatched vulnerabilities deep in the tree, edit `pnpm-workspace.yaml`:

```yaml
overrides:
    'vulnerable-pkg@<1.2.3': '1.2.3' # range form
    'another-pkg': '^2.0.0' # all versions
```

Then `pnpm install` to apply. Verify with `pnpm why vulnerable-pkg` that the resolved version is the patched one.

**Every override must carry its retirement test in a comment** — three parts: *why* it exists (CVE ID, bug, policy block), the *retirement condition* (a checkable upstream fact), and the *verification command*:

```yaml
overrides:
    # WHY: 1.7.0 chokes on TS $derived declaration tags.
    # RETIRE WHEN: eslint-plugin-svelte requires >=1.7.1 — VERIFY: pnpm lint
    svelte-eslint-parser: ^1.7.1
```

Undocumented overrides (e.g. inherited from a project scaffold) cost archaeology later: whether they pin a CVE fix, dodge a trust-policy block, or fix a peer-variant bug is indistinguishable from dead weight.

### 7. Retire stale overrides

For each existing override, run this loop:

1. **Check the retirement condition** from the comment — often a single `pnpm view <dependent> dependencies.<pkg>` or a glance at upstream. Not met → keep, move on.
2. **`pnpm why <pkg>` returns nothing** → the package left the graph entirely; delete the override.
3. **Delete the override and re-resolve**: `pnpm update --depth Infinity --lockfile-only` (step 4 — a plain `pnpm install` is lockfile-biased and proves nothing), then judge:
    - resolution error → still needed; restore with `git checkout -- pnpm-workspace.yaml pnpm-lock.yaml` and record the error in the comment
    - `git diff pnpm-lock.yaml` empty → fresh resolution picks the same version unaided; the override is dead weight, remove it
    - diff non-empty → resolution changed; run the override's verification command before deciding. **Resolver success ≠ runtime success** — an override that fixes a peer-variant or behavior bug only reveals itself when the consumer actually runs.

### 8. Confirm `allowBuilds` is current

After major upgrades, new packages may want to run install scripts. pnpm v11 blocks them by default. Run:

```bash
pnpm install 2>&1 | grep -i "ignored build"
```

Add deliberate entries to `allowBuilds:` in `pnpm-workspace.yaml` — never blanket-allow.

## Reporting back

End the session with:

- What changed (deps bumped, transitives refreshed, overrides added or retired, dedupe run)
- What was deferred (majors not taken, advisories pending patch)
- Any failing checks that still need attention

Do not commit. Let the user review the diff.

## Notes

- `pnpm audit --fix` writes patched versions into `minimumReleaseAgeExclude` so security fixes bypass the 1-day cooldown
- `pnpm outdated` exits non-zero when outdated deps exist — that's expected, not an error
- In monorepos, prefer `pnpm -r update --interactive` over per-package updates
- `engineStrict` and `preferFrozenLockfile` are pnpm 11 defaults — don't re-add them
- `pnpm ci`, `pnpm install --force`, `pnpm install --resolution-only`, and `pnpm dedupe --check` are all lockfile-biased — none of them detect latent resolution problems; only step 4 does
- When removing packages, stale optional-peer variants can linger in the lockfile through `pnpm install` and even `pnpm dedupe`; step 4 (or regenerating the lockfile) prunes them

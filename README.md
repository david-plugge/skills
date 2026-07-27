# Agent Skills

A collection of agent skills for software engineering workflows.

## Installation

As a Claude Code plugin:

```
/plugin marketplace add david-plugge/skills
/plugin install david-plugge-skills@david-plugge-skills
```

Or copy the skills into a project:

```sh
pnpx skills@latest add david-plugge/skills
```

## Skills

Two **foundation skills** define the project's shape and own the shared vocabulary; the rest reference them by name so every workflow speaks the same language and respects the same decisions: [domain-modeling](skills/domain-modeling/SKILL.md) owns the domain glossary (`CONTEXT.md`) and ADRs; [codebase-design](skills/codebase-design/SKILL.md) owns the deep-module vocabulary (module, interface, seam, adapter, depth).

| Skill | Description |
| --- | --- |
| [branch-summary](skills/branch-summary/SKILL.md) | Summarize differences between the current branch and a base branch with per-file +/- line counts. |
| [codebase-design](skills/codebase-design/SKILL.md) | **Foundation.** Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface. Referenced by `tdd`, `diagnosing-bugs`, and `improve-codebase-architecture`. |
| [diagnosing-bugs](skills/diagnosing-bugs/SKILL.md) | Disciplined diagnosis loop for hard bugs and performance regressions: reproduce → minimise → hypothesise → instrument → fix → regression-test. |
| [domain-modeling](skills/domain-modeling/SKILL.md) | **Foundation.** Actively build and sharpen a project's domain model — challenge terms, stress-test with scenarios, and update `CONTEXT.md` and ADRs inline. Referenced wherever a skill needs the project's domain language. |
| [git-summary](skills/git-summary/SKILL.md) | Summarize unstaged git changes with per-file +/- line counts. |
| [grill-with-docs](skills/grill-with-docs/SKILL.md) | A grilling session that also builds your project's domain model — runs `/grilling` together with `/domain-modeling`. |
| [grilling](skills/grilling/SKILL.md) | Interview the user relentlessly about a plan or design until every branch of the decision tree is resolved. The reusable loop behind `grill-with-docs`. |
| [handoff](skills/handoff/SKILL.md) | Compact the current conversation into a handoff document for another agent to pick up. |
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| [mermaid-diagrams](skills/mermaid-diagrams/SKILL.md) | Author and edit Mermaid diagrams in Markdown that render cleanly on GitHub, VS Code, and mermaid.js. Use when creating, editing, or debugging Mermaid diagrams or `mermaid` code blocks, or when a Mermaid "Parse error" / "Lexical error" occurs. |
| [pnpm-hygiene](skills/pnpm-hygiene/SKILL.md) | Walk through pnpm dependency maintenance for a v11+ project — dedupe, outdated checks, controlled upgrades, security audits, and override management for transitive CVEs. |
| [setup-skills](skills/setup-skills/SKILL.md) | Wire up a repo to use these skills — add a domain entry point to `CLAUDE.md`/`AGENTS.md` so every session reads the project's glossary and ADRs. Run once per repo. |
| [tdd](skills/tdd/SKILL.md) | Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time. |
| [write-a-skill](skills/write-a-skill/SKILL.md) | Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill. |
| [yeet](skills/yeet/SKILL.md) | Add, commit, and push current repo changes in one shot. |
| [zoom-out](skills/zoom-out/SKILL.md) | Ask the agent to zoom out a level and map the relevant modules and callers using the project's domain glossary vocabulary. |

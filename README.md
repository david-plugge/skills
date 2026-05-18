# Agent Skills

A collection of agent skills for software engineering workflows.

See the [tutorial](TUTORIAL.md) for a walkthrough of how the skills work, how Claude picks them up, and how they chain together on real tasks.

## Installation

```sh
pnpx skills@latest add david-plugge/skills
```

## Skills

| Skill                                                                          | Description                                                                                                              |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| [adr](skills/adr/SKILL.md)                                                     | Draft a Confluence-ready Architecture Decision Record in M3's house style.                                               |
| [diagnose](skills/diagnose/SKILL.md)                                           | Disciplined reproduce → hypothesise → instrument → fix → regression-test loop for hard bugs and performance regressions. |
| [document-project](skills/document-project/SKILL.md)                           | Bootstrap `CONTEXT.md` (and optional ADR seeds) from codebase exploration plus a guided interview — cold-start only.     |
| [gitlab-ci-component](skills/gitlab-ci-component/SKILL.md)                     | Scaffold and configure a GitLab CI/CD catalog component.                                                                 |
| [grill-me](skills/grill-me/SKILL.md)                                           | Interview the user about a plan or design until major assumptions, trade-offs, and open questions surface.               |
| [grill-with-docs](skills/grill-with-docs/SKILL.md)                             | Docs-aware grilling — challenges the plan against `CONTEXT.md` and ADRs, and updates them inline as decisions land.      |
| [handoff](skills/handoff/SKILL.md)                                             | Compact the current conversation into a handoff document for a fresh agent.                                              |
| [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md) | Find deepening opportunities in a codebase, guided by `CONTEXT.md` and `docs/adr/`.                                      |
| [jira](skills/jira/SKILL.md)                                                   | Read Jira tickets via the official `acli` CLI — view, list comments, or search by JQL. Composes with other skills.       |
| [pin-behavior](skills/pin-behavior/SKILL.md)                                   | Pin existing behavior with characterization tests before refactoring or fixing untested code.                            |
| [prototype](skills/prototype/SKILL.md)                                         | Build a throwaway prototype — terminal app for state/logic questions, or radically different UI variations on one route. |
| [review-with-docs](skills/review-with-docs/SKILL.md)                           | Review a diff against `CONTEXT.md`, `docs/adr/`, and security exclusions via parallel subagents — report-only findings.  |
| [setup-skills](skills/setup-skills/SKILL.md)                                   | One-time repo wiring of `AGENTS.md`/`CLAUDE.md` + `docs/agents/domain.md` so the engineering skills find domain docs.    |
| [tdd](skills/tdd/SKILL.md)                                                     | Red-green-refactor loop emphasising behaviour-focused integration tests and vertical slices.                             |
| [write-a-skill](skills/write-a-skill/SKILL.md)                                 | Author new agent skills with proper structure, progressive disclosure, and bundled resources.                            |
| [write-prd](skills/write-prd/SKILL.md)                                         | Synthesize the current conversation into a PRD markdown file using the M3 PRD template.                                  |
| [zoom-out](skills/zoom-out/SKILL.md)                                           | Step back from current detail to re-anchor on the bigger picture.                                                        |

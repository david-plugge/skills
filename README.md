# Agent Skills

A collection of agent skills for software engineering workflows.

## Installation

```sh
pnpx skills@latest add david-plugge/skills
```

## Skills

| Skill                                            | Description                                                                                                                                               |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [branch-summary](skills/branch-summary/SKILL.md) | Summarize differences between the current branch and a base branch with per-file +/- line counts.                                                         |
| [git-summary](skills/git-summary/SKILL.md)       | Summarize unstaged git changes with per-file +/- line counts.                                                                                             |
| [mermaid-diagrams](skills/mermaid-diagrams/SKILL.md) | Author and edit Mermaid diagrams in Markdown that render cleanly on GitHub, VS Code, and mermaid.js. Use when creating, editing, or debugging Mermaid diagrams or `mermaid` code blocks, or when a Mermaid "Parse error" / "Lexical error" occurs. |
| [pnpm-hygiene](skills/pnpm-hygiene/SKILL.md)     | Walk through pnpm dependency maintenance for a v11+ project — dedupe, outdated checks, controlled upgrades, security audits, and override management for transitive CVEs. |
| [write-a-skill](skills/write-a-skill/SKILL.md)   | Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill. |
| [yeet](skills/yeet/SKILL.md)                     | Add, commit, and push current repo changes in one shot.                                                                                                   |
| [zoom-out](skills/zoom-out/SKILL.md)             | Tell the agent to zoom out and give broader context or a higher-level perspective.                                                                        |

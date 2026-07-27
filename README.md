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

| Skill | Description |
| --- | --- |
| [mermaid-diagrams](skills/mermaid-diagrams/SKILL.md) | Author and edit Mermaid diagrams in Markdown that render cleanly on GitHub, VS Code, and mermaid.js. Use when creating, editing, or debugging Mermaid diagrams or `mermaid` code blocks, or when a Mermaid "Parse error" / "Lexical error" occurs. |
| [pnpm-hygiene](skills/pnpm-hygiene/SKILL.md) | Walk through pnpm dependency maintenance for a v11+ project — dedupe, outdated checks, controlled upgrades, security audits, and override management for transitive CVEs. |
| [write-a-skill](skills/write-a-skill/SKILL.md) | Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill. |
| [yeet](skills/yeet/SKILL.md) | Add, commit, and push current repo changes in one shot. |
| [zoom-out](skills/zoom-out/SKILL.md) | Ask the agent to zoom out a level and map the relevant modules and callers using the project's domain glossary vocabulary. |

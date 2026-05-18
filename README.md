# Agent Skills

A collection of agent skills for software engineering workflows.

See the [tutorial](TUTORIAL.md) for a walkthrough of how the skills work, how Claude picks them up, and how they chain together on real tasks.

## Installation

```sh
pnpx skills@latest add david-plugge/skills
```

## Skills

| Skill                                            | Description                                                                                                                                                      |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [branch-summary](skills/branch-summary/SKILL.md) | Summarize differences between the current branch and a base branch with per-file +/- line counts.                                                                |
| [git-summary](skills/git-summary/SKILL.md)       | Summarize unstaged git changes with per-file +/- line counts.                                                                                                    |
| [yeet](skills/yeet/SKILL.md)                     | Add, commit, and push current repo changes in one shot.                                                                                                          |
| [zoom-out](skills/zoom-out/SKILL.md)             | Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need the bigger picture. |

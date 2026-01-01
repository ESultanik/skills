# Contributing to esultanik-skills

Thank you for your interest in contributing to this Claude Code skills marketplace!

## Adding a New Plugin

### 1. Create the Plugin Directory Structure

```
plugins/
└── your-plugin/
    ├── .claude-plugin/
    │   └── plugin.json       # Plugin manifest
    ├── skills/
    │   └── your-skill/
    │       └── SKILL.md      # Skill definition
    └── README.md             # Plugin documentation
```

### 2. Create the Plugin Manifest

Create `plugins/your-plugin/.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin",
  "version": "0.1.0",
  "description": "Description of your plugin",
  "author": "your-username",
  "license": "AGPL-3.0",
  "skills": "./skills/"
}
```

### 3. Create a Skill

Create `plugins/your-plugin/skills/your-skill/SKILL.md`:

```markdown
---
description: Brief description of what the skill does
tags:
  - relevant
  - tags
---

# Your Skill Name

Instructions for Claude on how to execute this skill.
```

### 4. Add Plugin Documentation

Create `plugins/your-plugin/README.md` with:
- Plugin description
- Available skills
- Installation instructions
- Usage examples

### 5. Register in Marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "description": "Description of your plugin",
  "version": "0.1.0",
  "author": "your-username",
  "category": "appropriate-category",
  "tags": ["relevant", "tags"],
  "license": "AGPL-3.0"
}
```

## License Requirements

All contributions must be licensed under AGPL-3.0 to be included in this marketplace.

## Submitting

1. Fork this repository
2. Create your plugin following the structure above
3. Submit a pull request

## Questions?

Open an issue if you have questions about contributing.

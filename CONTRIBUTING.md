# Contribute to esultanik-skills

Package reusable skills for both Claude Code and Codex. Keep one shared workflow;
put genuine runtime differences in referenced instructions.

## Add a plugin

Use this layout:

```text
plugins/your-plugin/
├── .claude-plugin/plugin.json
├── assets/icon.png
├── skills/your-skill/SKILL.md
└── README.md
```

Create `.claude-plugin/plugin.json` with two-space JSON indentation:

```json
{
  "name": "your-plugin",
  "version": "0.1.0",
  "description": "Describe the plugin's implemented capability",
  "author": {
    "name": "Your name"
  },
  "license": "AGPL-3.0",
  "skills": ["./skills/"]
}
```

Include a square PNG icon between 512 and 2048 pixels per side. Add a README with
prerequisites, installation for both runtimes, and invocation examples.

Register the plugin in the root `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin",
  "source": "./plugins/your-plugin",
  "category": "development",
  "tags": ["relevant", "tags"]
}
```

Keep source paths relative to the repository root and retain AGPL-3.0 licensing.
Bump plugin versions for changed packages and the marketplace version for catalog changes.

## Write portable skills

Each skill starts with standard YAML metadata, an H1, and a contents block:

```markdown
---
name: your-skill
description: Describe the task and when the skill applies.
---

# Your skill

## Contents

- [Workflow](#workflow)

## Workflow

Instructions for the agent.
```

Use lowercase, hyphenated directory and skill names. Give every skill a `name`
and `description`; place optional tags inside `metadata`, not custom top-level
frontmatter fields. Put substantial procedures in linked references and include
them in the contents block.

Implement reusable commands as skills. Do not depend on Claude-only command
files, bundled agent definitions, `$ARGUMENTS`, or `${CLAUDE_PLUGIN_ROOT}` for core
behavior. Resolve helpers relative to the installed skill file and quote paths
and user arguments. Describe runtime-specific tools only in the relevant branch
of the instructions; do not assume they exist in the other runtime.

Plan approval does not override an active runtime's Plan mode. A worker must
respect inherited permissions, and each development worker needs an exclusive
worktree. Keep external mutations within the user's authorized scope.

See the [Agent Skills format](https://developers.openai.com/codex/skills) and
[Claude plugin porting guidance](https://developers.openai.com/plugins/guides/submit-claude-plugin#review-what-openai-supports).

## Validate changes

Install the repository hooks and run the offline built-in checks:

```sh
prek install
prek auto-update --cooldown-days 7
prek run --all-files
```

There are no external hook dependencies to update. For new, untracked files, run
`prek run --files PATH...` before staging. Validate the marketplace and each edited plugin:

```sh
claude plugin validate --strict .claude-plugin/marketplace.json
claude plugin validate --strict plugins/github-issues
claude plugin validate --strict plugins/interslavic
```

Exercise changed skills in both runtimes. Verify discovery, referenced files, and
helper execution from an unrelated working directory. For batch issue workflows,
use fixture issue/PR data and temporary Git repositories: test selection, approval
boundaries, ownership changes, existing fixes, dependencies, publication failures,
and cleanup without mutating live GitHub repositories. For dictionary checks, use
controlled CSV data and temporary caches rather than relying on the public download.

## Submit changes

Use focused feature branches and pull requests with factual descriptions and
validation results. Keep commit subjects imperative and at most 72 characters.
Update installation and usage documentation whenever packaging or behavior changes.

# Repository Guidelines

## Project structure and module organization

This repository is the `esultanik-skills` marketplace for Claude Code and Codex.

- `.claude-plugin/marketplace.json` registers available plugins and their source paths.
- `plugins/<plugin-name>/.claude-plugin/plugin.json` defines each plugin's metadata.
- `plugins/github-issues/skills/fix-issues/` contains the batch issue workflow and runtime references.
- `plugins/interslavic/skills/lookup/` contains the standalone dictionary lookup skill.
- `plugins/interslavic/skills/translate/` contains `SKILL.md` and the standard-library
  dictionary tool, `translate.py`.
- Root and plugin `README.md` files document installation and usage; `CONTRIBUTING.md`
  describes adding plugins. Plugin `assets/` directories contain marketplace icons.

## Development and validation commands

There is no build step or dependency installation requirement for the dictionary tool.
From the repository root, use Python 3.13 through `uv`:

```sh
uv run --python 3.13 --no-project plugins/interslavic/skills/translate/translate.py --help
uv run --python 3.13 --no-project plugins/interslavic/skills/translate/translate.py --json water
uv run --python 3.13 --no-project -m json.tool .claude-plugin/marketplace.json
```

These commands inspect options, exercise a lookup, and validate marketplace
JSON syntax. Run `prek run --all-files` and validate edited plugins with
`claude plugin validate --strict plugins/<plugin-name>`. In Claude Code, use
`/plugin marketplace add esultanik/skills` and `/plugin install interslavic@esultanik-skills`
to check installation. In Codex CLI, use `codex plugin marketplace add ESultanik/skills`
and `codex plugin add interslavic@esultanik-skills`.

## Coding style and naming conventions

Use four-space Python indentation, `snake_case` functions and variables, uppercase constants,
type annotations, and Google-style docstrings for non-trivial public functions. Keep lines
within 100 characters. Prefer standard-library solutions; justify new dependencies.
Use two-space JSON indentation and lowercase, hyphenated plugin and skill directory names.
Keep skill metadata in YAML front matter, followed by an H1 and a `## Contents` section.
The prek configuration uses offline built-in syntax and hygiene checks. No Python
formatter, linter, or type-checker configuration is currently checked in.

## Testing guidelines

No automated test framework or coverage threshold is defined. For lookup changes, check
plain-text and JSON output, language filtering, diacritic normalization, duplicate matches,
empty results, and download failures. Use controlled CSV data and temporary cache paths for
repeatable tests. If adding tests, place `test_*.py` files under `tests/` and document their
run command. For skill edits, exercise the affected workflow in both runtimes. Use fixtures
and temporary Git repositories for batch workflow checks without live GitHub mutations.

## Commit and pull request guidelines

History uses focused subjects about translation, commands, and marketplace metadata.
Use imperative subjects such as `Fix plugin source path`, limited to 72 characters.
Keep each commit focused. Submit feature branches through pull requests with a description,
validation commands and results, and linked issues when applicable. Update plugin documentation
and marketplace registration when adding a plugin. Contributions must retain AGPL-3.0 licensing.

## Cache and configuration

The first lookup downloads a public Google Sheets dictionary into `~/.cache/interslavic/`.
Subsequent lookups use SQLite; `--refresh` replaces the cache and `--info` inspects metadata.
Keep generated caches and credentials out of commits.

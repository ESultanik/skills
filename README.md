# esultanik-skills

[Evan Sultanik](https://www.sultanik.com/)'s skills marketplace for Claude Code and Codex.

## Install

In Claude Code:

```text
/plugin marketplace add esultanik/skills
/plugin install github-issues@esultanik-skills
/plugin install interslavic@esultanik-skills
```

In Codex CLI:

```sh
codex plugin marketplace add ESultanik/skills
codex plugin add github-issues@esultanik-skills
codex plugin add interslavic@esultanik-skills
```

Start a new session after installation if the skills do not appear. You can also
select installed skills through Codex's `/skills` menu. Both runtimes use the same
skill files and the repository's Claude-compatible marketplace catalog.

See [Codex marketplace support](https://developers.openai.com/codex/plugins/build)
and [Claude Code plugins](https://code.claude.com/docs/en/plugins).

## Available plugins

| Plugin | Description | Skills |
| --- | --- | --- |
| [github-issues](plugins/github-issues/) | Plan and fix batches of GitHub issues | `fix-issues` |
| [interslavic](plugins/interslavic/) | Interslavic translation and vocabulary | `translate`, `lookup` |

## Use the skills

| Task | Claude Code | Codex |
| --- | --- | --- |
| Fix issues | `/github-issues:fix-issues` | `$github-issues:fix-issues` |
| Translate | `/interslavic:translate Hello` | `$interslavic:translate Hello` |
| Look up words | `/interslavic:lookup water` | `$interslavic:lookup water` |

The issue skill asks you to select all bugs, all issues, a maximum by priority, or
explicit issue numbers. It researches and plans before asking you to approve
changes. Development uses subagents in separate worktrees; PRs remain for
maintainers to merge. Read the [GitHub issue workflow](plugins/github-issues/README.md)
for prerequisites, ownership confirmation, closure rules, and native stacks.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for packaging, validation, and portability rules.

## License

This marketplace and all plugins use the
[GNU Affero General Public License v3.0](LICENSE).

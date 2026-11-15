# GitHub issue batches

Plan and fix batches of GitHub issues in Claude Code or Codex, using subagents in
exclusive Git worktrees. Independent fixes can run concurrently; dependent fixes
become native GitHub stacked PRs. Maintainers merge the resulting PRs.

## Prerequisites

- A local Git checkout and authenticated GitHub access, with permission to assign
  issues, comment, close issues, create issues, and publish PRs.
- A runtime with subagents and isolated worktree support, plus the repository's
  normal development tools.
- The official `github/gh-stack` extension and direct feature-branch push access
  for dependent PRs. Native stacks require all branches in the same repository.

The skill reports missing prerequisites without weakening permissions or silently
substituting ordinary PR chains. It does not automatically install extensions or
change repository settings. See [GitHub's stacking documentation](https://github.com/github/gh-stack).

## Install and invoke

Claude Code:

```text
/plugin marketplace add esultanik/skills
/plugin install github-issues@esultanik-skills
/github-issues:fix-issues
```

Codex CLI:

```sh
codex plugin marketplace add ESultanik/skills
codex plugin add github-issues@esultanik-skills
```

Then invoke `$github-issues:fix-issues` or select it from `/skills`. You can include
the selection, such as `$github-issues:fix-issues Address issues #12, #18, and #25`.

## Selection and planning

The skill asks you to choose:

- **All bugs:** classify issues using behavior, discussion, and code rather than labels.
- **All issues:** consider the complete open backlog.
- **A maximum:** select up to that many open issues by assessed priority.
- **Issue numbers:** address the explicit list you provide.

It checks for existing merged or open PRs before proposing work. The plan includes
evidence, acceptance checks, ownership, dependencies, and proposed direct closures.
You approve the concrete plan before changes begin. Issues assigned to another
user require explicit confirmation, including issues where you are a co-assignee;
existing assignees are preserved when you are added.

Claude Code enters native Plan mode when available. In Codex, you can invoke the
skill from `/plan`; implementation waits for the client to exit Plan mode. When
agent-callable mode controls are unavailable, the skill uses read-only planning
and explicit approval without claiming to switch the native mode.

## Results and closure

Workers implement and check approved fixes in their own worktrees. The coordinator
reviews their output, opens PRs with closing references, and creates native stacks
where fixes depend on one another. It leaves merging to maintainers and does not
enable auto-merge. For stacked PR squash merges, retain closing references in the
resulting commit messages or verify issue closure after landing.

Verified fixes already on the default branch can be closed with a resolving
PR/commit comment. WONTFIX proposals are closed as "not planned" only when approved
in the plan; later proposals require new approval. Existing open PRs leave issues
open until merge, with comments added where useful.

New bugs and concrete improvements are shown to you, deduplicated, filed, and
assigned to you without expanding the batch. Regressions of previously completed
issues get a linked report with current evidence. Confidential security findings
follow the repository's private reporting process.

Run-created worktrees are removed after work is preserved. Branches backing open
PRs or unpublished work remain. Any unpreserved files, cleanup exceptions, or
blocked issues are reported alongside PR links, direct closures, and new findings.

## License

AGPL-3.0

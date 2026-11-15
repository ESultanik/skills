---
name: fix-issues
description: >-
  Plan and implement batches of GitHub issues, including all bugs, all open issues,
  a priority-limited batch, or explicit issue numbers. Use for batch issue fixing
  through reviewed plans, worktree-isolated subagents, and pull requests for
  maintainers to merge, rather than read-only triage or PR review.
---

# Fix GitHub issues in batches

## Contents

- [Workflow](#workflow)
- [Authorization and outcomes](#authorization-and-outcomes)
- [References](#references)
- [references/workflow.md](references/workflow.md)
- [references/runtimes.md](references/runtimes.md)
- [references/worker.md](references/worker.md)

## Workflow

1. Ask which issues to address: **All bugs**, **All issues**, **Highest priority up
   to a maximum**, or **Issue numbers**. Confirm a selection already provided in
   the invocation instead of asking the user to repeat it.
2. Read [references/workflow.md](references/workflow.md) and the applicable runtime
   section in [references/runtimes.md](references/runtimes.md).
3. Research the selected issues and existing fixes, then obtain approval of the
   complete batch plan before assignments, source edits, or GitHub writes.
4. Delegate development using [references/worker.md](references/worker.md). Each
   development worker must have an exclusive worktree and branch. Coordinate PRs,
   native stacks, issue updates, new findings, and cleanup in the parent session.

## Authorization and outcomes

Use native Plan mode when the host exposes it. Respect an active Plan mode until
the host exits it; approval text alone does not change a runtime restriction.

Ask explicitly before proceeding on an issue with another assignee. Add the local
user without removing existing assignees. Close only approved WONTFIX decisions or
verified fixes already on the default branch. An open PR leaves its issue open.

Open PRs with closing references and leave merging to maintainers. File new,
evidence-backed findings and report their links without expanding the batch.
Remove run-created worktrees after preserving the work; disclose cleanup failures.

## References

The shared workflow defines selection, evidence, approval, publication, and cleanup.
The runtime reference defines planning and delegation for Claude Code and Codex.
The worker reference is the common delegation contract, not a separately installed
agent or a dependency on another skill.

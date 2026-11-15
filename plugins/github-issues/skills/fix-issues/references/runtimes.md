# Runtime orchestration

## Contents

- [Claude Code](#claude-code)
- [Codex](#codex)
- [Shared worktree rules](#shared-worktree-rules)

## Claude Code

Run the skill in the main conversation. Do not configure the whole skill with
`context: fork` or `agent: Plan`: it must ask questions and coordinate implementation
after planning, not remain confined to a read-only planning subagent.

After selection, call `EnterPlanMode` when exposed and not already active. Use
read-only research agents as useful, present the batch plan through `ExitPlanMode`,
and await approval plus the actual mode transition. When these tools are absent,
perform the same read-only research and explicit plan-approval exchange without
claiming to have enabled native Plan mode.

Delegate development through the Agent tool with worktree isolation when supported.
Use a general-purpose development worker with the shared worker contract. Otherwise,
create each worker's worktree explicitly and use a delegation facility that pins
the worker to that path. If neither mechanism is available, stop development.

Native isolation may initially branch from the default branch rather than the
requested dependency. Before edits, have the worker verify its worktree and create
its own named branch from the coordinator's exact base SHA inside that worktree.
Do not change shared worktree settings to alter the default. Retain changed
worktrees until the coordinator verifies preservation and removes them.

See [Claude Code tools](https://code.claude.com/docs/en/tools-reference)
and [worktree isolation](https://code.claude.com/docs/en/worktrees).

## Codex

Use the host's actual question and collaboration tools; do not invent Claude tool
names. Read active mode instructions. A skill cannot change a developer-enforced
collaboration mode. While native Plan mode is active, research and present the
plan, then wait for the client to switch to an execution-capable mode. A user saying
"approved" does not itself override that restriction. In Codex CLI, the user can
start native planning with `/plan` before invoking the skill.

If the session is execution-capable and no agent-callable mode switch is exposed,
use a read-only planning phase and explicit approval before execution. Do not alter
configuration, start an unrestricted nested session, or delegate writes to bypass
the active mode or sandbox.

After approval and the permitted mode transition, use available native subagents.
Create exclusive worktrees with the host worktree tools, `wt`, or `git worktree
add -b BRANCH PATH BASE_SHA`. Use a persistent location outside the caller's source
tree, or a verified ignored worktree directory. Resolve paths from the repository
or environment, not user-specific constants or temporary directories.

Supply an explicit working directory when the delegation API supports it.
Otherwise, put the absolute worktree path in the worker's task and require every
shell call to use it, every edit to stay under it, and an initial isolation report
before changes. If the host cannot honor that isolation, stop development.
The coordinator records worktree paths and performs cleanup after workers finish.

See [Codex commands](https://learn.chatgpt.com/docs/developer-commands#built-in-slash-commands).

## Shared worktree rules

Verify each worker's `git rev-parse --show-toplevel`, branch, and `HEAD` against the
assigned path, branch, and base. Never edit the caller's checkout to implement a
fix. Each worker owns one worktree at a time; release it before another worker
uses it. Read-only research may use the caller's checkout.

Git refs, configuration, hooks, stash, and some caches are shared across worktrees.
Workers must not stash, change shared Git configuration, install hooks, delete
locks, move another worktree's branch, or run repository maintenance. The
coordinator prepares required hooks before parallel work when authorized.
Pass `-c rerere.enabled=false -c rebase.autoStash=false` for run-owned merges or
rebases. Never force checkout or update branches owned by other sessions.

Use inherited model, permissions, and sandbox settings. Missing authentication,
network access, or worker capacity is a prerequisite to report, not permission to
weaken controls. Supply workers with trusted check requirements explicitly;
do not assume a subagent inherits the full parent conversation or project context.

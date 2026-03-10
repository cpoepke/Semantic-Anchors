# Agent Support

## Recommended Strategy

Use `AGENTS.md` as the portable baseline when the user wants semantic anchors to work across multiple coding agents. Then add native mirror files only for agents whose startup context is centered on their own filename or settings.

Project-local onboarding is the strongest cross-agent answer. Home-directory onboarding is useful for personal defaults, but it is not universally portable across all coding agents.

When installing into a live repository, follow the ToonDex pattern: inject a marked `Semantic Anchors` block into the first suitable existing markdown file, and create a minimal `AGENTS.md` only when no suitable file exists.

## Support Matrix

| Agent | Project-level startup context | User or home-level startup context | Hooks or dynamic injection | Guidance |
| --- | --- | --- | --- | --- |
| Codex | `AGENTS.md` in the repo; project-root and subdirectory files can be aggregated hierarchically | `$CODEX_HOME/AGENTS.md` (commonly `~/.codex/AGENTS.md`) | None documented in the product docs used here | Use `AGENTS.md` as the primary file. This is the best baseline for portable semantic-anchor onboarding. |
| Claude Code | `CLAUDE.md` in the project root | `~/.claude/CLAUDE.md` | Hooks in settings, especially `SessionStart` and `UserPromptSubmit` | Use `CLAUDE.md` for static anchors. Use hooks only when the injected anchor set must depend on runtime context. |
| Gemini CLI | `GEMINI.md` by default; optionally configure Gemini to also load `AGENTS.md` via `context.fileName` | `~/.gemini/GEMINI.md` | Hooks such as `BeforeAgent` and `SessionStart` | If standardizing across agents, prefer `AGENTS.md` plus Gemini settings; otherwise mirror into `GEMINI.md`. |
| Cursor | `AGENTS.md`, `CLAUDE.md`, or `.cursor/rules/*.mdc` | User Rules in Cursor settings | None needed for this use case | Use `AGENTS.md` unless path-scoped behavior is required, in which case use `.cursor/rules`. |
| GitHub Copilot | `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` for agent instructions; `.github/copilot-instructions.md` for repository-wide guidance | IDE-specific global instructions, not one portable path | Custom agents exist, but are not required for default anchor onboarding | Use both `AGENTS.md` and `.github/copilot-instructions.md` when you want broad coverage across coding agent, chat, and review workflows. |

## Scope Rules

- Choose project scope when the user wants team-wide behavior or maximum portability.
- Choose home scope when the user wants personal defaults across many repositories.
- If the user wants both, split responsibilities: personal style in home memory, team or repo conventions in project files.

## Portable Defaults

For the widest practical coverage, create these files in this order:

1. `AGENTS.md`
2. `CLAUDE.md` only if Claude Code is a target
3. `GEMINI.md` or Gemini `context.fileName` settings only if Gemini CLI is a target
4. `.github/copilot-instructions.md` only if Copilot chat or review behavior also needs the same defaults

The bundled installer automates only the shared-file step plus optional Claude hook installation. Use that as the default path before adding mirrors.

## When to Use Hooks

Use hooks only when static files are insufficient.

Examples:

- The active anchor set depends on the branch, directory, or file type.
- The team wants to inject recent ADRs, issue metadata, or generated summaries at session start.
- The team wants enforcement, blocking, or validation, not just startup guidance.

For static, always-on semantic anchors, plain instruction files are simpler, safer, and easier to debug.

## Practical Conclusions

- `AGENTS.md` is the right canonical project artifact.
- `CLAUDE.md` and `GEMINI.md` are compatibility mirrors, not the first file to author.
- Home-directory onboarding cannot be guaranteed for every coding agent, so avoid claiming a single universal global install path.
- If the user says "all coding agents," interpret that as "all agents that can reliably consume repository instructions," and prefer project-local files.

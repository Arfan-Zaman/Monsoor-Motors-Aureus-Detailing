# Status

Claude updates this file after every step and pushes it to GitHub. Newest entry at the top.

---

## 20 Nov 2026: rule merged into main

**What I did**
- Merged the latest `main` from GitHub into this branch (no conflicts), then pushed it to `main`. Every session now gets the push + status rule.

**Files changed**
- `.claude/STATUS.md` (this entry). `CLAUDE.md` and `Tools/autosave.sh` are now on `main`.

**What's next**
- Nothing pending for this task. The next session that works here adds its own entry above this one.

---

## 20 Nov 2026: push + status rule set up

**What I did**
- Added the rule "after every step, push to GitHub and update this file" to `CLAUDE.md`, so every future session follows it.
- Fixed auto-save: on new worktree branches it ran a plain `git push`, which failed without telling anyone because the branch had no upstream. It now runs `git push -u origin HEAD` the first time.
- Created this status file.

**Files changed**
- `CLAUDE.md` (Git rules section)
- `Tools/autosave.sh` (push step)
- `.claude/STATUS.md` (new)

**What's next**
- Merge this branch (`claude/github-push-status-workflow-15710a`) into `main` so all sessions pick up the rule. Local `main` is also 8 commits behind `origin/main`.

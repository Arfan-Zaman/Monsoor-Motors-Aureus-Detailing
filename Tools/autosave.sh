#!/bin/zsh
# Auto-save: commit and push any changes in the Monsoor Motors repo.
# Run by the Claude Code Stop hook after every turn (.claude/settings.json).
# Safe by design: .gitignore keeps HR/, videos and big files out, and this
# script double-checks before committing. Never force-pushes.
cd "${CLAUDE_PROJECT_DIR:-/Users/mdarfanuzzaman/Documents/Monsoor Motors}" || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# Nothing changed? Do nothing.
[[ -z "$(git status --porcelain)" ]] && exit 0

# Keep any new file over 95 MB local only (GitHub limit is 100 MB).
git ls-files --others --modified --exclude-standard -z | while IFS= read -r -d '' f; do
  [[ -f "$f" ]] || continue
  if (( $(stat -f%z "$f") > 95*1024*1024 )); then
    grep -qxF "/$f" .git/info/exclude 2>/dev/null || print -r -- "/$f" >> .git/info/exclude
  fi
done

git add -A

# Final guard: never commit HR, videos, audio or secrets, even if forced.
blocked=$(git diff --cached --name-only | grep -iE '^HR/|\.(mp4|mov|m4v|avi|webm|mkv|wav)$|(^|/)\.env|\.(pem|key)$')
if [[ -n "$blocked" ]]; then
  print -r -- "$blocked" | while IFS= read -r f; do git rm -q --cached -- "$f"; done
fi
git diff --cached --quiet && exit 0

n=$(git diff --cached --name-only | wc -l | tr -d ' ')
first=$(git diff --cached --name-only | head -3 | sed 's#.*/##' | paste -sd ', ' -)
git commit -q -m "Auto-save: $n file(s) – $first" -m "Saved automatically after a Claude Code step on $(date '+%Y-%m-%d %H:%M')." || exit 0

# Push in the background so Claude isn't slowed down; log any failure.
# New worktree branches have no upstream yet, so set one on first push.
if git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
  ( git push -q >/dev/null 2>"$HOME/.claude/monsoor-autosave-push.log" || true ) &!
else
  ( git push -q -u origin HEAD >/dev/null 2>"$HOME/.claude/monsoor-autosave-push.log" || true ) &!
fi
exit 0

---
name: save-progress
description: Save the current Monsoor Motors work to GitHub. Use when the user says "save", "save progress", "commit", "push", "back it up", or at the end of a finished piece of work. Updates the playbook daily log, commits with a clear message and pushes to the private repo.
---

# Save progress

Run from the project root (`/Users/mdarfanuzzaman/Documents/Monsoor Motors`).

1. **Check what changed:** `git status --short`. If nothing changed, say so and stop.
2. **Safety check before staging.** None of these may be staged:
   - anything under `HR/`
   - videos or audio (`.mp4 .mov .m4v .avi .webm .mkv .wav`)
   - any file over 100 MB
   - secrets (`.env`, keys, tokens, passwords)
   
   They should already be in `.gitignore`. If something new would slip through, add it to `.gitignore` first.
3. **Update the playbook** (`Monsoor Motors - Playbook & Daily Log.md`). Add or extend today's entry at the bottom of the Daily Log using the template there: what was made or changed, files, decisions or feedback, and what's next. Also update the Finished files and Reusable tools sections if they changed.
4. **Stage and commit:**
   - `git add -A`
   - then `git diff --cached --stat` to review
   - then commit with a short summary line plus 1–3 lines saying what and why, ending with the attribution line from the system reminder, if there is one
5. **Push:** `git push`. If it fails, report the error; never force-push.
6. **Report** in one or two lines: the commit message and that it's on GitHub.

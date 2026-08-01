---
title: "1.8 Checkpoint: prove the toolkit works"
sidebar_position: 8
---

# 1.8 Checkpoint: prove the toolkit works

Like every checkpoint from here on, this one is commands plus a
checklist, and you run it from your vault folder. Everything here works
in both PowerShell and bash.

```bash
cd ~/git/lab-journal    # adjust to your vault path

# At least three commits, with messages you wrote.
git log --oneline

# A remote named "origin" pointing at your PRIVATE GitHub repo.
git remote -v

# Nothing uncommitted left behind.
git status

# The ignore rules are active: this should print the workspace
# file, proving Git knows to skip it.
git check-ignore .obsidian/workspace.json
```

And in Obsidian:

- create today's daily note and confirm it lands in `Journal/`
  pre-filled with the four headings

## Pass criteria

- [ ] `git log` shows at least three commits with meaningful messages
- [ ] `git remote -v` shows an `origin` on GitHub, and the repo is
      **private** (check the badge next to its name in the browser)
- [ ] `git status` reports a clean working tree after your last push
- [ ] `git check-ignore` prints the workspace.json path
- [ ] The daily-note template works, and your Module 0 entry lives in
      `Journal/`
- [ ] `Projects/lab-progress.md` has Modules 0 and 1 ticked, with your
      setup facts filled in
- [ ] You have a Claude account, and one command explanation from
      lesson 1.6 saved in your journal
- [ ] macOS/Linux only: you detached from a tmux session and
      reattached to find it still running

All green means you now work like an engineer: notes that accumulate,
history you can rewind, a backup that leaves the building, and an AI
you command instead of obey. Module 2 puts this toolkit to work on
scripting.

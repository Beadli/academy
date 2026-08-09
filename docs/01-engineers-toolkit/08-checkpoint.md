---
title: "1.8 Checkpoint: prove the toolkit works"
sidebar_position: 8
---

# 1.8 Checkpoint: prove the toolkit works

Like every checkpoint from here on, this one is commands plus a
checklist, and you run it from your vault folder. It's a `bash` block, so
Git Bash on Windows, per lesson 1.3.

```bash
cd ~/git/lab-journal    # the vault folder from lesson 1.2

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

- [ ] `git log` shows at least three commits with meaningful messages:
      lesson 1.3's first one, at least one daily round trip from 1.4,
      and 1.7's module close
- [ ] `git remote -v` shows an `origin` on GitHub, and the repo is
      **private** (check the badge next to its name in the browser), as
      lesson 1.4 created it
- [ ] `git status` reports a clean working tree after your last push
      (the rhythm from lesson 1.3)
- [ ] `git check-ignore` prints the workspace.json path, proving the
      ignore rules from lesson 1.3 are active
- [ ] The daily-note template from lesson 1.2 works, and your Module 0
      entry lives in `Journal/`
- [ ] `Projects/lab-progress.md` has Modules 0 and 1 ticked, with your
      setup facts filled in (lessons 1.2 and 1.7)
- [ ] You have a Claude account, and one command explanation from
      lesson 1.6 saved in your journal
- [ ] macOS/Linux only: you detached from the tmux session lesson 1.5
      started and reattached to find it still running

All green means you now work like an engineer: notes that accumulate,
history you can rewind, a backup that leaves the building, and an AI
you command instead of obey. Module 2 puts this toolkit to work on
scripting.

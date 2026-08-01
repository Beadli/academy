---
title: "1.3 Git, the five commands that matter"
sidebar_position: 3
---

# 1.3 Git, the five commands that matter

Git has a reputation for being hard, earned by people teaching all of it
at once. Daily Git is five commands, and you're going to learn them on
your own vault, where the stakes are your notes instead of somebody's
production code.

First, the mental model, because Git makes no sense without it. Git
doesn't track "versions of a file." It takes snapshots of an entire
folder, whenever you ask, and remembers every snapshot forever. Each
snapshot is called a commit. That's the whole idea. Everything else is
bookkeeping around it.

Why you want this for a journal: fearlessness. Once your vault is under
Git, you can reorganize, rewrite, and delete with total confidence,
because any earlier state is one command away. I've restored
accidentally gutted notes more than once, and the calm that comes from
knowing you can is worth the lesson on its own.

## Install Git

```powershell
# Windows (PowerShell). winget ships with Windows 10/11.
winget install --id Git.Git -e
```

```bash
# Debian/Ubuntu
sudo apt install git

# macOS: running "git" in Terminal offers to install the
# command line tools; accept and you're done.
```

Close and reopen your terminal afterward, then introduce yourself. Git
stamps this onto every commit:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Put the vault under Git

```bash
# Move into your vault folder first. Adjust the path to yours.
cd ~/git/lab-journal

# Turn this folder into a Git repository. This creates a hidden
# .git directory where every snapshot will live. Your files are
# not touched.
git init

# What does Git see? Everything, currently "untracked."
git status
```

Notice `.obsidian/workspace.json` in that list. That file is Obsidian
remembering which tabs you had open, and it changes every time you
breathe. The starter vault ships a `.gitignore` that tells Git to
disregard it; open `.gitignore` and read it, because knowing *why* a
file is ignored is the difference between using a config and cargo
culting one.

## The daily rhythm

```bash
# Stage everything that changed. "Staging" is choosing what goes
# in the next snapshot; -A means "all of it."
git add -A

# Take the snapshot, with a message future-you will read.
git commit -m "journal: first day under version control"

# Look at your history. One line per commit, newest first.
git log --oneline
```

Make a change to any note, save it, and run the three again. Then once
more. The rhythm you're building (`status`, `add`, `commit`) is the
same one you'll use on Ansible playbooks in Module 9 and detection
rules in Module 11. There's a cheatsheet already in your vault at
`Resources/cheatsheets/git-basics.md`, which also covers `git diff` and
`git restore`, the two commands for when something went sideways.

Commit at the end of every lab session from now on. It takes ten
seconds, and it's the habit the rest of the course quietly depends on.

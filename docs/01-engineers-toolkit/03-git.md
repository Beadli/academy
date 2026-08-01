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

## The ignore rules

Before the first commit, a problem worth meeting on purpose. Obsidian
keeps a file called `.obsidian/workspace.json` that remembers which tabs
you had open, and it changes every time you breathe. Snapshot it and
every future commit fills up with noise about nothing.

Git's answer is a file named `.gitignore`: a plain-text list of paths
Git pretends not to see. There's nothing to activate or turn on. If the
file exists in the repository, Git reads it, every time, automatically.
The starter vault shipped one; confirm it survived the unzip, since
files starting with a dot like to play hidden:

```bash
# -a lists dotfiles too. You should see .gitignore here.
ls -a

# Print it. Every line is a path Git will skip, and the comments
# explain why each one deserves to be skipped.
cat .gitignore
```

You should be looking at this:

```text
# Per-machine Obsidian state: window layout, open tabs, cache. Syncing
# these between machines causes pointless conflicts, so Git ignores them.
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
```

Note what's *not* ignored: the rest of `.obsidian/`, including the
daily-notes and template settings. Those you want travelling with the
vault to any future machine. The line between the two is the principle:
share configuration, ignore per-machine state. You'll redraw that line
in every tool you ever put under version control.

Now watch the rules work:

```bash
# -uall makes status name every untracked file individually instead
# of collapsing folders. The .obsidian settings files appear;
# workspace.json does not, because the rules are already active.
git status -uall

# And the direct question: "would Git ignore this path?" If it
# prints the path back, the answer is yes. Silence means no.
git check-ignore .obsidian/workspace.json
```

Knowing *why* a file is ignored is the difference between using a
config and cargo-culting one, which is why the checkpoint at the end of
this module asks Git this exact question again.

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
same one you'll use on Ansible playbooks in Module 10 and detection
rules in Module 12. There's a cheatsheet already in your vault at
`Resources/cheatsheets/git-basics.md`, which also covers `git diff` and
`git restore`, the two commands for when something went sideways.

Commit at the end of every lab session from now on. It takes ten
seconds, and it's the habit the rest of the course quietly depends on.

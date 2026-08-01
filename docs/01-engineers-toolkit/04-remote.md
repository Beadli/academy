---
title: "1.4 A remote: your journal, off your laptop"
sidebar_position: 4
---

# 1.4 A remote: your journal, off your laptop

Right now every snapshot of your vault lives in one place: the laptop
that could be stolen, dropped, or die of an SSD failure the week before
an interview where you wanted to show off this exact journal. A remote
fixes that. It's a copy of your repository on someone else's server that
you push commits to and pull commits from.

We'll use GitHub, because it's free for private repositories and because
a GitHub account is de facto professional infrastructure in this
industry anyway. (GitLab and others work identically; the course
standardizes on GitHub so the screenshots match.) Later, in Module 6,
you'll build your *own* Git server inside the lab and point the vault at
it instead. Cloud first, self-hosted once you can host.

## Account and tooling

Create an account at [github.com](https://github.com) if you don't have
one. Enable two-factor authentication while you're there; a security
course that skips 2FA on day one would be embarrassing.

Then install GitHub's command line tool, which makes authentication
painless:

```powershell
# Windows
winget install --id GitHub.cli -e
```

```bash
# Debian/Ubuntu
sudo apt install gh

# macOS (with Homebrew)
brew install gh
```

Reopen your terminal and log in:

```bash
# Starts a browser-based login. Pick "GitHub.com", then "HTTPS",
# then "Login with a web browser" and follow the code it shows.
gh auth login
```

## Create the remote and push

```bash
cd ~/git/lab-journal

# Create a PRIVATE repository on GitHub named lab-journal, wire
# it up as this folder's remote, and push everything in one go.
gh repo create lab-journal --private --source=. --push
```

Private matters here. Your journal will eventually contain the guts of
your lab, and "what broke" sections are exactly what you don't publish.

Check your work:

```bash
# Which remote is this folder connected to?
git remote -v

# Open the repository in your browser and see your notes online.
gh repo view --web
```

From now on the daily rhythm from lesson 1.3 gains one beat: `status`,
`add`, `commit`, **`push`**. Commit is the snapshot; push is the
snapshot leaving the building.

## The habit that proves it works

Edit a note, commit, push. Then open the repo in your browser and find
your change. Do that round trip once a day for the rest of this module
until it's boring. Boring is the goal; backup systems you have to think
about are backup systems you'll eventually skip.

---
title: "1.4 Push your journal to GitHub"
sidebar_position: 4
---

# 1.4 Push your journal to GitHub

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
# An interactive login. It asks four questions before it does
# anything, and the four are answered below.
gh auth login
```

**Answer them like this.** The exact wording drifts between versions of `gh`,
so match the meaning rather than the letters. Move with the arrow keys and
press Enter to choose.

1. **Where do you use GitHub?** Choose **GitHub.com**. The other option is a
   GitHub Enterprise Server, which is a company's own private installation.
   It is not what you just made an account on.
2. **What is your preferred protocol for Git operations?** Choose **HTTPS**.
   SSH sits directly beneath it and is a perfectly respectable answer in
   general, just not yet: it needs a key pair you have not created and have
   no way to reason about. You will set up SSH keys properly in Module 6,
   on your own server, where what they are for is visible. HTTPS also
   travels better, because it uses port 443 like ordinary web traffic, and
   plenty of office and campus networks block SSH's port 22 outright.
3. **Authenticate Git with your GitHub credentials?** Choose **Yes**. This is
   the one that quietly matters. It hands the login to `git` itself, so that
   `git push` later just works. Answer no and every push in this course stops
   to demand a username and a password that will not be accepted, because
   GitHub stopped taking account passwords for Git operations years ago.
4. **How would you like to authenticate GitHub CLI?** Choose **Login with a
   web browser**. The alternative expects you to have already created a
   personal access token by hand, with the correct permissions chosen from a
   long list.

Then `gh` shows you a one-time code, roughly `A1B2-C3D4`, and waits for you to
press Enter before opening your browser. **Copy that code before you press
Enter**, because the page asks for it straight away and the terminal is behind
the browser window by then. Paste it, approve the authorization, and the
terminal finishes by itself.

**How you know it worked:**

```bash
# Reports which host you are logged in to, as whom, and what the
# token is allowed to do.
gh auth status
```

It should name `github.com` and your account. If instead it says
`You are not logged into any GitHub hosts`, the login did not complete and
running `gh auth login` again is safe.

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

`repo` in those commands is just the usual short form of repository. Both
words mean the same thing and you will meet both everywhere.

From now on the daily rhythm from lesson 1.3 gains one beat: `status`,
`add`, `commit`, **`push`**. Commit is the snapshot; push is the
snapshot leaving the building.

## The habit that proves it works

Edit a note, commit, push. Then open the repo in your browser and find
your change. Do that round trip once a day for the rest of this module
until it's boring. Boring is the goal; backup systems you have to think
about are backup systems you'll eventually skip.

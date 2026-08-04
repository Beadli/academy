---
title: "6.8 Move your journal home"
sidebar_position: 8
---

# 6.8 Move your journal home

Lesson 1.4 said: cloud first, self-hosted once you can host. You can
host. Time to collect.

## Make a home for it

In Gitea, at `http://git.lab.internal`, signed in as the account
you created:

1. Click the **+** in the top right and choose **New Repository**.
2. Name it `lab-vault`.
3. Set visibility to **Private**. Your journal has your lab's addresses
   and your "what broke" notes in it, and that's not public reading even
   on a private network.
4. **Do not** tick anything that initialises the repository. No README,
   no `.gitignore`, no licence. Your vault already has all of that, and
   an initialised repository would collide with the history you're about
   to push.
5. Create it, and copy the HTTP clone URL it shows you.

## Point the vault at it

On the machine where your vault lives:

```bash
cd ~/git/lab-vault

# Where does it currently point?
git remote -v

# Rename the GitHub remote rather than deleting it. Keeping a second
# copy of your notes somewhere off this lab is sensible, and you'll
# see why at the end of this lesson.
git remote rename origin github

# Add your own server as the new default.
git remote add origin http://git.lab.internal/sam/lab-vault.git

# Push everything, and set this remote as the tracking default.
git push -u origin main
```

It'll ask for your Gitea username and password. Refresh the repository
in your browser and there's your journal: every entry since Module 0,
every script from Module 2, the whole history, on a server you built.

Take a second with that. In lesson 1.3 you learned what a commit was. In
1.4 you pushed to someone else's machine. Today you're running the
machine.

## Prove the round trip

The point of a remote isn't storage, it's that two places can stay in
step. Prove it:

```bash
# Make a change and send it.
echo "- Journal now hosted on UBNT01" >> Projects/lab-progress.md
git add -A
git commit -m "journal: moved to self-hosted Gitea"
git push
```

Then, from a *different* machine (your workstation if the vault lives on
your laptop, or the other way round), clone it fresh:

```bash
git clone http://git.lab.internal/sam/lab-vault.git
```

Two copies, one server, both in step. That's the workflow every
development team on earth runs, and you just built the middle of it.

## Keep the other copy

You renamed the GitHub remote instead of removing it, and here's the
reason: **your Git server lives on the same machine as everything else
in your lab.** If UBNT01's disk fails, or you delete the wrong VM, your
journal goes with it, and the journal is the part of this course you
can't rebuild.

So push to both when something matters:

```bash
git push origin main      # your server
git push github main      # the copy that isn't in your lab
```

That's the 3-2-1 idea in its smallest form: more than one copy, in more
than one place. Module 15 makes it a real backup strategy rather than a
habit you have to remember. Until then, "push to both after a big
session" is enough, and it's more than most people do.

## The stacks too

While you're here, your compose files from lesson 6.5 deserve the same
treatment. Create a `docker-stacks` repository in Gitea and push the
`~/docker` directory you put under Git:

```bash
cd ~/docker
git remote add origin http://git.lab.internal/sam/docker-stacks.git
git push -u origin main
```

Now every service on this machine is described by a file, and every file
is in version control, with history. When Module 12 adds a SIEM and
Module 10 automates deployments, they land in the same place. That's not
tidiness for its own sake: it's the difference between a lab you can
rebuild and a lab you'd have to remember.

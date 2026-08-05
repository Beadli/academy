---
title: "15.9 Journal: what you can actually recover"
sidebar_position: 9
---

# 15.9 Journal: what you can actually recover

**Make a permanent note.** In your vault, create `Projects/lab-operations.md`
and record:

- **Your RPO and RTO** from lesson 15.1, and the reasoning. Not just the
  numbers: why those numbers are acceptable for this environment.
- **What is backed up, where it goes, and how often.** Include what is
  **not** backed up and why that is a decision rather than an oversight.
- **Where the restic password lives.** Not the password. Where it lives.
- **Your measured restore time** from lesson 15.3, next to your RTO, with the
  date you measured it.
- **The restore test log.** Date, what you restored, whether it matched. Add
  a line every month. This list is the evidence that the rest of the note is
  true.
- **What needs special handling**, from lesson 15.4: which services must be
  stopped, which databases need their own backup command.
- **Where the runbooks are**, and their review dates.

Then link it to `Projects/lab-changes.md` from lesson 15.8.

## Then today's daily note

Under **what I did**: the backup, and specifically the restore. The restore is
the achievement; the backup is just a command.

Under **what broke**: this module breaks quietly, which is the theme. A
restore that produced files in a path you did not expect. A database copy
that would not open. A cron job that did not run because of a path. Write
down **which, and what you checked before you understood it**.

Under **what I learned**: pick one.

- Why a backup you have not restored is a hypothesis, with your own evidence
- Why copying a live database file can produce a backup with nothing in it
- Why a domain controller cannot be restored like a file server
- Why `serial: 1` is the whole safety property of a patching playbook

Under **open questions**: the good ones here are about coverage and honesty.
What in your lab is not backed up, and would you notice? If UBNT01's disk
died tonight, what exactly would you have lost, and how long would you be
rebuilding? Which of your runbooks has never been followed by anybody?

## The exercise worth doing before you close

Answer this in writing, honestly:

**If your laptop were stolen tonight, with every VM on it, what would you
still have, and how long would getting back take?**

Work through it properly rather than reassuring yourself:

- Your journal is in Gitea (on the stolen laptop) and GitHub (not). **You
  have it.**
- Your compose files and playbooks are in Git, pushed. **You have them.**
- Your restic repository is on a USB drive. Was it plugged into the laptop?
  **Then you do not have it.** That is the "off-site" part of 3-2-1 being an
  actual requirement rather than a slogan.
- Your VMs themselves: gone, and you would rebuild from Modules 3 to 7.
- Your domain: gone, unless you have that system state backup somewhere else.

**Whatever gaps that exercise finds are the most useful output of this
module.** Write them down as findings, not as intentions. "The backup drive
lives permanently plugged into the machine it backs up" is a finding with a
fix, and it is the single most common real-world backup failure.

## Close the loop

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 15 complete"
git push
```

And the automation, which is now infrastructure rather than an exercise:

```bash
cd ~/ansible
git add -A
git commit -m "playbooks: patching and rescan automation"
git push
```

Tick Module 15 in `Projects/lab-progress.md`.

:::warning[Two things not to commit]
**Not the restic password**, obviously, and check you did not paste it into a
playbook or a crontab you committed. `git log -p | grep -i password` is worth
running once.

**Not the domain controller system state backup**, or anything derived from
it. Lesson 14.8 established that it contains every credential in your domain.
It belongs on backup storage, not in a repository.
:::

## And a real habit to leave with

Put a recurring monthly reminder somewhere you will see it:

> **Restore one thing. Write the date in `Projects/lab-operations.md`.**

Five minutes, once a month. It is the only thing on the list that proves any
of the rest of it works, and it is the item most likely to be quietly dropped
once the module is over.

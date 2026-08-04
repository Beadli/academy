---
title: "10.10 Journal: the machines describe themselves now"
sidebar_position: 10
---

# 10.10 Journal: the machines describe themselves now

**Make a permanent note.** In your vault, create `Projects/lab-automation.md`
and record:

- Where your Ansible repository lives, both on UBNT01 and in Gitea
- The **virtual environment** convention: `~/ansible/.venv`, activated with
  `source .venv/bin/activate`, rebuilt from `requirements.txt`. Write this
  down, because "command not found" a month from now is otherwise ten minutes
  of confusion.
- What each playbook does, in one line each
- Which groups exist in your inventory and what is in them
- For Tier 2: your Kerberos realm in capitals, and the fact that clock skew is
  the first thing to check

## Then today's daily note

Under **what I did**: what you automated, and what you deliberately did not.

Under **what broke**: this module has two clusters of failure and yours will be
in one of them. Either a playbook that did something you did not intend, which
is a reading failure, or Kerberos, which is a configuration failure. Both are
worth writing down specifically, because the Kerberos one in particular is
something you will meet again and will not remember the fix for.

Under **what I learned**: pick one and write it in your own words.

- Why `changed=0` on a second run is the whole point rather than a detail
- What the rebuild in 10.8 revealed that your playbooks did not cover
- Why staging in Git matters more for a repository that configures machines
  than for one holding notes

Under **open questions**: this module leaves good ones. What would it take to
run these playbooks automatically instead of by hand, and what would have to be
true before you trusted that? How would you test a playbook before it touched
anything real? Where does the machine's *existence* get described, rather than
its configuration?

That last one is provisioning, and it is the honest edge of what this course
covers.

## The rebuild list

Lesson 10.8 had you write down what a machine would need if it vanished, then
find the gaps. **Put that list in the permanent note, with the gaps marked.**

It is the most valuable artefact in this module. It is a tested statement about
what you can and cannot recover, and almost nobody has one.

Then close the loop:

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 10 complete"
git push
```

Tick Module 10 in `Projects/lab-progress.md`.

And commit the automation repository too, which is now a separate thing you
maintain:

```bash
cd ~/ansible
git status
git add -A
git commit -m "ansible: module 10 complete"
git push
```

Two repositories, two habits, same rhythm.

---
title: "11.4 The review discipline that makes this safe"
sidebar_position: 4
---

# 11.4 The review discipline that makes this safe

This is the most important lesson in the module. Everything else is
convenience; this is the part that decides whether the tool makes you better
or makes you confidently wrong at scale.

## Git is the safety net, and it is not optional

An agent proposes a change. You approve it. The file is different now.

If that file is in Git, you can see exactly what changed and undo it in one
command. If it is not, you are relying on your memory of what the file said
five minutes ago, which is worse than you think.

```bash
# What did it actually change?
git diff

# Nothing yet? Then it created files rather than editing them.
git status --short

# Undo everything uncommitted.
git restore .
```

**Work in a repository, and commit before you start.** A clean tree before an
agent session means `git diff` afterwards shows precisely its work and nothing
else. That single habit converts "I think it edited three files" into a fact.

This is the same rhythm from lesson 1.3, doing a job it was not designed for
and doing it well.

## Read the diff, not the summary

The agent will tell you what it did. That summary is written by the same
process that made the change, so it shares any misunderstanding the change
does.

**The diff is evidence. The summary is testimony.**

Read the diff. Every time, at first. Later you will develop a sense for which
tasks need a careful read and which need a glance, but that sense comes from
having read a lot of them, and the only way to get there is to start.

:::warning[The failure mode is social, not technical]
Nobody decides to stop reviewing. It erodes.

The first ten diffs you read carefully, and they are all fine. The eleventh you
skim, because the first ten were fine. By the thirtieth you are pressing accept
while thinking about something else, and the tool has trained you to do it by
being right often enough.

Then one is wrong, and it is wrong in a way that looks like all the right ones.

There is no technical fix. The countermeasure is a rule you set in advance and
follow when it is inconvenient: **anything touching a domain controller,
anything that deletes, anything in a firewall gets read line by line, no matter
how many correct diffs came before it.**
:::

## Four questions for any diff

**Did it change only what I asked?** The most common real failure is not a
wrong change, it is an extra one. A helpful tidy-up of something you did not
mention, in the same commit, which now hides in your history.

**Do I understand every line?** Lesson 1.6's rule, unchanged. If there is a
flag you do not recognise, ask before approving. The tool that made the change
will happily explain it.

**What happens if this is wrong?** Not "is it wrong" but "what does wrong cost
here". A typo in a journal note costs nothing. A typo in a firewall rule costs
your afternoon or your job.

**Would I have written this?** Not identically, but in shape. If the approach
is one you would not have chosen, that is worth a conversation before an
approval. Sometimes it knows something you do not. Sometimes it has pattern
matched to a different situation.

## Verify by running, where you can

Reading catches a lot. Running catches more.

You already have the tools, from earlier modules, and this is where they earn
their keep:

```bash
# Ansible, from Module 10: what would this actually do?
ansible-playbook harden.yml --check --diff

# nginx, from Module 6: is this config even valid?
sudo nginx -t

# A shell script, without running it.
bash -n script.sh

# Python, without running it.
python3 -m py_compile script.py
```

**A change to something with a syntax checker should never be approved without
running the checker.** It costs seconds and it catches the class of error that
is embarrassing rather than interesting.

## The rule about scale

One machine before thirty. This is the same rule as lesson 10.1, and it applies
harder here, because an agent will happily write the version that hits
everything.

```bash
# From Module 10. Still the right instinct.
ansible-playbook harden.yml --limit ubnt01 --check
```

## What to do when it is wrong

It will be wrong. The useful response is not to stop using it, and not to fix
the output silently.

**Tell it what was wrong and why.** Partly because you get a better next
attempt, and partly because articulating the error is how you find out whether
you actually understood it.

**Then write it into the context file** if it is a mistake it could make again.
That is how lesson 11.3's file grows: every recurring correction becomes a
line, and the same error stops happening.

That loop, correct then encode, is the difference between a tool that stays
mediocre and one that gets noticeably better at your specific environment over
months.

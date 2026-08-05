---
title: "11.2 Get an agent running against your own lab"
sidebar_position: 2
---

# 11.2 Get an agent running against your own lab

This lesson uses **Claude Code**, the terminal agent from the company whose
chat window you set up in lesson 1.6. It is what I use to run my own lab, and
it is what this course was written with.

:::note[Other tools exist, and the concepts transfer]
There are several agentic CLI tools now, from different vendors, and more will
exist by the time you read this. They differ in detail and agree on the shape:
a terminal session, a context file, permission controls, and packaged
procedures.

Learn the shape here. If your employer uses a different one, you will be
reading its documentation for the differences rather than starting over.
:::

## Where to run it

**Not on a domain controller. Not on your firewall.** Run it on your own
machine, or on UBNT01.

That is not superstition. An agent runs commands, and lesson 11.7 goes into
what that means properly. For now: give it somewhere with real work to do and
limited ability to ruin your week.

Your **journal vault** from Module 1 is the ideal first target. It is text you
own, it is in Git so every change is reversible, and there is nothing in it
that breaks if a command goes wrong.

## Install and start

Install it following the current instructions at
[code.claude.com](https://code.claude.com). Deliberately not reproduced here:
install methods for actively developed tools change, and a stale command in a
course is worse than a search.

**How we know it installed.** Open a new terminal, so you are not relying on
the one the installer touched, and run the command:

```bash
claude
```

**Success looks like an interactive prompt** waiting for you to type. If you
get `command not found`, the install did not put it on your PATH, and the
usual fix is to close and reopen your terminal, which is the same reason you
reopened one after installing Git in lesson 1.3.

Now the part that matters more than the install:

```bash
# Start it INSIDE the directory you want it working on.
cd ~/git/lab-journal
claude
```

The directory you start in is the directory it works in. Starting an agent in
your home directory gives it your whole home directory, which is a larger
blast radius than the job needs.

**Working directory is your first and cheapest safety control.** Use it.

## Your first three tasks

Do these in order. They escalate deliberately, from reading, to writing
something reversible, to touching real work.

**One: make it read.**

> Read my journal entries from the last two weeks and tell me which lab
> machines I mention most often, and what I was struggling with.

No changes, and it forces the agent to actually read your files rather than
answer from general knowledge. If the answer does not match what you remember
doing, that is worth knowing on a task where nothing is at stake.

**Two: make it write something small and reversible.**

> Create a note at `Projects/lab-hosts.md` listing every machine mentioned in
> my journal, with its address and role where I have recorded one. Mark
> anything you inferred rather than found.

The last sentence is the technique. **Asking it to mark inference separates
what it read from what it guessed**, and the guesses are where the errors live.

Then read the file and check it against reality. Some of it will be wrong.
Finding out which parts, on a note that costs nothing, is the point.

**Three: make it explain something you already understand.**

> Explain what `harden.yml` does, task by task, and tell me anything in it you
> think is a mistake.

You wrote that playbook in Module 10. You know the answer. This is a
calibration exercise: you are testing the tool against a known result, so you
learn how much to trust it before you use it on something you cannot check.

:::tip[Calibrate on things you know before trusting it on things you do not]
This is the habit that separates people who get value from these tools from
people who get burned.

Every time you meet a new model, a new tool, or a new kind of task, spend the
first few minutes on work where **you already know the right answer.** You are
not testing whether it is clever. You are measuring how often it is confidently
wrong, in this domain, on this kind of question.

That number is different for different tasks. It is low for "explain this bash
one-liner" and much higher for "what does this vendor's obscure error mean".
Knowing which you are in changes how hard you check.
:::

## Say no to something

Before the end of this session, deliberately reject a suggestion.

Ask it to do something, and when it proposes the change, decline and ask why it
chose that approach. Not because the suggestion is wrong, but because the
interface is designed for approval, and getting comfortable with declining
early is worth doing while the stakes are zero.

The failure mode this module is built to prevent is the habit of pressing
accept because reading is slower than agreeing.

## What you have

An agent, running in a directory you chose, on files you own, in a repository
where every change is one `git diff` from visible.

That last part is lesson 11.4, and it is the one that makes the rest safe.

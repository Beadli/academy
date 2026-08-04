---
title: "10.1 Why automate, and the rule that keeps it safe"
sidebar_position: 1
---

# 10.1 Why automate, and the rule that keeps it safe

You hardened UBNT01 in lesson 6.3. You did it by hand: updated packages,
checked services, edited the SSH configuration, restarted the daemon.

Now imagine doing that on thirty servers.

Not the typing, which is bad enough. The *drift*. Server four gets a setting
server five does not, because you were interrupted. Server eleven was built
six months later by someone else who had a slightly different idea. Two years
on, nobody can tell you what is actually configured on any given box, and the
only honest answer to "are all our servers hardened?" is "probably most of
them".

That is the problem automation solves, and it is not really about typing speed.

## What Ansible actually is

A program that reads a file describing what a machine should look like,
connects to that machine over SSH, and makes it look like that.

Three things follow from that sentence, and each one is a reason it won:

**It is agentless.** Nothing is installed on the machines it manages. It logs
in the way you would, does the work, and logs out. No agent to deploy, no
agent to patch, no agent to be the reason a server is unreachable.

**It is declarative.** You describe the end state, not the steps. "This package
is installed" rather than "run apt install". The difference matters more than
it sounds, and lesson 10.4 is entirely about why.

**It is readable.** Playbooks are YAML, and a well-written one can be
understood by someone who has never used Ansible. That is not an accident; it
is the whole design goal, and it is why this module can hand you the rule
below with a straight face.

## The rule

**Never run automation you cannot read.**

Lesson 1.2 promised you would meet this properly here. That lesson deferred an
Obsidian plugin that would commit to Git for you, on the grounds that taking
the shortcut before you understood the commands meant never learning what
`git status` was telling you.

Same trade, larger blast radius. A playbook you do not understand will
configure thirty machines wrongly in the time it would have taken you to get
one wrong by hand. Automation does not make mistakes less likely. **It makes
them faster, simultaneous, and identical.**

:::warning[The war story every ops team has]
Someone runs a playbook against production that they got from a colleague, or
adapted from a blog post, or wrote at the end of a long day.

It contains a task that removes a package. The package has a dependency
nobody thought about. Thirty servers uninstall it in fourteen seconds, in
parallel, with no pause at the moment a human would have said "wait, why is it
removing that too?".

The failure was not the tool. The tool did exactly what it was told, quickly
and consistently, which is what it is for. The failure was that nobody read
the thing before pointing it at everything.

Practical version of the rule: **run it against one machine first, and read
the output.** Lesson 10.4 shows you a mode that tells you what *would* change
without changing anything, and it costs nothing to use.
:::

## Why this is the third rung

Lesson 1.6 laid out the ladder: build with your hands, script what you
understood, automate what you scripted, and only then delegate to an AI agent.
Each rung depends on the one below.

You are on the third rung now, and the reason it is the third and not the
first is worth being explicit about.

When lesson 10.3 hands you a playbook that hardens a server, you will be able
to read every line of it, because you did all of it by hand in Module 6. You
know what `PermitRootLogin no` does, what breaks if you get it wrong, and how
you would get back into the box. **The playbook is a summary of things you
already understand.**

Someone who started at Module 10 would see the same file as a magic spell.
They would run it, it would work, and they would have learned nothing except
that a file exists which does a thing. The first time it failed they would be
stuck, because you cannot debug an abstraction whose underlying layer you have
never seen.

That is why this course made you wait.

## What you will actually build

By the end of this module you will have a directory of playbooks, under Git,
that can:

- harden a fresh Linux server to the standard you set in Module 6
- deploy and configure your reverse proxy from Module 6.7
- run against Windows as well as Linux
- rebuild a machine you deliberately destroyed

That last one is the point of the whole exercise, and lesson 3.5 promised it:
**servers are cattle, not pets.** You have believed that intellectually since
Module 3. Lesson 10.8 makes you prove it.

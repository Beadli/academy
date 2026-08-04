---
title: "11.8 A real task, start to finish"
sidebar_position: 8
---

# 11.8 A real task, start to finish

Everything so far has been mechanics. This lesson is one real piece of work,
done the way you would actually do it, so the discipline is something you have
practised rather than read.

The task: **document your lab's network from what you actually built**, and
check it against reality.

You have the raw material scattered across nine modules: an addressing plan in
lesson 4.3, a firewall in Module 4, machines added in 5, 6, 7 and 8, journal
entries about all of it. What you do not have is one current document, and you
almost certainly have drift between the plan and what exists.

## Set up so review is possible

```bash
cd ~/git/lab-journal
git status --short        # clean tree before you start
```

A clean tree is not a formality. It is what makes `git diff` a precise record
of the agent's work rather than a mixture of yours and its.

## Ask, with the constraints that matter

> Read my journal entries and any notes in `Projects/`, and draft
> `Projects/lab-network.md` describing my lab's network as it currently
> stands: segments, machines, addresses, and what each machine does.
>
> Two rules. Mark every fact with where you found it, so I can check.
> And mark anything you inferred rather than read, separately, because
> those are the lines I need to verify against the actual machines.

Three things are doing work there:

**"as it currently stands"** rather than "as planned", which invites it to
notice contradictions between an early plan and later reality.

**"mark where you found it"** turns an assertion into a claim you can check in
seconds instead of re-reading nine modules.

**"mark what you inferred"** is the technique from lesson 11.2, and it is the
single most useful instruction in this module. **The inferred lines are where
the errors are.** Without the separation you have to treat every line with equal
suspicion, which is slow enough that you will stop doing it.

## Review it properly

```bash
git diff
```

Read the whole thing. Then, for the inferred section specifically, go and
check. Not from your notes: from the machines.

On UBNT01:

```bash
ip -brief address
```

On DC01, in PowerShell:

```powershell
Get-NetIPConfiguration
```

And on FW01, the interfaces and their addresses from the console you used in
Module 4.

**This is the part that makes the exercise worth doing.** You will find at
least one thing that is not what you thought. A machine at a different address
than your plan says, a service you moved and never wrote down, a network you
described once and changed twice.

That gap is not the agent being wrong. It is your documentation having drifted
from your infrastructure, which is the normal state of all infrastructure
documentation everywhere, and you have just found it with an hour's work
instead of during an outage.

## Correct, and encode

Fix the document with what you found. Then, per lesson 11.4:

**If the agent made a mistake it could repeat, put a line in the context
file.** "Machine names are uppercase." "The firewall is FW01, never 'the
firewall'." "Do not state an address unless you found it in a note; mark it
for me to check instead."

That is the compounding part. This session made your documentation correct.
The context file makes the next one better.

```bash
git add -A
git commit -m "docs: current network topology, verified against the machines"
git push
```

## What you should notice about how that felt

Compare the work you just did to writing that document by hand.

The agent did the tedious part: reading nine modules of notes, extracting
scattered facts, and assembling a structure. That would have taken you an
evening and you would have avoided it, which is why the document did not exist.

**You did the part that required knowing things**: judging which claims to
check, going to the machines, recognising what was wrong.

That division is the honest version of what these tools are for. Not "it does
your job". It does the reading and the first draft, and hands you a document
where the uncertain parts are marked, and you spend your time where your
judgement is the scarce resource.

If it had done all of it, unreviewed, you would now have a confident, tidy,
partly-wrong document in your repository, and you would trust it. That is the
version to avoid, and the only thing standing between the two outcomes is the
half hour you spent reading and checking.

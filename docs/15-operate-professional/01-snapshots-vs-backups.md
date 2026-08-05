---
title: "15.1 Snapshots, backups, and what restore means"
sidebar_position: 1
---

# 15.1 Snapshots, backups, and what restore means

Lesson 3.6 asked you to leave this as an open question: "what's the
difference between reverting a snapshot and restoring a backup". Here is the
answer, and it is more interesting than the definitions suggest.

## The difference that actually matters

Lesson 3.5 gave you the short version: "Snapshots live on the same laptop, in
the same folder, as the VM they protect. A dead SSD takes both."

That is true and it is only half of it. The deeper difference is **what each
one is for**.

**A snapshot is an undo button for a change you are about to make.** You take
it because you are about to do something risky and you want the previous
state back. It is short-lived by design; lesson 3.5 also explained the disk
cost of leaving them lying around. Reverting one throws away everything that
happened after it, deliberately, because that is the point.

**A backup is a copy of your data that survives the machine.** It exists for
things you did not plan: hardware failure, ransomware, a deletion nobody
noticed for six weeks, a building fire. It is long-lived, it lives somewhere
else, and restoring one is a considered operation rather than a click.

**The failure mode people actually hit** is treating a snapshot as a backup,
discovering it too late, and losing everything. The second most common is
having real backups and never testing them, which lesson 15.3 exists to fix.

There is one more distinction worth having, because it comes up in
interviews:

**Reverting a snapshot takes the whole machine back in time.** Restoring a
backup usually puts *data* back onto a machine that keeps running. If a user
deletes one file, you do not want to revert the file server to Tuesday and
undo everybody else's week. You want that one file back.

## Two numbers that decide everything

Before choosing any tool, professionals decide two numbers. They sound like
jargon and they are genuinely just questions.

**RPO, Recovery Point Objective: how much data can you afford to lose?**
If you back up nightly at 2am and the disk dies at 5pm, you have lost fifteen
hours of work. If that is acceptable, your RPO is a day. If it is not, you
back up more often. **RPO determines backup frequency.**

**RTO, Recovery Time Objective: how long can you afford to be down?**
If restoring your server takes six hours and the business needs it in one,
your backup strategy has failed even though the data is intact. **RTO
determines the restore method**, and it is the one people forget, because
they optimise for the backup running rather than for getting back.

For your lab, decide now and write it down:

- **RPO:** a day is fine. You can rebuild a day's lab work.
- **RTO:** an evening is fine. Nothing depends on your lab being up.

Those numbers being generous is *why* your lab strategy can be simple. The
skill is knowing that you chose them rather than defaulting into them, and
being able to say what would change if the answers were "an hour" and
"fifteen minutes".

:::tip[In GRC terms]
RPO and RTO are the two numbers a **business continuity** conversation is
built on, and an auditor will ask for them by name.

The reason they matter to a framework is not technical. They are the point
where the business states what it is willing to lose, in writing, which turns
an infrastructure decision into a documented risk decision. Module 16 asks
you for yours.
:::

## 3-2-1, properly this time

Lesson 6.8 introduced this: "more than one copy, in more than one place" when
you pushed your journal to both Gitea and GitHub, and said Module 15 "makes
it a real backup strategy rather than a habit you have to remember."

The full rule:

- **3** copies of your data
- **2** different media or storage types
- **1** copy off-site

Your journal already satisfies it loosely: the working copy on your laptop,
the Gitea copy on UBNT01, the GitHub copy off-site. **That is genuinely
3-2-1**, which is worth noticing, because people assume backup strategy has
to be complicated.

Two modern additions, both from ransomware:

**One copy offline or immutable.** Ransomware looks for backups and encrypts
them too. A backup your server can write to at any time is a backup an
attacker can destroy. This is why "append-only" storage and unplugged drives
came back into fashion. You met this idea from the other side in lesson 14.8:
an attacker who reaches your domain controller reaches everything it can
reach.

**Zero errors on restore tests.** Some people write it as 3-2-1-1-0. The
final zero is the only part that is a verb.

## What "restore" means when you say it precisely

Three different things get called restoring, and confusing them causes real
outages:

**File-level restore.** Put back one file or folder. Most common by far,
usually a deletion.

**Bare-metal or full-system restore.** Rebuild an entire machine from
nothing. Slow, rare, and the one your RTO is really about.

**Application-consistent restore.** Put back a *database* or a service such
that it actually works afterwards, rather than being a copy of files that
happened to be on disk. This is the one people get wrong, and lesson 15.4 is
entirely about it.

## What you take from this

A snapshot undoes a change you made; a backup survives the machine. You have
two numbers written down and the reasoning behind them. And you know that
"restore" names three different operations with very different costs.

Next lesson you make a real backup.

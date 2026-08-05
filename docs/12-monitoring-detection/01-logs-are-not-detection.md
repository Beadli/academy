---
title: "12.1 Collecting logs is not detecting"
sidebar_position: 1
---

# 12.1 Collecting logs is not detecting

Your lab already produces logs. DC01 records every authentication. UBNT01's
journal has every service start and every SSH connection. Nginx logs every
request. FW01 logs what it dropped.

Nobody is reading any of it, and if you collected all of it into one place,
still nobody would be reading it. **That is the distinction this module is
built on.**

## The three things people mean by "monitoring"

They get used interchangeably and they are different jobs.

**Collection** is getting events off the machine that produced them and into
somewhere central. Valuable on its own, for one reason worth stating: an
attacker who compromises a machine can edit its logs, and cannot edit the copy
that already left. Collection is mostly a plumbing problem.

**Search** is being able to ask questions of what you collected. "Did anything
authenticate as that account last Tuesday?" This is what a SIEM's index is for
and it matters during an investigation, which is after the fact.

**Detection** is a machine deciding, without being asked, that something is
worth a human's attention right now. **This is the hard one**, and it is the
only one that works while you are asleep.

Most organisations are much better at the first two than the third. It is easy
to be proud of a lot of collected data.

## Why the hard one is hard

A detection has to answer a question with no clean answer: **is this normal?**

Consider a single failed login on DC01. Almost certainly a typo. Five in ten
seconds from one address, less so. Five hundred across forty accounts, that is
password spraying. Same event type, four readings, and the difference is
volume, timing and spread, not the event.

Now the real problem. **Your lab's normal is not another lab's normal.** An
administrator logging in at 3am is alarming in an office and routine for
someone who does maintenance at night. A rule that works perfectly for one
environment is noise in the next.

That is why detection cannot be bought finished, and why "detection engineer"
is a job. Somebody has to know what normal looks like here.

:::tip[The signal-to-noise problem, stated properly]
Two failures, and they are not symmetrical.

A **false negative** is an attack you did not alert on. Obviously bad, and
obviously what everyone worries about.

A **false positive** is an alert for something benign. Individually harmless,
and this is the one that actually kills detection programmes. Enough of them
and the queue stops being read, at which point your false negative rate is
effectively one hundred percent, because nobody is looking at the true
positives either.

**The queue nobody reads is worse than no queue**, because it also carries the
belief that you are covered. Lesson 12.5 is entirely about this.
:::

## What makes a good detection

Four properties, and they are worth having as a checklist before you write
anything.

**It describes behaviour, not a string.** "A new service was installed on a
domain controller" survives an attacker renaming their tool. "A process called
`evil.exe` ran" does not.

**It is actionable.** The analyst who receives it can do something. An alert
saying "unusual activity detected" with no context is a message telling
somebody to go and find out, which is work you have created rather than work
you have done.

**It is tuned to this environment.** It knows your vulnerability scanner runs
on Wednesdays and does not alert on it. That knowledge lives nowhere else.

**It has a documented reason to exist.** Six months on, somebody will find a
rule firing constantly and want to delete it. If there is no note saying what
it was for, they will either delete something important or leave noise
forever.

## The scanner story, from the other side

Lesson 0.1 told you about an endpoint tool flagging an attack toolkit on a
domain controller, which turned out to be a credentialed vulnerability scan
doing exactly what it had been scheduled to do.

That story was told from the point of view of somebody who knew their
environment. This module puts you on the other side of it: **you will generate
that alert deliberately, in lesson 12.6, and triage it.**

The detection was not wrong. Credentialed scanning genuinely does look like
lateral movement, because it is the same protocols doing the same things with
valid credentials. The tool cannot tell the difference. The analyst can, and
only because they know something the tool does not.

That gap, between what the tool sees and what the analyst knows, is the entire
job.

## What you are about to build

An agent on each machine, shipping events to a manager on UBNT01. Rules that
decide which events matter. A tuned set of alerts you would actually be
willing to be woken up for.

And then you will attack your own lab and watch it notice.

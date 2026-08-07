---
title: "OPS-01 Restore a service without reading the runbook"
sidebar_position: 10
---

# OPS-01: Restore a service without reading the runbook

|  |  |
|---|---|
| **Objective** | Destroy a running service and bring it back from backup, timed, without opening your notes until you are stuck |
| **Success signal** | The service serves again, you have the elapsed time, and you have a written list of everything you had to look up |
| **Needs** | Module 15 |
| **Effort** | An evening |
| **Risk** | Destructive, and safe anyway because you snapshot first. Read step 1 before anything else |
| **Check** | Mechanical |

## Why this drill exists

Lesson 15.3 had you restore a directory. You checksummed it, deleted it,
brought it back, compared, and timed it. That was the right first restore and
it proved the backup works.

**It also had three things a real restore does not.** Your notes were open.
Nothing was actually broken. And you were restoring files, not a service.

Your own assessment already says this. **POA&M-05**, from lesson 16.7, reads:
*"Restore testing has one data point; no operating trend exists."* One
successful restore tells you the backup was readable that day. It does not
tell you whether you can do it when it matters.

This drill is the second data point, and it is deliberately harder than the
first.

## The three things that make it different

**You do not open your runbook until you are stuck.** This is the point of the
whole exercise. A runbook you have never tested is a document, not a control,
and the only way to find out what it is missing is to need it and not have it.
When you do give in and look something up, that is data: write down what you
needed and where you found it.

**You restore a service, not a directory.** Files coming back is not the same
as a service running. A container needs its image, its compose file, its
volumes and its database to be mutually consistent, and lesson 15.4 was about
exactly why those are the hard ones.

**You produce a comparison, not a result.** The number only means something
next to the number from 15.3. Faster is not automatically better and slower is
not automatically worse; what matters is that you now have a trend and a
reason for the difference.

## Your objective

**Destroy your Gitea service completely, restore it from backup, and get it
serving again, with a stopwatch running and your notes closed.**

Gitea is the right target and not an arbitrary one. It holds your journal and
your repositories, so it is the service whose loss would actually hurt, and it
is the one lesson 15.4 warned you about: a database inside a container, where
copying the files while it runs gives you a backup that restores into
something subtly broken.

Four things must be true when you finish:

1. Gitea serves over HTTPS again, at its normal name, and you can log in.
2. A repository you pushed before the destruction is present, with its history.
3. You have the elapsed time, measured from destruction to working service.
4. You have a written list of every time you gave in and looked something up.

**Point four is the deliverable**, more than the restore itself. It is the gap
analysis for your own documentation, and you can only produce it once.

## How you will know

```bash
# On UBNT01, after the restore. The service answers and the
# certificate is still the one your machines trust.
curl -sS -o /dev/null -w "%{http_code}\n" https://git.lab.internal
```

And the check that decides it: **log in and open a repository you pushed
before you destroyed it.** A Gitea that starts with an empty database is not
a restore, it is a fresh install, and the difference is the entire point.

<details>
<summary>Nudge, if you do not know where to start</summary>

Before you break anything, make yourself a way back that does not depend on
the backup working. Module 3 taught you the tool and lesson 15.1 taught you
why it is not a backup. Today it is the safety net *underneath* the thing you
are testing, which is a different job.

Then think about what "destroy" honestly means. Stopping a container proves
almost nothing, because everything the service needs is still sitting on
disk. The interesting question is what has to be gone before the restore is
a real test.

**Close your notes before you start the clock.** If you find yourself
reasoning about what your backup script does rather than remembering it, that
is the finding, and it belongs in the list.

</details>

<details>
<summary>Fuller hint, if you know the direction but not the shape</summary>

**Destroy has to include the volumes.** `docker compose down` removes the
container and leaves your data exactly where it was. The command that makes
this a real test is the one that removes volumes too, and if you have to look
up which
flag that is, write it down: you are already collecting findings.

**Three things have to come back, and they fail differently:**

- The **compose file**, which describes the service. If this is in Gitea, you
  have just met the circular dependency this drill exists to expose.
- The **volumes**, which hold the repositories and the database.
- The **certificate and reverse proxy config**, or the service comes back on
  plain HTTP and nothing trusts it.

**On the database specifically:** lesson 15.4's point was that a database
copied while running can restore into a state it never actually had. Your
backup either handled that or it did not, and this is where you find out.

**The thing worth checking before you start the clock**, because it is the
failure that ends restores in real organisations: where does your restic
repository password live? If the answer is "in my vault, on the machine I am
about to destroy", stop, and treat that discovery as the drill's most
valuable output.

</details>

<details>
<summary>Full walkthrough</summary>

### 1. Build the way back, first

**Snapshot UBNT01 before you touch anything.** Lesson 15.1 was clear that a
snapshot is not a backup, and that is still true. Its job here is different:
it is the escape hatch so that a failed restore costs you five minutes rather
than your Git server.

Name it something a stranger could read, like `before-ops-01`, per lesson 3.5.

**Then check the circular dependency, before the clock starts.** Answer this
out loud:

- Where is your restic repository password?
- Where is the repository URL or path?
- If UBNT01 were genuinely gone, could you still reach both?

If either answer is "in the vault, which is in Gitea, which is on UBNT01",
**you have found the most valuable thing in this drill and you have not run
it yet.** Fix that first: a copy somewhere off the machine, in whatever form
you would actually be able to reach at 3am.

### 2. Record what "working" means

You cannot prove a restore without a before.

```bash
# On UBNT01. A repository you know exists, and its most recent commit,
# so you can prove afterwards that history came back rather than
# just the service.
cd ~/git/your-repo && git log --oneline -1
```

Write that commit hash down on paper, or anywhere that is not UBNT01.

### 3. Close your notes and start the clock

Genuinely close them. The point is not to make it hard for its own sake; it
is that you cannot discover a gap in a document you are reading.

Note the time. A phone stopwatch is fine.

### 4. Destroy it

```bash
# On UBNT01. -v is the important flag: it removes the named volumes,
# which is where the repositories and the database live. Without it
# you are only restarting a container and proving nothing.
cd ~/docker/gitea && docker compose down -v
```

```bash
# Confirm it is really gone rather than assuming. Expect no gitea
# volumes listed, and the site to stop answering.
docker volume ls | grep -i gitea
curl -sS -o /dev/null -w "%{http_code}\n" https://git.lab.internal
```

**Expect the curl to fail outright**, not to return a page. If it still
serves, something is still running and you have not destroyed what you think
you destroyed.

### 5. Bring it back

This is the part with no instructions, on purpose.

You built the backup in 15.2 and restored from it in 15.3. Everything you
need is in that repository. Work it out, and **every time you give up and go
looking, write down what you looked for.**

Keep the list in this shape, because it is what turns the exercise into a
document:

| What I needed | Where I eventually found it | Should have been |
|---|---|---|
| the restic repo path | shell history | the runbook |

### 6. Prove it, then stop the clock

```bash
# The service answers again.
curl -sS -o /dev/null -w "%{http_code}\n" https://git.lab.internal
```

Then the real proof, in a browser: log in, open the repository from step 2,
and confirm the commit hash you wrote down is there.

**Stop the clock when the service works, not when the restore command
finishes.** Those are different moments and the gap between them is usually
where the surprises live.

### 7. Write the comparison

In your journal, next to the number from 15.3:

- The date, and the elapsed time.
- What you had to look up, from your table.
- What you would change in the runbook as a result.
- Whether you would have met the RTO you wrote in 15.1, honestly.

**That is the trend POA&M-05 asked for**, and you can now close it with
evidence rather than an assertion. Two data points is not much of a trend, and
it is infinitely more than one.

### 8. Decide about the snapshot

If the restore worked, delete the `before-ops-01` snapshot. Leaving snapshots
around is how a lab quietly runs out of disk, and lesson 3.5 said so.

If the restore did not work, **that is a finding, not a failure.** Roll back
to the snapshot, and write down what stopped you. A backup that cannot be
restored under drill conditions would not have been restorable in an incident
either, and you have just learned that for free.

</details>

## Going further

- **Restore to a different machine.** Everything above assumes UBNT01 still
  exists. A real disaster does not. Restoring onto a fresh VM tests the parts
  you did not test today: whether you can install restic somewhere new, reach
  the repository, and remember the password without the machine that held it.
- **Do it again next month.** POA&M-05 asks for a monthly cadence, and the
  third data point is where a trend starts being one. Put it in the calendar
  rather than trusting yourself to remember.
- **Have somebody else do it from your runbook**, with you not in the room.
  This is the only genuine test of a runbook, and lesson 15.7 was about
  exactly that.

## What this proves

You can bring back a service from nothing, and you know how long it takes,
which are two different claims and most people can only make the first. You
also know which parts of your own documentation are missing, because you found
them the only way anybody ever does.

The part worth defending is the list of things you had to look up. Anybody can
say their backups work. Being able to say "I restored it in fifty minutes,
here are the four things my runbook should have contained, and here is the
updated runbook" is a different order of answer.

:::note[Write this down before you close the tab]

In your own words, in your journal, while it is fresh:

- The moment you first reached for your notes, and what you were looking for.
- Whether your restic repository password would have been reachable if UBNT01
  had genuinely been destroyed, and what you changed as a result.

Six months from now you will remember that the restore worked. You will not
remember what you did not know at the time, which is the part worth keeping.

:::

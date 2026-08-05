---
title: "15.7 Runbooks somebody else can follow"
sidebar_position: 7
---

# 15.7 Runbooks somebody else can follow

A **runbook** is a document that tells somebody how to do one specific
operational task. Not how the system works, not why it was designed that way:
what to type, in what order, and how to tell whether it worked.

It sounds like the least interesting thing in this course. It is the artefact
most likely to get you promoted, for a reason worth understanding.

## Why they matter more than they look

**The test of a runbook is that somebody who is not you, at 3am, under
pressure, having never done this before, can follow it and succeed.**

That test is brutal, and everything about the format follows from it.

Three things happen in an organisation with good runbooks:

- **You stop being the single point of failure.** The person who is the only
  one who can restore the database does not get promoted, because they cannot
  be moved. This is counterintuitive and it is consistently true.
- **The task gets done the same way every time**, so when it fails you are
  debugging one procedure rather than four people's habits.
- **The procedure gets better**, because each person who follows it fixes the
  step that confused them.

And the reason to write them *now*: you have just spent fourteen modules
learning things you will forget. **Future you is somebody else**, and that
person will be grateful.

## What a runbook is not

**Not documentation of how the system works.** That is your permanent notes
in `Projects/`. A runbook is a procedure.

**Not a script.** If a task can be fully automated with no judgement, automate
it, as in lesson 15.6. A runbook exists for tasks that need a human in the
loop, or that happen too rarely to be worth automating, or where the
automation exists but somebody has to decide whether to run it.

**Not a wiki page nobody can find.** A runbook that is not linked from where
the alert arrives is a runbook nobody reads at 3am.

## The shape

Six sections. Every one earns its place.

```markdown
# Runbook: [what this does, in plain words]

## When to use this
The trigger. An alert name, a symptom, a schedule.
Also: when NOT to use it, if there is a similar procedure.

## Before you start
- Access you need (which account, which machine)
- Expected duration
- Impact: what breaks or goes offline while you do this
- Who to tell before you begin

## Steps
Numbered. One action each. Exact commands.
After each step that matters: how you know it worked.

## How you know it is finished
The end state, as something you can check rather than a feeling.

## If it goes wrong
The two or three most likely failures and what to do.
Including: how to back out, and who to escalate to.

## Notes
Last reviewed date. Last time it was actually used.
```

**The two sections juniors leave out are "Impact" and "If it goes wrong"**,
and they are the two that matter most under pressure. Somebody following your
runbook at 3am needs to know that step 4 takes the service offline for two
minutes *before* they run it, not after.

## Write one, for real

Write the runbook for restoring a file from backup, because you performed
exactly that in lesson 15.3 and the details are fresh.

Create `Projects/runbooks/restore-a-file.md` in your vault:

```markdown
# Runbook: restore a file or directory from backup

## When to use this
Someone deleted or corrupted a file on UBNT01 and needs it back.
Use for individual files and directories.

For a whole service, including its database, use
`runbooks/restore-a-service.md` instead, because a database
needs the extra consistency steps from lesson 15.4.

## Before you start
- **Access:** SSH to UBNT01 as an account with sudo
- **Also need:** the backup drive mounted at /mnt/backup.
  Check with `df -h /mnt/backup` before anything else
- **Duration:** 5 to 15 minutes for a small directory
- **Impact:** none. Restores go to a scratch location first
- **Tell:** whoever asked, that you have started

## Steps

1. Confirm the repository is reachable.
   `sudo restic -r /mnt/backup/lab-repo --password-file /root/.restic-password snapshots`
   You should see a list ending in a snapshot count.
   If this errors, STOP and go to "If it goes wrong".

2. Find the snapshot from before the file was lost.
   Read the Time column. Note the ID.

3. Check the file is actually in that snapshot before restoring.
   `sudo restic -r /mnt/backup/lab-repo --password-file /root/.restic-password ls <ID> | grep <filename>`
   No output means wrong snapshot. Go back to step 2.

4. Restore to a scratch location, NOT over the original.
   `sudo restic -r /mnt/backup/lab-repo --password-file /root/.restic-password restore <ID> --target /tmp/restore --include <path>`
   Expect a "Summary: Restored N files" line.

5. Find what you restored. restic recreates the full path
   under the target, so it is not directly in /tmp/restore.
   `find /tmp/restore -name '<filename>'`

6. Check it is the right thing. Open it, or check its size
   and date. Do not skip this.

7. Copy it into place.
   `sudo cp /tmp/restore/<full path> <destination>`

8. Fix ownership, which cp does not preserve by default.
   `sudo chown <user>:<group> <destination>`
   Compare against a neighbouring file with `ls -l`.

## How you know it is finished
- The file is at its original path
- `ls -l` shows the same owner and group as its neighbours
- The person who asked confirms it is the right version

## If it goes wrong
- **"repository not found"**: the drive is not mounted.
  `sudo mount /dev/sdb1 /mnt/backup` then retry from step 1.
- **"wrong password"**: the password file is missing or wrong.
  The password is in the password manager under "restic lab repo".
- **The file is in no snapshot**: it was created and deleted
  between backups. It is not recoverable. Say so plainly and
  record it, because that is an RPO problem rather than a
  restore problem.

## Notes
- Last reviewed: [date]
- Last used in anger: never yet
- Written after lesson 15.3
```

## Test it the only way that works

**Give it to somebody else and watch them fail.**

You cannot test your own runbook, because you already know the missing steps.
Every assumption you made is invisible to you and obvious to a stranger.

If nobody is available, the next best thing is time: **come back in three
weeks and follow it exactly as written**, doing only what it says. You will
find at least one step that assumes something.

**When you find a gap, fix the runbook rather than remembering the fix.**
That instinct, correcting the document instead of your own memory, is most of
what separates an operations engineer from somebody who is merely competent.

## Which ones to write

You do not need many. Write runbooks for tasks that are **rare, risky, or
handed to somebody else**, because those are where memory fails:

| Runbook | Why |
|---|---|
| Restore a file (just written) | Most common real request |
| Restore a service with its database | Needs lesson 15.4's ordering |
| Patch the domain controllers | Lesson 13.7's ordering, and getting it wrong is an outage |
| Rebuild a failed domain controller | Lesson 15.5's metadata cleanup and seize |
| Onboard a new machine into monitoring | Otherwise machines quietly go unmonitored |
| What to do when a Wazuh alert fires | The one that turns an alert into an action |

**Link them from where they are needed.** The patching runbook should be
referenced in the change record from lesson 15.8; the alert runbook should be
named in the Wazuh rule's own comment, so the person triaging finds it
without searching.

:::tip[In GRC terms]
Runbooks are evidence of **operational maturity**, and auditors ask for them
by name.

The reason is not that a document proves anything by existing. It is that a
runbook with a review date, a change history in Git, and a record of having
been followed demonstrates a *repeatable process* rather than one person's
knowledge. That distinction is what Module 16 assesses.
:::

## What you take from this

One real runbook, in the format the industry uses, for a task you performed
this module. And the understanding that a runbook's value is measured by
somebody else's ability to follow it, not by your confidence in it.

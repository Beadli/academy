---
title: "Module 15: Operate like a professional"
sidebar_position: 0
---

# Module 15: Operate like a professional

This module has no new technology in it, and it is the one that most changes
whether you are trusted with anything.

You have built an environment, monitored it, scanned it and attacked it.
None of that is *operating* it. Operating is the part that happens every
week for years: the backup that runs, the patch that gets applied on
purpose, the runbook somebody else can follow at 3am, and the record of what
changed. It is unglamorous, nobody puts it on a CV, and it is the difference
between a lab and an environment.

Four modules made promises that come due here:

- Lesson 3.5 said a snapshot is not a backup, and "Module 15 covers the real
  thing".
- Lesson 3.6 left "what's the difference between reverting a snapshot and
  restoring a backup" as an open question this module "takes seriously".
- Lesson 5.12 said "what happens if this single domain controller dies" is
  the right question, and that the production answer is proper backup and
  restore "rather than hypervisor snapshots at all".
- Lesson 6.8 called pushing to two remotes "the 3-2-1 idea in its smallest
  form" and said Module 15 "makes it a real backup strategy rather than a
  habit you have to remember".
- Lesson 13.7 said the scan, prioritise, fix, rescan loop "is what you will
  automate in Module 15".

What's in it:

- **15.1** snapshots, backups, and what restore actually means
- **15.2** a real backup, with restic
- **15.3** restore it, because a backup you have not restored is a guess
- **15.4** the hard ones: databases and containers
- **15.5** back up a domain controller, and put one back
- **15.6** automate the vulnerability loop
- **15.7** runbooks somebody else can follow
- **15.8** change discipline
- **15.9** journal entry
- **15.10** checkpoint

## What you need

**Lessons 15.1 to 15.4, 15.7 and 15.8 need only UBNT01**, so every tier gets
them. They are also most of the module's value.

**Lesson 15.5 needs the domain**, both controllers, so Tier 2 and up. Tier 1
students should read it: the concepts (system state, authoritative versus
non-authoritative restore, USN rollback) come up in interviews far more often
than they come up at a keyboard.

**Lesson 15.6 needs the Ansible from Module 10** and, ideally, the scanner
from Module 13. It works without the scanner; you get the patching half.

**You also need somewhere to put backups that is not UBNT01.** A USB drive,
a spare disk, a network share, or a cheap object storage bucket. Lesson 15.2
covers the options honestly, including the free one.

:::warning[The one habit this module is really about]
Every lesson here has a verification step, and in this module the
verification *is* the lesson rather than a check on it.

A backup job that reports success proves that a job ran. It does not prove
you have a backup. The only thing that proves you have a backup is putting
the data back somewhere and comparing it to what you lost.

If you take one thing from this module, take that.
:::

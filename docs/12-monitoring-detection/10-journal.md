---
title: "12.10 Journal: what you watch, and what you decided not to"
sidebar_position: 10
---

# 12.10 Journal: what you watch, and what you decided not to

**Make a permanent note.** In your vault, create `Projects/lab-detection.md`
and record:

- Where the manager runs, and UBNT01's memory after the increase
- Which machines have agents, and which do not, **and why not**. An
  unmonitored machine is a decision, not an oversight, and it should read as
  one.
- Your custom rules, by ID, with one line each on what they detect
- **Every tuning exception, with what it silences and what still fires.**
  This is the most important list in the note. Each one is a blind spot you
  created on purpose.
- Your level scheme from 12.4: what 12 means to you, and what you would do
  about it at 3am
- Where the detections repository lives in Gitea

## Then today's daily note

Under **what I did**: what you built, and one detection you wrote yourself.

Under **what broke**: this module's failures are unusually informative. A rule
that would not fire, and the decoder was not extracting the field you assumed.
An agent that said `Never connected`. A rule that fired constantly. Write down
which, and specifically **what you checked before you found it**, because that
sequence is the skill.

Under **what I learned**: pick one.

- Why a credentialed scan is indistinguishable from lateral movement, and what
  that means about tooling
- Why an alert queue nobody reads is worse than no queue
- Why absence detection is the category most setups are missing

Under **open questions**: good ones here. What in your lab would fail silently
that you have *not* covered? If your manager were compromised, what would you
lose, and how would you know? How would you test that a detection still works
six months from now?

## The exercise worth doing before you close

Take ten minutes and write the answer to one question:

**If an attacker were in your lab right now, which of your machines would tell
you, and which would not?**

Be honest. Machines with no agent will not. Machines whose noisy rules you
silenced may not. Anything that only alerts on an event, when the attacker's
first move is to stop events being produced, may not.

That list is the most useful thing this module produces, and it is what a real
detection engineering backlog looks like. Put it in the permanent note.

Then close the loop:

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 12 complete"
git push
```

And the detections repository, which is now a thing you maintain:

```bash
cd ~/detections
git add -A
git commit -m "detections: module 12 baseline and tuning"
git push
```

Tick Module 12 in `Projects/lab-progress.md`, and snapshot UBNT01 with the
stack working.

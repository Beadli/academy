---
title: "11.10 Checkpoint: delegate the drafting, keep the deciding"
sidebar_position: 10
---

# 11.10 Checkpoint: delegate the drafting, keep the deciding

Prove the module stuck. Most of this is behavioural rather than a command,
because the thing being tested is a working practice.

## The end-to-end test

1. Start an agent in your journal vault, with a clean Git tree.
2. Ask it to do something that changes files.
3. Read `git diff` before accepting anything.
4. Find at least one thing you would have done differently, and say so.
5. Commit the result, having verified it.

If you did that without skipping step three, you have the habit this module
exists to build.

## Commands

```bash
cd ~/git/lab-journal

# Clean tree before an agent session, so the diff is only its work.
git status --short

# After: exactly what changed.
git diff

# The escape hatch, if you need it.
git restore .
```

## Pass criteria

- [ ] An agent runs in a directory you chose deliberately, not your home
      directory (lesson 11.2)
- [ ] You calibrated it on a task where you already knew the answer, before
      trusting it on one where you did not (lesson 11.2)
- [ ] A context file exists describing your conventions, and you proved it is
      being read (lesson 11.3)
- [ ] You start agent sessions from a clean Git tree and read `git diff` before
      accepting (lesson 11.4)
- [ ] You have declined at least one suggestion and asked why it was proposed
      (lessons 11.2, 11.4)
- [ ] At least one skill exists, packaging a procedure you actually repeat
      (lesson 11.5)
- [ ] A generated journal entry was edited by you before committing, not
      accepted as written (lesson 11.6)
- [ ] A deny list exists covering at least SSH keys and any secrets paths, and
      you can say why each entry is there (lesson 11.7)
- [ ] You can explain prompt injection and why it resembles SQL injection from
      lesson 6.9 (lesson 11.7)
- [ ] `Projects/lab-network.md` exists, its inferred claims were checked against
      the real machines, and you found at least one discrepancy (lesson 11.8)
- [ ] `Projects/lab-ai.md` records your own line on what you will not delegate
      (lesson 11.9)

## What you can now say

That you use these tools, and that you can explain what you check.

The second half is what makes the first half employable. Plenty of candidates
now say they use AI tools. **Far fewer can describe their review discipline,
name what they refuse to delegate, or explain prompt injection as an
instruction-versus-data problem.** That is the difference between someone who
has used a tool and someone who has thought about it, and it is visible in about
thirty seconds of conversation.

The other thing worth saying is what lesson 11.8 found. "I generated a network
document from my notes, checked it against the machines, and found three places
my documentation had drifted" is a story about verification, which is the
skill actually being assessed.

Module 12 turns to monitoring and detection. You will use these tools there,
on rules where being subtly wrong means either missing an attack or drowning in
alerts, and the discipline from this module is what keeps that useful.

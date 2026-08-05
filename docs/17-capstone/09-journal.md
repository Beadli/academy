---
title: "17.9 Journal: finish the course"
sidebar_position: 9
---

# 17.9 Journal: finish the course

Last journal entry. This one is different from the sixteen before it.

## The permanent notes

Two, and then the course's records are complete.

**`Projects/incident-2026-01.md`** is your working note, already written.
Change its status to Closed and add the closing timestamp. **Do not tidy the
working log**; the mess is the record, and a note that reads too cleanly is a
note that was rewritten afterwards.

**`Projects/lab-progress.md`** gets its last tick. Tick Module 17.

Then look at that file properly, because you have been filling it in since
lesson 1.2 and this is the last time you will open it as a student. Eighteen
modules. Read the "My setup" section you wrote in Module 1, when you did not
know what a domain controller was.

## Then today's daily note

Under **what I did**: the incident, end to end, in three sentences.

Under **what broke**: this module's version of "broke" is what your
monitoring missed, and you have it written down honestly from lesson 17.3,
captured at the only moment you could still be objective.

Under **what I learned**: pick one, and write it properly, because this is
the last one.

- Why a baseline captured before an incident is worth more than any tool
  during one
- Why containment and eradication are separate phases
- Why "initial access not established" is a better sentence than a guess
- What it felt like to have a POA&M item you wrote in Module 16 come back and
  cost you something real

Under **open questions**: the good ones now are about what you do next.
Which of the eighteen modules do you understand well enough to teach? Which
did you get through without really understanding? What in your lab do you
still not know how to fix?

**That middle question deserves a real answer.** There is almost certainly at
least one module you completed by following instructions. Naming it is not a
failure; it is the most useful thing you can write today, because it tells
you where to go back.

## The exercise that closes the course

Write two things.

**First: the one-page version of what you built.** Imagine explaining your
lab to a competent person who knows nothing about it, in one page, with no
diagram. What is it, what is it for, how do the pieces connect, what would
break if each piece failed.

**If you cannot do it in a page, you do not understand it yet**, and that is
worth knowing. This is the same test lesson 0.1 set on your first evening,
when it described the morning login chain and said the person who can follow
it end to end is rare and gets hired. **Follow your own chain now.**

**Second: what you would do differently if you started over.** You have
opinions now that you did not have in Module 0. Different tier, different
tooling choices, more time on one module and less on another.

Those opinions are the actual output of this course. Anybody can follow
instructions; **having a defensible view about how you would build it
differently is what expertise looks like early on.**

## Close the loop, for the last time

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 17 complete, course finished"
git push
```

And the portfolio from lesson 17.8, which is the one that is public:

```bash
cd ~/git/lab-portfolio
git add -A
git commit -m "portfolio: incident report, assessment summary, triage"
git push
```

## One last piece of housekeeping

**Your lab is still running, and it is now your responsibility rather than a
course exercise.**

Three things that keep it from decaying, and each takes minutes:

- **The monthly restore test** from lesson 15.3. Put it in a calendar. This
  is the one that quietly gets dropped once the course is over, and it is the
  one that matters most.
- **The patching schedule** from lesson 15.6, if you automated it. Check the
  logs occasionally, or it is scheduled work nobody reads.
- **The POA&M** from lesson 16.7. It has dates on it, and this incident just
  demonstrated what happens when items are not worked.

**And decide what to leave running.** A lab that costs you nothing to keep on
is worth keeping on. If yours needs the laptop, powering the VMs off between
sessions is fine; the snapshots and the backups mean nothing is lost.

## What happens next

Lesson 0.4 said "the suffering is the curriculum. It's also temporary." You
are at the end of the temporary part.

You have a working enterprise, an assessment of it, an incident report about
it, and a portfolio. What you do not have yet is **repetition**, and that is
the difference between having done something once and being able to do it.

**[Drills](/drills)** is where that goes. Exercises against the lab you built
rather than more instructions for building it: attack your own domain and
check whether your detections notice, write and tune rules against real
techniques, run automation with a defined outcome, practise finding things
that are broken.

The lab was never the point. Using it is.

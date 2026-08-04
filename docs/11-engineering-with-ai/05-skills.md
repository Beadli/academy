---
title: "11.5 Skills: packaging the procedures you repeat"
sidebar_position: 5
---

# 11.5 Skills: packaging the procedures you repeat

Lesson 11.3 taught the agent about your environment. This lesson teaches it a
**procedure**: a job you do repeatedly, done your way, invoked by name.

Claude Code calls these **skills**. Each is a folder containing a `SKILL.md`
that describes when to use it and how to do it. Other tools have equivalents
under other names, and the idea is more durable than any of the names.

## Recognise the candidate

A procedure is worth packaging when three things are true:

**You do it repeatedly.** Once is a request. The fourth time is a skill.

**You do it a specific way.** If any reasonable approach would do, you do not
need to write it down. The value is in encoding *your* conventions.

**Explaining it takes longer than doing it.** That is the moment. When you find
yourself typing three paragraphs of "and remember to put it in this folder, in
this format, and don't touch the headings", the paragraphs are the skill.

Your journal is the obvious first one. You have a vault with a fixed structure,
a template with four headings, and a set of rules about what goes where. You
have already explained that to the agent more than once.

## Write one

Create `~/.claude/skills/lab-journal/SKILL.md`:

```markdown
---
name: lab-journal
description: Turn a lab session into a journal entry in my vault, following
  my structure and voice.
---

# Lab journal entry

Use this when I say I have finished a lab session and want it written up.

## Where things go

- Daily notes: `~/git/lab-journal/Journal/<YYYY-MM-DD>.md`
- Create from `Templates/Daily.md` if today's does not exist
- Never invent a new folder

## The four headings, which do not change

What I did / What broke / What I learned / Open questions

## How to write it

- First person, past tense, my voice. Do not tidy my phrasing.
- **Keep the dead ends.** What broke is the most valuable section and
  the one I am most tempted to leave out.
- Machine names uppercase: DC01, UBNT01.
- Never write a password or key into a note, even an example one.

## Before you finish

- Show me the diff before writing
- Remind me to commit and push
```

Read what that is. It is not code. **It is the instruction you would give a
competent colleague**, written down once so you never give it again.

## Use it

```text
/lab-journal
```

Or just describe the job; a well-described skill gets picked up when the work
matches.

The first few runs will be wrong in small ways. That is expected, and it is the
same loop as lesson 11.4: correct it, then **edit the skill so the correction
is permanent**. A skill is a living document that gets better every time it
disappoints you.

:::tip[This is documentation that happens to be executable]
Look at that file again with the agent removed from the picture.

It is a written procedure. It says where files go, what the conventions are,
what to keep, what never to do. If your agent vanished tomorrow, it would still
be the best onboarding document for that task you have ever written.

**That is the real reason to write skills, and it is why the discipline
survives whatever tool you use next.** Most infrastructure teams have this
knowledge entirely in people's heads. Writing it down has always been valuable;
having something that can act on it just gives you a reason to finally do it.
:::

## Skills worth having in a lab

From my own set, as a starting list rather than a prescription:

**Journal writing**, as above. The highest-value one because it is the task you
are most likely to skip.

**Documentation lookup**, which fetches current vendor documentation before
answering rather than relying on training data. This matters more than it
sounds: infrastructure documentation changes, and a confident answer from
eighteen months ago is worse than no answer.

**A troubleshooting log**, which records what broke, what you tried, and what
worked, in a consistent format so it accumulates into something searchable.

**Anything with a checklist you keep half-remembering.** The steps to build a
new VM to your standard. The things to check before promoting a change. If you
have a checklist in a note somewhere, it is a skill.

## Where they live and who can see them

Personal skills live in your home directory and follow you between projects.
Project skills live in the repository and are shared with everyone who clones
it.

The same split as context files in 11.3, and the same caution: **a skill in a
shared repository is an instruction anyone with commit access can change.**
Lesson 11.7 takes that seriously.

## The honest limit

A skill makes the agent consistent. It does not make it correct.

If your procedure is wrong, you have now automated a wrong procedure and made
it repeatable, which is worse than doing it wrong occasionally by hand. Skills
are worth writing for procedures you have *already validated* by doing them
manually, which is the same argument as every other rung of the ladder.

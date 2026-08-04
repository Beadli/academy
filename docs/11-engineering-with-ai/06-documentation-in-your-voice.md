---
title: "11.6 Documentation that sounds like you"
sidebar_position: 6
---

# 11.6 Documentation that sounds like you

Lesson 1.6 promised this one: turning a lab session into notes without the
twenty minutes of "ugh, documentation".

It is the most immediately useful thing in the module, and the place people
most often produce something worse than what they would have written
themselves. Both halves are worth understanding.

## The raw material you already have

Your terminal history is a record of what you actually did, in order,
including the parts that did not work.

```bash
# The last fifty commands, numbered.
history 50

# Just this session's, on a fresh shell.
history
```

That is the input. Not your memory of the session, which has already quietly
edited out the twenty minutes you spent going the wrong way. **The history has
the dead ends in it, and the dead ends are the valuable part.**

## The ask that works

Vague requests produce corporate mush. Specific requests produce something you
can edit.

Bad:

> Write up my session.

Better:

> Here is my shell history from tonight. Write a journal entry for
> `Journal/2026-08-04.md` using my four headings. First person, past tense.
> Under "what broke", include the thing I spent twenty minutes on before
> realising the interface was on the wrong network. Do not tidy up my
> reasoning into something that sounds cleverer than it was.

The last sentence is the important one, and it is worth keeping in a skill so
you never have to type it again.

## Why the output sounds wrong, and how to fix it

Left alone, these tools write in a register that is fluent, slightly formal,
and completely characterless. You know it when you read it: everything is
"seamless", "robust", or "leverages", and no sentence is ever unsure.

Your journal should not sound like that. It should sound like you, six months
ago, telling yourself what happened.

Three things fix most of it:

**Give it a sample.** The fastest correction is to point at two of your own
entries and say "match this". Style transfers far better from examples than
from adjectives.

**Ban the tells explicitly.** Every register has them. In your context file:
"no em dashes, no 'seamless', no 'robust', no sentence that starts with
'Additionally'". Add to the list as you notice them.

**Insist on uncertainty.** Real engineering notes contain "I think", "not
sure why", and "this worked but I do not know if it was the right fix".
Generated text almost never does, and its absence is what makes documentation
read as untrustworthy. Ask for it directly.

:::warning[Editing is not optional, and the reason is not quality]
The output is a draft. Lesson 1.6 said so and it is still true.

The reason is not that it writes badly. It is that **writing the entry is part
of how you learn from the session.** The act of putting "I did not understand
why that failed" into words is what turns a confusing evening into knowledge
you keep.

Accept a generated entry unread and you get a tidy note and none of the
learning. That is a bad trade dressed up as efficiency, and it is the specific
way this tool can make you worse at your job while appearing to make you
faster.

Read it. Change the bits that are not how you would have said it. Add the thing
it could not know, which is what you were thinking at the time.
:::

## The other documents worth generating

**Runbooks.** "Here is the sequence of commands that fixed this. Turn it into a
runbook someone else could follow, and mark the steps where they need to
substitute their own values." Very good at this, because the structure is
predictable and you can verify it by following it.

**Post-incident notes.** When something breaks and you fix it, the write-up is
usually the thing that never happens. Getting a first draft out of the history
while the details are fresh means it exists at all, which beats a perfect note
you never wrote.

**Explaining your own old work.** Point it at a playbook you wrote four months
ago and ask what it does. Genuinely useful, occasionally humbling, and a good
signal about whether your comments were adequate.

## What not to generate

**Anything asserting a fact about your environment that you have not checked.**
It will confidently write "DC01 holds the PDC Emulator role" because that is
usually true, not because it looked. Notes are read later and believed. A
plausible wrong fact in your documentation is worse than a gap, because a gap
prompts you to check.

The discipline from lesson 11.2 applies: **ask it to mark what it inferred**,
and verify those lines before you commit them.

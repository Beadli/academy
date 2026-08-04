---
title: "11.1 What changes when the AI is in your terminal"
sidebar_position: 1
---

# 11.1 What changes when the AI is in your terminal

In Module 1 the loop was: hit a problem, copy the error, paste it into a
browser, read the answer, come back, type something.

An agent collapses that. It is already in the directory. It can read the file
you are asking about, run the command that reproduces the problem, see the
output, and propose a change to the actual file on disk.

Three things follow, and only the first is obvious.

## It has context you did not have to supply

The chat window knew what you pasted. An agent can read your inventory, your
playbooks, your journal, the actual error in the actual log.

That removes most of the friction, and it removes a failure mode you may not
have noticed: when you paste an excerpt, **you have already decided what is
relevant.** If the cause was three lines above what you copied, the chat
window never had a chance. An agent that reads the whole file does.

## It can act, not just advise

This is the real change, and it cuts both ways.

The chat window's worst outcome was bad advice you might follow. An agent's
worst outcome is bad advice **already applied** to twelve files before you
looked. Same wrongness, no gap in which to notice.

Everything in lesson 11.4 exists because of that sentence.

## The bottleneck moves to you

The old constraint was how fast you could type and search. The new constraint
is **how fast you can read and verify**, and that is the constraint this
course spent ten modules preparing you for.

An agent that produces work faster than you can check it is not making you
faster. It is building a backlog of things you have not read, which is a debt
that comes due at the worst moment.

:::tip[The honest description of what you get]
It is not a senior engineer. It is not junior either, which is why the usual
comparisons mislead.

It is closer to **an extremely fast, widely-read colleague with no memory of
your environment and no stake in the outcome.** It has read more documentation
than you ever will. It does not know that your DNS is unusual, that the last
person to touch that playbook left it broken, or that the change it is
proposing will page someone at 3am.

You supply the context and the judgement. It supplies breadth and speed. That
trade is genuinely valuable and it is not the same as delegation to a person.
:::

## What it is good at

From actual use, not from marketing:

**Reading things you did not write.** Somebody else's playbook, a config file
you inherited, a script with no comments. Asking what a file does before you
touch it is the single highest-value use of one of these.

**The first draft of anything.** A runbook, a playbook, a detection rule, a
journal entry. First drafts are where the tedium lives, and editing a wrong
draft is usually faster than facing a blank file.

**Explaining an error in context.** Not "what does this error mean" but "what
does this error mean *here*, given these files". That is the version the chat
window could not do.

**Mechanical transformation.** Rename this across forty files. Convert this
config to that format. Extract the addresses from this output. Tedious,
well-defined, easy to verify.

## What it is bad at

**Knowing what it does not know.** It will answer confidently about your
environment based on patterns from other environments. The failure is not
usually a wrong fact; it is a right fact about a different system.

**Anything where being subtly wrong is expensive.** Firewall rules. Anything
that deletes. Anything touching a domain controller. The output looks
identical whether it is right or catastrophic.

**Judging blast radius.** It does not feel the difference between a change to
your lab and a change to production, because it cannot see the difference. You
can.

**Knowing when to stop.** Ask for a solution and you will get one, whether or
not the right answer was "do not do this".

## The fourth rung

Lesson 1.6's ladder: build by hand, script what you understood, automate what
you scripted, delegate what you can verify.

Each rung is the same trade. You give up some direct control for reach, and
the price is that you must be able to check the result. A playbook you cannot
read is dangerous for exactly the reason an agent's diff you have not read is
dangerous, which is why Module 10 came first.

Nothing about the fourth rung suspends the rule. It raises the stakes on it.

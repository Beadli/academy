---
title: "Module 17: The capstone incident"
sidebar_position: 0
---

# Module 17: The capstone incident

Something is going to go wrong in your lab. You are going to detect it,
investigate it, contain it, recover from it, and write it up.

This module teaches almost nothing new. That is the point. Lesson 16.10 said
this one "asks you to demonstrate the environment rather than describe it",
and after sixteen modules of being told things, the last one asks what you
can do.

## How this works

You will run a script that plants an incident on UBNT01. It performs a
handful of actions over several minutes, in a **randomised order with
randomised delays**, some hostile and some ordinary. Then you investigate as
though you did not run it.

That randomisation is doing real work. You know roughly what kind of thing
happened, which is exactly the position a real analyst is in when an alert
fires. **What you do not know is what happened, in what order, or when**, and
the only way to find out is to read the evidence.

**The rule for this module, and it is the whole discipline:**

> **Investigate from the evidence, not from memory.** Every conclusion you
> reach must be supported by something you can point at: a log line, a
> timestamp, a file. If you know something only because you read the script,
> it does not go in the report.

That rule is lesson 12.6's instruction, grown up: *"work out whether it is
real, using only what the alert tells you, and write down your reasoning as
you go."*

What's in it:

- **17.1** the rules, and the shape of an incident
- **17.2** plant it
- **17.3** detect: what did your lab notice?
- **17.4** investigate: build a timeline
- **17.5** contain, and the decisions inside that word
- **17.6** eradicate and recover, and prove it
- **17.7** write the incident report
- **17.8** the portfolio, and how to publish it safely
- **17.9** journal: finish the course
- **17.10** checkpoint

## What you need

**Tier 1 and up.** The core of this module runs on UBNT01 alone, which means
nobody is excluded from the capstone.

**Your monitoring stack from Module 12 should be running.** If it is not,
you can still do 17.4 onwards from the machine's own logs, and 17.3 becomes a
finding rather than an exercise.

**Everything else you need, you already have**: the addressing plan from
lesson 4.3, written so you would still be able to read it this far into the
course; the journal with module numbers in its properties, which lesson 1.2
set up so you could pull up every note from the week you built the domain;
the runbooks from 15.7; and the GSS-1 package from Module 16.

**Take a snapshot of UBNT01 before you start.** Lesson 14.1's habit. The
cleanup script undoes everything, and a snapshot means you do not have to
trust it.

:::warning[Read both scripts before you run either]
Lesson 6.4 taught you not to pipe a script from the internet into a shell,
and lesson 1.6 gave you the rule about understanding a command before running
it. **That applies to me too.**

Lesson 17.2 prints both scripts in full. Read them. They create a user
account, an SSH key, a cron job and a sudoers rule on UBNT01, and the cleanup
script removes all four. Nothing is encrypted, nothing is deleted, nothing
leaves your machine.

If you are not willing to run a script you have read, that is the correct
instinct and you should not make an exception for a course. Type the commands
yourself instead; the module works the same way.
:::

## What you will have at the end

An **incident report** about a real investigation you performed, on
infrastructure you built, detected by monitoring you configured, in an
environment you assessed.

Combined with the Module 14 penetration test and the Module 16 authorisation
package, that is a portfolio covering build, attack, operate, assess and
respond. Lesson 0.5 promised that on day one:

> by the capstone, this journal becomes a portfolio, a written record of
> everything you built and every problem you solved, in your own words, and
> it interviews better than any certificate.

Lesson 17.8 is where you turn it into something you can actually show
somebody.

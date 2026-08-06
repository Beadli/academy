---
title: "Module 14: Adversary simulation"
sidebar_position: 0
---

# Module 14: Adversary simulation

<div className="stackLine">

Kali Linux · BloodHound · Impacket · Certipy · DVWA

</div>

You have spent thirteen modules building an environment and two of them
watching it. This module attacks it.

Everything here points at machines you built, on a network you own, from a
machine you control. That is not a disclaimer bolted on the front. It is the
first lesson, it has a gate you have to walk through, and the reason it comes
first is that the difference between a security professional and a criminal
is not skill. It is authorisation, and knowing exactly what yours covers.

## Why this module exists at all

Not to make you a penetration tester. Lesson 0.2 promised "a taste, aimed
strictly at your own lab", and that is what this is.

It exists because **you cannot tell whether a defence works until something
tries it.** You wrote detection rules in Module 12 and believed they were
good. You found vulnerabilities in Module 13 and prioritised them by
reasoning. Both of those are theories about your environment. This module
tests them, and some of them will be wrong, which is the entire value.

The most useful output of this module is not a compromised machine. It is a
list of the attacks your detections did not notice.

What's in it:

- **14.1** the authorisation gate, and writing real rules of engagement
- **14.2** reconnaissance, against your own baseline
- **14.3** a deliberately vulnerable target, and defence in depth from the
  other side
- **14.4** map the domain, and find the paths you did not know existed
- **14.5** asking the directory for credentials
- **14.6** pass-the-hash, finally
- **14.7** audit your own certificate templates
- **14.8** the crown jewels, and why domain controllers are different
- **14.9** what fired, what did not, and what you do about it
- **14.10** journal entry
- **14.11** checkpoint

## What you need

**Tier 2 and up.** This module attacks the domain from Module 5, so you need
DC01, DC02, KALI01 from lesson 4.4, and the segmentation from 4.6. Lesson
14.3 also uses UBNT01.

**Module 12's monitoring stack should be running for all of it.** Attacking a
lab with the detections switched off wastes most of the lesson. If your
machine cannot run the SIEM and the attacks at once, run each attack, then
start the stack and look at what it recorded; the logs are still there.

**Tier 1 students:** you have no firewall and no second domain controller,
but you do have DC01 and KALI01, so 14.2 and 14.4 through 14.8 mostly work.
Lesson 14.3 runs entirely on UBNT01 and needs no domain at all. Where a
lesson needs FW01, it says so.

:::warning[Read lesson 14.1 before running anything in this module]
Not as a formality. 14.1 is where you write down what you are allowed to
touch, and every later lesson assumes that document exists.

The techniques in this module are ordinary, publicly documented, and taught
in every security curriculum. That is exactly why the boundary matters: none
of this is hard to do, and the only thing separating legitimate testing from
an offence is a piece of paper saying which machines are yours.
:::

## A note on how this module is written

Each lesson has the same three parts, deliberately:

1. **What the attack is, and why it works.** The mechanism, not the command.
   A technique you can run but not explain is worthless in an interview and
   worse in a job.
2. **Doing it, against your lab.**
3. **What it looked like from the defensive side.** Every single time. This
   is the part that makes the module worth your evening, and it is why
   Module 12 came first.

You will find that some attacks are loud, some are almost silent, and the
ones that are silent are silent for structural reasons you can now
articulate. That distinction is the thing to take away.

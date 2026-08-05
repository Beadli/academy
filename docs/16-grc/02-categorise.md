---
title: "16.2 Categorise it: how much would it hurt"
sidebar_position: 2
---

# 16.2 Categorise it: how much would it hurt

Before you can decide which controls a system needs, you have to decide how
much you care about it. That is what **categorisation** is, and it is the
step that stops security being applied uniformly to things that deserve
wildly different amounts of it.

## The three questions

Categorisation asks what harm would result if each part of the classic triad
failed. In the US federal process this is **FIPS 199**, and the vocabulary is
worth having because the same three ideas underpin every framework:

**Confidentiality: what if the information were disclosed?**

**Integrity: what if it were modified without authorisation, or destroyed?**

**Availability: what if it were unavailable when needed?**

Each gets a rating of **Low**, **Moderate** or **High**, meaning the adverse
effect on operations, assets or individuals would be limited, serious, or
severe and catastrophic.

**Then the system takes the highest of the three.** That rule is called the
**high-water mark**, and it is worth understanding because it is where the
argument usually happens: one High rating drags the whole system up, and
people will try to talk you out of that rating for exactly that reason.

## Do it for GSS-1

Be honest rather than dramatic. Your lab is a lab.

Create `Projects/gss1-categorisation.md`:

```markdown
# GSS-1: security categorisation

## Confidentiality: LOW
The system holds no personal data, no customer data, and no
information of value to anyone else. It holds credentials for
itself, which matter only within the boundary.

Disclosure would embarrass me and would let somebody attack this
lab, which affects nobody else. Limited adverse effect.

## Integrity: MODERATE
Unauthorised modification would be serious rather than limited,
for one specific reason: this system is used to learn from, and
subtly wrong configuration teaches subtly wrong lessons that I
would carry into a real job.

The journal is also the record of the work, and a corrupted or
falsified journal undermines everything the system exists for.

## Availability: LOW
Nobody depends on this system. If it is down for a week, the
consequence is that I do not study for a week.

## Overall categorisation: MODERATE
By the high-water mark rule, driven by integrity.
```

**Notice the integrity argument**, because that reasoning is the actual
skill. The obvious answer for a personal lab is Low across the board, and it
would not be wrong. Rating integrity Moderate requires an argument about what
the system is *for*, and that argument is what a categorisation is.

**Assessors do not check your ratings against a table.** They read your
justification and decide whether you thought about it. A page of Lows with no
reasoning fails; a Moderate you can defend passes.

## Now the part everybody gets wrong

**The system's rating is not the same as every component's rating.**

Within GSS-1, some components would hurt far more than others:

| Component | If compromised | Why |
|---|---|---|
| **DC01 / DC02** | Highest impact | Lesson 14.8: `ntds.dit` holds every credential. Compromise here is compromise everywhere |
| **ROOTCA01** | Highest impact, lowest likelihood | Lesson 7.2: it signs everything. It is also powered off, which is the control |
| **UBNT01** | High impact | Monitoring, Git, and the backup source all in one place |
| **KALI01** | Moderate | Holds attack tooling and, per lesson 12.6, a suppression rule that makes it quiet |
| **FW01** | High | The boundary itself |

**This is why "we protect everything equally" is not a strategy.** Finite
effort spread evenly means the domain controllers get the same attention as
the testing box. Lesson 14.6's tiered administration is this idea applied to
accounts; categorisation is it applied to systems.

Add that table to your categorisation note. When you assess controls in
lesson 16.5, this is what tells you which findings are serious.

## The two numbers you already decided

Lesson 15.1 had you write down an RPO and an RTO and said:

> They are the point where the business states what it is willing to lose, in
> writing, which turns an infrastructure decision into a documented risk
> decision. Module 16 asks you for yours.

Bring them in, because **they are your availability rating expressed as
numbers**, and an assessor will notice if the two disagree.

Add to the note:

```markdown
## Recovery objectives
- **RPO: 24 hours.** A day of lab work is acceptable to lose.
- **RTO: one evening.** Measured restore time from lesson 15.3:
  [your measured number]. Consistent with an Availability rating
  of Low.
```

**If your measured restore time is longer than your stated RTO, say so here
rather than quietly adjusting one to match the other.** That mismatch is a
genuine finding, it goes in the POA&M in lesson 16.7, and noticing it is
exactly the value of doing this exercise. The instinct to make the numbers
agree by editing the easier one is the instinct this module exists to break.

## Where the categorisation goes next

Everything downstream depends on this number:

- **Which control baseline you use**, in lesson 16.3. A Moderate system gets
  more controls than a Low one.
- **How serious each gap is**, in lesson 16.7.
- **Whether the residual risk is acceptable**, in lesson 16.8.

**Categorise too high and you drown in controls that do not fit.** Categorise
too low and you under-protect something that mattered. Both happen constantly
in real organisations, and the second one happens more often because it is
cheaper in the short term.

## What you take from this

A defensible categorisation with the reasoning written down, a
component-level view showing that not everything inside a boundary deserves
the same attention, and your recovery objectives reconciled against a number
you actually measured.

Next lesson turns that categorisation into a list of controls.

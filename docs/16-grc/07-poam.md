---
title: "16.7 The POA&M"
sidebar_position: 7
---

# 16.7 The POA&M

A **Plan of Action and Milestones**, pronounced "po-am", is the list of your
gaps with a plan attached to each one. It is the document that turns an
assessment from a complaint into a commitment.

Lesson 16.1 said the surprising thing about it, and it is worth repeating
because it governs how you should write yours:

> A system with a POA&M full of honestly recorded gaps and realistic dates is
> in far better shape than one claiming everything is perfect, and assessors
> read it that way. An empty POA&M is a red flag, not a gold star.

## Why an empty POA&M is bad news

Put yourself in the assessor's chair. You are handed a Moderate system's
assessment saying every control is Implemented and there is nothing
outstanding.

**There are only two explanations, and one of them is very unlikely.** Either
this system is genuinely in perfect compliance with a Moderate baseline, or
the person assessing it did not look hard enough. Assessors have seen enough
of the second to assume it.

Whereas a POA&M with eight specific items, each with a plan and a date, tells
them: this person understands their system, knows where it is weak, and has a
plan. **That is a better position to be in, and it is also just true**, which
is easier to maintain.

## What each item needs

Six fields. Each exists because somebody once produced a POA&M without it and
it turned out to be useless.

| Field | Why |
|---|---|
| **Identifier** | So it can be referenced and tracked across versions |
| **The weakness** | Specific. "Improve monitoring" is not a weakness |
| **Which control** | Ties it to the assessment |
| **Remediation plan** | What will actually be done |
| **Owner** | A person. Not "the team", not "IT" |
| **Milestone date** | When. A real date, not "ongoing" |

**"Ongoing" is the word that kills POA&Ms.** An item with no date is an item
nobody is accountable for, and a POA&M full of them is a list of things that
will never happen. Lesson 13.8 made the same point about risk acceptances
with no review date; it is the same failure.

## Build it

Everything you need is in the assessment from lesson 16.5 and the register
from 16.6. Create `Projects/gss1-poam.md`:

```markdown
# GSS-1: Plan of Action and Milestones

**System:** GSS-1  **Owner:** [you]
**Created:** [today]  **Last updated:** [today]
**Review cycle:** monthly

| ID | Weakness | Control | Remediation | Owner | Due | Status |
|---|---|---|---|---|---|---|
| POA&M-01 | Segmentation was tested in Module 4 and not re-tested since, although the rule set has changed | SC-7 | Re-run the both-direction test from lesson 4.6 and record the result. Add it to the monthly restore-test reminder so both happen together | [you] | [+1 month] | Open |
| POA&M-02 | FW01 configuration is not under version control; rule changes are recorded only manually | SC-7, CM-3 | Export the OPNsense config to the Git repository on a schedule | [you] | [+2 months] | Open |
| POA&M-03 | Container application logs are not collected; DVWA attacks in lesson 14.3 produced no alerts | AU-2 | Configure the Wazuh agent to read container logs. Verify by repeating one attack and confirming an alert | [you] | [+1 month] | Open |
| POA&M-04 | Directory enumeration (BloodHound, lesson 14.4) is not detectable with current rules | AU-6 | Accepted as not signature-detectable. Investigate behavioural baselining as a longer-term option | [you] | [+6 months] | Open |
| POA&M-05 | Restore testing has one data point; no operating trend exists | CP-10 | Perform and log a monthly restore test. Re-assess CP-10 after three months | [you] | [+3 months] | Open |
| POA&M-06 | Audit record review (AU-6) is performed ad hoc rather than on a defined schedule | AU-6 | Define a weekly review of the alert queue. Record each review with date and outcome | [you] | [+1 month] | Open |
| POA&M-07 | Only 15 of the Moderate baseline controls have been assessed | CA-2 | Assess a further 15 controls, prioritising the AC and IA families | [you] | [+6 months] | Open |

## Closed items
| ID | Weakness | Closed | Evidence |
|---|---|---|---|
| (none yet) | | | |
```

**Add your own.** In particular, if lesson 16.5 found a mismatch between your
stated RTO and your measured restore time, that is a POA&M item with two
legitimate remediations: make recovery faster, or revise the objective with a
documented decision. Either is fine. Silence is not.

## POA&M-04 is worth studying

Look at that item again. The remediation is essentially "we have concluded
this is not solvable the obvious way, and here is what we will investigate
instead."

**That is a legitimate POA&M entry**, and knowing that saves you from the two
bad alternatives: pretending you will fix something you cannot, or omitting
it because you cannot fix it.

Lesson 14.4 established *why* it is hard: BloodHound collection is ordinary
authenticated LDAP traffic, and there is no signature because nothing
anomalous happens. Carrying that forward as a known, characterised,
non-trivial gap is better security than a rule that does not work.

**The general principle: a POA&M item can be an investigation.** What it
cannot be is a placeholder with no date.

## Closing items, and why the evidence column exists

When you complete something, do not delete the row. **Move it to the closed
section with the evidence that closed it.**

Two reasons, and the second is the one that matters:

- The history shows the system improving over time, which is what an
  assessor wants to see across successive assessments.
- **It stops you closing things without evidence.** "Done" is a claim; "done,
  and here is the alert that fired when I re-ran the attack" is a fact. This
  is lesson 13.7's rescan discipline applied to compliance: the fix is not
  closed because you performed it, it is closed because you re-verified.

Close POA&M-03 that way when you get to it: fix the collection, re-run the
DVWA SQL injection, confirm an alert arrives, and cite the alert.

## The rhythm this creates

A POA&M is not a document you write. It is a loop:

1. Assess, find gaps
2. Record them with owners and dates
3. Work them
4. Close them **with evidence**
5. Re-assess, which finds new gaps

**That loop is the same shape as the vulnerability loop from lesson 13.7 and
the detection-improvement loop from 14.9.** Three different domains, one
structure: measure, decide, act, re-measure. Once you see it, most of security
operations turns out to be that loop applied to different subject matter.

## What you take from this

A POA&M with real dates and real owners, an understanding that an empty one
is a warning sign, and one item that honestly says "this is hard and here is
what we will try instead".

Next lesson writes the document that holds all of it together, and then
somebody signs it.

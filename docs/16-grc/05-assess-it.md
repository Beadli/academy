---
title: "16.5 Assess it honestly"
sidebar_position: 5
---

# 16.5 Assess it honestly

Now the actual work. Fifteen controls, each graded against evidence, with the
grade written down and defensible.

**This lesson is mostly about resisting one temptation**, which is the
temptation to grade yourself well.

## The grades

| Grade | Meaning |
|---|---|
| **Implemented** | Doing it, and you can prove it with all three kinds of evidence |
| **Partially Implemented** | Doing some of it, or doing it without evidence of operation |
| **Planned** | Not doing it yet, with a plan and a date |
| **Not Implemented** | Not doing it, no plan yet |
| **Not Applicable** | Genuinely does not apply, with the justification from 16.3 |

**Partially Implemented is the honest answer far more often than people
use it**, and the most common reason is missing evidence of operation. A
control that is correctly configured but never reviewed is partial, not
complete, and grading it Implemented is the single most common
self-assessment error.

## How to assess one control

Four steps. Do them in order, and notice that step 3 is where the honesty
lives.

1. **Read what the control actually requires.** Not the title. The title of
   AU-6 is about reviewing audit records; the control text says how often and
   what you do with what you find. Titles flatter you; text does not.
2. **Find your evidence**, from the index in lesson 16.4.
3. **Ask what an assessor would say if they wanted to fail you.** This is the
   step that produces real grades. You are looking for the objection, not the
   confirmation.
4. **Write the grade with its justification.** The justification is the
   deliverable; the grade is a summary of it.

## Worked example, done properly

Take SC-7, Boundary Protection, where your evidence is strongest.

**What it requires:** monitor and control communications at the external
boundary and at key internal boundaries.

**Evidence:** the policy in `lab-network.md`, FW01's rules implementing it,
and the lesson 4.6 test showing traffic blocked inbound and permitted
outbound, with the exact commands.

**What would an assessor object to?** Three things, and finding them yourself
is the exercise:

- The both-direction test was performed once, in Module 4. There is no
  evidence it has been re-tested since, and the rules have changed since
  then (you opened 9392 in lesson 13.4 and 8081 in 14.3).
- FW01's configuration is not under version control, so there is no reliable
  record of what changed and when.
- The 8081 rule from lesson 14.3 was supposed to be removed. Was it?

**Grade: Partially Implemented.** Not because the firewall is bad, but
because the evidence of *ongoing* operation is missing and there is a
verification gap.

**That is a good finding and you should feel fine about it.** It is specific,
true, and fixable, and it came out of your own documentation rather than an
incident.

Go and check that last point now, actually:

```bash
# On UBNT01. Is the DVWA rule from lesson 14.3 still there?
sudo ufw status | grep 8081 || echo "removed, as intended"
```

**Whatever that returns is a real assessment result**, and it belongs in the
document either way.

## A second worked example, where you do well

CP-10, System Recovery.

**Evidence:** the restore drill from lesson 15.3, with checksums compared
before and after and a measured restore time.

**What would an assessor object to?** Genuinely not much, if you did it. The
one question is frequency: one restore test is a point, not a trend. If your
`lab-operations.md` has a single dated entry, this is **Implemented** with a
note that the operating record is young; if you have several months of
entries, it is Implemented and unusually well evidenced.

**Notice the difference between this and SC-7.** Same effort from you, but
one control has evidence of operation and the other does not. That is the
distinction from lesson 16.4 deciding a grade, which is what it is for.

## Now assess all fifteen

Create `Projects/gss1-assessment.md`. One entry per control, in this shape:

```markdown
# GSS-1: control assessment

**Assessor:** [you]  **Date:** [today]
**Scope:** the fifteen controls in gss1-control-selection.md
**Method:** documentary review and technical verification against
the evidence index. Where a check was re-run today, the command
and result are recorded.

---

## SC-7, Boundary Protection
**Grade: Partially Implemented**

**Implemented:** FW01 enforces a stated policy. Inbound from the
NAT segment to the lab is blocked, outbound is permitted. Tested
in both directions in lesson 4.6 with results recorded.
Host-level firewalling with ufw on UBNT01 adds a second layer.

**Gaps:**
1. The both-direction test has not been repeated since Module 4,
   and the rule set has changed since (9392 added in 13.4, 8081
   added and removed in 14.3).
2. FW01's configuration is not under version control, so change
   evidence depends on manual change-log entries.

**Evidence:** lab-network.md; FW01 rule screenshots; ufw status
output dated [today].

**POA&M:** items 1 and 2.

---

## CP-10, System Recovery
**Grade: Implemented**

**Implemented:** A full restore drill was performed on [date]:
data deleted, restored from the restic repository, and verified
byte-for-byte by sha256 comparison, which matched. Restore time
measured at [N] minutes against a stated RTO of one evening.

**Gaps:** the operating record is young. One test is a point, not
a trend. Monthly restore testing is scheduled.

**Evidence:** lab-operations.md restore test log; checksum
comparison from lesson 15.3.

**POA&M:** none. Re-assess after three months of test records.
```

Work through the rest. **Expect to spend real time on this**, and expect
roughly this distribution if you are being honest:

- **A few Implemented**, most likely CP-9, CP-10, RA-5, CA-8, AC-8. These are
  the ones where the course made you produce evidence of operation.
- **Most Partially Implemented**, usually for one of two reasons: no evidence
  of operation, or the control has a review-and-act requirement you have not
  been performing on a schedule.
- **One or two Not Implemented**, honestly recorded.

**If everything comes out Implemented, you have graded yourself wrong.** Go
back to step 3 and try harder to fail yourself. A first assessment of any
real system that finds no gaps has found only that the assessor was not
looking.

## The specific trap in AU-6

Assess this one carefully, because it is where Module 14 gave you an
uncomfortable answer.

**AU-6 is about reviewing audit records and acting on findings.** You have
excellent evidence for the *reviewing* part: the triage note from lesson 12.6
and the coverage table from 14.9.

**But the coverage table says several attacks produced no alert at all.** So
the honest grade has to account for the fact that you know your collection
has gaps, that you documented them, and that some remain open.

**Partially Implemented, with the coverage table as evidence, is a stronger
document than Implemented with no table.** An assessor who sees a table of
known gaps concludes you are measuring. One who sees an unqualified
Implemented concludes you have not looked.

That is the single most useful thing to understand about this whole
discipline: **honest, specific self-criticism reads as competence.**

## The mismatch you may have to write down

Lesson 16.2 warned about this. If your measured restore time from lesson 15.3
exceeds your stated RTO, you have two numbers that disagree, and the
assessment is where that becomes visible.

**Write the mismatch as a finding.** Do not adjust the RTO to match the
measurement, and do not claim a restore time you have not achieved. The
finding is: "stated RTO is X, measured recovery is Y, the gap is not
currently addressed." That goes to the POA&M with either a plan to speed up
recovery or a documented decision to revise the objective.

## What you take from this

Fifteen controls graded against real evidence, a set of specific findings you
discovered rather than suffered, and a document whose credibility comes from
what it admits rather than what it claims.

Next lesson organises the risks; the one after that organises the fixes.

---
title: "14.9 What fired, what did not"
sidebar_position: 9
---

# 14.9 What fired, what did not

This is the lesson the module exists for. Everything before it was generating
evidence.

The placeholder for this module always promised "watching your own detections
fire, and tuning what didn't". The tuning is the job.

## Build the table

Open your journal and your Wazuh dashboard together. For every attack you ran,
fill in one row. Do this honestly; the value is entirely in the gaps.

| Attack | Lesson | Did anything fire? | Should it have? |
|---|---|---|---|
| Network sweep and service scan | 14.2 | | |
| SQL injection against DVWA | 14.3 | | |
| XSS against DVWA | 14.3 | | |
| BloodHound collection | 14.4 | | |
| Kerberoasting | 14.5 | | |
| Pass-the-hash logon | 14.6 | | |
| Certificate template enumeration | 14.7 | | |
| DCSync | 14.8 | | |

If you predicted the answers before looking, mark your predictions too. The
gap between what you expected and what happened is the most useful thing on
the page.

## What the answers usually look like

Do not read this section before filling in your own table. Once you have:

**Loud, and you should have caught it:** the network scan (14.2) and
Kerberoasting (14.5). Both produce distinctive events in volume.

**Loud, but only if you were collecting:** DCSync (14.8) produces 4662, but
only with object access auditing enabled. Pass-the-hash produces 4624 with
NTLM, which you are certainly collecting.

**Effectively silent, for structural reasons:** BloodHound collection (14.4)
and certificate template enumeration (14.7). Both are ordinary authenticated
LDAP reads. There is no signature because there is nothing anomalous in any
individual request.

**Silent because you were not looking:** the DVWA attacks (14.3), where the
logs were inside a container your agent never read.

**Four different kinds of "nothing fired", and they need four different
responses.** That distinction is the professional skill in this lesson, and
it is why "improve our detection coverage" is a meaningless instruction
without it:

| Kind of gap | What it actually is | What to do |
|---|---|---|
| Not collected | The log source is not reaching the SIEM | Fix collection. No rule can help |
| Collected, no rule | The evidence is there, unexamined | Write the rule |
| Rule exists, suppressed | Your own tuning silenced it | Revisit the exception |
| Not detectable by signature | The activity is indistinguishable from normal | Behavioural baseline, or move the detection elsewhere |

## Now fix the ones worth fixing

You are not going to close every gap, and attempting it produces the alert
queue nobody reads from lesson 12.5. Pick deliberately.

**Do these three**, in this order, because they have the best ratio of value
to noise:

**1. DCSync detection (from 14.8).** The highest-value rule in the module.
Replication requests from anything that is not a domain controller have no
legitimate explanation, so the false positive rate is near zero.

First confirm you are collecting the event at all:

```bash
# On UBNT01. Are any 4662 events arriving?
sudo grep -c '"id":"4662"' /var/ossec/logs/alerts/alerts.json || echo "none found"
```

**If that is zero**, this is a collection problem. Object access auditing is
off by default on Windows. Enable it on DC01 and re-run the DCSync from 14.8
before writing any rule.

Then write it, using lesson 12.4's process and lesson 12.5's discipline of
testing before trusting.

**2. Kerberoasting detection (from 14.5).** Event 4769 with RC4 encryption
type, or one account requesting many service tickets in a short window.
Genuinely achievable, and it will need tuning, which is the realistic part.

**3. The container log gap (from 14.3).** Not a rule at all: a collection
change. Your agent needs to read the container's logs. This is the least
glamorous item and probably the most valuable, because it applies to every
containerised application you will ever add, not just the deliberately
vulnerable one.

## And revisit the exception you wrote

Lesson 12.6 had you suppress alerts from KALI01, with a comment saying it was
"deliberately narrow". Lesson 13.6 tested whether that was true by scanning
from a different host.

**This module ran almost everything from KALI01.** Look at your table again
with that in mind. How many of your blanks are blank because the activity was
genuinely undetected, and how many because you silenced the source address
back in Module 12?

That is a very uncomfortable question and it is the correct one. **The
exception you wrote to reduce noise may have hidden your entire assessment.**

You do not necessarily need to remove it. Real environments do have
authorised testing hosts. But you now have evidence about what it costs, and
the honest options are the same three from lesson 13.6: suppress narrowly,
suppress only during a window, or accept the noise.

Whatever you choose, **update the comment on that rule** so it records what
you learned here. A tuning decision with the evidence attached is worth
several times one without.

## Write the assessment

An assessment nobody can read is not an assessment. This is the deliverable,
and it is a portfolio piece.

In your vault, create `Projects/lab-assessment-2026.md`, adjusting the date:

```markdown
# Internal assessment: Beadli lab

**Tester:** [you]  **Dates:** [when]
**Authorisation:** Projects/lab-rules-of-engagement.md
**Scope:** 10.10.10.0/24

## Summary
Two or three sentences a non-technical reader would understand.
What is the overall state, and what is the one thing to fix first?

## Findings
For each, in this order:
- What I did, and what happened
- Why it matters, in terms of consequence rather than severity
- What I recommend
- **Whether the monitoring noticed**

## Detection coverage
The table from this lesson.

## What I could not test
Be explicit. Untested is not the same as secure, and an assessment
that does not say what it skipped is misleading.
```

**That last section is the mark of a professional report** and the one
juniors leave out. An assessment with no stated limitations reads as
"everything else is fine", which is a claim you cannot support.

## What you take from this

A coverage table built from attacks you actually ran, three concrete
improvements rather than a vague intention to do better, and an honest look at
what your own noise-reduction decision cost you.

That table is the most valuable artefact this course produces, and it is the
thing to talk about in an interview.

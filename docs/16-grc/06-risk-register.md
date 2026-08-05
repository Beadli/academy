---
title: "16.6 The risk register"
sidebar_position: 6
---

# 16.6 The risk register

Lesson 13.8 made this promise twice. It had you write one risk acceptance in
a five-part format and said "it is the document Module 16 asks you to produce
at scale", and its GRC admonition said plainly:

> What you just wrote is a **risk acceptance**, and in a company it lives in
> a **risk register** with the others. Module 16 builds one.

Here it is.

## What a risk register is, and what it is not

A **risk register** is the list of things that could go wrong, what you have
decided about each one, and who decided.

**It is not a list of vulnerabilities.** That is what
`lab-vulnerabilities.md` is for, and lesson 13.3 showed you what happens when
you treat a scanner's output as a work queue.

**The difference is that a risk is a statement about consequences.**
"CVE-2023-4911 is present on UBNT01" is a finding. "An attacker with local
access to UBNT01 could escalate to root and reach the monitoring data and the
backup source" is a risk. The first is a fact; the second is something a
person can make a decision about.

**Write risks as: something happens, therefore something bad results.** If
your risk statement has no "therefore", it is a finding wearing a risk's
clothes.

## The four responses, and there are only four

Every risk gets exactly one of these. Knowing there are only four makes the
decision tractable.

| Response | Meaning | Example from your lab |
|---|---|---|
| **Mitigate** | Reduce likelihood or impact | Patching, from lesson 13.7 |
| **Accept** | Live with it, deliberately, in writing | Lesson 13.8's acceptance |
| **Transfer** | Somebody else carries it | Insurance, or a cloud provider's responsibility |
| **Avoid** | Stop doing the risky thing | Removing DVWA in lesson 14.3 |

**Avoid is underused.** The DVWA removal is a genuine example: rather than
securing a deliberately vulnerable application, you deleted it. When a risk
comes from an activity that is not essential, stopping is often cheaper than
any control.

**Transfer is frequently misunderstood.** Buying cyber insurance transfers
some *financial* consequence. It does not transfer the outage, the data loss,
or the reputational damage, and it never transfers accountability. Saying "we
transferred that risk to the cloud provider" without reading the shared
responsibility model is how organisations discover they own something they
thought they did not.

## Scoring, and the honest limits of it

Most registers score risk as likelihood times impact, on a scale of one to
five each, giving one to twenty-five.

**Use it, and understand what it is.** These numbers are not measurements.
Nobody knows the true probability of a domain controller compromise in your
lab next year. What the scoring does is force a comparison: it makes you say
that this risk is worse than that one, and it makes the ordering visible so
somebody can disagree with it.

**The number is a conversation starter, not an answer**, and treating it as
precise is a well-known failure mode in this field. If two risks score 12 and
you would obviously fix one first, fix that one and adjust your reasoning
rather than deferring to the arithmetic.

## Build it

Create `Projects/gss1-risk-register.md`. Populate it from what you already
know: the assessment gaps from lesson 16.5, the accepted risks from 13.8, the
detection gaps from 14.9, and the boundary exclusions from 16.1.

```markdown
# GSS-1: risk register

**Owner:** [you]  **Last reviewed:** [today]
**Review cycle:** quarterly

Scoring: likelihood 1-5 x impact 1-5. Numbers are for ordering,
not prediction.

---

## R-01: hypervisor host is outside the system boundary
**Risk:** the laptop hosting every VM is a personal general-purpose
machine, not managed as part of GSS-1. If it is compromised or
fails, every component of GSS-1 is compromised or lost with it,
regardless of any control inside the boundary.

**Likelihood:** 3  **Impact:** 5  **Score:** 15
**Response:** ACCEPT, with mitigation
**Mitigation:** backups are on separate media (lesson 15.2), so a
host failure loses availability but not data. Full disk encryption
on the host.
**Residual:** a compromised host still yields everything.
**Decided by:** [you], [date]  **Review:** [date + 3 months]

---

## R-02: KALI01 is a documented blind spot in monitoring
**Risk:** the tuning exception written in lesson 12.6 suppresses
alerts from 10.10.10.50. An attacker who compromises KALI01 can
operate from a host that generates reduced alerting, and lesson
14.9 showed this affected the visibility of most of the Module 14
assessment.

**Likelihood:** 2  **Impact:** 4  **Score:** 8
**Response:** ACCEPT, deliberately
**Justification:** an authorised testing host generating constant
alerts causes alert fatigue, which is a larger risk to AU-6 than
this one. The exception is narrow (one source address), commented,
and in version control.
**Mitigation:** KALI01 is powered off when not in use.
**Residual:** accepted.
**Decided by:** [you], [date]  **Review:** [date + 3 months]

---

## R-03: FW01 configuration is not under version control
**Risk:** firewall rule changes are recorded only by manual change-log
entries. A rule added and forgotten (as happened with port 8081 in
lesson 14.3) may persist unnoticed, widening the attack surface
without any record.

**Likelihood:** 4  **Impact:** 3  **Score:** 12
**Response:** MITIGATE
**Plan:** export the OPNsense configuration to Git on a schedule.
**Tracked as:** POA&M-02
**Decided by:** [you], [date]

---

## R-04: single administrator
**Risk:** one person holds all knowledge and all access. Absence,
illness, or loss of credentials means nobody can operate or recover
GSS-1.

**Likelihood:** 2  **Impact:** 4  **Score:** 8
**Response:** ACCEPT
**Justification:** GSS-1 is a personal learning system. Nobody
depends on its availability, per the Low availability rating.
**Mitigation:** runbooks (lesson 15.7) exist so procedures are
documented rather than remembered. Credentials in a password
manager with recovery configured.
**Decided by:** [you], [date]  **Review:** [date + 6 months]
```

**Add the accepted risk you wrote in lesson 13.8**, reformatted to match.
That is the promise being kept literally: one acceptance became a register.

## What makes a register credible

Three properties, and they are what an assessor checks first:

**Every entry has a named decider.** Risk acceptance is a decision somebody
makes, not a state a document is in. On a real system this must be somebody
with the authority to carry the consequence. In your lab it is you, and
writing your own name teaches the shape.

**Every entry has a review date.** Lesson 13.8 called this the point people
skip and the one auditors ask about first. Circumstances change; an
acceptance made on last year's information is not an acceptance, it is a
lapse.

**The register is reviewed as a whole, on a cycle.** Individual review dates
catch individual staleness. A quarterly read-through catches the risks nobody
wrote down because they emerged gradually.

## The register is not the goal

Worth saying plainly, because this is the failure mode of the whole
discipline.

**A risk register that is written once and never opened is a compliance
artefact, not a management tool.** The value is in the recurring conversation
it forces: are these still the risks, are these still the right decisions,
has anything we accepted become unacceptable.

**The test:** if something goes wrong in your lab next month, will you open
this file? If the honest answer is no, the register is decoration and the
problem is not the format.

## What you take from this

A risk register built from your own findings, with four possible responses
used deliberately, scores you understand the limits of, and every entry
carrying a decider and a review date.

Next lesson turns the mitigate decisions into a plan with dates on it.

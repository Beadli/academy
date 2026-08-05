---
title: "17.7 Write the incident report"
sidebar_position: 7
---

# 17.7 Write the incident report

The investigation is over. The report is the deliverable, and it is the part
of incident response that most affects whether anything changes afterwards.

Lesson 12.6 made you write a triage note and said "the write-up is the job as
much as the triage". This is that, at full size.

## Who reads it, and why that changes the shape

An incident report has at least three audiences, and they want different
things from the same document:

- **Somebody senior** who needs to know what happened and whether it is over.
  They read the first paragraph and possibly nothing else.
- **An engineer** who has to implement the recommendations. They read the
  timeline and the actions.
- **Future you, or your replacement**, six months from now, when something
  similar happens. They read all of it and curse any ambiguity.

**Hence the structure: summary first, detail after.** Not chronological order
of your investigation, which is how the story felt, but importance order,
which is how it is read.

**Write the summary last and put it first.** Everybody knows this and few
people do it.

## The report

Create `Projects/incident-2026-01-report.md`. Your working note stays as it
is; this is the clean version built from it.

```markdown
# Incident report 2026-01

**Classification:** Internal
**Status:** Closed
**Incident window:** 2026-08-05 15:43 to 15:46 (activity),
detected 15:55, contained 16:18, eradicated 16:32
**Systems affected:** UBNT01 (10.10.10.20)
**Author:** [you]  **Date:** [today]

## Summary

Between 15:43 and 15:46 on 5 August 2026, an unauthorised local
account was created on UBNT01 and given persistent access and
full administrative privileges. Persistence was established via
an SSH key and a scheduled task that contacted an external host
every five minutes.

The activity was contained within 35 minutes of detection and
fully eradicated. No evidence was found of access to other lab
systems, and no data is believed to have been exfiltrated.

**Initial access was not established.** The earliest observed
activity was already privileged, which means the entry point is
outside the evidence available.

**Most significant finding:** three of the five actions produced
no alert in the monitoring platform. This is a detection gap,
not a containment failure, and it is the reason the activity ran
for 12 minutes before being noticed.

## What happened

[The timeline table from lesson 17.4, with the evidence column.]

## Impact assessment

**Confidentiality:** UBNT01 holds the Gitea repositories, the
monitoring data and the backup password. An attacker with root
had access to all of it. No evidence of data being read or
copied was found, but **absence of evidence here is weak**,
because the logging that would show it is not in place.

**Integrity:** four configuration changes, all enumerated and
reversed. No binaries or application data were altered, verified
by comparing against the pre-incident baseline.

**Availability:** none. Services remained running throughout.

## Response actions

[The Actions taken table from 17.5 and 17.6.]

## What worked

- The pre-incident baseline made "is this new?" answerable in
  seconds rather than by judgement.
- Evidence was preserved before any change, and hashes confirm
  it is unchanged.
- Backups and configuration in Git meant rebuild was a real
  option rather than a threat.

## What did not work

- Three of five actions produced no alert. Specifically: SSH key
  addition, cron job creation, and the outbound beacon.
- File integrity monitoring is not configured for /etc/cron.d,
  /etc/sudoers.d or home directories.
- No detection exists for regular outbound connections to a
  consistent destination.
- The alert queue is not reviewed on a schedule, so detection
  depended on somebody happening to look.

## Recommendations

| # | Recommendation | Why | Priority |
|---|---|---|---|
| 1 | Enable file integrity monitoring on /etc/cron.d, /etc/sudoers.d and authorized_keys files | Would have detected three of five actions | High |
| 2 | Alert on local account creation and on sudoers changes | Cheap, low false positive rate | High |
| 3 | Define and follow a weekly alert queue review | Detection currently depends on chance | Medium |
| 4 | Investigate outbound beaconing detection | Hard problem; characterise before committing | Low |

## Unknowns and limitations

- Initial access vector not established.
- Whether data was read cannot be determined from available
  logging.
- Investigation was performed by the system owner, who is not
  independent.
```

## The three sections that make it credible

**"What did not work."** A report without one is a report nobody believes.
You are describing your own environment's failures, which feels bad and reads
as competence. Lesson 16.5 made the same argument about assessment grades.

**"Unknowns and limitations."** Lesson 14.9 required this in the penetration
test report and lesson 16.8 in the SSP. Third time, same reason: **a document
with no stated limits implicitly claims certainty it does not have.**

**Recommendations with a priority.** A list where everything is important is
a list nobody can act on. Note that recommendation 4 is honestly rated Low
despite being about the scariest-sounding finding, because lesson 14.4
established that this class of detection is hard and characterising it first
is the responsible order.

## Close the loop into Module 16

**Your recommendations are POA&M items.** Open `Projects/gss1-poam.md` from
lesson 16.7 and add them, with owners and dates.

**And check whether any of them are already there.** POA&M-03 was about
container log collection; POA&M-06 was about reviewing the alert queue on a
schedule. If recommendation 3 duplicates POA&M-06, **do not add a second
entry.** Update the existing one with a note that an incident has now
demonstrated the consequence.

**That is what a POA&M is for**, and this is the moment it stops being
paperwork: an item you wrote down as a theoretical gap has just cost you
twelve minutes of undetected intrusion in your own lab. Lesson 16.7 described
the loop; you have now run one full turn of it.

Also update the risk register. **A risk that has materialised is no longer a
theoretical risk**, and its likelihood rating should reflect that.

## The lessons-learned conversation

In a real organisation the report triggers a meeting. It has a name people
use carefully: a **blameless post-mortem**.

**Blameless does not mean nobody made a mistake.** It means the question is
what let the mistake become an incident, rather than who to punish. The
practical argument: teams that punish people for mistakes get told about
fewer mistakes, which makes them less safe rather than more.

You are one person, so run it as five minutes of writing:

- **What surprised me?**
- **What took longest, and why?**
- **What did I want to know and could not find out?**
- **What would I do differently?**
- **What one change would have made the most difference?**

**That last question is the one that produces action.** For most people
running this capstone the answer is file integrity monitoring, and it is one
configuration change.

## What you take from this

A report structured for the people who read it, with failures and limitations
stated plainly, recommendations that are prioritised honestly, and the whole
thing wired back into the POA&M and risk register from Module 16.

Next lesson turns all of this into something you can show an employer.

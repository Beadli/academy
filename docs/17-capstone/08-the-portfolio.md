---
title: "17.8 The portfolio, and how to publish it safely"
sidebar_position: 8
---

# 17.8 The portfolio, and how to publish it safely

Lesson 0.5 made a promise on your first evening, before you had built
anything:

> by the capstone, this journal becomes a portfolio, a written record of
> everything you built and every problem you solved, in your own words, and
> it interviews better than any certificate.

Time to collect on it.

## What you actually have

Go and look, rather than taking my word for it. Lesson 1.2 told you to put
module numbers in your daily notes' properties specifically so that "in
Module 17 you can pull up every note from the week you built the domain".
Use it: filter your journal by module and read a week you have forgotten.

The inventory:

| Artefact | From | What it demonstrates |
|---|---|---|
| The lab itself | 3 to 11 | You can build enterprise infrastructure |
| `lab-network.md` and the addressing plan | 4 | Design before implementation |
| Detection rules, in Git | 12 | You can write and tune detections |
| Detection coverage table | 14 | You measure your own blind spots |
| Penetration test report | 14 | You can test and report on it |
| Vulnerability triage: 772 findings to 4 | 13 | You can prioritise under noise |
| Restore drill with checksums | 15 | You can prove recovery, not claim it |
| Runbooks | 15 | Somebody else could operate what you built |
| **GSS-1 authorisation package** | 16 | Full assessment lifecycle |
| **Incident report 2026-01** | 17 | You can respond and write it up |
| ~17 permanent notes and months of daily notes | all | You work like an engineer |

**Almost nobody applying for a junior role has any of this**, and the two in
bold are the ones that are genuinely unusual.

## The problem with showing it

Lesson 16.9 raised this and called sanitisation "itself a professional
skill":

> Your SSP describes, in one place, every control protecting your lab and
> every place it is weak.

Your incident report is worse. It is a working description of how to
establish persistence on a Linux host, next to a list of what your monitoring
does not catch.

**Three bad options and one good one:**

- **Publish it as-is.** You are handing a map to anyone who finds it, and
  demonstrating poor judgement to the employer you were trying to impress.
- **Show nothing.** Wastes the work.
- **Say "I have a lab" without evidence.** So does everybody.
- **Publish a sanitised version.** Same reasoning, same structure, specifics
  removed.

**The fourth option is what professionals do**, because it is what
consultants must do with client work and what everybody does when writing
publicly about real incidents.

## How to sanitise properly

Sanitising is not find-and-replace. **The test: could a reader use this
document to attack the real system, or identify it?**

**Remove or generalise:**

- Real addresses. `10.10.10.20` becomes "the application server". Your
  addresses are private ranges, so this is more habit than necessity, but the
  habit is the point.
- Real hostnames and domains, if they identify you.
- Anything that maps a specific current weakness to a specific reachable
  system. **This is the one that matters.** "Our monitoring does not detect
  X on the server at Y" is an invitation.
- Usernames, key comments, anything personally identifying.

**Keep, because it is the whole value:**

- The reasoning. Why you chose containment over observation.
- The methodology. The order you investigated in.
- The honest failures. "Three of five actions produced no alert" is the most
  credible sentence in the document.
- The numbers, where they demonstrate judgement: 772 findings to 4.

**A sanitised report should still be recognisably the same piece of thinking.
If sanitising removed the interesting parts, you removed the wrong things.**

## Do it

Create a **separate public repository**, distinct from your private journal.
Do not sanitise in place; you will need the real one.

```bash
mkdir -p ~/git/lab-portfolio && cd ~/git/lab-portfolio
git init -b main
```

Copy in sanitised versions of three documents, which is enough:

1. **The incident report** from 17.7
2. **A summary of the GSS-1 assessment** from Module 16, not the full SSP
3. **The Module 13 triage write-up**, which is short and demonstrates
   judgement quickly

Add a `README.md` that frames it:

```markdown
# Lab portfolio

A home lab built from nothing: Active Directory, PKI, single
sign-on, containers, automation and a monitoring stack, then
assessed, attacked and operated.

These documents are sanitised. Addresses, hostnames and
specific current weaknesses have been removed or generalised;
the reasoning and methodology are unchanged.

## Contents
- `incident-report.md`: investigation of a simulated intrusion,
  timeline, containment decisions, and an honest account of
  what the monitoring missed
- `assessment-summary.md`: control assessment of the
  environment against a subset of NIST 800-53, with findings
- `vulnerability-triage.md`: reducing 772 scanner findings to
  the 4 that were actively exploited, and why severity was the
  wrong sort order

## What this is not
A production environment, or an independent assessment. It is a
learning system assessed by the person who built it, and both
documents say so.
```

**That "What this is not" section is doing real work.** It pre-empts the
obvious objection, demonstrates you know the difference between a lab and
production, and is the kind of honesty that makes the rest believable.

**How you know it worked:**

```bash
# Nothing sensitive survived. Substitute your own real values.
grep -rn "10\.10\.10\." . || echo "no lab addresses"
grep -rni "lab.internal" . || echo "no internal domain"
grep -rn "restic\|password" . || echo "no credential references"
```

**Read the output rather than trusting the greps.** They catch the obvious
cases; a screenshot with an address in it, or a hostname in a code comment,
they will not.

Then push it, and put the link on your CV.

## Talking about it

Two questions you will be asked, and what makes a good answer.

**"Tell me about your lab."** The weak answer lists technologies. The strong
answer is a story with a decision in it: *"I built a domain, then attacked it
and found my monitoring missed three of five techniques. The interesting part
was working out which gaps were collection problems and which were rule
problems, because they need different fixes."*

**"What went wrong?"** The best question they ask, and candidates waste it by
minimising. You have real material: the `master`/`main` mismatch, the backup
that would have restored nothing, a detection gap you found by attacking
yourself.

**Answer with the diagnosis, not the mistake.** "I assumed my backups worked
until I actually restored one and compared checksums" is a much better answer
than any success story, because it shows you know the difference between
believing and verifying.

## What you take from this

A public, sanitised portfolio of three documents that demonstrate judgement
rather than tool familiarity, a repository you can link to, and two answers
prepared for the questions that decide interviews.

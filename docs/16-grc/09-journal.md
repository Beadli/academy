---
title: "16.9 Journal: what you can prove"
sidebar_position: 9
---

# 16.9 Journal: what you can prove

This module's permanent notes *are* the deliverables, so the journal work here
is different: rather than writing a new note, you are making sure the nine
you just produced hang together and can be found.

**Check your `Projects/` folder contains all of these:**

- `gss1-boundary.md` (16.1)
- `gss1-categorisation.md` (16.2)
- `gss1-control-selection.md` (16.3)
- `gss1-evidence.md` (16.4)
- `gss1-assessment.md` (16.5)
- `gss1-risk-register.md` (16.6)
- `gss1-poam.md` (16.7)
- `gss1-ssp.md` and `gss1-authorisation.md` (16.8)

**Then do the thing that makes them a package rather than nine files.** Create
`Projects/gss1.md` as the front door:

```markdown
# GSS-1: authorisation package

**Status:** authorised [date], expires [date + 12 months]
**Categorisation:** Moderate

Read in this order:
1. [[gss1-ssp]]: the main document
2. [[gss1-poam]]: what is outstanding
3. [[gss1-risk-register]]: what was accepted and by whom

Supporting:
- [[gss1-boundary]], [[gss1-categorisation]],
  [[gss1-control-selection]], [[gss1-evidence]],
  [[gss1-assessment]], [[gss1-authorisation]]

Underlying evidence lives in the lab notes: [[lab-network]],
[[lab-domain]], [[lab-detection]], [[lab-vulnerabilities]],
[[lab-attacks]], [[lab-operations]], [[lab-changes]].
```

**"Read in this order" is doing real work.** An assessor handed nine files
reads them in whatever order they happen to open, and forms an impression
from whichever one that was. A front door with a reading order is the
difference between a package and a pile.

## Then today's daily note

Under **what I did**: the assessment, and your headline number. "Fifteen
controls assessed: four Implemented, nine Partial, two Not Implemented" is a
sentence worth having in your own words.

Under **what broke**: this module breaks differently from every other one,
because nothing technical fails. What breaks is your account of your own
system. Write down the moment you had to grade something lower than you
wanted to, and what the evidence was that forced it.

Under **what I learned**: pick one.

- Why an empty POA&M is a warning sign rather than an achievement
- The difference between evidence of design, implementation and operation,
  and why the third is rare
- Why a risk statement needs a "therefore"
- Why authorisation expires on purpose

Under **open questions**: the good ones here are about the honesty of the
exercise. Which control did you most want to grade higher than the evidence
supported? Which piece of evidence would not survive somebody asking a
follow-up question? If a stranger assessed GSS-1 next week, what would they
find that you did not?

## The exercise worth doing before you close

Answer this in writing, and be uncomfortable about it:

**Which of your Implemented grades would survive an assessor who wanted to
fail you?**

Go back through the fifteen. For each one graded Implemented, imagine
somebody asking one more question: *how do you know that is still true this
week?* Several will not survive it, and those should be Partial.

**This is the single most valuable habit in GRC**, and it is not a technique.
It is a willingness to argue against your own document, which is rare enough
that people who do it get trusted with bigger things.

## Close the loop

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 16 complete, GSS-1 authorisation package"
git push
```

Tick Module 16 in `Projects/lab-progress.md`.

:::warning[What this package contains]
Your SSP describes, in one place, every control protecting your lab and every
place it is weak. The POA&M is a list of your known gaps with dates by which
they are still open.

**That is an extremely useful document for somebody attacking you**, which is
worth noticing given what Module 14 taught you. Keep the journal repository
private, as lesson 1.4 set it up to be.

If you want to show this work to an employer, and you should, **write a
sanitised version**: same structure, same reasoning, real addresses and
specific weaknesses removed. That sanitisation is itself a professional
skill, and doing it deliberately is a better answer than either publishing
the real thing or having nothing to show.
:::

## What this is worth outside the lab

Worth being direct about, because it is the reason this module exists.

Almost everybody applying for a junior GRC role has assessed a case study.
You have an SSP, a POA&M, a risk register and an authorisation memo for a
real system, and **you can answer follow-up questions about every control**,
because you built the thing each one describes.

The interview question that separates candidates is not "what is a POA&M". It
is "tell me about a control you assessed as partially implemented and why."
You have fifteen of those, with evidence, and the reasoning is yours.

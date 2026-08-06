---
title: "16.8 The SSP and the authorisation memo"
sidebar_position: 8
---

# 16.8 The SSP and the authorisation memo

Two documents left. One describes the system; the other is somebody putting
their name to it.

## The System Security Plan

The **SSP** is the main document. It says what the system is, where its
boundary is, how it is categorised, and how each selected control is
implemented.

**Most of it is already written.** Everything from lessons 16.1 to 16.5 is a
section of the SSP; this lesson assembles them and adds the parts that only
make sense once the rest exists.

The reason it is one document rather than seven is that an SSP is read by
somebody who does not know your system. They need the boundary before the
controls, the categorisation before the control selection, and the assessment
after all of it. **The order is an argument**, and the document is
persuasive in the same way a well-taught lesson is.

Create `Projects/gss1-ssp.md`:

```markdown
# System Security Plan: GSS-1

**System name:** GSS-1, Beadli Lab General Support System
**Owner:** [you]
**Version:** 1.0  **Date:** [today]
**Categorisation:** Moderate (integrity-driven)

## 1. System description
What GSS-1 is and what it is for, in a paragraph a
non-technical reader could follow. Include that it is a
learning environment, because purpose drives the
categorisation.

## 2. System boundary
[from gss1-boundary.md: components, network, external
interfaces, and the explicit exclusions with justification]

## 3. Security categorisation
[from gss1-categorisation.md: the three ratings with their
reasoning, the high-water mark, the component-level table,
and the recovery objectives]

## 4. Control selection and tailoring
[from gss1-control-selection.md: the fifteen controls, the
statement that this is a deliberate subset, and the scoping-out
justifications]

## 5. Control implementation
[from gss1-assessment.md: one section per control, describing
how it is implemented and citing evidence]

## 6. Assessment results
Summary of grades: N Implemented, N Partially Implemented,
N Not Implemented. Method and date.

## 7. Known limitations of this assessment
- Only 15 of the Moderate baseline controls were assessed.
- The assessment was performed by the system owner, not an
  independent assessor. Self-assessment is inherently weaker.
- The hosting hypervisor is excluded from the boundary and
  is not assessed, though GSS-1 fully depends on it.
- [any evidence you reconstructed after the fact rather than
  recording contemporaneously]

## 8. Risks and outstanding actions
Reference to gss1-risk-register.md and gss1-poam.md rather
than duplicating them, so there is one authoritative copy of
each.

## 9. Supporting evidence
Reference to gss1-evidence.md.
```

**Section 7 is the one that makes this document professional.** Lesson 14.9
said the same about penetration test reports: an assessment with no stated
limitations reads as "everything else is fine", which is a claim you cannot
support.

**Naming self-assessment as a limitation is not false modesty.** It is a
genuine methodological weakness, every framework treats independent
assessment as stronger, and stating it costs you nothing while demonstrating
that you know the difference.

## Reference, do not duplicate

Notice that sections 8 and 9 point at other files instead of copying them.

**This is a real operational decision, not formatting.** A POA&M copied into
an SSP is a POA&M that will diverge from the real one within a month, and
then you have two documents disagreeing and no way to know which is current.

The general rule: **one authoritative copy of each fact, referenced from
everywhere else.** You have been applying it since lesson 6.9 noticed that
Gitea stores the owner's name once and refers to it by ID.

## The authorisation memo

The last document, and the shortest. Somebody with authority reads the SSP,
the risk register and the POA&M, and decides: **may this system operate,
given what we now know is wrong with it?**

In US federal practice this produces an **Authority to Operate**, and the
person signing is an **Authorising Official**. The vocabulary is specific to
that context; the act is universal. Somebody accepts the residual risk.

Create `Projects/gss1-authorisation.md`:

```markdown
# Authorisation to operate: GSS-1

**System:** GSS-1, Beadli Lab General Support System
**Categorisation:** Moderate
**Authorising official:** [your name], system owner
**Date:** [today]
**Authorisation period:** 12 months, or until a significant
change to the system, whichever comes first.

## Basis for this decision
I have reviewed:
- The System Security Plan, version 1.0
- The control assessment dated [date], covering 15 controls
- The risk register, [N] entries
- The POA&M, [N] open items

## Findings summary
[N] controls Implemented, [N] Partially Implemented,
[N] Not Implemented. The most significant outstanding
weaknesses are:
1. [your top item]
2. [second]
3. [third]

## Decision
GSS-1 is **authorised to operate** for 12 months, subject to:
- The POA&M items being worked to their stated dates
- A restore test being performed and logged monthly
- Re-authorisation if the system boundary changes materially

## Residual risk accepted
I accept the risks recorded in gss1-risk-register.md as
R-01, R-02 and R-04, on the justifications recorded there.

The most significant is R-01: GSS-1 depends entirely on a
hosting platform outside its own boundary. This is accepted
because GSS-1 is a learning system with a Low availability
rating and no external dependants.

**Signed:** [your name]
**Role:** system owner and authorising official
```

## What the memo is actually for

It looks like a formality. It does two real things, and the second is the
important one.

**It creates a decision point.** Without it, systems drift into production
because nobody said no. Requiring somebody to write down "yes, given these
known problems" forces the known problems to be assembled and read.

**It puts a name on the residual risk.** This is why authorising officials
are senior: the person accepting the risk should be the person who carries
the consequence. **An engineer accepting risk on behalf of an organisation is
a structural failure**, and one you should recognise if it happens to you.
When somebody asks you to sign off on a risk you do not own, the correct
response is to escalate it to whoever does, in writing.

In your lab you are both, which is tidy and is also why the exercise cannot
teach you that tension. Knowing it exists is the transferable part.

## And the expiry date

**Authorisation expires.** Twelve months, or on significant change.

That is what stops an assessment from being a one-off event, and it is the
same mechanism as review dates on risk acceptances and due dates on POA&M
items. **The whole discipline is built out of things that expire on
purpose**, because the alternative is a document describing a system that
stopped existing two years ago.

## Two worked examples, in the formats the industry actually uses

Everything you have written this module is Markdown, because that is what
your vault is and because it keeps the reasoning in version control.

**Real GRC work is not in Markdown.** An SSP is a Word document and a POA&M
is an Excel workbook, in almost every organisation you will meet. You will be
handed a template on your first day, and the structure will be imposed on you
rather than chosen.

So here are both, fully worked for GSS-1:

- **[GSS-1 System Security Plan (.docx)](/templates/GSS-1-SSP.docx)**, about
  25 pages: every section from this module, with each of the fifteen controls
  written up individually.
- **[GSS-1 Plan of Action and Milestones (.xlsx)](/templates/GSS-1-POAM.xlsx)**,
  five worksheets: the POA&M itself, the risk register with computed scores,
  an empty Closed Items sheet, control status with a chart, and maintenance
  instructions.

**Use them as a comparison, not a substitute.** Write yours first, then open
these and see what a longer treatment of the same system looks like. The
things worth stealing are structural: how each control section separates the
requirement from the implementation from the evidence from the conclusion,
and how the limitations section is worded.

**They describe the same GSS-1 you have been assessing**, with the same
categorisation, the same fifteen controls and the same honest grade split of
seven Implemented and eight Partially Implemented. If your own assessment came
out very differently, that is worth understanding rather than correcting; your
lab is not identical to the one described.

:::note[A tension worth noticing]
These are binary files. Git cannot diff them, cannot merge them, and cannot
tell you what changed between two versions.

That is a real cost, and it is the same problem lesson 15.8 identified: the
things hardest to track are the things changed by clicking. Real GRC documents
live in SharePoint and get emailed around as attachments, which is exactly why
"which version is current" is a chronic problem in that job.

**Keep your Markdown originals.** The Word and Excel versions are what you
hand to somebody; the text ones are what you actually maintain.
:::

## What you take from this

An SSP that assembles five lessons of work into one argument, a limitations
section that strengthens rather than weakens it, and a signed authorisation
with an expiry date and explicitly accepted residual risk.

You have now produced the three documents a GRC role is interviewed on, about
a system you built with your own hands.

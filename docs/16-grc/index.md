---
title: "Module 16: GRC, assess your own system"
sidebar_position: 0
---

# Module 16: GRC, assess your own system

Governance, risk and compliance has a reputation for being paperwork
disconnected from reality, and lesson 0.2 was blunt about where that
reputation comes from:

> The role has a reputation for paperwork, and the reputation is earned
> exactly when the analyst has never touched the systems they're assessing.
> You won't have that problem: in Module 16 you'll formally assess the lab
> you built with your own hands.

That is the whole premise of this module. Most GRC training has students
assess an imaginary company from a case study, which teaches the format and
none of the judgement. You are going to assess a real system, because you
built it, broke it, monitored it and recovered it, and you can answer follow-up
questions about every control in it.

## What you are actually going to do

You will take your lab through an **authorisation lifecycle**, which is the
process an organisation uses to decide whether a system is fit to operate:

1. **Define the system**, including where its boundary is
2. **Categorise it** by the harm its failure would cause
3. **Select** a set of controls appropriate to that categorisation
4. **Assess** what is genuinely implemented, with evidence
5. **Record the gaps** honestly, with owners and dates
6. **Document and authorise it**, in writing

Your lab gets a name for this: **GSS-1**. In US federal terminology a
**General Support System** is an interconnected set of information resources
under the same direct management control, which is exactly what you have.

What's in it:

- **16.1** what GRC is, and why your lab is a system
- **16.2** categorise it: how much would it hurt
- **16.3** select and scope your controls
- **16.4** you already have the evidence
- **16.5** assess it honestly
- **16.6** the risk register
- **16.7** the POA&M
- **16.8** the system security plan and the authorisation memo
- **16.9** journal entry
- **16.10** checkpoint

## What you need

**Nothing new, and no particular tier.** This module installs no software and
attacks nothing. What it needs is your journal, and specifically the
permanent notes you have been writing since Module 1.

If you have skipped the journal entries, this is the module where that
becomes expensive. **Go back and reconstruct what you can before starting
16.4**, because that lesson inventories your evidence and an empty inventory
makes the rest of the module hypothetical.

If you did keep them, you are about to find out why every module ended that
way.

## A word on which framework

This module uses **NIST 800-53** controls and the US federal authorisation
process, for three reasons: it is free to read, it is extremely detailed, and
its vocabulary (SSP, POA&M, control families) turns up in job descriptions
worldwide.

**It is not the only option, and the skill transfers.** ISO 27001 is the
international standard and more common outside the US. The CIS Critical
Security Controls are shorter and more prescriptive, and a better first
framework for a small organisation. SOC 2 is what a customer asks a SaaS
vendor for.

**They differ in vocabulary and emphasis, not in the underlying question**,
which is always: what could go wrong, what have you done about it, and can
you show me?

:::warning[Control identifiers change between revisions]
The control numbers in this module (SC-7, AC-8, RA-5 and so on) come from
NIST 800-53, and **some were renumbered or renamed between Revision 4 and
Revision 5.**

Treat the identifiers here as teaching examples rather than a citation. When
you do this for real, read the control text in the current revision of the
publication itself rather than trusting any secondary source, including this
one. Getting a control ID slightly wrong in a real assessment is the kind of
error that undermines everything else in the document.

The *reasoning* in this module does not depend on the numbers being current.
The habit of checking them does.
:::

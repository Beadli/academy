---
title: "16.3 Select and scope your controls"
sidebar_position: 3
---

# 16.3 Select and scope your controls

You have a Moderate system. Now you choose what you are going to be assessed
against.

## Control families, and why the numbers look like that

NIST 800-53 organises controls into **families**, each with a two-letter
prefix. You have already met eight of them in passing, because the GRC
admonitions throughout this course have been naming them as you went.

The families that matter for GSS-1:

| Family | What it covers | Where you built it |
|---|---|---|
| **AC** Access Control | Who can do what | Modules 5, 6, 8 |
| **AU** Audit and Accountability | Logging and reviewing it | Module 12 |
| **CA** Assessment, Authorisation and Monitoring | This module, and Module 14 |
| **CM** Configuration Management | Knowing and controlling what changed | Modules 10, 15 |
| **CP** Contingency Planning | Backup and recovery | Module 15 |
| **IA** Identification and Authentication | Proving who you are | Modules 5, 7, 8, 9 |
| **IR** Incident Response | What you do when it happens | Module 12 |
| **RA** Risk Assessment | Knowing what is wrong | Module 13 |
| **SC** System and Communications Protection | Boundaries and cryptography | Modules 4, 6, 7 |
| **SI** System and Information Integrity | Patching, monitoring, detection | Modules 12, 13, 15 |

**That table is worth pausing on.** Every family maps onto work you actually
did. GRC feels abstract when you have not built the thing; you have, so this
is a re-description of your own lab rather than new material.

## Baselines and tailoring

A **baseline** is the starting set of controls for a given categorisation.
Low gets fewer, Moderate more, High most. You do not choose controls
individually from scratch; you start from the baseline and adjust.

That adjustment is called **tailoring**, and it goes both ways:

**Scoping out.** A control that genuinely does not apply. GSS-1 has no
physical data centre, so most of the **PE** (Physical and Environmental)
family does not apply in the form written.

**Compensating controls.** You cannot do the control as written, so you do
something else achieving the same objective. This is legitimate and it must
be *argued*, not asserted.

**Adding.** Something the baseline does not require but your risk assessment
says you need.

:::warning[The scoping-out trap]
"Not applicable" is the most abused phrase in self-assessment, because it
removes work and looks like an answer.

**The test: could you defend it to somebody who wants the control
implemented?** "We have no physical facility, the system runs as virtual
machines on a laptop, and physical security of that laptop is addressed as
an excluded dependency in the boundary document" is a defence.

"N/A, small system" is not a defence. It is a gap wearing a disguise, and an
assessor reading a document full of those will stop believing the parts that
say Implemented.
:::

## Scope it down to something you can actually finish

The full Moderate baseline is hundreds of controls. **Assessing all of them
would teach you nothing that the first fifteen do not**, and you would not
finish.

So do what real assessments do under time pressure, and do it explicitly:
pick a subset, state that it is a subset, and say how you chose.

**Choose fifteen controls**, weighted toward what your lab actually
demonstrates. Create `Projects/gss1-control-selection.md`:

```markdown
# GSS-1: selected controls

## Scope of this assessment
This is a DELIBERATE SUBSET of the NIST 800-53 Moderate baseline,
not the full baseline. Fifteen controls were selected to cover
each major family represented in the system, weighted toward
controls with technical evidence available.

Assessing the full baseline is out of scope for this assessment
and is recorded as a limitation in the SSP.

## Selected controls
| ID | Control | Where it lives in GSS-1 |
|---|---|---|
| AC-2 | Account Management | Two-account model, lesson 5.6 |
| AC-8 | System Use Notification | Logon banner GPO, lesson 5.7 |
| AC-17 | Remote Access | SSH key-only, lesson 6.3 |
| AU-2 | Event Logging | Wazuh collection, lesson 12.2 |
| AU-6 | Audit Record Review | Alert triage, lessons 12.4 to 12.6 |
| CA-8 | Penetration Testing | Module 14 assessment |
| CM-3 | Configuration Change Control | Change log, lesson 15.8 |
| CP-9 | System Backup | restic, lesson 15.2 |
| CP-10 | System Recovery | Restore drill, lesson 15.3 |
| IA-2 | Identification and Authentication | Kerberos and SSO, Modules 5, 8 |
| IA-5 | Authenticator Management | Key-based auth, password policy |
| RA-5 | Vulnerability Monitoring and Scanning | Module 13 |
| SC-7 | Boundary Protection | FW01 and ufw, lessons 4.6, 6.3 |
| SC-12 | Cryptographic Key Establishment and Management | PKI, Module 7 |
| SI-2 | Flaw Remediation | Patching, lessons 13.7, 15.6 |

## Scoped out, with justification
| Family | Why |
|---|---|
| PE, Physical and Environmental | No facility. The hosting laptop is an excluded dependency per the boundary document, and carried as a risk |
| PS, Personnel Security | Single-person system. No hiring, transfer or termination processes exist to assess |
| SA, System and Services Acquisition | Nothing is procured. Supply chain risk IS in scope and appears under RA-5 and SI-2 |
```

**Verify the control IDs and titles against the current revision of the
publication before you use this anywhere real.** The index of this module
explains why: identifiers moved between revisions, and a wrong ID undermines
the credibility of correct work.

## Why this selection, specifically

Two things to notice about how that list was chosen, because the method
matters more than the list.

**Every selected control has evidence available.** You are not going to
assess a control you cannot substantiate. That is not cheating; it is what
makes an assessment finishable. Controls with no evidence available are
either gaps or out of scope, and both of those are honest answers.

**The selection covers the failure modes you found in Modules 13 and 14.**
CA-8 exists in the list because you did a penetration test. AU-6 is there
because Module 14 showed you gaps in exactly that. **A control set that
avoids the areas where you know you are weak is a control set designed to
pass**, which is the opposite of the point.

## The mapping trick that saves real time

Frameworks overlap enormously. The same firewall evidence supports SC-7 in
800-53, A.13 in ISO 27001, and CIS Control 4.

**So collect evidence once and map it to many frameworks**, rather than
running a separate assessment per framework. This is what "crosswalk" means
when you see it in a job description, and organisations that do it well
answer a customer security questionnaire in an afternoon instead of a
fortnight.

You will not build a crosswalk here, but structure your evidence in lesson
16.4 as though you might: **organised by what it proves, not by which
framework asked.**

## What you take from this

Fifteen controls selected with a stated method, an explicit note that this is
a subset, and scoping decisions you could defend to somebody who disagreed.

Next lesson you discover you already have most of the evidence.

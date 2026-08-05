---
title: "16.10 Checkpoint: a system you can account for"
sidebar_position: 10
---

# 16.10 Checkpoint: a system you can account for

This module produces documents rather than configuration, so this checkpoint
is almost entirely questions. That is appropriate: the deliverable is your
reasoning, and the test is whether you can defend it.

The only mechanical check is that the package exists and hangs together.

```bash
# On the machine holding your vault. All nine documents plus
# the front door. Expect ten files.
ls ~/git/lab-journal/Projects/gss1*.md | wc -l
ls ~/git/lab-journal/Projects/gss1*.md

# And that it is committed, not just written.
cd ~/git/lab-journal && git status --short Projects/
```

Expect the file list and **no output** from `git status`, meaning everything
is committed.

## Pass criteria

**Understanding the discipline:**

- [ ] You can define governance, risk and compliance separately, and say why
      the order matters (lesson 16.1)
- [ ] You can name the four states a control can be in, and explain why
      "installed" is not "implemented" (lesson 16.1, building on 4.6)
- [ ] You can state the three questions every assessor asks, and notice they
      are the same three this course has asked since Module 0 (lesson 16.1)
- [ ] You can name the three deliverables and say what each is for
      (lesson 16.1)

**Boundary and categorisation:**

- [ ] `gss1-boundary.md` lists what is inside, what is outside, and how you
      connect to each external thing (lesson 16.1)
- [ ] **It names at least one excluded dependency with a justification**,
      rather than silently omitting it (lesson 16.1)
- [ ] `gss1-categorisation.md` rates confidentiality, integrity and
      availability **with reasoning**, not just letters (lesson 16.2)
- [ ] You can explain the high-water mark rule and which rating drove yours
      (lesson 16.2)
- [ ] The component-level table shows that not everything in the boundary
      deserves equal protection (lesson 16.2)
- [ ] Your RPO and RTO are carried in from lesson 15.1, and **any mismatch
      with your measured restore time is recorded rather than reconciled
      away** (lesson 16.2, building on 15.3)

**Control selection:**

- [ ] Fifteen controls selected, with the selection method stated
      (lesson 16.3)
- [ ] The document says explicitly that this is a **subset**, not the full
      baseline (lesson 16.3)
- [ ] Every scoped-out family has a justification you could defend to
      somebody who wanted the control implemented (lesson 16.3)
- [ ] You can explain why the selection deliberately includes the areas
      Modules 13 and 14 showed you were weak (lesson 16.3)

**Evidence:**

- [ ] You can name the three kinds of evidence and say which is rarest and
      why it carries the most weight (lesson 16.4)
- [ ] `gss1-evidence.md` maps each control to specific evidence and its
      location (lesson 16.4)
- [ ] **Several rows are evidence of operation**, not just design and
      implementation (lesson 16.4)
- [ ] Any evidence reconstructed after the fact is labelled as such
      (lesson 16.4)

**The assessment:**

- [ ] `gss1-assessment.md` grades all fifteen with written justification
      (lesson 16.5)
- [ ] **Not everything is Implemented**, and you can say what evidence forced
      each lower grade (lesson 16.5)
- [ ] You re-ran at least one technical check during the assessment rather
      than trusting an older record, and recorded the result and date
      (lesson 16.5)
- [ ] AU-6 is graded honestly against the detection coverage table, including
      the gaps (lesson 16.5, building on 14.9)
- [ ] You can explain why a document that admits gaps is more credible than
      one that does not (lesson 16.5)

**Risk and remediation:**

- [ ] `gss1-risk-register.md` states risks as consequences, with a
      "therefore", not as findings (lesson 16.6)
- [ ] You can name the four risk responses and give an example of **avoid**
      from your own lab (lesson 16.6, building on 14.3)
- [ ] Every entry has a named decider and a review date (lesson 16.6,
      building on 13.8)
- [ ] The risk acceptance you wrote in lesson 13.8 is in the register
      (lesson 16.6)
- [ ] You can say what a risk score is and is not (lesson 16.6)
- [ ] `gss1-poam.md` has six fields per item, with **real dates and no
      "ongoing"** (lesson 16.7)
- [ ] You can explain why an empty POA&M is a warning sign (lesson 16.7)
- [ ] At least one item is honestly characterised as hard or not
      signature-detectable, rather than omitted (lesson 16.7, building on
      14.4)
- [ ] You can say why closed items are moved rather than deleted, and why
      they need evidence (lesson 16.7, building on 13.7)

**The package:**

- [ ] `gss1-ssp.md` assembles boundary, categorisation, selection,
      implementation and results in an order that argues (lesson 16.8)
- [ ] **Section 7 names the limitations**, including that this was a
      self-assessment (lesson 16.8)
- [ ] The SSP references the POA&M and register rather than duplicating them,
      and you can say why (lesson 16.8)
- [ ] `gss1-authorisation.md` names an authorising official, summarises the
      findings, accepts specific residual risks, and **expires** (lesson 16.8)
- [ ] You can explain why an engineer accepting organisational risk is a
      structural problem, and what to do if asked (lesson 16.8)
- [ ] `gss1.md` exists as a front door with a reading order (lesson 16.9)
- [ ] You worked through "which Implemented grades would survive an assessor
      who wanted to fail you", and moved any that would not (lesson 16.9)
- [ ] Journal committed and pushed, Module 16 ticked (lesson 16.9)

All green? Then you have done something almost nobody applying for these
roles has done: taken a real system through a full authorisation lifecycle,
with evidence you generated yourself over fifteen modules, and produced a
package you can defend line by line.

Module 17 is the capstone. It puts the whole thing together, and it asks you
to demonstrate the environment rather than describe it.

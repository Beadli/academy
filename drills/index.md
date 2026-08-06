---
title: "Drills"
sidebar_position: 0
---

# Drills

**Opening now, one drill at a time.** Whatever is written and tested is in
the sidebar on the left; the rest arrive as they are done.

## The problem it solves

You will finish this course with a working enterprise on your own hardware: a
domain, a certificate authority, single sign-on, containers, automation, and a
SIEM watching all of it.

And then, if nothing changes, it will sit there.

That is the most common ending for a home lab. Somebody builds one, follows a
guide to the end, and is left with an expensive, humming reminder that they
once followed a guide. **The lab was never the point. Using it is.**

Drills are the answer to "I built this, now what?" Exercises against the lab
you built, each with an objective and a way to tell whether you succeeded:
attack your own domain and check whether your detections noticed, write and
tune rules against real techniques, run automation with a defined outcome,
find things that are broken.

## What is coming

Thirteen categories, roughly 120 exercises mapped out, in rough order of how
soon:

| Category | What it covers | Live | Planned |
|---|---|---|---|
| **Integrations** | Alert routing, notification, status pages | 1 | 10 |
| **Detection** | Write and tune rules against real techniques | | 12 |
| **Offensive** | Attack your own domain, under the Module 14 rules | | 12 |
| **Defensive** | Hardening, tiering, allowlisting, LAPS | | 11 |
| **Operations** | Failure injection, restore drills, patching | | 10 |
| **PKI** | Revocation, expiry, CA compromise, rotation | | 8 |
| **Identity** | Lifecycle, access review, MFA, federation | | 8 |
| **Investigation** | Timelines, memory, correlation, false positives | | 8 |
| **GRC** | Extend the assessment, crosswalk, questionnaires | | 8 |
| **Automation** | Make a drill idempotent, compliance as code | | 7 |
| **Networking** | Segmentation, DNS failure, rogue devices | | 7 |
| **Meta** | Cold start, drift audits, explain it in one page | | 6 |
| **New services** | Deploy something new, then defend it | | 15 |

**Each drill has one objective and a way to tell whether you succeeded.** No
drill is an open-ended "explore X", because if there is no way to fail there
is no way to have passed.

Not started the course yet? [Start at Module 0](/course/intro) and build the
thing they will run against.

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

Fifteen categories, roughly 138 exercises mapped out.

Every drill is numbered by its category, so `INT-01` is the first
Integrations drill and `DEF-11` the eleventh Defensive one. Those prefixes
are how drills refer to each other, and they are how the sidebar is grouped.
Roughly in the order they will arrive:

| ID | Category | What it covers | Live | Planned |
|---|---|---|---|---|
| **INT** | Integrations | Alert routing, notification, status pages | 1 | 10 |
| **DET** | Detection | Write and tune rules against real techniques | 1 | 12 |
| **OFF** | Offensive | Attack your own domain, under the Module 14 rules | 1 | 12 |
| **DEF** | Defensive | Hardening, tiering, allowlisting, LAPS | 1 | 11 |
| **AI** | Engineering with AI | Review discipline, context drift, prompt injection against your own agent | | 8 |
| **CI** | Continuous integration | Workflows, runners, secrets, and treating your pipeline as a privileged machine | | 8 |
| **OPS** | Operations | Failure injection, restore drills, patching | 1 | 10 |
| **PKI** | Certificates | Revocation, expiry, CA compromise, rotation | 1 | 8 |
| **IAM** | Identity | Lifecycle, access review, MFA, federation | | 8 |
| **IR** | Investigation | Timelines, memory, correlation, false positives | 1 | 8 |
| **GRC** | Governance | Extend the assessment, crosswalk, questionnaires | | 8 |
| **AUTO** | Automation | Make a drill idempotent, compliance as code | | 7 |
| **NET** | Networking | Segmentation, DNS failure, rogue devices | | 7 |
| **META** | The lab itself | Cold start, drift audits, explain it in one page | | 6 |
| **APP** | New services | Deploy something new, then defend it | | 15 |

**Each drill has one objective and a way to tell whether you succeeded.** No
drill is an open-ended "explore X", because if there is no way to fail there
is no way to have passed.

## Extensions

A few drills need a machine or a service the course never builds, because
making every student build it would have cost them memory they may not have.
Those builds live under **Extensions** in the sidebar, written as proper
walkthroughs, and a drill that needs one says so at the top.

**Only build one when a drill you want needs it.** An extension with no drill
behind it is a lab growing for its own sake, which is the habit this whole
section argues against.

Not started the course yet? [Start at Module 0](/course/intro) and build the
thing they will run against.

---
title: "Drills: coming when the course is done"
sidebar_position: 0
---

# Drills

**Nothing here yet, deliberately.** This section opens when the course is
finished, and this page exists so you know it is coming rather than wondering
whether the tab is broken.

## The problem this solves

You are going to finish this course with a working enterprise on your own
hardware: a domain, a certificate authority, single sign-on, containers,
automation, a SIEM watching all of it.

And then, if nothing changes, it will sit there.

That is the most common ending for a home lab. Somebody builds one, follows a
guide to the end, and is left with an expensive, humming reminder that they
once followed a guide. **The lab was never the point. Using it is.**

Drills are the answer to "I built this, now what?"

## What a drill is, and is not

The distinction matters, so it is worth being precise.

**A module teaches you something new.** How Kerberos works. How to promote a
domain controller. What a detection rule does.

**A drill gives you a job to do** with things you already have, against the lab
you already built, with an objective and a way to tell whether you succeeded.
It teaches nothing new in the lecture sense. It makes what you learned real,
and it usually reveals which bits you had not really learned.

Modules build capability. Drills prove it, and deepen it.

## What they will look like

Structured like the course: a small number of top-level areas, each holding
individual drills. The shape being planned:

**Offensive drills against your own domain.** You built the directory, so now
attack it, and then go and look at whether your Module 12 detections noticed.
The pairing is the point: nearly every drill has a defensive half.

**Detection engineering.** Given a technique, write the rule that catches it,
tune it, and prove it fires without drowning you. This is the job the course
teaches the tools for and does not give you enough reps at.

**Automation engagements.** Real Ansible work with a defined outcome. Deploy an
agent fleet. Rebuild a machine and prove it came back correctly. Enforce a
configuration and detect the drift.

**Operations and incident practice.** Something is broken, here is the symptom,
find it. The lab is your own, so the answer is always findable, which is what
makes it a fair exercise.

Each will state what it needs, roughly how long it takes, and what "done"
looks like, in the same shape as the course's checkpoints.

## Why nothing is here yet

Because a drill that exercises a module you have not written is a drill nobody
can do, and a section full of empty pages is a promise rather than a resource.

The course comes first. When Module 17 is finished and verified, this fills up.

In the meantime, [start at Module 0](/course/intro) and build the thing the
drills will run against.

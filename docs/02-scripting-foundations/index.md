---
title: "Module 2: Scripting foundations"
sidebar_position: 0
---

# Module 2: Scripting foundations

You're about to meet the three languages that run this field: PowerShell
for anything Windows, Bash for anything Linux, and Python for the glue in
between. You'll use all three constantly for the rest of the course, and
this module exists so that when a later lesson hands you a script, you
read it like a colleague's work instead of staring at it like a spell.

Here's what this module is not: a programming course. There are no
chapters on data types, no exercises about calculating fibonacci numbers,
and nobody will ask you to invert a binary tree. That approach front-loads
weeks of abstraction before you touch anything real, and for
infrastructure work it's backwards. You don't need to *write* great
software. You need to read a script and know its intent, change the three
lines that matter, and spot the line that would ruin your day. That's
called functional literacy, and it's the actual bar at most jobs.

So instead, each lesson is one real task and one real script, commented
to death. You'll run it, then change it, and the concepts (variables,
loops, functions, pipelines) get explained at the exact moment they
appear, which is also how you'll meet them for the rest of your career.
The three tasks:

- **2.1** PowerShell: measure your machine and file the report in your
  vault, properly this time
- **2.2** Bash: dig the attacker out of a hostile `auth.log`
- **2.3** Python: query CISA's live catalog of actively exploited
  vulnerabilities
- **2.4** journal entry
- **2.5** checkpoint

One habit to start now: every script you touch in this course gets saved
to `Resources/scripts/` in your vault and committed. Your vault is a
diary that's growing a toolbox.

Tier required: none. Everything runs on your own machine. Budget two or
three evenings, more if the concepts are brand new, and that's fine.

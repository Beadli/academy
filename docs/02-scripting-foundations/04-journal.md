---
title: "2.4 Journal: three languages in"
sidebar_position: 4
---

# 2.4 Journal: three languages in

Daily note, four headings, same rhythm as Module 1. Prompts for this
one:

Under **what I did**: which of the three scripts you ran, and which
"make it yours" changes you attempted. Be specific enough that
future-you could find the right script and repeat the change.

Under **what broke**: the execution policy wall counts. So does an awk
field that grabbed the wrong column, a Python traceback, or Git Bash
not being where the Start menu said. Paste the actual error text into
the note; error messages are searchable gold later, and "some Python
error" is worth nothing in six months.

Under **what I learned**: pick the one concept that clicked hardest
(pipes as an assembly line, objects with properties, the sort-and-count
trio, what a function is for) and explain it in two sentences of your
own words. Your words, not the lesson's; copying mine teaches nothing.

Under **open questions**: anything still murky. "Why does awk count
fields from the end with NF?" is a good one. So is "when would I choose
Python over Bash?", which Module 9 and Module 11 will answer with
examples instead of rules.

Then commit and push, and make sure the three scripts went with it:

```bash
cd ~/git/lab-journal
git add -A
git commit -m "journal: module 2, first three scripts in the toolbox"
git push
```

Tick Module 2 in `Projects/lab-progress.md`. Three ticks now. The list
is doing its job.

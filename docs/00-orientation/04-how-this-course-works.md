---
title: "0.4 How this course works"
sidebar_position: 4
---

# 0.4 How this course works

A few mechanics, so nothing later feels arbitrary.

## Numbering and rhythm

Modules are folders, lessons are numbered pages: 5.2 means Module 5,
lesson 2. Every module ends the same way, with a journal entry and then a
checkpoint. The repetition is deliberate. By Module 6 you'll write the
journal entry without being told, and that habit is worth more than any
single lesson in this course.

## Checkpoints

A checkpoint is how you know you're done, instead of hoping you're done.
Early ones are checklists you verify by hand. Once your lab can run
Ansible, checkpoints become playbooks: run one command, and it tells you
in green or red whether your build matches what the module expects. "Did I
do it right?" is the question that kills most self-taught labs, so this
course answers it after every module.

## You build everything by hand first

Later modules teach automation, and automation is the job. But you'll
click through every install manually before you're allowed to automate it,
because you can't troubleshoot a playbook that builds a thing you've never
built yourself. The suffering is the curriculum. It's also temporary.

## One domain for everyone

Every screenshot, command, and checkpoint in this course uses the same
internal domain: **`lab.cyber.internal`**. Use it exactly, even if it
feels odd not to pick your own. When your screen matches the material
character for character, you always know whether a difference is a mistake
or a decision. A later module explains internal naming properly, including
why so many companies that picked `.local` twenty years ago still regret
it. Once you understand the rules, renaming a future lab of your own is
easy.

## Using AI while you learn

You'll use Claude in this course as a working tool, starting properly in
Module 1. That module also sets the rules, and they matter more than the
tool: understand a command before you run it, and keep secrets out of the
chat window. An AI that explains your error message is a tutor. An AI
that does the lab for you is a very fast way to stay unemployable. The
difference is entirely in how you use it, so we teach the how.

## When you get stuck

You will get stuck. That's the course working, not failing. The order I
recommend: reread the lesson (slowly, most stuckness is a skipped line),
check the module checkpoint to narrow down where reality diverged, ask
Claude to explain the error in front of you, and then, if you're still
stuck, post in the course's GitHub Discussions. When you post, say what
you did, what you expected, and what happened instead, and include the
exact error text. That format gets answers, and writing it often reveals
the problem before anyone replies.

## Pacing

The modules get large, and there's no ceiling on depth, so don't binge.
One lesson done properly, journaled, and understood beats three lessons
skimmed. The lab keeps state between sessions; your VMs will wait for you.

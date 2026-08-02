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

## How to read the code in this course

Code blocks look like this, and the label above the box tells you which
shell it belongs in: `powershell` runs on a Windows machine,
`bash` on a Linux one.

Two conventions worth knowing before you meet your first one:

**The comments are the lesson.** Lines starting with `#` explain what
the next line does and why. They're not decoration to skip past, and
they're the reason the code blocks in this course are longer than the
commands they contain.

**A block usually holds several separate commands, not one long
program.** Run them one at a time, read what each returns, and move on.
Where a block is meant to be run as a whole, or saved as a file, the
lesson says so.

Lesson 2.1 covers actually driving a shell: opening it, running
commands, escaping when you've typed something it won't accept, and
getting help without leaving the window. Nothing before that needs it.

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

## Why the lab is on-premises, in 2026

You'll notice the machines in this course live on your laptop rather
than in a cloud account, and it's worth saying plainly that this is a
decision rather than an oversight.

Cloud identity is a synchronization *of* something. Conditional access
policies apply to accounts that came from somewhere. The hybrid setups
that most real enterprises run have an on-premises directory at one
end, and the people who struggle with them are the ones who only
ever learned the cloud end. So this course builds the half that
everything else hangs off, and then bridges it: in Module 9 you'll sync
the directory you built to a cloud tenant of your own and sign in to a
cloud service with credentials you created in Module 5. From Module 4
onward you'll also see short "in cloud terms" notes translating what
you just built into its Azure equivalent, so the vocabulary is familiar
long before you need it.

There's a practical reason too. Your laptop costs nothing per month,
runs on a plane, and lets you break things in ways no cloud account
should ever let you break them. Rented infrastructure would put a
credit card between you and the material, and this course refuses to do
that.

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

---
title: "1.6 Claude, with the rules that keep it useful"
sidebar_position: 6
---

# 1.6 Claude, with the rules that keep it useful

You're learning infrastructure in the first era where every engineer has
an AI assistant, and pretending otherwise would make this course a
museum. So we use one, openly, with rules. Working engineers use AI
constantly; the ones worth hiring can also explain every line it gave
them. This lesson is about becoming the second kind.

Create a free account at [claude.ai](https://claude.ai). The free tier
is enough for this entire course.

## What it's for

Three uses cover most of what I do with it in a lab, and they're the
three I want you practicing:

**Explaining errors.** Paste the full error text and ask what it means,
not how to fix it. "What is this error telling me?" produces
understanding; "fix this" produces dependence. The difference in
phrasing is small and the difference in what you learn is not.

**Explaining commands before you run them.** Found a command in a
forum, in a script, even in this course? Paste it and ask what each
flag does. If the explanation surprises you, you just avoided running
something you didn't understand.

**Turning your terminal history into notes.** At the end of a session,
paste the commands you ran and ask for a summary of what you did, in
order, with the dead ends noted. Edit the result (it's a draft, not a
deliverable) and drop it into your journal. This turns twenty minutes
of "ugh, documentation" into five.

## The rules

There are two, and they're not negotiable.

**Understand a command before you run it.** An AI-suggested command you
don't understand is a stranger's command. It's usually right; the times
it's confidently wrong are exactly the times you can't afford to be
running it blind on a domain controller. If you can't explain what each
part does, ask until you can, then run it.

**Keep secrets out of the chat window.** No passwords, no API keys, no
tokens. Sanitize before you paste; a password in a pasted config is
still a password you've shared. This habit matters at work even more
than in the lab, because companies have lost real secrets exactly this
way.

And one rule for you as a learner rather than an operator: don't let it
do the labs. If Claude writes your GPO and your Ansible playbook and
your detection rule, you'll finish this course with a working lab and
no skills, which is the most expensive possible way to get neither. Use
it to understand your work, not to replace it.

## Do this now

Take any command from lesson 1.3 or 1.4 (`gh repo create` with its
flags is a good candidate), paste it into Claude, and ask what each
part does. Compare the answer against what the lesson told you. Then
save anything new you learned into your journal, because that's the
loop: encounter, understand, record.

## There's a deeper end, and it's locked for a reason

What you've set up here is the shallow end: a chat window and two
rules. Module 11 is the deep end. There, Claude stops being a tab in
your browser and starts working inside your terminal and your repos as
an agent: reading your lab's files, drafting your documentation in your
voice, and running procedures you've packaged for it. It's the closest
thing this course has to a superpower, and working engineers use it
every day. I do.

So why make you wait ten modules for it?

Because this course runs on an escalation ladder. First you build
things with your hands. Then you script what you understood. Then, in
Module 10, you automate what you scripted. Delegating to an AI agent is
the top rung of that same ladder, and every rung depends on the one
below it, for one reason: **you can only safely delegate what you can
verify.** An agent's output looks equally polished whether it's right
or subtly wrong, and the only defense is a reviewer who has built the
thing before. Ten modules from now, that reviewer is you. Today it
isn't, and an agent handed to you today wouldn't make you faster; it
would make you confidently wrong at scale.

You learned arithmetic before you were handed a calculator, and not
because anyone hated you. Same deal. Endure the manual work between
here and Module 11 and you arrive there with the one thing the agent
can't supply: judgment. Skip ahead and you'll finish with a lab you
can't explain in an interview, which is worth exactly nothing.

The pain has a payoff date. It's Module 11.

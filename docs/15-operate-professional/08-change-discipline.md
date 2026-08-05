---
title: "15.8 Change discipline"
sidebar_position: 8
---

# 15.8 Change discipline

Ask anybody who has run production systems what causes outages and you will
hear the same answer before they hear the question: **something changed.**
Not an attack, not hardware, not load. Somebody changed something.

I am stating that as the received wisdom of the field rather than a figure I
can cite, because the published numbers vary enormously with how you count.
What is not in dispute is the practical consequence, and it is the only part
you need.

That is not an argument for changing less. It is an argument for changing in
a way that lets you find out what you did.

## The question that starts every incident

Something breaks. The first useful question is always the same:

**"What changed?"**

If you can answer that in thirty seconds, most incidents become short. If you
cannot, you are debugging a system whose current state is a mystery, and
you will spend hours ruling out things that were never touched.

Everything in this lesson exists to make that question answerable.

## You have been doing this since Module 1

The good news is that change discipline is mostly habits you already have.
Look at what is already true in your lab:

- **Your configurations are in Git.** The compose files from lesson 6.5, the
  detection rules from Module 12, the playbooks from Module 10. Git *is* a
  change log: what changed, when, and who, with the ability to go back.
- **Your journal records what you did and what broke.** Every module.
- **You snapshot before risky changes.** Lesson 3.5, reinforced in 14.1.
- **You check before you apply.** `--check --diff` in Ansible, `--dry-run` in
  restic, `apt list --upgradable`, `nginx -t` before reload.

**That last one is worth naming as a principle**, because you have now met it
in five places: **see what will change before you change it.** It is the same
instinct every time, and it is most of what separates a careful engineer from
a lucky one.

What is missing is small, and it is the part that makes the rest legible.

## Record changes where you will find them

A Git history tells you a file changed. It does not tell you *why*, or that
you also clicked something in a GUI, or that you rebooted a machine.

Keep a running change log. In your vault, `Projects/lab-changes.md`:

```markdown
# Lab change log

Newest first.

## 2026-08-05: Enabled object access auditing on DC01
**Why:** Module 14 found DCSync events (4662) were not being
collected, so the detection could not be written.
**What:** Advanced Audit Policy > DS Access > Audit Directory
Service Access, Success, on the Default Domain Controllers policy.
**Verified:** ran DCSync again, 4662 events now arrive in Wazuh.
**Rollback:** set the same setting back to Not Configured.
**Risk:** increases log volume on DC01. Watch disk.

## 2026-08-04: Upgraded nginx base image 1.20 to latest
**Why:** lesson 13.3, four KEV findings in the old image.
**What:** compose.yaml image tag, committed as a1b2c3d.
**Verified:** rescanned, KEV count 0. Site loads over HTTPS.
**Rollback:** revert the commit, docker compose up -d.
```

**Five fields, and each one is a question somebody asks later:**

- **Why** stops you undoing your own deliberate decision in six months.
- **What**, specifically enough to find it. A commit hash where there is one.
- **Verified**, which is this whole course's habit. A change you did not
  verify is a change you hope happened.
- **Rollback**, written *before* you need it and while you still remember.
- **Risk**, if any, so the next symptom has a suspect.

**Write the entry when you make the change, not later.** Later does not
happen, and the details that matter are the ones you lose first.

## The four questions before any change

Real change processes, the heavyweight ones with committees and forms, are
attempts to make people answer four questions. You can answer them in a
minute, alone, and get most of the value:

1. **What could this break?** Not "will it", could it. Name the blast radius.
2. **How will I know if it worked?** Decide the check before you make the
   change, so you are not inventing success criteria afterwards.
3. **How do I undo it?** If the answer is "restore from backup", that is
   fine, but know it, and know how long that takes from lesson 15.3.
4. **Who else is affected?** In your lab, nobody. In a job this is the
   question that stops you patching the file server during payroll.

**Question three is the one that changes behaviour.** Asking "how do I undo
this" before starting is why you snapshot, why you keep the old config, and
why you move a directory aside rather than deleting it, as lesson 15.3 had
you do.

## Change windows, and why they are not bureaucracy

A **change window** is an agreed period when changes are allowed. It looks
like process for its own sake until you have been on the receiving end.

The real reasons:

- **Somebody is awake and watching.** A change made at 2pm Tuesday gets
  noticed in minutes. The same change at 11pm Friday is discovered by
  customers on Monday.
- **Changes do not collide.** Two teams changing things simultaneously turns
  "what changed" into an unanswerable question.
- **There is time to roll back.** A change made an hour before you leave has
  no rollback time, which means the rollback becomes tomorrow's problem.

**The infamous version is "never deploy on Friday."** The rule is not about
Fridays. It is about not starting something you will not be present to
finish. In your lab that means not patching the domain controllers at
midnight when you want to sleep, which is a real temptation and produces the
same result at a smaller scale.

## Emergency changes, and the honest handling

Sometimes something is on fire and the process is in the way. The
professional answer is not to pretend that never happens.

**Make the emergency change. Then write it up afterwards, marked as an
emergency change, with the same five fields.**

What makes this legitimate rather than an excuse is that the write-up
happens, and that emergency changes are rare enough to notice. **If most of
your changes are emergencies, that is the finding**, and it is about your
environment rather than about your process.

## Test it on yourself

The proof that any of this works is a question you can answer.

Pick something in your lab and answer, without guessing:

**"When did this last change, why, and who did it?"**

Try it on: your nginx configuration, your Wazuh rules, your compose files,
your firewall rules on FW01.

**You will find the answer easily for everything in Git** and struggle for
everything you changed in a GUI. FW01's firewall rules are the likely gap,
because OPNsense's web interface does not commit to your repository.

That gap is real and it is the same one every organisation has: **the things
that are hardest to track are the things changed by clicking.** The honest
mitigations are exactly two: write them in the change log by hand, or export
the configuration into Git periodically. Pick one and do it, rather than
assuming you will remember.

## What you take from this

A change log with the five fields, four questions you can run through in a
minute, and a tested answer to "what changed" for most of your lab plus an
honest note about where you cannot answer it.

That last part, knowing where your visibility ends, is worth more than
pretending it does not.

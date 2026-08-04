---
title: "5.12 Journal: you have a domain"
sidebar_position: 12
---

# 5.12 Journal: you have a domain

Two notes today: one permanent, one daily.

**Permanent.** Create `Projects/lab-domain.md` in your vault and record
the facts you'll look up for the next twelve modules:

- Domain name `lab.internal`, NetBIOS name `LAB`, and the date you
  promoted it
- DC01's address, and that it's also your DNS server
- Where you wrote the Administrator and DSRM passwords
- Your two accounts, and which one holds Domain Admin
- Your OU structure, as a small tree
- The install date and today's `slmgr /dli` reading, so future-you knows
  when the evaluation clock runs out

**Daily note**, four headings as always.

Under **what I did**: installed, named, addressed, promoted, populated,
and wrote a policy. It reads like a lot because it was.

Under **what broke**: the Desktop Experience choice, the DSRM password
prompt, a static address typed into the wrong adapter, a policy that
wouldn't apply because the DC isn't in your `Lab` OU. Write which one
got you and how you worked it out.

Under **what I learned**: explain in your own words why Active Directory
depends on DNS, and what a Kerberos ticket-granting ticket is for. If
you can write those two clearly, you understand more about enterprise
identity than most people who list AD on their CV.

Under **open questions**: "what happens if this single domain controller
dies" is the right question to be asking, and Module 15 takes it
seriously.

```bash
cd ~/git/lab-vault
git add -A
git commit -m "journal: module 5, lab.internal exists"
git push
```

Tick Module 5 in `Projects/lab-progress.md`, and take a snapshot of DC01
called `domain-built`, with DC02 shut down at the time. You've just
crossed the biggest single milestone in this course, and a snapshot means
the next module can't cost you it.

:::warning[Snapshotting domain controllers: this now applies to you]
Reverting a domain controller to an old snapshot in a domain that has
*more than one* can corrupt replication. The reverted DC starts handing
out change numbers it has already issued, the other DCs see updates they
believe they already have, and the two quietly stop agreeing. It's called
a USN rollback, and the supported fix is to demote the rolled-back DC and
rebuild it.

**Until lesson 5.8 your lab had one DC and this was purely theoretical.
It isn't any more.** Two rules from here on:

- Snapshot both DCs at the same time, with both powered off, or not at
  all. A pair of snapshots taken minutes apart is not a consistent pair.
- If you do revert one DC on its own, expect to demote and re-promote it
  rather than hoping. That is genuinely faster than diagnosing it.

In production the answer is a proper backup and restore rather than
hypervisor snapshots at all, which Module 15 covers.
:::

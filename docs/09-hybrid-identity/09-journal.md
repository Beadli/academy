---
title: "9.9 Journal: the account that lives in two places"
sidebar_position: 9
---

# 9.9 Journal: the account that lives in two places

Part of this entry is reference material, and part of it is a decision you
need to make before you walk away.

**Make a permanent note.** In your vault, create `Projects/lab-cloud.md` and
record:

- The **tenant name**, the `yourlab.onmicrosoft.com` one
- The **global administrator account**, and where its password lives. Not the
  password itself, per lesson 1.6.
- Which **signup route** you used from lesson 9.3, and **when it expires** if
  it does. Put the expiry in your calendar as well as your notes; a note you
  do not open is not a reminder.
- The **UPN suffix** you added in 9.2, and whether you verified the domain
- Which machine runs **Entra Connect**, which for you is DC01, and that this
  is a lab compromise rather than how it should be done

That last line is worth writing down in your own words. In an interview, "I
installed it on the domain controller because my lab had no spare memory, and
in production it belongs on a dedicated member server because a DC should run
as little as possible" is a much better answer than not remembering there was
a choice.

## Decide what happens to the tenant

Before you close this, decide one of two things and write it down:

**Keep it.** Reasonable if it does not expire and costs nothing. Note the
expiry and any subscription attached to it, and set a reminder to check in
three months.

**Tear it down.** Also reasonable, and the safer default if you used a trial
with a card attached. Cancel the subscription rather than just abandoning it.
A forgotten trial that renews is the most common way a free lab costs money.

Either is fine. Deciding by accident is not, which is why this is in the
journal rather than left implied.

## Then today's daily note, four headings as usual

Under **what I did**: the bridge you built, in order. The UPN suffix, the
tenant, the sync, and the first user you watched arrive.

Under **what broke**: this module has an unusually consistent failure, so name
yours specifically. A UPN that stayed on `lab.internal`, a domain you could
not verify, credentials confused between the cloud admin and the domain admin,
a disk that was too small, a trial that wanted a card you did not want to give.
Write the symptom and the fix, not just the fix.

Under **what I learned**: pick one of these and write it in your own words,
because writing it is how you find out whether you have it.

- Why the direction of authority means you go to the domain controller to
  disable a leaver, even though you live in the cloud portal all day
- Why password hash sync sends a hash of a hash, and what that protects
- Why a **stalled** sync is more dangerous than a **failed** one

Under **open questions**: this module deliberately leaves several. What would
change if you had used pass-through authentication instead? What happens to
group memberships that exist only in the cloud? What would it take to make the
cloud authoritative instead, and why do organisations mostly not?

Then close the loop:

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 9 complete"
git push
```

Tick Module 9 in `Projects/lab-progress.md`, and take a snapshot of DC01 while
Entra Connect is installed and working. That snapshot is worth having: it is
the only machine in your lab whose state depends on a service you do not
control.

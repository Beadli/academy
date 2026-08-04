---
title: "9.8 What breaks when the bridge goes down"
sidebar_position: 8
---

# 9.8 What breaks when the bridge goes down

You have a directory on your network and a copy in the cloud, joined by an
agent on DC01. Time to break the join deliberately and find out what each side
can still do alone.

This is the lesson that turns the architecture diagram into something you can
reason about during an outage, and it is the reason 9.1 spent time on which
sign-in method you chose.

## Break it

On DC01:

```powershell
# Stop the schedule. The agent stays installed; it just stops running cycles.
Set-ADSyncScheduler -SyncCycleEnabled $false

# Confirm.
(Get-ADSyncScheduler).SyncCycleEnabled
```

The bridge is now down in the way that matters: changes stop flowing.

## What still works

**Cloud sign-in works.** This is the payoff from choosing password hash sync.
The hash is already in the cloud, the check happens there, and nothing needs
your network. Sam can sign in to cloud services with your sync server switched
off, your domain controller switched off, and your entire lab unplugged.

**On-premises sign-in works.** Domain logons never involved the cloud. DC01 is
still authenticating people to domain-joined machines exactly as it did in
Module 5.

**Everything already synced stays synced.** The cloud does not forget its users
because the feed paused. It keeps serving the copy it has.

## What stops

**Changes stop propagating**, in one direction only. Create a user on-premises
and they will not appear in the cloud. Disable someone and their cloud access
stays live.

That second one is the important sentence in this lesson.

:::warning[A broken sync is a security problem, not just an inconvenience]
The failure mode is quiet and asymmetric. Sign-in keeps working, so nobody
raises a ticket. Users are happy. Nothing looks wrong.

Meanwhile every offboarding you perform is silently half-done. You disable a
leaver on the domain controller, watch it succeed, and their cloud access
continues indefinitely.

**This is why sync health is monitored, and why organisations alert on the
sync being late rather than on it failing.** A failure is loud. A pause is not.

You built a monitoring stack in Module 6 and will do detection properly in
Module 12. This is a good example to keep in mind for it: the thing worth
alerting on is not an error, it is the *absence* of an expected event.
:::

## Prove the asymmetry to yourself

Worth doing, because it makes the warning above concrete rather than
theoretical.

```powershell
# With sync still disabled, disable the account.
Disable-ADAccount -Identity sokoth
Get-ADUser sokoth -Properties Enabled | Select-Object SamAccountName, Enabled
```

On-premises she is disabled. Check the cloud portal: she is still enabled
there, and still able to sign in to cloud services.

Two systems, disagreeing, with no error anywhere. Nothing in either interface
tells you they disagree. That is the state a stalled sync leaves you in, and
you would only find it by looking.

## Put it back

```powershell
# Re-enable the schedule.
Set-ADSyncScheduler -SyncCycleEnabled $true

# Push the backlog through.
Start-ADSyncSyncCycle -PolicyType Delta
```

Now the cloud catches up and Sam is disabled in both places, which is what you
wanted the whole time. Re-enable her:

```powershell
Enable-ADAccount -Identity sokoth
Start-ADSyncSyncCycle -PolicyType Delta
```

## The single point of failure you just met

Your sync agent runs on one machine. If that machine dies, the bridge is gone
until you rebuild it, and everything above applies for however long that
takes.

Real environments handle this with a second server installed in **staging
mode**: a full Entra Connect installation that reads everything and writes
nothing, kept ready to take over. You can inspect the setting on your own
install:

```powershell
# StagingModeEnabled should be False on yours: it is the one doing the work.
Get-ADSyncScheduler | Select-Object StagingModeEnabled
```

You are not building a second one; it would mean another Windows server for
one property. But you now know what the word means, why it exists, and that
"we have a staging server" is the answer to a question an interviewer might
ask about resilience.

The general shape is one you have met before and will meet again: **a copy is
only as current as the thing keeping it current.** That is true of your
sync, your backups, your monitoring, and your documentation.

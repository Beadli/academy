---
title: "9.5 Watch your users arrive, and drive the sync yourself"
sidebar_position: 5
---

# 9.5 Watch your users arrive, and drive the sync yourself

The installer ran a sync when it finished. Time to confirm what crossed and,
more usefully, to stop waiting thirty minutes every time you want to see a
change.

## Look in the cloud first

In the Entra admin centre, open the users list. Sam Okoth should be there.

Two things to check on her, because they are the two that tell you whether 9.2
worked:

**Her UPN.** If you verified a domain, it should be the one you set in 9.2. If
you did not, it will be `sokoth@yourlab.onmicrosoft.com`, exactly as
predicted. Neither is a failure; they are different outcomes of the same
mechanism.

**Her source.** The user should be marked as synchronised from on-premises
Active Directory rather than created in the cloud. This is the field that
records which system is authoritative, and it is the one 9.7 makes vivid.

## Check the group came too

Lesson 5.6 built `Lab Engineers` as a security group and put Sam in it, on the
argument that you grant access to groups rather than to people. That argument
holds on the other side of the bridge.

Find the group in the cloud directory's group list. It should be there, marked
as synchronised from on-premises, with Sam as a member.

This matters more than it looks. Cloud services grant access to groups exactly
the way your file server does, so a group you manage in Active Directory can
control who reaches a cloud application. **You add someone to a group on
DC01, and their cloud access changes.** That is the same single point of
control as the account itself, applied to permissions.

One thing to notice: you cannot edit the group's membership in the cloud
portal. Same rule as 9.7, for the same reason.

## Sign in as her

This is the moment lesson 0.4 promised eight modules ago: a credential you
created on your own domain controller, used against a service you did not
build.

Open a **private browser window**, so you are not signed in as your
administrator, and go to a Microsoft cloud sign-in page. `portal.office.com`
or `office.com` will do; you are testing authentication, not the service
behind it.

Sign in as Sam:

- **Username:** her UPN, either `sokoth@yourdomain` if you verified one in 9.3,
  or `sokoth@yourlab.onmicrosoft.com` if you did not. This is where knowing
  which one you have saves confusion.
- **Password:** the one you set on DC01 in Module 5. Not a new one. That is the
  whole point.

You may be prompted to set up multi-factor authentication or change the
password on first sign-in, depending on your tenant's defaults. Both are
sensible defaults doing their job; work through them.

**Stop and notice what just happened.** You typed a password into Microsoft's
sign-in page, and it was checked against a hash derived from the one your own
domain controller holds, for a user you created with a PowerShell command in
Module 5. Your domain controller was not contacted. Lesson 9.6 explains why
that works and what it means.

Sign out of the private window afterwards.

## Now drive it from PowerShell

On DC01, the sync engine exposes a PowerShell module. This is where the module
stops being a portal tour.

```powershell
# The scheduler's current state: how often it runs, and whether it is enabled.
Import-Module ADSync
Get-ADSyncScheduler
```

Read what comes back. The fields worth understanding:

**`CurrentlyEffectiveSyncCycleInterval`** is how often it actually runs, 30
minutes by default. **`NextSyncCycleStartTimeInUTC`** is when it will next go,
in UTC, which catches people out in summer. **`SyncCycleEnabled`** tells you
whether the schedule is running at all.

### Force a cycle

```powershell
# Send what changed since last time. This is what you want almost always.
Start-ADSyncSyncCycle -PolicyType Delta
```

That is the command to remember. Change something in AD, run it, and the
change is in the cloud in seconds instead of half an hour.

There is a heavier one:

```powershell
# Re-evaluate every object, not just what changed. Slow, and rarely the answer.
Start-ADSyncSyncCycle -PolicyType Initial
```

:::tip[Delta versus full, and why the distinction survives everywhere]
A **delta** sync processes what changed. A **full** sync re-reads everything.

That distinction is not a Microsoft idea; you have met it already. It is the
same reason `git` sends only new commits, the same reason a backup can be
incremental, and the same reason Module 5's domain controllers replicate
changes rather than copying the database.

The practical rule is the same everywhere too: delta is for normal operation,
full is for when you have changed the *rules* rather than the data, and
reaching for full to fix a problem you have not diagnosed mostly just means
waiting longer for the same wrong answer.
:::

## Make a change and follow it

This is the loop worth doing at least once by hand, because it turns the
mechanism into something you have watched rather than read about.

On DC01:

```powershell
# Change something visible.
Set-ADUser -Identity sokoth -Title "Infrastructure Engineer" -Department "IT"

# Confirm it landed locally.
Get-ADUser sokoth -Properties Title, Department |
  Select-Object SamAccountName, Title, Department

# Push it.
Start-ADSyncSyncCycle -PolicyType Delta
```

Give it a minute, refresh the user in the cloud portal, and the job title is
there.

You have just watched an attribute travel from a directory you built to a
cloud you own, on a schedule you controlled. That is the whole module in one
loop, and everything left is understanding what it means.

## When nothing arrives

The failures here are boringly consistent, which is good news.

**The user has no UPN in a verified domain.** They still sync, but under
`onmicrosoft.com`. This is 9.2, and it is the most common surprise.

**The object is outside what the sync is configured to read.** Express settings
sync everything by default, so this is more likely if you customised.

**The sync has not run yet.** Thirty minutes is longer than anyone's patience.
Use the delta command above rather than waiting and doubting.

**The sync engine is erroring.** The Synchronization Service Manager, installed
alongside Entra Connect on DC01, shows each connector run and what it did.
Open it and read the most recent run before searching the internet for the
symptom; the error is usually named plainly in there.

```powershell
# Is the scheduler even running? A "False" here explains a lot.
(Get-ADSyncScheduler).SyncCycleEnabled
```

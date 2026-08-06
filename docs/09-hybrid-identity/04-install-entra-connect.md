---
title: "9.4 Install Entra Connect Sync against your own domain"
sidebar_position: 4
---

# 9.4 Install Entra Connect Sync against your own domain

**Entra Connect Sync** is the agent that reads your Active Directory and
writes into your cloud tenant. It runs on a Windows server on your network,
holds a database of what it has seen, and by default wakes every thirty
minutes to send what changed.

## First, give DC01 room

Entra Connect asks for **4 GB of RAM and 70 GB of disk**. Your DC01 was built
in Module 5 with 3 GB and 60 GB, so it needs a bump.

Shut DC01 down cleanly, raise its memory to 6 GB in the hypervisor, and start
it again. This takes two minutes, and it is worth noticing that it takes two
minutes: on physical hardware it would be a purchase, a maintenance window and
a screwdriver. That is a large part of why Module 3 built virtual machines.

Disk is the more awkward one. Expanding a virtual disk means growing it in the
hypervisor *and then* extending the volume inside Windows, which is a two-step
job people routinely half-do and then wonder why Windows still reports the old
size.

```powershell
# What Windows currently thinks it has.
Get-Volume -DriveLetter C | Select-Object DriveLetter, Size, SizeRemaining
```

After growing the disk in the hypervisor, extend the partition inside Windows:

```powershell
# The maximum size the partition could now become.
$max = (Get-PartitionSupportedSize -DriveLetter C).SizeMax

# Take it.
Resize-Partition -DriveLetter C -Size $max
```

:::info[If you would rather not grow the disk]
Your lab has two users. The sync database will be a few megabytes, not
gigabytes, and the 70 GB figure is Microsoft sizing for real organisations.

The installer checks against that production figure rather than against your
actual data, so it may warn. **A warning is not a blocker: read it and
continue.** If it refuses outright, grow the disk and run it again.
:::

:::warning[You are about to do something the documentation advises against]
Microsoft's guidance is to install Entra Connect on a **dedicated
domain-joined member server**, not on a domain controller. Installing on a DC
is supported on Server 2016 and later with Desktop Experience, which is what
you built, but it is not recommended.

The reasons are worth understanding rather than obeying. A domain controller
holds the crown jewels of your identity system and should run as little else
as possible, so every additional service on it is additional attack surface on
the one machine you least want compromised. And in a real environment the sync
process competes for resources with authentication.

You are doing it here because a second Windows server means another 4 GB, and
that is a real cost in a laptop lab for no additional learning. **Know that it
is a lab compromise and say so if an interviewer asks.** Being able to name
where your lab departs from production, and why, reads far better than not
knowing there was a choice.
:::

## Download and run it

Get **Microsoft Entra Connect** from Microsoft's download centre. Search for
it by name rather than following a link from here; the URLs move, and a stale
link is worse than a search term.

You want the one called Entra Connect (formerly Azure AD Connect), not **Entra
Connect cloud sync**, which is a different, lighter agent with different
capabilities. Both are current products and both are things you might use at
work. This module uses the first.

Run the installer on DC01 as a domain administrator.

## Express settings, and why they fit here

The installer offers **Express settings** and **Customize**. Take Express.

Express is the right answer when you have a single forest and you want
password hash sync, which is exactly your situation and the most commonly
deployed configuration in the world. It will:

- connect to your tenant
- connect to your directory
- enable **password hash synchronisation** automatically
- sync everything, then keep syncing every 30 minutes

You will be asked for two sets of credentials, and confusing them is the usual
stumble:

**Your cloud global administrator**, from lesson 9.3. This is the
`something@yourlab.onmicrosoft.com` account, not your domain account.

**A domain administrator on your AD**, so it can read the directory. This is
`LAB\sokoth.adm` or equivalent, the admin account from lesson 5.6, not your
everyday user.

If it rejects the domain credentials, check you are giving it `LAB\username`
or `username@lab.internal` rather than a bare username.

## How we know it worked

The installer says it succeeded. Confirm that independently, because "the
wizard closed" and "the thing is running" are different claims.

On DC01, in PowerShell:

```powershell
# The sync service exists and is running.
Get-Service -Name ADSync | Select-Object Name, Status, StartType

# The scheduler is loaded and knows when it next runs.
Import-Module ADSync
Get-ADSyncScheduler | Select-Object SyncCycleEnabled, NextSyncCycleStartTimeInUTC
```

**`Running` and `SyncCycleEnabled: True` is what you want.** If the service is
stopped, the install completed but something is preventing it starting, and the
Windows event log on DC01 will say what.

Lesson 9.5 uses these same commands to drive the sync deliberately, so you are
meeting them here rather than for the first time when something is wrong.

## Let it finish, then leave it alone for a bit

The first sync runs when the installer completes. In a lab with a handful of
objects it takes a minute or two.

Do not immediately start changing things and re-running it. Lesson 9.5 is
about driving the sync deliberately, and it is much easier to read what is
happening if the first cycle has completed cleanly on its own.

## What you have just built

A one-way pipe from a directory you promoted, to a cloud directory you own,
carrying accounts you created. It runs on a schedule, it holds its own record
of what it has already sent, and it will keep doing this without you.

Lesson 9.5 confirms it worked and shows you how to make it run on demand.

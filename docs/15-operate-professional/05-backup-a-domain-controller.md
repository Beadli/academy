---
title: "15.5 Back up a domain controller"
sidebar_position: 5
---

# 15.5 Back up a domain controller

Lesson 5.12 left you with an open question it called "the right question to be
asking": what happens if this domain controller dies. It also said, when
warning you about snapshotting DCs:

> In production the answer is a proper backup and restore rather than
> hypervisor snapshots at all, which Module 15 covers.

Both promises come due here. **Tier 2 and up**, since you need both
controllers. Tier 1 students should read it anyway; the concepts come up in
interviews constantly.

## Why domain controllers are a special case

Every other machine in your lab can be restored by putting its files back.
A domain controller cannot, and the reason is the thing to understand.

A DC is not a standalone machine holding data. It is **one replica of a
distributed database**, constantly reconciling with its peers. Lesson 5.9 had
you create an object on one and watch it appear on the other. That
replication is tracked with sequence numbers, and every DC keeps a record of
how far it has seen every other DC get.

Now imagine you revert one DC to Tuesday.

That DC believes it is at sequence number 5000. Its partner knows it already
received updates from it up to 5200. So when the reverted DC starts issuing
numbers from 5000 again, it is **reusing numbers its partner has already
seen and filed away**. The partner ignores them, because as far as it is
concerned those updates already happened.

The result is two domain controllers that both believe they are healthy,
that disagree about the contents of the directory, and that will never
reconcile because neither one thinks anything is wrong. It has a name,
**USN rollback**, and it is genuinely one of the nastier states in Windows
administration precisely because nothing looks broken.

**That is why lesson 5.12 told you to snapshot both DCs together with both
powered off, or not at all.** You now know what the rule was protecting you
from.

Modern Windows Server has a safety net (a VM-Generation ID that lets it
detect it was rolled back and recover), but relying on it is not a strategy,
and it does not cover every scenario.

## What you actually back up: system state

The supported way to back up a domain controller is a **system state**
backup. It captures the pieces that make the machine what it is: the
directory database `ntds.dit` from lesson 5.5, SYSVOL, the registry, and the
boot files.

**And note what that means**, having done Module 14: a system state backup
contains `ntds.dit`, which contains every password hash in your domain.
Lesson 14.8 said DC backups "are as sensitive as they are" and now you are
creating one. Wherever this file goes is, effectively, a domain controller.

## Do it

On DC01, in PowerShell as your `.adm` account.

**Install the feature**, which is not present by default:

```powershell
Install-WindowsFeature -Name Windows-Server-Backup -IncludeManagementTools
```

**How you know it worked:**

```powershell
# Expect Installed in the InstallState column.
Get-WindowsFeature -Name Windows-Server-Backup
```

**Take the backup.** It needs somewhere to write that is not the system
volume. Add a second virtual disk to DC01 in your hypervisor, initialise it
in Disk Management, and give it a letter such as `E:`.

```powershell
# -systemStateBackup is the DC-appropriate one. -quiet suppresses
# the confirmation prompt, which is what makes it schedulable.
wbadmin start systemstatebackup -backuptarget:E: -quiet
```

**This takes a while and produces a lot of output.** It is copying the
directory database and SYSVOL.

**How you know it worked:**

```powershell
# The list of backups this machine knows about. Expect an entry
# with today's date and "System State" in its contents.
wbadmin get versions
```

**If it fails complaining about the target**, the most common causes are that
the target is the system volume (not allowed), or the disk is not formatted
NTFS. Both are fixed in Disk Management rather than in the command.

## The two kinds of restore, and why the distinction exists

This is the part worth understanding even if you never perform it, because
choosing wrong makes things worse.

**Non-authoritative restore.** You put the DC's data back, it starts up, and
then it **accepts** everything its partners have that is newer. This is what
you want when a DC's disk failed and you are just rebuilding that machine.
The rest of the domain is the source of truth and this machine catches up.

**Authoritative restore.** You put the data back and declare that this copy
**wins**, forcing it out to the other controllers even though they have
newer information. You want this in one situation: somebody deleted
something important and the deletion has already replicated everywhere. A
non-authoritative restore would just have the deletion replicate straight
back in.

**Get it backwards and you cause the outage.** Restoring authoritatively when
you meant to rebuild a failed machine forces stale data across a healthy
domain and undoes everybody's recent changes.

The mental test: **am I fixing a broken machine, or undoing a bad change?**
Broken machine, non-authoritative. Bad change, authoritative, and only for
the specific objects.

## But the honest answer for a two-DC lab

**With two healthy domain controllers, the fastest recovery from one dying is
usually not a restore at all.**

Lesson 5.9 proved your domain survives losing one DC. So if DC01 dies:

1. **Clean up its remains from the directory**, so the surviving DC stops
   waiting for a machine that is never coming back. This is `ntdsutil`'s
   metadata cleanup, and skipping it leaves a domain full of references to a
   ghost.
2. **Move any FSMO roles it held** to the survivor, seizing them, which is
   exactly the disaster path lesson 5.10's `move-fsmo.ps1` script has a
   `-Seize` flag for.
3. **Build a new DC and promote it**, which is lesson 5.8 again.

The new machine replicates everything from the survivor. **You have lost
nothing, and you never restored a backup.**

That is why redundancy is the primary control and backup is the secondary
one. Your backup exists for the case redundancy cannot cover: both DCs gone,
or a bad change that replicated to all of them.

**Practise the cheap half now.** With DC01 powered off, on DC02:

```powershell
# Report where the roles are. This is the script from 5.10.
.\move-fsmo.ps1

# Seize them, because DC01 is not coming back in this scenario.
.\move-fsmo.ps1 -To DC02 -Seize
```

**How you know it worked:** run the report mode again; all five roles should
name DC02.

Then power DC01 back on.

:::warning[Seizing has a consequence, and this is the lab to learn it in]
**A domain controller whose roles were seized while it was offline must not
be brought back onto the network.** Two machines both believing they hold the
same role is a real problem, and the supported answer is to rebuild it from
scratch rather than reconnect it.

In this exercise you are bringing DC01 back, so **transfer the roles back
gracefully** with `.\move-fsmo.ps1 -To DC01` once both are up and
replication is healthy, and confirm with `repadmin /replsummary` from lesson
5.9.

If your lab ends up confused, this is what the snapshots from lesson 14.1
were for.
:::

## What you take from this

You know why a domain controller cannot be restored like a file server, what
USN rollback is and what lesson 5.12's snapshot rule was protecting you from,
the difference between the two restore types and how to choose, and the
honest answer that with two DCs your real recovery is rebuild rather than
restore.

You also have a system state backup, which is now one of the most sensitive
files in your lab.

---
title: "5.10 FSMO roles, and a script to move them"
sidebar_position: 10
---

# 5.10 FSMO roles, and a script to move them

Lesson 5.9 ended on a loose end: replication is multi-master, both DCs are
writable, and yet five operations still can't be done by just anybody.

Some jobs cannot safely happen in two places at once. If two domain
controllers both handed out the same account identifier at the same
moment, or both accepted a different change to the directory's schema, the
directory would have no way to decide which one was right. So Active
Directory keeps five jobs single-master: exactly one DC holds each, and
that DC is the only one allowed to do it.

They're called **FSMO roles**, for Flexible Single Master Operation, and
everyone pronounces it "fizz-mo." The name is unhelpful. The idea is
simply: five jobs, one holder each.

## The five, and what actually breaks

Two are forest-wide, meaning one holder across the whole forest:

| Role | What it does | What breaks without it |
|---|---|---|
| **Schema Master** | The only DC that can change the directory's schema | You can't extend the schema. Installing Exchange or similar fails. Nothing else notices. |
| **Domain Naming Master** | Approves adding or removing domains | You can't add a domain. Nothing else notices. |

Three are per-domain:

| Role | What it does | What breaks without it |
|---|---|---|
| **PDC Emulator** | Time source for the domain, handles password changes urgently, target for GPO edits and account lockout | The most missed. Time drifts, recent password changes take longer to work everywhere, lockouts behave oddly. |
| **RID Master** | Hands out blocks of the numbers used to build new account identifiers | Existing accounts fine. Eventually you cannot create new ones, once the current DC's block runs out. |
| **Infrastructure Master** | Keeps references to objects in other domains current | Irrelevant in a single-domain forest like yours. Genuinely matters in a multi-domain one. |

Notice how unevenly that table falls. Losing the Schema Master is
survivable for months. Losing the PDC Emulator is felt the same afternoon.
That asymmetry is why "which roles were on the dead server" is one of the
first questions in a real DC outage.

## Find out who holds what

```powershell
# Domain-level roles.
Get-ADDomain | Select-Object PDCEmulator, RIDMaster, InfrastructureMaster

# Forest-level roles.
Get-ADForest | Select-Object SchemaMaster, DomainNamingMaster
```

All five will name `DC01.lab.internal`, because the first DC in a new
forest takes every role by default and nothing has moved them since.

There is also an older command that prints all five at once, and you'll
see it in every support article ever written:

```powershell
netdom query fsmo
```

## Transfer versus seize, which is the distinction that matters

There are two ways to move a role, and confusing them is how people
damage domains.

**Transfer** is the planned move. Both DCs are up and talking. The
current holder hands the role over cleanly and knows it no longer holds
it. This is what you do before decommissioning a DC, before a rebuild, or
to rebalance roles. It is safe, and it is reversible by transferring back.

**Seize** is the disaster move. The holder is gone and is not coming
back, so another DC simply declares that it holds the role now. The old
holder is never told, because it can't be.

:::warning[The rule that has no exceptions]
**A domain controller whose roles were seized must never come back
online.** Not to copy files off, not "just to check something."

If it does, two DCs believe they hold the same single-master role, and
you get exactly the split-brain the roles exist to prevent. The correct
handling of a seized-from DC is a forced removal from the directory and a
rebuild from scratch. Plan on that before you seize anything.

Seize only when the machine is genuinely unrecoverable. If it can be
booted, transfer instead.
:::

## When you'd actually move roles

Transfers aren't an exotic operation. The most common reason is the
dullest one: **you are about to patch and reboot the DC holding them.**

Move the roles to the other DC first, then patch. The reasoning isn't
really about the few minutes of downtime, because most of these roles
aren't missed over a reboot. It's about what happens if the patch goes
badly and that server never comes back up.

- **Roles already moved:** you've lost a replica. Annoying, rebuild it
  when convenient, nothing urgent.
- **Roles still on it:** you now have to *seize* them, which per the
  warning above means that machine can never rejoin the domain and must
  be demoted forcibly and rebuilt from scratch.

One two-minute command beforehand turns a disaster-recovery exercise into
a Tuesday. That is the whole argument, and it's why "move the FSMO roles"
appears in the patching runbook of essentially every organization that has
been bitten once.

The same logic applies to decommissioning a DC, moving one to different
hardware, or any planned outage longer than a reboot.

Two habits that go with it, both of which Module 13 revisits when it
covers patching properly:

- **Never patch both domain controllers at once.** Lesson 5.9 showed you
  the domain survives losing one. It does not survive losing both, and a
  patch window is the most common way people accidentally arrange that.
- **Check where the roles are before you start**, not from memory. The
  report mode of the script below exists for exactly this.

## The script

Save this as `move-fsmo.ps1` in `Resources/scripts/` in your vault, the
same way you saved the scripts in Module 2. Read every comment; the
comments are the lesson.

```powershell
# move-fsmo.ps1
# Report on, and optionally move, the five FSMO roles.
# Usage:
#   .\move-fsmo.ps1                          report only
#   .\move-fsmo.ps1 -To DC02                 transfer all five to DC02
#   .\move-fsmo.ps1 -To DC02 -Roles PDCEmulator,RIDMaster
#   .\move-fsmo.ps1 -To DC02 -Seize          disaster path, read the warning

# param() must be the first code in the file. It defines what the script
# accepts, so PowerShell validates the input instead of you doing it.
param(
    # The DC to move roles TO. Optional: with no -To, this only reports.
    [string]$To,

    # Which roles. The default is all five. ValidateSet means PowerShell
    # rejects a typo with a helpful message instead of failing halfway.
    [ValidateSet("PDCEmulator","RIDMaster","InfrastructureMaster",
                 "SchemaMaster","DomainNamingMaster")]
    [string[]]$Roles = @("PDCEmulator","RIDMaster","InfrastructureMaster",
                         "SchemaMaster","DomainNamingMaster"),

    # A switch is a true/false flag: present means true, absent means false.
    [switch]$Seize
)

# Stop on the first error rather than carrying on after something failed.
# Half-moved roles are worse than none moved.
$ErrorActionPreference = "Stop"

# Import-Module makes the AD cmdlets available. It is already loaded on a
# DC, but saying so means the script also runs from a workstation with the
# remote administration tools installed.
Import-Module ActiveDirectory

function Show-CurrentHolders {
    # A function groups steps under a name so the script reads as a
    # sequence of intentions rather than a wall of commands.
    $domain = Get-ADDomain
    $forest = Get-ADForest

    # [PSCustomObject] builds an object with the properties we name, so
    # the output formats as a table instead of loose text.
    [PSCustomObject]@{
        PDCEmulator          = $domain.PDCEmulator
        RIDMaster            = $domain.RIDMaster
        InfrastructureMaster = $domain.InfrastructureMaster
        SchemaMaster         = $forest.SchemaMaster
        DomainNamingMaster   = $forest.DomainNamingMaster
    }
}

Write-Host "`nCurrent FSMO role holders:" -ForegroundColor Cyan
Show-CurrentHolders | Format-List

# No -To means the caller wanted a report. Stop here.
# Doing the safe thing by default is deliberate: running this script with
# no arguments must never change anything.
if (-not $To) {
    Write-Host "Report only. Pass -To <DC> to move roles.`n"
    exit 0
}

# Confirm the destination exists and is really a domain controller.
# Get-ADDomainController throws if the name is wrong, which combined with
# $ErrorActionPreference stops us before anything is moved.
$target = Get-ADDomainController -Identity $To
Write-Host "Target: $($target.HostName)" -ForegroundColor Cyan

if ($Seize) {
    # The dangerous path. Make the caller type the DC's name to proceed,
    # so a seize can never happen because someone pressed Enter twice.
    Write-Warning "SEIZE is for a domain controller that is GONE and will NEVER return."
    Write-Warning "A seized-from DC that comes back online creates a split-brain domain."
    $confirm = Read-Host "Type the target DC name ($To) to confirm seizing"

    if ($confirm -ne $To) {
        Write-Host "Names did not match. Nothing was changed."
        exit 1
    }
} else {
    # The planned path. Both DCs must be up, so prove the target answers
    # before starting rather than discovering it halfway through.
    Write-Host "Transferring (planned move, both DCs must be online)."
    if (-not (Test-Connection -ComputerName $target.HostName -Count 2 -Quiet)) {
        throw "$To is not responding. Transfer needs it online; use -Seize only if it is gone for good."
    }
}

# The move itself. One cmdlet does both jobs: adding -Force turns a
# transfer into a seize, which is a remarkably small difference for an
# operation with such different consequences.
foreach ($role in $Roles) {
    Write-Host "  moving $role ..."
    if ($Seize) {
        Move-ADDirectoryServerOperationMasterRole -Identity $To `
            -OperationMasterRole $role -Force -Confirm:$false
    } else {
        Move-ADDirectoryServerOperationMasterRole -Identity $To `
            -OperationMasterRole $role -Confirm:$false
    }
}

Write-Host "`nDone. Holders are now:" -ForegroundColor Green
Show-CurrentHolders | Format-List
```

## Run it

Report first, always:

```powershell
cd ~\git\lab-journal\Resources\scripts
.\move-fsmo.ps1
```

Five lines, all naming DC01. Now move one role and watch it land:

```powershell
.\move-fsmo.ps1 -To DC02 -Roles PDCEmulator
```

Check from the other direction, so you're not just trusting the script's
own output:

```powershell
netdom query fsmo
```

The PDC Emulator is now DC02 and the other four are still DC01. Splitting
roles across DCs like this is completely normal in production.

Move it back when you're done, because the rest of the course assumes
DC01 unless it says otherwise:

```powershell
.\move-fsmo.ps1 -To DC01 -Roles PDCEmulator
```

:::tip[Least privilege]
Notice the script's default with no arguments is to **report and change
nothing**, and that `-Seize` demands you type the DC's name before it will
act.

That's the same instinct as `?mode=ro` in lesson 6.9 and the two accounts
in 5.6, applied to your own tooling: the safe operation is the default,
and the dangerous one has to be asked for explicitly. Scripts you write
for other people to run should always be built this way. The person
running it at 3am will not have read the comments.
:::

## Make it yours

1. Add a `-WhatIf` style dry run that prints what it *would* move without
   moving anything. PowerShell has real support for this via
   `SupportsShouldProcess`, and looking up how it works is a good use of
   lesson 1.6.
2. Make the script refuse to move the Schema Master unless the caller
   names it explicitly, since it's the one with the most far-reaching
   consequences and the least reason to move casually.
3. Harder: have it write what it did, with a timestamp, into a Markdown
   file in your journal. Real change records are written by the thing that
   made the change, not by somebody remembering afterwards.

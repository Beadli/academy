---
title: "9.10 Checkpoint: one identity, two directories"
sidebar_position: 10
---

# 9.10 Checkpoint: one identity, two directories

Prove the module stuck. The test that matters is behavioural: an account you
created on your own domain controller can be switched off from that domain
controller, and its cloud access stops.

## The end-to-end test

1. Confirm Sam is enabled and can sign in to a cloud service.
2. On DC01, `Disable-ADAccount -Identity sokoth`.
3. `Start-ADSyncSyncCycle -PolicyType Delta`.
4. Wait a minute, then try to sign in to the cloud service as her.
5. Blocked.
6. Re-enable, sync, confirm she is back.

If that works, the whole chain works: the UPN, the tenant, the sync agent, the
schedule, and the direction of authority.

## Commands

On DC01, in PowerShell:

```powershell
# The forest offers a routable suffix, and your users use it.
(Get-ADForest).UPNSuffixes
Get-ADUser -Filter * -Properties UserPrincipalName |
  Select-Object SamAccountName, UserPrincipalName

# The sync engine is installed, scheduled and enabled.
Import-Module ADSync
Get-ADSyncScheduler |
  Select-Object SyncCycleEnabled, CurrentlyEffectiveSyncCycleInterval,
                NextSyncCycleStartTimeInUTC, StagingModeEnabled

# A delta cycle runs on demand without erroring.
Start-ADSyncSyncCycle -PolicyType Delta
```

## Pass criteria

- [ ] `(Get-ADForest).UPNSuffixes` lists the suffix you added in lesson 9.2
- [ ] Every user you intended to sync has a UPN in that suffix, not
      `@lab.internal` (lesson 9.2)
- [ ] A tenant exists, and you have recorded its name and admin account in
      `Projects/lab-cloud.md` (lessons 9.3, 9.9)
- [ ] Entra Connect Sync is installed and `SyncCycleEnabled` is `True`
      (lesson 9.4)
- [ ] Sam Okoth appears in the cloud directory, marked as synchronised from
      on-premises rather than cloud-only (lesson 9.5)
- [ ] A change made in Active Directory appears in the cloud after a delta
      sync (lesson 9.5)
- [ ] `Lab Engineers` from lesson 5.6 appears as a synced cloud group with Sam
      in it (lesson 9.5)
- [ ] You signed in to a cloud service as Sam, in a private window, using the
      password you set on DC01 in Module 5 (lesson 9.5)
- [ ] Editing a synced attribute in the cloud portal is refused (lesson 9.7)
- [ ] Disabling on-premises blocks cloud sign-in after a sync (lesson 9.7)
- [ ] You disabled the schedule, saw the two directories disagree with no
      error shown anywhere, and re-enabled it (lesson 9.8)
- [ ] You have decided, and written down, whether the tenant is being kept or
      torn down (lesson 9.9)

## What you can now say

That you have run hybrid identity from both ends. Not clicked through a
portal: built the directory, fixed the UPN problem that blocks real
migrations, installed the sync agent, and watched authority flow one way and
refuse to flow the other.

The specific thing worth saying in an interview is the offboarding one. **You
can explain why disabling a leaver happens on the domain controller and not in
the cloud portal, and what it means if the sync is stalled when you do it.**
Plenty of people administering these environments have never had that
explained to them, and it is the difference between following a runbook and
knowing what the runbook is for.

Module 10 turns to automation, and the manual work you have done since Module 5
is exactly what makes an Ansible playbook readable rather than magic.

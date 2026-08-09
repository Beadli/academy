---
title: "5.9 Watch replication work, then break it on purpose"
sidebar_position: 9
---

# 5.9 Watch replication work, then break it on purpose

You have two domain controllers. Neither is a copy of the other in the
way a backup is a copy: **both are writable, and both are authoritative.**
Create a user on either one and it becomes real on both.

That model is called multi-master replication, and it's the reason Active
Directory scales to organizations with domain controllers on four
continents. It's also the source of its stranger failure modes, so it's
worth watching happen rather than taking on faith.

Both DCs need to be running for this lesson.

## Watch a change cross

On **DC01**, create something you'll recognise:

```powershell
New-ADUser -Name "Replication Test" `
           -SamAccountName "reptest" `
           -Path "OU=Users,OU=Lab,DC=lab,DC=internal" `
           -AccountPassword (Read-Host -AsSecureString "Password") `
           -Enabled $true
```

Now on **DC02**, ask that specific machine, not "the domain":

```powershell
# -Server forces the question at one named DC rather than letting
# Windows pick. Without it you might be answered by DC01 and learn
# nothing.
Get-ADUser -Identity reptest -Server DC02
```

It's already there. On a healthy network inside one site, replication of a
change like this happens within about fifteen seconds, because domain
controllers in the same site notify each other rather than waiting for a
schedule.

If it isn't there yet, wait and ask again. If it still isn't, you've got a
real problem to diagnose, and the rest of this lesson is the toolkit.

## The command that answers "is replication healthy?"

```powershell
repadmin /replsummary
```

You want a table with both DCs listed, `0` in the fails column, and a
recent time in `largest delta`. That is the single fastest health check
for a multi-DC domain, and it's the first thing to run when users report
that "something is weird since this morning."

For detail on one machine:

```powershell
# Every inbound replication partner for this DC, what it last pulled,
# and whether it worked.
repadmin /showrepl
```

`Last attempt ... was successful` on each line is what healthy looks like.

## Two things replicate, by two different mechanisms

This trips people up, so meet it now.

**Directory objects** (your users, groups, computers, OUs) replicate
through AD's own replication, which is what you just watched.

**SYSVOL**, short for *system volume*, is a folder every domain controller
shares out to the whole domain. It holds logon scripts and the actual files
behind the Group Policy object you created in lesson 5.7, and it replicates
separately, over DFS Replication. It's a file share, not directory data.

Check the second one exists on DC02:

```powershell
# The GPO you made in 5.7 should be here, as files, on both DCs.
Get-ChildItem \\DC02\SYSVOL\lab.internal\Policies
```

Why care about the distinction? Because they fail independently. A domain
where users and groups replicate perfectly but SYSVOL is broken looks
completely healthy in ADUC while group policy silently stops applying to
half the estate. When someone says "the GPO isn't applying and I can't see
why," this is the second thing to check.

## Now switch DC01 off

This is the lesson. Everything above was preparation.

Shut DC01 down properly, then, from a domain-joined machine or from DC02
itself:

```powershell
# Who answered this time?
(Get-ADDomain).PDCEmulator
Get-ADUser -Identity reptest
```

The queries still work. Logins still work. DNS still resolves, because
lesson 5.8 pointed both machines at both DNS servers.

**Nothing you built has stopped.** That is what the second domain
controller was for, and it's a far more convincing argument than any
diagram: the domain survived losing the machine that created it.

Write in your journal what you did and what still worked, because "we
tested DC failure and here is the evidence" is exactly the kind of thing
Module 16 will ask you to produce for real.

### What does degrade

Be precise rather than triumphant, because a beginner who concludes
"nothing breaks when a DC dies" will be surprised later.

With DC01 off, five special roles it was holding are now unavailable. Most
day-to-day work does not touch them, which is why everything above kept
running. But some operations will fail or behave oddly until those roles
move, including password changes propagating promptly, adding new domains,
and running out of the pool of security identifiers used to create
accounts.

Those roles are the subject of the next lesson, and moving them is exactly
what you'd do at this point in a real outage.

Bring DC01 back up before continuing. Give it a couple of minutes, then
confirm the pair re-converged:

```powershell
repadmin /replsummary
```

## Make it yours

1. Create a user on **DC02** this time and watch it appear on DC01.
   Replication is genuinely bidirectional, and proving that to yourself
   beats being told.
2. Force replication rather than waiting: `repadmin /syncall /AdeP`. Read
   `repadmin /syncall /?` first and work out what those flags mean, per
   lesson 1.6's rule about understanding a command before running it.
3. Harder: change the same user's description on both DCs within a few
   seconds of each other, then see which value survives. You've just
   created a replication conflict, and AD resolves it by timestamp with
   the later write winning. This is why "who changed this?" is sometimes
   genuinely difficult to answer in a large directory.

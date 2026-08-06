---
title: "DEF-11 Prove a policy applied, properly"
sidebar_position: 10
---

# DEF-11: Prove a policy applied, properly

|  |  |
|---|---|
| **Objective** | Prove a Group Policy reached a machine that represents your estate, and that one you scoped out did not reach it |
| **Success signal** | `gpresult` on a member machine showing the policy you targeted, and a second policy provably absent for a reason you can name |
| **Needs** | Module 5, and a domain-joined Windows machine that is not a domain controller. If you do not have one, build [EXT-07](/drills/extensions/ext-07-windows-client) first |
| **Effort** | An evening |
| **Risk** | Reversible. You are adding policies and moving one computer object |
| **Check** | Mechanical |

## Why this drill exists

In lesson 5.7 you wrote a Group Policy, ran `gpresult`, and saw it applied.
That lesson had one machine available to it, and that machine was a domain
controller.

**A domain controller is close to the worst machine in the estate to test a
policy against.** It sits in its own OU, created by Active Directory rather
than by you, carrying its own policies that apply nowhere else. It is the one
machine you would never deploy a workstation setting to. Proving a policy
works there proves it works there.

That was forced by sequencing rather than chosen: at that point in the course
DC01 was the only Windows machine you had. Now you have another one, so you
can do this the way it is actually done.

**And you can do the half nobody practises.** Everyone verifies that a policy
arrived. Almost nobody verifies that a policy stayed away from the machines
they deliberately excluded, which is how a GPO linked one level too high goes
unnoticed until it breaks something at three in the morning.

## Your objective

**Prove two things about scope, on a machine that is not a domain
controller:**

1. A policy you targeted at workstations reaches your workstation.
2. A policy you targeted at servers does not, **and you can demonstrate that
   the reason is scope rather than the policy being broken.**

That second clause is the entire drill. It is easy to point at a policy that
appears nowhere and call it correctly scoped. A policy that is silently
failing for every machine in the domain looks exactly the same from where you
are standing.

Three things have to be true when you are done:

1. Your workstation lives in an OU you created, not in a built-in container.
2. `gpresult` on the workstation lists the policy you meant it to have.
3. You have shown the server-scoped policy working *somewhere*, so its absence
   on the workstation means something.

## How you will know

```powershell
# On the workstation. The list of policies this machine believes
# apply to it. This is the command lesson 5.7 taught you.
gpresult /r /scope:computer
```

And the check that actually decides the drill: **you can say out loud why the
server policy is missing, and back it with a run where it was present.**
"It didn't show up" is not a result. "It didn't show up here, and it did show
up when the same machine sat in the other OU" is.

<details>
<summary>Nudge, if you do not know where to start</summary>

Start by asking where your workstation actually is in the directory. Not where
you assume it is: look.

When a machine joins a domain, Active Directory puts its computer account
somewhere by default, and lesson 5.6 already warned you about the difference
between that place and the OUs you created. Re-read the last paragraph of
"Build an OU structure first" if it has gone fuzzy.

Once you know where it is, the rest of the drill is the four-item checklist at
the end of lesson 5.7, run deliberately instead of in a panic.

</details>

<details>
<summary>Fuller hint, if you know the direction but not the method</summary>

**The machine is in the `Computers` container, not an OU.** That is where
domain joins land by default, and it is a *container*, so you cannot link a
Group Policy to it at all. Your first job is to create an OU for workstations
and move the computer object into it.

Note what that means: until you move it, the only policies your workstation
can receive are ones linked at the domain root. Lesson 5.7's logon notice
reaches it. Nothing you scope to an OU ever will.

**For the negative case, the tool matters.** `gpresult /r` lists what applied.
A policy linked to an OU your machine is not in does not appear in that output
as denied or filtered. It simply is not there, exactly as a broken policy is
not there. The two look identical.

So do not try to prove the negative by staring harder at the output. **Change
one variable and watch the result change.** You have one machine and two OUs,
which is all a controlled experiment needs.

**On the setting to use:** you do not need a new one. The logon notice from
5.7 is visible, harmless, and you already know where it lives. Three notices
with three different messages will tell you exactly which policy won.

</details>

<details>
<summary>Full walkthrough</summary>

### 1. Find out where the computer object actually is

On DC01:

```powershell
# Where did the domain join put this machine? Substitute your own
# machine name if it is not WKS01.
Get-ADComputer WKS01 | Select-Object Name, DistinguishedName
```

Expect something ending `CN=Computers,DC=lab,DC=internal`. **`CN=`, not
`OU=`**, and that single letter is the whole problem. `Computers` is a
built-in container, and Group Policy cannot be linked to a container. Lesson
5.6 told you this about the `Users` container; it is the same trap with the
same shape.

### 2. Make an OU for workstations, and move the machine into it

Lesson 5.6 built you `Lab` with `Users`, `Servers` and `Groups` inside it.
There was no reason to make a workstation OU then, because you had no
workstations.

```powershell
# On DC01. A place for machines people sit at.
New-ADOrganizationalUnit -Name "Workstations" `
                         -Path "OU=Lab,DC=lab,DC=internal"
```

```powershell
# Move the computer account into it.
Get-ADComputer WKS01 |
    Move-ADObject -TargetPath "OU=Workstations,OU=Lab,DC=lab,DC=internal"
```

**How you know it worked:**

```powershell
# The DistinguishedName should now contain OU=Workstations.
Get-ADComputer WKS01 | Select-Object DistinguishedName
```

**Why separate workstations from servers at all**, since this is the question
the drill is really about: they need opposite policies. A server should refuse
interactive logins from ordinary staff; a workstation exists for them. Lock a
server's screen after a minute and nobody notices; do it to a workstation and
you get complaints. Scope exists because one setting is right in one place and
wrong in another, and the OU structure is how you say which is which.

### 3. Write the two policies

Both are logon notices, the same setting you used in 5.7, so nothing here is
new except where you attach it. Open **Group Policy Management**
(`gpmc.msc`) on DC01.

**Policy one, for workstations:**

1. Right-click `OU=Lab > Workstations` and choose **Create a GPO in this
   domain, and Link it here**. Name it `Lab - Workstation Notice`.
2. Edit it, and go to **Computer Configuration > Policies > Windows Settings >
   Security Settings > Local Policies > Security Options**, exactly as in 5.7.
3. Define **Interactive logon: Message title for users attempting to log on**
   as `Workstation policy applied`.

**Policy two, for servers:**

1. Right-click `OU=Lab > Servers`, create and link a GPO named
   `Lab - Server Notice`.
2. Set the same message title setting to `Server policy applied`.

Two policies, one setting, different links. **The link is the only difference,
and the link is what you are testing.**

### 4. Prove the positive

On the workstation:

```powershell
# Moving a computer between OUs changes which policies apply to it,
# and the machine will not notice until it refreshes. A reboot is the
# reliable way to pick up a move, because computer policy applies at
# boot.
gpupdate /force
```

**If the move was recent, reboot rather than trusting `gpupdate`.** A computer
account that has changed OU sometimes needs the reboot before it reads its new
scope, and chasing a result that is only stale wastes an hour.

```powershell
# Then ask what the machine believes applies to it.
gpresult /r /scope:computer
```

**What you are looking for:** `Lab - Workstation Notice` in the applied list,
and `Lab - Logon Notice` from 5.7 still there as well, because that one is
linked at the domain root and reaches everything.

Now sign out. **The notice you see is `Workstation policy applied`**, not the
5.7 text, because two policies set the same value and the one linked closest
to the object wins. Lesson 5.7 stated that rule in one sentence. This is you
watching it happen.

### 5. Prove the negative, and prove it properly

`Lab - Server Notice` should be absent from that `gpresult` output. Confirm it
is.

**Then stop and be suspicious of your own result.** You have a policy that is
not there. So far that is equally consistent with three things: you scoped it
correctly, you mislinked it somewhere harmless, or you never actually defined
the setting and it does nothing anywhere.

Change one variable:

```powershell
# On DC01. Temporarily move the workstation into the Servers OU.
# This is the experiment: nothing about the policy changes, only
# where the object sits.
Get-ADComputer WKS01 |
    Move-ADObject -TargetPath "OU=Servers,OU=Lab,DC=lab,DC=internal"
```

Reboot the workstation, then run `gpresult /r /scope:computer` again.

**Now `Lab - Server Notice` applies and `Lab - Workstation Notice` does not**,
and the login screen says `Server policy applied`. The policies did not
change. The OU did.

"It didn't show up" has now become a proof. You have demonstrated that the
server policy works, and that the only thing keeping it off your workstation
is scope.

Put the machine back:

```powershell
# On DC01. Return it to where it belongs.
Get-ADComputer WKS01 |
    Move-ADObject -TargetPath "OU=Workstations,OU=Lab,DC=lab,DC=internal"
```

Reboot once more and confirm you are back to `Workstation policy applied`.
**Leaving the lab in the state you found it is part of the drill**, and it is
the habit that separates people who can be trusted with production from people
who cannot.

### 6. Get the report an auditor would ask for

```powershell
# On the workstation. A full HTML report of computer policy, which
# is far more readable than the console output and is the artefact
# worth keeping.
gpresult /h C:\gpresult-wks01.html /scope:computer
```

Open it. It shows what applied, what was denied and why, and the winning
policy for each individual setting. **The per-setting winner is the part worth
looking at**, because it answers the question `gpresult /r` cannot: not which
policies applied, but which one actually decided each value.

Lesson 5.7 mentioned that auditors ask for the policy object, its link, and
`gpresult` output proving it reached a machine. You now have that trio for a
machine that represents the estate rather than for a domain controller.

</details>

## Going further

- **Prove it for a user setting, not a computer setting.** User policy follows
  the account, not the machine, so the OU that matters is the one your user
  lives in. Run `gpresult /r /scope:user` and work out why the answer is
  different.
- **Break it deliberately.** Link `Lab - Server Notice` at the domain root as
  well and work out, from the HTML report alone, which link is winning and
  why. This is the everyday skill.
- **Block inheritance on the Workstations OU** and see what stops arriving.
  Then find out what **Enforced** does to your answer, because those two
  features exist to fight each other and the interaction is a standard
  interview question.

## What this proves

You can demonstrate that a configuration reached the machines you intended and
stayed off the ones you did not. That second half is rare. Most people can
show you a policy working; far fewer have ever confirmed the boundary of one,
which is the thing an auditor is actually asking about when they ask whether a
control is applied.

You also now know the difference between a policy that is correctly scoped out
and a policy that is quietly broken, and that telling them apart takes an
experiment rather than a closer look.

:::note[Write this down before you close the tab]

In your own words, in your journal, while it is fresh:

- Why a domain controller is a poor machine to test a workstation policy on.
- How you proved the server policy was excluded rather than broken, and what
  you would have concluded if you had skipped that step.

Six months from now you will remember that you moved a computer between OUs,
and not what it demonstrated.

:::

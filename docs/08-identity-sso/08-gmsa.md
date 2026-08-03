---
title: "8.8 gMSA: accounts that rotate their own passwords"
sidebar_position: 8
---

# 8.8 gMSA: accounts that rotate their own passwords

:::note[Tier 2, because it needs a domain. Tier 1, read it.]
Group Managed Service Accounts are an Active Directory feature, so this
lesson needs the domain from Module 5. The problem it solves is universal
though, and the reasoning transfers to every platform.
:::

In lesson 8.3 you created `svc-adfs`, an ordinary user account with a long
password, and handed that password to a service. That's how most service
accounts in most organizations work, and it has three problems that
compound over time.

**Somebody knows the password.** You do. Probably it's in a password
manager, possibly it's in a runbook, and in a great many organizations it's
in a text file on somebody's desktop.

**It never changes.** Rotating it means scheduling downtime, changing it in
the directory, changing it in every service that uses it, and restarting
those services. So it doesn't get rotated. Service account passwords set
in 2019 are entirely normal.

**It doesn't leave with people.** The administrator who set it up
remembers it after they change teams or leave.

A **Group Managed Service Account** removes all three. Active Directory
generates the password, hands it only to the machines you authorise,
rotates it automatically every 30 days, and never shows it to a human.
Nobody knows the password, because there is nothing to know.

## Set up the key that makes it possible

The domain needs a **KDS root key** once, ever. It's the seed from which
the directory derives every gMSA password.

On DC01:

```powershell
# Does one already exist?
Get-KdsRootKey
```

If that returns nothing, create one:

```powershell
# The effective time is deliberately in the past. By default a new key
# is not usable for 10 hours, to let it replicate to every DC. In a lab
# with two controllers that finish in seconds, waiting is pointless.
# Never do this in production: you would be using a key before every
# domain controller has it, and accounts would fail unpredictably.
Add-KdsRootKey -EffectiveTime ((Get-Date).AddHours(-10))
```

That comment matters more than the command. The ten-hour delay exists for
a reason, and the lab is skipping it because your replication is instant
and observable, which you proved in lesson 5.9.

## Create the account

```powershell
# A group holding the machines allowed to retrieve the password.
# A group rather than a machine, so adding a second AD FS server later
# is one membership change instead of recreating the account.
New-ADGroup -Name "gMSA-ADFS-Hosts" `
            -GroupScope Global -GroupCategory Security `
            -Path "OU=Groups,OU=Lab,DC=lab,DC=internal"

Add-ADGroupMember -Identity "gMSA-ADFS-Hosts" -Members "ADFS01$"

# The account itself. The trailing $ on ADFS01 above is not a typo:
# computer accounts end in $, and this is a computer, not a person.
New-ADServiceAccount -Name "gmsa-adfs" `
                     -DNSHostName "sso.lab.internal" `
                     -PrincipalsAllowedToRetrieveManagedPassword "gMSA-ADFS-Hosts"
```

Then on ADFS01, install and test it:

```powershell
Install-ADServiceAccount -Identity "gmsa-adfs"

# Should return True. If False, the machine is not in the group, or
# it has not picked up the membership yet.
Test-ADServiceAccount -Identity "gmsa-adfs"
```

:::warning[Group membership needs a reboot]
`Test-ADServiceAccount` returning `False` right after you added the machine
to the group is the normal first experience, and it is not a mistake in the
commands.

A computer learns its group memberships when it authenticates, which
happens at boot. Adding `ADFS01$` to a group while ADFS01 is running does
not tell ADFS01. **Reboot it**, then test again.

This catches people with security groups generally, not just gMSA. If you
add a *user* to a group, they must log out and back in for the same reason.
:::

## Point AD FS at it

```powershell
# The $ suffix tells Windows this is a managed account with no password
# to supply. That absence is the entire point.
Set-AdfsProperties -ServiceAccount "LAB\gmsa-adfs$"
```

In practice, changing the service account of a running AD FS farm is
fiddly, and the supported path is often to specify the gMSA when the farm
is first created:

```powershell
# What lesson 8.3 would have looked like with a gMSA from the start.
Install-AdfsFarm `
    -CertificateThumbprint "<thumbprint>" `
    -FederationServiceName "sso.lab.internal" `
    -GroupServiceAccountIdentifier "LAB\gmsa-adfs$"
```

Lesson 8.3 used an ordinary account on purpose, so that this lesson has
something to replace and you feel the difference. In a real build you
would use the gMSA from the outset, and the fact that you cannot easily
retrofit one is itself worth knowing before you build something you care
about.

:::tip[Least privilege]
This is the principle taken as far as it goes: a credential no human has
ever seen and no human can produce.

Trace the thread through the course. Lesson 5.6 gave you two accounts so
your everyday session held no privilege. Lesson 6.3 stopped root logging in
at all. Lesson 7.2 switched the root CA off. Lesson 6.9 opened a database
read-only. Every one of them asks the same question: what could somebody do
with this if they had it, and can they hold less?

A gMSA answers it by removing the thing entirely. There is no password to
phish, to reuse, to find in a runbook, or to take to a new employer.
:::

## Where you'll meet this

gMSAs are the correct answer for AD FS, SQL Server, IIS application pools,
scheduled tasks, and most Windows services that need a domain identity.
Interviews ask about them because they separate people who have run a
Windows estate from people who have read about one.

The concept generalises well beyond Windows. Managed identities in cloud
platforms, instance roles, and workload identity in Kubernetes are all the
same idea: the platform supplies a short-lived credential to a workload it
has already authenticated, so no long-lived secret has to exist. If you
understand why a gMSA is better than `svc-adfs`, you understand why those
exist too.

## Make it yours

1. Try to read the gMSA's password. There is no supported way, and
   confirming that for yourself is the lesson.
2. Check when it last rotated:
   `Get-ADServiceAccount gmsa-adfs -Properties PasswordLastSet`
3. Write in your journal what would have to happen to rotate `svc-adfs`
   safely, listing every system that would need changing and in what
   order. That list is why service account passwords never get rotated,
   and writing it out is more persuasive than any argument for gMSA.

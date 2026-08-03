---
title: "5.8 Add a second domain controller"
sidebar_position: 8
---

# 5.8 Add a second domain controller

Everything in your domain currently depends on one virtual machine. If
DC01 stops, nobody logs in, no name resolves, no group policy applies, and
your lab is a set of unrelated computers again.

That's not a lab problem. It's the reason essentially every organization
running Active Directory runs at least two domain controllers, and it's
one of the first things an auditor or a new hire checks. A single DC is a
single point of failure for the thing every other system authenticates
against.

So today you build DC02, and then you spend two lessons on what having it
actually buys you: replication, the roles that only one DC can hold, and
what happens when you switch the first one off on purpose.

:::note[Tier 1 does this too]
DC02 needs 3 GB, but it spends most of the course **powered off**. You
only need it running for this lesson, 5.9, and 5.10. Shut it down
afterwards and your everyday memory use goes back to what it was before,
which is the same habit Module 7 uses for the offline root CA.
:::

## Build the machine

Same as DC01 in Module 3, with three differences:

- **Name it `DC02`** during Windows setup.
- **3 GB of RAM**, the same as DC01, and 60 GB of disk.
- **Static address `10.10.10.11`**, from the addressing plan you wrote in
  lesson 4.3.

Take Desktop Experience again, for the same reason as lesson 5.2.

:::tip[What production would do differently]
A lot of real second domain controllers run **Server Core**: no desktop,
no Server Manager, managed entirely over PowerShell and remote consoles.
It uses roughly half the memory and has a much smaller attack surface,
because software that isn't installed can't be exploited.

Lesson 5.2 had you take Desktop Experience because Core is a hard place to
*learn*. That reasoning still holds, so DC02 gets a desktop here too. But
now you know what the other option was for, and if you rebuild this lab
later, making DC02 Core is a genuinely good exercise.
:::

## The one setting people get wrong

Before promoting, **DC02's DNS server must point at DC01**, not at itself
and not at your router.

```powershell
# Run on DC02. Substitute your interface name if it differs;
# Get-NetAdapter will tell you what it's called.
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" `
                           -ServerAddresses 10.10.10.10
```

Confirm it can find the domain before going further:

```powershell
# Should return DC01. If this fails, promotion will fail too,
# and the wizard's error will be much less clear than this one.
Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.lab.internal
```

This is lesson 5.1's point arriving as a practical consequence. A machine
joining a domain finds it through DNS, so a server that can't resolve the
domain's SRV records cannot join it, no matter how correct everything else
is. It is the single most common cause of a failed promotion.

## Promote it, as code this time

Lesson 5.4 said the shape of this course is *GUI to learn, script to
repeat*. You've read every screen of the promotion wizard once. This is
the repeat.

```powershell
# 1. Same role as DC01, same command.
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools

# 2. This is the different one. DC01 used Install-ADDSForest, because
#    it was creating a forest that didn't exist. DC02 is JOINING a
#    domain that already exists, so the cmdlet is different.
#
#    -InstallDns puts a DNS server on this machine too, so the domain
#    has two. -Credential asks who you are, because unlike DC01 this
#    operation has to be authorised by the existing domain.
Install-ADDSDomainController -DomainName "lab.internal" `
                             -InstallDns `
                             -Credential (Get-Credential "LAB\Administrator")

# 3. It prompts for a DSRM password, exactly as the wizard did for
#    DC01, and then reboots itself.
```

Expect it to ask for the domain Administrator password, then a DSRM
password. **Write DC02's DSRM password in your journal too**, labelled
separately from DC01's. They are per-machine, not per-domain, and
discovering that during a recovery is a bad time to learn it.

The reboot takes a while. It is copying the entire directory across.

## Confirm you have two

Log back in as `LAB\Administrator`, and from **either** DC:

```powershell
# Every domain controller in the domain, with its address and site.
Get-ADDomainController -Filter * |
    Select-Object Name, IPv4Address, Site, IsGlobalCatalog
```

You should see two rows, `DC01` and `DC02`, both in `Default-First-Site-Name`,
both showing `True` for global catalog.

That last column is worth a sentence. A **global catalog** holds a partial
copy of every object in the forest, which is what lets a login be answered
without walking off to another domain. Windows makes additional DCs global
catalogs by default, and that default is correct for a single-domain
forest like yours.

Now the health check, which is the tool you'll reach for whenever a domain
misbehaves:

```powershell
# Run on DC02. It tests dozens of things and is verbose on purpose.
dcdiag /c
```

Read the summary at the bottom rather than the wall above it. You want
`passed test` on the entries that name DC02. Some warnings are normal in a
lab, particularly anything about time sources or about DNS delegation,
which is the same delegation warning lesson 5.4 told you to expect.

## Point the domain at both

One loose end. DC02's DNS still points only at DC01, which means if DC01
is down, DC02 cannot resolve names, including its own domain's. Fix both
machines so each prefers itself and falls back to the other:

```powershell
# On DC01
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" `
                           -ServerAddresses 10.10.10.10,10.10.10.11

# On DC02
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" `
                           -ServerAddresses 10.10.10.11,10.10.10.10
```

There is a long-running argument among Windows administrators about
whether a DC should list itself first or second. The version above is
readable and works. What genuinely matters is that **neither machine
depends only on the other**, because that is how you get a domain that
cannot start after a power cut.

Update your addressing note from lesson 4.3 with DC02, and shut DC02 down
until the next lesson if you're tight on memory.

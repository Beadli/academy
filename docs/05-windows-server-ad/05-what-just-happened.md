---
title: "5.5 What just happened: the database, DNS, and Kerberos"
sidebar_position: 5
---

# 5.5 What just happened: the database, DNS, and Kerberos

A wizard ran for four minutes and rebooted your server. Underneath, it
created a directory database, built a DNS zone, generated a set of
cryptographic keys, and turned your machine into an authentication
authority. This lesson opens each of those up, because a domain
controller you can inspect is a domain controller you can fix.

## The directory exists

Open **Active Directory Users and Computers**. Windows administration
tools have short names ending in `.msc`, and there are three ways to
reach any of them, all worth knowing:

- Press the **Windows key**, start typing the tool's name, and press
  Enter when it appears.
- Press **Windows key + R** for the Run box, type the short name
  (`dsa.msc` for this one), and press Enter. This is the fast way, and
  it's how you'll see experienced admins do it.
- In **Server Manager**, use the **Tools** menu, which lists everything
  installed.

Any of them opens the same console. This is the one administrators have
used for a quarter of a century, and you'll spend real time in it.

Expand `lab.internal` and look at what the promotion created for
you:

- **Builtin** and **Users**: containers holding the accounts and groups
  every domain starts with, including `Administrator`, `Domain Admins`,
  and `Domain Users`.
- **Computers**: where machines land by default when they join.
- **Domain Controllers**: an *organizational unit*, and note that it's
  a different icon from the containers above. Your DC01 is in it. That
  difference matters in lesson 5.7.

The same view as a query, which is where this is heading:

```powershell
# Every user in the directory. -Filter * means "no filter, all of them".
Get-ADUser -Filter *

# The domain itself: its name, its functional level, its DCs.
Get-ADDomain

# And the machine you're standing on, in its new role.
Get-ADDomainController
```

## DNS exists, and it's yours now

Open **DNS Manager** (`dnsmgmt.msc`) and expand your server, then
**Forward Lookup Zones**, then `lab.internal`.

Look for a folder called `_tcp`, and inside it records named things like
`_ldap` and `_kerberos`. Those are **service records**, and they are the
mechanism from lesson 5.1: they're how any machine on this network finds
out that DC01 provides authentication for this domain. The promotion
wrote them about itself.

Check your own DNS settings changed too:

```powershell
# The promotion should have pointed this machine's DNS at itself,
# which is correct now that it IS the DNS server. Expect 127.0.0.1
# or 10.10.10.10.
Get-DnsClientServerAddress -InterfaceAlias "Ethernet0"

# Ask the directory's DNS for its own service records.
Resolve-DnsName -Type SRV _ldap._tcp.lab.internal
```

If DNS is still pointing at your gateway, set it to the machine itself
now. A domain controller that asks someone else about its own domain is
a fault waiting to happen:

```powershell
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" `
                           -ServerAddresses 127.0.0.1
```

Internet names still resolve, by the way, because your DNS server
forwards anything it isn't authoritative for. Check **Forwarders** in
the DNS Manager properties to see where it sends them. If internet
names *don't* resolve from this machine, that forwarder list is the
first place to look.

:::note[Tier 2: tell your firewall about the domain]
Lesson 4.5 promised you'd come back for this, and here it is. FW01 is
handing out DNS settings to everything on your LAN, and it's currently
telling them to use a resolver that has never heard of
`lab.internal`. Any machine that takes that answer will be able to
browse the internet and unable to join your domain, which is exactly the
confusing failure lesson 5.1 warned about.

In the OPNsense web interface, go to **Services > ISC DHCPv4 > [LAN]**
(or the Dnsmasq/Kea equivalent your version uses) and set the **DNS
servers** handed out to `10.10.10.10`. Save and apply.

DC01 itself is unaffected, because you gave it a static address and it
now points at itself. This is for UBNT01 in Module 6 and every machine
after it.
:::

## Kerberos exists, and you're holding a ticket

You logged in a minute ago, so the authentication you read about in 5.1
has already happened to you. Look at the evidence:

```powershell
# The Kerberos tickets currently cached for your session.
klist
```

Among the entries you should find one for `krbtgt/LAB.INTERNAL`.
That's your **ticket-granting ticket**, the thing the domain controller
issued when it verified your password. Here's the model in three
sentences:

You proved who you are once, at login, and got a TGT. When you connect
to a service, your machine quietly presents the TGT and asks for a
ticket for that specific service. The service checks the ticket and lets
you in, and at no point did your password go anywhere near it.

That's single sign-on, and it's the same mechanism underneath the fancier
web version you'll build in Module 8. Note the ticket's expiry time in
that output: tickets are deliberately short-lived, which is why a
disabled account stops working across an organization within hours
rather than instantly. Knowing that lag exists is the kind of detail
that separates an answer from a good answer in an interview.

## Why the clock matters more than you'd think

One more thing Kerberos cares about, and it bites lab users specifically.

Tickets are stamped with times, and to stop an attacker replaying an old
one, every machine checks that the times are close to its own. The
default tolerance is **five minutes**. Beyond that, authentication
fails, and it fails with messages that don't obviously say "your clock
is wrong."

In a real domain this is handled for you: the domain controller is the
time authority and members sync to it. In a lab it goes wrong for a
reason production doesn't have. **Virtual machines that were suspended,
snapshotted, or left powered off for a week come back with the wrong
time.** Come back to your lab after a break, find you can't
authenticate, and this is the first thing to check.

```powershell
# What does this machine think the time is?
Get-Date

# Force a resync and report what happened.
w32tm /resync
w32tm /query /status
```

Add it to your mental checklist: if authentication breaks after your lab
has been off for a while, check the clocks before you check anything
else. It costs ten seconds and it's the answer more often than it has
any right to be.

## Where the database actually lives

For completeness, because people ask: the directory is a database file
called `ntds.dit`, in `C:\Windows\NTDS`, and you cannot open or copy it
while the service is running. Every password hash in your domain lives
in that file, which is why domain controllers are the crown jewels, why
their backups are as sensitive as they are, and why Module 14 spends
its time trying to reach exactly this machine.

Don't go poking at it. Do remember it's there.

---
title: "5.12 Take over DHCP from your hypervisor"
sidebar_position: 12
---

# 5.12 Take over DHCP from your hypervisor

There has been a DHCP server on your lab network since Module 4, and you did
not configure it, cannot log into it, and have never seen its settings. It is
your hypervisor, quietly handing out addresses to anything that asks.

That was the right thing to lean on while you had nothing else. It stops being
the right thing the moment you have a domain, for a reason lesson 5.5 already
made you live with: **the hypervisor has never heard of `lab.internal`.** It
hands out a DNS server that cannot find your domain, so every machine that
takes an address from it can browse the internet and cannot join the domain.

Today you take the job away from it.

:::note[Tier 2: you already did this, in a different place]
FW01 has been your DHCP server since lesson 4.5, and in 5.5 you told it to
hand out `10.10.10.10` as the DNS server. Your addressing is already correct
and there is nothing to fix.

**Read the lesson anyway**, and skip the commands. The reasoning about
authorisation, scope options and cutover is the same wherever the service
runs, and the closing section on where DHCP belongs in a real network is the
part worth having an opinion about in an interview.
:::

## This is a migration, not an installation

Worth being clear about the shape before you start, because it changes how you
work.

You are not adding a service to a network that lacks one. You are **replacing
a running service that things depend on**, which is most of what infrastructure
work actually is. Nobody gets to build greenfield very often. What they get is
a thing that already works, owned by something they want to stop depending on,
and a requirement to swap it without an outage.

That shape has a standard order, and it is the order below: build the
replacement while the old one still runs, cut over deliberately, verify, and
know how to go back.

## Step 1: Install the role

On DC01:

```powershell
# The DHCP Server role, plus the management tools. Without
# -IncludeManagementTools you get the service and none of the commands
# used in the rest of this lesson.
Install-WindowsFeature -Name DHCP -IncludeManagementTools
```

**How you know it worked:** the command reports `Success : True` and an
`ExitCode` of `Success` or `SuccessRestartRequired`.

```powershell
# Confirm independently rather than trusting the installer's summary.
Get-WindowsFeature -Name DHCP
```

Expect `Install State : Installed`.

## Step 2: Authorise it in Active Directory

A Windows DHCP server that is domain-joined refuses to hand out a single
address until it has been **authorised in the directory**. This trips people
up constantly: the service is running, the scope is configured, and nothing
gets an address.

```powershell
# Tell the directory this server is allowed to run DHCP.
Add-DhcpServerInDC -DnsName dc01.lab.internal -IPAddress 10.10.10.10
```

```powershell
# How you know it worked: your server is listed.
Get-DhcpServerInDC
```

**This is a security control, and lesson 4.2 already told you why it exists.**
It warned that running a DHCP server carelessly could start answering for
your housemate's laptop and your TV. A rogue DHCP server is one of the
easiest attacks on a local network: answer faster than the real server, and
you decide what gateway and what DNS server every machine uses. Handing out
your own DNS server is how an attacker reads traffic without touching a
router.

Active Directory's answer is that a domain-joined Windows DHCP server checks
the directory for permission before serving. It does not stop a Linux laptop
under a desk from doing it, which is why the network-side answer, DHCP
snooping on a switch, exists too. Knowing both halves is the useful thing.

## Step 3: Build the scope

A **scope** is a range of addresses a DHCP server may hand out, plus the
settings that go with them. Yours was designed in lesson 4.3 and you have
been reserving it ever since: `.100` to `.199`.

**In the console**, which is how most administrators do this the first time:
open **Server Manager**, then **Tools > DHCP**. Expand your server, right-click
**IPv4** and choose **New Scope**. The wizard asks for a name, the start and
end addresses, a subnet mask, then the router and DNS settings in later
steps, which are the same values as the commands below.

**Learn the console even though the commands are faster**, because reading is
a console job. When somebody asks which machine had `10.10.10.137` last
Tuesday, you open this and look at **Address Leases**. There is no satisfying
way to eyeball that from a command line.

Or, as in lesson 5.6, do it in PowerShell, which is what the rest of this
lesson uses because it is copy-pasteable and every step can be verified:

```powershell
# The range. Everything below .100 stays reserved for machines you
# address by hand, exactly as the plan in 4.3 says.
Add-DhcpServerv4Scope -Name "Lab clients" `
                      -StartRange 10.10.10.100 `
                      -EndRange 10.10.10.199 `
                      -SubnetMask 255.255.255.0
```

Now the settings that ride along with the address. **These are the whole point
of the exercise**, because this is where the domain's DNS server finally gets
handed out automatically:

```powershell
# -Router is your hypervisor's NAT gateway, which is still doing the
# routing even though it is no longer doing DHCP. Read yours rather than
# copying mine: VMware conventionally uses .2 and VirtualBox .1, and
# lesson 4.3 told you to check it on the machine.
Set-DhcpServerv4OptionValue -ScopeId 10.10.10.0 `
                            -DnsServer 10.10.10.10 `
                            -Router 10.10.10.2 `
                            -DnsDomain lab.internal
```

```powershell
# How you know it worked. Expect three options listed: 003 Router,
# 006 DNS Servers, 015 DNS Domain Name.
Get-DhcpServerv4OptionValue -ScopeId 10.10.10.0
```

**Those numbers are worth recognising.** DHCP options are numbered, the
numbers are the same on every DHCP server ever made, and option 6 is the one
this entire lesson exists for. When you meet a firewall, a router or a cloud
service handing out network settings, it is the same option 6.

## Step 4: Cut over

Right now you have two DHCP servers on one network. **That is the state
lesson 4.3 called a coin flip that lands differently every boot**, and it is
worth being in it for exactly as long as it takes to read this paragraph.

Turn the hypervisor's DHCP off, on the same network you edited in 4.3:

- **VMware Workstation:** Edit > Virtual Network Editor, select the NAT
  network, and untick **Use local DHCP service to distribute IP addresses**.
  Leave everything else alone. The NAT device keeps routing.
- **VirtualBox:** Network Manager, your NAT network, untick **Supports DHCP**.

**Do not skip this and hope.** Two DHCP servers do not produce an error
anywhere. They produce machines that work on Tuesday and fail on Wednesday,
which is a far worse problem than an outage because nobody can reproduce it.

## Step 5: Prove it, with the only client you have

Here is something worth noticing before you test: **you have no DHCP clients
left.** DC01, DC02 and UBNT01 are all statically addressed, and you pinned
KALI01 in lesson 4.4 precisely so that later lessons could refer to it by
address. Everything on your network has a fixed address, which means nothing
is currently proving your new server works.

So borrow KALI01 for two minutes. On KALI01:

```bash
# Put it back on DHCP temporarily. Substitute your connection name
# from lesson 4.4 if it differs.
sudo nmcli con mod "Wired connection 1" ipv4.method auto
sudo nmcli con up "Wired connection 1"
```

```bash
# What did the new server give it?
ip -brief addr
cat /etc/resolv.conf
```

**How you know it worked**, and this is the moment the whole lesson pays off:
an address between `10.10.10.100` and `.199`, and a DNS server of
`10.10.10.10`. Not the hypervisor's resolver. Your domain controller.

Prove that means something:

```bash
# A name only your domain knows. This could not have worked
# an hour ago.
nslookup dc01.lab.internal
```

Then put KALI01 back where lesson 4.4 left it:

```bash
sudo nmcli con mod "Wired connection 1" ipv4.method manual
sudo nmcli con up "Wired connection 1"
```

And confirm the lease was really issued by your server, from the server side:

```powershell
# On DC01. Expect KALI01's temporary lease, or an empty list if you
# have already released it.
Get-DhcpServerv4Lease -ScopeId 10.10.10.0
```

## What you just made load-bearing

DC01 now hands out addresses as well as answering directory and DNS queries.
That is normal in real networks and it has a consequence this course has been
telling you to create since Module 0: **you power machines off to save
memory.**

Power DC01 off now and a machine that boots gets no address at all. Before, it
would have got one from the hypervisor and merely failed to find the domain.
You have traded a confusing partial failure for an obvious total one, which is
usually the better trade, but it is a trade and you should know you made it.

**Write it in your journal**, with the addressing plan: DHCP now lives on
DC01, and DC01 being off means no new leases.

In a production network the answer to this is a second DHCP server splitting
the scope, or a failover relationship between two of them. You have DC02, and
that is a genuinely good exercise once this one works.

## Where DHCP belongs, and what the answer tells you

You now have it on a domain controller. Tier 2 readers have it on a firewall.
**Both are correct**, and which one an organisation has chosen tells you
something about it.

**On the firewall** is common in smaller networks. One box does routing,
addressing and filtering; there is one place to look and one thing to keep
running.

**On Windows servers** is usual once a network gets big enough to care about
who had which address at 3am last Tuesday. Windows DHCP logs leases, integrates
with the directory for authorisation, and can register client names in DNS
automatically, which matters when your monitoring is trying to tell you which
machine did something.

The question an interviewer is really asking, when they ask where you put
DHCP, is whether you know it is a decision at all.

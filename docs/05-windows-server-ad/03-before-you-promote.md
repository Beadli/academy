---
title: "5.3 Before you promote: name, address, and the clock"
sidebar_position: 3
---

# 5.3 Before you promote: name, address, and the clock

Three jobs, and the order matters. A domain controller writes its own
name and address into the directory and into DNS when it's promoted.
Change either afterwards and you're editing records in several places
and cleaning up what you missed for weeks. Do them now and it's two
commands.

## Name it

Windows generated something like `WIN-4F9K2L1QZ3A` at install. Give it
the name your addressing plan already uses.

```powershell
# -Restart reboots immediately, because the name change needs it.
Rename-Computer -NewName DC01 -Restart
```

Log back in and confirm it took:

```powershell
hostname
```

## Address it

Your plan says `10.10.10.10`, static. Static because everything in the
lab is about to depend on finding this machine, and a server whose
address can change is a server that will change its address at the worst
possible moment.

You need two pieces of information first: the name Windows gave the
network adapter, and your gateway.

```powershell
# The adapter's name, usually "Ethernet" or "Ethernet0".
Get-NetAdapter

# Your current address and gateway, handed over by DHCP.
Get-NetIPConfiguration
```

:::warning[Your gateway depends on your tier. Read it, don't assume it.]
This is the one place in the module where Tier 1 and Tier 2 genuinely
differ, and copying the wrong address leaves you with a server that can't
reach anything.

- **Tier 2**, you built FW01 in lesson 4.5, and your gateway is
  **`10.10.10.254`**.
- **Tier 1**, you have no firewall. Your gateway is the hypervisor's own
  NAT device, and the address depends on your hypervisor: VMware and
  VirtualBox use different conventions, as lesson 4.2 explained.

**Don't guess either way.** The `Get-NetIPConfiguration` output above
already tells you, on the `IPv4DefaultGateway` line. That is the number to
use below.
:::

Capture it in a variable so the rest of this lesson is correct for both
tiers, and so you're reading your machine's actual configuration rather
than trusting a printed address:

```powershell
# Substitute your adapter name from Get-NetAdapter above.
$adapter = "Ethernet0"

# Read the gateway DHCP gave you, rather than assuming it.
$gw = (Get-NetIPConfiguration -InterfaceAlias $adapter).IPv4DefaultGateway.NextHop

# Print it and sanity-check it before going further. Tier 2 should see
# 10.10.10.254. Tier 1 will see whatever your hypervisor uses.
$gw
```

If `$gw` comes back empty, this adapter never got a DHCP lease. Fix that
before continuing, because everything below depends on it.

Now set the static address:

```powershell
# A fixed address for this machine. -PrefixLength 24 is the /24
# from lesson 4.1.
New-NetIPAddress -InterfaceAlias $adapter `
                 -IPAddress 10.10.10.10 `
                 -PrefixLength 24 `
                 -DefaultGateway $gw

# DNS, for now, is whatever can resolve internet names so the server
# can reach Windows Update. Point it at your gateway. The promotion
# in 5.4 changes this to the machine itself, which is correct once
# it IS the DNS server.
Set-DnsClientServerAddress -InterfaceAlias $adapter `
                           -ServerAddresses $gw
```

:::warning[You may lose the console for a second]
If you're working through a remote session the address change will drop
it. You're at the VM's own console, so you'll be fine, but the same
command on a real remote server is how people lock themselves out of
machines in datacenters they can't drive to.
:::

Verify all four answers from lesson 4.1, from the Windows side:

```powershell
# Address, mask, gateway and DNS in one view.
Get-NetIPConfiguration

# And prove it works, one rung at a time. This is the ladder from
# lesson 4.4: can I reach my gateway, can I reach the internet by
# address, can I resolve a name.
ping $gw
ping 1.1.1.1
Resolve-DnsName ubuntu.com
```

If `$gw` has been lost because you opened a new PowerShell window, read it
again with the same command as before:

```powershell
$gw = (Get-NetIPConfiguration -InterfaceAlias "Ethernet0").IPv4DefaultGateway.NextHop
```

## Check the clock, and push it back

Module 3 promised this. Your evaluation is running, and Windows will
tell you exactly where it stands.

```powershell
# License status and the days remaining on the evaluation.
slmgr /dli
```

That opens a dialog box rather than printing to the shell, which
surprises people the first time. Read the remaining days.

When the number gets uncomfortable, reset it:

```powershell
# Resets the evaluation period. Reboot afterwards.
slmgr /rearm
```

Two honest caveats. The number of times you can rearm is limited rather
than infinite, so this stretches a single install well past a year but
not forever. And an evaluation that fully expires starts shutting the
server down on a schedule, which is unmistakable and easily mistaken for
a fault.

Set yourself a reminder for a few months out, or better, note the
install date in your journal now and check `slmgr /dli` whenever you
come back to the lab after a break. By the time it matters you'll be
able to rebuild this machine in an evening, and Module 10 will rebuild
it for you.

## One last thing before promoting

Give the machine a moment to be a normal server: let Windows Update run
if it wants to, and take a **snapshot** and call it
`pre-promotion`. Lesson 3.5 was practice for exactly this. The promotion
is a one-way door in the sense that undoing it properly is fiddly, and
a snapshot turns "I answered a wizard wrong" from an evening into a
minute.

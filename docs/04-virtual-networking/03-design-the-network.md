---
title: "4.3 Design your lab network, then build it"
sidebar_position: 3
---

import Module4Networks from '@site/static/img/module4-networks.svg';

# 4.3 Design your lab network, then build it

Real networks are designed on paper before anything is plugged in, and
the design is written down somewhere people can find it. Labs that skip
this end up with machines nobody can locate and addresses nobody
remembers choosing. Ten minutes now, and your lab has an addressing plan
you'll still be able to read in Module 17.

Here are the two shapes this module builds, side by side:

<Module4Networks role="img" aria-label="Two panels. Tier 1: a single hypervisor NAT network on 10.10.10.0/24 holding KALI01 now and DC01 and UBNT01 in later modules, with the hypervisor providing gateway and DHCP. Tier 2: an outer WAN segment on the hypervisor NAT network holding KALI01, an OPNsense firewall FW01 at 10.10.10.254 in the middle with inbound denied and outbound allowed, and an inner host-only LAN segment on 10.10.10.0/24 holding the domain machines." style={{width: '100%', height: 'auto'}} />

## The plan

Every machine in this course lives on **`10.10.10.0/24`**. That's the
lab LAN, and it's the same address range whichever tier you're on, so
every command and screenshot in every later module matches your screen.

| Address | Machine | Arrives in |
|---|---|---|
| `10.10.10.1` | your own computer's adapter on this network, claimed by the hypervisor | already there |
| `10.10.10.10` | DC01, domain controller and DNS | Module 5 |
| `10.10.10.20` | UBNT01, Docker and Ansible host | Module 6 |
| `10.10.10.30` | SUBCA01, issuing certificate authority (Tier 2) | Module 7 |
| `10.10.10.40` | ADFS01, single sign-on (Tier 2) | Module 8 |
| `10.10.10.100` to `.199` | DHCP pool, for anything that doesn't need a fixed address | this module |
| `10.10.10.254` | FW01, the firewall and gateway (Tier 2 only) | this module |

Servers get the low numbers, statically. The pool starts at `.100` so
there's no chance of DHCP handing out an address you've already nailed
to a server, which is a real outage in real companies and an afternoon
of confusion in a lab.

The firewall sitting at `.254` rather than `.1` is worth a word, because
`.1` is the more common convention. Your hypervisor claims `.1` for your
own computer's adapter on this network, and two devices answering to one
address is the kind of fault that wastes an evening. Plenty of real
networks put the gateway at the top of the range for their own reasons,
so this is a convention you'll meet in the wild rather than a lab
compromise.

**Tier 2 adds a second segment.** Kali and the firewall's outside
interface live there, on whatever range your hypervisor's NAT network
uses. You don't need to control that one; it stands in for "the
internet" and the only thing that matters is that it's a different
network from `10.10.10.0/24`.

Copy that table into your journal now, under a heading like "lab
addressing plan." You will look it up more than any other note you take
in this course.

:::tip In cloud terms
This is the same exercise cloud engineers do before creating anything.
Your `10.10.10.0/24` is a **subnet** inside what Azure calls a **virtual
network**; the firewall you're about to build does the job of a **network
security group** plus a route table; and the plan you just wrote is what
gets encoded into a deployment template. The vocabulary is different, the
thinking is identical, and doing it here means the cloud version is
familiar rather than new.
:::

## Build it: Tier 1

One network, run by the hypervisor, with internet through NAT. You're
going to change its address range to match the plan.

In VMware Workstation, open **Edit > Virtual Network Editor**. On
Windows you'll need to click a button to get administrator rights before
anything is editable; on Linux the tool is `vmware-netcfg` and wants
`sudo`.

1. Select the NAT network, usually named **VMnet8**.
2. Set its subnet address to `10.10.10.0` and its mask to
   `255.255.255.0`.
3. Leave **Use local DHCP service** ticked. VMware will hand addresses
   to anything that asks.
4. Open the DHCP settings and set the range to `10.10.10.100` through
   `10.10.10.199`, matching your plan.
5. Apply, and let it restart the network.

Your gateway on this network is the NAT device VMware runs, and by
convention it takes `10.10.10.2`. Don't take my word for it: after the
next lesson boots a VM, run `ip route` and read the address on the
`default` line. Reading the answer off the machine beats trusting any
document, including this one.

:::info VirtualBox difference
Use **File > Tools > Network Manager**, the **NAT Networks** tab, and
create one named `lab-nat` with the range `10.10.10.0/24`. Tick
**Supports DHCP**. VirtualBox's gateway convention is `.1`, so read
yours from `ip route` rather than assuming either number.
:::

## Build it: Tier 2

Two networks, with a firewall between them. The outer one is NAT, the
inner one is host-only, and nothing on the inner network reaches the
internet except through the firewall you'll build in 4.5.

1. **The outer segment.** Leave VMnet8 (NAT) exactly as VMware set it
   up, on whatever range it chose. Note that range down; it's your WAN
   side. Leave its DHCP on.
2. **The inner segment.** Add a host-only network, typically the next
   free one such as **VMnet2**. Set its subnet to `10.10.10.0` and mask
   `255.255.255.0`.
3. **Turn its DHCP off.** This is the step people miss, and the symptom
   is horrible: machines get addresses from the wrong server
   intermittently, and half your lab works. Your firewall is going to
   be the DHCP server for this segment, and two DHCP servers on one
   network is a coin flip that lands differently every boot.
4. **Leave "connect a host virtual adapter to this network" ticked.**
   That's what puts your own computer on `10.10.10.1`, and it's how
   you'll reach the firewall's web interface in 4.5 without needing
   another VM to browse from.

:::info VirtualBox difference
Make the outer segment a **NAT Network** as above, and the inner one a
**Host-only Network** in the same Network Manager, set to
`10.10.10.0/24` with its **DHCP Server disabled** on the host-only tab.
:::

## Write it down

Add to your journal, under the addressing plan: which hypervisor network
name is which segment (`VMnet8` = outer, `VMnet2` = lab LAN, or your
VirtualBox equivalents), and whether their DHCP is on or off. In six
weeks, when a machine won't get an address, this note is the first thing
you'll read and it'll usually contain the answer.

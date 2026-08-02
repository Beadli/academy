---
title: "4.2 The hypervisor's network modes"
sidebar_position: 2
---

# 4.2 The hypervisor's network modes

Your hypervisor can build virtual switches, and every VM's network card
plugs into one of them. Which switch you choose decides who that machine
can talk to. There are four modes, the names differ slightly between
VMware and VirtualBox, and choosing wrongly is the single most common way
a home lab ends up confusing.

## NAT

The VM sits on a private network the hypervisor invents, and the
hypervisor translates its traffic so it can reach the internet using your
computer's own connection. The VM can start conversations outward.
Nothing on your home network can start one inward.

This is what your practice VM used in Module 3, which is why it had
internet without you configuring anything, and why its address came from
a DHCP server you never installed.

**Use it for:** anything that needs the internet but shouldn't be
reachable from your house. In this lab, that's the outer edge.

## Host-only

A private switch with no route to the internet at all. VMs plugged into
it can talk to each other and to your computer, and that's the entire
world. Isolation is the feature.

**Use it for:** the segment where your domain lives, if you're on Tier 2
and putting a firewall in front of it. The firewall then becomes the only
door out, which is the whole point of building one.

## Internal (VirtualBox) or a custom non-NAT network (VMware)

Like host-only, but even your own computer can't see it. Total isolation
between the VMs and everything else.

**Use it for:** malware analysis, and eventually a detonation segment if
you go that direction. Not needed in this course.

## Bridged, and why the course avoids it

Bridged mode puts the VM directly onto your real home network, as if you
had plugged a second physical computer into your router. It gets an
address from your home router and your phone can ping it.

It's the mode beginners reach for because it feels simplest, and this
course does not use it. Three reasons, none of them theoretical:

- **You're about to run a DHCP server.** Later in this module and again
  in Module 5, machines in your lab start handing out addresses. On a
  bridged network they'd hand them to your housemate's laptop and your
  TV. Rogue DHCP is a genuinely miserable thing to diagnose from the
  other side.
- **You're about to run deliberately vulnerable things.** A Kali box and
  an unpatched Windows Server belong behind a boundary, not on the same
  network as the family iPad.
- **Your lab stops being portable.** Bridged means the lab's addressing
  depends on whatever router it's near. Take the laptop to a café and
  nothing works. NAT and host-only travel with you.

If you later have a reason to bridge a machine deliberately, you'll know
why you're doing it. Until then, don't.

:::info VirtualBox difference
The names map almost directly: NAT Network, Host-only Adapter, Internal
Network, Bridged Adapter. One trap worth knowing: VirtualBox offers both
**NAT** and **NAT Network**. Plain "NAT" gives each VM its own private
translation with no way for VMs to talk to each other, which will quietly
break your lab. Use **NAT Network**, which is a shared switch, wherever
this course says NAT.
:::

## Promiscuous mode, for later

By default a virtual switch shows each VM only the traffic addressed to
it. That's normally what you want, and it becomes a problem exactly once:
in Module 12, when a Suricata sensor needs to see everyone's traffic in
order to inspect it. Letting it do that is called promiscuous mode.
VirtualBox has a dropdown for it; VMware needs a configuration file edit.

You don't need it yet. You need to know the term, so that when a sensor
sees nothing you know which knob was never turned.

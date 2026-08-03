---
title: "0.3 The lab you'll build"
sidebar_position: 3
---

import LabArchitecture from '@site/static/img/lab-architecture.svg';

# 0.3 The lab you'll build

This course is modeled on a lab I run for real: same architecture, same
services, scaled down to fit on hardware a student can own. Everything you
build here, I operate a bigger version of, which is where the war stories
come from.

Here's the destination, all of it, before we talk about the road:

<LabArchitecture role="img" aria-label="Architecture diagram of the full lab on one laptop: OPNsense firewall splitting a WAN segment (Kali attacker box) from a LAN segment (domain controller, issuing CA, AD FS, offline root CA, Ubuntu Docker host running Wazuh, Grafana and Gitea), with an OpenVAS vulnerability scanner and a Suricata sensor watching both segments, and the domain controller syncing outward to a Microsoft Entra ID cloud directory." style={{width: '100%', height: 'auto'}} />

The tier badges (T1, T2, T3) mark when each piece arrives, and that's
what the rest of this lesson explains.

The lab grows in three tiers. You pick a tier based on the machine you
have, not the machine you wish you had, and the course tells you at the
top of every module which tier it needs.

## Tier 1: Core (a 16 GB laptop)

| VM | What it is | RAM | Usually running? |
|---|---|---|---|
| DC01 | Windows Server, your domain controller and DNS | 3 GB | yes |
| DC02 | A second domain controller | 3 GB | **no**, three lessons only |
| UBNT01 | Ubuntu, running Docker, Ansible, and a trimmed SIEM | 6 GB | yes |
| KALI01 | The attacker box | 2 GB | when you're attacking |

That last column is the one that matters, and it's the difference between
this list looking impossible on a 16 GB laptop and being comfortable.

**A virtual machine only uses memory while it's switched on.** Add those
numbers up and you get 14 GB, which would indeed be too much. But you will
almost never run all four at once. Day to day it's DC01, UBNT01 and
KALI01, which is **11 GB**, and even that overstates it because Kali sits
off unless you're using it.

DC02 exists so you can learn what every real organization does: run more
than one domain controller, so that losing one doesn't stop everybody
working. You build it in Module 5, spend three lessons on replication and
what happens when a controller dies, and then shut it down. It costs you
nothing for the rest of the course.

Get used to powering off what you aren't using. It's the single most
effective thing you can do to make a modest laptop feel adequate, every
module says which machines it needs, and it's also just how people run
labs. The root CA in Module 7 takes the same treatment for a much more
serious reason.

Tier 1 covers most of the course: Active Directory including replication
and the roles only one controller may hold, Linux, Docker, Ansible, basic
detection, basic attacks.

## Tier 2: Enterprise (32 GB)

Adds an OPNsense firewall (1.5 GB) splitting the lab into WAN and LAN
segments, an issuing certificate authority (3 GB), and an AD FS single
sign-on server (4 GB). There's also a root CA, but it spends nearly its
whole life powered off. You build it, it signs your issuing CA, and then
it goes dark. That isn't a compromise to save RAM. Keeping the root
offline is exactly how it's done in production, and the fact that your
laptop forces good practice on you is a happy accident.

## Tier 3: Full homelab (64 GB or a dedicated box)

The rest of it: Suricata sniffing the network, a full SIEM deployment,
OpenVAS vulnerability scanning, Grafana and Prometheus, and a second
network segment worth defending. This is old-desktop territory, and used
office machines with lots of RAM sell cheap. Retired workstations make
better lab boxes than new laptops.

Two of those get their own virtual machines rather than joining the
containers on the Ubuntu host, for different reasons worth
distinguishing. **Suricata** needs its own because of *where it sits*:
it has to see traffic addressed to other machines, which means its own
network cards in a listening mode. **OpenVAS** needs its own because of
*what it is*: vulnerability scanners are heavy, and a scanner living on
a machine it also scans gives you muddled answers. Real organizations
deploy scanners as their own appliances for exactly that second reason.

## Hardware honesty

Some plain talk before you spend money, because lab guides that pretend
everything runs on anything waste everyone's time.

Don't buy hardware yet. Finish this module, measure what you have (that's
checkpoint 0.6), and start on the tier that fits. Upgrade when you *feel*
the ceiling, not before.

RAM is the whole game. The CPU in any laptop from the last decade is fine.
16 GB is the honest minimum for Tier 1. On 8 GB you can read along and run
one or two VMs, but you'll be fighting the machine instead of learning,
and I'd rather you wait than suffer.

A SIEM is the hungriest thing you'll run. Wazuh wants several gigabytes
before you've sent it a single event. This surprises everyone, and it's
why UBNT01 gets the largest allocation in the table above while two
Windows servers make do with 3 GB each.

Disk: an SSD matters more than its size, but plan on roughly 180 GB free
for Tier 1 once VMs and ISOs pile up. Disk is where the second domain
controller does cost you something real: unlike memory, a powered-off VM
still occupies its whole virtual hard disk. If you're tight, that's the
one to build last.

One hard limitation: **Apple Silicon Macs (M1 through M4) can't take this
course past the Linux parts.** The lab depends on x86 Windows Server VMs,
and those don't run on ARM Macs in any way I can recommend to a beginner.
An Intel Mac, any Windows laptop, or any Linux box is fine. I don't enjoy
writing that paragraph, but you deserve to know before lesson one rather
than during Module 5.

Software cost: zero. Windows Server runs on free 180-day evaluation
licenses (Module 3 shows you how to live with that clock), and everything
else is open source or free for personal use.

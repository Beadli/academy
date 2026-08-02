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

| VM | What it is | RAM |
|---|---|---|
| DC01 | Windows Server, your domain controller and DNS | 4 GB |
| UBNT01 | Ubuntu, running Docker, Ansible, and a trimmed SIEM | 6 GB |
| KALI01 | The attacker box | 3 GB |

Around 13 GB of guests, which fits on a 16 GB machine as long as you're
not also running forty browser tabs. Tier 1 covers most of the course:
Active Directory, Linux, Docker, Ansible, basic detection, basic attacks.

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
before you've sent it a single event. This surprises everyone.

Disk: an SSD matters more than its size, but plan on roughly 150 GB free
for Tier 1 once VMs and ISOs pile up.

One hard limitation: **Apple Silicon Macs (M1 through M4) can't take this
course past the Linux parts.** The lab depends on x86 Windows Server VMs,
and those don't run on ARM Macs in any way I can recommend to a beginner.
An Intel Mac, any Windows laptop, or any Linux box is fine. I don't enjoy
writing that paragraph, but you deserve to know before lesson one rather
than during Module 5.

Software cost: zero. Windows Server runs on free 180-day evaluation
licenses (Module 3 shows you how to live with that clock), and everything
else is open source or free for personal use.

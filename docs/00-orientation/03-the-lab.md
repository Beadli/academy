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

<LabArchitecture role="img" aria-label="Architecture diagram of the full lab on one laptop: OPNsense firewall splitting a WAN segment (Kali attacker box) from a LAN segment holding two domain controllers replicating with each other, an issuing CA, an AD FS server, an offline root CA, and an Ubuntu Docker host running Wazuh, Grafana and Gitea, with an OpenVAS vulnerability scanner and a Suricata sensor watching both segments, and the first domain controller syncing outward to a Microsoft Entra ID cloud directory." style={{width: '100%', height: 'auto'}} />

Three things to read in it before moving on.

**The tier badges (T1, T2, T3)** mark when each piece arrives, and that's
what the rest of this lesson explains.

**Dashed and faded means the machine is usually switched off.** DC02 and
ROOTCA01 are both drawn that way. They're real machines you build and
genuinely use, they just spend most of their lives powered down, for
different reasons: DC02 because it has done its teaching job after three
lessons, ROOTCA01 because an offline root CA that stays online isn't one.

**The double-headed arrow between DC01 and DC02** is replication. It
points both ways deliberately, because neither is a copy of the other:
both are writable, and a change made on either appears on the other within
seconds. Contrast it with the single-headed arrow leaving DC01 for the
cloud, which points one way because your directory is the source of truth
and Entra ID follows it.

That difference is worth carrying: an arrow's direction in this course
always means where authority sits, not merely where data moves.

The lab grows in three tiers. You pick a tier based on the machine you
have, not the machine you wish you had, and the course tells you at the
top of every module which tier it needs.

Each tier **adds to** the one before it. Tier 2 is everything in Tier 1
plus four machines; Tier 3 is everything in Tier 2 plus three more. You
never rebuild, you only extend.

## Tier 1: Core (a 16 GB laptop)

<div className="labTable">

| VM | Role | RAM | On? |
|---|---|---|---|
| DC01 | domain controller, DNS | 3 GB | always |
| DC02 | second DC: replication, FSMO | 3 GB | 3 lessons |
| UBNT01 | Docker, Ansible, trimmed SIEM | 6 GB | always |
| KALI01 | attacker box | 2 GB | as needed |

</div>

**14 GB allocated · 11 GB in normal use**

That last column is the one that matters, and it's the difference between
this list looking impossible on a 16 GB laptop and being comfortable.

**A virtual machine only uses memory while it's switched on.** Add the
numbers up and you get 14 GB, which would indeed be too much. But you will
almost never run all four at once. Day to day it's DC01, UBNT01 and
KALI01, which is 11 GB, and even that overstates it because Kali sits off
unless you're using it.

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

**Everything in Tier 1, plus:**

<div className="labTable">

| VM | Role | RAM | On? |
|---|---|---|---|
| FW01 | OPNsense firewall, WAN/LAN split | 1.5 GB | always |
| SUBCA01 | issuing certificate authority | 3 GB | always |
| ADFS01 | AD FS single sign-on | 4 GB | always |
| ROOTCA01 | offline root CA | 2 GB | once, then off |

</div>

**24.5 GB allocated · around 19 GB in normal use**

The root CA is the one to look at. You build it, it signs your issuing CA,
and then it goes dark for the rest of the course. That isn't a compromise
to save RAM: keeping the root offline is exactly how it's done in
production, and your laptop forcing good practice on you is a happy
accident.

## Tier 3: Full homelab (64 GB or a dedicated box)

**Everything in Tier 2, plus:**

<div className="labTable">

| VM | Role | RAM | On? |
|---|---|---|---|
| SURICATA01 | network sensor, dual NIC | 4 GB | always |
| OPENVAS01 | vulnerability scanner | 4 GB | when scanning |
| TS01 | Tailscale subnet router, remote access | 1 GB | optional |
| UBNT01 | *upgraded*: full SIEM, Grafana, Prometheus | 12 GB | always |

</div>

**Roughly 37 GB allocated**, plus a second network segment worth
defending. Note UBNT01 isn't a new machine here, it just gets more memory
once the SIEM stops being a trimmed one, which is most of the jump.

Treat these four numbers as starting points rather than requirements. By
the time you reach Tier 3 you'll be sizing machines from what you observe
them using, which is the right way round and a skill in itself. The Tier 1
and Tier 2 figures above are the ones I'd hold you to.

This is old-desktop territory, and used office machines with lots of RAM
sell cheap. Retired workstations make better lab boxes than new laptops.

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

### Disk, which surprises more people than RAM

An SSD matters more than its size. But disk is the one budget that only
ever grows, and unlike memory a powered-off VM still occupies every byte
it has written.

Each lesson gives its machine a size when you build it. Collected, so you
can plan:

<div className="labTable">

| VM | Virtual disk | Tier |
|---|---|---|
| DC01 | 60 GB | 1 |
| DC02 | 60 GB | 1 |
| UBNT01 | 60 GB | 1 |
| KALI01 | as the image ships | 1 |
| FW01 | 20 GB | 2 |
| SUBCA01 | 60 GB | 2 |
| ROOTCA01 | 40 GB | 2 |

</div>

**Those are ceilings, not consumption.** Every VM in this course uses
grow-as-used disks, explained in lesson 3.4: the guest believes it has 60
GB, and the file on your laptop starts near zero and grows only as data is
actually written. A freshly built Windows Server occupies something closer
to 15 or 20 GB in practice.

So the arithmetic that matters is not the column above. Budget instead for:

- **Real consumption**, perhaps a third to a half of the allocated figure
  early on, growing as you install things
- **Installer ISOs**, several gigabytes each, and easy to forget because
  they sit in a different folder
- **Snapshots**, which is the one that catches people, and which the next
  paragraph is about

**Roughly 180 GB free for Tier 1** covers all three with room to work.
Tier 2 roughly doubles it. If you're tight, DC02 is the machine to build
last: it costs nothing in memory when powered off, but its disk is
occupied the whole time.

Two habits worth starting immediately: keep VMs and ISOs on the same drive
so you only watch one number, and check that number occasionally rather
than discovering it at 11pm when a VM refuses to start.

One hard limitation: **Apple Silicon Macs (M1 through M4) can't take this
course past the Linux parts.** The lab depends on x86 Windows Server VMs,
and those don't run on ARM Macs in any way I can recommend to a beginner.
An Intel Mac, any Windows laptop, or any Linux box is fine. I don't enjoy
writing that paragraph, but you deserve to know before lesson one rather
than during Module 5.

Software cost: zero. Windows Server runs on free 180-day evaluation
licenses (Module 3 shows you how to live with that clock), and everything
else is open source or free for personal use.

---
title: "Can I start here instead?"
sidebar_position: 5
---

# Can I start here instead?

You have hardware, or the budget for it, and starting on a laptop or
desktop looks like a detour. Reasonable question, and the answer has two
halves.

**Yes, the course runs on this.** No, I don't think a beginner should
start that way.

## Why the course still says "the machine you own"

Not because an ordinary computer is better. Because of what you'd be
debugging.

Building a rack means learning infrastructure **and** commissioning
physical hardware at the same time. When the Proxmox cluster won't form a
quorum, you cannot tell whether that's you misunderstanding quorum, a
switch port in the wrong VLAN, a bad cable, or a firmware setting. Every
problem has two possible layers and no way to isolate them.

On one machine, when something breaks, it's you. That sounds worse and is
much better, because a beginner learns from a failure they can attribute.

There's a second reason, and lesson 3.1 already names it: **when your
screen matches the material, you can tell a mistake from a cosmetic
difference.** Module 3 walks the VMware and VirtualBox interfaces
click-by-click. Proxmox is a different program with different words in
different places. You'd be translating every step while also being
uncertain whether you'd translated correctly.

## What actually diverges

If you go ahead anyway, here's the honest map. Most of the course does not
care what it runs on.

<div className="labTable">

| Module | On a rack |
|---|---|
| 0 Orientation | fine |
| 1 Engineer's toolkit | fine, it's your own machine |
| 2 Scripting | fine |
| **3 Virtualization** | **rewrite it.** Entirely VMware and VirtualBox specific. |
| **4 Networking** | **translate it.** Virtual switches become VLANs on real hardware. |
| 5 Windows Server and AD | fine, it's guest-OS work |
| 6 Linux and Docker | fine |
| 7 PKI | fine |
| 8 onward | fine |

</div>

So two modules of the eight authored need real work from you, and they're
the two that teach the foundations everything else sits on. That's the
cost, stated plainly.

**Addressing is the other divergence.** The course uses a flat
`10.10.10.0/24` with no VLANs. CyberRack uses seven VLANs on `192.168.x`.
Pick one and stay with it. Running the course's addressing inside
CyberRack's VLAN 20 works fine and is probably the least confusing option,
but then the course's `10.10.10.x` addresses appear in a design that
documents `192.168.20.x`, and you'll need to keep that straight yourself.

## What I'd actually do

**Run Module 3 on the machine you already have, then move.**

It's the only module that's genuinely hypervisor-specific, it's one
evening, and it teaches the concepts (virtual disks, snapshots,
grow-as-used, why you size RAM up front) that transfer to Proxmox
unchanged. Delete the practice VM at the end as the module tells you to,
then build the real lab machines on the rack from Module 5 onward.

Module 4 is the interesting one, and I'd do it twice. Once as written, virtually, so you understand what a network segment *is* without cables
in the way. Then again on real hardware, where you'll discover that a
VLAN you configured on the switch and forgot to tag on the trunk behaves
exactly like a cable nobody plugged in. That second pass is worth more
than either alone.

## If you've already bought it

Then none of the above is a reason to leave it in a box. Build it, and
work through the course on it, accepting that Modules 3 and 4 are yours to
adapt.

Just be honest with yourself about which layer you're debugging when
something doesn't work, and keep a VM on your everyday computer available for the moments
when you need to check whether a problem is you or the rack. That single
habit will save you more evenings than any guide.

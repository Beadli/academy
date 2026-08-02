---
title: "Module 3: Virtualization"
sidebar_position: 0
---

# Module 3: Virtualization

Two modules of tooling, and now the payoff starts: by the end of this
one there will be a machine running inside your machine, you'll have
killed it on purpose, and you'll have brought it back from the dead with
one click. That last trick is the single most useful thing in lab work,
and I want you to feel it early.

Virtualization is the technology that makes this whole course possible
on one computer. Instead of six physical servers humming in your closet,
one hypervisor carves your laptop into virtual machines, each one a
complete computer with its own OS, convinced it owns real hardware. Your
domain controller, your Ubuntu host, and your attacker box will all be
guests on the machine you measured in checkpoint 0.6.

What's in it:

- **3.1** what a hypervisor is, and why we're using this one
- **3.2** install VMware Workstation Pro (VirtualBox path included)
- **3.3** where VMs and installers live, collecting and verifying your
  ISOs, and the 180-day clock
- **3.4** build a practice VM and install Ubuntu Server on it
- **3.5** snapshots: break the machine, then undo it
- **3.6** journal entry
- **3.7** checkpoint

A note on how this module treats its VM: the practice machine you build
in 3.4 gets deleted in 3.5, on purpose, after you've wrecked and
restored it. Its job is to teach you the moves without any pressure to
get it perfect. The real, permanent lab VMs start in Module 5, and
you'll build them better for having done a run you knew was disposable.

Tier required: 1. This is where the 16 GB minimum and the disk space
from checkpoint 0.6 start mattering. Budget an evening for install and
downloads (the ISOs are big; start them early and let them run), and a
second evening for the practice VM.

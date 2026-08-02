---
title: "3.1 What a hypervisor is"
sidebar_position: 1
---

# 3.1 What a hypervisor is

A hypervisor is a program that lies to operating systems. It presents
each guest OS with what looks like a computer (a CPU, some RAM, a disk,
a network card) and secretly maps all of it onto slices of your real
hardware. The guest can't tell. Windows Server will boot inside your
laptop genuinely believing it's on a rack somewhere, and that belief is
what the virtualization setting you checked in 0.6 makes efficient: your
CPU has instructions specifically built to keep guests fast and
contained.

Two flavors exist, and the names come up in interviews. A **type 1**
hypervisor runs on bare metal with no OS underneath; that's what runs
enterprise datacenters (VMware ESXi, Proxmox, Hyper-V Server), and my
own lab runs on one. A **type 2** hypervisor runs as an application on
top of your normal OS, which is what you'll use, because your laptop
also needs to stay your laptop.

## Why VMware Workstation Pro

This course standardizes on **VMware Workstation Pro**, and the
reasoning is worth stating rather than asserting. It's free now
(Broadcom dropped the license fee for everyone in late 2024). It's the
desktop sibling of the ESXi/vSphere stack that dominates enterprise
virtualization, so its concepts and vocabulary transfer directly to
what you'll meet at work. And it's what the course's own screenshots
use, which matters for a beginner more than any feature does: when your
screen matches the material, you can tell a mistake from a cosmetic
difference.

**VirtualBox is a fully supported second path.** It's open source, it
runs the same lab, and if you already use it, keep it. Wherever the two
tools genuinely differ, you'll see a callout box like this:

:::info[VirtualBox difference]
Boxes like this one translate the step for VirtualBox users. If there's
no box, the step is the same in both tools apart from cosmetics.
:::

What we're *not* using, and why, since you'll wonder: cloud VMs cost
real money monthly and vanish when you stop paying, while this lab is
yours forever and works on a plane. Hyper-V comes free inside Windows
but can't run the whole course comfortably and its skills transfer less
broadly. Proxmox is wonderful and is the natural next step *after* this
course, when you graduate to a dedicated homelab box and want the
type 1 experience.

One honest limitation to carry forward: a type 2 hypervisor shares your
laptop with everything else you run. Forty browser tabs and three VMs
will fight, and the VMs will win, because you gave them their RAM up
front. Close what you don't need on lab nights.

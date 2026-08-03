---
title: "3.1 What virtualization is, and what a hypervisor does"
sidebar_position: 1
---

# 3.1 What virtualization is, and what a hypervisor does

You're about to run a domain controller, a Linux server and an attacker
machine on the computer you're reading this on. Before you do, it's worth
having a one-sentence answer to what that actually is, because "I set up
some VMs" and being able to define virtualization are different things in
an interview.

> **Virtualization is using software to divide one physical computer into
> several independent computers, each running its own operating system,
> each isolated from the others, and each behaving as though it owns real
> hardware.**

Three words in that sentence are doing the work.

**Divide.** One machine's CPU, memory and disk get carved into portions
and handed out. Nothing is copied or emulated in the slow sense; the
guest's instructions mostly run directly on your real processor.

**Independent.** Each virtual machine boots, runs and crashes on its own.
You can reboot one without touching the others, and that's what makes a
lab like this one possible rather than a single computer you keep
reinstalling.

**Isolated.** A guest cannot see the others or reach into the host except
through channels you deliberately open. That's why you'll shortly run
malware-adjacent tooling on Kali next to a domain controller without
fear, and it's why the offensive work in Module 14 is safe to do at all.

Organizations virtualize for reasons you'll feel in this course: one
physical server can do the work of many, machines can be created in
minutes instead of ordered in weeks, and a broken system can be rolled
back to a snapshot instead of rebuilt. You'll experience that last one
personally in lesson 3.5.

Worth knowing that the idea generalizes well beyond servers. Module 4
virtualizes **networks**, building switches and segments that exist only
in software. Module 6 introduces **containers**, which chase the same
isolation with a lighter mechanism. Storage and desktops get the same
treatment in industry. The pattern is always identical: a layer of
software presents something that looks like dedicated hardware, backed by
shared real hardware underneath.

## The program that does it

A hypervisor is a program that lies to operating systems. It presents
each guest OS with what looks like a computer (a CPU, some RAM, a disk,
a network card) and secretly maps all of it onto slices of your real
hardware. The guest can't tell. Windows Server will boot inside your
desktop or laptop genuinely believing it's on a rack somewhere, and that
belief is
what the virtualization setting you checked in 0.6 makes efficient: your
CPU has instructions specifically built to keep guests fast and
contained.

Two flavors exist, and the names come up in interviews. A **type 1**
hypervisor runs on bare metal with no OS underneath; that's what runs
enterprise datacenters (VMware ESXi, Proxmox, Hyper-V Server), and my
own lab runs on one. A **type 2** hypervisor runs as an application on
top of your normal OS, which is what you'll use, because the computer
running it also needs to stay your everyday computer.

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
computer with everything else you run. Forty browser tabs and three VMs
will fight, and the VMs will win, because you gave them their RAM up
front. Close what you don't need on lab nights.

## What you'll meet at work

You will almost certainly not administer VMware Workstation in a job. You
will administer one of these, so it's worth knowing the names before
somebody says one in an interview and watches your face.

The reassuring part first: **a virtual machine is a virtual machine.**
Everything Module 3 teaches you (what a hypervisor does, virtual disks,
snapshots, virtual network adapters, why you size RAM up front) is the
same on every platform below. What changes is the management layer and
the scale: instead of one host you have a cluster, instead of a local disk
you have shared storage, and instead of shutting a VM down to move it you
migrate it while it's running.

- **VMware vSphere** (the ESXi hypervisor plus vCenter to manage it) has
  been the enterprise default for two decades. If you join a large
  organization, this is the most likely thing you'll find. Its position
  is less certain than it was: Broadcom's acquisition brought significant
  licensing and packaging changes, and a lot of shops have been actively
  evaluating alternatives since. That churn is why the rest of this list
  matters more than it would have a few years ago.
- **Microsoft Hyper-V** comes inside Windows Server at no extra cost,
  which makes it common wherever the estate is already Windows. Managed
  through Windows Admin Center, Failover Cluster Manager, or System
  Center. You are already running Windows Server in this course, so this
  is the shortest hop from what you'll know.
- **Proxmox VE** is open source, built on Linux KVM, and has grown
  sharply, particularly in smaller organizations and among the
  VMware-alternative crowd. It's also the most likely thing you'll run
  yourself when you outgrow a laptop and buy a dedicated box. The
  **CyberRack** section in the top menu specifies exactly that build, and
  says [what changes if you run the course on it](/cyberrack/start-here-instead)
  rather than on a laptop.
- **Nutanix AHV** shows up in hyperconverged environments, where compute
  and storage are sold as one appliance rather than assembled.
- **KVM with libvirt** is the Linux-native foundation underneath Proxmox
  and most public cloud. Worth recognising as the layer, not just a
  product.
- **The cloud providers** are running hypervisors too. An EC2 instance or
  an Azure VM is a guest on somebody else's host; you just never touch the
  host. That's the whole difference.

### The vocabulary changes, the ideas don't

This is the genuinely useful part to carry into an interview, because the
same concept has a different name on each platform:

<div className="labTable">

| Concept | VMware | Hyper-V | Proxmox |
|---|---|---|---|
| point-in-time copy | snapshot | checkpoint | snapshot |
| move a running VM | vMotion | live migration | migrate |
| where disks live | datastore | SMB/CSV share | storage pool |
| management console | vCenter | Windows Admin Center | web UI, built in |

</div>

Don't go and learn all of these. Recognise the names, know which family
each belongs to, and remember that the concepts underneath are the ones
this module is teaching you. Somebody who understands snapshots properly
can work out `checkpoints` in an afternoon. Somebody who only memorised
where the buttons are in one product cannot.

If one of them interests you, the vendor documentation is free and the
community editions of Proxmox and Hyper-V cost nothing to try.

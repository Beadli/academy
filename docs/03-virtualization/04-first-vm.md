---
title: "3.4 Build a practice VM"
sidebar_position: 4
---

# 3.4 Build a practice VM

Time to build a computer out of settings. This VM is a rehearsal: you'll
install Ubuntu Server on it, and in the next lesson you'll snapshot it,
destroy it, resurrect it, and then delete it. Knowing it's disposable is
the point. Nobody learns the piano at a recital.

## Create the VM

In Workstation: **File > New Virtual Machine**. Take the Custom path if
it's offered with defaults otherwise, and when the wizard asks, answer
like this. Every choice teaches something, so the reasons ride along:

- **Installer**: point it at your Ubuntu Server ISO from 3.3. If the
  wizard offers an "Easy Install" that promises to answer the
  installer's questions for you, decline it. The installer's questions
  are the curriculum.
- **Name**: `practice01`. Boring names sort well; you'll appreciate
  this when there are seven VMs.
- **CPU**: 2 cores. Enough to feel responsive, small enough to share.
- **RAM**: 2 GB. A headless Ubuntu Server idles far below this.
- **Disk**: 25 GB, and here's the setting worth understanding: the
  hypervisor offers to allocate space now or let the disk **grow as
  it's used** (thin provisioning, in datacenter vocabulary). Choose
  grow-as-used. The guest sees a 25 GB disk either way, but the file
  on your laptop only occupies what's really written, which is how
  your machine from 0.6 fits a whole lab.
- **Network**: leave it on **NAT**. Module 4 is entirely about what
  that means and what the alternatives are; today the VM just needs
  the internet.

:::info VirtualBox difference
Same decisions, different wizard: **Machine > New**, and untick any
"unattended install" option so you get the real installer. RAM and CPU
live on the first screens; pick "dynamically allocated" for the disk,
which is VirtualBox's name for grow-as-used. Networking defaults to
NAT already.
:::

## Install Ubuntu Server

Power the VM on and it boots your ISO exactly as a physical server
would boot a DVD. The installer is text-mode: arrow keys, tab, enter.
It looks austere and it teaches well. Walk it like this:

1. Language and keyboard: yours.
2. Installation type, network, proxy, mirror: accept the defaults.
   (The installer configures the network automatically via that NAT
   connection; noticing that will pay off in Module 4.)
3. Storage: use the entire (virtual) disk, defaults throughout, and
   confirm. You're erasing a 25 GB file, not your laptop; the guest
   can't see your real disk at all.
4. Profile: your name, `practice01` as the server's name, a username
   you'll remember, and a password you'll type a lot. Lab passwords
   can be simple; production passwords can't; know which world you're
   in.
5. **OpenSSH server: tick yes.** One habit worth installing every
   time on every server, because a server you can only reach from its
   own console isn't really a server.
6. Skip the featured snaps list, let it install, and reboot when
   offered. If it complains about the CD-ROM on reboot, that's the
   ISO still "in the drive"; the hypervisor usually handles it, and
   disconnecting the ISO from the VM's settings fixes it if not.

Log in at the console with the account you created. Look around for a
minute; this is the same OS your permanent lab server will run, and
Module 6 goes deep on it. For today, prove it's a real computer on a
real network:

```bash
# Ubuntu's IP address on the NAT network. Yours will differ from
# your neighbor's, and Module 4 explains where it came from.
ip addr

# A round trip to the outside world, four times.
ping -c 4 ubuntu.com
```

A machine you built from settings just spoke to the internet. Leave it
running and go straight into lesson 3.5, where you'll learn why it was
never in any danger.

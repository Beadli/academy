---
title: "What to buy first"
sidebar_position: 2
---

# What to buy first

The v1.0 build specified in this section costs just under $3,000. Almost nobody
should buy it in one go, and presenting it as a shopping list is exactly
how these guides mislead people.

Buy in stages. Each stage below is useful on its own, teaches something
specific, and works whether or not you ever go further. If you stop after
stage one you'll still have a better lab than most people who read about
labs.

## Stage 1: one small machine, around $200 to $400

**Buy a used mini PC.** A single Intel-based small-form-factor desktop:
Lenovo ThinkCentre Tiny, Dell OptiPlex Micro, HP EliteDesk Mini. They were
bought by corporations in enormous quantities, they get replaced on a
cycle, and the used market is consequently flooded.

Look for:

- **Memory capacity above all.** 32 GB is a good target and 64 GB is
  better. Check the specific model's maximum before buying, because it's
  the ceiling on everything you'll do.
- **An Intel chip with virtualization support**, which any business
  machine of the last decade has.
- **Room for an NVMe drive**, ideally two.

Install a type 1 hypervisor on it, most likely **Proxmox VE**, which is
free. This is the single biggest jump in the whole progression: you go
from a laptop that pretends to be a lab to a machine whose entire job is
running virtual machines, always on, reachable from your desk.

What it teaches: a real hypervisor, remote management, uptime, and the
difference between a lab you visit and a lab that runs.

## Stage 2: somewhere to put the data, around $150 to $500

**Add storage.** Either a purpose-built NAS or a second mini PC with
drives in it, running TrueNAS or similar.

Do this second because until now everything you own lives on one machine,
and that machine is one failure away from taking your work with it. Shared
storage also unlocks the concepts that matter later: backups that live
somewhere other than the thing being backed up, and storage that survives
a node being rebuilt.

What it teaches: ZFS, snapshots, NFS and SMB, backup and restore, and the
lesson every professional learns eventually, which is that a backup you
have never restored is not a backup.

## Stage 3: real networking, around $150 to $350

**Add a managed switch and a firewall appliance.** A small managed switch
with VLAN support, and a multi-port Intel N100 box running OPNsense.

Now the segmentation the course taught you in Module 4 stops being virtual
adapters and becomes cables, ports, and VLAN tags. This is the stage that
most changes how you think, because a mistake here disconnects something
and you have to work out why.

What it teaches: VLANs on real hardware, inter-VLAN routing, firewall
policy, and the physical layer that virtual networking abstracts away.

## Stage 4: a cluster, another $400 to $800

**Add a second and third node.** Matching the first if you can, because
identical hardware makes everything easier to reason about.

Three nodes is where clustering concepts become real: quorum, live
migration, high availability, and workloads that survive a machine being
switched off. Two nodes cannot form a proper quorum, which is itself worth
understanding.

What it teaches: clustering, quorum, live migration, and the operational
practices that only make sense once there's more than one of something.

## Stage 5: the rack, and the rest

Only now does a rack make sense, along with power protection, a patch
panel, and cable management. These make an existing lab pleasant rather
than making a lab exist.

Power protection is the one I'd bring forward if your mains is
unreliable, since it protects the storage you added in stage 2. It goes
*beside* the rack rather than in it: no UPS is made for ten-inch rails,
and [the build page](./build#power-and-why-there-is-no-ups-in-this-rack)
explains why that turns out not to matter much.

## The order matters more than the parts

If you take one thing from this page: **compute, then storage, then
network, then scale.** Each stage is usable on its own and each one makes
the next one obvious.

The failure mode is buying stage 5 first, because the rack is the part
that looks like a lab in photographs. It's the part that teaches you
least.

## Buying used, briefly

Business-class used hardware is the whole reason this is affordable.

- Search by model number rather than browsing categories.
- Ex-corporate machines are usually well-maintained and boringly reliable.
- Assume you'll replace the drive; treat a bundled one as a bonus.
- Memory is usually cheaper to add yourself than to buy pre-installed.
- Avoid rack-mount enterprise servers unless the noise genuinely doesn't
  matter to you. They are cheap for a reason.

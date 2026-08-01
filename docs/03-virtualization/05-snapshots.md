---
title: "3.5 Snapshots: break it, then undo it"
sidebar_position: 5
---

# 3.5 Snapshots: break it, then undo it

A snapshot freezes a VM's complete state (disk, and optionally memory)
at a moment you choose, and lets you return to that moment later, as
many times as you like. It's `git commit` for an entire computer, and
it will change how brave you are.

It changes how professionals work too. Before I replaced the TLS
certificate on the single most load-bearing VM in my lab, I snapshotted
it first. The swap went fine, but I'd have bet money it would; the
snapshot wasn't pessimism, it was the reason my hands were steady.
Snapshot before risk is the habit this lesson installs, and I want it
installed the memorable way: you're going to destroy a working server
and then make that not have happened.

## Take the snapshot

With `practice01` running from lesson 3.4: **VM > Snapshot > Take
Snapshot**. Name it `clean-install`, and put something in the
description; six VMs from now, "snapshot 3" tells you nothing. Naming
discipline starts with the first one.

:::info VirtualBox difference
Machine tools menu > **Snapshots**, then the Take button. Same concept,
same advice about names.
:::

## Now wreck the machine

In the VM's console, delete the folder that holds the operating
system's kernel, which is the part that boots:

```bash
# This destroys the machine's ability to start. That is the point.
# Read lesson 1.6's rule again: never run a command you don't
# understand. You understand this one: /boot holds the kernel, and
# we are deleting it inside a machine we intend to kill.
sudo rm -rf /boot

# Prove it's gone, then pull the trigger.
ls /boot
sudo reboot
```

Watch the reboot fail. The exact error varies by version (a GRUB
complaint, a missing-kernel message, a rescue prompt), but the meaning
doesn't: this computer no longer has an operating system it can start.
On a physical server, what you're looking at is a reinstall-from-backup
afternoon and a very quiet drive to the office. Sit with that for a
second, because the next ten seconds are the whole argument for
virtualization.

## Undo it

Power the VM off (hard off is fine; it's already dead). Then **VM >
Snapshot > Revert to `clean-install`** (in VirtualBox: select the
snapshot, **Restore**). Boot it.

It's back. Kernel present, logins working, your command history in
`~/.bash_history` right up to the moment of the snapshot, and no
evidence the machine ever suffered. The disaster didn't get repaired;
it got *unhappened*. From this day forward, the ritual before anything
risky in your lab (a patch, a promotion, a config you're not sure
about) is a snapshot with a decent name. It costs seconds. You've now
seen exactly what it buys.

Two honest limits before you over-trust it. Snapshots live on the same
laptop as the VM, so they're an undo button, not a backup; a dead SSD
takes both. And a pile of old snapshots quietly eats disk and slows the
VM, so keep one or two meaningful ones per machine, not a museum.
Module 14 covers real backups.

## Now delete the whole thing

Last move of the module, and it matters more than it looks: delete
`practice01` entirely. **VM > Manage > Delete from Disk** (VirtualBox:
**Machine > Remove > Delete all files**).

If that gives you a flicker of reluctance, notice it, because it's the
instinct this lesson exists to remove. There's a phrase in operations:
servers are **cattle, not pets**. The VM was never the valuable thing.
The valuable thing is that you now know how to make another one, and
the proof is that you can do it from memory tonight. Every permanent
machine in your lab will die and be rebuilt eventually, some of them on
purpose in Module 9, and the students who struggle with that are always
the ones who let a VM become precious. Yours never will.

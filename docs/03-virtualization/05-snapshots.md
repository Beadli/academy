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

:::info[VirtualBox difference]
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

Two honest limits before you over-trust it.

**A snapshot is not a backup.** Snapshots live on the same laptop, in the
same folder, as the VM they protect. A dead SSD takes both. They're an
undo button for changes you made, not protection against hardware, and
Module 15 covers the real thing.

## What snapshots cost you

This is the part that surprises people, and it's worth understanding
before you have eight VMs rather than one.

Taking a snapshot doesn't copy the disk. The hypervisor freezes the
current disk and starts writing every subsequent change to a **separate
delta file**. That file starts at nothing and grows with every write the
VM makes from that moment on.

The consequence catches everyone once: **a snapshot's cost depends on how
long you keep it and how busy the machine is, not on how big the VM was
when you took it.** A snapshot taken this morning is nearly free. The same
snapshot left on a domain controller for two months, through a round of
Windows updates, can grow larger than the original disk. Windows Update
alone will do it.

They also slow the machine down, because every read may have to walk back
through the chain of deltas to find the current data. Several stacked
snapshots on one VM is genuinely noticeable.

### The rules that keep this from biting

- **Name them properly.** `pre-promotion`, not `Snapshot 1`. In three
  weeks you will not remember what "Snapshot 3" was for, and an unnamed
  snapshot is one nobody dares delete.
- **Take one before something risky, delete it once the risk has passed.**
  A snapshot's useful life is usually hours. If the change worked, you
  don't need the escape hatch any more.
- **One or two per machine, not a museum.** If a VM has five snapshots,
  that's a decision nobody made.
- **Check the folder occasionally.** Your VM's directory shows the delta
  files. If they're bigger than the disk they belong to, that's your
  answer.
- **Never leave a snapshot on a machine for weeks** and then wonder where
  the disk went. This is the single most common way lab builders run out
  of space.

Deleting a snapshot does not undo your work. It merges the changes
permanently into the disk and reclaims the space, which is exactly what
you want once you've decided to keep the changes.

:::warning[Domain controllers are a special case]
From Module 5 you'll be running domain controllers, and reverting *those*
to an old snapshot can corrupt Active Directory replication in a way that
is genuinely painful to repair. Lesson 5.13 explains why and what to do
instead. Taking snapshots of them is fine; reverting one of a pair on its
own is not.
:::

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
purpose in Module 10, and the students who struggle with that are always
the ones who let a VM become precious. Yours never will.

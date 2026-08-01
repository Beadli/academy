---
title: "3.7 Checkpoint: ready to build for real"
sidebar_position: 7
---

# 3.7 Checkpoint: ready to build for real

Most of this module happened in windows and wizards, so this checkpoint
is more checklist than command output. Two commands first, run on your
host machine:

```bash
# The ISO shelf is stocked. You should see Ubuntu Server, Windows
# Server eval, and the Kali VM image.
ls ~/lab/isos

# Disk reality check after the downloads: you still need room for
# the real VMs. df on Linux/mac; Get-PSDrive C on Windows.
df -h ~
```

## Pass criteria

- [ ] The hypervisor installs and opens cleanly (lesson 3.2), and you
      know which one you're on for the rest of the course
- [ ] All three images are in `~/lab/isos`: Ubuntu Server LTS, the
      newest Windows Server evaluation ISO, and the Kali prebuilt VM
      image (lesson 3.3)
- [ ] You verified the Ubuntu and Kali checksums against the vendor's
      published values, and you can say in one sentence what that
      proved and what the Microsoft download's assurance rests on
      instead (lesson 3.3)
- [ ] You can state when the Windows 180-day clock starts, and name
      the two reasons it shouldn't scare you (lesson 3.3)
- [ ] You built `practice01` from the ISO, declined the automated
      install, and ticked OpenSSH during setup (lesson 3.4)
- [ ] You snapshotted it, destroyed `/boot`, watched it fail to
      start, and reverted it back to life (lesson 3.5)
- [ ] You then deleted the VM without ceremony, and you can explain
      "cattle, not pets" to someone in one breath (lesson 3.5)
- [ ] At least 100 GB of disk remains free for the permanent lab VMs
- [ ] Journal entry written, committed, pushed; Module 3 ticked in
      `lab-progress.md` (lesson 3.6)

All green? Then you can make computers now. Module 4 teaches the part
you deferred today: what NAT was doing, where that IP came from, and
how to wire multiple VMs into an actual network with an inside and an
outside.

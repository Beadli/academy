---
title: "0.6 Checkpoint: measure your machine"
sidebar_position: 6
---

# 0.6 Checkpoint: measure your machine

Time to replace guesses with numbers. You need four facts about the
machine that will host your lab: how much RAM it has, how many CPU cores,
how much free disk, and whether hardware virtualization is switched on.
The last one trips people up constantly, because plenty of laptops ship
with it disabled and nothing ever complains until a hypervisor won't
start.

Run the commands for your operating system. Reading the comments counts
as part of the lesson; this is also your first taste of how scripts are
written in this course.

## Windows

Open PowerShell (Start menu, type "powershell") and run these:

```powershell
# Total RAM in GB. Win32_ComputerSystem holds physical hardware facts;
# the division just converts bytes into something readable.
(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB

# Physical cores and logical processors (hyperthreading counts double).
Get-CimInstance Win32_Processor |
  Select-Object Name, NumberOfCores, NumberOfLogicalProcessors

# Free space on C: in GB.
(Get-PSDrive C).Free / 1GB
```

For virtualization, the quickest check is Task Manager: press
Ctrl+Shift+Esc, open the **Performance** tab, click **CPU**, and look for
the line **Virtualization: Enabled** on the right.

## Linux

```bash
# RAM, human readable. Look at the "total" column.
free -h

# CPU model, core count, and a "Virtualization:" line that should say
# VT-x (Intel) or AMD-V.
lscpu

# Free space on your home filesystem.
df -h ~
```

## macOS

Apple menu, About This Mac. If the chip line says **Apple M1/M2/M3/M4**,
stop here: as covered in lesson 0.3, the Windows portions of this course
won't run on Apple Silicon, and I'd rather lose you honestly at Module 0
than dishonestly at Module 5. An Intel Mac works; virtualization is
always enabled on those, so you only need the RAM and disk numbers.

## If virtualization shows disabled

It's a firmware setting. Reboot into your BIOS/UEFI setup (usually
mashing F2, F10, or Del during startup, and laptop vendors all hide it
somewhere different) and look for **Intel VT-x**, **Intel Virtualization
Technology**, or **SVM Mode** on AMD, usually under an Advanced or CPU
menu. Enable it, save, reboot, and re-run the check. If the option truly
doesn't exist, the machine is too old for this lab.

## Pass criteria

- [ ] You know your RAM, cores, and free disk as actual numbers
- [ ] Virtualization shows **Enabled** (or VT-x / AMD-V in `lscpu`)
- [ ] You have roughly 150 GB free, or a plan to free it up
- [ ] You've picked your starting tier from lesson 0.3
- [ ] All four facts are written in your journal entry from lesson 0.5

All checked? Module 1 is waiting, and it's where the tools come out.

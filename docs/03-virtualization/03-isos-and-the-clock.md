---
title: "3.3 ISOs, checksums, and the 180-day clock"
sidebar_position: 3
---

# 3.3 ISOs, checksums, and the 180-day clock

An ISO is a disc image: the installer for an operating system, packed
into one file your hypervisor can pretend is a DVD. Tonight you're
collecting the three the lab needs. They're large, so start the
downloads and read the rest of the lesson while they run.

Make a home for them first, because ISOs scattered across a Downloads
folder is how you end up installing the wrong thing at midnight:

```bash
# One folder, all installers. Adjust the base path to taste.
mkdir -p ~/lab/isos
```

## The three downloads

**Ubuntu Server.** From
[ubuntu.com/download/server](https://ubuntu.com/download/server), take
the **LTS** release, which the page marks clearly. LTS means five years
of support, which is why it's what real servers run and what this
course runs.

**Windows Server evaluation.** From the [Microsoft Evaluation
Center](https://www.microsoft.com/evalcenter/), find Windows Server,
pick the **newest version offered**, and download the **64-bit ISO**
edition of the evaluation. It asks for a name and email; give it
something real enough to pass validation.

**Kali Linux.** From
[kali.org/get-kali](https://www.kali.org/get-kali/), grab the
**pre-built virtual machine image** for your hypervisor (VMware or
VirtualBox) rather than the installer ISO. Kali publishes ready-made
lab VMs, and when we build KALI01 you'll import one instead of
installing from scratch. Less time watching progress bars, same result.

## Verify what you downloaded

You're training for security work, so here's the habit that separates
professionals: never boot an installer you haven't verified. A
checksum is a fingerprint of a file's exact contents; if your
download's fingerprint matches the one the vendor publishes, the file
arrived intact and unmodified. Both Ubuntu and Kali publish SHA256
checksums right next to their download links.

```bash
# Linux (and Git Bash on Windows): fingerprint the file, then
# compare it by eye to the value on the vendor's download page.
sha256sum ~/lab/isos/ubuntu-*.iso
```

```powershell
# Windows PowerShell equivalent.
Get-FileHash ~\lab\isos\ubuntu-*.iso -Algorithm SHA256
```

```bash
# macOS ships shasum instead.
shasum -a 256 ~/lab/isos/ubuntu-*.iso
```

Honest note: Microsoft's evaluation center doesn't publish a checksum
next to its download. There, your assurance is that you downloaded
over HTTPS directly from microsoft.com and nowhere else. That's also
the real lesson of this section: verification means knowing exactly
what assurance you have for each file, not performing a ritual. A
checksum from the same page as the download proves integrity, not
holiness.

## The 180-day clock, demystified

The Windows Server evaluation is the full product, free, for 180 days
per install. People treat this clock like a bomb, and it isn't. Three
things defuse it:

First, **the clock starts when you install, not when you download.**
The ISO in your folder tonight costs nothing and never expires.
Nothing starts ticking until Module 5.

Second, **the countdown can be extended in place.** Windows ships a
licensing tool, and one administrator command (`slmgr /rearm`, which
you'll meet properly in Module 5) resets the evaluation period,
several times. Run the arithmetic and a single install stretches
comfortably past a year, which is longer than this course.

Third, and this is the mindset shift: **by the time a clock ever runs
out, rebuilding will be cheap.** A domain controller that took you a
weekend in Module 5 takes an evening once you've done it twice, and
Module 10 teaches automation that rebuilds machines while you make
dinner. Labs aren't heirlooms. The knowledge is in your journal and
your playbooks, not in any single VM's disk file.

So: download without fear, install without ceremony, and let day 180
be a problem for a version of you that has long since outgrown it.

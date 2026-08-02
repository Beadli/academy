---
title: "3.3 ISOs, checksums, and the 180-day clock"
sidebar_position: 3
---

# 3.3 ISOs, checksums, and the 180-day clock

An ISO is a disc image: the installer for an operating system, packed
into one file your hypervisor can pretend is a DVD. Tonight you're
collecting the three the lab needs. They're large, so start the
downloads and read the rest of the lesson while they run.

## Where everything lives

Set up your folders before you download anything. This looks like
housekeeping and it isn't: a VM is not one file, it's a directory full of
them (a virtual disk that grows to gigabytes, a config file, log files,
snapshot data, sometimes a saved copy of the machine's memory). Let two
VMs share a folder and you can no longer move, back up, or delete either
one without holding your breath.

The convention for this course, and the one I use:

```powershell
# Windows PowerShell. Two folders off the root of C: so paths stay
# short and predictable.
New-Item -ItemType Directory -Force -Path C:\VMs, C:\ISOs
```

```bash
# Linux and macOS. Same idea, in your home directory.
mkdir -p ~/VMs ~/ISOs
```

Installers go in `ISOs`. Every virtual machine gets **its own folder**
under `VMs`, named after the machine: `C:\VMs\practice01`,
`C:\VMs\DC01`, `C:\VMs\UBNT01`, and so on. When you build a VM in lesson
3.4 the wizard will ask where to put it, and that's the answer.

Three rules that will save you real grief later:

- **One folder per VM, always.** Deleting a machine becomes "delete that
  folder." Moving one to a bigger disk becomes "drag that folder."
  Backing one up is the same. All of that is only true if nothing else
  is living in there.
- **Name the folder after the machine, not the project.** In six months
  `DC01` tells you what it is. `test-thing-2` does not.
- **Never put VMs in OneDrive, Dropbox, iCloud, or any synced folder.**
  This one bites Windows users especially, because `Documents` is often
  OneDrive-backed by default and a VM parked there is the default
  suggestion. Sync clients try to upload a multi-gigabyte disk file
  while the VM is writing to it, which is slow at best and corrupts the
  disk at worst. `C:\VMs` sits outside all of that, which is exactly why
  I put it there.

## The three downloads

Whatever your browser saves to `Downloads`, move it into your `ISOs`
folder when it finishes. Do that each time, or by Module 5 you'll be
hunting through Downloads wondering which of three similar files is the
one you want.

**Ubuntu Server.** Go to
[ubuntu.com/download/server](https://ubuntu.com/download/server) and
take the **LTS** release the page leads with. Two ways to take the wrong
thing here, and beginners take both:

- **Ubuntu Server, not Ubuntu Desktop.** Desktop is a different download
  with a graphical environment attached. Real servers don't have one,
  this course doesn't use one, and the desktop version will waste your
  RAM running a login screen nobody looks at.
- **LTS, not the interim release.** If the site offers a newer
  non-LTS version, skip it. LTS means five years of support, which is
  why it's what production runs.

You'll get a file named something like
`ubuntu-<version>-live-server-amd64.iso`, a couple of gigabytes. The
"amd64" part just means standard 64-bit Intel or AMD, which is right for
your machine regardless of whose CPU is in it.

**Windows Server evaluation.** Go to the [Microsoft Evaluation
Center](https://www.microsoft.com/evalcenter/), find Windows Server, and
pick the **newest version offered**. Microsoft asks for a name, email,
and company before it lets you download; give it something real enough
to pass validation. When it offers formats, choose the **64-bit ISO**,
not the VHD and not the Azure option. It's a large file, 5 GB or more,
so start it early.

**Kali Linux.** Go to [kali.org/get-kali](https://www.kali.org/get-kali/)
and choose **Virtual Machines**, not the installer image. Kali publishes
ready-made VMs, so when KALI01 joins the lab later you'll import one
instead of sitting through another install. Pick the build matching your hypervisor (VMware
or VirtualBox).

It arrives as a compressed archive rather than an ISO, so you'll need an
unpacking tool: Windows users want [7-Zip](https://www.7-zip.org/), and
Linux or macOS can install `p7zip`. Unpack it into its own folder under
`VMs` (so `C:\VMs\KALI01`), following the same one-folder-per-machine
rule from above. This is the one download that lands in `VMs` rather
than `ISOs`, because it *is* a virtual machine rather than an installer.

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
sha256sum ~/ISOs/ubuntu-*.iso
```

```powershell
# Windows PowerShell equivalent.
Get-FileHash C:\ISOs\ubuntu-*.iso -Algorithm SHA256
```

```bash
# macOS ships shasum instead.
shasum -a 256 ~/ISOs/ubuntu-*.iso
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

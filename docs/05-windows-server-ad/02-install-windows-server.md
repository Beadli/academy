---
title: "5.2 Build DC01 and install Windows Server"
sidebar_position: 2
---

# 5.2 Build DC01 and install Windows Server

You've done this once already with `practice01` in Module 3, so the VM
part will feel familiar. The install itself has one screen where
beginners reliably take the wrong option, and it's flagged below.

## Create the VM

New virtual machine, pointed at the Windows Server evaluation ISO you
collected in lesson 3.3:

- **Name and location:** `DC01`, in `C:\VMs\DC01`, per the folder rules
  in 3.3.
- **RAM:** 4 GB. Windows Server with a desktop is not shy, and this
  machine runs for the rest of the course.
- **CPU:** 2 cores.
- **Disk:** 60 GB, grow-as-used. Windows plus updates plus the
  directory will not fill this, and running out of disk on a domain
  controller is a bad day.
- **Network:** your **lab LAN**. Tier 1, that's the NAT network you
  reconfigured in 4.3. Tier 2, that's the host-only segment behind
  FW01. Either way this machine goes on `10.10.10.0/24`.
- If the wizard offers to install Windows automatically for you,
  decline it, exactly as in Module 3. You want to see the screens.

## Install it

Boot the VM. You may need to press a key quickly when it says "press any
key to boot from CD"; if you miss it, the VM will fail to boot and you
simply reset it and try again. Nothing is broken.

Then walk the installer:

1. Language, time, keyboard: yours. Next, then **Install now**.
2. **Choose the edition. This is the screen that catches people.** You
   will be offered several options, and the difference that matters is
   whether the name includes **"(Desktop Experience)"**.
   - **Take the Desktop Experience option**, on either Standard or
     Datacenter. This gives you the familiar graphical Windows you can
     click around in.
   - The options *without* Desktop Experience are **Server Core**: no
     desktop, no Server Manager, a command prompt and nothing else.
     Server Core is a perfectly good production choice and a miserable
     first-domain-controller experience. If you install it by accident
     you cannot add the desktop later; you reinstall.
   - Standard versus Datacenter makes no practical difference to this
     lab. Take Standard.
3. Accept the licence terms.
4. Choose **Custom: Install Windows only**. The "Upgrade" option is for
   existing installs and will get you nowhere on an empty disk.
5. Select the single unallocated disk and continue. Windows creates its
   own partitions.
6. Wait. This takes a while and reboots itself on the way through.
7. When it asks, set a password for the local **Administrator** account.
   It has to satisfy complexity rules, so a short simple one will be
   rejected. Use something you'll type often and **write it in your
   journal**; a lab password you can't remember costs you a rebuild.

Log in. You'll land on a desktop with **Server Manager** opening by
itself, which is the console you'll use for the next few lessons.

:::info[VirtualBox difference]
Same install, and one setting worth checking first: in
**Settings > System**, make sure **Enable EFI** matches how you intend
to boot. VirtualBox defaults vary by version, and a Windows Server ISO
that boots on one setting may not on the other. If the installer never
appears, that switch is the first thing to try.
:::

## Give it working hands

Two small quality-of-life steps that pay for themselves immediately.

**Install the guest tools.** In VMware that's **VM > Install VMware
Tools**, which mounts a virtual disc inside the guest; open it and run
the installer. In VirtualBox it's **Devices > Insert Guest Additions CD
image**. These give you a properly sized screen, a mouse that moves
between host and guest without being trapped, and copy-paste. Reboot
when it asks.

**Find PowerShell.** Right-click the Start button and choose the
Windows PowerShell or Terminal entry marked **(Admin)**. From here to
the end of the course you'll spend real time in this window, so if you
read lesson 2.1 without a Windows machine to try it on, go back and
skim its "Running PowerShell" section now: running commands one at a
time, what the backtick at the end of a line means, and how to escape
the `>>` prompt when a command isn't finished. Ten minutes there saves
an hour of confusion here.

Check it responds:

```powershell
# Which Windows is this, and which build? Useful in every support
# conversation you will ever have.
Get-ComputerInfo -Property WindowsProductName, OsVersion, OsBuildNumber
```

The machine now exists. It has the wrong name, the wrong address, and a
clock running down. Lesson 5.3 fixes all three, and every one of them
has to happen **before** the promotion in 5.4, because changing them
afterwards is genuinely painful.

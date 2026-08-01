---
title: "3.2 Install the hypervisor"
sidebar_position: 2
---

# 3.2 Install the hypervisor

Fair warning before you start: the download is the annoying part, not
the install. Since Broadcom bought VMware, getting the free installer
requires creating a free Broadcom account and navigating a portal that
was clearly designed for enterprise procurement rather than for you.
Budget fifteen minutes of mild irritation. It's still worth it, and
it's a one-time toll.

## Get VMware Workstation Pro

1. Create a free account at
   [support.broadcom.com](https://support.broadcom.com) (register,
   confirm your email, log in).
2. Once logged in, find the software downloads area and search for
   **VMware Workstation Pro**. (Broadcom reshuffles this portal often
   enough that turn-by-turn directions would rot; searching the
   product name from your logged-in session is the reliable path. If
   you land somewhere asking about entitlements or contracts, you've
   wandered into the enterprise side; back out and search again.)
3. Pick the **newest version listed** for Windows or Linux. Don't
   copy a version number from this page or any other; take the top of
   the list on the day you're downloading.
4. Run the installer with its defaults. Decline the trial-of-extras
   prompts if any appear; the free product is the product.
5. Launch it once and confirm you get the main window. If it asks
   about a license, choose the personal/free use option.

Windows may ask to reboot after install. Let it.

:::info VirtualBox difference
VirtualBox skips the portal saga entirely: download it from
[virtualbox.org](https://www.virtualbox.org), install with defaults,
and also install the matching **Extension Pack** from the same page
(it adds USB and other conveniences the lab will want).
:::

## If Windows complains about another hypervisor

On some Windows machines, the first VM you ever boot will be slow or
the tool will warn about Hyper-V or "virtualization-based security."
That's Windows itself quietly using the virtualization hardware for
its own security features, and two hypervisors are now sharing one
CPU feature. Modern Workstation versions cooperate with it and run
anyway, just with a performance tax. If your VMs later feel sluggish
out of proportion to your hardware, search your Windows version's
settings for **Memory integrity** (under Core isolation) and know
that turning it off trades a Windows hardening feature for VM speed.
That's a real trade with a real cost; I'm telling you the lever
exists, not pulling it for you.

## Prove it works

Open the application. You don't need to build anything yet; that's
lesson 3.4. For today, success is the main window opening without
errors and a **File > New Virtual Machine** menu item that's clickable.
If the app instead complains that virtualization is disabled, revisit
checkpoint 0.6: the firmware setting didn't take, and the fix is the
BIOS trip described there.

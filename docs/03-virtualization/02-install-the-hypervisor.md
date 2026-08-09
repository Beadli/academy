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

**First, a free Broadcom account.** Register at
[support.broadcom.com](https://support.broadcom.com), confirm your email, and
log in. Nothing below is visible to a logged-out visitor, so do this part
first even though it feels like a detour.

Then the portal, which is where people give up. The route to the free
installer is not something you can reason your way to, because Workstation
now sits behind a menu entry named after an entirely different product.

:::tip[The portal path, verified August 2026]
Broadcom rearranges this site, so treat the steps as a snapshot of one
working route rather than a permanent map.

1. In the menu down the left-hand side, choose **VMware Cloud Foundation**.
   That is genuinely where the desktop products live, and no, nothing on
   the page tells you that.
2. Click **My Downloads**.
3. Find the text link reading **Free Software Downloads available HERE**
   and click it. This is the step people miss, and missing it is exactly
   how you end up on pages demanding entitlements and contract numbers.
4. Type **Workstation** into the search box and choose
   **VMware Workstation Pro**.
5. Choose your operating system, Windows or Linux, and take the newest
   release listed. Don't copy a version number from this page or any
   other; take the top of the list on the day you download.
6. Tick **I agree to the Terms and Conditions**. The download button does
   nothing at all until you do, and it does not tell you why.
7. Click the download icon.

**If the portal has been rearranged since this was written**, search the
product name from your logged-in session and look for wording about free or
personal downloads. If you land somewhere asking about entitlements or
contracts, you are on the enterprise side of the house: back out and search
again. And if it becomes a fight, take the VirtualBox path below. It runs
this whole course.
:::

Then install it:

1. Run the installer with its defaults. Decline the trial-of-extras
   prompts if any appear; the free product is the product.
2. Launch it once and confirm you get the main window. If it asks
   about a license, choose the personal/free use option.

Windows may ask to reboot after install. Let it.

:::info[VirtualBox difference]
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

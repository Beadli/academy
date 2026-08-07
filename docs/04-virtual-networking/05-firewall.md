---
title: "4.5 Build a real firewall (Tier 2)"
sidebar_position: 5
---

# 4.5 Build a real firewall (Tier 2)

:::note[Tier 2 from here]
This lesson and the next need the 32 GB tier, because they add a
seventh machine and a second network segment. **Tier 1 students: read
both anyway, then skip to 4.7.** Nothing later in the course breaks
without a firewall, your addresses are identical either way, and the
concepts in 4.6 (what a boundary does, and how you prove it works) come
up in every job interview you'll ever have for a security role.
:::

You're about to build the machine that sits between your lab and
everything else. OPNsense is a real, open-source firewall used by real
organizations, and running one is the difference between knowing that
firewalls exist and knowing what a rule actually does.

## Get OPNsense

From [opnsense.org/download](https://opnsense.org/download/), choose:

- **Architecture:** `amd64`
- **Image type:** `dvd`, which is the installable ISO. The other options
  exist for real hardware: `vga` and `serial` are pre-made disk images
  for appliances, and `nano` is for flash media. Take `dvd`.
- **Mirror:** anything geographically near you

What downloads is a compressed file ending `.iso.bz2`. Unpack it with
7-Zip on Windows, or `bunzip2 <filename>` on Linux and macOS, and put
the resulting `.iso` in your `ISOs` folder next to the others.

## Create the VM

The one thing that matters here is the network cards, and the order you
add them.

- **Guest OS type:** FreeBSD (64-bit). OPNsense is built on FreeBSD, and
  telling the hypervisor that gets you sensible defaults.
- **Name and location:** `FW01`, in `C:\VMs\FW01`, per lesson 3.3.
- **RAM:** 2 GB. **CPU:** 1 core. **Disk:** 20 GB, grow-as-used.
- **Network adapter 1:** your NAT network. This becomes **WAN**, the
  outside.
- **Network adapter 2:** your host-only network (VMnet2). This becomes
  **LAN**, your lab.

**Order matters.** OPNsense names the cards in the order the hypervisor
presents them and will offer to call the first one WAN. If you add them
backwards you'll spend the install wondering why the internet is on the
wrong side, so add NAT first and host-only second. In VMware you may
need to open the VM's settings and **Add** a second network adapter
before first boot, because the wizard only offers one.

## Install it

Boot the VM from the ISO. OPNsense starts a live system first, which
confuses people who expect an installer to appear.

1. Let it boot to a login prompt. It may run an auto-configuration
   sequence first; wait for it to settle.
2. Log in with the installer account. OPNsense's installer credentials
   are shown on screen at the login prompt; at the time of writing that
   is `installer` with password `opnsense`, and the on-screen text is
   authoritative over this page.
3. Accept the defaults through the installer, including the filesystem
   choice, unless you have a reason to change one.
4. When it offers to set a root password, set one you'll remember and
   write it in your journal. This is a lab, and you're allowed to write
   lab passwords down. You're not allowed to reuse a real one.
5. Reboot when prompted, and make sure the ISO is disconnected so it
   boots from disk.

## Assign the interfaces

After reboot you land on the console menu. This is where you tell the
firewall which card is which.

If it didn't assign them automatically, choose **1) Assign interfaces**
and set WAN to the first card and LAN to the second. The card names look
like `em0` and `em1`, or `vtnet0` and `vtnet1` depending on the
hypervisor's emulated hardware.

Then choose **2) Set interface IP address**, pick **LAN**, and give it:

- IPv4 address: `10.10.10.254`
- Subnet bits: `24`
- No upstream gateway for LAN (this interface *is* the gateway)
- Decline IPv6 configuration
- **Enable DHCP on LAN: yes**, with a range from `10.10.10.100` to
  `10.10.10.199`, exactly matching the plan in lesson 4.3
- Decline the offer to revert the web interface to HTTP

Leave WAN alone. It takes its address from your hypervisor's NAT DHCP,
which is the correct behaviour: to your firewall, that side simply looks
like an internet connection.

:::tip[What this is called at work]
OPNsense is a real firewall, and the ones in most enterprises are **Palo Alto,
Fortinet, Cisco and Check Point**. The model you are about to learn is the
model they use: interfaces, zones, rules evaluated in order, default deny
inbound, stateful return traffic and NAT.

**Three things are different, and only one of them is technical.**

Enterprise firewalls identify traffic by application rather than by port, and
can write rules about *users* by talking to Active Directory, so a rule reads
"finance can reach the finance app" instead of "this subnet can reach port
443". The threat and filtering subscriptions are usually where the real cost
sits.

They are managed centrally, because nobody logs into forty firewalls
individually.

And the one that surprises people most: **you will not click Apply.** A
firewall change goes through a change request, a review and a window. The
technical work is ten minutes and the process is two weeks, and learning the
rule logic here is what lets you argue for the change convincingly.
:::

## Reach the web interface

From your own computer, browse to `https://10.10.10.254`.

Your browser will warn you loudly that the certificate can't be trusted.
That's expected and it's not a fault: the firewall generated its own
certificate and nothing on earth has any reason to trust it yet. Click
through the warning. In Module 7 you'll build a certificate authority
and issue this box a certificate your machines actually trust, and the
day that warning disappears is a genuinely satisfying moment.

Log in as `root` with the password you set, and work through the setup
wizard. Take its defaults, with two exceptions worth understanding:

- **DNS servers:** leave blank to use your upstream connection's own, or
  set a public resolver if you prefer. In Module 5 you'll come back and
  point this at your domain controller instead, because in a Windows
  domain the DC is the DNS server.
- **Block private networks on WAN:** leave this ticked. It tells the
  firewall to ignore private-range traffic arriving from the outside,
  which is right for a real edge device. Your WAN is a private range in
  this lab, so if you later can't reach the firewall's WAN side
  deliberately, this setting is why.

Change the root password when the wizard offers, and note the new one in
your journal.

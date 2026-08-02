---
title: "4.4 Import KALI01 and go exploring"
sidebar_position: 4
---

# 4.4 Import KALI01 and go exploring

Time to put a machine on the network you just built. Kali is the
attacker box you'll use in Module 14, and it earns its place today for a
duller reason: it's a prebuilt VM, so it boots in two minutes instead of
forty, and it comes with every networking tool already installed.

You downloaded and unpacked it in Module 3. If you skipped that, go back
to lesson 3.3; you want the **virtual machine** build for your
hypervisor, not the installer ISO, unpacked into `C:\VMs\KALI01`.

## Import it

In VMware: **File > Open**, then select the `.vmx` file inside the
folder you unpacked. That's it. There's no install, because someone at
Offensive Security already did it.

Before you power it on, set its network:

- **Tier 1:** the NAT network (VMnet8), which is your lab LAN.
- **Tier 2:** the NAT network too, and here the choice is deliberate.
  That's the *outer* segment, outside the firewall you're about to
  build. Your attacker starts on the far side of the boundary, exactly
  like a real one, and getting from there to your domain is what Module
  14 is about.

:::info VirtualBox difference
Use **Machine > Add** and pick the `.vbox` file from the unpacked
folder. Set the adapter in **Settings > Network** to your `lab-nat` NAT
Network (Tier 1) or leave it on the NAT Network as the outer segment
(Tier 2).
:::

Power it on and log in. Kali publishes the default credentials for its
prebuilt images on the same page you downloaded from, and they are
`kali` / `kali` unless that page tells you otherwise. **Change the
password now**, because a default credential you meant to change later
is how labs become other people's labs:

```bash
passwd
```

## Answer the four questions

Lesson 4.1 said every machine answers four questions. Make this one show
you its answers.

```bash
# 1. Who am I? Look for the address on the interface that isn't "lo".
#    The -brief flag gives one tidy line per interface.
ip -brief addr

# 2 and 3. Who's local, and who do I hand everything else to?
#    The "default via" line names your gateway.
ip route

# 4. How do I turn names into addresses?
cat /etc/resolv.conf
```

If that last file shows `127.0.0.53` rather than a real address, you've
met a local DNS caching service: the machine asks itself first, and that
service forwards to the real server. `resolvectl status` shows you the
one it's forwarding to. Kali usually shows the real address directly,
but plenty of Linux systems don't, and knowing both shapes saves you
from concluding DNS is broken when it isn't.

You should be looking at an address from the DHCP pool you defined, a
gateway that matches what your hypervisor runs, and a DNS server. Nobody
typed any of that in. Something handed it over on boot, which is exactly
what lesson 4.1 described.

Now prove each layer works, in order, because this sequence is how you
debug a network for the rest of your life:

```bash
# Layer 1: can I reach my own gateway? If this fails, the machine is
# on the wrong virtual switch. Substitute your real gateway address.
ping -c 3 10.10.10.2

# Layer 2: can I reach the outside world by address? If the gateway
# answers but this doesn't, routing or NAT is the problem.
ping -c 3 1.1.1.1

# Layer 3: can I resolve names? If ping by address works and this
# fails, it's DNS. It is very often DNS.
ping -c 3 ubuntu.com

# And the direct DNS question, which separates "DNS is broken" from
# "something else is broken and DNS gets blamed":
dig +short ubuntu.com
```

Work down that list whenever something can't reach something, in that
order, and you will find the layer that's broken instead of guessing.
I still do this exact sequence, in this exact order, and it still finds
the problem faster than thinking hard does.

## See your neighbors

Kali ships with `nmap`, and this is a fair use of it: scanning a network
you built, on hardware you own.

```bash
# Who else is on this network? -sn means "discover hosts, don't probe
# their ports", which is the polite version. Adjust the range to your
# own network if you're on Tier 2 and the outer segment differs.
sudo nmap -sn 10.10.10.0/24
```

Right now the answer is thin: your gateway, your own machine, maybe your
computer's adapter on that network. That's the point of running it
today. In Module 5 a domain controller appears here, and in Module 6 a
Docker host, and by Module 14 this same command tells a story. Save
today's output to your journal so you can watch the network fill up.

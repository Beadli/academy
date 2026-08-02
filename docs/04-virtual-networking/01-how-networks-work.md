---
title: "4.1 The four questions every machine answers"
sidebar_position: 1
---

# 4.1 The four questions every machine answers

Before a computer can talk to anything, it has to answer four questions.
Every network problem you will ever debug is one of these four being
wrong, so it's worth knowing them by name.

1. **Who am I?** Its IP address.
2. **Who's local?** Its subnet mask, which decides which addresses it
   can reach directly.
3. **Who do I hand everything else to?** Its default gateway.
4. **How do I turn names into addresses?** Its DNS server.

That's the whole model. Everything else is detail.

## Who am I: the address

An IP address like `10.10.10.10` identifies one machine on one network.
The addresses your lab uses come from ranges reserved for private
networks, which means they're free to use, they repeat harmlessly in
millions of homes and offices, and nothing on the public internet will
ever route to them. Three such ranges exist, and you'll meet all of them
in your career:

| Range | Where you'll see it |
|---|---|
| `10.0.0.0` to `10.255.255.255` | Big corporate networks. Your lab LAN. |
| `172.16.0.0` to `172.31.255.255` | Docker's default networks, some enterprises |
| `192.168.0.0` to `192.168.255.255` | Home routers, almost universally |

Your home router almost certainly hands out `192.168.x.x` addresses.
That's why the course puts the lab on `10.10.10.x` instead: two networks
using the same addresses in the same building is a specific kind of
misery, and picking a range your home network doesn't use avoids it
entirely.

## Who's local: the subnet mask

Written as `/24`, or as `255.255.255.0`, this is the machine's answer to
"which addresses can I reach by just shouting on the local wire, and
which ones need to go through a router?"

A `/24` means the first three numbers identify the *network* and the last
number identifies the *machine*. So `10.10.10.10` and `10.10.10.20` are
neighbors: they talk directly. `10.10.10.10` and `10.20.30.40` are not,
and traffic between them has to be routed. That single distinction, local
versus not-local, is what a subnet mask exists to answer.

A `/24` gives you 254 usable addresses, which is far more than this lab
needs and is the size almost every small network uses. Subnetting can get
deep, and if you go on to networking exams you'll do the arithmetic in
your head. For this course, `/24` everywhere, and the shape of the idea.

## Who do I hand everything else to: the gateway

If the destination isn't local, the machine hands the packet to its
**default gateway** and stops thinking about it. The gateway is just
another machine on the same network whose job is knowing what to do next.

The gateway is a *role*, not a fixed address. In Module 3 your practice
VM's gateway was a piece of software inside VMware. On Tier 2 later in
this module, it'll be a firewall you built. At home, it's your router.
Same job, three very different boxes.

## How do I turn names into addresses: DNS

You typed `ping ubuntu.com` in Module 3 and it worked, which means
something translated that name into an address first. That's DNS, and it
matters more than beginners expect. In Module 5 your domain controller
becomes your lab's DNS server, and Active Directory depends on DNS so
completely that "AD is broken" and "DNS is broken" are the same sentence
most of the time.

## The one that hands out the answers: DHCP

A machine can be told all four answers by hand (a **static**
configuration) or it can ask on boot and be handed them (**DHCP**).
Nobody typed anything into your practice VM, so it asked, and VMware's
built-in DHCP server answered.

The rule of thumb, which the lab follows: **servers get static addresses,
everything else gets DHCP.** A domain controller whose address changes
after a reboot is a bad afternoon, and things that point at servers by
address deserve an address that stays put.

## See it on a real machine

Run these on your own computer right now. The output is the four answers.

```bash
# Linux and macOS: addresses per interface.
ip addr          # or, on macOS: ifconfig

# The routing table. The line starting "default" names your gateway.
ip route         # or, on macOS: netstat -rn
```

```powershell
# Windows: all four answers in one place. Look for IPv4 Address,
# Subnet Mask, Default Gateway, and DNS Servers.
ipconfig /all
```

On the Linux side the route line looks like this, and it's worth reading
in full:

```text
default via 10.10.10.1 dev ens160 proto dhcp src 10.10.10.25 metric 100
```

That says: anything I don't know how to reach, hand to `10.10.10.1`,
send it out of the interface named `ens160`, I got this instruction from
DHCP, and my own address is `10.10.10.25`. Four questions, one line.

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

## Now the names for what you just learned

The four questions are how networking *works*. The rest of this section
is what the industry *calls* it, and you need both. Not because the
vocabulary makes you better at fixing things, but because every
certification exam, job interview, and senior colleague uses it, and
"the thing that turns names into addresses" gets tiring when the room
says "layer 7."

Network people describe communication as a stack of layers, each one
handing work to the one below. The full model has seven layers and is
called the **OSI model** (Open Systems Interconnection). Four of them
carry almost all everyday conversation:

| Layer | Name | What lives there | Where you met it |
|---|---|---|---|
| 7 | Application | The thing you actually wanted | DNS, HTTP, SSH |
| 4 | Transport | Which program on that machine, and whether delivery is guaranteed | Ports, TCP, UDP |
| 3 | Network | Addresses that work across networks | IP address, subnet, gateway |
| 2 | Data link | Addresses on one local wire | MAC address, switches |

Read your own route line again with that in mind. `10.10.10.25` is layer
3. The interface `ens160` sends frames at layer 2. When you open a web
page, the name lookup is layer 7, the connection to port 443 is layer 4,
the routing to the server is layer 3, and getting onto your local wire is
layer 2. Every message goes down the stack on the way out and back up on
the way in.

The practical payoff is that it makes questions specific. "The network is
broken" is not a question. "Can I ping the gateway?" tests layer 3. "Can
I resolve the name?" tests layer 7. "Is the cable in?" is layer 1. A
layered model turns a vague failure into an ordered set of checks, which
is what lesson 4.6 will have you do for real.

### Layer 4: TCP and UDP, the only two you need today

Layer 4 answers two questions: **which program** on the machine, and
**do we care whether it arrives?**

The first is the **port number**. One server can run a web server, SSH,
and DNS at once because each listens on a different port. Ports are why
firewall rules in lesson 4.5 read like "allow 443 from here to there."

The second is the choice between two protocols:

- **TCP** (Transmission Control Protocol) sets up a connection first,
  numbers everything, and re-sends whatever goes missing. Slower to
  start, but nothing is silently lost. Web, SSH, and email use it.
- **UDP** (User Datagram Protocol) just sends. No setup, no
  acknowledgement, no retry. Faster and cheaper, and if a packet
  vanishes, it's gone. DNS, DHCP, and voice or video calls use it.

The trade is honest rather than technical. Ask for a web page and you
want the whole page, so TCP. Ask a DNS server to resolve a name and it's
a single question with a single answer, so UDP is fine: if it goes
missing, just ask again. A stutter in a video call is better than the
call pausing to recover a fragment of a second nobody will ever see.

You'll watch a TCP connection actually being set up in lesson 4.7, and
by the end of Module 7 you'll watch one carrying traffic nobody can read.

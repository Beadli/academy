---
title: "5.8 See your domain from the network"
sidebar_position: 8
---

# 5.8 See your domain from the network

Everything so far has been the view from inside DC01. Now look at it
from outside, from KALI01, because what a domain controller announces
about itself to the network is both how legitimate machines find it and
the first thing an attacker enumerates. Same information, two very
different intentions.

:::note Tier 2: your firewall will block this, and that's correct
KALI01 sits outside your boundary and cannot reach `10.10.10.0/24`,
which is exactly what you proved in lesson 4.6. To do this lesson,
shut Kali down, move its network adapter to the LAN segment, and boot
it. Move it back to the NAT segment afterwards. Notice what that
means: you had to grant yourself access deliberately, and an attacker
would have to earn it.
:::

## Find the domain controller without being told about it

On KALI01, point questions at the DC directly with `dig @`:

```bash
# Does it answer for the domain at all?
dig @10.10.10.10 lab.cyber.internal +short

# The service records from lesson 5.1. This is the question a
# Windows machine asks when it needs to log someone in: "who
# provides LDAP for this domain?"
dig @10.10.10.10 -t SRV _ldap._tcp.lab.cyber.internal +short

# And the authentication one.
dig @10.10.10.10 -t SRV _kerberos._tcp.lab.cyber.internal +short
```

Those replies name DC01 and the ports it serves on. That is the entire
discovery mechanism: no broadcasts, no configuration on the client, just
DNS answering a specific question. A machine that can't ask this question
can't join or log in to your domain, which is why lesson 5.1 insisted
that DNS and Active Directory are one topic.

## What it looks like as a target

```bash
# Which services is this machine offering? -Pn skips host discovery,
# because Windows firewalls often drop the pings that discovery uses
# and you'd wrongly conclude the host is down.
sudo nmap -Pn 10.10.10.10
```

Compare that against the near-empty result you got in lesson 4.4 when
this network held nothing. A domain controller is a *loud* machine, and
you should recognise its signature:

| Port | Service | What it's for |
|---|---|---|
| 53 | DNS | the discovery you just used |
| 88 | Kerberos | issuing the tickets from lesson 5.5 |
| 135, 445 | RPC and SMB | remote management, file sharing |
| 389, 636 | LDAP and LDAPS | directory queries, plain and encrypted |
| 3268, 3269 | Global catalog | forest-wide directory searches |

Seeing 88 and 389 together on one host is how anyone scanning a network
concludes "that's a domain controller" within seconds. You've just done
the reconnaissance step of Module 14 against your own machine, which is
the only place you're allowed to do it.

## Ask the directory a question from outside

```bash
# An anonymous LDAP query for the directory's public information.
# Even unauthenticated, a DC will usually tell you its naming
# contexts, which reveals the domain's structure.
ldapsearch -x -H ldap://10.10.10.10 -s base -b "" namingContexts
```

If that returns the distinguished name of your domain, sit with it for a
second: an unauthenticated machine on the network just learned your
domain's real name and structure. That's normal, it's how the protocol
works, and it's why "the network is inside the firewall" is not a
security model. Everything meaningful beyond this point requires
credentials, which is what Module 14 goes after and Modules 12 and 13
detect.

## Put things back

Tier 2: shut Kali down and move its adapter back to the NAT segment.
Then confirm your boundary still works, because a temporary exception
you forget to remove is one of the most common real-world findings:

```bash
ping -c 3 10.10.10.10      # should fail
```

Tier 1: nothing to undo. Note in your journal that your attacker box
shares a network with your domain controller, and that Tier 2 exists to
fix precisely that.

---
title: "4.6 Segmentation: prove what can reach what (Tier 2)"
sidebar_position: 6
---

# 4.6 Segmentation: prove what can reach what (Tier 2)

A firewall you haven't tested is a firewall you're hoping about. This
lesson is the testing, and the habit it builds outlives the lab: after
any change to a boundary, prove both halves of the claim. Prove the
traffic you want still flows, and prove the traffic you don't want still
doesn't. People reliably test the first half and skip the second, and
that's how open boundaries survive audits for years.

## What OPNsense already does, before you write a rule

Fresh out of the wizard your firewall has a default policy, and it's the
right one:

- **From LAN, outbound: allowed.** Your lab machines can reach the
  internet and each other.
- **From WAN, inbound: denied.** Anything arriving from the outside is
  dropped unless a rule says otherwise.
- **Return traffic: allowed.** The firewall remembers connections your
  side started and lets the answers back in. That's what "stateful"
  means, and it's why outbound browsing works without you writing a rule
  for every website.

This shape, permissive outbound and default-deny inbound, is what almost
every organization runs at its edge. Understanding that you get it for
free, rather than building it, is the point of reading the rules before
touching them. Have a look: **Firewall > Rules**, and read the LAN and
WAN tabs.

## Test one: does the inside work?

You have exactly one VM to test with, so borrow it. Shut Kali down, and
in its settings move its network adapter from the NAT network to the
host-only network. Boot it back up. Kali is now, temporarily, an
inside machine.

```bash
# 1. Did the firewall's DHCP give it an address from your pool?
#    Expect something in 10.10.10.100-199.
ip -brief addr

# 2. Is the firewall its gateway? Expect 10.10.10.254 on the
#    "default via" line.
ip route

# 3. Can it get out? This proves the firewall is routing and
#    translating for the whole segment.
ping -c 3 1.1.1.1
dig +short ubuntu.com
```

Three commands, three proofs: DHCP works, routing works, name
resolution works. If any fails, you've found which of the four questions
from lesson 4.1 is unanswered, and that's precisely why the lesson made
you learn them by name.

## Test two: does the boundary block?

Shut Kali down again and move its adapter back to the **NAT** network,
where an attacker belongs. Boot it, and try to get in.

```bash
# Can the outside reach the firewall's inside interface?
ping -c 3 10.10.10.254

# Can it reach the lab network at all? -sn is host discovery,
# and a healthy answer here is a boring one: nothing found.
sudo nmap -sn 10.10.10.0/24
```

Both should fail. Failure is the pass condition, which is a sentence
worth sitting with. Your lab now has an inside and an outside, and the
only reason the outside can't reach in is a policy you can read, change,
and be held accountable for.

Write both results in your journal, including the exact commands. In
Module 14 you'll run these again from a position of having
compromised something, and having today's baseline to compare against is
what turns "I poked at it" into an assessment.

:::tip In GRC language
What you just built and tested has a name in control frameworks:
**boundary protection**, SC-7 in NIST 800-53, and it's one of the
controls auditors ask about first. Notice what made it assessable: not
the fact that a firewall exists, but that you can state the policy, show
the rules that implement it, and produce evidence you tested both
directions. That's the difference between a control that's implemented
and one that's merely installed, and in Module 16 you'll formally assess
this exact control on this exact lab.
:::

## Optional: reach your lab from anywhere

:::note Tier 3, and genuinely optional
Skip this without guilt. It's here because it's the piece people ask
about most once their lab exists.
:::

At some point you'll want to reach your lab from a laptop that isn't the
one it runs on. The wrong answer is forwarding ports from your home
router to the firewall's WAN, which puts your deliberately vulnerable
lab on the public internet. Don't.

The right answer is a private overlay network. [Tailscale](https://tailscale.com)
is free for personal use, installs as a package on OPNsense, and gives
you an encrypted path to the firewall without opening anything inbound.
Configured as a **subnet router**, it advertises `10.10.10.0/24` to your
other devices, so your laptop can reach the whole lab as if it were
plugged in.

Two things to know before you enable it, because they surprise people:
it creates a path that bypasses the boundary you just built, so the
segmentation tests above no longer describe every route into your lab;
and any device you add to your Tailscale network gets that reach. Set it
up deliberately, note in your journal that it exists, and remember it in
Module 14 when you're testing what can reach what.

---
title: "4.6 Segmentation: prove what can reach what (Tier 2)"
sidebar_position: 6
---

import Module4Tailscale from '@site/static/img/module4-tailscale.svg';

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

:::tip[In GRC terms]
What you just built and tested has a name in control frameworks:
**boundary protection**, SC-7 in NIST 800-53, and it's one of the
controls auditors ask about first. NIST is the US National Institute of
Standards and Technology, and 800-53 is its catalogue of security controls,
which Module 16 puts to work on your own lab. Notice what made it assessable: not
the fact that a firewall exists, but that you can state the policy, show
the rules that implement it, and produce evidence you tested both
directions. That's the difference between a control that's implemented
and one that's merely installed, and in Module 16 you'll formally assess
this exact control on this exact lab.
:::

## Optional: reach your lab from anywhere

:::note[Tier 3, and genuinely optional]
Skip this without guilt. It's here because it's the piece people ask
about most once their lab exists, and because doing it wrong is one of
the more effective ways to get yourself compromised.
:::

At some point you'll want to reach your lab from a laptop that isn't the
one it runs on. The wrong answer is forwarding ports from your home
router to the firewall's WAN, which puts your deliberately vulnerable
lab on the public internet where anyone scanning the address range will
find it. People do this. Don't.

The right answer is a **private overlay network**: a virtual network laid
on top of the internet, where only devices you have explicitly added can
see each other. [Tailscale](https://tailscale.com) is one, free for
personal use, and it builds that network without opening anything inbound
at all.

That last part is the bit worth understanding rather than just doing.

<Module4Tailscale role="img" aria-label="How Tailscale reaches the lab without opening a port. Your other laptop, on a network you do not control, dials outward to the Tailscale coordination server. FW01 running OPNsense dials outward too, through the home router, which forwards no ports and opens nothing inbound. The coordination server introduces the two, which then build an encrypted tunnel directly between themselves. The tunnel arrives on FW01 as a firewall interface called TLSCL, where normal firewall rules apply, and FW01 advertises the whole 10.10.10.0/24 lab subnet behind it." style={{width: '100%', height: 'auto'}} />

**How to read it.** The numbered steps run in order, and the order is the
whole trick.

Both ends make **outbound** connections (1 and 2), which is the same kind
of connection your browser makes to any website, and which every home
router already allows. Neither end waits for an incoming connection, so
nothing has to be opened on your router. That red strip is the point of
the diagram: the thing you were tempted to configure, you don't.

The coordination server then introduces the two devices to each other,
and steps out of the way. It is drawn away from the tunnel deliberately,
because the common misconception is that your traffic flows through
Tailscale's servers. It doesn't. The tunnel at (3) runs directly between
your laptop and your firewall, encrypted end to end.

Step (4) is why this lesson puts Tailscale on the firewall rather than
on a machine inside the lab. The tunnel arrives as an interface named
**TLSCL**, and OPNsense treats it like any other interface, which means
your firewall rules apply to it. The remote access is inside the boundary
you spent this module building, rather than around it.

### Install the plugin

OPNsense has shipped a Tailscale plugin since version 24.7, so there's no
command line involved.

1. **System → Firmware → Plugins.**
2. At the bottom of the page, click the line about community plugins to
   reveal them. This step is easy to miss: without it, searching for
   Tailscale returns nothing and you'll conclude the plugin doesn't
   exist.
3. Find **os-tailscale** and click **+** to install.
4. A **VPN → Tailscale** entry appears in the left menu. If it doesn't,
   reload the page rather than reinstalling.

:::warning[This is a community plugin]
OPNsense is a community-supported platform for Tailscale, not an
officially supported one, and `os-tailscale` is a community plugin rather
than a core component. In practice it works well. It's worth knowing
because you're installing extra software onto your firewall, which is the
one machine in the lab where the course otherwise tells you to keep the
surface small. That tension is real, and the next section is the reason
I think it's worth accepting here.
:::

### Connect it, advertise the lab, and approve the route

Under **VPN → Tailscale → Settings**, enable it and authenticate. You'll
be handed a URL to open in a browser and sign in with, which is how the
device joins your tailnet.

Then add `10.10.10.0/24` to the **advertised routes** and apply.

Now the step almost everyone misses. **Advertising a route does not
publish it.** Open the Tailscale admin console in a browser, find FW01 in
the machines list, open its route settings, and *approve* the subnet
route. Until you do, the tunnel comes up, the firewall is reachable by
its Tailscale address, and nothing behind it works, which looks exactly
like a broken routing problem and isn't one.

That approval step exists on purpose. A machine can claim to route any
subnet it likes; requiring a human to approve it means a compromised
device can't quietly volunteer to route your whole network.

### Prove it, then constrain it

From a device on your tailnet that is not the lab machine:

```bash
# The firewall itself, over the tunnel.
ping 10.10.10.254

# Something behind it. This is the one that proves the route works.
ping 10.10.10.10
```

The second one is the real test. The first only proves the tunnel is up.

Then do the part most people skip: go to **Firewall → Rules → TLSCL**
and decide what the overlay is allowed to reach. It is a normal interface
with normal rules, and leaving it wide open means every device you ever
add to your tailnet, including your phone, gets unrestricted access to a
lab that by Module 14 will contain deliberately vulnerable machines.

Write down in your journal that this path exists and what it can reach.
You'll want that note in Module 14 when you're testing which routes into
your lab you actually know about.

:::info[If you'd rather not add software to your firewall]
A reasonable alternative is a small Linux VM inside the lab running the
Tailscale client as a subnet router. It keeps the firewall untouched, at
the cost of about 1 GB of RAM.

Two things to get right if you go this way. **It must sit on the LAN
segment.** A machine on the WAN segment cannot reach the lab servers,
because that is precisely what you configured FW01 to prevent, so a
subnet router there would advertise a route to a network it can't reach.

And accept the trade: the tunnel then lands *inside* the LAN, past every
rule FW01 enforces. You get remote access, but you lose the ability to
filter it, which is the opposite of the situation the diagram above
describes. That's the reason this lesson teaches the firewall plugin as
the main path.
:::

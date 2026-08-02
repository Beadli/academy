---
title: "Module 4: Virtual networking"
sidebar_position: 0
---

# Module 4: Virtual networking

At the end of Module 3 your practice VM had an IP address you never
typed, a route to the internet you never configured, and a working DNS
lookup you never set up. That was deliberate. This module explains where
all of it came from, and then has you build the network your lab will
live on for the next thirteen modules.

Networking is where most self-taught labs quietly go wrong. People get
machines running, wire them however the wizard suggested, and then spend
months confused about why the domain controller can't be reached or why
the firewall rule they wrote does nothing. Getting this right once, on
purpose, saves all of that.

What's in it:

- **4.1** the four questions every machine has to answer
- **4.2** the hypervisor's network modes, and which one to use when
- **4.3** design your lab network, then build it
- **4.4** import KALI01 and go exploring
- **4.5** build a real firewall (Tier 2)
- **4.6** segmentation: prove what can reach what (Tier 2)
- **4.7** journal entry
- **4.8** checkpoint

**Tier 1** does 4.1 through 4.4 and finishes with a working lab network.
**Tier 2** continues into 4.5 and 4.6 and puts a real firewall in the
middle of it. Tier 1 students should still read the firewall lessons;
understanding what a boundary does matters even in a lab that doesn't
have one yet, and the addresses are identical either way so nothing
later in the course depends on which path you took.

Budget an evening for the concepts and the network build, and a second
one for the firewall if you're on Tier 2.

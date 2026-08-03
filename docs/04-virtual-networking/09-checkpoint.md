---
title: "4.9 Checkpoint: a network you can describe"
sidebar_position: 9
---

# 4.9 Checkpoint: a network you can describe

Run these on KALI01, since it's the machine you have.

```bash
# The four answers. Address from your DHCP pool, a gateway you can
# name, and a DNS server.
ip -brief addr
ip route
cat /etc/resolv.conf

# The debugging ladder from lesson 4.4, in order. Substitute your
# own gateway address on the first line.
ping -c 3 10.10.10.2
ping -c 3 1.1.1.1
dig +short ubuntu.com

# Who's on the network so far.
sudo nmap -sn 10.10.10.0/24
```

## Pass criteria

Everyone:

- [ ] You can name all four questions a machine answers at boot, and
      point at where KALI01's answers came from (lesson 4.1)
- [ ] Your lab network uses `10.10.10.0/24`, with DHCP handing out
      `.100` to `.199` (lesson 4.3)
- [ ] The addressing plan is written in `Projects/lab-network.md`, and
      matches what you built (lessons 4.3, 4.8)
- [ ] KALI01 boots, has an address from the pool, and its password is
      no longer the published default (lesson 4.4)
- [ ] All three rungs of the ladder pass from KALI01: gateway, then
      `1.1.1.1`, then a name lookup (lesson 4.4)
- [ ] You can explain in one sentence why the course doesn't use
      bridged networking (lesson 4.2)
- [ ] You captured a DNS lookup and can say why it used UDP rather than
      TCP (lesson 4.7)
- [ ] You captured the three-way handshake between your machine and
      KALI01, and can name the three packets in order (lesson 4.7)
- [ ] You followed the TCP stream and read your own HTTP request back as
      plain text, and that capture is saved in your journal for the
      comparison in lesson 7.6 (lesson 4.7)
- [ ] Given any packet, you can point at which rows in the middle pane
      are layers 2, 3, 4, and 7 (lessons 4.1, 4.7)

Tier 2 as well:

- [ ] FW01 is built with WAN on the NAT network and LAN on the
      host-only network, and you can say which adapter is which and
      why the order mattered (lesson 4.5)
- [ ] Its LAN interface is `10.10.10.254` and it serves DHCP for the
      segment (lesson 4.5)
- [ ] You reached the web interface at `https://10.10.10.254`, and you
      know why the certificate warning appears and which module fixes
      it (lesson 4.5)
- [ ] **Inside works:** with Kali temporarily on the LAN segment, it
      got a pool address, used `10.10.10.254` as its gateway, and
      reached the internet (lesson 4.6)
- [ ] **Outside is blocked:** with Kali back on the NAT segment, it
      cannot ping `10.10.10.254` and discovers nothing on
      `10.10.10.0/24` (lesson 4.6)
- [ ] Both test results are recorded in your journal with the exact
      commands, as the baseline Module 14 will compare against
      (lesson 4.6)

Green across the board means your lab has a real network with a plan
behind it, which is more than a lot of production environments can say.

Module 5 is the big one: Windows Server, your first domain controller,
and the moment `lab.internal` stops being a string in a document
and starts being a domain.

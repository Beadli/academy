---
title: "12.7 Detecting without decrypting"
sidebar_position: 7
---

# 12.7 Detecting without decrypting

Lesson 7.6 made a point while you were looking at a TLS handshake in
Wireshark: the hostname travels in the clear before encryption is negotiated,
because a server hosting many sites needs to know which certificate to
present. It said encryption hides the *contents* of a conversation, not the
fact that it happened or who it was with, and that Module 12 would rely on
exactly that.

This is that lesson.

## The problem, stated honestly

Nearly all traffic is encrypted now, and that is a good thing. It also means a
sensor watching the wire cannot read what is inside.

Organisations sometimes respond by decrypting: terminating TLS at a middlebox,
inspecting, and re-encrypting. It works, it is expensive, it breaks
certificate pinning, and it means a device on your network holds the plaintext
of everything your staff do, including their banking.

**Most detection does not need it**, and understanding why is the useful part.

## What is visible anyway

Even with perfect encryption:

**Who talked to whom, and when.** Source, destination, port, timing. All in
clear headers, necessarily, or the packet could not be routed.

**How much, and in what shape.** Volume and timing patterns. A connection
sending small bursts every sixty seconds looks nothing like a person browsing.

**The hostname**, via the TLS SNI field, exactly as lesson 7.6 showed you.

**The certificate the server presented.** Issuer, subject, validity. In the
clear during the handshake.

**How long it lasted.** A connection open for six hours to an address nobody
else in the building talks to is interesting regardless of content.

That is a great deal, and much of the best network detection uses only this.
An implant beaconing home is recognisable by its rhythm without a single
decrypted byte.

You have already seen this from the inside. Lesson 8.7 had you capture a
federated login and found you could see the sequence of hosts contacted and
the timing, but not the username, the token or the password. That lesson said
the split between visible metadata and hidden payload was the whole basis of
the detection work here, and this is why: **everything a sensor gets to reason
about is the part of that capture you could still read.**

:::tip[Metadata is often better evidence than content]
Counter-intuitive and worth holding onto.

Content can be obfuscated, encoded, compressed or encrypted by the attacker
inside your encryption. **Behaviour is much harder to disguise**, because it
is a consequence of what the software is actually doing.

A tool that checks for instructions every sixty seconds has to check for
instructions every sixty seconds. It can encrypt what it says, pad the length,
even jitter the timing, and the connection pattern remains a connection
pattern.

This is why the good network detections are about rhythm, volume, duration and
destination rarity rather than payload strings.
:::

## Tier 3: put a sensor on the wire

**This section needs SURICATA01**, the dual-NIC sensor from lesson 0.3.

Lesson 4.2 promised this: a sensor needs to see everyone's traffic, which is
not how a switch normally behaves. A switch sends each machine only its own
frames.

Two ways round it, and both have real names worth knowing:

**A monitor port**, which Cisco calls **SPAN** for Switched Port Analyzer and
others call port mirroring: the
switch is configured to copy traffic to one port. This is how it is done on
physical hardware.

**Promiscuous mode on a virtual switch**: your hypervisor's virtual network is
told to stop filtering, so every adapter attached to it sees everything. This
is the lab version, and it is a setting on the virtual network rather than on
the VM.

That is why SURICATA01 has two network adapters. One sits on the segment being
watched in promiscuous mode and never sends anything. The other is a normal
management interface you connect over.

**A sensor interface with no address is the right design**, not a shortcut. An
interface that cannot be addressed cannot be connected to, which means the
machine watching your network is not reachable from the network it watches.

## Install Suricata

On SURICATA01:

```bash
sudo apt update
sudo apt install -y suricata

# Which interface is the sensor one? Match it to the MAC in the hypervisor.
ip -brief link
```

Set the monitored interface and your home network in
`/etc/suricata/suricata.yaml`, then:

```bash
# Update the rule set. Suricata ships with community rules available.
sudo suricata-update

sudo systemctl enable --now suricata

# It logs in the same JSON shape you already know from Wazuh.
sudo tail -f /var/log/suricata/eve.json | \
  jq -r 'select(.event_type=="alert") |
         [.alert.severity, .src_ip, .dest_ip, .alert.signature] | @tsv'
```

## Watch the metadata

With nothing alerting, look at what the sensor sees anyway:

```bash
# Every TLS handshake: who connected to which hostname.
# This is lesson 7.6's SNI field, at scale.
sudo tail -f /var/log/suricata/eve.json | \
  jq -r 'select(.event_type=="tls") | [.src_ip, .tls.sni] | @tsv'
```

Browse something from a lab machine and watch the hostname appear. **You are
reading the destination of encrypted traffic without decrypting anything**,
which is the claim lesson 7.6 made and this is the demonstration.

## Send it to Wazuh

A second alert stream in a second place is two places to not look. On
SURICATA01, install the Wazuh agent as in 12.2, then add:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>
```

Now network alerts arrive in the same queue as host alerts, which is what a
SIEM is for: **one place where a host event and a network event about the same
incident sit next to each other.**

## Tier 1 and 2: what to take from this

You have not built a sensor, and the ideas are the point.

You already saw SNI in Wireshark in lesson 7.6, so you have seen the mechanism
first-hand. You know that timing, volume, duration and destination rarity are
detectable without decryption. And you know that "we cannot see inside TLS" is
not the same as "we cannot detect anything", which is a claim you will hear
made confidently by people who are wrong.

Module 4's Wireshark lesson gave you the tool to check any of this yourself on
your own machine, which is the version of this that needs no extra hardware.

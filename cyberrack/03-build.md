---
title: "The v1.0 build"
sidebar_position: 3
---

# The CyberRack v1.0 build

This is the whole design on one page. The [charter](./charter) has the
reasoning in full; this is the specification and what each part is there
to teach.

[![CyberRack v1.0: 10U rack elevation, network architecture showing an OPNsense firewall routing all seven VLANs over a single 802.1Q trunk to a Layer 2 MikroTik switch, a three-node Proxmox compute cluster, TrueNAS storage appliance, physical connectivity, VLAN and IP plan, power budget and hardware costs](/img/cyberrack-v1.png)](/img/cyberrack-v1.png)

*The diagram is dense. Open it in a new tab for a readable version; it's
designed to be looked at large rather than squinted at on a phone.*

## What it is

Three matched mini PCs running a **Proxmox VE** cluster, a dedicated
storage appliance running **TrueNAS SCALE**, an **OPNsense** firewall, and
a managed switch, in a 10-inch, 10U rack. Roughly the footprint of a large
shoebox, targeting about 125 watts idle.

:::warning[Designed, not yet built]
Nobody has assembled this. Every figure below is a design target or an
estimate from vendor specifications and used-market prices, not a
measurement from a running rack. Treat the costs as a shape and the power
numbers as a budget you'd verify with a plug meter on day one.
:::

<div className="labTable">

| Domain | Standard | Qty | Est. cost |
|---|---|---|---|
| Compute | Lenovo ThinkCentre M920q (i5-8500T, 64 GB, 1.5 TB NVMe) | 3 | $1,950 |
| Storage | AOOSTAR WTR Pro (N100, 32 GB, 2× 4 TB) | 1 | $480 |
| Firewall | Intel N100 mini PC | 1 | $160 |
| Switch | MikroTik CRS310-8G+2S+IN | 1 | $179 |
| Rack | 10-inch rack, panel, shelves, cables | 1 | $150 |
| Power | PDU strip, plus a shutdown-grade UPS (see below) | 1 | $150 |

</div>

**Estimated total: $3,069.** Prices are from the used market and move
around; treat them as a shape rather than a quote, and keep five to ten
percent back for the part that arrives broken.

Worth noticing: [the charter](./charter) sets a target of **$2,500**, and
this bill of materials comes to $3,069. That gap is left visible on
purpose. Budgets get set before prices get checked, every real project
meets this moment, and the useful question is which line you cut rather
than whether the spreadsheet was ever wrong. The stage-by-stage path in
[what to buy first](./what-to-buy-first) is how most people should resolve
it: buy a third of this, use it, and let the next purchase justify itself.

## The three nodes

Identical hardware, deliberately. Standardisation makes troubleshooting
dramatically easier and mirrors how real estates are built.

<div className="labTable">

| Node | Primary role |
|---|---|
| **Atlas** | Identity: Active Directory, AD CS, Keycloak, DNS, PKI |
| **Hermes** | Security: Wazuh, Suricata, OPNsense lab, logging |
| **Daedalus** | Platform: Docker, k3s, Gitea, CI/CD, development |

</div>

Those are preferred placements, not permanent homes. Workloads stay
migratable between nodes, which is the entire point of running a cluster
rather than three separate servers.

## The network

Seven VLANs, with inter-VLAN routing controlled by OPNsense and default
deny between segments:

<div className="labTable">

| VLAN | Name | Subnet | Purpose |
|---:|---|---|---|
| 10 | Management | 192.168.10.0/24 | Proxmox, switch, firewall, storage admin |
| 20 | Servers | 192.168.20.0/24 | VMs, containers, internal apps |
| 30 | Backup | 192.168.30.0/24 | Backup and replication traffic |
| 40 | Monitoring | 192.168.40.0/24 | Logging, metrics, SIEM |
| 50 | Guest | 192.168.50.0/24 | Internet-only, isolated |
| 60 | IoT | 192.168.60.0/24 | Untrusted devices |
| 70 | Security Lab | 192.168.70.0/24 | Attack simulation, vulnerable systems |

</div>

VLAN 70 is the one that matters most for anyone doing offensive work.
Deliberately vulnerable machines belong on a segment that cannot reach
anything you care about, and building that separation yourself is a
better lesson than reading about it.

### Who does the routing, and why it matters

**OPNsense routes every VLAN. The MikroTik is a Layer 2 switch.**

Physically there is one 802.1Q trunk between them carrying all seven
VLANs tagged, and the firewall holds a sub-interface for each. Every
device in the rack attaches to the switch and nothing attaches to anything
else.

That arrangement is deliberate, and it costs you something. All traffic
between VLANs has to travel up to the firewall and back down, which caps
east-west throughput at what a small N100 box can route. A Layer 3 switch
would move that traffic at line rate and never bother the firewall.

The reason to accept the cost: **every VLAN-to-VLAN crossing passes
through a device that can filter and inspect it.** Suricata sees it,
firewall policy applies to it, and the logs record it. In a lab built to
practise segmentation and detection, traffic that silently bypasses the
firewall is the opposite of what you want.

Be aware this is an SMB pattern rather than a large-enterprise one. Real
enterprises route east-west on Layer 3 switches and reserve firewalls for
trust boundaries. You'll meet that design, and the [phase 2 upgrade
path](#phase-2-move-some-routing-to-the-switch) below is how to build your
way to it deliberately.

## What each choice teaches

This is the column that justifies the spend. Nothing is here because it
was on sale.

<div className="labTable">

| Component | Enterprise skill |
|---|---|
| Proxmox cluster | clustering, quorum, live migration, HA concepts |
| TrueNAS SCALE | ZFS, NFS, SMB, iSCSI, snapshots, replication |
| OPNsense | VLAN routing, firewall policy, NAT, VPN, IDS/IPS |
| MikroTik switch | VLANs, trunking, link aggregation, spanning tree |
| Proxmox Backup Server | incremental backup, verification, restore testing |
| AD, AD CS, Keycloak | LDAP, Kerberos, SAML, OIDC, certificate lifecycle |
| Wazuh, Suricata | SIEM, host and network intrusion detection |
| Ansible, Gitea | configuration management, version control, IaC |

</div>

## The parts worth arguing with

A specification you can't disagree with isn't a design, it's a shopping
list. The choices most worth reconsidering for your own situation:

- **Three nodes.** Three is the minimum for real quorum, and it's also
  most of the budget. One node teaches you the majority of what's here.
  Start at one if the money matters, which it usually does.
- **64 GB per node.** Generous, and the main reason the M920q was chosen.
  If your workloads are lighter, 32 GB halves a significant cost.
- **The 10-inch rack.** Genuinely optional. A shelf works. The rack buys
  tidiness and portability, not capability.
- **Power protection.** Worth having, because it protects the storage
  everything else depends on. Worth sizing properly, for the reasons in
  the next section.

## Power, and the portability trap

The charter asks for a rack that is "desk-friendly, dorm-friendly,
apartment-friendly, quiet, portable, energy efficient, easy to relocate",
and puts **UPS and power distribution** in U1 of a 10-inch rack. Those two
requirements fight each other, and an earlier version of this page lost
the fight by specifying a 1000 VA consumer tower UPS.

Three things were wrong with that, and they're worth walking through
because the reasoning generalises well beyond this rack.

**It doesn't fit.** A 10-inch rack is ten inches wide. Nearly everything
sold as a rack-mount UPS is built for the 19-inch standard, and consumer
units like the one previously listed are tower-shaped and mount in
nothing at all. It would have sat on the floor beside the rack while the
elevation diagram claimed it was in U1.

**It's the heaviest thing you'd own.** Sealed lead-acid is most of the
weight of a UPS in that class, and weight is the requirement portability
actually cashes out to. A rack you can lift is a rack you'll take to a
friend's place, a study group, or an interview. One anchored by a lead
brick is furniture.

**It's sized for a problem this rack doesn't have.** Run the charter's own
numbers. The target is 80 to 150 watts idle and under 300 at peak:

<div className="labTable">

| Load | Runtime | Battery energy needed |
|---|---|---|
| 150 W | 5 minutes | 12.5 Wh |
| 150 W | 10 minutes | 25 Wh |
| 300 W | 5 minutes | 25 Wh |
| 300 W | 10 minutes | 50 Wh |

</div>

A 600 watt UPS is twice the wattage this rack will ever ask for, holding
far more stored energy than the job needs.

:::tip[Size it for shutdown, not for uptime]
This is the question people get backwards. Ask what the battery is *for*.

You are not trying to keep working through an outage. You're trying to
give ZFS and the databases underneath your services a few minutes to
finish writing and shut down cleanly, so a power cut costs you nothing
instead of costing you a rebuild. That job needs **minutes**, and the
table above says minutes are cheap.

What that buys you: a small lithium unit instead of a lead-acid tower,
which is lighter, smaller, has a longer service life, and doesn't need
the battery replaced every three years.

Two things to check before buying, because I can't check them for you:
whether the unit physically fits a 10-inch rack or is meant to sit on a
shelf, and whether it can signal the shutdown. A UPS with no data
connection is just a delay. You want one your machines can talk to, over
USB or the network, so they know to shut themselves down.
:::

**If your rack never moves**, ignore most of this and buy a conventional
tower UPS. It's cheaper per watt-hour and entirely sensible next to a
rack that lives in one corner. Just put it *beside* the rack in your own
plan, not in U1.

:::warning[The other portability cost: spinning disks]
The storage node's mechanical drives are the second thing that doesn't
love being carried. Hard drives are far more fragile while spinning than
when parked, so power the rack down before moving it rather than carrying
it live. If you expect to move it often, that's a real argument for SSDs
in the storage node despite the cost per terabyte.
:::

## Phase 2: move some routing to the switch

Once v1.0 works and you understand it, this is the upgrade worth doing,
and it's a better lesson than either endpoint on its own.

Migrate **Servers, Backup and Monitoring** routing from OPNsense to Layer
3 on the MikroTik. Those three are high-volume, low-risk and all inside
the trusted zone: backup jobs and log shipping have no business
hairpinning through a firewall. Keep **Guest, IoT and Security Lab** at
the firewall, because those are exactly the crossings you want inspected.

What it teaches, beyond the configuration:

- **Switched virtual interfaces** and routing on a switch, which is what
  the distribution layer of a real network does
- **Static routes** between two routing devices, and why they have to
  agree
- **Asymmetric routing**, which you will almost certainly cause by
  accident the first time, and which is a genuinely common production
  fault worth having debugged once
- The architectural judgement itself: **where you put the Layer 3
  boundary decides what your firewall can see**

Write it up as an Architecture Decision Record, per the charter's §26.2.
Recording why you moved the boundary, and what visibility you traded for
throughput, is the part that turns a configuration change into experience
you can talk about.

Do not start here. The value is in feeling the difference.

## Living with it

The charter sets the targets rather than reporting results: **80 to 150
watts idle**, under 300 at peak, and quiet enough for a bedroom, dorm or
home office. That last requirement is what ruled out secondhand rack
servers, which are cheaper for the same specification and sound like a
hairdryer.

Whether the build meets those targets is exactly the sort of claim worth
measuring rather than trusting. A cheap plug-in power meter settles the
first one in a day, and your own ears settle the second.

Work out your electricity cost before committing, using whichever figure
you end up with: 125 watts running continuously is roughly 90
kilowatt-hours a month, and only you know what that costs where you live.

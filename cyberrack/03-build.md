---
title: "The v1.0 build"
sidebar_position: 3
---

# The CyberRack v1.0 build

This is the whole design on one page. The [charter](./charter) has the
reasoning in full; this is the specification and what each part is there
to teach.

[![CyberRack v1.0: rack elevation, network architecture, compute cluster, storage appliance, VLAN plan, power budget and hardware summary](/img/cyberrack-v1.png)](/img/cyberrack-v1.png)

*The diagram is dense. Open it in a new tab for a readable version; it's
designed to be looked at large rather than squinted at on a phone.*

## What it is

Three matched mini PCs running a **Proxmox VE** cluster, a dedicated
storage appliance running **TrueNAS SCALE**, an **OPNsense** firewall, and
a managed switch, in a 10-inch, 10U rack. Roughly the footprint of a large
shoebox, drawing about 125 watts idle.

<div className="labTable">

| Domain | Standard | Qty | Est. cost |
|---|---|---|---|
| Compute | Lenovo ThinkCentre M920q (i5-8500T, 64 GB, 1.5 TB NVMe) | 3 | $1,950 |
| Storage | AOOSTAR WTR Pro (N100, 32 GB, 2× 4 TB) | 1 | $480 |
| Firewall | Intel N100 mini PC | 1 | $160 |
| Switch | MikroTik CRS310-8G+2S+IN | 1 | $179 |
| Rack | 10-inch rack, panel, shelves, cables | 1 | $150 |
| Power | APC BX1000M UPS (1000 VA / 600 W) | 1 | $179 |

</div>

**Estimated total: $2,898.** Prices are from the used market and move
around; treat them as a shape rather than a quote, and keep five to ten
percent back for the part that arrives broken.

Worth noticing: [the charter](./charter) sets a target of **$2,500**, and
this bill of materials comes to $2,898. That gap is left visible on
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
- **The UPS.** The one I would not skip, because it protects the storage
  that everything else depends on.

## Living with it

Around **125 watts idle**, under 300 at peak. Quiet enough for a room you
sleep in, which is the constraint that ruled out secondhand rack servers
despite them being cheaper for the same specification.

Work out your own electricity cost before committing: 125 watts running
continuously is roughly 90 kilowatt-hours a month, and only you know what
that costs where you live.

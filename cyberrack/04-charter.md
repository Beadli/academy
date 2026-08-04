---
title: "The project charter"
sidebar_position: 4
---

# CyberRack project charter

The complete design document behind [the v1.0 build](./build), published
as written rather than rewritten for the course.

Two reasons it's here in full. First, if you're building your own version
you should be able to see the reasoning, disagree with parts of it, and
fork it. Second, it's a worked example of the thing this course keeps
insisting matters: infrastructure documentation with a stated mission,
explicit design principles, scope boundaries, a technology baseline,
success criteria, and a decision rule for future changes.

Most people have never seen one. If you're heading for a role where you'll
be asked to write a design document, read this for its shape as much as
its content.

:::note[Its voice is different on purpose]
This reads like a formal charter rather than a lesson, because that's what
it is. Course modules talk to you; this specifies a system.
:::

:::warning[It contradicts itself in one place, and that's left in]
§5.4 requires the platform to be portable and easy to relocate. §7's rack
elevation then puts **UPS and power distribution** in U1 of a ten-inch
rack. Read those together and they don't hold: the UPS class that phrase
usually implies is a lead-acid tower that neither fits a ten-inch rack nor
gets carried anywhere.

The charter is published unedited, so the contradiction stays. It's also
the most useful thing in here for anyone who has to write one of these.
Requirements documents contradict themselves constantly, almost always
between a section about *qualities* and a section about *parts*, and the
contradiction is invisible until someone tries to buy something.

[The build page](./build#power-and-the-portability-trap) resolves this one
by asking what the battery is actually for. Read it as a worked example of
catching a requirements conflict at the specification stage, which is
where it is cheap.
:::

---

## CyberRack Project Charter

### Enterprise Mini Infrastructure Platform

**Version:** 1.0
**Status:** Approved Project North Star
**Target Budget:** $2,500 USD
**Target Audience:** College students, early-career IT professionals, cybersecurity students, and self-directed infrastructure learners

---

## 1. Mission Statement

> **Build a lab that demonstrates modern enterprise infrastructure using the fewest possible devices while maximizing learning, portability, and long-term upgradeability.**

CyberRack is an intentionally designed miniature enterprise infrastructure platform.

It is not intended to be the largest homelab, the fastest server environment, or a collection of unrelated technology products. Its purpose is to provide a compact, affordable, reproducible, and professionally documented platform for learning modern infrastructure, networking, cybersecurity, storage, identity, automation, and platform engineering.

Every hardware purchase, software deployment, and architectural decision must support a clearly defined learning objective.

---

## 2. Project Vision

CyberRack should operate like a miniature enterprise datacenter while remaining small enough for a desk, dorm room, apartment, home office, or classroom.

Although physically compact, the platform should demonstrate the technologies and operational practices found in modern organizations, including:

* Clustered virtualization
* Enterprise networking
* Network segmentation
* Shared storage
* Centralized identity
* Public key infrastructure
* Security monitoring
* Network intrusion detection
* Centralized logging
* Backup and disaster recovery
* Infrastructure automation
* Containerized applications
* Observability
* Configuration management
* Infrastructure as Code
* Technical documentation

The platform should be useful both as a learning environment and as a professional portfolio project.

---

## 3. Project Objectives

CyberRack must accomplish the following objectives:

1. Provide hands-on experience with modern enterprise infrastructure technologies.
2. Fit within an initial project budget of approximately $2,500.
3. Use a small number of standardized, power-efficient devices.
4. Remain quiet enough for use in a bedroom, dorm, library workspace, or home office.
5. Support incremental upgrades without requiring a complete rebuild.
6. Demonstrate professional infrastructure design and operational practices.
7. Be reproducible by another student using the project documentation.
8. Produce artifacts that can be included in a professional portfolio.
9. Encourage automation instead of permanent manual administration.
10. Provide a safe environment for cybersecurity experimentation and defensive testing.

---

## 4. Budget Principle

The initial CyberRack build should target a total project cost of no more than:

> **$2,500 USD**

The budget should include:

* Compute nodes
* Storage appliance
* Firewall appliance
* Managed network switch
* Rack
* Patch panel
* Cabling
* Power distribution
* UPS
* Memory and storage upgrades
* Required adapters and mounting hardware

Optional future upgrades are not required to fit inside the initial $2,500 budget.

Because used-equipment prices fluctuate, the final bill of materials should include a contingency reserve of approximately 5–10 percent.

A purchase should not be made solely because money remains in the budget. Unused budget should be preserved for failures, replacement parts, storage expansion, or future upgrades.

---

## 5. Core Design Principles

### 5.1 Learning First

Learning takes priority over maximum performance.

Every hardware or software component must teach one or more transferable enterprise skills.

Examples include:

* Virtualization
* Network segmentation
* Firewall administration
* Identity management
* Storage administration
* Backup and recovery
* Monitoring
* Automation
* Security operations
* Container orchestration

Hardware exists to support learning. Hardware acquisition is not the primary objective of the project.

---

### 5.2 Fewest Practical Devices

CyberRack should use the smallest number of physical devices that can still demonstrate the required enterprise concepts.

Device consolidation is encouraged when it:

* Reduces cost
* Reduces power usage
* Reduces cable complexity
* Simplifies maintenance
* Preserves educational value

Additional devices should only be introduced when they provide a meaningful architectural or educational benefit.

---

### 5.3 Simplicity Before Complexity

The simplest architecture that satisfies the learning objectives should be preferred.

Avoid unnecessary:

* Servers
* Appliances
* Network hops
* Management consoles
* Duplicate applications
* Storage layers
* Authentication systems
* Monitoring systems

Complexity should be introduced deliberately rather than accidentally.

---

### 5.4 Small Form Factor

The platform should remain:

* Desk-friendly
* Dorm-friendly
* Apartment-friendly
* Quiet
* Portable
* Energy efficient
* Easy to relocate

The preferred physical format is a compact 10-inch rack.

The initial rack should target approximately 10U of usable space.

---

### 5.5 Standardization

Identical hardware should be used whenever practical.

The compute cluster should use three matching systems with equivalent:

* Processors
* Memory
* Storage
* Network interfaces
* Firmware
* BIOS settings
* Hypervisor versions

Standardization reduces troubleshooting time and reflects normal enterprise infrastructure practices.

---

### 5.6 Enterprise Architecture

CyberRack should model enterprise design practices rather than relying on shortcuts.

Examples include:

* VLAN segmentation
* Centralized authentication
* Role-based access control
* Least privilege
* Certificate-based encryption
* Dedicated management networks
* Monitoring and alerting
* Automated backups
* Change documentation
* Recovery testing
* Configuration management
* Version control

---

### 5.7 Open Standards

Preference should be given to technologies that implement widely used and interoperable standards.

Examples include:

* Ethernet
* VLAN
* IPv4 and IPv6
* DNS
* DHCP
* NTP
* LDAP
* Kerberos
* SAML
* OAuth 2.0
* OpenID Connect
* TLS
* SSH
* NFS
* SMB
* iSCSI
* SNMP
* Syslog
* REST APIs

Open standards reduce vendor dependency and improve the transferability of learned skills.

---

### 5.8 Upgrade Without Rebuilding

The architecture must support incremental growth.

Future improvements should extend or replace individual components without requiring the entire platform to be redesigned.

Examples include:

* Increasing memory
* Replacing NVMe drives
* Adding storage capacity
* Adding 10GbE interfaces
* Adding a GPU-enabled node
* Introducing Kubernetes
* Adding redundant storage
* Adding high availability
* Replacing the firewall platform
* Adding cloud integration

---

### 5.9 Replaceability

No individual technology should become an irreplaceable dependency.

Each major component should communicate through documented standards and interfaces.

A firewall, switch, compute node, storage platform, monitoring system, or identity provider should be replaceable without invalidating the entire architecture.

---

### 5.10 Reproducibility

Another student should be able to recreate CyberRack using the project repository.

The documentation must include:

* Project charter
* Bill of materials
* Rack elevation
* Network topology
* VLAN plan
* IP addressing plan
* Storage design
* Power design
* Installation procedures
* Configuration procedures
* Automation scripts
* Backup procedures
* Recovery procedures
* Upgrade procedures
* Architecture Decision Records

Documentation is part of the infrastructure.

---

## 6. Scope

### 6.1 Included in Scope

CyberRack includes the design and implementation of:

* A three-node virtualization cluster
* A dedicated shared-storage appliance
* A dedicated firewall appliance
* A managed network switch
* A segmented network architecture
* Centralized identity services
* Certificate services
* Centralized monitoring
* Security monitoring
* Network intrusion detection
* Automated virtual-machine backups
* Containerized application hosting
* Configuration automation
* Version-controlled documentation
* Recovery testing
* A compact rack and power system

---

### 6.2 Out of Scope for Version 1.0

The following capabilities are not required for the initial build:

* Production-grade uptime guarantees
* Fully redundant power
* Fully redundant switching
* Dual storage controllers
* Enterprise support contracts
* Large-scale GPU computing
* Multi-site disaster recovery
* Public cloud dependency
* Full Ceph deployment
* Production Kubernetes
* Internet-facing production services
* Large-scale surveillance storage
* High-end enterprise SAN hardware

These capabilities may be explored in later phases when they provide clear educational value.

---

## 7. Physical Architecture

The preferred rack format is:

> **10-inch, approximately 10U mini rack**

The rack should emphasize:

* Density
* Organization
* Portability
* Cable management
* Airflow
* Serviceability
* Maintainability
* Visual clarity

A reference rack layout is:

| Rack Unit | Component                           |
| --------- | ----------------------------------- |
| U10       | Monitoring or status display        |
| U9        | Intel N100 firewall appliance       |
| U8        | MikroTik managed switch             |
| U7        | Brush or cable-management panel     |
| U6        | 12-port CAT6 keystone patch panel   |
| U5        | Lenovo ThinkCentre M920q — Atlas    |
| U4        | Lenovo ThinkCentre M920q — Hermes   |
| U3        | Lenovo ThinkCentre M920q — Daedalus |
| U2        | AOOSTAR WTR Pro storage appliance   |
| U1        | UPS and power distribution          |

The exact mounting arrangement may change based on equipment dimensions, airflow, rack depth, and available mounting accessories.

---

## 8. Technology Selection Philosophy

Technology selections are evaluated using the following questions.

### 8.1 Does It Teach an Enterprise Skill?

Every technology must answer:

> **What enterprise skill does this teach?**

If the answer is unclear, the technology should not become part of CyberRack.

---

### 8.2 Is It Widely Applicable?

Preference should be given to technologies with skills that transfer to:

* Enterprise IT
* Cybersecurity
* Cloud engineering
* DevOps
* Platform engineering
* Systems administration
* Network engineering
* Security operations

---

### 8.3 Does It Fit the Budget?

The technology must provide reasonable educational value for its total cost.

Total cost includes:

* Hardware
* Licensing
* Memory
* Storage
* Networking
* Power consumption
* Required accessories
* Maintenance
* Replacement availability

---

### 8.4 Can It Scale?

The selected technology should remain useful as the student advances.

The preferred solution should support both basic learning and more advanced future implementation.

---

### 8.5 Is It Supported by a Strong Community?

Preference should be given to technologies with:

* Active documentation
* Large user communities
* Available troubleshooting resources
* Regular security updates
* Accessible installation media
* Broad hardware compatibility

---

## 9. Technology Baseline — Version 1.0

CyberRack intentionally standardizes on a selected technology stack.

These selections are strategic commitments for Version 1.0 and should only change when there is a compelling architectural, financial, security, or educational reason.

The baseline is selected according to:

* Enterprise relevance
* Learning value
* Community support
* Hardware availability
* Affordability
* Long-term sustainability
* Interoperability
* Upgradeability

---

## 10. Compute Platform

### 10.1 Standard Compute Hardware

The standard CyberRack compute platform is:

> **Lenovo ThinkCentre M920q Tiny**

Three identical Lenovo ThinkCentre M920q systems will form the Proxmox virtualization cluster.

#### Minimum Standard Configuration per Node

* Intel Core i5-8500T
* Six physical CPU cores
* 64 GB DDR4 memory
* 512 GB NVMe operating-system drive
* 1 TB NVMe virtual-machine storage drive
* Intel Gigabit Ethernet
* Intel virtualization extensions
* Intel VT-d support
* Intel vPro where available

#### Preferred Configuration

* Intel Core i7-8700T
* 64 GB DDR4 memory
* 512 GB NVMe operating-system drive
* 1–2 TB NVMe virtual-machine storage drive
* PCIe riser
* 2.5GbE or 10GbE network interface

#### Selection Rationale

The Lenovo ThinkCentre M920q was selected because it provides:

* Enterprise-class build quality
* Low power consumption
* Quiet operation
* Compact dimensions
* Strong Proxmox compatibility
* 64 GB memory support
* Intel virtualization support
* Optional PCIe expansion
* A large used-equipment market
* Accessible replacement parts
* Consistent hardware standardization
* A practical upgrade path to faster networking

---

### 10.2 Compute Node Names

The three compute nodes will use the following hostnames:

| Node     | Hardware                 | Primary Learning Role                                             |
| -------- | ------------------------ | ----------------------------------------------------------------- |
| Atlas    | Lenovo ThinkCentre M920q | Identity, directory services, PKI, DNS and foundational services  |
| Hermes   | Lenovo ThinkCentre M920q | Security monitoring, logging, IDS, SIEM and firewall laboratories |
| Daedalus | Lenovo ThinkCentre M920q | Containers, development, automation, CI/CD and Kubernetes         |

These roles describe the preferred workload placement but do not create permanent physical dependencies.

Virtual machines and containers should remain migratable between cluster nodes.

---

## 11. Virtualization Platform

The primary virtualization platform is:

> **Proxmox Virtual Environment**

Proxmox VE is the foundation of CyberRack.

The three M920q systems will operate as one Proxmox VE cluster with a shared management plane.

### 11.1 Required Capabilities

The cluster should demonstrate:

* Centralized management
* Cluster membership
* Quorum
* Virtual machines
* Linux containers
* Storage integration
* Snapshots
* Templates
* Cloning
* Live migration
* Backup integration
* Role-based access
* Virtual networking
* Resource monitoring
* High availability concepts

### 11.2 Future Capabilities

Later phases may introduce:

* Proxmox high availability
* Software-defined networking
* Automated node deployment
* API-based provisioning
* Terraform integration
* Ceph as an educational experiment
* Cluster-aware monitoring
* Automated workload balancing

The project intentionally standardizes on Proxmox rather than requiring a proprietary virtualization management appliance.

---

## 12. Storage Platform

### 12.1 Storage Hardware

The preferred dedicated storage appliance is:

> **AOOSTAR WTR Pro**

#### Initial Configuration

* Intel N100 processor
* 32 GB memory
* Dual 2.5GbE networking
* TrueNAS SCALE
* Two matched 4 TB NAS drives
* ZFS mirror
* Approximately 4 TB of usable mirrored storage

Additional drives may be added when the hardware configuration and budget allow.

### 12.2 Storage Operating System

The primary storage operating system is:

> **TrueNAS SCALE**

### 12.3 Storage Technologies

The storage platform should demonstrate:

* ZFS
* Storage pools
* Datasets
* NFS
* SMB
* iSCSI
* Snapshots
* Replication
* Data integrity
* Storage monitoring
* Capacity management
* File permissions
* Network storage security

### 12.4 Storage Architecture Principle

Storage must remain independent of the compute cluster.

The failure, replacement, or maintenance of one Proxmox node should not eliminate access to the primary shared-storage platform.

The initial design should favor simplicity and recoverability over maximum storage performance.

---

## 13. Firewall Platform

### 13.1 Firewall Hardware

The preferred firewall platform is:

> **Intel N100 multi-port firewall appliance**

The appliance should include:

* At least four Ethernet interfaces
* Preferably 2.5GbE interfaces
* Intel network controllers where possible
* Replaceable storage
* Sufficient memory for firewall, VPN, and IDS laboratory workloads

### 13.2 Firewall Operating System

The primary firewall operating system is:

> **OPNsense**

### 13.3 Learning Objectives

The firewall platform should teach:

* IPv4 and IPv6 routing
* VLAN interfaces
* Firewall rules
* Stateful inspection
* Network Address Translation
* DHCP
* DNS forwarding
* VPN
* WireGuard
* IPsec
* Traffic shaping
* Logging
* IDS/IPS
* Certificate management
* Reverse-proxy concepts
* Multi-WAN concepts
* Network isolation

The firewall should remain vendor-independent and should not require a proprietary cloud-management ecosystem.

---

## 14. Switching Platform

The preferred switching platform is:

> **MikroTik CRS310-8G+2S+IN**

### 14.1 Required Capabilities

The switch provides:

* Eight 2.5 Gigabit Ethernet ports
* Two 10 Gigabit SFP+ interfaces
* VLAN support
* Layer 2 switching
* Link aggregation
* Spanning Tree
* Port isolation
* Traffic monitoring
* MikroTik RouterOS and SwitchOS learning
* A future 10GbE upgrade path

### 14.2 Selection Rationale

The MikroTik CRS310-8G+2S+IN was selected because it provides:

* Multi-gigabit connectivity
* 10GbE uplinks
* Strong learning value
* Enterprise-style switching concepts
* Compact dimensions
* Low power consumption
* Good price-to-capability ratio
* Freedom from a single-vendor ecosystem

The switching platform should expose enterprise networking concepts without requiring enterprise hardware pricing.

---

## 15. Network Segmentation Baseline

CyberRack should use VLANs to separate management, workloads, backups, monitoring, guests, and untrusted devices.

The initial VLAN structure is:

| VLAN | Name         | Example Subnet  | Purpose                                                          |
| ---: | ------------ | --------------- | ---------------------------------------------------------------- |
|   10 | Management   | 192.168.10.0/24 | Proxmox, switch, firewall, storage and administrative interfaces |
|   20 | Servers      | 192.168.20.0/24 | Virtual machines, containers and internal applications           |
|   30 | Backup       | 192.168.30.0/24 | Backup, replication and recovery traffic                         |
|   40 | Monitoring   | 192.168.40.0/24 | Logging, metrics, SIEM and observability platforms               |
|   50 | Guest        | 192.168.50.0/24 | Internet-only guest access                                       |
|   60 | IoT          | 192.168.60.0/24 | Isolated or untrusted devices                                    |
|   70 | Security Lab | 192.168.70.0/24 | Cybersecurity testing, attack simulation and vulnerable systems  |

The exact addressing may change, but functional separation should remain.

Traffic between VLANs must be controlled through documented firewall policies.

---

## 16. Identity Platform

The primary identity technologies are:

* Microsoft Active Directory Domain Services
* Keycloak
* Microsoft Active Directory Certificate Services

### 16.1 Learning Objectives

The identity platform should demonstrate:

* LDAP
* Kerberos
* DNS integration
* Organizational Units
* Group Policy
* Role-based access
* Service accounts
* Group Managed Service Accounts
* Single Sign-On
* SAML
* OAuth 2.0
* OpenID Connect
* Multi-factor authentication
* Certificate enrollment
* Certificate templates
* Certificate revocation
* Trust relationships
* Identity federation

### 16.2 Identity Principle

Active Directory, Keycloak, and AD CS should each have a defined purpose.

Duplicate identity services should not be deployed without a specific learning objective.

---

## 17. Public Key Infrastructure

Microsoft Active Directory Certificate Services will provide the initial enterprise PKI environment.

The PKI should demonstrate:

* Offline root CA concepts
* Enterprise subordinate CA
* Certificate templates
* Server certificates
* User certificates
* Computer certificates
* TLS
* Smart-card concepts
* Certificate revocation lists
* Auto-enrollment
* Certificate lifecycle management
* Private-key protection
* Certificate renewal
* Certificate inventory

PKI should support other CyberRack services rather than existing as an isolated laboratory.

---

## 18. Monitoring and Observability Platform

The primary monitoring technologies are:

* Prometheus
* Grafana
* Uptime Kuma
* Alertmanager

### 18.1 Learning Objectives

The monitoring platform should demonstrate:

* Metrics collection
* Dashboards
* Service availability
* Node monitoring
* Capacity planning
* Alerting
* Threshold configuration
* Trend analysis
* Infrastructure health
* Storage utilization
* Network visibility
* Backup status
* Cluster health

Monitoring should be introduced early rather than added only after failures occur.

---

## 19. Security Monitoring Platform

The primary security monitoring technologies are:

* Wazuh
* Suricata

Future technologies may include:

* Zeek
* CrowdSec
* OpenSearch
* Vulnerability-management integrations
* Threat-intelligence feeds

### 19.1 Learning Objectives

The security platform should demonstrate:

* Security Information and Event Management
* Host-based intrusion detection
* File-integrity monitoring
* Log analysis
* Network intrusion detection
* Traffic analysis
* Alert triage
* Threat hunting
* Vulnerability detection
* Endpoint visibility
* Security dashboards
* Incident response workflows

Security monitoring should be integrated with the broader infrastructure rather than deployed as an isolated product demonstration.

---

## 20. Backup Platform

The primary virtualization backup platform is:

> **Proxmox Backup Server**

### 20.1 Responsibilities

Proxmox Backup Server should provide:

* Virtual-machine backups
* Container backups
* Incremental backups
* Deduplication
* Compression
* Retention policies
* Backup verification
* Encryption
* Scheduled jobs
* Recovery testing

### 20.2 Backup Policy

The initial backup policy should include:

* Daily incremental backups
* Weekly full validation or verification
* Monthly offline or off-system copies where practical
* Regular virtual-machine restore tests
* Configuration backups for the firewall, switch, storage appliance, and Proxmox cluster
* Documentation of recovery procedures

A backup is not considered reliable until it has been successfully restored.

---

## 21. Automation Platform

The primary automation technologies are:

* Git
* Gitea
* Ansible

Future automation technologies may include:

* Terraform
* Packer
* OpenTofu
* GitOps tools
* CI/CD runners
* Proxmox API automation

### 21.1 Automation Objectives

Automation should eventually support:

* Virtual-machine provisioning
* Container deployment
* Operating-system configuration
* User creation
* Package installation
* Certificate deployment
* Monitoring-agent installation
* Backup configuration
* Network configuration
* Configuration validation
* Documentation generation

Manual configuration should gradually decrease as CyberRack matures.

Automation should be version controlled and documented.

---

## 22. Container Platform

The initial container platform is:

> **Docker**

The future orchestration platform is:

> **Kubernetes using k3s**

### 22.1 Container Objectives

The container platform should demonstrate:

* Container images
* Registries
* Volumes
* Container networking
* Secrets
* Compose files
* Service health
* Reverse proxies
* Persistent storage
* Application deployment
* CI/CD
* Kubernetes fundamentals
* High-availability concepts
* GitOps concepts

Containers should become the preferred deployment method for lightweight services when appropriate.

Virtual machines should remain available where operating-system isolation or specialized networking is required.

---

## 23. Documentation Platform

The preferred documentation technologies are:

* Markdown
* Mermaid
* Draw.io
* Git
* Gitea
* MkDocs in a future phase

### 23.1 Required Documentation

The project repository should contain:

* Project charter
* Requirements
* Bill of materials
* Architecture Decision Records
* Rack elevation
* Network topology
* VLAN plan
* IP addressing plan
* Firewall rule matrix
* Storage design
* Virtualization design
* Identity design
* PKI design
* Monitoring design
* Backup strategy
* Build procedures
* Recovery procedures
* Upgrade procedures
* Security procedures
* Lessons learned

Documentation must be maintained as the environment changes.

Outdated documentation should be treated as an infrastructure defect.

---

## 24. Power, Noise, and Thermal Requirements

CyberRack should target:

* Approximately 80–150 watts at idle
* Less than approximately 300 watts during normal peak activity
* Quiet operation suitable for a bedroom, dorm, or office
* No dependency on high-speed server fans
* No requirement for specialized cooling
* Adequate airflow between rack components
* UPS protection for all critical components

Power bricks and adapters should be organized safely.

USB-C power conversion may be used only when voltage, amperage, connector polarity, and total power capacity have been verified.

Reliability takes priority over eliminating every individual power adapter.

---

## 25. Security Principles

CyberRack must follow the following security principles:

* Default-deny inter-VLAN routing
* Least-privilege access
* Dedicated management network
* Strong administrator credentials
* Multi-factor authentication where supported
* Certificate-based encryption
* No unencrypted administrative interfaces
* Centralized logging
* Regular patching
* Secure secrets storage
* Restricted backup access
* Documented firewall rules
* No direct exposure of management interfaces to the internet
* Separation of vulnerable laboratory systems from trusted networks
* Regular recovery testing

Cybersecurity experimentation must be contained within authorized laboratory networks.

---

## 26. Technology Governance

### 26.1 Standardize

Use one preferred solution whenever possible.

Avoid maintaining multiple technologies that solve the same problem unless the comparison itself is an explicit learning exercise.

---

### 26.2 Document Decisions

Major technology choices must be recorded through Architecture Decision Records.

An ADR should include:

* Decision
* Context
* Options considered
* Rationale
* Consequences
* Risks
* Reconsideration triggers

---

### 26.3 Avoid Unplanned Technology Sprawl

New applications should not be deployed simply because they are popular or available.

Before adding a technology, document:

1. The problem it solves.
2. The enterprise skill it teaches.
3. Its resource requirements.
4. Its security implications.
5. Its backup requirements.
6. Its dependencies.
7. Whether an existing platform already provides the capability.

---

### 26.4 Preserve Replaceability

Each technology should use documented protocols and interfaces whenever possible.

Replacement of one component should not require a complete platform redesign.

---

### 26.5 Control Scope

The project should prioritize completing functional capabilities before introducing additional platforms.

A smaller, well-documented, recoverable environment is preferred over a larger environment with incomplete configuration.

---

## 27. CyberRack Version 1.0 Reference Architecture

| Domain                   | Approved Standard                                 |
| ------------------------ | ------------------------------------------------- |
| Compute                  | 3× Lenovo ThinkCentre M920q Tiny                  |
| Minimum CPU              | Intel Core i5-8500T                               |
| Memory                   | 64 GB DDR4 per compute node                       |
| Hypervisor               | Proxmox VE cluster                                |
| Storage hardware         | AOOSTAR WTR Pro                                   |
| Storage operating system | TrueNAS SCALE                                     |
| Storage protocols        | ZFS, NFS, SMB and iSCSI                           |
| Firewall hardware        | Intel N100 multi-port appliance                   |
| Firewall software        | OPNsense                                          |
| Switching                | MikroTik CRS310-8G+2S+IN                          |
| Backup                   | Proxmox Backup Server                             |
| Identity                 | Active Directory and Keycloak                     |
| PKI                      | Microsoft Active Directory Certificate Services   |
| Monitoring               | Prometheus, Grafana, Uptime Kuma and Alertmanager |
| Security monitoring      | Wazuh                                             |
| Network security         | Suricata                                          |
| Automation               | Git, Gitea and Ansible                            |
| Future automation        | Terraform or OpenTofu                             |
| Containers               | Docker                                            |
| Future orchestration     | Kubernetes using k3s                              |
| Documentation            | Markdown, Mermaid, Draw.io, Git and MkDocs        |
| Rack                     | Approximately 10U, 10-inch mini rack              |
| Power protection         | UPS and managed power distribution                |

---

## 28. Success Criteria

CyberRack Version 1.0 will be considered successful when it can demonstrate the following capabilities.

### 28.1 Physical Infrastructure

* All equipment is securely mounted or positioned.
* Cabling is labeled and organized.
* Power consumption is documented.
* The system operates within acceptable temperature and noise limits.
* The rack can be moved without requiring a complete rebuild.

### 28.2 Virtualization

* Three Proxmox nodes operate as one cluster.
* Cluster quorum is healthy.
* Virtual machines and containers can be created from templates.
* Workloads can be migrated between nodes.
* Shared storage is available to the cluster.
* Proxmox Backup Server successfully backs up and restores workloads.

### 28.3 Networking

* VLANs are implemented.
* Inter-VLAN routing is controlled by OPNsense.
* Management interfaces are isolated.
* Guest and IoT networks are restricted.
* Firewall rules are documented.
* Remote access uses a secure VPN.

### 28.4 Storage

* TrueNAS SCALE provides shared storage.
* ZFS snapshots are scheduled.
* NFS or iSCSI is available to Proxmox.
* SMB is available for administrative file storage.
* Storage recovery procedures are documented and tested.

### 28.5 Identity

* Active Directory provides centralized Windows identity.
* Keycloak provides SAML or OpenID Connect services.
* AD CS issues certificates.
* At least one application uses centralized authentication.
* At least one service uses an internally issued TLS certificate.

### 28.6 Security

* Wazuh receives endpoint events.
* Suricata analyzes network traffic.
* Security alerts are visible in a central dashboard.
* Vulnerable laboratory systems are isolated.
* An incident-response exercise is documented.

### 28.7 Monitoring

* Proxmox nodes are monitored.
* Storage health is monitored.
* Firewall and switch availability are monitored.
* Dashboards display resource use and service status.
* At least one meaningful alert is configured and tested.

### 28.8 Automation

* Git stores configuration and documentation.
* Ansible performs at least one repeatable infrastructure deployment.
* A virtual machine or service can be rebuilt using documented automation.
* Secrets are not stored in plaintext repositories.

### 28.9 Documentation

* Another person can understand the architecture from the repository.
* The bill of materials matches the physical environment.
* IP addresses and VLANs are documented.
* Backup and recovery procedures are current.
* Major decisions are recorded through ADRs.

---

## 29. Project Roadmap

### Phase 1 — Foundation

Objectives:

* Finalize bill of materials
* Acquire hardware
* Assemble rack
* Install UPS and power distribution
* Install OPNsense
* Configure MikroTik switch
* Create VLANs
* Install Proxmox on three M920q systems
* Form the Proxmox cluster
* Establish the Git repository
* Document the physical and network architecture

---

### Phase 2 — Storage and Recovery

Objectives:

* Install TrueNAS SCALE
* Create ZFS storage pools
* Configure NFS, SMB and optional iSCSI
* Integrate shared storage with Proxmox
* Deploy Proxmox Backup Server
* Create backup schedules
* Test virtual-machine restoration
* Document disaster-recovery procedures

---

### Phase 3 — Enterprise Identity

Objectives:

* Deploy Active Directory
* Configure DNS and NTP
* Deploy AD CS
* Create certificate templates
* Deploy Keycloak
* Integrate an application with SSO
* Implement role-based access
* Document identity and PKI architecture

---

### Phase 4 — Monitoring and Security

Objectives:

* Deploy Prometheus
* Deploy Grafana
* Deploy Uptime Kuma
* Deploy Wazuh
* Deploy Suricata
* Configure centralized logging
* Create dashboards
* Test alerts
* Perform a documented security exercise

---

### Phase 5 — Automation

Objectives:

* Deploy Gitea
* Create Ansible inventory
* Automate operating-system configuration
* Automate monitoring-agent deployment
* Automate certificate deployment
* Automate backup validation
* Introduce Terraform or OpenTofu where appropriate
* Establish configuration review practices

---

### Phase 6 — Containers and Platform Engineering

Objectives:

* Deploy Docker services
* Implement container registries
* Deploy a k3s cluster
* Integrate persistent storage
* Implement CI/CD
* Explore GitOps
* Document container and Kubernetes operations

---

### Phase 7 — Advanced Expansion

Possible future objectives:

* Upgrade selected links to 10GbE
* Add higher-capacity storage
* Add a GPU node
* Test Proxmox high availability
* Explore Ceph
* Add a second storage appliance
* Implement off-site replication
* Integrate public cloud services
* Explore zero-trust architecture
* Add automated compliance checks

Expansion is optional and must remain aligned with the project mission.

---

## 30. Definition of Done

CyberRack is not considered complete merely because all hardware has been installed.

A phase is complete only when:

* The capability works.
* The configuration is documented.
* Monitoring is enabled.
* Backup requirements are addressed.
* Recovery has been tested.
* Security implications are understood.
* The learning outcome is recorded.
* Another person could reproduce the result.

---

## 31. Final Definition of Success

CyberRack succeeds when it becomes more than a homelab.

It should function as:

* A learning platform
* A cybersecurity range
* A miniature enterprise datacenter
* A professional portfolio project
* An architecture reference
* An automation laboratory
* A documentation repository
* A disaster-recovery exercise platform
* A repeatable blueprint for other students

The project is successful not when there is nothing left to add, but when every remaining addition must justify itself through a clear educational or architectural purpose.

Every upgrade should increase knowledge, capability, resilience, or maintainability—not merely specifications.

---

## 32. North Star Decision Rule

When evaluating any future purchase, deployment, or architecture change, ask:

1. What enterprise skill does this teach?
2. Does it reduce or unnecessarily increase complexity?
3. Does it preserve the small-form-factor objective?
4. Does it fit the project budget or documented upgrade plan?
5. Can it be replaced later?
6. Can it be automated?
7. Can it be monitored?
8. Can it be backed up and recovered?
9. Can another student reproduce it?
10. Does it move CyberRack closer to its mission?

If the answer to these questions is unclear, the proposed change should not be adopted until its purpose is better defined.


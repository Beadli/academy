---
title: "Module 12: Monitoring and detection"
sidebar_position: 0
---

# Module 12: Monitoring and detection

<div className="stackLine">

Wazuh · Sysmon · Suricata

</div>

Lesson 0.2 described a security analyst as the person who watches the SIEM,
triages alerts and decides what is real, and said the scanner-on-the-domain-
controller story from lesson 0.1 was a day in their life.

**This module puts you in that seat**, in a lab where the attacker is you.

You have spent eleven modules building things that produce logs. A domain
controller authenticating people, a firewall dropping packets, a Git server
accepting pushes, a certificate authority issuing certificates. None of it is
being watched. That changes here.

What's in it:

- **12.1** collecting logs is not detecting
- **12.2** install the manager, enrol your first agent
- **12.3** Sysmon: make Windows worth watching
- **12.4** read an alert, then write a rule
- **12.5** tuning, and the queue nobody reads
- **12.6** detect your own scanner
- **12.7** detecting without decrypting
- **12.8** alerting on absence
- **12.9** the indexer and dashboard
- **12.10** Grafana, and the difference between events and metrics
- **12.11** journal entry
- **12.12** checkpoint

## Two paths, and both are real detection work

This module forks by tier more sharply than any other, because a SIEM is the
hungriest thing you will install.

**Everyone builds the whole SIEM**: the manager that detects, and the indexer
and dashboard that make it searchable. You enrol agents, write rules, tune
them, and then investigate with the same interface an analyst uses at work.

Lessons 12.2 to 12.8 deliberately have you read alerts as JSON at the command
line before 12.9 puts a dashboard in front of them. That order is on purpose.
You will see the raw event, the rule that matched it, and why, which is what
the dashboard is drawing on. **Analysts who only ever saw the dashboard tend
to be the ones who cannot explain why an alert fired.**

**Tier 3 adds a Suricata network sensor** in 12.7, and **Grafana and Prometheus**
in 12.10.

:::warning[UBNT01 needs more memory, and this one is not optional]
UBNT01 was built in lesson 6.1 with 6 GB, and that note said a SIEM would be
hungry. It undersold it.

**Wazuh's own guidance is 4 GB for the manager alone**, and the full stack's
published requirement is 4 CPU cores, 8 GB and 50 GB of disk. UBNT01 is already
running Gitea, Keycloak, step-ca and nginx.

**Take UBNT01 to 8 GB before you start**, and to 10 or 12 if your host can
spare it. Shut it down, change the memory in the hypervisor, start it again;
two minutes, the same way Module 9 grew DC01.

Those published figures are sized for thousands of endpoints and you have
four. Lesson 12.9 tunes the indexer's heap down accordingly, which is what
makes this fit on a laptop. **On a 16 GB machine you will need to shut DC02
and KALI01 down while you work**, which is what lesson 0.3's "On?" column was
always for.
:::

## What this module is really teaching

Not a product. Wazuh is one SIEM and your employer may run a different one.

The transferable part is the reasoning: what a log is worth, why raw
collection is not detection, how a rule decides something is interesting, and
why an alert queue nobody reads is worse than no alerts at all.

Every one of those survives a change of vendor. The XML syntax does not.

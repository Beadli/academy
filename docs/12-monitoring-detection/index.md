---
title: "Module 12: Monitoring and detection"
sidebar_position: 0
---

# Module 12: Monitoring and detection

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
- **12.9** dashboards, and what they are actually for
- **12.10** journal entry
- **12.11** checkpoint

## Two paths, and both are real detection work

This module forks by tier more sharply than any other, because a SIEM is the
hungriest thing you will install.

**Everyone runs the Wazuh manager**, which is the part that receives events,
matches them against rules, and raises alerts. You enrol agents, write rules,
tune them, and read what comes out. That is detection engineering, all of it.

**Tier 3 adds the indexer and dashboard**, plus Grafana and a Suricata sensor.
That is the searching and visualising layer.

If you are on Tier 1 or 2 you will read alerts as JSON at the command line
rather than clicking a dashboard. **That is not the consolation prize.** You
will see the raw event, the rule that matched it, and why, which is exactly
what the dashboard is drawing on and exactly what you need to understand to
write rules that work. Analysts who only ever saw the dashboard tend to be the
ones who cannot explain why an alert fired.

:::warning[UBNT01 needs more memory, and this one is not optional]
UBNT01 was built in lesson 6.1 with 6 GB, and that note said a SIEM would be
hungry. It undersold it.

**Wazuh's own guidance is 4 GB for the manager alone**, and UBNT01 is already
running Gitea, Keycloak, step-ca and nginx. **Take it to 8 GB before you
start.** Shut it down, change the memory in the hypervisor, start it again;
two minutes, the same way Module 9 grew DC01.

**Tier 3 wants 12 GB or more**, because the full stack's published requirement
is 4 CPU cores, 8 GB of RAM and 50 GB of disk *on its own*. Lesson 12.9 shows
how to tune the indexer's heap down for a lab, because that figure is sized
for thousands of endpoints and you have four.

If your host cannot spare it, do the Tier 1 path. You will learn more from it
than from a dashboard that swaps constantly.
:::

## What this module is really teaching

Not a product. Wazuh is one SIEM and your employer may run a different one.

The transferable part is the reasoning: what a log is worth, why raw
collection is not detection, how a rule decides something is interesting, and
why an alert queue nobody reads is worse than no alerts at all.

Every one of those survives a change of vendor. The XML syntax does not.

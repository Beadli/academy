# Beadli Lab Academy

**Build the enterprise yourself — then defend it.**

Nobody should walk into their first IT or security job never having seen a
domain controller. Beadli Lab Academy is a free, hands-on curriculum that
takes you from a bare laptop to running — and defending — your own mock
enterprise environment: Active Directory, PKI, single sign-on, Docker,
Ansible automation, monitoring and detection, and finally attacking your own
lab and watching your defenses fire.

!!! info "Under construction"
    The Academy is being built module by module. Module 0 (Orientation) is
    the place to start; modules are published as they're completed.

## What makes this different

- **You build one coherent environment** — not isolated exercises. Every
  module adds to the same lab, and by the capstone you're investigating a
  real incident inside infrastructure you built from nothing.
- **Educational, not just instructional.** Every step explains *why* — the
  concept, the problem it solves, and how it's done in a real enterprise —
  so you can troubleshoot a lab (or a job) that doesn't match the
  screenshots.
- **Professional habits from day one.** Documentation (Git, Markdown,
  Obsidian), persistent terminal sessions (tmux), scripting (PowerShell,
  Bash, Python), and AI-assisted engineering are part of the curriculum,
  not an afterthought. You graduate with a portfolio repo, not just
  screenshots.
- **Honest hardware tiers.** A 16 GB laptop completes most of the
  curriculum. Every module declares what it needs up front.
- **Self-grading checkpoints.** Each module ends with a validation playbook:
  run it, all green, move on.

## The lab you'll build

| Tier | Hardware | You get |
|---|---|---|
| **Core** | 16 GB RAM laptop | Domain controller, Ubuntu Docker host, Kali attacker box |
| **Enterprise** | 32 GB RAM | + OPNsense firewall, issuing CA, AD FS single sign-on, offline root CA |
| **Full homelab** | 64 GB+ / dedicated box | + Suricata, full Wazuh, OpenVAS, Grafana/Prometheus, Tailscale |

## Start here

Head to **[Module 0 — Orientation](modules/00-orientation/index.md)**.

## Support this project

The Academy is free and always will be. If it helps you, donations keep it
growing — *(donation links coming with the first published modules)*.

---
title: "Module 10: Automation with Ansible"
sidebar_position: 0
---

# Module 10: Automation with Ansible

You have built nine modules of infrastructure by hand. Every domain
controller promoted, every firewall rule written, every container started, you
did yourself, in a terminal, one command at a time.

This module is where that stops being the plan.

Not because doing it by hand was wasted. It is the opposite: the hand-built
version is the only reason the automated version will make sense to you.
Lesson 1.6 called this an escalation ladder. Build with your hands, script what
you understood, automate what you scripted. This is the third rung, and you
have earned it.

What's in it:

- **10.1** why automate, and the rule that keeps automation safe
- **10.2** install Ansible, describe your lab, run your first command
- **10.3** your first playbook: the hardening from Module 6, done properly
- **10.4** idempotence, and why running it twice proves something
- **10.5** templates, variables and handlers
- **10.6** roles and Galaxy: other people's automation, and whether to trust it
- **10.7** Windows: WinRM, Kerberos, and the traps
- **10.8** rebuild a machine on purpose
- **10.9** playbooks belong in Git
- **10.10** journal entry
- **10.11** checkpoint

## Where this runs

**UBNT01 is your control node.** It has been labelled "Ansible control" in the
lab diagram since Module 0, and this is the module that makes that true. It
reaches your Linux hosts over SSH, which Module 6 already set up, and your
Windows hosts over a protocol lesson 10.7 introduces.

Ansible is agentless. Nothing gets installed on the machines it manages. That
is worth knowing up front, because it is the main reason it won: no agent to
deploy, no agent to upgrade, no agent to be the thing that broke.

**Tier 1** can do 10.1 through 10.6 and 10.9. You have UBNT01, and one machine
managing itself teaches most of the mechanics.

**Tier 2 and up** get 10.7 and 10.8, which need Windows hosts to manage and a
machine you are willing to destroy.

Budget two evenings. The Linux half goes faster than you expect. The Windows
half does not, and lesson 10.7 is honest about why.

## The one rule

Before any of it, the rule this module is built around, and the one lesson 1.2
promised you would meet here:

**Never run automation you cannot read.**

A playbook that does something you do not understand is worse than doing it by
hand, because it does it faster, everywhere, and without pausing at the moment
you would have noticed. Every failure in this module's war stories comes back
to that sentence.

You are ready for this precisely because you have done all of it manually
first. When a playbook says it will disable password authentication over SSH,
you know what that means, what breaks if it is wrong, and how to get back in.
Someone who started here would not.

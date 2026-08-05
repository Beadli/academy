---
title: "12.2 Install the manager, enrol your first agent"
sidebar_position: 2
---

# 12.2 Install the manager, enrol your first agent

**Everyone does this lesson.** It builds the part that actually detects things.

## Give UBNT01 the memory first

Shut UBNT01 down, raise it to **8 GB** in the hypervisor, start it again. If
you skip this the manager will install and then behave strangely under load,
which is a worse afternoon than the two minutes this takes.

```bash
# On UBNT01, confirm what it thinks it has.
free -h
```

## Install the manager

Wazuh publishes an apt repository. Follow the current installation
instructions from [wazuh.com](https://documentation.wazuh.com) for adding the
repository and its signing key, then:

```bash
sudo apt update
sudo apt install -y wazuh-manager
```

Deliberately not reproducing the key and repository commands here: signing
keys rotate, and a stale key in a course is a confusing failure rather than an
honest one. The vendor's page is the right source.

```bash
# Start it and make it survive a reboot.
sudo systemctl daemon-reload
sudo systemctl enable --now wazuh-manager

# The four verbs from lesson 6.3, on a new service.
sudo systemctl status wazuh-manager
```

:::info[What you did not install, and why]
A full Wazuh deployment has three parts: the **manager** (receives events,
runs rules, raises alerts), the **indexer** (stores and searches them), and
the **dashboard** (draws them).

You installed the manager only. That is the part that detects. The other two
are for searching and looking, they carry the 8 GB requirement between them,
and Tier 3 adds them in lesson 12.9.

This split is worth understanding beyond Wazuh, because most SIEMs have the
same shape: something that decides, something that stores, something that
draws. When a vendor quotes you a hardware requirement, it is almost always
the storage layer talking.
:::

## Where things live

Two paths to remember, because everything in this module happens in them:

```bash
# Configuration, including which agents exist and what to watch.
sudo ls /var/ossec/etc/

# The output. Every alert the manager has raised.
sudo ls /var/ossec/logs/alerts/
```

`/var/ossec` is the whole installation. If you have used other tools in this
family the layout will look familiar; it is inherited from OSSEC, which Wazuh
grew out of.

## Enrol UBNT01 itself

The manager can monitor the machine it runs on, which is the quickest way to
see the pipeline work end to end.

```bash
# Install the agent alongside the manager.
sudo apt install -y wazuh-agent
```

Point it at `127.0.0.1` when asked for the manager address, then:

```bash
sudo systemctl enable --now wazuh-agent

# Does the manager see it?
sudo /var/ossec/bin/agent_control -l
```

You should see one agent, `Active`. If it says `Never connected`, the agent
cannot reach the manager: check the address in
`/var/ossec/etc/ossec.conf` on the agent side.

## Watch an alert happen

This is the moment the pipeline becomes real rather than theoretical.

```bash
# Watch the alert log. Leave this running.
sudo tail -f /var/ossec/logs/alerts/alerts.json
```

In a second SSH session, do something worth noticing:

```bash
# Three failed sudo attempts. Type a wrong password deliberately.
sudo -k
sudo true
```

Back in the first window, alerts appear as JSON, one per line.

That is dense. Make it readable:

```bash
# jq is from Module 6's toolkit. If it is missing: sudo apt install -y jq
sudo tail -f /var/ossec/logs/alerts/alerts.json | \
  jq -r '[.rule.level, .rule.id, .rule.description] | @tsv'
```

Now each line is a level, a rule ID, and what the rule thinks happened.

:::tip[Reading alerts as JSON is a skill worth having deliberately]
Tier 3 will put a dashboard in front of this. Learn to read the raw form
first, because it is what the dashboard is rendering and it is what you will
be looking at when something is wrong with the dashboard.

More practically: **this is the shape of every modern security tool's output.**
JSON events, a severity, an identifier, a description, and a pile of context
fields. Being comfortable with `jq` against a stream of them transfers to
every SIEM you will ever meet, and to plenty of things that are not SIEMs.
:::

## Enrol a machine that is not this one

Now DC01, which is where the interesting events are.

On DC01, download the Wazuh agent for Windows from the vendor's page and
install it, giving your manager's address, `10.10.10.20`.

Then in PowerShell on DC01:

```powershell
# The service should be running.
Get-Service -Name WazuhSvc | Select-Object Name, Status, StartType
```

Back on UBNT01:

```bash
sudo /var/ossec/bin/agent_control -l
```

Two agents, both `Active`. Your domain controller is now shipping events to a
machine it does not trust and cannot edit, which is the collection property
from lesson 12.1 in practice.

## What you have, and what you do not

You have collection and a default rule set. Wazuh ships thousands of rules and
some of them are already firing.

What you do not have is anything tuned to your environment. Lesson 12.3 makes
Windows produce events worth detecting on, and 12.4 writes the first rule that
is yours.

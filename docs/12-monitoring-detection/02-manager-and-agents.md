---
title: "12.2 Install the manager, enrol your first agent"
sidebar_position: 2
---

import Module12Dataflow from '@site/static/img/module12-dataflow.svg';

# 12.2 Install the manager, enrol your first agent

**Everyone does this lesson.** It builds the part that actually detects things.

## The shape of what you are building

Before installing anything, here is where every piece sits and what it does.
Come back to this picture whenever a later lesson asks you to change a
configuration file, because it will tell you which box you are editing.

<Module12Dataflow role="img" aria-label="Data flow: DC01, UBNT01 and SURICATA01 produce logs. An agent on each machine reads only the log sources listed in its configuration and sends them to the manager on UBNT01. In the manager, a decoder turns each raw line into named fields, then rules test those fields and decide whether it is interesting and at what level. Alerts are written to alerts.json. Optionally an indexer stores them for searching and a dashboard draws them; neither decides anything." style={{width: '100%', height: 'auto'}} />

**How to read it.** Follow it left to right, in the four numbered steps.

**The agent (1) is a reader, not a thinker.** It sits on the machine being
watched and ships logs elsewhere. It makes no decisions, and critically **it
only reads the log sources listed in its configuration file**. That last point
is the one that catches people: installing an agent does not mean it is
collecting everything on that machine. It collects what you told it to. This
is why lessons 12.3 and 12.7 both involve editing that file.

**The manager (2 and 3) is where detection happens.** Two stages, and keeping
them separate in your head will save you hours later. A **decoder** parses a
raw log line into named fields, turning `Failed password for sam from
10.10.10.50` into a username and a source address. Then **rules** test those
fields and decide whether it matters. If a decoder does not extract a field, a
rule referencing it has nothing to compare against and silently never fires.

**The output (4) is a file.** Every alert becomes a line of JSON in
`alerts.json`. That is the whole product of the system.

**The indexer and dashboard, added in lesson 12.9, are optional layers on
top.** They store and draw. **Neither of them detects anything**, and if you
switched both off your detections would carry on working exactly as before.
Knowing that keeps you from confusing "the dashboard is down" with "we are not
monitoring".

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

You installed the manager only, and you will add the other two in lesson 12.9.
That is deliberate: the manager is the part that detects, and lessons 12.3 to
12.8 have you write and tune rules while reading their raw output, before a
dashboard starts rendering it for you.

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
Lesson 12.9 will put a dashboard in front of this. Learn to read the raw form
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

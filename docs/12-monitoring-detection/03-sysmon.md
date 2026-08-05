---
title: "12.3 Sysmon: make Windows worth watching"
sidebar_position: 3
---

# 12.3 Sysmon: make Windows worth watching

Windows logs a great deal by default and almost none of it is what a defender
wants.

It will tell you an account logged on. It will not, by default, tell you that
`powershell.exe` was launched by `winword.exe`, which is one of the most
useful sentences in security. **Sysmon fixes that**, and it is free, from
Microsoft, and the single highest-value thing you can install on a Windows
machine you intend to defend.

## What it adds

Sysmon is a driver and service that writes detailed events to its own Windows
event log. The ones that matter most:

<div className="labTable">

| Event | Why a defender cares |
|---|---|
| **Process creation** | With the **parent** process and the full command line |
| **Network connection** | Which process connected where, not just that a connection happened |
| **File creation time changed** | Attackers backdate files to hide them |
| **Registry changes** | Where persistence usually lives |
| **Image loaded** | Which DLLs a process pulled in |

</div>

The first row carries most of the value, and specifically the two words
**parent** and **command line**.

Native Windows process auditing can be configured to log process creation, but
Sysmon gives you the parent relationship and the full command line reliably and
by default. That matters because almost every real attack shows up as a
*relationship*: a document spawning a shell, a web server spawning `cmd.exe`,
an office application launching PowerShell with a base64 blob attached.

None of those processes is suspicious alone. The parentage is the signal.

## Install it

On DC01, download **Sysmon** from Microsoft Sysinternals.

Sysmon with no configuration logs almost everything, which is unusable. It is
driven by a config file, and you do not write one from scratch: the community
maintains well-commented baseline configurations. **SwiftOnSecurity's
sysmon-config** is the usual starting point and has been for years.

```powershell
# From an elevated PowerShell, in the folder holding both files.
.\Sysmon64.exe -accepteula -i sysmonconfig.xml

# Confirm the service is running.
Get-Service Sysmon64 | Select-Object Name, Status
```

:::warning[You are installing a driver, and lesson 11.7's question applies]
Sysmon is a kernel driver from Microsoft, so the software itself is about as
trustworthy as software gets.

**The configuration file is the part to think about.** It is a community
artefact that decides what your security monitoring sees and, more
importantly, what it ignores. A config with an over-broad exclusion is a
blind spot you installed on purpose and will never notice.

Same four questions as lesson 11.7: who maintains it, how many people use it,
can you read it, do you need it. This one passes clearly, and **you can read
it**, which is the point. Open it. It is heavily commented and it is a genuine
education in what defenders care about.
:::

## Tell the agent to collect it

**What we are doing.** Adding one log source to the agent's configuration file
on DC01.

**Why.** Installing Sysmon made DC01 *record* these events. It did not send
them anywhere. Look back at step 1 of the diagram in lesson 12.2: the agent
reads only the log sources listed in its configuration, and Sysmon writes to a
channel that is not in that list.

So right now you have excellent telemetry sitting on a machine, and a manager
that has never heard of it. This step connects the two.

### Where Windows puts logs, briefly

Windows does not keep logs in text files. It has an **event log service**, and
events go into named **channels**. `Security` is the channel holding logons and
account changes. `System` holds service and driver events.

**Sysmon creates its own channel**, called
`Microsoft-Windows-Sysmon/Operational`, and writes everything there. That name
is what you are about to give the agent. It is not a file path; it is the name
of a channel, and the agent asks Windows for its contents.

You can see it yourself, which is worth doing once so the name means something
rather than being a string you pasted. On DC01, open **Event Viewer** and
navigate to **Applications and Services Logs → Microsoft → Windows → Sysmon →
Operational**. Those are the events you are about to start shipping.

### Make the change

On DC01, open the agent's configuration in an editor running as
administrator:

```text
C:\Program Files (x86)\ossec-agent\ossec.conf
```

It is XML, and everything lives inside a single `<ossec_config>` element. Find
the closing `</ossec_config>` at the bottom, and add this block **above** it:

```xml
<!-- Collect Sysmon's events. "location" is the Windows channel name,
     not a file path. "eventchannel" tells the agent to read it through
     the Windows event log API rather than treating it as a text file. -->
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

Two things to understand rather than copy:

**`<localfile>`** is how you add any log source to an agent. Every log the
agent collects is one of these blocks. When you later want it to read
something else, this is the shape you will use again, and lesson 12.7 does
exactly that for a different source.

**`<log_format>eventchannel</log_format>`** tells the agent *how* to read it.
Windows channels are not text files, so the agent has to ask the event log
service rather than opening a file. Using the wrong format here is a common
mistake and produces silence rather than an error.

### Restart the agent so it re-reads the file

```powershell
Restart-Service -Name WazuhSvc
```

Configuration is read at startup. Without this, you have edited a file and
changed nothing, which is a confusing five minutes if you go straight to
looking for events.

### How we know it worked

Three checks, cheapest first. Do them in order, because each one narrows down
where a problem would be.

**One: the agent restarted cleanly.** On DC01:

```powershell
Get-Service -Name WazuhSvc | Select-Object Name, Status
```

`Running` means the file parsed. **If the service will not start, your XML is
malformed**, which is nearly always a missing closing tag or the block pasted
outside `</ossec_config>`.

**Two: the manager still sees the agent.** On UBNT01:

```bash
sudo /var/ossec/bin/agent_control -l
```

DC01 should still be `Active`. If it went to `Disconnected`, the agent is
struggling to start rather than struggling to read Sysmon.

**Three: Sysmon events are actually arriving.** This is the real test, and
lesson 12.3's next section walks through generating one deliberately.

## Prove it works

On UBNT01:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json | \
  jq -r 'select(.rule.groups[]? == "sysmon") |
         [.rule.level, .rule.description] | @tsv'
```

On DC01, create a parent-child relationship worth noticing:

```powershell
# cmd launching PowerShell. Innocuous here, and the exact shape
# of a thing you would want to know about on a server.
cmd.exe /c "powershell.exe -Command Get-Date"
```

The alert should arrive within seconds, carrying the parent process.

If nothing appears, work through it in this order: is the Sysmon service
running, is the event visible in Event Viewer under
`Applications and Services Logs > Microsoft > Windows > Sysmon`, did the agent
restart cleanly, and is the agent still `Active` on the manager.

## The part worth remembering

Sysmon does not detect anything. It is **telemetry**, not detection: it makes
the machine tell you what happened in enough detail that a rule can decide
something.

That distinction matters when someone says they have "installed Sysmon" as a
security measure. They have installed the ability to answer questions. Whether
anyone is asking is lesson 12.4.

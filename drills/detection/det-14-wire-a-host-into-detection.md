---
title: "DET-14 Wire your identity server into detection"
sidebar_position: 15
---

# DET-14: Wire your identity server into detection

|  |  |
|---|---|
| **Objective** | Get ADFS01 sending the Windows telemetry that detection needs into your Wazuh manager, and prove it with a test event |
| **Success signal** | A distinctive command you run on ADFS01 shows up in your manager within seconds; before you wire it, the same command shows up nowhere |
| **Needs** | Modules 8 and 12 (Tier 2: this is the AD FS server) |
| **Effort** | An evening |
| **Risk** | Safe and reversible. You are adding monitoring and enabling a log, nothing destructive |
| **Check** | Mechanical: the test event either arrives or it does not |

## Why this drill exists

In Module 12 you built a Wazuh manager and enrolled your first agents: UBNT01,
DC01 and SURICATA01. You installed Sysmon on DC01 and taught its agent to forward
the Sysmon channel. That was the whole point of the module, and it works.

But you built **ADFS01** back in Module 8, and Module 12 never touched it. So the
one server that issues every login token in your lab, the single most valuable box
an attacker could reach, is sending **nothing** to your SIEM. Your SIEM is the
security information and event management platform you stood up in Module 12, and
right now it cannot see your identity server at all.

There is a second gap, quieter and worse. Module 12 turned on **Sysmon**, which
records processes. It never turned on **PowerShell script-block logging**, which
records the actual commands PowerShell runs. A large share of modern Windows
attacks live entirely inside PowerShell, and without that log they are invisible
even on the hosts you did enrol. This drill closes both gaps on ADFS01, and the
method is the same for any host you add later.

**Do this drill before [DET-13](/drills/detection/det-13-catch-a-forged-identity).**
DET-13 asks you to catch an attack on ADFS01.
There is no point writing a detection for events your manager never receives.

## The trap this drill is built around

Ask "is my lab watching my servers?" and the comfortable answer is "yes, I set up
Wazuh in Module 12." The honest answer is **it is watching the servers you
enrolled, and only the log sources you listed.**

An agent is not a net that catches everything on a machine. It reads **only** the
log sources named in its configuration and sends **only** those. Enrolling DC01
did not enrol ADFS01. Forwarding the Sysmon channel did not forward the PowerShell
channel. A tool being installed somewhere in your lab is not the same as that tool
watching the thing in front of you, and the gap between those two is exactly where
a real attacker operates unseen.

So this is not a drill about installing Wazuh. You already did that. It is about
the difference between "Wazuh exists in my lab" and "Wazuh is watching this
specific host for the specific things that matter," which is a distinction you
will make every time you add a server for the rest of your career.

## Your objective

**Make ADFS01 a monitored host, and prove a command run on it reaches your
manager.**

Three things must be true when you finish:

1. ADFS01 shows as **Active** in your manager's agent list, next to DC01.
2. ADFS01 forwards **two** Windows channels: the Sysmon channel (processes) and
   the PowerShell Operational channel (command text), the second of which also
   needs script-block logging switched on to contain anything.
3. A distinctive command you run on ADFS01 is **findable in your manager within
   seconds**, and you have confirmed that the same command produced nothing before
   you wired the channel.

Point three is the drill. Anyone can edit a config file. Proving an event made the
whole trip, from a keystroke on ADFS01 to a searchable record on UBNT01, is the
part that tells you the wiring is real and not just tidy.

## How you will know

You run a marked command on ADFS01, then search your manager for the mark. Before
the wiring, it is not there. After, it is, within seconds.

```powershell
# On ADFS01, once wired. A harmless command carrying a mark you can search for.
Write-Output "DET14-WIRING-PROOF-a7f3"
```

The real check is finding `DET14-WIRING-PROOF-a7f3` in your Wazuh dashboard, in
the PowerShell script-block data, a few seconds after you run it. If it is not
there, the wiring is not finished, however correct the configuration file looks.

<details>
<summary>Nudge, if you do not know where to start</summary>

You have done every piece of this before, on a different host. Go back to how you
brought DC01 into Wazuh in Module 12 and do the same to ADFS01, then add the one
thing Module 12 left out.

Three questions to answer in order:

- **How did DC01 get an agent?** Lesson 12.2 walked you through installing the
  Windows agent and pointing it at the manager. ADFS01 needs the identical thing,
  with its own name.
- **How did DC01 start forwarding Sysmon?** Lesson 12.3 installed Sysmon and added
  one `<localfile>` block to the agent's configuration. ADFS01 needs that too.
- **What did neither lesson ever turn on?** The log that records PowerShell
  *commands*, not just PowerShell *processes*. It is off by default on Windows, it
  is a single setting to enable, and then it needs its own `<localfile>` block the
  same way Sysmon did. This is the only genuinely new step in the drill.

</details>

<details>
<summary>Fuller hint, if you know the direction but not the specifics</summary>

**The agent and Sysmon** are lessons 12.2 and 12.3 applied to ADFS01. Same
installer, same manager address you used for DC01, a new agent name. Same Sysmon
install, same Sysmon `<localfile>`.

**The new step is PowerShell script-block logging.** Two parts, and missing either
means an empty channel:

- **Enable the logging.** It is a Windows setting, off by default. There is a
  Group Policy for it under Windows PowerShell, and there is an equivalent
  registry value if you would rather set it directly. The value name says exactly
  what it does.
- **Forward the channel.** Once logging is on, the commands land in a Windows
  channel named for PowerShell's Operational log. Add a `<localfile>` for it in
  the agent config, exactly the shape you used for Sysmon, then restart the agent
  so it re-reads its configuration.

**The order matters and catches people.** If you enable the setting but do not
forward the channel, the events exist on ADFS01 and never leave it. If you forward
the channel but never enable the setting, the channel exists and stays empty. You
need both, and you will only know you have both when your marked command appears
in the manager.

Lesson 12.3 already warned you that the agent has to be restarted before a
configuration change takes effect, and that a malformed config stops the agent
starting at all. Both still apply here.

</details>

<details>
<summary>Full walkthrough</summary>

Everything here runs on **ADFS01** unless a step says otherwise, in an elevated
**Windows PowerShell** (Run as administrator). ADFS01 is the Tier 2 server you
built at `10.10.10.40` in lesson 8.3.

### 1. Prove the gap first

Before you change anything, run the marked command and confirm your manager has
never heard of ADFS01:

```powershell
# On ADFS01. This runs, and as far as your SIEM is concerned it never happened.
Write-Output "DET14-WIRING-PROOF-a7f3"
```

On UBNT01, search your dashboard for `DET14-WIRING-PROOF-a7f3`. Expect nothing,
and expect ADFS01 to be absent from the agent list entirely. **Write that down.**
That absence is the "before" this whole drill is measured against, and it is more
convincing as your own screen than as my assertion.

### 2. Enrol ADFS01, the way you enrolled DC01

This is lesson 12.2, pointed at a new host. Download the Wazuh agent for Windows
from the vendor's page, take the version the page offers, then install it pointed
at your manager. Substitute your manager's address, the same one you used for DC01:

```powershell
# On ADFS01. YOUR-MANAGER-IP is UBNT01, the address from lesson 12.2.
msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER="YOUR-MANAGER-IP" WAZUH_AGENT_NAME="ADFS01"
NET START WazuhSvc
```

```powershell
# How you know it worked, on UBNT01:
sudo /var/ossec/bin/agent_control -l
```

**Expect ADFS01 to appear as `Active`** in that list, alongside DC01. If it says
`Never connected`, the agent cannot reach the manager: check the address you gave
it and that the firewall rules from Module 4 let ADFS01 reach UBNT01. This is the
same wall lesson 12.2 described when you enrolled DC01.

### 3. Install Sysmon and forward its channel

This is lesson 12.3, on ADFS01. Install Sysmon from Sysinternals exactly as you
did on DC01, then add its channel to this agent's configuration. The agent config
on Windows lives at `C:\Program Files (x86)\ossec-agent\ossec.conf`. Open it in an
editor running as administrator and add, inside the `<ossec_config>` block:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

That is the same block you wrote for DC01. `<localfile>` adds a log source;
`eventchannel` tells the agent to read it as a Windows event channel rather than a
text file.

### 4. Turn on PowerShell script-block logging, the step Module 12 skipped

This is the only new thing in the drill. Windows does not record the text of
PowerShell commands unless you tell it to. Turn it on:

```powershell
# On ADFS01. Create the policy key and enable command logging.
$key = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging'
New-Item -Path $key -Force | Out-Null
Set-ItemProperty -Path $key -Name EnableScriptBlockLogging -Value 1
```

**What this does and why it matters:** from now on, every PowerShell command runs
through a logger that writes the command's text to the
`Microsoft-Windows-PowerShell/Operational` channel as event 4104. Without it, an
attacker working in PowerShell leaves you process names and nothing about what
those processes actually did. With it, you have the commands themselves, which is
the difference between "powershell.exe ran" and seeing the exact line an attacker
typed.

Now forward that channel, the same way you forwarded Sysmon. Add a second
`<localfile>` to the agent config:

```xml
<localfile>
  <location>Microsoft-Windows-PowerShell/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

### 5. Restart the agent so it re-reads its configuration

```powershell
# On ADFS01.
Restart-Service WazuhSvc
```

```powershell
# How you know it worked. Expect "Running".
Get-Service WazuhSvc | Select-Object Status
```

**If the service will not start, your XML is malformed**, which is the most common
failure here and the same one lesson 12.3 warned about. The agent log names the
line it choked on:

```powershell
Get-Content 'C:\Program Files (x86)\ossec-agent\ossec.log' -Tail 20
```

### 6. Prove the gap is closed

Run the marked command again:

```powershell
# On ADFS01.
Write-Output "DET14-WIRING-PROOF-a7f3"
```

**How you know it worked:** search your dashboard for `DET14-WIRING-PROOF-a7f3`
and find it, in the PowerShell script-block data, within a few seconds. The exact
command you ran, the account that ran it, and the host it ran on are all there.

Now you have the "after" to sit beside the "before" from step 1. Same command,
same host, and the only thing that changed is that your SIEM can now see your
identity server. That is the whole drill.

</details>

## Going further

- **Wire the rest of your unenrolled hosts.** ADFS01 is unlikely to be the only
  thing you built after Module 12. SUBCA01 from Module 7 is another Tier 2 server
  doing sensitive work with nothing watching it. The method you just used is the
  method for all of them.
- **Add the Security channel too.** Sysmon and PowerShell cover processes and
  commands. Logon events, the `4624` and `4625` that show you who signed in and who
  failed to, live in the Windows Security channel, which is a third `<localfile>`.
  Decide whether you want it, and what it would cost you in volume.
- **Turn script-block logging on everywhere it should be.** You just enabled it on
  ADFS01. DC01 has been enrolled since Module 12 and still does not have it. Every
  Windows host you care about detecting on has the same gap until you close it.

## What this proves

You can bring a new host into your detection pipeline and confirm, with your own
eyes and a marked event, that its logs are arriving. That confirmation is the
precondition for every detection you will ever write. A rule against events that
never reach the manager is not a detection, it is a wish.

You also learned that "the tool is installed" and "the tool is watching this" are
different claims, and that only the second one keeps you safe. Most people never
check which one they actually have.

:::note[Write this down before you close the tab]

In your own words, in your journal, while it is fresh:

- Which of your lab's hosts were sending nothing to your SIEM before today, and
  why you had assumed otherwise.
- What script-block logging records that Sysmon does not, and why an attacker who
  lives in PowerShell would have been invisible to you until you turned it on.

Now go do [DET-13](/drills/detection/det-13-catch-a-forged-identity). Your identity server is finally being watched, so you can find
out whether being watched is the same as being caught.

:::

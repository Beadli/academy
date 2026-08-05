---
title: "12.4 Read an alert, then write a rule"
sidebar_position: 4
---

# 12.4 Read an alert, then write a rule

You have events arriving and default rules firing. This lesson writes one that
is yours, for something the defaults do not know to care about.

## First, read an alert properly

Take one from the stream and look at all of it:

```bash
# The most recent alert, in full.
sudo tail -n 1 /var/ossec/logs/alerts/alerts.json | jq .
```

Four parts matter:

**`rule`** is the verdict: which rule matched, at what level, and its
description. `rule.level` is severity, 0 to 15.

**`agent`** is which machine it came from.

**`data`** or `win.eventdata` is the decoded content: usernames, process
names, addresses. **This is what you write rules against.**

**`full_log`** is the raw event as it arrived. When a rule is not matching and
you cannot see why, the answer is usually here, because the field you assumed
exists is spelled differently or is not there.

:::tip[Decoders come before rules, and this is where people get stuck]
A SIEM does two things to every event. A **decoder** parses the raw text into
named fields. A **rule** then makes a decision about those fields.

If your rule is not firing, the usual cause is not the rule. It is that the
field you referenced was never extracted, so the comparison is against
nothing.

```bash
# Feed a raw log line in and watch decoding and rule matching happen.
sudo /var/ossec/bin/wazuh-logtest
```

Paste a line from `full_log` and it shows you the decoder that claimed it,
every field extracted, and which rule matched. **This tool is the difference
between writing detections and guessing at them.** Use it before you write a
rule, not after it fails.
:::

## Levels, and what they should mean

Wazuh levels run 0 to 15. What matters is not the numbers but that **you decide
what they mean and stay consistent.** A workable scheme:

<div className="labTable">

| Level | Meaning | Response |
|---|---|---|
| 0 to 3 | Logged, not alerted | Nothing. It is there if you search. |
| 4 to 7 | Notable | Review when you are looking anyway |
| 8 to 11 | Investigate | Someone should look today |
| 12 to 15 | Wake someone up | Now |

</div>

Most detection programmes fail at the top two rows: everything gets written at
level 12 because everything felt important when it was written. Lesson 12.5 is
about digging out of that.

## Write one

Something the defaults will not flag but you would want to know: **a new local
user created on your domain controller.**

Custom rules live in one file so they survive upgrades:

```bash
sudo nano /var/ossec/etc/rules/local_rules.xml
```

```xml
<group name="local,windows,">

  <!--
    A local user account was created on a Windows machine.
    Windows Security event 4720.

    Why this exists: in this lab, accounts are created in Active Directory
    on DC01 with New-ADUser. Nobody has any reason to create a LOCAL
    account on a domain-joined machine. If one appears, either somebody is
    doing something unusual, or somebody is establishing persistence that
    survives the domain.

    Level 12 because it is rare, it is deliberate, and it wants looking at
    the same day.
  -->
  <rule id="100001" level="12">
    <if_sid>60109</if_sid>
    <field name="win.system.eventID">^4720$</field>
    <description>Local user account created on $(win.system.computer)</description>
    <group>authentication,account_creation,</group>
  </rule>

</group>
```

Three things to understand rather than copy:

**`id` must be 100000 or above.** Below that is reserved for Wazuh's own
rules, and using a reserved ID means your rule vanishes on upgrade.

**`if_sid`** chains this rule to a parent. Rather than matching every event on
the system, this only considers events the parent already identified as
Windows security events, which is faster and much easier to reason about.

**The comment is not optional.** Read it again: it says what the rule detects,
*why that is suspicious in this environment*, and why the level was chosen.
Six months from now that comment is the difference between someone
understanding the rule and deleting it.

## Test before you trust

```bash
# Syntax check without restarting anything.
sudo /var/ossec/bin/wazuh-logtest -t
```

Then restart and generate the event:

```bash
sudo systemctl restart wazuh-manager
```

On DC01, in PowerShell:

```powershell
# Create a local account, which is exactly what the rule is watching for.
New-LocalUser -Name "testuser12" -NoPassword -AccountNeverExpires
```

On UBNT01:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json | \
  jq -r 'select(.rule.id == "100001") | [.rule.level, .rule.description] | @tsv'
```

Then clean up, because a lab full of forgotten test accounts is its own
problem:

```powershell
Remove-LocalUser -Name "testuser12"
```

## Put the rules in Git

Lesson 1.3 said the `status`, `add`, `commit` rhythm would be used on Ansible
playbooks in Module 10 and detection rules here. This is that.

```bash
mkdir -p ~/detections && cd ~/detections
sudo cp /var/ossec/etc/rules/local_rules.xml .
sudo chown $USER:$USER local_rules.xml

git init -b main
git add -A
git commit -m "detections: alert on local account creation"
git remote add origin http://git.lab.internal/sam/detections.git
git push -u origin main
```

**Detection rules are code**, and they deserve the same treatment: history,
review, and a message explaining why a change was made. When an alert starts
misbehaving, `git log` tells you what changed and when, which is a question
you will actually need to answer.

Copying the file back and forth by hand is clumsy. That is a good candidate
for an Ansible playbook from Module 10, and a reasonable exercise once the
rest of this module is working.

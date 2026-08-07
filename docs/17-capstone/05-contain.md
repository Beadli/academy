---
title: "17.5 Contain, and the decisions inside that word"
sidebar_position: 5
---

# 17.5 Contain, and the decisions inside that word

Containment means stopping it getting worse. It is a separate phase from
eradication for a reason that is easy to state and hard to follow under
pressure: **the fastest way to stop an intrusion is usually the fastest way
to destroy the evidence of it.**

## The decision nobody warns you about

You have found a hostile account with passwordless sudo and a beacon running
every five minutes. The instinct is to delete all of it right now.

**Before you do, there is a real decision to make, and both answers are
defensible:**

**Contain immediately.** Stop the damage now. You lose the chance to observe
what the intruder does next, and you tell them they have been detected, which
means the ones who are still connected will react.

**Watch first.** Leave it running under observation to learn scope: what else
they touch, where they call out to, whether other machines are involved. You
accept that the intrusion continues while you watch.

**The real-world answer depends on things a lab cannot simulate**: whether
data is actively leaving, what the regulator requires, whether legal wants
evidence for prosecution, and whether anybody senior is awake to authorise
the risk.

**The wrong answer is to make the decision by accident**, which is what
happens when somebody deletes the account thirty seconds after finding it
because it felt urgent.

**For this exercise: contain, and write down that you chose to.** Note in
your report which you chose and why. That sentence is what an incident review
asks for.

## Preserve first

Before changing anything, collect what you would lose. Once the account is
gone, so is its home directory, its timestamps and its key.

```bash
# A place to keep evidence, outside the areas you are about to change.
sudo mkdir -p /var/tmp/incident-2026-01
cd /var/tmp/incident-2026-01

# The artefacts themselves.
sudo cp -a /etc/cron.d/system-health        ./ 2>/dev/null
sudo cp -a /etc/sudoers.d/svc-update        ./ 2>/dev/null
sudo cp -a /home/svc-update/.ssh/authorized_keys ./svc-update-authorized_keys 2>/dev/null

# The metadata, which the copies do not fully preserve.
sudo stat /etc/cron.d/system-health /etc/sudoers.d/svc-update \
          /home/svc-update/.ssh/authorized_keys > ./stat-output.txt 2>&1

# The account records, and the relevant logs.
sudo grep svc-update /etc/passwd /etc/shadow /etc/group > ./account-records.txt 2>&1
sudo journalctl --since "2026-08-05 15:30" > ./journal-window.txt
```

**`cp -a` preserves timestamps and ownership**, which plain `cp` does not.
That distinction matters here: a copy with today's timestamp is much weaker
evidence than one carrying the original.

**How you know it worked:**

```bash
# Everything collected, with sizes. Nothing should be 0 bytes.
sudo ls -l /var/tmp/incident-2026-01/
```

Then hash it, so you can show later that nothing changed after collection:

```bash
cd /var/tmp/incident-2026-01
sudo sha256sum * > ../incident-2026-01-hashes.txt
sudo cat ../incident-2026-01-hashes.txt
```

**That hash file is what makes your evidence defensible.** It is the same
technique as lesson 15.3's restore verification, applied to a different
purpose: proving something did not change.

:::warning[Where evidence handling gets serious]
In a real incident with legal implications, this is where **chain of
custody** begins: a record of who collected what, when, and who has had
access since.

Your lab does not need that formality, but the habit does transfer. If an
incident might ever involve a court, an insurer or a regulator, **stop
touching things and get somebody who does this professionally.** The most
expensive mistakes in incident response are made in the first hour by people
trying to be helpful.
:::

## Now contain

Containment for this incident, in an order chosen so each step reduces
capability without destroying what you have not collected yet.

**1. Stop the beacon**, because it is the only thing actively communicating:

```bash
sudo rm /etc/cron.d/system-health
```

**How you know it worked:**

```bash
# Gone from the directory.
ls /etc/cron.d/ | grep system-health || echo "removed"

# And confirm nothing runs it in the next five minutes.
sudo journalctl -u cron --no-pager --since "5 min ago" | grep -i health || echo "no further executions"
```

**2. Remove the privilege**, which is what makes the account dangerous rather
than merely present:

```bash
sudo rm /etc/sudoers.d/svc-update
```

**How you know it worked:**

```bash
# The account can no longer sudo. Expect: "may not run sudo"
# or a "not in the sudoers file" message.
sudo -l -U svc-update 2>&1 | tail -3
```

**3. Disable the account, without deleting it yet.** This is the step people
skip, and it is the one that keeps your evidence:

```bash
# Lock the password and set the shell to nologin. The account
# still exists, and everything about it is still inspectable.
sudo usermod -L -s /usr/sbin/nologin svc-update
```

**How you know it worked:**

```bash
# The shadow entry now starts with ! meaning locked, and the
# shell is nologin.
sudo passwd -S svc-update
getent passwd svc-update
```

Expect `svc-update L` in the first, where `L` means locked.

**4. Neutralise the key**, since a key works regardless of password state:

```bash
# You already copied it. Now empty it rather than deleting the
# file, so the file's own timestamps remain.
sudo truncate -s 0 /home/svc-update/.ssh/authorized_keys
```

**How you know it worked:**

```bash
# Zero bytes.
sudo ls -l /home/svc-update/.ssh/authorized_keys
```

**Notice the sequencing.** Nothing is destroyed. The account, its home
directory and its files all still exist and remain inspectable, but the
account cannot log in, cannot escalate, and nothing is calling out.

**That is containment**: capability removed, evidence retained.

## Then ask the question containment always raises

**Is it only this machine?**

You have contained UBNT01. You have not established that UBNT01 is the whole
of it, and assuming so is the most common error in real incidents.

**Open your addressing plan from lesson 4.3**, written so you would still be
able to read it this far into the course. This is what it is for: scoping
requires a list of every host that exists, and reconstructing that from
memory during an incident is how machines get missed. Work down the list.

```bash
# Does this account name exist on your domain, too?
# Run on DC01, in PowerShell.
Get-ADUser -Filter "SamAccountName -like '*svc-update*'"
```

```bash
# And on UBNT01: any sign of connections to other lab hosts
# in the window?
sudo journalctl --since "2026-08-05 15:30" | grep -iE '10\.10\.10\.(10|11|30|254)' | head
```

**In this exercise the answer is no, and that is a result you should record
rather than assume.** "Checked DC01 and DC02 for the same indicator; not
present" is a finding. Silence about it is a gap in your report.

**The general shape:** when you find an indicator, ask what else it would
appear on, and go and look. That is what turns a single-host investigation
into scoping.

## Update your note

```markdown
## Actions taken
| Time | Action | Reason | Verified by |
|---|---|---|---|
| 16:12 | Collected artefacts to /var/tmp/incident-2026-01, hashed | Preserve before changing | ls -l; sha256sum output |
| 16:15 | Removed /etc/cron.d/system-health | Stop active beaconing | No further cron executions |
| 16:16 | Removed /etc/sudoers.d/svc-update | Remove privilege | sudo -l -U shows no rights |
| 16:17 | Locked svc-update, shell to nologin | Contain without destroying evidence | passwd -S shows L |
| 16:18 | Truncated authorized_keys | Key auth works despite lock | File is 0 bytes |
| 16:22 | Checked DC01/DC02 for same indicators | Scope beyond this host | Get-ADUser: no match |

**Containment decision:** contained immediately rather than
observing. Reason: [yours].
```

## What you take from this

A contained host with its evidence intact, a deliberate decision about
containment versus observation with the reasoning recorded, and a scoping
check that went beyond the machine you already knew about.

Next lesson you get them out and prove the machine is clean.

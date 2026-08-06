---
title: "DET-05 Watch the files an attacker changes"
sidebar_position: 10
---

# DET-05: Watch the files an attacker changes

|  |  |
|---|---|
| **Objective** | Get an alert when cron, sudoers or an SSH authorised-keys file changes, fast enough to matter |
| **Success signal** | You edit each of the three and an alert naming the file arrives within seconds |
| **Needs** | Module 12 |
| **Effort** | Under an hour |
| **Risk** | Reversible. You are adding monitoring and making test edits you undo |
| **Check** | Mechanical |

## Why this drill exists

If you have finished Module 17, you have already written the recommendation
this drill implements. The capstone report lists it first, marked High:
**enable file integrity monitoring on `/etc/cron.d`, `/etc/sudoers.d` and
authorised-keys files**, with the note that it would have caught three of the
five things you did to your own lab.

Then the course ends and nobody does it.

**Those three paths are not an arbitrary list.** They are where persistence
lives. A scheduled job that runs as root, a file that grants sudo, and a key
that logs someone in without a password. An attacker who reaches any of them
does not need to come back through the front door again.

Not finished Module 17 yet? The drill still works. You are getting to the
finding early rather than after it bites you.

## The trap this drill is built around

Ask whether file integrity monitoring is enabled and the honest answer on your
lab is **partly, and not usefully.**

Wazuh ships with it on, and `/etc` is in the default list of watched
directories. So `/etc/cron.d` and `/etc/sudoers.d` are covered, technically.

**The default scan frequency is 43200 seconds.** Twelve hours. A change made
one minute after a scan sits undetected until the next one, and "we found it
within twelve hours" is not detection, it is archaeology.

Meanwhile authorised-keys files live in home directories, which are **not** in
the default list at all, so that third path is not watched by anything.

**So this is not a drill about turning a feature on.** It is about the gap
between a feature being enabled and a feature being able to catch someone,
which is a distinction you will meet in every security product you ever
operate.

## Your objective

**Make a change to each of the three paths produce an alert you would actually
act on, in seconds rather than hours.**

Four things must be true when you finish:

1. Editing a file in `/etc/cron.d` alerts within seconds, not on the next scan.
2. The same for `/etc/sudoers.d`.
3. The same for an authorised-keys file, which needs watching that does not
   exist yet.
4. The alert tells you **what changed**, not merely that something did.

Point four is the one people skip. "A file in /etc changed" at three in the
morning tells you to get up and go looking. "Line added to
`/etc/sudoers.d/oops`: `www-data ALL=(ALL) NOPASSWD: ALL`" tells you what
happened before you have opened a terminal.

## How you will know

```bash
# On UBNT01. Make a harmless change, then watch the alert arrive.
sudo touch /etc/cron.d/drill-test
sudo tail -f /var/ossec/logs/alerts/alerts.log
```

The real check is the clock. **Time the gap** between making the change and
the alert appearing. If it is minutes or hours rather than seconds, the drill
is not finished, however correct the configuration looks.

<details>
<summary>Nudge, if you do not know where to start</summary>

Before you configure anything, find out what is already being watched. You
almost certainly have some of this already and do not know it, and changing
settings you have not read is how people end up with two conflicting blocks.

The feature is part of the agent, not the manager, and it is configured in the
same file the agent already uses. Wazuh's documentation indexes it under both
its full name and a shorter one that appears in the configuration.

Two questions worth answering before you edit anything:

- **How often does it currently look?** There is a setting for this, it has a
  default, and the default is much larger than you would guess.
- **Which directories are in the default list?** One of your three paths is
  not, and working out which tells you most of what this drill is about.

</details>

<details>
<summary>Fuller hint, if you know the direction but not the syntax</summary>

The feature is **syscheck**, configured in the `<syscheck>` block of
`/var/ossec/etc/ossec.conf` **on the agent**, which for this drill is UBNT01.

The attributes that matter, and each fixes a different failure:

- **`realtime="yes"`** watches continuously instead of waiting for the
  scheduled scan. This is the one that turns twelve hours into seconds.
- **`report_changes="yes"`** includes what actually changed in the alert
  rather than only reporting that the file is different.
- **`check_all="yes"`** checks size, permissions, owner, group, and hashes
  rather than a subset.

Two things that catch people:

- **`/etc` is already in the default configuration.** Adding your own block
  for a path underneath it means two rules cover the same file. Read the
  existing block before adding a new one, and be deliberate about whether you
  are replacing or supplementing.
- **The agent has to be restarted** for `ossec.conf` changes to take effect.
  Nothing warns you, exactly as in INT-01.

And one thing worth thinking about before you enable `report_changes`
everywhere: it puts file contents into alerts. That is the point for
`sudoers.d`. It is a problem for anything holding a secret.

</details>

<details>
<summary>Full walkthrough</summary>

### 1. Find out what is already watched

```bash
# On UBNT01. Read the existing block before changing it.
sudo grep -A 30 "<syscheck>" /var/ossec/etc/ossec.conf
```

Look for two things.

**The frequency.** Expect `<frequency>43200</frequency>`, which is twelve
hours. That single number is why the default configuration would not have
caught the capstone's attacker.

**The directories.** Expect `/etc` to be among them. So `/etc/cron.d` and
`/etc/sudoers.d` are already watched, on that twelve-hour cycle, without
`report_changes`. Home directories are not listed, so authorised-keys files
are not watched at all.

**Write those two facts in your journal before you change anything.** They are
the "before" half of this drill, and they are more interesting than the after.

### 2. Prove the delay is real

Do not take my word for the twelve hours. Make a change and watch nothing
happen:

```bash
# Create a file in a directory that is already monitored.
sudo touch /etc/cron.d/drill-before
```

```bash
# Look for an alert about it. Expect no output.
sudo grep -c "drill-before" /var/ossec/logs/alerts/alerts.log
```

**Expected output: `0`**, and that is the finding. The directory is monitored,
the file is new, and nothing has been reported, because the next scheduled
scan has not run yet.

This is what "we have file integrity monitoring" looks like in a great many
real organisations.

### 3. Watch the three paths properly

Edit `/var/ossec/etc/ossec.conf` on UBNT01 and add these inside the existing
`<syscheck>` block. Substitute your own username in the last line.

```xml
<directories check_all="yes" realtime="yes" report_changes="yes">/etc/cron.d</directories>
<directories check_all="yes" realtime="yes" report_changes="yes">/etc/sudoers.d</directories>
<directories check_all="yes" realtime="yes" report_changes="yes">/home/YOURUSER/.ssh</directories>
```

**Why three separate lines rather than one comma-separated list:** when you
later want different treatment for one of them, and you will, you change one
line rather than unpicking a list. It also makes the configuration readable to
whoever inherits it, which in a lab is you in eight months.

**On `report_changes` and secrets.** You are about to put changed file
contents into alerts. For `sudoers.d` that is exactly what you want. For a
private key it would copy the key into your log. Wazuh has a `<nodiff>`
setting for precisely this, and the shipped configuration already uses it for
`/etc/ssl/private.key`. Worth reading that line and understanding why it is
there before you point `report_changes` at anything sensitive.

### 4. Restart the agent

```bash
# On UBNT01.
sudo systemctl restart wazuh-agent
```

```bash
# How you know it worked. Expect "active (running)".
sudo systemctl status wazuh-agent
```

**If the agent refuses to start, your XML is malformed**, which is the most
common failure here and the same one INT-01 warns about. The agent log names
the line:

```bash
sudo tail -20 /var/ossec/logs/ossec.log
```

### 5. Test all three, and time them

Watch the alert log in one terminal:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.log
```

Then, in another, trigger each path in turn:

```bash
# 1. A scheduled job. This is persistence.
echo '* * * * * root /bin/true' | sudo tee /etc/cron.d/drill-test
```

```bash
# 2. A sudo grant. This is privilege escalation, written to disk.
echo '# drill test, not a real grant' | sudo tee /etc/sudoers.d/drill-test
```

```bash
# 3. An SSH key. This is a way back in that needs no password.
echo '# drill test' >> ~/.ssh/authorized_keys
```

**How you know it worked:** three alerts, each naming its file, each arriving
within seconds. For the second and third, the alert should also carry the
line you added, because `report_changes` is on.

**If an alert names the file but not the change**, `report_changes` did not
take for that path. If an alert never arrives, check that the path in your
configuration matches reality: `~/.ssh` expands to your home directory in the
shell, but `ossec.conf` needs the full path written out.

### 6. Clean up

```bash
# Remove the test artefacts. Each of these should also alert,
# because a deletion is as interesting as a creation.
sudo rm /etc/cron.d/drill-test /etc/cron.d/drill-before /etc/sudoers.d/drill-test
sed -i '/# drill test/d' ~/.ssh/authorized_keys
```

**Watch for those deletion alerts.** An attacker cleaning up after themselves
looks exactly like this, and if your monitoring reports creation but not
removal you have half a control.

</details>

## Going further

- **Find out who changed it.** Wazuh can attribute a change to a user and a
  process rather than only reporting the difference, and on Linux that hooks
  into the audit subsystem. An alert carrying the account and the command is
  one you have already understood; without it you are starting an
  investigation.
- **Do the same on the workstation.** If you built [EXT-07](/drills/extensions/ext-07-windows-client),
  the Windows equivalents of these paths are startup folders, scheduled tasks
  and run keys. Different paths, identical reasoning.
- **Re-run the capstone attack.** Module 17 said this would have caught three
  of five actions. Now that it is configured, find out whether that estimate
  was right. Being wrong about your own coverage estimate is a more useful
  result than being right.

## What this proves

You can take a control that was technically enabled and make it capable of
catching someone, and you can tell the difference between the two states. That
distinction is most of what tuning a security product consists of, and it is
not what a product's own dashboard will tell you.

You also closed a finding from your own assessment, which is the loop that
matters: assess, find a gap, fix it, prove the fix. Most people stop at the
first step and call the document the work.

:::note[Write this down before you close the tab]

In your own words, in your journal, while it is fresh:

- What the default configuration was actually doing, and why "file integrity
  monitoring is enabled" was a true statement that meant very little.
- Which of the three paths was not watched at all, and what someone could have
  done with it.

Six months from now you will remember switching on real-time monitoring, and
not that twelve hours was the number you were living with beforehand.

:::

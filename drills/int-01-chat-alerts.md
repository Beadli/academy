---
title: "INT-01 Get alerts where you will see them"
sidebar_position: 1
---

# INT-01: Get alerts where you will see them

|  |  |
|---|---|
| **Objective** | Make high-severity Wazuh alerts arrive in a chat channel you actually read |
| **Success signal** | You trigger an alert and the message appears in chat within a minute |
| **Needs** | Module 12 |
| **Effort** | Under an hour |
| **Risk** | Reversible. You are adding an integration, not changing detection |
| **Check** | Mechanical |

## Why this one first

Lesson 12.5 called it the queue nobody reads, and it is the most common way a
monitoring stack quietly stops being monitoring. You built the detections, the
rules fire correctly, and the alerts land in a dashboard that nobody opens
between Tuesday and the following month.

An alert that reaches a dashboard is logging. An alert that reaches a person
is detection. This drill closes that gap in about forty minutes, and it is the
cheapest improvement available to you.

## Your objective

**Get Wazuh alerts of level 10 and above into a chat channel, and prove it
by making one fire.**

You need a destination that pushes to you. Slack and Discord both do this for
free and both take about two minutes to set up; either is fine, and the
mechanism is identical because both accept a JSON payload over HTTPS.

Three things have to be true when you are done:

1. A real alert, not a hand-crafted test message, arrives in chat.
2. Only alerts above your chosen level arrive. Everything below stays in the
   dashboard.
3. The message tells you enough to decide whether to get out of bed: which
   host, what fired, and when.

**Point three is the one people skip**, and it is what separates a useful
integration from a noise pipe. A message reading "Wazuh alert" has told you
nothing you did not already fear.

## How you will know

```bash
# On UBNT01, after triggering something. The integration logs
# its own activity, so this is where a failure shows up first.
sudo tail -20 /var/ossec/logs/integrations.log
```

And the real check: **the message is in your chat client.** If you had to go
looking in a dashboard to confirm the alert existed, the drill has not
succeeded yet.

<details>
<summary>Nudge, if you do not know where to start</summary>

Wazuh has a built-in mechanism for this. You do not need to write a script
that tails a log file, and if you find yourself doing that, stop and look
again.

The two things to find: **where you declare an external destination in
`ossec.conf`**, and **what Wazuh calls that feature**. Their documentation
indexes it under the obvious word.

Then think about the level threshold before you enable it. Lesson 12.4 had you
decide what your levels mean; this is the first time that decision has a
consequence you will feel at 3am.

</details>

<details>
<summary>Fuller hint, if you know the direction but not the syntax</summary>

The feature is **integrations**, configured in
`/var/ossec/etc/ossec.conf` inside an `<integration>` block. Wazuh ships
handlers for Slack and for a generic webhook, so you are configuring rather
than writing code.

The fields you need to think about:

- **`name`** selects the built-in handler.
- **`hook_url`** is the webhook URL your chat service gave you.
- **`level`** sets the threshold, and this is the field that decides whether
  this integration is useful or unbearable.
- **`alert_format`** in JSON gives the handler structured data to build a
  readable message from, rather than a flat string.

Two things that catch people:

- **The manager must be restarted** for a change to `ossec.conf` to take
  effect. Nothing warns you.
- **The integration runs as a script on the manager**, so if your manager is
  in a container, the outbound connection comes from inside that container.
  If your firewall or egress rules are strict, that is where it fails.

Before you touch Wazuh at all, prove the webhook itself works. That separates
two problems you otherwise debug together.

</details>

<details>
<summary>Full walkthrough</summary>

### 1. Get a webhook URL

**Slack:** create a workspace if you do not have one, then add an *Incoming
Webhook* app to a channel. It gives you a URL of the shape
`https://hooks.slack.com/services/...`.

**Discord:** channel settings, Integrations, New Webhook, Copy Webhook URL.
Discord's URL needs `/slack` appended if you want it to accept Slack-format
payloads, which is the easy path since Wazuh already speaks that.

**Treat that URL as a credential.** Anyone holding it can post into your
channel. It does not belong in Git, which is the same reasoning as lesson
15.2's backup password.

### 2. Prove the webhook before involving Wazuh

```bash
# Substitute your real URL. Expect the message to appear in chat
# within a second or two.
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test from UBNT01"}' \
  https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**How you know it worked:** the message is in your channel, and curl printed
`ok`.

**If it fails here, stop.** You have a webhook problem, not a Wazuh problem,
and the error is far easier to read now than it will be buried in an
integration log. A 404 usually means the URL is wrong or the app was removed;
a 403 usually means the webhook was revoked.

### 3. Configure the integration

Edit `/var/ossec/etc/ossec.conf` on the manager. If your manager runs in a
container, edit the file on the volume rather than inside the container, so
your change survives a recreate. That is lesson 15.4's point about volumes
being the thing that persists.

Add inside the `<ossec_config>` block:

```xml
<integration>
  <name>slack</name>
  <hook_url>https://hooks.slack.com/services/YOUR/WEBHOOK/URL</hook_url>
  <level>10</level>
  <alert_format>json</alert_format>
</integration>
```

**Why level 10.** Lesson 12.4 had you decide what your levels mean. Ten is
high enough that a message means something and low enough that you will see
one during this drill. Tune it after a week of living with it, not before.

### 4. Restart the manager

```bash
# Native install.
sudo systemctl restart wazuh-manager

# Or, if it runs in a container.
cd ~/docker/wazuh && docker compose restart wazuh.manager
```

**How you know it worked:**

```bash
# The manager came back. Expect "active (running)" or a running
# container, depending on your install.
sudo systemctl status wazuh-manager
```

**If the manager refuses to start, your XML is malformed.** That is the most
common failure in this drill, and the log will tell you the line.

### 5. Make something fire

Do not hand-craft a test message. **Trigger a real alert**, because the point
of the drill is to prove the whole path works, not that curl works.

The quickest reliable trigger, from your own machine:

```bash
# Several failed SSH logins in a row. Answer the password prompt
# wrongly each time. Wazuh's default rules escalate repeated
# failures, which is the behaviour you are relying on.
ssh nosuchuser@10.10.10.20
```

**How you know it worked:** the alert appears in your chat channel, naming
UBNT01 and the rule that fired.

### 6. Read what arrived, critically

Look at the message as though it woke you up. Does it tell you the host, the
rule, and the time? If it does not, the integration is delivering but not
communicating, and that is worth fixing now rather than during an incident.

</details>

## Going further

Each of these is a small extension, and each corresponds to a separate drill
if you want to take it seriously.

- **Route by severity.** Level 12 and above to a channel that notifies you,
  level 10 and 11 to one that does not. That is **INT-02**.
- **Add context before it sends.** A message naming the host's role, not just
  its hostname, is the difference between triage and lookup. That is
  **INT-04**.
- **Alert on the integration failing.** You have just built something that
  can silently stop working, which is exactly the class of problem lesson
  12.8 was about. What tells you when the messages stop?

**That last one is the uncomfortable question**, and it is the right instinct
to finish this drill with. You have added a dependency to your alerting path
and nothing is watching it.

## What this proves

You can take a detection stack that technically works and make it reach a
human. Most home labs never close that gap, and most of the ones that do
close it badly, by sending everything.

Nobody will be impressed that you configured a webhook. The two things worth
having an answer ready for are why you picked level 10 and not 7, and what
you would do about the fact that nothing is watching the integration itself.

Write both in your own words in your journal now, while the reasoning is
fresh. Six months from now you will remember that you did this, and not why
you chose 10.

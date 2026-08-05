---
title: "12.8 Alerting on absence"
sidebar_position: 8
---

# 12.8 Alerting on absence

Every rule you have written so far fires when something happens. This lesson
is about the opposite, and it is the category most detection setups are
missing entirely.

Lesson 9.8 set this up. You disabled the Entra Connect sync schedule and
found that cloud sign-in kept working, on-premises sign-in kept working, and
nothing errored anywhere. The only symptom was that changes stopped
propagating, so a disabled leaver kept their cloud access indefinitely. That
lesson said the thing worth alerting on is not an error, it is **the absence
of an expected event**, and that Module 12 would come back to it.

## Why absence is hard and matters

An error is loud. Something failed, something logged it, a rule matches the
log, you get an alert.

**Absence produces nothing to match.** The agent that stopped reporting sends
no "I have stopped reporting" message. The backup that did not run logs no
failure. The scheduled job that silently stopped being scheduled is not
mentioned anywhere.

And the failure mode is always the same shape: **everything looks fine.** No
red on any dashboard, no alerts in any queue, and a control you believe you
have is not operating.

The three most common examples, all of which are exactly this:

- A log source stops sending, and its machine is now unmonitored
- A backup stops running, and is discovered at a restore
- A sync stops, and offboarding silently half-works

## Wazuh's version: agents that go quiet

The manager knows which agents it expects and when each last checked in.

```bash
# The state of every agent. "Disconnected" or "Never connected" are
# the interesting words here.
sudo /var/ossec/bin/agent_control -l
```

Wazuh raises an event when an agent disconnects, which you can lift to a level
you would act on:

```xml
<!--
  An agent going quiet means a machine is no longer monitored, and
  nothing else will tell you. This is the "absence" case: the symptom
  is the lack of events, not an event.

  Level 12 because an unmonitored domain controller is exactly the
  gap an attacker wants, and because it is rare enough not to be noise.
-->
<rule id="100030" level="12" overwrite="yes">
  <if_sid>503</if_sid>
  <description>Wazuh agent disconnected: $(agent.name) is no longer reporting</description>
  <group>agent_status,availability,</group>
</rule>
```

Prove it. On DC01:

```powershell
Stop-Service -Name WazuhSvc
```

Wait, and the alert should arrive on UBNT01. Then put it back:

```powershell
Start-Service -Name WazuhSvc
```

**Notice what just happened.** You made a machine stop reporting, which is
what an attacker does early, and the system noticed *the silence*.

## The general technique

Absence detection needs three things, and the first is the one people skip.

**A statement of what you expect.** "DC01 reports continuously." "The backup
runs daily by 03:00." You cannot detect a missing thing without first writing
down that you expected it. This is usually the missing piece, and it is not a
technical problem.

**A window.** How long is silence acceptable? Too short and a reboot pages
you; too long and a real gap goes unnoticed. There is no correct answer, only
a decision you should make deliberately.

**Something that checks.** A timer, not an event, because there is no event to
trigger on.

For anything outside the SIEM's own knowledge, that last part is a small
scheduled script:

```bash
#!/usr/bin/env bash
# Alert if the backup marker has not been touched in 26 hours.
# 26 rather than 24: a daily job that drifts by an hour is not a failure,
# and a window with no slack is a window that pages you for nothing.

MARKER=/var/backups/last-success
MAX_AGE=$((26 * 3600))

if [ ! -f "$MARKER" ]; then
  logger -t backup-check -p user.err "No backup marker found at all"
  exit 1
fi

age=$(( $(date +%s) - $(stat -c %Y "$MARKER") ))
if [ "$age" -gt "$MAX_AGE" ]; then
  logger -t backup-check -p user.err "Backup marker is $((age / 3600))h old"
fi
```

`logger` writes to the system log, where your agent already collects, so the
alert path is the one you have. Run it from a systemd timer, per lesson 10.9.

:::tip[Why that is bash, and when it would not be]
Lesson 2.4 suggested "when would I choose Python over Bash?" as a good open
question, and said Modules 10 and 12 would answer with examples. Here is one.

**That script is bash because it is gluing commands together.** `stat`, `date`
and `logger` are separate programs, the logic is one comparison, and there are
no data structures. Bash is a language for orchestrating other programs, and
this is exactly that job.

**It would be Python the moment any of these became true:** it needed to parse
JSON (bash can, via `jq`, but nested logic gets unreadable fast), it needed to
hold state across several checks, it needed to talk to an API, or the
branching got past two or three conditions.

The counting commands in lesson 12.5 are the same judgement going the other
way. `jq | sort | uniq -c | sort -rn` is four programs in a pipe doing what
would be twenty lines of Python, and the pipe is clearer.

**The rule that actually works: bash until you need a data structure.** When
you catch yourself building an array in bash, you wanted Python two steps ago.
:::

:::warning[Absence detection has to be tested, and almost nobody tests it]
A rule that fires on an event gets tested constantly by the event happening.
A rule that fires on absence is tested only when absence occurs, which is
never, until the day it matters.

So it can be silently broken for a year. The check script has a typo, the
timer was never enabled, the rule references a field that changed. Nothing
tells you, because the *expected* state is silence and broken also produces
silence.

**Test it deliberately.** Stop the agent, as you just did. Touch the marker
file to an old date. Once a quarter, break the thing on purpose and confirm
you are told.

This is the same instinct as lesson 10.8's rebuild: **a control you have not
tested is a control you are assuming.**
:::

## The one to take away

If you remember one thing from this module, make it this: **ask what would
fail silently.**

Every system you build from here has an answer, and the answer is nearly
always a thing nobody is watching. The alerts you have written so far were the
easy half. This is the half that catches the failures nobody discovers until
they need the thing.

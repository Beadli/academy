---
title: "IR-08 Clear an alert you cannot immediately explain"
sidebar_position: 10
---

# IR-08: Clear an alert you cannot immediately explain

|  |  |
|---|---|
| **Objective** | Take a real alert from your own queue that you cannot explain on sight, and either clear it or escalate it, with reasoning somebody could check |
| **Success signal** | A written triage note that names the evidence, not a conclusion that names a hunch |
| **Needs** | Module 12. Richer after Module 15, when your lab is generating more of its own noise |
| **Effort** | An evening |
| **Risk** | Safe. You are reading, not changing |
| **Check** | Written. The drill supplies the exact questions below |

## Why this drill exists

You have triaged a false positive before, in lesson 12.6. You scanned your own
lab, watched the alert fire, and concluded it was you.

**Notice what was missing: you already knew the answer.** You caused the
alert deliberately, thirty seconds earlier, and the triage was writing down
something you were never in doubt about. That was the right way to learn the
shape of a triage note. It was not an investigation.

The real skill is the one you have not practised: **an alert you did not cause
on purpose, cannot explain on sight, and have to decide about anyway.**

Most of security work is this. Not incidents, but a queue of things that look
wrong and mostly are not, where the job is to clear them safely and quickly
enough that you still have attention left for the one that matters.

**And there is a trap in only ever practising on real incidents.** If every
exercise you have ever done contained something, you learn to keep digging
until you find something, because finding nothing feels like failing. That
habit is expensive. Clearing correctly is a skill with its own standard, and
this drill is where you meet it.

## Where the alert comes from

You cannot surprise yourself. Anything you plant, you know about.

So do not plant anything. **Your lab has been generating unexplained benign
alerts for weeks.** Ansible runs on a schedule, packages update themselves,
backups run at night, certificates renew, containers restart, cron fires. Some
of that produces alerts you have never looked at, and at least one of them
will not be obvious when you read it cold.

That is your material, and it is better material than anything you could
stage, because you genuinely do not know the answer.

**This is also POA&M-06 from lesson 16.7**, which says audit record review is
performed ad hoc rather than on a schedule, and asks for a weekly review of
the alert queue with each review recorded. This drill is one of those reviews,
done properly.

## Your objective

**Find an alert in your own queue you cannot explain at a glance, then reach a
defensible decision about it.**

Defensible means a specific thing here. Three tests:

1. **You can name the evidence that ties the alert to its cause.** Not the
   cause you assume, the evidence you found.
2. **You can say what would have changed your mind.** If nothing would have,
   you were not investigating, you were confirming.
3. **Somebody else could follow your note and reach the same conclusion**, or
   disagree with it for a reason you could argue about.

"It was probably the backup" fails all three, and it is what most people
write.

## How you will know

There is no command that decides this one, which is why the drill supplies the
questions instead. You are done when you have written answers to these, in
your journal:

- **What fired, exactly?** Rule, host, time, source, and the raw event, not
  your paraphrase of it.
- **What benign explanation did you land on, and what evidence connects it?**
  Name the log line, the schedule, the process, the timestamp that matches.
- **What would have made this an incident instead?** Be specific: what would
  you have needed to see?
- **How long did you spend, and what made you stop?** The honest answer is
  sometimes "I ran out of ideas", and that is worth writing down.
- **Should this alert exist at all in its current form?**

<details>
<summary>Nudge, if you do not know where to start</summary>

Do not go looking for something interesting. Go looking for something
**boring that you cannot immediately account for**, which is a different
search and a harder one.

The queue you built in Module 12 is the source. If everything in it is
obviously explainable, that is itself a finding: either your detections are
too quiet, or you have been unconsciously filtering. Lesson 12.5 was about the
queue nobody reads, and this is what reading it looks like.

Two things to resist once you have picked one:

- **Resist explaining it before you have looked.** You will have a theory
  within about four seconds. Write the theory down, then go and try to
  disprove it rather than confirm it.
- **Resist the tidy ending.** Some alerts do not resolve cleanly, and
  "unexplained, monitored, here is what I checked" is a legitimate and honest
  outcome. It is not a failed drill.

</details>

<details>
<summary>Fuller hint, if you know the direction but not the method</summary>

**Work outward from the event, not inward from your theory.** The order that
holds up:

1. **The raw event.** Not the alert summary, the underlying log line. Alert
   descriptions are written by rule authors who were guessing about your
   environment.
2. **The host, at that moment.** What else happened on that machine within a
   minute either side? Scheduled jobs, package activity, logins, service
   restarts.
3. **Everywhere else, at that moment.** If the same thing fired on four hosts
   at 03:00, you are looking at something scheduled, and that is close to
   proof on its own.
4. **The schedule.** Your own automation runs at times you chose. Module 10's
   playbooks, Module 15's backups, the OS updater. Compare timestamps before
   you theorise about anything else.

**Correlation by time across hosts is the strongest tool you have here** and
it is the one people skip, because it is easier to stare harder at one event
than to go and look at four.

**On stopping:** you are trying to reach *defensible*, not *certain*. Certain
is often unavailable. A note saying "matches the backup window on all three
hosts, same rule, same minute, no process I do not recognise, cleared" is a
good answer even though it is not a proof.

</details>

<details>
<summary>Full walkthrough</summary>

### 1. Pull the queue, not one alert

On UBNT01, look at what has actually fired recently rather than what you
remember firing.

```bash
# The shape of your queue, most frequent first. This is lesson 12.5's
# command, and 12.5 told you to run it weekly forever. This drill is
# one of those weeks.
sudo cat /var/ossec/logs/alerts/alerts.json | \
  jq -r '[.rule.id, .rule.level, .rule.description] | @tsv' | \
  sort | uniq -c | sort -rn | head -20
```

```bash
# And the opposite end: rules that fired once or twice. This is where
# the interesting one usually is, and it is the end nobody reads.
sudo cat /var/ossec/logs/alerts/alerts.json | \
  jq -r '[.rule.id, .rule.level, .rule.description] | @tsv' | \
  sort | uniq -c | sort -n | head -20
```

**Read that count before you pick anything.** The rules at the top are your
noise. The interesting one for this drill is usually further down: something
that fired once or twice, that you do not recognise.

### 2. Pick one you genuinely cannot explain

Write down, before you investigate: **what you think it is.** One line.

You are writing it down so you cannot quietly revise it later, which is the
thing everybody does and nobody notices they did.

### 3. Get the raw event

```bash
# Replace 100020 with your rule id. full_log is the original line that
# triggered the alert, which is what you actually want to read.
sudo cat /var/ossec/logs/alerts/alerts.json | \
  jq -r 'select(.rule.id == "100020") |
         [.timestamp, .agent.name, .full_log] | @tsv'
```

**Read the raw line, not the description.** A rule description says what the
author expected. The log line says what happened.

### 4. Put it on a timeline with everything else

```bash
# Everything that alerted in that window, whatever the rule.
# Substitute your own timestamp prefix; alerts.json timestamps
# look like 2026-08-07T03:14:22.
sudo cat /var/ossec/logs/alerts/alerts.json | \
  jq -r 'select(.timestamp | startswith("2026-08-07T03:1")) |
         [.timestamp, .agent.name, .rule.id, .rule.description] | @tsv'
```

```bash
# And on the host itself: scheduled work, package activity, service
# restarts around that time.
sudo journalctl --since "2026-08-07 03:10" --until "2026-08-07 03:20" | head -60
```

**This is the step that resolves most of them.** Something you scheduled ran,
and the alert is downstream of it.

### 5. Check whether it happened elsewhere

If the same rule fired on more than one host at nearly the same time, you have
found a schedule, not an intruder. Attackers are rarely simultaneous across
machines you chose the maintenance windows for.

```bash
# Same rule, which hosts, what times. If several agents appear with
# timestamps a minute apart, you have found a schedule.
sudo cat /var/ossec/logs/alerts/alerts.json | \
  jq -r 'select(.rule.id == "100020") | [.agent.name, .timestamp] | @tsv' | \
  sort
```

### 6. Write the triage note

Answer the five questions from "How you will know", in your journal, dated.
Follow lesson 12.6's format, and keep the dead ends in, because the things you
checked and ruled out are most of the value to whoever reads it next.

**Then answer the question the drill is really about**, and write this one out
properly rather than thinking it:

> What would I have needed to see to escalate this instead of clearing it?

If you cannot answer that, you have not cleared the alert. You have dismissed
it, and the two look identical in a journal and completely different in a
breach report.

### 7. Decide about the rule

You have just spent an evening on one alert. Was it worth firing?

Three honest outcomes, and the middle one is the most common:

- **Keep it as is.** It is rare and it would matter if it were real.
- **Tune it**, using lesson 12.5's method, so the benign cause stops
  producing it while the interesting version still does. Narrow, and write
  down what you have made yourself blind to.
- **Turn it off**, and record that you decided to, so that the next person
  finds a decision rather than a gap.

**Doing nothing is the fourth outcome and it is the bad one**, because the
alert fires again next week and somebody spends the evening again.

</details>

## Going further

- **Do it weekly, and record each one.** That is literally what POA&M-06 asks
  for, and four dated review notes let you close it with evidence.
- **Track your clear rate.** Over a few weeks, how many alerts did you clear
  and how many were real? If it is a hundred percent cleared, your detections
  may be too quiet rather than your lab too safe.
- **Have a go at the opposite failure.** Deliberately clear something you are
  not sure about, then investigate it properly a week later and see whether
  you were right. Uncomfortable, and the fastest way to calibrate.

## What this proves

You can work an alert queue, which is what the job mostly is, and you can
clear something safely rather than either chasing it forever or waving it
away. Those two failure modes are the common ones and they look like
diligence and efficiency respectively.

The part worth defending is that you wrote down what would have changed your
mind. Anyone can produce a conclusion. Being able to state the evidence that
would have overturned it is what separates an investigation from an opinion.

:::note[Write this down before you close the tab]

In your own words, in your journal, while it is fresh:

- The theory you wrote down before investigating, and whether the evidence
  supported it or you quietly adjusted it along the way.
- What you would have needed to see to escalate, and how close the real
  evidence came to that line.

Six months from now you will remember that the alert was benign. You will not
remember how confidently you assumed that before you had checked.

:::

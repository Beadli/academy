---
title: "17.1 The rules, and the shape of an incident"
sidebar_position: 1
---

# 17.1 The rules, and the shape of an incident

Before you plant anything, two things: the phases an incident moves through,
and the rules you are going to hold yourself to.

## The phases

Incident response frameworks differ in the details and agree on the shape.
Six phases, and each one answers a different question:

| Phase | The question | Where you do it |
|---|---|---|
| **Preparation** | Are we ready? | Modules 12 to 16, already done |
| **Detection and analysis** | What is happening, and is it real? | 17.3, 17.4 |
| **Containment** | How do we stop it getting worse? | 17.5 |
| **Eradication** | How do we get them out? | 17.6 |
| **Recovery** | How do we get back to normal, safely? | 17.6 |
| **Lessons learned** | What do we change? | 17.7 |

**Preparation is the phase that decides how the others go**, and it is the
one you cannot do during an incident. Everything you built from Module 12
onwards was preparation: the logging, the backups you proved restore, the
runbooks, the knowledge of what normal looks like.

That is worth naming explicitly, because it is the argument for this entire
course. **You cannot investigate an environment you do not understand.** An
analyst parachuted into an unfamiliar network with the same skills and the
same tools would be much slower than you are about to be, and not because
they are worse at the job.

## The rules

**Rule one: evidence, not memory.** Stated in the module introduction and
repeated here because it is the one that makes the exercise worth doing.
Every conclusion needs something you can point at.

**Rule two: write as you go, not afterwards.** Lesson 11.6 established this
and lesson 12.6 applied it to triage. Open a note now, before you start, and
timestamp entries as you make them. Reconstructed notes are wrong in ways you
will not notice.

**Rule three: record what you ruled out.** Lesson 12.6 said it: "If you
checked something that turned out to be irrelevant, say so. Someone reading
it later needs to know what was ruled out." An investigation that only
records hits reads as luck.

**Rule four: do not destroy evidence while responding.** The instinct on
finding a hostile account is to delete it immediately. That instinct
destroys the timestamps, the home directory, and the record of what it did.
Containment and eradication are separate phases for exactly this reason, and
17.5 covers the order.

**Rule five: separate what you know from what you infer.** Your report will
have both. Label them. "A cron job exists that runs curl every five minutes"
is an observation. "This is command-and-control beaconing" is an inference,
and a reasonable one, and it is still an inference.

That fifth rule is the one that most distinguishes good analysts, and the
failure mode it prevents is the expensive one: a confident conclusion that
sends everybody in the wrong direction for two days.

## Open your investigation note now

Create `Projects/incident-2026-01.md` in your vault. Adjust the number; if
this is your first, it is 01.

```markdown
# Incident 2026-01

**Status:** investigating
**Opened:** [timestamp, with timezone]
**Investigator:** [you]
**Systems involved:** UBNT01 (10.10.10.20), and anything else found

## Working log
Timestamped, append-only. Newest at the bottom.
Write here as you work. Do not tidy it afterwards; the mess is
the record.

[HH:MM] Opened investigation.

## Observations
Things I can point at. Facts with evidence.

## Inferences
What I think those facts mean, and my confidence.

## Ruled out
Things I checked that turned out not to be relevant, and why.

## Timeline
Built in 17.4. Chronological, with the evidence for each entry.

## Actions taken
Everything I changed, with the time. This becomes the recovery
record and it matters if something goes wrong later.
```

**The separation of Observations from Inferences on the page is not
decoration.** It is a forcing function: when you catch yourself writing an
inference in the observations section, you have caught yourself assuming
something, which is exactly the moment worth catching.

## What normal looks like, and why you should look now

Before the incident happens, spend five minutes recording normal. **This is
the single highest-value thing you can do before an investigation**, and
almost nobody does it because it feels like nothing.

On UBNT01:

```bash
# Accounts that can log in. Know this list BEFORE something
# adds to it.
awk -F: '$3>=1000 && $3<65534 {print $1, $3, $6}' /etc/passwd

# Scheduled jobs, in all the places they hide.
ls -la /etc/cron.d/ /etc/cron.daily/
sudo crontab -l 2>/dev/null || echo "no root crontab"

# Who may use sudo, beyond the defaults.
sudo ls -la /etc/sudoers.d/

# What is listening.
sudo ss -tlnp
```

**Save that output to your investigation note**, under a heading called
"Baseline, captured before the incident". Then when something appears, you
will not be asking "was that always there?", which is the question that
wastes the most time in real investigations.

Lesson 14.2 made the same argument about network scans: "A scan tells you
what is open. A comparison tells you what changed, and change is where
findings live." Same idea, applied to a host.

:::tip[This is the part that transfers]
Capturing a baseline is unglamorous, takes five minutes, and is the reason
some organisations detect intrusions in hours and others in months.

The technical term is **configuration baseline**, and it is CM-2 in the
framework you used in Module 16. You are about to experience directly why it
is a control rather than a nicety.
:::

## What you take from this

Six phases, five rules, an open investigation note, and a baseline of what
normal looks like captured before anything happens to it.

Next lesson, something happens.

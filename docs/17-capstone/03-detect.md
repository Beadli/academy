---
title: "17.3 Detect: what did your lab notice?"
sidebar_position: 3
---

# 17.3 Detect: what did your lab notice?

Ten minutes have passed. Before you go looking at the machine, look at your
monitoring, because the order matters.

**Ask the question your monitoring is supposed to answer, before you go and
find the answer yourself.** If you investigate the host first, you will know
what happened, and you will no longer be able to judge honestly whether your
detections would have told you.

## Open the dashboard and look

Go to your Wazuh dashboard from lesson 12.9. Set the time range to the window
since you started the script.

Write down, in your investigation note, exactly what you see. Not what you
expected. What is there.

**Then answer these four, in writing:**

1. **Did anything fire at all?**
2. **If so, what did it say, and would it have told you what to look at?**
3. **Which of the five actions produced an alert, and which did not?**
4. **Would you have noticed this if you were not looking for it?**

**Question four is the one that matters and the one people skip.** An alert
that fires into a dashboard nobody is watching is not detection, it is
logging. Lesson 12.5 called this the queue nobody reads.

## What you are likely to find

Do not read this until you have written your own answers.

Wazuh ships rules that cover some of this out of the box, so you may see
alerts for the account creation and possibly for the sudoers change. Both are
default rule sets doing their job.

**You are less likely to have caught:**

- **The SSH key added to `authorized_keys`.** This is file-integrity
  monitoring territory, and unless you configured `syscheck` to watch home
  directories, nothing was looking.
- **The cron job.** Same reason: a file appeared in `/etc/cron.d/` and
  nothing was watching that directory.
- **The beaconing.** This is the interesting one. The traffic is outbound
  HTTPS to a legitimate domain on a regular schedule, which looks exactly
  like any other software checking for updates. Lesson 12.7 covered why you
  cannot see inside it, and the detection here would have to be behavioural:
  *this host contacts this destination every five minutes and never did
  before*.

**If your answer to question one is "nothing at all", do not be embarrassed
and do not skip ahead.** That is a finding, it is the most valuable output
this module can give you, and lesson 17.7 has a specific place for it. A
capstone where the monitoring caught everything would teach you less.

## Check the collection, not just the rules

Lesson 14.9 established a distinction worth applying here immediately: **not
collected and not detected are different problems.**

Before concluding your rules are inadequate, check whether the events even
arrived:

```bash
# On UBNT01. Did the agent send anything in the window at all?
sudo tail -50 /var/ossec/logs/alerts/alerts.json | jq -r \
  '[.timestamp, .rule.level, .rule.description] | @tsv' 2>/dev/null | tail -20
```

**How you read that:** if you see entries from your window, collection is
working and the gap is in your rules. If the file is empty or has nothing
recent, collection is the problem and no rule would have helped.

**If `alerts.json` does not exist**, your Wazuh manager is not running or the
path differs; `docker compose ps` in your Wazuh directory tells you which.

Write the answer in your note as an observation, with the command you ran.
That is evidence, and it is the difference between "my monitoring missed it"
and "my monitoring did not receive it".

## And check the logs directly

Regardless of what Wazuh did, the operating system recorded things. This is
your first look at the machine itself:

```bash
# Authentication and privilege events, in the window.
# Substitute your actual start time.
sudo journalctl --since "2026-08-05 15:40" --no-pager | \
  grep -iE 'useradd|usermod|new user|sudo|cron' | head -30
```

**How you know it worked:** you should see lines from `useradd` recording the
new account, and possibly `cron` reloading. Expect something like:

```text
useradd[12345]: new user: name=svc-update, UID=1002, GID=1002, home=/home/svc-update, shell=/bin/bash
```

**Note the UID in that line.** You will use it in the next lesson, and it is
your first piece of hard evidence.

**If `journalctl` shows nothing**, check your time window is right. This is
the most common reason an investigation appears to find nothing, and it is
worth building the habit of doubting the window before doubting the data.

## Now write the honest assessment

In your investigation note, under Observations:

```markdown
## Detection assessment
Window examined: [start] to [now]

| Action | Alerted? | Where it was visible |
|---|---|---|
| Account created | | |
| SSH key added | | |
| Cron job written | | |
| Sudoers rule added | | |
| Outbound beacon | | |

**Would I have noticed without looking?** [honest answer]
**Collection or detection?** [which gaps were which]
```

**Fill that in now, before you investigate further**, because in twenty
minutes you will know what happened and you will not be able to answer
honestly any more. This is the only moment in the module where you can.

## What this connects to

You did this exact exercise in lesson 14.9, with attacks instead of an
incident, and produced a coverage table. **Go and look at it.**

Two questions worth asking:

- **Did you fix the gaps you found then?** POA&M-03 in lesson 16.7 was about
  container log collection. POA&M-06 was about reviewing the alert queue on a
  schedule.
- **Are you finding the same gaps again?** If so, that is not a failure of
  this exercise. It is evidence that a POA&M item did not get worked, which
  is exactly what a POA&M is for and exactly the conversation a real one
  triggers.

**That is the loop from lesson 16.7 closing on you personally**, and feeling
it once is worth more than reading about it.

## What you take from this

An honest, written record of what your monitoring did and did not catch,
captured at the only moment you could still be objective about it, with
collection gaps distinguished from detection gaps.

Next lesson you find out what actually happened.

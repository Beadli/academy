---
title: "12.6 Detect your own scanner"
sidebar_position: 6
---

# 12.6 Detect your own scanner

Lesson 0.1 opened this course with a story: an endpoint tool flagged an attack
toolkit executing on a domain controller, every instinct said breach, and the
investigation ended at a credentialed vulnerability scan doing exactly what it
had been scheduled to do.

Lesson 0.2 said a security analyst's day is that story, and that Module 12
would put you in the seat.

**Here it is.** You are going to generate the alert and triage it.

## Make some noise

From **KALI01**, scan your own lab. Everyone has Kali, so everyone can do this.

```bash
# A service and version scan against the domain controller.
# -sV asks each open port what it is running, which is chatty
# and exactly what makes it visible.
nmap -sV 10.10.10.10
```

If you are on Tier 3 and built OPENVAS01, run a credentialed scan instead.
That is closer to the original story, because credentialed scanning
authenticates rather than just knocking, and authenticated activity is what
makes it resemble an intruder rather than a stranger.

## Watch it arrive

On UBNT01, before you scan, have this running:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json | \
  jq -r '[.timestamp, .rule.level, .agent.name, .rule.description] | @tsv'
```

Depending on what fired, you will see connection attempts, possible port scan
detection, and authentication events if you scanned with credentials.

## Now do the actual job

This is the part that matters, and it is deliberately not a command.

You have an alert. **Work out whether it is real, using only what the alert
tells you, and write down your reasoning as you go.**

Ask, in this order:

**What exactly is it claiming?** Read the rule description and the raw event.
Not the summary in your head.

**Where did it come from?** `agent.name` and the source address in the data.

**When?** Compare it to when you ran the scan. Timing is usually the fastest
discriminator and analysts underuse it.

**Is there a benign explanation that fits all of it?** Here, obviously, yes:
you did it. The discipline is checking that the explanation fits *everything*
in the alert rather than the first field you looked at.

**What would change your mind?** If the source address had been one you did
not recognise. If the timing had been 4am. If it had continued after you
stopped. Naming this in advance is what stops you talking yourself into
"probably fine".

## Why the tool cannot do this for you

The scan looks like reconnaissance because **it is reconnaissance**. Same
packets, same sequence, same protocols. A credentialed scan looks like lateral
movement because it is authenticating to machines in sequence with valid
credentials, which is what lateral movement is.

There is no signature that distinguishes them, because there is no technical
difference. **The only difference is authorisation, and authorisation is not
in the packet.**

That is the whole lesson from 0.1, arrived at from the other side. The tool
was not wrong. It lacked one piece of context, and the context lived in a
person's head.

:::tip[Now put the context in the system]
The analyst's knowledge is a single point of failure, and it is on holiday
next week.

Lesson 12.5's second technique is how you fix that: a rule that suppresses
this specific source, with a comment explaining what it is and what would
still alert.

```xml
<!--
  KALI01 (10.10.10.50) is this lab's authorised testing host.
  Scanning FROM it is expected and is dropped to level 3.

  Deliberately narrow: this only covers this one source address.
  The same activity from anywhere else still alerts at full level,
  which is the property that makes this tuning rather than blindness.
-->
<rule id="100020" level="3">
  <if_sid>5710</if_sid>
  <srcip>10.10.10.50</srcip>
  <description>Authorised scanning host activity</description>
</rule>
```

**Read the comment before you accept the rule.** You are creating a blind
spot on purpose. That is a legitimate thing to do and it must be a decision
somebody can find later, which is why it is written down and in Git.

An attacker who compromises KALI01 now has a quiet place to work from. That is
the real cost, it is a reasonable trade for a testing host, and it is the kind
of trade worth being able to articulate.
:::

## Write it up

Do this properly, because the write-up is the job as much as the triage.

In your journal, record it as a real triage note: what the alert said, when it
arrived, what you checked, what you concluded, and what you changed as a
result.

That format is what an incident ticket looks like. Practising it on something
you know the answer to is how you get fluent at it before you meet one where
you do not.

The habit is also lesson 11.6's: **written while the detail is fresh, with the
dead ends kept in.** If you checked something that turned out to be irrelevant,
say so. Someone reading it later needs to know what was ruled out.

## What you can say about this

You attacked your own lab and then had to work out whether the alert was
real. That is the whole analyst loop, and the exception you wrote afterwards
is the part most people never get to practise.

The part that impresses is not the tooling. It is that you can explain why the
scan was indistinguishable from an attack, and what you did about it.

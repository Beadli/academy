---
title: "12.5 Tuning, and the queue nobody reads"
sidebar_position: 5
---

# 12.5 Tuning, and the queue nobody reads

Leave your lab running for a day and come back to the alert log. There will be
more in it than you expected, and most of it will be your own lab being
itself.

This lesson is about that, and it is the difference between a detection setup
that works and one that exists.

## Look at what you actually have

```bash
# What is firing, and how often? Most frequent first.
sudo cat /var/ossec/logs/alerts/alerts.json | \
  jq -r '[.rule.id, .rule.level, .rule.description] | @tsv' | \
  sort | uniq -c | sort -rn | head -20
```

That command is the most useful one in this module. Run it weekly, forever.

The top few lines are your noise. Not because they are wrong, but because
anything firing hundreds of times a day is not being read, and its presence is
training you to skim.

```bash
# How much of your total volume is the single noisiest rule?
sudo cat /var/ossec/logs/alerts/alerts.json | jq -r '.rule.id' | \
  sort | uniq -c | sort -rn | head -3
```

In most untuned deployments one or two rules produce the majority of alerts.

## The four questions for a noisy alert

For each one at the top of that list, in order. Only the last is "write a
rule".

**Is it wrong?** Does it fire for something that is not what it claims? Then
the rule is broken and it gets fixed or disabled, not tuned around.

**Is it right but expected here?** Your backup job authenticates at 2am every
night. The alert is correct and the behaviour is normal *in this environment*.
This is the common case, and it is what tuning means.

**Is it right, unexpected, and you should fix the cause?** Sometimes the alert
is telling you something true about your lab that you should change. A service
retrying because it is misconfigured, for instance. **Fix the thing, not the
alert.** This case gets missed constantly, because silencing is faster.

**Is it right, unexpected, and rare?** Leave it alone. That is a working
detection.

## Tuning, three ways

Ordered by how much they cost you in coverage.

**Change the level.** The cheapest and most underused. The alert still exists,
still gets recorded, still turns up in a search. It just stops demanding
attention.

```xml
<!--
  Wazuh 5710 is "attempt to login using a non-existent user". It is
  correct and it is constant, because this lab has a Kali box on the
  WAN segment and the internet is the internet.

  Dropped to level 3: recorded, not alerted. A spike is still visible
  in the counts, and rule 100002 below catches the version that matters.
-->
<rule id="100010" level="3" overwrite="yes">
  <if_sid>5710</if_sid>
  <description>Non-existent user login attempt (expected in this lab)</description>
</rule>
```

**Add a condition.** Keep the alert, exclude the specific known-good case.
Narrower than silencing the whole rule.

```xml
<!--
  Suppress the vulnerability scanner's authentication only.
  OPENVAS01 is 10.10.10.60 and scans on a schedule. Any OTHER
  source doing this still alerts at full level.
-->
<rule id="100011" level="0">
  <if_sid>5710</if_sid>
  <srcip>10.10.10.60</srcip>
  <description>Scanner authentication, expected</description>
</rule>
```

**Aggregate.** Do not alert on one; alert on a pattern of them. This is the
technique that turns noise into signal rather than throwing it away.

```xml
<!--
  One failed login is a typo. Eight in two minutes from one source
  is somebody trying passwords. The individual events stay at level 3
  from rule 100010; this fires once on the pattern.
-->
<rule id="100012" level="10" frequency="8" timeframe="120">
  <if_matched_sid>5710</if_matched_sid>
  <same_source_ip />
  <description>Repeated failed logins from $(srcip): possible password guessing</description>
  <group>authentication_failures,</group>
</rule>
```

:::tip[Aggregation is the technique worth internalising]
The first two throw information away. This one changes what the question is.

"Was there a failed login?" is not interesting; there are always failed
logins. "Were there eight from one source in two minutes?" is interesting, and
it is a different question about the same data.

Most good detections are shaped like this. Not *this event happened*, but
*this many, this fast, from this one place, at this hour*. When you find
yourself lowering a rule's level because it fires constantly, ask first
whether there is a count and a window that would make it worth alerting on.
:::

## Write down why

Every tuning decision needs a comment saying what was silenced and why. Look
at the comments above: each says what the rule does, what is being suppressed,
and what would still fire.

Without that, a later reader sees a rule that suppresses alerts and has two
options: leave it and hope, or remove it and get the noise back. **Both are
bad, and both are caused by a missing sentence.**

This is also the argument for the Git repository from 12.4. A tuning change
with a commit message is a decision with a date and a reason attached.

## The number that matters

Not how many rules you have. **How many alerts you would actually look at in a
day.**

If the answer is more than a handful for a lab this size, you are not tuned. A
four-machine lab should be quiet, and every alert that arrives should be worth
the interruption.

That is the standard to hold. When you get to a real environment with a queue
of hundreds, you will at least know what the target looks like, which is more
than many people working in one do.

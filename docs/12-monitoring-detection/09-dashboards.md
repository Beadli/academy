---
title: "12.9 Dashboards, and what they are actually for"
sidebar_position: 9
---

# 12.9 Dashboards, and what they are actually for

**Tier 3 for the building. Everyone should read the argument**, because it is
the part that transfers.

## First, the argument

Dashboards are the most photographed and least useful part of a security
programme. A wall of graphs looks like capability and is frequently not.

**A dashboard cannot detect anything.** It renders what is already known, to a
person who is already looking. Everything that works while you are asleep is a
rule, not a chart. If your alerting is untuned, a beautiful dashboard is a
beautiful picture of an untuned system.

So what are they for? Three things, genuinely:

**Investigation.** Once you know something happened, seeing it in time next to
everything else is how you find what else it touched. This is the strongest
case and it is after the fact.

**Spotting the shape of normal.** Looking at a week of authentication volume
teaches you what your environment does. That knowledge is what lets you write
the rules in 12.5 with sensible thresholds.

**Showing someone else.** A graph of what changed after a fix is how you
demonstrate the fix worked, to people who will not read an alert log.

None of those is detection. All three are worth having.

## Add the indexer and dashboard

The manager holds alerts in a file. Searching a file gets old, and this is what
the other two components are for.

:::warning[Memory, and the number that is not what it seems]
Wazuh's published requirement for the full single-node stack is **4 CPU cores,
8 GB RAM and 50 GB disk**, on top of what UBNT01 already runs.

That figure is sized for thousands of endpoints. You have four. The dominant
consumer is the indexer's Java heap, the memory a **Java Virtual Machine
(JVM)** reserves for the program it runs. It is configurable, and the default
sizing assumes a workload you do not have.

Take UBNT01 to **12 GB** and tune the heap down, below. If your host cannot
spare it, stay on the Tier 1 path: you keep every detection you have written,
and you lose searching and drawing.
:::

Deploy the single-node stack with Docker, from lesson 6.4's skills. Clone
Wazuh's Docker repository, use the `single-node` directory, generate the
certificates their script provides, and bring it up with Compose.

Before you do, set the indexer heap. In the compose file, the indexer service
takes a Java options environment variable:

```yaml
# Default is 1g. For a four-agent lab this is generous already, and the
# published 8 GB figure assumes an index thousands of times larger.
# The rule of thumb elsewhere is half of system RAM; that rule is for a
# machine doing nothing else, which this is not.
- "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"
```

```bash
docker compose up -d
docker compose ps
```

Give it several minutes. The indexer is slow to become healthy and will
refuse connections until it is, which reads as a failure and is not.

:::tip[Heap sizing is a transferable lesson]
You will meet this exact decision with Elasticsearch, OpenSearch, Kafka,
Solr and any other JVM-based data platform.

Two rules, both real: **give it no more than half the machine's memory**,
because the operating system's file cache does the other half of the work and
starving it makes things slower rather than faster. And **never set the
maximum above about 32 GB**, because above that the JVM loses a pointer
compression optimisation and you get *less* usable heap from more memory.

`-Xms` and `-Xmx` set the same value on purpose: fixing the heap avoids the
pauses that come from growing it.
:::

## Grafana, and what to put on it

Grafana is a separate thing and it is worth adding, because it is what you
will meet at work for anything that is not security-specific.

```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

Point it at your Wazuh indexer as a data source and build exactly four panels.
Resist more.

**Alert volume over time**, by level. The single most useful security panel
there is. A spike is worth investigating; a flat line at a high number means
you are not tuned; a sudden drop to zero means something has broken, which is
lesson 12.8's problem in visual form.

**Agents reporting.** A count that should equal the number of machines you
have. Any other number is a question.

**Top rules by volume.** The visual version of 12.5's counting command. It is
your tuning backlog, and it is never empty.

**Authentication successes and failures**, side by side. Their normal ratio
becomes obvious after a week, and a change in the ratio is more informative
than either line alone.

Four panels you look at beats forty you scroll past. The instinct to add more
is the same one that produced the untuned alert queue.

## Prometheus, briefly

Prometheus is in lesson 0.3's Tier 3 line and it is a different job from
everything else here.

Wazuh answers *what happened*, from events. Prometheus answers *what is the
state right now*, from metrics: CPU, memory, disk, request rates. It polls
things that expose numbers, and Grafana draws both.

Worth knowing the distinction rather than blurring it: **events versus
metrics**. A failed login is an event, and you want every one. CPU at 80% is a
metric, and you want it sampled over time. Tools that are excellent at one are
usually poor at the other, which is why environments run both.

If you want it, run it in Docker alongside Grafana with a node exporter on each
machine. It is a good exercise and it is not on the critical path for
detection, which is what this module is about.

## What to take from this

Build the dashboard, then notice how rarely you use it compared to the alert
stream and the counting command from 12.5.

That ratio is the lesson. The dashboard is for investigating and for
explaining. **The rules are what actually watch your lab**, and they were
written before any of this existed.

---
title: "12.10 Grafana, and the difference between events and metrics"
sidebar_position: 10
---

# 12.10 Grafana, and the difference between events and metrics

**Tier 3 for the building. Everyone should read the distinction**, because it
decides which tool you reach for and people get it wrong constantly.

## Events and metrics are different shapes of data

Everything in this module so far has been **events**. A failed login. A process
started. An agent disconnected. Each is a discrete thing that happened at a
moment, and **you want every single one**, because the interesting question is
usually about a specific occurrence.

**Metrics** are different. CPU at 73%. Disk 61% full. 40 requests per second.
These are measurements of a continuous state, sampled on a schedule, and you do
not want every one forever. You want them summarised over time.

<div className="labTable">

| | Events | Metrics |
|---|---|---|
| Example | "sokoth failed to log in at 14:03:22" | "CPU was at 73% at 14:03" |
| You want | all of them, kept | a sample, aggregated over time |
| Question it answers | what happened | what is the state |
| Tool here | Wazuh | Prometheus |

</div>

Tools that are excellent at one are usually poor at the other, which is why
environments run both and why trying to store metrics in a SIEM gets expensive
and slow.

**Grafana draws either.** That is its whole job: a visualisation layer that
connects to many data sources. Which is why it is worth knowing separately from
anything security-specific, and why it is the one tool in this module you are
most likely to meet in a job that has nothing to do with security.

## Run Grafana

```bash
docker run -d --name grafana \
  --restart unless-stopped \
  -p 3000:3000 \
  -v grafana-data:/var/lib/grafana \
  grafana/grafana
```

The volume matters, per lesson 6.5: without it every dashboard you build
disappears the next time the container is recreated, which is a lesson people
usually learn the hard way.

**How we know it worked:**

```bash
# Running, not restarting.
docker ps --filter name=grafana --format '{{.Names}} {{.Status}}'

# Answering. Expect a JSON response with a database status.
curl -s http://localhost:3000/api/health
```

Then browse to UBNT01 on port 3000. The default login is `admin` / `admin` and
it will insist you change it, which is the correct behaviour and worth doing
rather than dismissing.

Add your Wazuh indexer as a data source, then build exactly four panels.
**Resist more.**

**Alert volume over time, by level.** The single most useful security panel
there is. A spike is worth investigating. A flat line at a high number means
you are not tuned. A sudden drop to zero means something has broken, which is
lesson 12.8's problem rendered visually.

**Agents reporting.** A count that should equal the number of machines you
have. Any other number is a question.

**Top rules by volume.** The visual form of 12.5's counting command. It is your
tuning backlog and it is never empty.

**Authentication successes against failures.** Their normal ratio becomes
obvious after a week, and a *change* in the ratio is more informative than
either line alone.

Four panels you look at beats forty you scroll past. The instinct to add more
is the same one that produced the untuned alert queue.

## Prometheus, and why it is here

Prometheus polls things that expose numbers and stores them as time series.
Install a **node exporter** on each machine, which is a small program that
publishes CPU, memory, disk and network figures, and point Prometheus at them.

```bash
docker run -d --name prometheus \
  --restart unless-stopped \
  -p 9090:9090 \
  -v ~/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

**How we know it worked:**

```bash
docker ps --filter name=prometheus --format '{{.Names}} {{.Status}}'

# Which targets is it polling, and are they up? "health":"up" is what
# you want; "down" names the target it cannot reach.
curl -s http://localhost:9090/api/v1/targets | jq -r '.data.activeTargets[] | [.labels.job, .health] | @tsv'
```

A target showing `down` is almost always a node exporter that is not running,
or a firewall rule on the machine you are polling.

Then add Prometheus as a second Grafana data source, and you have one place
showing both what happened and what the state is.

:::tip[Why a security course cares about disk graphs]
It looks like operations rather than security, and there are two reasons it is
both.

**Availability is a security property.** The usual framing is
confidentiality, integrity and availability, and the third gets forgotten
because it feels like somebody else's job. A SIEM whose disk filled up stopped
protecting you, and nothing in your alert queue will say so.

**Metrics catch what events miss.** An attacker exfiltrating data produces
outbound network volume. A crypto miner produces CPU. Neither necessarily
generates an event anyone wrote a rule for, and both are obvious on a graph of
what normal looks like.

That second one is why "monitor your monitoring" is not a joke. Lesson 12.8's
absence detection and this lesson's metrics are two answers to the same
question: **what would fail without telling you?**
:::

## What to take from this if you are not building it

The distinction, and one habit.

**Events and metrics are different, need different storage, and answer
different questions.** When someone proposes putting application metrics into
the SIEM, or alerting on a threshold from a log search, that is usually the
distinction being missed.

And the habit: **look at a week of your own normal before you set any
threshold.** Every number in a detection rule, every alert on CPU, is a
statement about what normal looks like. Most people guess. The graph is right
there.

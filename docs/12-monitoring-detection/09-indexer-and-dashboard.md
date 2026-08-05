---
title: "12.9 The indexer and dashboard"
sidebar_position: 9
---

# 12.9 The indexer and dashboard

**Everyone does this lesson.** You have been reading alerts as JSON at the
command line, which was the right way to learn. Now add the two components
that make a SIEM searchable, because searching is what you will actually do in
the job.

## What these two parts are

**The indexer** stores every alert and makes it searchable. It is OpenSearch,
which is a fork of Elasticsearch, and it is the reason a SIEM can answer "did
anything authenticate as that account last Tuesday" in a second rather than by
reading files.

**The dashboard** is a web interface onto the indexer. It searches, filters,
and draws.

Neither detects anything. The manager you built in 12.2 is still doing all the
detection, and it would keep working if both of these were switched off. What
they add is the ability to *ask questions*, which is most of an analyst's day.

:::info[A dashboard cannot detect, and this is worth being clear about]
A wall of graphs looks like capability and frequently is not. Everything that
works while you are asleep is a rule. If your alerting is untuned, a beautiful
dashboard is a beautiful picture of an untuned system.

What they are genuinely for:

**Investigation.** Once you know something happened, seeing it in time next to
everything else is how you find what else it touched. This is the strongest
case and it is after the fact.

**Learning what normal looks like.** A week of authentication volume teaches
you the shape of your environment, which is what lets you pick sensible
thresholds in 12.5.

**Showing someone else.** A graph of what changed after a fix persuades people
who will not read an alert log.

Build it, then notice how often you still reach for the counting command from
12.5. That ratio is the lesson.
:::

## Memory, honestly

The published requirement for the full single-node stack is **4 CPU cores,
8 GB RAM and 50 GB disk**, on top of what UBNT01 already runs.

**That figure is sized for thousands of endpoints. You have four.** The
dominant consumer is the indexer's Java heap, the memory a **Java Virtual
Machine (JVM)** reserves for the program it runs, and it is configurable.

**Take UBNT01 to 8 GB minimum, 10 or 12 if your host can spare it.** Then tune
the heap down, below, which is what makes this fit.

:::warning[Tier 1, this will be tight, and here is how to make it work]
On a 16 GB laptop your allocation from lesson 0.3 is DC01 at 3 GB, DC02 at 3,
UBNT01 at 6 and KALI01 at 2. Taking UBNT01 to 8 puts you at 16 GB allocated
before the host operating system gets any, which does not work.

So do not run them all at once. **For this module you need DC01 and UBNT01**,
which is 11 GB, leaving your host four or five. Shut DC02 and KALI01 down when
you are not using them, which is what lesson 0.3's "On?" column was for.

This is not a lab compromise, it is the normal condition of running
infrastructure: **resources are finite and tuning is the response.** Being able
to make something fit by understanding what it actually needs, rather than
accepting a vendor's sizing sheet, is a genuinely useful habit.
:::

:::info[If you already have hardware, this is the module where it pays off]
Everything to Module 11 ran comfortably on a laptop. A SIEM is the first thing
in this course that genuinely wants more than one, and if you have a spare
machine or a small rack sitting there, **this is where it stops being a
nice-to-have.**

Something with 32 GB lets you run the full stack without shutting other
machines down, keep DC02 up so replication keeps working while you monitor it,
and leave the indexer with a heap that does not need thinking about.

The [CyberRack](/cyberrack) section describes a build shaped for exactly this,
and its three-node cluster exists partly because a SIEM plus a domain plus
everything else stops fitting on one box.

**This is not a suggestion to go and buy one.** The whole course is designed to
be completed without it, this lesson included, and the tuning above is how. But
if you already have a functional rig, or you have been wondering what one would
actually get you, the honest answer is: it gets you this module without the
juggling.
:::

## Deploy it

Use the Docker skills from lesson 6.4. Clone Wazuh's Docker repository, work in
the `single-node` directory, and run the certificate generation step their
documentation provides before bringing anything up.

**Before `docker compose up`, make three changes.** These are what turn a
production-sized deployment into a lab-sized one.

**Set the heap.** In the compose file, the indexer service takes a Java options
variable:

```yaml
# Default is 1g. For four agents, 512m is ample and leaves room for
# everything else on this machine.
- "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
```

Minimum and maximum are set to the same value deliberately: a fixed heap
avoids the pauses that come from growing one at runtime.

**Turn off replicas.** A single node cannot replicate to itself, so replica
shards sit permanently unassigned, the cluster reports yellow forever, and you
waste effort wondering why. In a single-node deployment set the replica count
to zero.

**Give the dashboard less.** It is a Node.js application and its default
allocation assumes many concurrent analysts. You are one.

```bash
docker compose up -d
docker compose ps
```

**Give it several minutes.** The indexer is slow to become healthy and refuses
connections until it is. That reads as a failure and is not. Watch it:

```bash
docker compose logs -f wazuh.indexer
```

## Get in

Browse to the dashboard on UBNT01's address, port 443, and sign in with the
credentials from the compose file.

**Change those credentials.** They ship as defaults, they are in a file in a
public repository, and this is the same instinct as lesson 6.6's Gitea setup.

:::tip[Put it behind nginx with a real certificate]
The dashboard serves its own self-signed certificate, so your browser will
warn, and you will click through, and clicking through warnings is a habit
worth not building.

You already have the pieces: nginx from lesson 6.7, a certificate authority
from Module 7, and step-ca issuing certificates automatically. Putting the
dashboard behind `siem.lab.internal` with a certificate your machines already
trust takes twenty minutes and removes a warning you would otherwise learn to
ignore.

Lesson 7.10's checkpoint said Module 12 would use those certificates. This is
where.
:::

## Now use it, which is the actual lesson

Deploying it is not the skill. Investigating with it is.

**Find the scan from 12.6.** You know roughly when you ran it. Set the time
range to that window and look at what arrived.

**Filter to one agent.** `agent.name` is the field. This is how you answer
"what was happening on DC01 at the time".

**Filter by rule level.** `rule.level >= 10` strips out everything you decided
was not worth waking up for and leaves what was.

**Search the raw text.** Look for a username, an address, a process name. The
indexer searches inside the events, not just their descriptions.

**Then pivot.** Take a source address from one alert and search for everything
else from it. That single move, from one alert to everything related to it, is
the core of investigation and it is what the command line was making awkward.

## The exercise worth doing

Pick an alert from 12.6 and answer three questions using only the dashboard:

1. What else happened on that machine in the ten minutes either side?
2. Had that source address appeared before, ever?
3. What was the *first* event in the sequence?

That third one is the question that matters in a real incident, and it is the
one a stream of alerts scrolling past cannot answer. Being able to find the
beginning of something is why the indexer earns its memory.

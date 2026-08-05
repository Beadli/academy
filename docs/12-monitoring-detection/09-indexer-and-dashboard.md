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

## Deploy it, one step at a time

This is the most involved deployment in the course. It is three containers
with certificates between them, and the way to get through it is one step at a
time, checking each before moving on.

**Do not skip the checks.** They exist because a failure at step two is
invisible until step four, and by then you will be debugging the wrong thing.

### Step 1: get the files

Wazuh publishes a Docker Compose deployment. Clone it and move into the
single-node directory:

```bash
cd ~
git clone https://github.com/wazuh/wazuh-docker.git -b v4.x --depth 1
cd wazuh-docker/single-node
```

Substitute the current branch for `v4.x`; the repository's README says which
is current, and pinning to a branch rather than tracking `main` means your
deployment does not change under you.

```bash
# What did that give you?
ls
```

You should see `docker-compose.yml`, a `config` directory, and a
`generate-indexer-certs.yml`. Three files, three jobs, and the next three
steps are each about one of them.

### Step 2: generate the certificates

**What we are doing.** Creating the certificates the three containers use to
talk to each other.

**Why.** The indexer refuses unencrypted connections between components. This
is not the same thing as the certificate your browser will see; these are
internal, between containers, and they are generated by a script Wazuh
provides rather than by your own certificate authority.

```bash
docker compose -f generate-indexer-certs.yml run --rm generator
```

**How we know it worked:**

```bash
# Expect a handful of .pem files: one pair per component, plus a root CA.
ls config/wazuh_indexer_ssl_certs/
```

**If this directory is empty or missing, stop here.** Everything downstream
will fail with connection errors that look like networking problems and are
not.

### Step 3: size it for a lab, before starting anything

**What we are doing.** Three edits to `docker-compose.yml`.

**Why.** The defaults are sized for a real deployment. Starting it unmodified
on UBNT01 will either fail or make the machine unusable, and both are harder
to diagnose than just setting the right numbers now.

Open `docker-compose.yml` and make these changes to the `wazuh.indexer`
service:

```yaml
# The Java heap. Default is 1g; 512m is ample for four agents and leaves
# room for everything else already running on UBNT01. Minimum and maximum
# are the same value on purpose: a fixed heap avoids the pauses that come
# from growing one at runtime.
- "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
```

Then, in `config/wazuh_indexer/opensearch.yml`, set the replica count to zero.
**A single node cannot replicate to itself**, so by default the replica shards
sit permanently unassigned, the cluster reports its health as yellow forever,
and you spend an evening wondering what is broken. Nothing is; you asked for a
copy on a second machine that does not exist.

Finally, change the default passwords. They ship in this repository, which
means they are public. Same instinct as lesson 6.6's Gitea setup.

### Step 4: start it, and wait longer than feels right

```bash
docker compose up -d
```

```bash
# All three should appear. "starting" or "unhealthy" at first is expected.
docker compose ps
```

**The indexer takes several minutes to become healthy**, and refuses
connections until it is. During that window the dashboard cannot reach it and
logs errors. **That is not a failure**, and the single most common mistake
here is concluding it is and starting to change things.

Watch it come up rather than guessing:

```bash
docker compose logs -f wazuh.indexer
```

Wait for it to report the cluster is ready, then `Ctrl+C` out of the log.

### How we know the whole thing worked

Three checks, in order, each narrowing where a problem would be.

**One: all three containers are running and healthy.**

```bash
docker compose ps
```

**Two: the indexer answers.**

```bash
# -k because this is the internal certificate, not one your machine trusts.
curl -k -u admin:<your-password> https://localhost:9200/_cluster/health?pretty
```

Look at `status`. **`green` is what you want.** `yellow` almost always means
the replica setting in step 3 was missed. `red` means something is genuinely
wrong. If this command refuses to connect at all, the indexer is still
starting.

**Three: the dashboard loads**, which is the next section.

### When it goes wrong

The failures here are consistent, and knowing them turns an evening into ten
minutes.

**Containers restart in a loop.** Almost always memory. `docker compose logs`
will show the indexer being killed. Check `free -h`, and revisit step 3.

**`max virtual memory areas vm.max_map_count is too low`.** The indexer needs
a kernel setting raised. This is a documented prerequisite and the error names
it exactly:

```bash
sudo sysctl -w vm.max_map_count=262144

# Make it survive a reboot.
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

**Dashboard says it cannot reach the indexer.** Usually you are looking too
early. Give it five minutes. If it persists, step 2's certificates are the
next suspect.

**Cluster health is stuck yellow.** The replica setting from step 3.

**Everything looks fine but no alerts appear.** The stack is up and the
manager is not feeding it. Check the manager is still running with
`sudo systemctl status wazuh-manager`, because the memory pressure from
starting three containers can be enough to disturb it.

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

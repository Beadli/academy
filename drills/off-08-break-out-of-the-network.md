---
title: "OFF-08 Break out of the network"
sidebar_position: 10
---

# OFF-08: Break out of the network

|  |  |
|---|---|
| **Objective** | From KALI01, work out exactly what your lab can reach beyond itself, and whether that matches what you intended |
| **Success signal** | A recorded result for each boundary, and for every one of them you can say whether the answer is the one you wanted |
| **Needs** | Module 4 |
| **Effort** | Under an hour, and much less on later runs |
| **Risk** | Safe. You are sending packets to addresses you own and changing nothing |
| **Check** | Mechanical |

## Why this drill exists

Your lab is going to contain a deliberately vulnerable machine. Module 14
builds one on purpose, and long before that you will have installed
something you did not read the source of.

The question that matters is not whether that machine gets compromised. It is
**what a thing standing on that machine can reach.** If the answer includes
your actual computer, or the network your family is on, then the lab is not a
lab. It is a hole in your house with a hypervisor around it.

Lesson 4.6 tested this once, if you are on Tier 2. Lesson 14.2 tests it again
during an engagement. **This drill is the version you re-run**, after every
firewall change, every new network adapter, every "I just moved that VM to a
different segment for a minute". Boundaries do not decay loudly. They decay
during a change you made for an unrelated reason and forgot.

## Before anything: what you are allowed to touch

This drill sends packets toward your home network. That is the only part of
the course that points at anything outside the lab, so the rule is worth
stating plainly rather than assuming.

**Test single addresses that you personally own. Never scan a range that is
not your lab.**

The difference is not pedantry. Your home network holds equipment that is not
yours: a housemate's laptop, a router your internet provider owns and you
merely rent, a landlord's camera, a family member's phone. Enumerating those
is testing somebody else's estate without their permission, and the fact that
it is easy and that you pay the bill does not make it yours.

**One address answers the question completely.** If KALI01 can reach your
router, the boundary is open, and what else lives back there is not something
you need to find out to know that.

:::warning[If your internet connection is not yours to test]
On university halls, a shared office, a managed building network, or anything
where an IT department exists, **do not run the home-network part of this
drill at all.** Run the first two boundaries, record the third as not tested
and why, and move on. That is a complete result. Somebody else's monitoring
picking up a Kali box probing the gateway is a conversation you do not want
to have.
:::

## Your objective

**Establish what KALI01 can reach beyond the lab, and check each answer
against the one you intended.**

There are three boundaries, and they matter in this order:

1. **The lab LAN**, if you are on Tier 2 and have FW01 between the segments.
2. **Your hypervisor host**, which is the machine you are sitting at.
3. **Your home network**, one address only.

**The correct answer is different for each tier, and knowing which answer you
should be getting is the actual skill here.** A result is only a pass if it
matches your intent. "Failure is the pass" is true for some of these and
flatly wrong for others, which is why this drill asks you to predict before
you test.

Write your predictions down **before** you run anything. A prediction made
after seeing the result is not a prediction.

## How you will know

You are done when you have a small table with a row per boundary: what you
predicted, what happened, and whether that is acceptable to you. Two of the
three questions have no single right answer, only an answer you have decided
on and can defend.

<details>
<summary>Nudge, if you do not know where to start</summary>

You already have every command you need. Lesson 4.6 gave you the pattern for
proving a boundary in both directions, and lesson 4.1 gave you the four
questions a machine asks about its own network.

The part that is new is not technical. It is that **you have to say what you
expect before you look**, because otherwise you will accept whatever you find
as normal. That is the failure mode this drill exists to break.

Start by working out where KALI01 actually sits. On Tier 2 it is on the outer
segment; on Tier 1 there is only one segment and it is on that. Then ask what
sits next to it that is not part of the lab.

**One of those things is the computer you are reading this on.** That is the
boundary people never think to test.

</details>

<details>
<summary>Fuller hint, if you know the direction but not what to look for</summary>

**Boundary one, the lab LAN.** Tier 2 only, and lesson 4.6 already walked it.
From KALI01 on the outer segment, the inner segment should be unreachable.
Tier 1 has no firewall and one segment, so this boundary does not exist for
you, and the honest answer is "not applicable, because my lab is flat".

**Boundary two, your hypervisor host.** Look again at the addressing plan in
lesson 4.3. The first row is `10.10.10.1`, described as *your own computer's
adapter on this network*. Your laptop is on the lab network. It has always
been on the lab network. Most people build a lab for a year without once
noticing that the attacker box can reach the machine they do their banking on.

Whether that is acceptable is a decision, not a defect. But it should be a
decision you have made rather than one you inherited from a wizard.

**Boundary three, your home network.** One address, the router, and only if
the connection is yours. See the warning at the top.

**On tooling:** `ping` is not proof of unreachability on its own, because
plenty of things drop ICMP while happily accepting TCP. If a ping fails,
confirm with a TCP connection attempt to a port something is likely
listening on before you record it as blocked.

</details>

<details>
<summary>Full walkthrough</summary>

### 1. Write your predictions first

Before a single packet. In your journal:

| Boundary | I expect | Because |
|---|---|---|
| Lab LAN from KALI01 | | |
| Hypervisor host | | |
| Home router | | |

Fill the first two columns now. **If you cannot fill in "because", that is
the finding**, and it is a more useful one than anything the commands are
about to tell you.

### 2. Find out where KALI01 actually is

```bash
# On KALI01. Address, gateway, and what it uses for DNS.
# These are lesson 4.1's four questions, asked in one go.
ip -brief addr
ip route
resolvectl status | grep -i "dns server"
```

Note the gateway address. On Tier 2 with KALI01 outside, that is your
hypervisor's NAT gateway. On Tier 1 it is the same thing, because there is
only one network.

### 3. Boundary one: the lab LAN

**Tier 2 only.** Skip to step 4 if you have no firewall, and record this row
as not applicable rather than leaving it blank.

```bash
# Can the outside reach the firewall's inside interface?
ping -c 3 10.10.10.254
```

```bash
# And can it reach anything behind it? Host discovery across the
# lab range only. This is your network, in your scope.
sudo nmap -sn 10.10.10.0/24
```

**Expect both to fail**, and here failure genuinely is the pass. This is
lesson 4.6's result, and re-running it is the point: you are confirming that
whatever you have changed since then did not quietly open it.

**If something answers that did not answer in Module 4, stop and find out
why before doing anything else.** That is a regression in a security control,
which is exactly the class of problem this drill is meant to catch.

### 4. Boundary two: your hypervisor host

This is the one nobody tests.

```bash
# Your own computer, on the lab network. Substitute the gateway
# address from step 2 if yours differs.
ping -c 3 10.10.10.1
```

It will almost certainly answer. Now find out what is actually exposed on it:

```bash
# A port scan of ONE address: the machine you are sitting at.
# This is yours, so it is in scope, and it is the only host
# outside the lab proper that this drill scans.
sudo nmap -Pn --top-ports 100 10.10.10.1
```

**Read that output as though you found it on a client's network.** File
sharing, remote desktop, a development server you left running, a database
you installed last year. Every open port there is reachable from a machine
whose entire purpose is to run attack tools, and by Module 14 it will be
reachable from a deliberately vulnerable target as well.

**What to do about it is a judgement call, and the drill will not make it for
you.** The options, roughly in order of how much they cost you:

- Accept it, having looked, and write down that you accepted it.
- Close the ports you did not mean to have open, which is worth doing
  regardless of this lab.
- Move the lab onto a host-only network with no route to your host's other
  interfaces, and accept that the lab loses easy internet access.
- Run the lab on a machine you do not otherwise use.

**Most people should pick the first or second and get on with the course.**
The reason this step exists is not to frighten you into a rebuild. It is so
that when an interviewer asks what your lab's exposure is, you have looked.

### 5. Boundary three: your home network, one address

Only if the connection is yours to test. Re-read the warning at the top of
this page if you are not certain.

```bash
# Find your router's address from your OWN computer first.
# Windows PowerShell:
ipconfig
```

```bash
# Linux or macOS, on your own computer:
ip route | grep default
```

Then, from KALI01, that single address:

```bash
# ONE address. Not the range. Substitute your real router address.
ping -c 3 192.168.1.1
```

If ping fails, confirm before you celebrate, because plenty of routers drop
ICMP and answer TCP perfectly happily:

```bash
# A single port on a single address. -Pn skips the ping check,
# which is the point, since the ping is what just failed.
sudo nmap -Pn -p 80,443 192.168.1.1
```

**Whether you want this to fail depends on your tier**, and this is the row
where people record the wrong verdict:

- **Tier 2, with FW01 doing its job:** you probably still reach the router,
  because KALI01 sits on the *outer* segment, which is the segment that has
  internet access by design. Your firewall protects the lab LAN from KALI01.
  It was never protecting your house from KALI01.
- **Tier 1:** you will reach it. There is no boundary. That is not a broken
  lab, it is a flat one, and now you know.

**That distinction is the most useful thing in this drill.** People assume a
firewall in the lab protects the house. It protects one lab segment from
another. Nothing in the course, at any tier, puts a boundary between your
attacker box and your home network unless you build one deliberately.

### 6. Record it, in a form you can re-run against

Finish the table. Then write one line under it: **the date, and what you
changed since the last run.** That line is what makes this a regression test
rather than a one-off curiosity.

The course's own security assessment in Module 16 has an open item about
re-testing the boundary after firewall changes. This table is the evidence
that closes it, and "we tested it once when we built it" is not.

</details>

## Going further

- **Do it from a compromised machine instead.** Module 14 leaves you standing
  on a machine inside the lab. Reachability from there is a different and more
  honest question than reachability from the box you already control.
- **Build the boundary this drill keeps finding missing.** A second firewall
  interface, or a host-only network with no NAT, between your lab and
  everything else. Then re-run this drill and watch the rows change.
- **Automate it.** The commands are fixed and the expected answers are
  written down, which is the definition of something that should be a script
  you run rather than a page you follow.

## What this proves

You know what your lab can reach, which sounds obvious and is a question most
people who own a home lab cannot answer. You also know the difference between
a boundary you built and a boundary you assumed, and you found at least one
of the second kind, because everybody does.

The part worth defending is not that you ran some scans. It is that you wrote
down what you expected first, and that you can name what you decided to accept
rather than fix.

:::note[Write this down before you close the tab]

In your own words, in your journal, while it is fresh:

- Which of your three predictions was wrong, and why you had expected
  otherwise.
- What your attacker box can reach that you have decided to live with, and
  what would have to change for that decision to stop being reasonable.

Six months from now you will remember running the scans, and not what you
chose to accept.

:::

---
title: "CyberRack: start here"
sidebar_position: 0
slug: /
---

# CyberRack

**An enterprise mini infrastructure platform.** A physical lab small
enough for a desk, a dorm room, or an apartment, that behaves like a
miniature datacentre.

This section is for one specific person: you've decided you want real
hardware, you can afford some, and you have no idea what to buy or in what
order. That's a genuinely hard problem, and most of the advice online is
bad. It's either somebody showing off a rack that cost more than a car, or
a forum thread where six people recommend six different things and nobody
asks what you're trying to learn.

CyberRack is a specified answer: a documented design where every component
exists to teach a named enterprise skill, and where the reasoning is
written down so you can disagree with it deliberately rather than by
accident.

:::warning[Status: designed, not yet built]
This is a specification, not a build log. The hardware has been chosen and
the architecture worked out, but nobody has assembled it yet, so every
number here (power draw, noise, prices) is a **design target or an
estimate**, not something measured off a running rack.

That's worth saying plainly because the rest of this course leans on war
stories from a lab that genuinely runs, and this section can't. Read it as
a design you can copy and argue with. When it exists, the figures get
replaced with real ones and this box goes away.
:::

:::note[You do not need any of this to take the course]
Be precise about what the course does and doesn't require, because the
difference matters if you're deciding what to spend.

**Tier 1 needs 16 GB and no purchase at all.** On a computer you already
own, laptop or desktop, that covers most of the curriculum: Active
Directory including replication and FSMO roles, Linux, Docker, Ansible,
scripting, packet capture, basic detection and basic attacks.

**Tiers 2 and 3 need more memory**, and the course says so at the top of
every module that does. The firewall lessons in Module 4, the two
certificate authorities in Module 7 and the single sign-on server in
Module 8 want 32 GB. The full monitoring stack wants 64 GB.

But **more memory is not the same as a rack.** Tier 2 is usually a RAM
upgrade to a machine you already have, often under $100 and the best value
purchase in this whole section. Nothing in the curriculum requires the
build described here, at any tier.

CyberRack sits **beside** the course, not inside it. If you're partway
through a module and wondering whether you're missing equipment, you
aren't. Go back and carry on.
:::

## What's here

- **[Do you actually need one?](./do-you-need-one)** The honest signals
  that a laptop has stopped being enough, the cheaper answers to try
  first, and the running costs people forget.
- **[What to buy first](./what-to-buy-first)** The incremental path, in
  stages of a few hundred dollars each. You do not start by buying a rack.
- **[The v1.0 build](./build)** The full specification: compute, storage,
  firewall, switching, VLANs, power budget, and what each choice teaches.
- **[The project charter](./charter)** The complete design document,
  published as-is. Also worth reading as an example of what professional
  infrastructure documentation looks like, which is something this course
  keeps telling you matters and can otherwise only describe.

## The rule the whole design runs on

Every purchase has to answer one question:

> **What enterprise skill does this teach me?**

If the answer is unclear, don't buy it yet.

A lab is not a collection of equipment. It's an environment for practising
things you'll be paid to do, and the equipment is a means to that. Plenty
of people spend thousands assembling something impressive that teaches
them nothing they didn't already know, because they bought hardware before
they had a learning objective for it.

Buy the smallest thing that unblocks the next skill you want. Then use it
until it hurts. The pain tells you what to buy next, more reliably than
any recommendation, including this one.

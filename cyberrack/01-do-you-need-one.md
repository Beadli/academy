---
title: "Do you actually need one?"
sidebar_position: 1
---

# Do you actually need one?

Before spending anything, it's worth being honest about whether hardware
solves your problem. Sometimes it does. Often the real constraint is
somewhere else and a purchase just moves the frustration.

## The signals that a laptop has genuinely stopped being enough

These are the ones I'd act on:

- **You're out of memory, repeatedly.** Not once during a heavy module,
  but routinely. You're shutting down one machine to start another and it
  interrupts what you're actually trying to learn.
- **You want things to stay running.** A lab you rebuild every time you
  close the lid is fine for lessons and useless for anything that needs to
  observe over time: monitoring, log collection, backup schedules,
  certificate renewals. Half the interesting failures only appear after a
  few days of uptime.
- **You want to break things properly.** There's a category of learning
  that involves genuinely wrecking a machine, pulling a disk, or cutting
  power mid-write. Doing that on the laptop you also work on is a bad idea.
- **You want to practise the physical layer.** VLANs on a real switch,
  cabling, a firewall appliance with actual interfaces. You can simulate a
  lot of this, and at some point simulation stops teaching you the thing
  that goes wrong in a datacentre.

## The cheaper answers to try first

Every one of these has solved the problem for somebody who was about to
spend money:

- **More RAM in the machine you own.** Frequently the single best
  price-to-relief ratio available, and often under $100. Check what your
  laptop's maximum is before assuming you need a new machine.
- **An external SSD.** If your complaint is disk space rather than memory,
  this is a fraction of the cost of a server.
- **Shut things down.** Genuinely. The course's Tier 1 works because
  machines that aren't in use are powered off. If everything you own is
  running all the time, you have a habit problem rather than a hardware
  problem.
- **Cloud, briefly.** For a specific experiment that needs more machine
  than you own, a few hours of a large cloud instance costs less than
  lunch. It's a bad permanent home for a lab and an excellent temporary
  one.

## The costs people forget

If you're still reading, budget for these, because they're what turns an
exciting purchase into a regret:

**Electricity.** A lab running continuously costs real money every month,
forever. Work out your local rate per kilowatt-hour and multiply. A build
drawing 125 watts costs roughly 90 kilowatt-hours a month, which at $0.15
is about $13.50. That's manageable; at 500 watts it isn't.

**Noise.** Enterprise servers from eBay are cheap because they sound like
a hairdryer and were designed for a room nobody sits in. If the lab lives
where you sleep or work, this decides what you can buy far more than price
does.

**Heat.** Everything above turns into warmth in a room you're in.

**Time.** Hardware you own is hardware you maintain. That's part of the
learning, and it's also evenings you don't spend on the curriculum.

**Where it lives.** Whether the machine is welcome in a shared space is a
real constraint and worth settling before it arrives rather than after.

## The honest recommendation

Finish the course first, or at least get well into it.

By Module 12 you'll know which parts of infrastructure you actually enjoy,
and that changes what you should buy. Somebody who discovered they love
detection engineering needs memory and storage for logs. Somebody drawn to
networking needs a managed switch and a firewall with real interfaces.
Somebody heading for platform engineering wants nodes for a cluster.

Buying before you know which of those you are is how people end up with
expensive hardware that doesn't fit the thing they turned out to care
about.

If you've read all that and still want one, the [next
page](./what-to-buy-first) is the order I'd buy in.

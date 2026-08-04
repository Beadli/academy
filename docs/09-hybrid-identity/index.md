---
title: "Module 9: Hybrid identity with Entra ID"
sidebar_position: 0
---

# Module 9: Hybrid identity with Entra ID

Almost no enterprise runs purely on-premises anymore, and almost none runs
purely in the cloud either. What they run is **hybrid**: the Active Directory
you built in Module 5 stays the source of truth for identity, and it
synchronises to a cloud directory that fronts email, SaaS applications, and
everything else the business signs in to.

This module builds that bridge with your own domain. By the end, the account
you created for Sam Okoth in Module 5 will exist in a cloud directory, sign in
to a cloud service, and disable itself in the cloud when you disable it on
your domain controller. You will have built every piece of that chain.

What's in it:

- **9.1** what hybrid identity is, and which direction authority flows
- **9.2** the UPN problem, and why `lab.internal` will never be enough
- **9.3** getting a tenant, honestly
- **9.4** install Entra Connect Sync against your own domain
- **9.5** watch your users arrive, and drive the sync yourself
- **9.6** what actually crossed the wire
- **9.7** disable an account and follow it
- **9.8** what breaks when the bridge goes down
- **9.9** journal entry
- **9.10** checkpoint

## Read this before you start

This module is different from the eight before it, in a way that matters
enough to say plainly rather than bury.

:::warning[This is the one module that depends on somebody else]
Everything else in this course runs on hardware you control, with software
that will still install in five years. This module needs an account with
Microsoft, and Microsoft changes the rules about who can have one for free.

**Lessons 9.1 and 9.2 need no cloud account at all.** They are concepts and
real Active Directory work, and 9.2 in particular fixes something in your
domain that would block a real migration. Do them regardless.

**From 9.3 onward you need a tenant.** Lesson 9.3 covers the current routes
and what each one actually costs, including which ones want a card and which
ones expire. If none of them work for you today, read 9.4 to 9.8 anyway. They
are written so the reasoning survives without the clicking, and you will meet
this again with an employer's tenant.
:::

**Tier 2 and up.** You need the domain from Module 5, which means DC01. There
is no Tier 1 path here, because there is nothing to synchronise without a
directory.

**DC01 needs more memory for this module.** Entra Connect Sync asks for 4 GB
of RAM and 70 GB of disk, and your DC01 was built with 3 GB and 60 GB.
Lesson 9.4 walks through raising it, which takes two minutes because it is a
virtual machine, and that is a decent illustration of why you built one.

Budget an evening for 9.1 to 9.5, and a second for the rest. Expect the sync
to fail once before it works. It nearly always does, and the failure is nearly
always the UPN problem from 9.2 catching someone who skipped it.

## Where this sits

Module 5 built a directory. Module 8 taught applications to trust it. This
module extends it past your own network, which is what every organisation you
will work for has already done.

There is a reason it comes ninth rather than first. Cloud identity is a
synchronisation *of* something, and people who start here learn to click
through a portal managing users whose origin they have never seen. You will be
syncing a directory you built, from a domain controller you promoted, using
accounts you created. That is the difference between operating a system and
operating a screen.

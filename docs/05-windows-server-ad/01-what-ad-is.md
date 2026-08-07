---
title: "5.1 What Active Directory is"
sidebar_position: 1
---

# 5.1 What Active Directory is

Before you install anything, ten minutes on what you're installing.
People who skip this end up with a working domain they can't reason
about, which is fine right up until something breaks.

## A database, a protocol, and a promise

Active Directory is a **database of who and what exists** in an
organization: every user, every computer, every group, every printer if
anyone still cares about printers. It's stored on machines called
**domain controllers**, and this module builds your first one.

Two things make it more than a spreadsheet.

It's **queryable over the network**, by a protocol called **LDAP**, the
Lightweight Directory Access Protocol. The name is a historical joke at
this point (its predecessor was heavier), but the idea is simple: a
standard way to ask a directory questions. When an application asks
"does the account `jsmith` exist, and which groups is it in?", that's an
LDAP query to a domain controller. It matters because it's not a
Microsoft invention: the same protocol queries directories on Linux and
in cloud services, so once you can read an LDAP query you can read them
everywhere. You'll watch this
happen in lesson 5.11.

And it **vouches for people**. When someone logs in, the domain
controller checks their password and issues them a cryptographic ticket
saying "this really is jsmith." Every service they touch afterwards
trusts that ticket instead of asking for the password again. That
ticketing system is **Kerberos**, and it's the reason you sign in once
in the morning and then reach a dozen systems without typing your
password again. Lesson 5.5 shows you your own tickets.

## The words people will use around you

You'll hear these constantly, and they're simpler than they sound:

**Domain.** One directory with one set of accounts and one security
boundary. Yours will be `lab.internal`.

**Forest.** One or more domains sharing a common configuration and
trusting each other. Yours will contain exactly one domain, which is
also true of an enormous number of real companies.

**Domain controller (DC).** A server holding a copy of the directory
and answering authentication requests. Production runs at least two,
because a single DC means a single point of failure for logging in.
Your lab runs one, and knowing why that's a compromise is part of the
lesson.

**Organizational Unit (OU).** A folder inside the domain for
organising objects. OUs exist mainly so you can apply different settings
to different groups of machines and people, which you'll do in 5.7.

**Object.** Anything stored in the directory: a user, a computer, or a
group.

## Why DNS is not a separate topic

Here's the part that catches people out, and the single most useful
thing in this lesson.

**Active Directory runs on DNS.** Not "uses" it. Runs on it. When a
computer needs to find a domain controller to log a user in, it doesn't
broadcast or guess: it makes a DNS query for a special record type that
says "which servers here provide authentication for this domain?" Domain
controllers publish those records about themselves. No DNS, no answer,
no login.

This is why your domain controller is also going to be your DNS server,
why the promotion wizard installs DNS without really asking, and why in
this lab every machine's DNS must eventually point at `10.10.10.10`
rather than at your router or a public resolver. A machine pointed at a
public DNS server can browse the internet perfectly and still be unable
to log in to your domain, which is a confusing failure the first time
you meet it.

There's a saying in operations, worn smooth from overuse because it
keeps being right: **it's always DNS.** In Active Directory it's true
more often than anywhere else. When something in your domain misbehaves
over the next twelve modules, check DNS first. You will be right often
enough to feel psychic.

:::tip[What this is called at work]
Active Directory needs no substitute here either: **the thing you are about to
build is the thing organisations run**, and it has been the backbone of
corporate identity for twenty-five years. A domain controller in a bank does
what DC01 will do, with more of everything.

**What scale changes is caution, not concepts.** Sites and replication
topology matter when controllers are in different countries. Group Policy
becomes hundreds of objects with conflicting precedence. And nobody makes
changes on a Friday, because the failure mode is that nobody in the company
can log in.

**The direction of travel is worth knowing.** Many organisations now run this
alongside **Microsoft Entra ID** rather than replacing it, which is Module 9's
whole subject. On-premises Active Directory is not going away, and being able
to explain how the two relate is more employable than either alone.
:::

## What you're about to build

One Windows Server, promoted to be the first domain controller of a new
forest, holding the domain `lab.internal`, serving DNS for it, and
sitting at `10.10.10.10` where your addressing plan said it would.

Everything after this module attaches to it.

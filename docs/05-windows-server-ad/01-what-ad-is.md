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

It's **queryable over the network**, by a protocol called LDAP. When an
application asks "does the account `jsmith` exist, and which groups is
it in?", that's an LDAP query to a domain controller. You'll watch this
happen in lesson 5.8.

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

## What you're about to build

One Windows Server, promoted to be the first domain controller of a new
forest, holding the domain `lab.internal`, serving DNS for it, and
sitting at `10.10.10.10` where your addressing plan said it would.

Everything after this module attaches to it.

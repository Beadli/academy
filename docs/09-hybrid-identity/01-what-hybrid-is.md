---
title: "9.1 What hybrid identity is, and who is in charge"
sidebar_position: 1
---

# 9.1 What hybrid identity is, and who is in charge

Your domain knows who Sam Okoth is. It knows her password, which groups she
belongs to, and whether her account is enabled. Every machine you have joined
to the domain asks DC01 those questions and believes the answer.

Now she needs to open her email, which is not on your network. It is hosted by
a company that has never heard of DC01 and never will.

That is the problem hybrid identity solves, and there are only three honest
answers to it.

**Give her a second account.** One for the office, one for the cloud, each with
its own password. This is what organisations did first and it is a quiet
disaster: two passwords that drift apart, two accounts to disable when she
leaves, and one of them will be forgotten. The forgotten one is how people get
breached months after an employee walks out.

**Move everything to the cloud.** Delete the domain, run the business from a
cloud directory. Some small companies genuinely do this and it works for them.
It stops working the moment you have something that must run on your own
network, which for most organisations is a file server, a line-of-business
application nobody will rewrite, or a printer.

**Sync one directory into the other.** Keep the domain as the place people are
created, changed and disabled, and copy what the cloud needs. One account, one
password, one place to disable it.

The third is hybrid, and it is what nearly everyone runs.

## The direction matters more than the mechanism

Here is the sentence to carry out of this module:

**Your on-premises Active Directory is the source of truth. The cloud
directory is a copy.**

Everything else follows from that. When you change Sam's job title in AD, it
appears in the cloud within half an hour. When you try to change it in the
cloud, you get an error, because the object is marked as owned by something
else. When you disable her account on DC01, the cloud disables it too.

That last one is why organisations do this at all. **Offboarding becomes a
single action.** One disable on the domain controller, and access to email,
files and every SaaS application wired into that directory stops together. The
alternative is a checklist of twelve systems, and checklists get half-done.

:::tip[The word for this is "authoritative"]
You will hear people say Active Directory is *authoritative* for identity, or
that an attribute is *sourced from* on-premises. Both mean the same thing: one
system decides, the others copy. Being able to answer "which system is
authoritative for this?" is most of what identity architecture is.

It is also the first question worth asking in an incident. If somebody's
account is behaving strangely in the cloud, the answer is usually not in the
cloud.
:::

## What actually gets synchronised

Not everything, and this surprises people.

**Users, groups and contacts** cross, along with a defined set of attributes:
name, sign-in name, email address, job title, department, whether the
account is enabled. It is a fixed list, not a copy of the object.

**A password hash crosses**, if you choose the default sign-in method, which
you will in 9.4. Lesson 9.6 goes into what that means, because "your password
is in the cloud" is both what people fear and not what happens.

**Group Policy does not cross.** Nothing does. GPOs are an on-premises
mechanism for domain-joined Windows machines, and the cloud has an entirely
separate system for policy on devices. People assume Group Policy follows
their users into the cloud and it does not, ever.

**Computer objects mostly do not cross**, and where they appear to, it is a
different feature doing different work.

The useful mental model: this is not a directory replica. It is a defined,
one-way feed of specific attributes into a different product with different
rules, which happens to be run by the same company.

## Three ways to handle the password

You will pick one in 9.4. They are worth knowing by name now, because the names
come up in interviews and the difference is genuinely architectural.

<div className="labTable">

| Method | Where the password is checked | If your network goes down |
|---|---|---|
| **Password hash sync (PHS)** | In the cloud, against a synced hash | Cloud sign-in keeps working |
| **Pass-through authentication (PTA)** | On your domain controller, via an agent | Cloud sign-in stops |
| **Federation** (AD FS, from Module 8) | On your federation server | Cloud sign-in stops |

</div>

You are going to use **password hash sync**, and not only because it is the
simplest. It is the one that keeps working when your building loses power,
which is the scenario the other two quietly fail. Organisations that federated
everything to an on-premises AD FS farm discovered this the hard way during
outages: their cloud email, hosted by a company with better uptime than they
had, was unreachable because the thing checking passwords was in a cupboard
that had just lost a switch.

You built an AD FS server in Module 8, so you have seen the third option from
the inside. That is exactly why it is worth understanding why you would not
reach for it here.

## What this module will not do

It will not make you an Entra ID administrator. That is a large product with
its own certification track.

It will do something narrower and more useful: take a directory you built
yourself, extend it into a cloud directory, and let you watch which system
wins when the two disagree. Almost nobody arriving at their first hybrid
environment has seen that from both ends. You will have.

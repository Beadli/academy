---
title: "8.1 What single sign-on actually is"
sidebar_position: 1
---

# 8.1 What single sign-on actually is

Count the passwords you have for work things. In a small organization it's
maybe five. In a large one it's forty, and about thirty of them are the
same password with a different number on the end.

That is the problem single sign-on exists to solve, and framing it as a
convenience feature undersells it badly. Password reuse across dozens of
systems is not a user failing, it's an architecture failing, and the fix is
to stop asking applications to store passwords at all.

## The idea, in one paragraph

**Applications stop checking passwords. One system checks, and the
applications trust that system.**

When you open the application, it doesn't ask who you are. It redirects you
to the one system that knows, waits for that system to send back a signed
statement saying "this is Sam Okoth, I verified it, here's when", and lets
you in on the strength of that statement.

The application never sees your password. It cannot leak your password,
because it never had it.

## The three parties, and their real names

Every federation conversation has exactly three participants, and every
protocol in the next lesson names them slightly differently. Learn the
roles now and the vocabulary stops mattering.

<div className="labTable">

| Role | What it is | In your lab |
|---|---|---|
| **The user** | A person with a browser | You |
| **Identity provider (IdP)** | The one system that verifies people | AD FS, or Keycloak |
| **Service provider (SP)** | The application you're trying to use | Gitea |

</div>

The service provider is also called the **relying party**, because it
relies on somebody else to do the verifying. AD FS uses that term
throughout, which is why lesson 8.4 is about creating a "relying party
trust". It just means "teach my identity provider about an application
that will be trusting it".

## You have already seen this work

Lesson 5.5 had you look at a Kerberos ticket and noted, in passing, that
it's "the same mechanism underneath the fancier web version you'll build in
Module 8". That was a promise, and this is it being kept.

Kerberos already does single sign-on inside your domain. You log in to
DC01 once, and when you connect to a file share on another domain-joined
machine, nobody asks for your password again. Your machine presents a
ticket, the other machine trusts the ticket because it trusts the domain
controller that issued it, and you're in.

That's the same three-party shape:

- **User:** you
- **Identity provider:** the domain controller, which issued the ticket
- **Service provider:** the file share, which trusts the issuer

So why build anything else? Because **Kerberos does not cross the
internet.** It expects domain-joined machines on a network that can reach a
domain controller, and it expects the client to speak a protocol nobody
implemented in a web browser. A web application on another network, or run
by another company, can't use it.

The protocols in the next lesson are what happens when you take Kerberos'
idea and rebuild it for the web: HTTP redirects instead of tickets, signed
tokens instead of encrypted blobs, and no requirement that anything be
domain-joined or even on the same continent.

## What the identity provider is really selling

Three things, and the second is the one people forget.

**Authentication.** Who is this? The IdP checks the password, or the
certificate, or the phone prompt, and vouches for the answer.

**Central control.** Disable an account once and every connected
application loses that user, immediately, without you touching any of them.
This is the reason security teams care. In an organization without
federation, an employee leaving means somebody has to remember all forty
systems. In one with it, disabling the account in the directory is the
whole job.

**A place to enforce policy.** Multi-factor prompts, conditional rules
about where a login can come from, session lifetimes. All of it lives in
one system and applies to every application behind it, rather than being
reimplemented forty times at forty different quality levels.

:::tip[Least privilege]
Federation is the principle from lesson 5.6 applied to secrets. Every
application that stores its own passwords is another copy of your
credentials to be stolen, and another database to be breached.

Federation removes the copies. The application holds no password, only a
short-lived token that says somebody else did the checking. When that token
expires, it's worth nothing.

That's the same instinct as the offline root in lesson 7.2 and the
read-only database in 6.9: hold the least you can get away with, for the
shortest time that works.
:::

## What breaks, and why it's always the same thing

Before you build anything, know the shape of the failure you'll hit,
because you will hit it and the error messages are famously unhelpful.

**Federation is a conversation between three parties who each hold a copy
of the same facts.** The identity provider knows the application's URL. The
application knows the identity provider's URL. Both hold a shared secret or
a certificate. If any of those disagree, even by a trailing slash or
`http` where the other says `https`, the login fails.

The error will not say "your URLs differ by one character". It will say
something like "invalid redirect URI", or nothing at all, and you'll be
staring at two configuration screens trying to spot the difference.

That's the job. When lesson 8.4 or 8.6 fails, the first thing to check is
always whether the two sides agree, character for character, about the
address they're each expecting.

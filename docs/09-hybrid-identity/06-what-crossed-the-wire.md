---
title: "9.6 What actually crossed the wire"
sidebar_position: 6
---

# 9.6 What actually crossed the wire

"We sync our passwords to the cloud" is a sentence that ends meetings badly. It
is also, as usually understood, wrong.

This lesson is about what password hash sync genuinely sends, because it is one
of the few places where the accurate answer is both more reassuring than the
fear and more interesting than the reassurance.

## What Active Directory stores

Your domain controller does not store Sam's password. It stores a **hash** of
it: the output of a one-way function that turns the password into a
fixed-length value you cannot reverse.

That is why an administrator cannot look up a user's password. It genuinely is
not there. It is also why a password reset does not tell you the old one.

The hash Active Directory keeps for this is an old one, and it has known
weaknesses. If an attacker steals it they can often attack it offline, and in
some protocols they can use it directly without ever cracking it. You will meet
that idea properly in Module 14, and its name is worth knowing now:
**pass-the-hash**.

## What gets sent is not that hash

Here is the part people miss.

Entra Connect does not send the hash Active Directory holds. It takes that
hash and **hashes it again**, with a different, deliberately slow algorithm and
a per-user salt, and sends the result.

So what sits in the cloud is a hash of a hash. Three consequences follow, and
they are the reason this design exists:

**The cloud cannot recover the password.** No surprise, that was true of the
original hash too.

**The cloud cannot recover the AD hash either.** This is the one that matters.
Even a full compromise of the cloud copy does not hand an attacker the thing
they would use to pass-the-hash against your on-premises domain. The two
credential stores are cryptographically separated.

**The second hashing is slow on purpose.** The original AD hash is fast to
compute, which is exactly what makes offline attacks against it cheap. The
algorithm used for the cloud copy is designed to be expensive to compute many
times over, which is what makes guessing at scale impractical.

:::tip[Why "slow" is a security feature]
Everywhere else in computing, fast is better. Password hashing is the
exception, and it is worth understanding once properly.

An attacker who steals hashes does not reverse them. They guess: take a
candidate password, hash it, compare, repeat. Their limit is how many guesses
per second the hardware can do.

Make the hash function a thousand times slower and legitimate sign-in is
unaffected, because that path hashes once and nobody notices a few
milliseconds. The attacker's throughput drops by the same factor, and an
attack that took a day now takes three years.

This is why you will see `bcrypt`, `scrypt`, `argon2` and `PBKDF2` recommended
for storing passwords, and why plain SHA-256 is not. Not because SHA-256 is
broken, but because it is *fast*, and fast is the wrong property here.
:::

## What a sign-in actually looks like

Once the hash is in the cloud, Sam signs in to a cloud service and the check
happens **in the cloud**. Her password never travels to your network. Your
domain controller is not consulted and does not need to be reachable.

That is the property from 9.1's table: cloud sign-in survives your building
losing power. It is also why the sign-in works before you have finished your
coffee, rather than making a round trip to a server in a cupboard.

## What this does not protect you from

Honesty matters more than reassurance here, so:

**A compromised sync server is still very bad.** The machine running Entra
Connect reads your entire directory and holds credentials for both sides. It
is a high-value target, and this is the real reason the documentation wants it
on a dedicated, hardened server rather than a domain controller. The hashing
protects the credential in transit and at rest in the cloud; it does not
protect you from someone standing on the bridge.

**A weak password is still weak.** Slow hashing raises the cost of guessing. It
does not save `Password1`, which will be guessed early regardless of how
expensive each guess is.

**The on-premises hash is still there**, with its original weaknesses, on your
domain controllers. Nothing about syncing to the cloud improves that, and
Module 14 will show you why it matters.

## The thing to be able to say

If someone asks whether password hash sync puts your passwords in the cloud,
the accurate answer is:

> No. It sends a salted hash of the on-premises hash, using a deliberately slow
> algorithm. The cloud cannot recover the password, and it cannot recover the
> on-premises hash either, so compromising the cloud copy does not give an
> attacker something they can replay against the domain.

That is a better answer than most people in the room will have, and you now
know why every clause in it is there.

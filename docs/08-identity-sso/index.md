---
title: "Module 8: Identity and single sign-on"
sidebar_position: 0
---

# Module 8: Identity and single sign-on

<div className="stackLine">

AD FS · Keycloak · Gitea

</div>

Module 5 gave your lab a directory that knows who people are. Module 7 gave
it certificates so machines can prove who they are. This module connects
the two to something a user actually touches: signing in to an application
with a domain account, once, and not being asked again.

That's single sign-on, and it is the part of enterprise IT that confuses
the most people. Not because it's hard, but because three different
protocols solve overlapping problems with overlapping vocabulary, and most
explanations start with the vocabulary.

We'll start with the problem instead.

By the end you'll log in to the Git server you built in Module 6 using the
domain account you created in Module 5, through a federation server you
built yourself, over a certificate your own authority issued. Every piece
in that sentence is something you made.

What's in it:

- **8.1** what single sign-on actually is, and the problem it solves
- **8.2** SAML, OAuth 2.0 and OpenID Connect: which is which and when
- **8.3** build ADFS01 and install AD FS (Tier 2)
- **8.4** federate Gitea with AD FS (Tier 2)
- **8.5** Keycloak: the same job, in a container (everyone)
- **8.6** federate Gitea with Keycloak (everyone)
- **8.7** watch a login happen on the wire
- **8.8** gMSA: service accounts that rotate their own passwords
- **8.9** journal entry
- **8.10** checkpoint

## Two paths, and you should read both

This module has a genuine fork, and it's the same shape as Module 7's.

**Tier 2** builds **AD FS** (Active Directory Federation Services) on a
new Windows server. That's what a Windows-shop employer runs, and being
able to say you've configured a relying party trust is worth real money in
an interview.

**Everyone**, including Tier 1, builds **Keycloak** in a container on
UBNT01. It's open source, it needs no extra virtual machine, and it does
the same job with the same protocols. It is also increasingly what
organizations reach for when they aren't already committed to Microsoft.

Lessons 8.5 onward work on any tier. If you're on Tier 1, read 8.3 and 8.4
anyway: the concepts are identical, the vocabulary is the vocabulary
employers use, and you'll meet AD FS eventually whether or not you built
one.

**Tier 2 and up.** ADFS01 wants 4 GB and lives at `10.10.10.40` from the
addressing plan in lesson 4.3. Keycloak runs as a container alongside the
ones already on UBNT01. Budget two evenings, and expect the first
federation to fail once before it works, because they all do and the
reason is almost always a URL that doesn't match by one character.

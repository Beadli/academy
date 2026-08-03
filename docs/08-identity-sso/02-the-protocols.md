---
title: "8.2 SAML, OAuth 2.0 and OpenID Connect"
sidebar_position: 2
---

# 8.2 SAML, OAuth 2.0 and OpenID Connect

Three names, endlessly confused, and the confusion is not your fault. Two
of them do the same job in different decades, and the third does a
different job that everyone describes as if it were the same one.

Here is the whole thing in three sentences, and then we'll earn them.

- **SAML** proves who you are, using XML, mostly to enterprise
  applications.
- **OAuth 2.0** grants access to your stuff without giving away your
  password, and does **not** prove who you are.
- **OpenID Connect** is a thin layer on top of OAuth 2.0 that adds the
  proving-who-you-are part.

## SAML: the enterprise one

**Security Assertion Markup Language**, and the expansion tells you both
what it does and roughly when it was designed. An *assertion* is a signed
statement of fact: this person authenticated, at this time, and here are
some attributes about them. *Markup language* means XML.

It dates from the early 2000s and it shows, but it is deeply entrenched. If
your employer has a payroll system, an HR portal or a VPN with a "sign in
with your company account" button, there's a good chance SAML is behind it.

**The flow, in the only detail you need:** you hit the application, it
redirects your browser to the identity provider with a request, you
authenticate, and the identity provider posts a signed XML assertion back
to the application. The application checks the signature against a
certificate it already trusts, reads your identity out of the XML, and logs
you in.

Everything travels through your browser as redirects and form posts. The
application and the identity provider never talk to each other directly,
which is why SAML works across organizational boundaries where no network
path exists.

## OAuth 2.0: the delegation one, and the one that isn't login

This is where nearly everyone goes wrong, so it's worth being blunt.

**OAuth 2.0 is not an authentication protocol.** It was designed to answer
a different question: how do I let an application do something on my behalf
in another service, without handing it my password?

The classic example is a photo printing site that wants your photos from a
cloud drive. You don't give it your drive password. You're redirected to
the drive, you approve "this app may read your photos", and the app
receives an **access token** that grants exactly that and nothing else.

The token says what the bearer may *do*. It does not reliably say who you
*are*. Applications that tried to use raw OAuth 2.0 as a login mechanism
had to guess at identity from whatever the API happened to return, and
several of them got it wrong in ways that let attackers sign in as other
people.

:::tip[Least privilege]
OAuth's whole design is the principle you've been following since lesson
5.6. The photo site gets read access to photos, not your password, not
your files, not your account. A token scoped to one capability, revocable
on its own, expiring by itself.

Compare it to the alternative it replaced, which was genuinely handing over
your password so an application could log in as you. That is the widest
possible privilege for the narrowest possible need.
:::

## OpenID Connect: OAuth 2.0, plus the missing piece

**OIDC** is the fix. It is a specification layered directly on OAuth 2.0
that adds one thing: alongside the access token, the identity provider
returns an **ID token**, a signed statement about who the user is.

Practically, that means:

- It uses OAuth 2.0's flow, endpoints and vocabulary, so anything that
  speaks OAuth mostly already speaks this
- The ID token is a **JWT** (JSON Web Token), which is signed JSON rather
  than signed XML, so it's smaller and far easier to work with in a browser
- It defines a discovery document at a well-known URL, so an application
  can be pointed at one address and configure itself

That discovery document is why lesson 8.6 is short. You paste one URL into
Gitea and it fetches everything else it needs.

## Which one will you meet?

<div className="labTable">

| | SAML 2.0 | OAuth 2.0 | OIDC |
|---|---|---|---|
| Answers | who are you | what may this app do | who are you |
| Format | signed XML | tokens, format unspecified | signed JSON (JWT) |
| Age | early 2000s | 2012 | 2014 |
| Typical use | enterprise web apps, VPNs | APIs, third-party access | modern web and mobile login |
| Meet it in | legacy and large enterprise | everywhere, under the hood | anything built recently |

</div>

**If you are building something new, use OIDC.** If you are integrating
with something that already exists, you use whatever it supports, and often
that's SAML. Both are fine. Neither is going away soon.

AD FS speaks all three. Keycloak speaks all three. You'll use OIDC in this
module because Gitea supports it cleanly and the discovery document makes
the configuration honest rather than a wall of copied URLs.

## The vocabulary you'll see in the consoles

The same concept has a different name in each protocol and each product,
which is most of why this subject feels harder than it is:

<div className="labTable">

| Concept | SAML | OIDC | AD FS calls it |
|---|---|---|---|
| The application | service provider | client, or relying party | relying party trust |
| The identity system | identity provider | OpenID provider | claims provider |
| The signed proof | assertion | ID token | claim set |
| A fact about the user | attribute | claim | claim |

</div>

Learn the middle column and translate. The concepts underneath are the
three parties from lesson 8.1, and they do not change.

## One thing worth understanding before you build

A token is only worth something because of the **signature**, and a
signature is only worth something because the receiver already trusts the
signer's certificate.

That's why this module comes after Module 7. When you configure Gitea to
trust your identity provider, what you're really doing is telling it which
public key to check signatures against. Get that wrong and every login
fails with an error about an invalid signature, which is the second most
common failure after mismatched URLs.

Certificates aren't a detail of federation. They're the thing that makes it
mean anything at all.

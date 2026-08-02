---
title: "7.1 What a certificate is, and why yours isn't trusted"
sidebar_position: 1
---

# 7.1 What a certificate is, and why yours isn't trusted

Take the warning your browser showed you at `git.lab.internal`
seriously for a minute, because it was telling the truth.

## The problem certificates solve

When your browser connects to a server, it wants two things. It wants
the conversation encrypted, and it wants to know it's talking to the
right machine. Encryption alone is worthless without the second part: an
encrypted conversation with an impostor is still a conversation with an
impostor.

A **certificate** is how a server answers "who are you?". It's a small
file containing a public key, the names the server claims (like
`git.lab.internal`), some dates, and a **signature** from somebody else
vouching for all of it.

That somebody else is a **certificate authority**. The signature is the
entire point: your browser doesn't trust the server, it trusts the CA,
and the CA has signed a statement saying this public key belongs to this
name.

## Why yours failed

Gitea and OPNsense both generated their own certificates and signed them
themselves. A **self-signed** certificate is a stranger vouching for
themselves, and your browser is right to reject it. Not because the
encryption is weaker, but because nobody it trusts has confirmed the
identity.

Your computer ships with a list of certificate authorities it trusts,
put there by your operating system and browser vendors. There are a few
hundred, they're audited, and any certificate signed by one of them is
accepted silently. That's why `https://ubuntu.com` produces no warning
and your own server does.

So you have two options. Convince a public CA to vouch for
`git.lab.internal`, which is impossible because you don't own
`.internal` and nobody can verify you control it. Or become a
certificate authority yourself and tell your own machines to trust you.
Every organization on earth does the second one for internal services,
and that's what this module builds.

## The words you'll meet

**Key pair.** Two mathematically linked keys. The **private key** never
leaves the server and is the actual secret. The **public key** is handed
to anyone. What one encrypts, only the other decrypts, which is what
makes signatures and key exchange possible.

**CSR (certificate signing request).** A server generates its key pair,
then wraps its public key and its claimed names into a request and sends
it to the CA. Notice what doesn't travel: the private key. It never
leaves the machine, and any procedure that emails you a private key is
a procedure to be suspicious of.

**Chain of trust.** Certificates form a chain. Your server's
certificate is signed by an issuing CA, which is signed by a root CA,
which your machines trust directly. A browser walks that chain up until
it reaches something in its trust store. Miss a link and it fails, which
is the single most common certificate problem in the real world:
everyone remembers to install the server certificate and forgets the
intermediate.

**SAN (subject alternative name).** The list of names the certificate is
valid for. This matters more than it sounds: modern browsers ignore the
old "common name" field entirely and check only the SAN list. A
certificate whose common name is right and whose SAN is missing is
rejected, and the error message will not tell you that clearly.

## Look at a real one

You have openssl on UBNT01, and inspecting certificates is a skill you
will use constantly.

```bash
# Fetch a real certificate from a public site and read it. The
# </dev/null stops s_client waiting for you to type.
openssl s_client -connect ubuntu.com:443 -servername ubuntu.com </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

You'll see the subject (who it's for), the issuer (who vouched), and the
validity window. Note how short that window is: public certificates now
last weeks or months rather than years, because short lifetimes limit
the damage when a key leaks. That's why automation matters, and why
lesson 7.6 sets up renewal rather than a yearly reminder.

Now the same for one of your own:

```bash
# Your Gitea certificate, the self-signed one your browser dislikes.
openssl s_client -connect git.lab.internal:443 -servername git.lab.internal </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

Compare the subject and the issuer. On a properly issued certificate
they're different: something vouched for something else. On a
self-signed one they're identical, which is the mathematical form of
"trust me, I'm me."

That's the problem. Lesson 7.4 becomes the somebody else.

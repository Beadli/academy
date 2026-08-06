---
title: "PKI-01 Revoke a certificate and prove it"
sidebar_position: 10
---

# PKI-01: Revoke a certificate and prove it

|  |  |
|---|---|
| **Objective** | Revoke a certificate, publish the updated list, and prove a client refuses it |
| **Success signal** | A verification command that reported success before you revoked, and reports revoked afterwards |
| **Needs** | Module 7, Tier 2 (you need SUBCA01, the issuing CA) |
| **Effort** | An evening |
| **Risk** | Reversible. You revoke a certificate you issued for this drill, not one anything depends on |
| **Check** | Mechanical |

## Why this drill exists

Lesson 7.8 explained revocation. It showed you `certutil -revoke`, it
explained why a revocation list carries its own expiry date, and it had you
diarise the day your offline root's list runs out.

**What it never did was revoke anything.** You have never seen a client refuse
a certificate, which means you have never confirmed that the revocation half
of your PKI works at all. It might not. It very often does not, in real
environments, for reasons nobody notices until an assessment.

7.8 also left a loose end on purpose: publishing the list somewhere clients
can actually fetch it, which it called the fiddliest part of standing up a PKI
and left as an optional exercise. **This is that exercise, done properly and
proved.**

## The thing that makes this harder than it sounds

Revoke a certificate, then test it, and it still works. What went wrong?

**There are three completely different answers, and they look identical.**

1. The certificate is revoked and the client **never checked**. Most clients
   do not check revocation unless told to, and some quietly skip it when the
   list is unreachable. This is called failing open.
2. The certificate is revoked, but you **never republished the list**, so the
   copy clients read does not mention it yet.
3. It genuinely is not revoked, because the revocation did not take.

A drill that stops at "I revoked it and the browser complained" has not
established which of those three you are in. **Telling them apart is the
skill this drill is actually about.**

## Your objective

**Revoke a certificate you issued, publish the list, and produce a
before-and-after pair of verification results from a client.**

Three things must be true when you finish:

1. You have a verification command that said **valid** before you revoked.
2. The same command against the same certificate says **revoked** after.
3. You can explain why a client that still accepts the certificate is not
   evidence that revocation failed.

## How you will know

The pass is a pair of outputs, not a feeling. Something of this shape, run
before and after, against the same file:

```bash
# On UBNT01. The exit code matters as much as the text.
openssl verify -crl_check -CAfile chain.pem -CRLfile crl.pem test.crt
echo "exit=$?"
```

Before revoking, expect `test.crt: OK` and `exit=0`. After revoking **and
republishing**, expect a `certificate revoked` error and a non-zero exit.

<details>
<summary>Nudge, if you do not know where to start</summary>

Do not revoke anything your lab depends on. The first move is to issue a
certificate that exists only to be destroyed, so that a mistake costs you
nothing.

Then work in this order, because each step is meaningless without the one
before it:

1. Capture a **before** result, so you have something to compare against. A
   result with no baseline proves nothing.
2. Revoke.
3. Republish the list. Lesson 7.8 gave you the command and explained why it
   is separate from revoking.
4. Capture the **after** result with the same command.

Step 3 is the one people skip, and skipping it produces exactly the confusing
outcome described at the top of this page.

</details>

<details>
<summary>Fuller hint, if you know the direction but not the tooling</summary>

**On the CA**, lesson 7.8 already gave you both commands: `certutil -revoke`
with a serial number and a reason code, then `certutil -CRL` to publish an
updated list immediately rather than waiting for the CA's own schedule. They
are two separate actions and that separation is the whole trap.

**On the client, the tool has to be one that tells you the truth.** Browsers
are the worst possible test instrument here: they cache aggressively, they
treat internal CAs differently from public ones, and several fail open without
saying so. A green padlock on a revoked certificate tells you nothing about
your PKI.

Use something that reports revocation status explicitly:

- **Linux, on UBNT01:** `openssl verify` with `-crl_check`. Without that flag
  it does not check revocation at all, which is worth demonstrating to
  yourself deliberately.
- **Windows:** `certutil -verify -urlfetch` against the certificate file. The
  `-urlfetch` part is what makes it actually go and download the list named in
  the certificate rather than using a cached copy.

**On finding the serial number:** it is on the certificate itself. You do not
need the CA console for it, though the console lists it too.

</details>

<details>
<summary>Full walkthrough</summary>

### 1. Issue a certificate that exists to be destroyed

Request a certificate from SUBCA01 the same way lesson 7.6 did, with a name
that makes its purpose obvious and that nothing in your lab will ever use:
`revoketest.lab.internal`.

**Do not use your nginx certificate.** You will be revoking this, and a
revoked certificate on a service you use is an outage you gave yourself for
no reason.

Get the issued certificate onto UBNT01 as a file, along with your CA chain.
You produced the chain in Module 7 when you made your machines trust the CA.

### 2. Capture the before result

This is the step that turns the drill into evidence.

```bash
# On UBNT01. Fetch the current revocation list from where your
# certificates say it lives. The URL is in the certificate itself:
# lesson 7.8 showed you how to read the CRL distribution point.
curl -sS -o crl.der http://<your-cdp-url>/subca.crl

# Revocation lists are usually published in DER, a binary format.
# openssl wants PEM, so convert it.
openssl crl -inform DER -in crl.der -outform PEM -out crl.pem
```

```bash
# The baseline. Expect OK.
openssl verify -crl_check -CAfile chain.pem -CRLfile crl.pem revoketest.crt
echo "exit=$?"
```

**Expected output:**

```
revoketest.crt: OK
exit=0
```

**If this fails before you have revoked anything, stop and fix it here.**
Common causes: the chain file is missing the root, or the list you downloaded
has expired, which lesson 7.8 warned makes clients treat it as no list at all.

### 3. Revoke it

On SUBCA01:

```powershell
# The serial number is on the certificate. Reason 4 is "superseded",
# which lesson 7.8 introduced. Reason codes are recorded in the list
# and some clients show them.
certutil -revoke <SerialNumber> 4
```

**Now test again without republishing.** Re-download the list and re-run the
verify from step 2.

**It will still say `OK`.** That is not a failure, it is the second of the
three cases from the top of this page, and meeting it deliberately is worth
more than reading about it. The certificate is revoked in the CA's database
and the list clients read has not been regenerated, so as far as every client
in your lab is concerned nothing has happened.

### 4. Publish the list

```powershell
# On SUBCA01. Generate and publish an updated list now rather than
# waiting for the CA's schedule.
certutil -CRL
```

Then make sure the published copy reached the place clients actually fetch
from. **This is the part 7.8 called the fiddliest bit of standing up a PKI**,
and it is where revocation quietly stops working in real environments: the CA
publishes correctly to a location nothing can reach.

### 5. Capture the after result

Re-download the list, convert it again, and run the identical command:

```bash
openssl verify -crl_check -CAfile chain.pem -CRLfile crl.pem revoketest.crt
echo "exit=$?"
```

**Expected output:**

```
CN = revoketest.lab.internal
error 23 at 0 depth lookup: certificate revoked
error revoketest.crt: verification failed
exit=2
```

That is the drill. A command that said `OK` now says `certificate revoked`,
and the only thing that changed is that you revoked the certificate and
published the fact.

### 6. Watch it fail open, on purpose

One more run, and it is the one that will stay with you. Same revoked
certificate, same published list, one flag removed:

```bash
# No -crl_check this time.
openssl verify -CAfile chain.pem revoketest.crt
echo "exit=$?"
```

**Expected output:**

```
revoketest.crt: OK
exit=0
```

**The revoked certificate passes.** Nothing is broken and nothing is
misconfigured. The client simply was not asked to check revocation, so it
did not, and a certificate you cancelled is accepted as valid.

Sit with that, because it is the actual finding of this drill. Revocation is
not a property of a certificate. It is a claim published by a CA that a client
has to go and look up, and **a client that does not look up finds a revoked
certificate perfectly acceptable.** Most of them do not look up by default.

### 7. Write down which of the three you can now distinguish

Go back to the three cases at the top. You have deliberately produced two of
them: the unpublished list in step 3, and the client that never checked in
step 6. Note in your journal how you would tell them apart from the client
side alone, given that both print `OK`.

</details>

## Going further

- **Publish the list where clients can reach it properly.** 7.8 named the
  target: nginx on UBNT01, serving the CRL over HTTP so every machine can
  fetch it. Do that, then re-run this drill against the real URL rather than a
  file you copied by hand.
- **Break it the other way.** Let a published list expire and watch what your
  clients do. Some fail closed and stop trusting everything, some fail open.
  Knowing which yours does is worth an evening.
- **Revoke something real, then recover.** Revoke your nginx certificate,
  confirm the outage, issue a replacement and restore service, timed. That is
  PKI-02 territory and it is the exercise that turns this from knowledge into
  a runbook.

## What this proves

You can revoke a certificate and demonstrate the effect, which is rarer than
it sounds. Most people who have built a PKI have never once confirmed that
the revocation half of it functions, and a fair number of production
environments publish revocation lists that nothing on the network can reach.

The part worth defending is not the revocation. It is that you can explain why
a client accepting a revoked certificate is usually a client that never asked,
and that you produced that failure on purpose rather than reading about it.

:::note[Write this down before you close the tab]

In your own words, in your journal, while it is fresh:

- The three reasons a revoked certificate can still be accepted, and how you
  would tell them apart from the client side.
- Whether the clients in your lab check revocation by default, and what you
  would have to change to find out for certain.

Six months from now you will remember revoking a certificate, and not that the
same certificate passed verification a minute later.

:::

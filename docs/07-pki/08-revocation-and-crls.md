---
title: "7.8 Revocation, CRLs, and the day it all stops (Tier 2)"
sidebar_position: 8
---

# 7.8 Revocation, CRLs, and the day it all stops (Tier 2)

Certificates expire on their own. The harder question is what happens
when one needs to stop being valid *before* its expiry date: a server is
decommissioned, a laptop is stolen, a private key is copied by someone
who shouldn't have it.

That's **revocation**, and it's the part of PKI most likely to break
your environment, usually at a moment nobody connected to certificates
at all.

## How revocation works

The CA publishes a **certificate revocation list**: a signed file naming
every certificate it has cancelled. Clients fetch it, check whether the
certificate in front of them is on it, and refuse if it is.

Revoking one is straightforward:

```powershell
# Find the certificate's request ID in the CA console, then:
certutil -revoke <SerialNumber> 4      # 4 = superseded

# Publish an updated list immediately, rather than waiting for the
# CA's schedule.
certutil -CRL
```

## The part that bites

Here's the detail that makes this lesson exist: **a CRL has an expiry
date of its own.**

Every list says "this is valid until *date*". That's deliberate, because
otherwise an attacker who blocked CRL downloads could serve an ancient
list forever and hide a revoked certificate. So clients are strict: a
CRL past its date is treated as no CRL at all, and depending on what's
checking, that means certificates start being rejected.

Now put that together with lesson 7.2. **Your root CA is powered off.**
It's the only thing that can sign a new CRL for itself. So its CRL sits
there, silently counting down, on a machine nobody has looked at in a
year.

I have a note in my own lab's documentation that reads, in effect: *root
CA CRL expires on this date, power the machine on and publish a new one
before then*. It's one of a small number of things I've deliberately
diarised years in advance, because the failure mode is genuinely nasty.
Nothing warns you. Everything works fine right up until the date passes,
and then certificate validation starts failing across the environment
for a reason that has nothing to do with any certificate's own expiry
date. People spend a long time looking at the wrong thing.

The lesson generalises beyond PKI: **when you deliberately turn
something off, write down what will eventually need it back on.** The
offline root is a good decision that quietly creates a maintenance
obligation, and good decisions with unrecorded obligations are how
environments decay.

## Do the diary entry now

Your root CA is off. Before you close this module:

```powershell
# On ROOTCA01, powered on one last time. When does the current
# list expire?
certutil -getreg CA\CRLPeriodUnits
certutil -getreg CA\CRLPeriod

# Look at the published list itself.
certutil -dump C:\Windows\System32\CertSrv\CertEnroll\*.crl | Select-String "NextUpdate"
```

Write in `Projects/lab-domain.md`:

- the date that CRL expires
- what to do (power on ROOTCA01, run `certutil -CRL`, copy the new list
  to where clients fetch it, power off)
- why anyone should care

Then power it off again.

## Check the other end too

Revocation only works if clients can actually reach the list. Every
certificate carries the URL where its CRL lives, in a field called the
CRL distribution point.

```powershell
# Look at a certificate your CA issued and find where clients are
# told to fetch the revocation list.
Get-ChildItem Cert:\LocalMachine\My |
    Select-Object -First 1 |
    ForEach-Object { certutil -dump $_.PSPath } |
    Select-String -Pattern "CRL Distribution", "URL"
```

If that URL is unreachable from where your clients live, revocation
checking either fails open (a certificate you revoked keeps working) or
fails closed (everything breaks), depending on the client. Both are bad
in different directions, and both are common findings in real
assessments.

In a production build this is the fiddliest part of standing up a PKI,
and it's usually solved by publishing the CRL to a web server that
everything can reach, which for you would be nginx on UBNT01. Doing that
properly is a good optional exercise, and knowing the problem exists is
the part that matters today.

## What to take from this module

You built a certificate authority, made your machines trust it, issued a
certificate automatically, and turned two browser warnings into
padlocks. On Tier 2 you also built the two-tier structure real
organizations use, issued certificates nobody asked for, and met the
maintenance obligation that comes with an offline root.

The through line: certificates are easy, and certificate *lifecycle* is
where organizations fail. Issuance is a one-time thrill; renewal,
revocation, chain completeness, and CRL freshness are the things that
take environments down. You've now met all four.

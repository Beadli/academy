---
title: "7.2 The offline root (Tier 2)"
sidebar_position: 2
---

# 7.2 The offline root (Tier 2)

:::note[Tier 2 builds this. Tier 1, read it anyway.]
This lesson and the next build two Windows Servers, so they need the
32 GB tier. **Tier 1: your hands-on work starts in lesson 7.4**, and you
will still finish this module with a real certificate authority and real
HTTPS. Read these two lessons regardless. They're short, they're the PKI
most Windows employers actually run, and being able to explain an offline
root in an interview is worth more than most certifications.
:::

Every certificate authority is built around one question: **where does
the private key that signs everything live, and who can reach it?**
Everything else in PKI is procedure hanging off that question, so that's
where this module starts.

## Why the top of the chain goes offline

A root CA's private key is the most valuable secret in an organization's
infrastructure. Anyone holding it can issue a certificate for any name,
and every machine that trusts that root will believe it: your web
servers, your domain controller, your VPN.

If that key is compromised, the fix is not "issue a new certificate."
The fix is: distrust the root everywhere, build a new one, redistribute
it to every machine you own, and reissue every certificate it ever
signed. For an organization with ten thousand endpoints that's a project
measured in months.

So real PKI splits the job across two tiers:

- The **root CA** signs exactly one thing: the issuing CA below it. Then
  it goes offline, powered off, and stays that way. A key that isn't on
  a running machine is dramatically harder to steal.
- The **issuing CA** stays online and signs the thousands of day-to-day
  certificates. If *it* is compromised you revoke it, sign a replacement
  from the root, and your root of trust survives. Painful, but
  survivable.

That's the entire reasoning. Everything below is ceremony built to
protect that arrangement.

## Build ROOTCA01

A Windows Server VM, built exactly as in lesson 5.2, with three
differences that all matter:

- **Name:** `ROOTCA01`. **RAM:** 2 GB. It barely does anything, and it
  won't be running most of the time.
- **Do not join it to the domain.** A domain-joined root is a root that
  can be reached, and attacked, through the domain. Standalone is the
  point.
- **Network: disconnected.** After installation, set its network adapter
  to disconnected in the VM's settings. It never needs a network again,
  and giving it one is how offline roots quietly stop being offline.

Install the certificate authority role:

```powershell
Install-WindowsFeature ADCS-Cert-Authority -IncludeManagementTools

# Standalone, because it isn't in the domain. Root, because nothing
# signs it. Ten years, because replacing a root is expensive enough
# that you want to do it rarely.
Install-AdcsCertificationAuthority `
    -CAType StandaloneRootCA `
    -CACommonName "Lab Root CA" `
    -ValidityPeriod Years -ValidityPeriodUnits 10 `
    -HashAlgorithmName SHA256 `
    -Force
```

Then set how long its revocation lists stay valid. Lesson 7.8 explains
why this number turns out to be one of the most consequential settings
in your whole lab:

```powershell
# 52 weeks, because publishing a new list means physically powering
# this machine on. Write the resulting date in your journal today.
certutil -setreg CA\CRLPeriodUnits 52
certutil -setreg CA\CRLPeriod "Weeks"
Restart-Service certsvc
certutil -CRL
```

## Get the root certificate off it

Two files need to leave this machine, and the private key is not one of
them. Ever.

```powershell
# The root's own certificate and its current revocation list.
dir C:\Windows\System32\CertSrv\CertEnroll\
```

Copy the `.crt` and `.crl` somewhere your other machines can reach: a
shared folder, or an ISO you attach to the other VMs. In a real
organization this is a USB stick, carried by two people, and logged.

Leave the machine powered on for now. Lesson 7.3 needs it to sign one
more thing, and then it goes dark for good.

## What you've just modelled

The awkwardness is the lesson. Copying files by hand between a
disconnected machine and the rest of your lab feels primitive, and it is
supposed to: the inconvenience *is* the security control. Every time
someone decides that carrying files around is too annoying and plugs the
root back into the network, they have traded away the only property that
made it worth building separately.

You'll feel that temptation yourself in the next lesson. Notice it when
it happens.

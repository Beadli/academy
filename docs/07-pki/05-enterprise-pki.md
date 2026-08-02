---
title: "7.5 The enterprise pattern: offline root, issuing CA (Tier 2)"
sidebar_position: 5
---

# 7.5 The enterprise pattern: offline root, issuing CA (Tier 2)

:::note[Tier 2 from here]
The next three lessons build two Windows Servers, so they need the 32 GB
tier. **Tier 1: read them anyway.** Your lab already has working
certificates, so you lose nothing operationally, and this is the PKI
most Windows employers actually run. Being able to explain an offline
root in an interview is worth more than most certifications.
:::

You have a working CA. Now build the shape a real organization uses, and
understand why it's more complicated than what you already have.

## Why two tiers

Your step-ca root signs certificates directly. It's online, in a
container, on a machine that also runs a web server and a Git server.
That's fine for a lab and unacceptable for an organization, for one
reason: **if that root key is compromised, every certificate ever issued
from it is worthless, and fixing it means re-trusting a new root on
every machine you own.** For a company with ten thousand endpoints,
that's a project, not an afternoon.

So real PKI splits the job:

- The **root CA** signs exactly one thing: the issuing CA. Then it goes
  offline, powered off, and stays that way. A key that isn't on a
  running machine is dramatically harder to steal.
- The **issuing CA** is online and signs the thousands of day-to-day
  certificates. If it's compromised you revoke it, issue a new one from
  the root, and your root of trust survives. Painful, but survivable.

That's the whole reasoning. Everything else is procedure.

## Build ROOTCA01

A Windows Server VM, built exactly as in lesson 5.2, with three
differences:

- **Name:** `ROOTCA01`. **RAM:** 2 GB. It barely does anything.
- **Do not join it to the domain.** A domain-joined root is a root that
  can be reached and attacked through the domain. Standalone is the
  point.
- **Network: disconnected.** After installation, set its network adapter
  to disconnected in the VM settings. It never needs a network again,
  and giving it one is how offline roots quietly stop being offline.

Install the CA role:

```powershell
Install-WindowsFeature ADCS-Cert-Authority -IncludeManagementTools

# Standalone (not Enterprise, because it isn't in the domain), Root,
# and a long life because replacing a root is expensive.
Install-AdcsCertificationAuthority `
    -CAType StandaloneRootCA `
    -CACommonName "Lab Root CA" `
    -ValidityPeriod Years -ValidityPeriodUnits 10 `
    -HashAlgorithmName SHA256 `
    -Force
```

Then tell it how long its revocation lists stay valid, which lesson 7.7
will explain the hard way:

```powershell
# 52 weeks, because you must power this machine on to publish a new
# one. Note the date you'd need to do that by, in your journal, now.
certutil -setreg CA\CRLPeriodUnits 52
certutil -setreg CA\CRLPeriod "Weeks"
Restart-Service certsvc
certutil -CRL
```

## Sign the issuing CA

Build a second Windows Server, `SUBCA01`, at `10.10.10.30` per your
addressing plan, **joined to the domain** this time. Install the role:

```powershell
Install-WindowsFeature ADCS-Cert-Authority -IncludeManagementTools

# Enterprise, Subordinate. Enterprise means it integrates with Active
# Directory, which is what makes templates and autoenrollment possible
# in lesson 7.6.
Install-AdcsCertificationAuthority `
    -CAType EnterpriseSubordinateCA `
    -CACommonName "Lab Issuing CA" `
    -HashAlgorithmName SHA256 `
    -Force
```

That leaves a certificate request file on disk, usually on `C:\`. This
is the ceremony, and it's deliberately manual:

1. Copy the `.req` file to ROOTCA01. With no network, that means
   attaching it as a file to the VM, or briefly using a shared folder,
   or in a real organization a USB stick carried by two people.
2. On ROOTCA01, submit and issue it:

   ```powershell
   certreq -submit -config "ROOTCA01\Lab Root CA" C:\SUBCA01.req
   # Note the RequestId it prints, then approve and retrieve:
   certutil -resubmit <RequestId>
   certreq -retrieve <RequestId> C:\SUBCA01.crt
   ```
3. Copy `SUBCA01.crt` back, along with the root certificate and the
   root's CRL.
4. On SUBCA01, install the chain and start the service:

   ```powershell
   certutil -installcert C:\SUBCA01.crt
   Start-Service certsvc
   ```
5. **Power ROOTCA01 off.** That's the point of the whole exercise. Note
   in your journal what would make you turn it back on: signing a
   replacement issuing CA, or publishing a fresh CRL before the current
   one expires.

## You now have two roots, and that's worth addressing

Your lab contains your step-ca root from lesson 7.2 and this new Windows
root. A real organization would have one.

In my own lab they're chained: step-ca's intermediate is signed by the
Windows issuing CA, so everything traces back to a single offline root,
and the Linux services get ACME automation while the Windows machines
get autoenrollment. That's the arrangement worth aiming at eventually.

I deliberately didn't start you there. Chaining step-ca under an
enterprise CA before you'd seen either one work would have meant
building two Windows servers before your browser ever showed a padlock,
and the padlock is what makes the concept stick. If you want to
consolidate now, step-ca can be re-initialised with an intermediate
signed by SUBCA01, and re-issuing your certificates afterwards is the
same `acme.sh` command you already ran.

Leaving both is also a perfectly reasonable lab state. Just know which
root signed what, and write it in your journal, because "why does this
machine trust that certificate" is a question you'll be asked.

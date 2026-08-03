---
title: "7.3 The issuing CA (Tier 2)"
sidebar_position: 3
---

# 7.3 The issuing CA (Tier 2)

The root exists and is about to disappear. Now build the machine that
does the actual work: the CA that signs certificates every day, joined
to your domain so it can integrate with Active Directory.

## Build SUBCA01

A Windows Server VM, as in lesson 5.2, with these settings:

- **Name:** `SUBCA01`, at **`10.10.10.30`**, per the addressing plan
  from lesson 4.3. **RAM:** 3 GB. **Disk:** 60 GB, grow-as-used.
- **Joined to the domain**, unlike the root. This is what makes
  templates and autoenrollment possible in lesson 7.7, and it's the
  difference between an Enterprise CA and a standalone one.

Join it to the domain first, then install the role:

```powershell
# Join the domain. It'll prompt for domain credentials and reboot.
Add-Computer -DomainName lab.internal -Restart

# After the reboot, install the CA role.
Install-WindowsFeature ADCS-Cert-Authority -IncludeManagementTools

# Enterprise, because it's domain-joined and will read templates from
# Active Directory. Subordinate, because ROOTCA01 signs it.
Install-AdcsCertificationAuthority `
    -CAType EnterpriseSubordinateCA `
    -CACommonName "Lab Issuing CA" `
    -HashAlgorithmName SHA256 `
    -Force
```

That command deliberately does **not** finish. It stops and leaves a
certificate request file on disk, usually at `C:\`, because it cannot
issue itself a certificate. Something above it has to agree.

## The signing ceremony

This is the part that only exists because the root is offline, and
walking it manually is the point.

**1. Carry the request to the root.** Copy the `.req` file to ROOTCA01.
With no network, that means attaching it to the VM as a file, or using
an ISO. Notice how inconvenient this is, and notice the temptation to
just reconnect the network for a minute.

**2. On ROOTCA01, submit and issue it:**

```powershell
# Submit the request. It prints a RequestId; note it.
certreq -submit -config "ROOTCA01\Lab Root CA" C:\SUBCA01.req

# A standalone CA holds requests for a human to approve, which is
# exactly what you want for the one certificate that matters most.
certutil -resubmit <RequestId>

# Retrieve the issued certificate.
certreq -retrieve <RequestId> C:\SUBCA01.crt
```

**3. Carry three files back** to SUBCA01: the issued `SUBCA01.crt`, the
root's own certificate, and the root's CRL.

**4. Install the chain and start the service:**

```powershell
certutil -installcert C:\SUBCA01.crt
Start-Service certsvc

# Confirm the CA is running and knows its own chain.
certutil -ping
certutil -dump C:\SUBCA01.crt | Select-String "Issuer", "Subject"
```

The issuer should read `Lab Root CA` and the subject `Lab Issuing CA`.
That one line is the chain of trust from lesson 7.1, now existing as a
fact about your lab.

**5. Power ROOTCA01 off.** That's the whole point of the exercise.

Before you do, write in your journal what would make you turn it back
on. There are exactly two reasons: signing a replacement issuing CA, and
publishing a fresh CRL before the current one expires. Lesson 7.8 is
about the second one, and it is the reason people's PKIs break years
after they were built.

## Publish a subordinate CA template

One more piece of setup, needed by lesson 7.4. Your issuing CA can
currently sign server and user certificates, but not *another CA*. Since
step-ca is going to sit beneath it, it needs to be able to.

On SUBCA01, open **Certification Authority** (`certsrv.msc`), right-click
**Certificate Templates**, choose **New > Certificate Template to
Issue**, and select **Subordinate Certification Authority**.

That's it. You've just granted your issuing CA the ability to delegate,
which is what makes the next lesson possible.

## Where you are

One root, offline. One issuing CA, online and domain-joined, holding a
certificate signed by that root. Every certificate from here on traces
back through that chain to a private key sitting on a powered-off
machine.

That's the structure real organizations run, and you built it by hand,
which means you'll recognise it the next time you see it drawn on a
whiteboard.

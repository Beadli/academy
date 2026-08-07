---
title: "8.3 Build ADFS01 and install AD FS (Tier 2)"
sidebar_position: 3
---

# 8.3 Build ADFS01 and install AD FS (Tier 2)

:::note[Tier 2 builds this. Tier 1, read it anyway.]
This lesson and the next need a seventh virtual machine, so they want the
32 GB tier. **Tier 1: your hands-on federation starts in lesson 8.5**, with
Keycloak in a container, and you will finish this module with a working
single sign-on you built yourself.

Read these two regardless. AD FS is what a Windows-shop employer runs, the
concepts are identical to the ones you'll implement in 8.5, and "I've
configured a relying party trust" is a sentence that lands in an interview.
:::

**Active Directory Federation Services** takes the identity you already
have in the directory and makes it usable by web applications, including
ones on networks your domain controller has never heard of.

It is a role you add to a Windows server, and the install is unusually
sensitive to two things being right beforehand. Get those wrong and the
wizard fails at the last screen with an error about the service account.

## Build the machine

As in lesson 5.2, with these settings:

- **Name:** `ADFS01`, at **`10.10.10.40`**, from the addressing plan in
  lesson 4.3. **RAM:** 4 GB. **Disk:** 60 GB, grow-as-used.
- **Joined to the domain.** AD FS reads the directory directly, so unlike
  the root CA in 7.2 this one belongs inside.
- **DNS pointing at DC01 and DC02**, as lesson 5.8 set up for the
  controllers themselves.

## The two prerequisites that decide whether this works

**First, a certificate.** AD FS is a web service, so it needs a TLS
certificate, and every client must trust the issuer. You have exactly that
from Module 7: an issuing CA whose root is trusted by every machine in the
domain.

Pick the name your users will type. This course uses **`sso.lab.internal`**.
It must not be the machine's own hostname, and here is the reason, because
it catches people: if the federation service name matches the server's
name, AD FS refuses to install on a domain controller and behaves oddly
elsewhere. Use a service name, not a machine name. It also means you can
move or rebuild the server later without every application needing
reconfiguring.

Request the certificate from SUBCA01 the same way lesson 7.7 did, with
`sso.lab.internal` as the subject name.

**Second, a DNS record.** On DC01:

```powershell
# The name clients will use, pointing at ADFS01. Substitute your zone
# if you named the domain differently.
Add-DnsServerResourceRecordA -ZoneName "lab.internal" `
                             -Name "sso" `
                             -IPv4Address "10.10.10.40"
```

Confirm from a different machine before continuing, because the install
will check:

```powershell
Resolve-DnsName sso.lab.internal
```

## Install the role

```powershell
# On ADFS01.
Install-WindowsFeature ADFS-Federation -IncludeManagementTools
```

As in lesson 5.4, installing the role does not configure it. The role puts
the software on disk; the configuration is a separate deliberate act.

## Configure the farm

The term is **farm** even when there's one server, because AD FS is
designed to be load-balanced across several and the tooling never assumed
otherwise.

You'll need the certificate's thumbprint:

```powershell
# Lists certificates in the machine store. Find the one for
# sso.lab.internal and copy its thumbprint.
Get-ChildItem Cert:\LocalMachine\My | Select-Object Subject, Thumbprint, NotAfter
```

Then configure:

```powershell
# -FederationServiceName is the name users type, NOT the server name.
# -FederationServiceDisplayName is what they see on the sign-in page.
# It prompts for domain admin credentials to create the service account.
Install-AdfsFarm `
    -CertificateThumbprint "<paste the thumbprint>" `
    -FederationServiceName "sso.lab.internal" `
    -FederationServiceDisplayName "Beadli Lab" `
    -ServiceAccountCredential (Get-Credential "LAB\svc-adfs")
```

That `-ServiceAccountCredential` expects an account you created earlier.
Lesson 8.8 explains why this particular account is worth replacing with a
managed one, and how. For now, create an ordinary domain user called
`svc-adfs` with a long password, in the `Users` OU from lesson 5.6.

:::warning[This is where it fails, and the error is unhelpful]
The two most common failures both happen at this command and neither says
what's actually wrong.

**"The certificate could not be found"** usually means the thumbprint has
an invisible character in it. Copying from the console sometimes brings a
leading space or a non-printing marker. Retype it or strip it:
`$t = (Get-ChildItem Cert:\LocalMachine\My | Where-Object Subject -like "*sso*").Thumbprint`

**Service account errors** are usually the account not existing, the
password being wrong, or the account lacking the right to log on as a
service. Create it first, test the credentials by logging in with them
once, then run the command.
:::

:::tip[What this is called at work]
AD FS is Microsoft's on-premises identity provider, and the ones you are more
likely to meet are **Okta, Microsoft Entra ID, Ping and Auth0**. They do the
same job: an application trusts them to say who a user is.

**The protocol knowledge transfers completely.** SAML assertions, claims,
relying parties, signing certificates and the trust relationship you are about
to configure are the same everywhere, because they are standards rather than
products.

**What does not transfer is running the thing.** A hosted identity provider
takes away the farm, the patching, the certificate renewals and the database,
and adds things AD FS never had: user provisioning into applications,
conditional access policies, and MFA that somebody else maintains.

Worth knowing honestly: **many organisations are moving off AD FS** towards
Entra ID, so you may meet it mainly in migrations. That is not a reason to
skip it. Understanding what a federation trust actually is makes the hosted
version comprehensible rather than magic, and somebody has to do the
migration.
:::

## Prove it works

AD FS publishes a metadata document describing itself. That document is
how every application you federate will learn what to trust, and fetching
it is the fastest confirmation the service is alive:

```powershell
# Should return 200 and a wall of XML.
Invoke-WebRequest https://sso.lab.internal/FederationMetadata/2007-06/FederationMetadata.xml |
    Select-Object StatusCode
```

Then open **`https://sso.lab.internal/adfs/ls/IdpInitiatedSignon.aspx`** in
a browser on a domain-joined machine.

You should get a sign-in page, with a padlock and no certificate warning,
because the certificate came from a CA your machines already trust. That
padlock is Module 7 paying for itself again.

If the page returns a 404, the IdP-initiated sign-on page is disabled by
default on newer versions. Turn it on for the lab:

```powershell
Set-AdfsProperties -EnableIdpInitiatedSignonPage $true
```

Sign in with the `sokoth` account from lesson 5.6. You should land on a
page saying you are signed in, which is unexciting and is exactly the
point: your directory identity just authenticated a web session.

Next lesson gives that session somewhere to go.

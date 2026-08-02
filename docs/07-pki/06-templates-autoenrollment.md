---
title: "7.6 Templates and autoenrollment (Tier 2)"
sidebar_position: 6
---

# 7.6 Templates and autoenrollment (Tier 2)

An issuing CA that people have to ask is an issuing CA that gets used
twice a year. The reason enterprise PKI is worth building is what this
lesson does: machines request their own certificates, get them approved
automatically, install them, and renew them, with nobody involved.

## Templates: what may be issued, and to whom

A **certificate template** is a form the CA will accept. It defines what
the certificate is for, how long it lasts, whether the private key can
be exported, and, importantly, **who is allowed to request one**.

That last part is the security boundary. A template that lets any
authenticated user request a certificate for any name is one of the
best-known privilege escalation paths in Active Directory, and it is
found in real environments constantly. You'll come back to this in
Module 14 from the other side.

On **SUBCA01**, open **Certification Authority** (`certsrv.msc`), then
**Certificate Templates > Manage**.

1. Find **Web Server**, right-click, **Duplicate Template**.
2. On **General**: name it `Lab Web Server`, and set the validity to
   1 year.
3. On **Security**: this is the part that matters. Add the group that
   should be allowed to enrol, and grant **Read** and **Enrol**. For a
   web server template that's your servers, not your users.
4. On **Request Handling**: leave the private key non-exportable unless
   you have a specific reason. A key that can't be exported can't be
   copied off the machine by someone who gets in.
5. Close the template console, then in the CA console right-click
   **Certificate Templates > New > Certificate Template to Issue** and
   pick your new template.

Creating a template does nothing until you publish it that way, which
catches people out constantly: the template exists, nobody can request
it, and the console gives no hint why.

## Autoenrollment: certificates nobody asks for

Now the automation. You're going to tell every domain machine to request
a certificate for itself.

First, a template they can use. Duplicate **Computer** the same way,
call it `Lab Computer`, and on **Security** grant **Domain Computers**
the **Read**, **Enrol**, and **Autoenrol** permissions. Autoenrol is the
one that makes it automatic. Publish it as above.

Then the policy, on **DC01**, in a GPO linked at the domain root:

**Computer Configuration > Policies > Windows Settings > Security
Settings > Public Key Policies**:

- **Certificate Services Client - Auto-Enrollment**: set to
  **Enabled**, and tick both boxes for renewing expired certificates and
  updating templates.

Then on any domain machine:

```powershell
gpupdate /force

# What certificates does this machine hold now?
Get-ChildItem Cert:\LocalMachine\My | Select-Object Subject, NotAfter, Issuer
```

A certificate appears, issued by your CA, for the machine's own name,
which nobody requested. It will renew itself before expiry, forever.

That is what enterprise PKI is *for*. Every domain-joined machine now
has an identity it can prove cryptographically, which is the foundation
for 802.1X network access, IPsec, and the smart-card logon you'd reach
for next.

## Prove it end to end

```powershell
# The CA's view: every certificate it has issued.
certutil -view -restrict "Disposition=20" -out "RequestID,CommonName,NotAfter" | more
```

Read that list. Those are certificates issued by a CA you built, from
templates you defined, to machines that asked on their own behalf,
validated by a root that is currently powered off in a drawer.

:::tip[In cloud terms]
The same problem exists in cloud environments and is solved with the
same shapes. Managed certificate services issue and renew for you the
way ACME did in lesson 7.4; key vaults hold private keys the way an
offline root holds yours, with access policies instead of a locked room;
and workload identity is the cloud version of the machine certificate
you just autoenrolled, a service proving what it is without a password.
Different consoles, identical questions: who may request, how long does
it live, where is the private key, and what happens when it leaks.
:::

## The dark side, briefly

Because you'll meet it in Module 14: misconfigured templates are one of
the most reliable ways to take over an Active Directory environment. A
template that lets a low-privileged user request a certificate
specifying *someone else's* identity hands the attacker a way to
authenticate as that person, and it doesn't look like an attack in the
logs, because nothing was broken. A certificate was issued, exactly as
configured.

The defence is entirely in the boring parts of this lesson: who has
Enrol rights, whether requesters may supply their own subject names, and
whether anybody reviews the templates. Write down what you configured
today, because in Module 14 you'll audit it and I'd like you to be able
to check your own homework.

---
title: "7.3 Teach your machines to trust it"
sidebar_position: 3
---

# 7.3 Teach your machines to trust it

A certificate authority nobody trusts is a very elaborate way of
producing the same warning you already had. This lesson is the other
half: putting your root certificate into the places your machines look
when they decide what to believe.

Every operating system keeps a **trust store**, a list of root
certificates it accepts. Adding yours is how a private CA becomes real.

## Get the root certificate out

```bash
# Copy it somewhere readable and take a look.
sudo cp ~/docker/step-ca/data/certs/root_ca.crt /tmp/lab-root.crt
sudo chmod a+r /tmp/lab-root.crt
openssl x509 -in /tmp/lab-root.crt -noout -subject -dates -fingerprint -sha256
```

That fingerprint should match the one step-ca printed in lesson 7.2.
Checking it is not ceremony: it's how you'd catch a substituted file,
and the whole point of a root certificate is that you install *the right
one*.

Copy it to your own computer:

```bash
# From YOUR machine, using the SSH config entry from lesson 6.2.
scp ubnt01:/tmp/lab-root.crt .
```

## Trust it on Linux

```bash
# Ubuntu and Debian read every .crt in this directory. The extension
# matters: files not ending .crt are ignored silently.
sudo cp /tmp/lab-root.crt /usr/local/share/ca-certificates/lab-root.crt
sudo update-ca-certificates
```

It'll report how many certificates were added. Test it properly, which
means testing the thing that failed before:

```bash
# Fetch the CA's own health endpoint over TLS. Success means curl
# validated the chain using the root you just installed.
curl https://ca.lab.internal:9000/health
```

If that returns without a certificate error, this machine now trusts
your CA. If it complains, the file is in the wrong place or doesn't end
in `.crt`.

## Trust it on Windows

Certificates for a whole machine go into the **Local Computer** store,
not the user's. Putting it in the wrong one is the classic first
mistake: it appears to work for you and for nobody else.

```powershell
# Run as Administrator. -CertStoreLocation targets the machine's
# Trusted Root store, which every user and service on the box reads.
Import-Certificate -FilePath "C:\Users\you\lab-root.crt" `
                   -CertStoreLocation Cert:\LocalMachine\Root

# Confirm it landed.
Get-ChildItem Cert:\LocalMachine\Root | Where-Object Subject -like "*Lab Internal CA*"
```

:::note[Tier 2: do this properly, with Group Policy]
Copying a root certificate onto machines by hand does not scale, and
this is exactly what your domain is for. On **DC01**, open **Group
Policy Management**, edit a GPO linked at the domain root, and go to
**Computer Configuration > Policies > Windows Settings > Security
Settings > Public Key Policies > Trusted Root Certification
Authorities**. Right-click, **Import**, and select your root
certificate.

Every domain-joined machine now trusts your CA automatically, at its
next policy refresh, including machines that don't exist yet. That is
the actual answer to "how does an organization distribute trust", and
it's one of the clearest demonstrations of why Group Policy earns its
place. Run `gpupdate /force` on DC01 and check the store with the
`Get-ChildItem` command above to prove it arrived.
:::

## Trust it in your browser

Firefox is the exception worth knowing about: it keeps its own trust
store and ignores the operating system's. If your page still warns in
Firefox after everything else works, that's why. **Settings > Privacy &
Security > Certificates > View Certificates > Authorities > Import**,
and tick the option to trust it for websites.

Chrome and Edge use the system store on Windows, so they'll follow the
steps above.

## What you've actually done

You've made a decision that deserves a moment of respect: you've told
your machines that anything this CA signs is legitimate. That's the same
decision your operating system vendor made about the few hundred public
CAs it shipped with, and it carries the same weight. If someone else
gets your CA's private key, every machine you just configured will
believe them.

That's not a reason to avoid running a private CA. Every organization
runs one. It's a reason to know exactly where that key is, which is why
lesson 7.2 made you think about it and why the offline root in lesson
7.5 exists at all.

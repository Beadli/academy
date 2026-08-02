---
title: "7.2 Build a certificate authority you control"
sidebar_position: 2
---

# 7.2 Build a certificate authority you control

You're going to run **step-ca**, an open-source certificate authority
that speaks **ACME**, the same protocol Let's Encrypt uses to issue most
of the public internet's certificates. That matters: the skill you build
here is the one used everywhere, and the automation in lesson 7.4 works
identically against a public CA.

It runs as one container on UBNT01, so this lesson needs no new virtual
machine and every tier can do it.

## Pick a version

step-ca is still on 0.x version numbers, which means minor releases can
change behaviour. Don't take a version number from this page; check
what's current and pin to it deliberately:

```bash
# What tags exist right now? Ignore the sha256-... signature tags.
curl -s "https://hub.docker.com/v2/repositories/smallstep/step-ca/tags?page_size=50" \
  | grep -o '"name":"[^"]*"' | grep -v sha256 | head
```

Use the newest plain version you see (something like `0.30.2`) wherever
this lesson writes `0.30`. Pinning rather than using `latest` means your
CA doesn't change underneath you overnight, which is exactly what you
want from the machine that vouches for everything else.

## Deploy it

```bash
mkdir -p ~/docker/step-ca
cd ~/docker/step-ca
nano compose.yaml
```

```yaml
services:
  step-ca:
    image: smallstep/step-ca:0.30
    container_name: step-ca
    restart: unless-stopped
    volumes:
      - ./data:/home/step
    ports:
      - "127.0.0.1:9000:9000"
    environment:
      # These three initialise the CA on first start. After that they
      # are ignored, because the CA already exists in the volume.
      - DOCKER_STEPCA_INIT_NAME=Lab Internal CA
      - DOCKER_STEPCA_INIT_DNS_NAMES=ca.lab.internal,localhost
      # Turn on the ACME endpoint, which is what lesson 7.4 talks to.
      - DOCKER_STEPCA_INIT_ACME=true
```

Before starting it, give the CA a name in DNS, the same way you did for
Gitea in lesson 6.7. On **DC01**:

```powershell
Add-DnsServerResourceRecordA -Name "ca" `
                            -ZoneName "lab.internal" `
                            -IPv4Address "10.10.10.20"
```

Then start it and watch the first run carefully, because it prints
something you need:

```bash
docker compose up -d
docker compose logs
```

In that output is the CA's **root fingerprint** and an initial admin
password. **Copy both into your journal now.** The fingerprint is how
other machines confirm they're bootstrapping trust from the right CA
rather than something impersonating it, and you'll paste it in lesson
7.3.

## Look at what you built

```bash
# The CA's own root certificate, in the volume you mounted.
sudo cat ~/docker/step-ca/data/certs/root_ca.crt

# Read it with the commands from lesson 7.1. Subject and issuer will
# be identical, because a root CA is by definition self-signed. That
# is fine HERE and was not fine for Gitea: the difference is that you
# are about to deliberately trust this one.
sudo openssl x509 -in ~/docker/step-ca/data/certs/root_ca.crt \
  -noout -subject -issuer -dates
```

Look at the dates. A root CA's certificate lasts years, because
replacing it means re-trusting it everywhere. The certificates it issues
will last days or weeks. That difference in lifetimes is deliberate and
it's the shape of every PKI you'll meet.

## The thing you now own

Two files in that volume matter more than anything else on this machine:
the root certificate and, especially, the root **private key**.

Anyone holding that key can issue a certificate for any name in your
lab, and every machine that trusts your CA will believe it. They could
be `git.lab.internal`. They could be your domain controller. The whole
security of everything you build in the next two modules reduces to
whether that key is under control.

In your lab it lives in a Docker volume, protected by the fact that the
machine is yours. That's an honest lab compromise, and worth naming as
one. In a real organization the equivalent key lives offline, in
hardware built to make extraction difficult, in a safe, with two people
required to touch it. Lesson 7.5 shows you the shape of that with an
offline root, and it's the reason that whole ceremony exists.

:::tip[In GRC language]
You have just become a key custodian, which is a role with control
requirements attached. **SC-12** covers cryptographic key
establishment and management, **SC-17** covers PKI certificates
specifically, and **SC-13** covers using approved cryptography. What an
assessor wants to see is not that a CA exists but that you can say who
can reach the private key, how it's protected, how long certificates
live, and what happens when one is compromised. Write your answers into
your journal as you go; in Module 16 they become part of your system
security plan.
:::

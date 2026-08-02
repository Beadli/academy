---
title: "7.4 A CA that issues certificates automatically"
sidebar_position: 4
---

# 7.4 A CA that issues certificates automatically

**Everyone builds this one.** Tier 1, this is where your hands-on work
begins.

A Windows enterprise CA is excellent at issuing certificates to Windows
machines that ask through Active Directory. It is much less pleasant for
a Linux server that wants a certificate for a web service, renewed
automatically, forever, without a human.

That job belongs to **ACME**, the protocol Let's Encrypt uses to issue
most of the public internet's certificates, and you're going to run a CA
that speaks it: **step-ca**, in one container on UBNT01.

The skill transfers directly. Once you can do this against your own CA,
doing it against a public one is the same commands with a different URL.

## Two paths, one lesson

**Tier 2:** step-ca becomes an *intermediate*, signed by SUBCA01. Your
lab ends up with a single chain of trust: everything traces back to the
offline root you built in 7.2. That's the arrangement my own lab runs,
and it's the right answer.

**Tier 1:** step-ca initialises as its own root, because you have no
enterprise CA above it. You get the same ACME automation and the same
HTTPS; your chain is simply shorter.

Both paths converge at the end of this lesson.

## Give the CA a name

First, DNS, the same way you did for Gitea in lesson 6.7. On **DC01**:

```powershell
Add-DnsServerResourceRecordA -Name "ca" `
                            -ZoneName "lab.internal" `
                            -IPv4Address "10.10.10.20"
```

## Pick a version

step-ca is still on 0.x version numbers, which means minor releases can
change behaviour. Don't take a version number from this page; check
what's current and pin to it deliberately:

```bash
# What tags exist right now? Ignore the sha256-... signature entries.
curl -s "https://hub.docker.com/v2/repositories/smallstep/step-ca/tags?page_size=50" \
  | grep -o '"name":"[^"]*"' | grep -v sha256 | head
```

Use the newest plain version you see wherever this lesson writes `0.30`.
Pinning rather than tracking `latest` means the machine that vouches for
everything else doesn't change underneath you overnight.

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
      # These initialise the CA on first start only. Afterwards they
      # are ignored, because the CA already exists in the volume.
      - DOCKER_STEPCA_INIT_NAME=Lab ACME CA
      - DOCKER_STEPCA_INIT_DNS_NAMES=ca.lab.internal,localhost
      # Turn on the ACME endpoint, which lesson 7.6 talks to.
      - DOCKER_STEPCA_INIT_ACME=true
```

```bash
docker compose up -d
docker compose logs
```

That first run prints two things you need: the CA's **root fingerprint**
and an **initial admin password**. Copy both into your journal now. The
fingerprint is how another machine confirms it's bootstrapping trust
from the right CA rather than something impersonating it.

## Tier 1: you're done building

Your CA is running and is its own root. Skip to "Check your work" below.

## Tier 2: put it under your enterprise root

Right now step-ca has generated its own root, which would leave your lab
with two unrelated chains of trust. Replace its intermediate with one
signed by SUBCA01, so everything traces back to ROOTCA01.

**1. Generate a signing request** for step-ca's intermediate:

```bash
cd ~/docker/step-ca

# Create a new key and a CSR for the intermediate. The name is what
# will appear as the issuer on every certificate step-ca signs.
docker compose exec step-ca step certificate create \
  "Lab ACME Intermediate" /home/step/acme-int.csr /home/step/acme-int.key \
  --csr --profile intermediate-ca --no-password --insecure
```

**2. Have SUBCA01 sign it**, using the Subordinate Certification
Authority template you published in lesson 7.3. Copy the `.csr` to
SUBCA01, then:

```powershell
certreq -submit -attrib "CertificateTemplate:SubCA" C:\acme-int.csr C:\acme-int.crt
```

**3. Install it** back on UBNT01, replacing step-ca's own intermediate,
and give step-ca the enterprise root as its root:

```bash
# Back up what step-ca generated, so a mistake is recoverable.
sudo cp -r ~/docker/step-ca/data/certs ~/docker/step-ca/data/certs.bak

# Replace the intermediate with the one SUBCA01 signed, and the root
# with your enterprise root certificate from lesson 7.2.
sudo cp acme-int.crt   ~/docker/step-ca/data/certs/intermediate_ca.crt
sudo cp acme-int.key   ~/docker/step-ca/data/secrets/intermediate_ca_key
sudo cp lab-root.crt   ~/docker/step-ca/data/certs/root_ca.crt

docker compose restart
docker compose logs --tail 20
```

:::warning[This is the most advanced step in the module]
Exact file names and flags vary between step-ca versions, and this is
the one procedure in Module 7 I'd expect to need adjusting against the
current documentation. Two things make that survivable: you backed up
the original `certs` directory, and step-ca's own docs describe this as
running with an existing PKI.

If you get stuck, **restore the backup and run step-ca standalone as
Tier 1 does.** You'll have two roots in your lab, which is untidy but
entirely functional, and you can come back to this later. Note the
decision in your journal either way, because "which root signed this"
is a question you will be asked.
:::

## Check your work

```bash
# The CA answers.
curl -k https://ca.lab.internal:9000/health

# Look at what it will present as its chain. Tier 2: the issuer
# should be your Lab Issuing CA. Tier 1: it's step-ca's own root.
sudo openssl x509 -in ~/docker/step-ca/data/certs/intermediate_ca.crt \
  -noout -subject -issuer -dates
```

Read those dates. Your root lasts a decade; this intermediate lasts a
few years; the certificates it issues in lesson 7.6 will last days or
weeks. Lifetimes get shorter as you move down the chain, because the
lower you are the easier you are to replace. That pattern holds in every
PKI you will ever meet.

:::tip[In GRC language]
You are now a key custodian, which is a role with control requirements
attached. **SC-12** covers cryptographic key establishment and
management, **SC-17** covers PKI certificates specifically, and
**SC-13** covers using approved cryptography. What an assessor wants is
not proof that a CA exists but answers to: who can reach the private
keys, how are they protected, how long do certificates live, and what
happens when one is compromised.

Write your answers in your journal as you go. On Tier 2 the honest
answer for the root is genuinely good, because it's powered off. For
step-ca's intermediate it's "in a Docker volume on a server I control,"
which is a real lab compromise worth naming rather than hiding. In
Module 16 these answers become part of your system security plan.
:::

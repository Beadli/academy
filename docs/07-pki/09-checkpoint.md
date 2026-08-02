---
title: "7.9 Checkpoint: trusted certificates"
sidebar_position: 9
---

# 7.9 Checkpoint: trusted certificates

On **UBNT01**:

```bash
# The CA is running and healthy, over TLS your system trusts.
docker compose -f ~/docker/step-ca/compose.yaml ps
curl https://ca.lab.internal:9000/health

# The root is in the system trust store.
ls /usr/local/share/ca-certificates/

# Gitea's certificate: who issued it, and for how long.
openssl s_client -connect git.lab.internal:443 -servername git.lab.internal </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates

# The name it is valid for, which is the field browsers check.
openssl s_client -connect git.lab.internal:443 -servername git.lab.internal </dev/null 2>/dev/null \
  | openssl x509 -noout -ext subjectAltName

# Renewal is scheduled, not remembered.
sudo crontab -l | grep acme
```

On **DC01** (Tier 2):

```powershell
# The root is trusted machine-wide, ideally delivered by GPO.
Get-ChildItem Cert:\LocalMachine\Root | Where-Object Subject -like "*Lab*"

# Autoenrollment worked: this machine holds a certificate nobody
# requested by hand.
Get-ChildItem Cert:\LocalMachine\My | Select-Object Subject, Issuer, NotAfter
```

## Pass criteria

Everyone:

- [ ] You can explain what a certificate proves, and why a self-signed
      one fails (lesson 7.1)
- [ ] You can read a certificate with `openssl` and say who the
      subject, issuer, and SAN are (lessons 7.1, 7.4)
- [ ] step-ca runs on UBNT01, and you recorded its root fingerprint
      and admin password in your journal (lesson 7.2)
- [ ] You can say where your CA's root private key lives, and what
      someone could do with it (lesson 7.2)
- [ ] The root certificate is in your Linux trust store and your
      Windows **Local Computer** store, and you know why the user
      store would have been wrong (lesson 7.3)
- [ ] **`https://git.lab.internal` loads with no warning**, in a
      browser, and the issuer is your CA (lesson 7.4)
- [ ] You forced a renewal and watched nginx reload without you
      (lesson 7.4)
- [ ] You can say what a full chain is and why installing only the
      leaf certificate breaks other people's browsers (lesson 7.4)

Tier 2 as well:

- [ ] ROOTCA01 exists, is **not** domain-joined, and is **powered off**
      with its network disconnected (lesson 7.5)
- [ ] SUBCA01 is an Enterprise Subordinate CA whose certificate was
      signed by ROOTCA01, and its service is running (lesson 7.5)
- [ ] You can explain in one breath why the root is offline (lesson 7.5)
- [ ] The root certificate reaches domain machines via Group Policy,
      not by hand (lesson 7.3)
- [ ] A `Lab Computer` template exists, is **published** for issuance,
      and grants Autoenrol to Domain Computers (lesson 7.6)
- [ ] A domain machine holds a certificate it requested automatically
      (lesson 7.6)
- [ ] You can say why a permissive template is a privilege escalation
      path (lesson 7.6)
- [ ] The root CA's CRL expiry date is written in your journal,
      together with what to do before it and why (lesson 7.7)
- [ ] OPNsense serves your certificate, and its warning is gone
      (lesson 7.4)

## Two warnings, collected

Module 4 and Module 6 each ended with a browser complaining at you, and
both are now padlocks. That's the first time in this course that
something you built earlier got materially better because of something
you built later, and it won't be the last: Module 8 uses these
certificates for single sign-on, and Module 12 will use them to protect
the SIEM you're about to stand up.

Next: Module 8, where the identity you built in Module 5 starts logging
people into applications.

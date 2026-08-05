---
title: "14.11 Checkpoint: you attacked it, and you know what noticed"
sidebar_position: 11
---

# 14.11 Checkpoint: you attacked it, and you know what noticed

The test for this module is not how many machines you compromised. It is
whether you can explain how each technique worked, and say honestly what your
own monitoring did about it.

Most of this checkpoint is therefore questions rather than commands, which is
deliberate.

Run what commands there are from KALI01 and DC01.

```bash
# The vulnerable application is gone, from 14.3.
docker ps -a --format '{{.Names}}' | grep dvwa || echo "dvwa removed"

# No credential material left lying around, from 14.6 and 14.8.
ls ~/*.txt ~/*.json 2>/dev/null || echo "clean"
```

```powershell
# The deliberately weak accounts are gone, from 14.5 and 14.6.
# "Cannot find an object" is the passing answer for both.
Get-ADUser -Identity svc-sql
Get-ADUser -Identity svc-backup

# And you can still name who holds replication rights, from 14.8.
(Get-Acl "AD:\DC=lab,DC=internal").Access |
  Where-Object { $_.ObjectType -match "1131f6a[ad]-9c07-11d1-f79f-00c04fc2dcd2" } |
  Select-Object IdentityReference
```

## Pass criteria

**Authorisation and process:**

- [ ] `Projects/lab-rules-of-engagement.md` exists, covers all six questions,
      and has an expiry date rather than "ongoing" (lesson 14.1)
- [ ] You can say why a friendly administrator's verbal "go ahead" is not
      authorisation (lesson 14.1)
- [ ] Snapshots were taken before testing, and recorded (lesson 14.1,
      building on 3.5)
- [ ] You checked which routes reach your lab, including the overlay from
      lesson 4.6, before introducing a vulnerable machine (lesson 14.1)

**Reconnaissance:**

- [ ] You swept the lab network and can account for **every** address that
      answered (lesson 14.2)
- [ ] You compared today's open ports against your Module 4 baseline and can
      explain each difference (lesson 14.2, building on 4.9)
- [ ] You confirmed KALI01 **cannot** reach your home network, and understand
      why that test came before lesson 14.3 rather than after (lesson 14.2,
      building on 4.6)

**Application attacks:**

- [ ] DVWA ran on the lab network only, never proxied or named, and was
      removed afterwards (lesson 14.3)
- [ ] You extracted data with the `' OR '1'='1` injection you were taught in
      lesson 6.9, and can explain what the query became (lesson 14.3)
- [ ] You can explain why SQL injection and XSS are **the same defect**, and
      state that defect in one sentence (lesson 14.3, building on 6.9)
- [ ] You ran the same attack at security level Impossible, and can describe
      what defence in depth feels like from the attacking side (lesson 14.3)
- [ ] You found the container logging gap, and it is in your detection-gap
      list (lesson 14.3)

**Directory attacks:**

- [ ] An unprivileged account enumerated Domain Admins, and you can say why
      that is by design rather than a misconfiguration (lesson 14.4)
- [ ] BloodHound collected and you read the shortest path to Domain Admins,
      even if it was short and boring (lesson 14.4)
- [ ] You checked whether your Module 13 scanning account's privileges held
      up, using the graph (lesson 14.4, building on 13.6)
- [ ] You can explain what a `HasSession` edge is, and why it makes lesson
      5.6's two-account habit a control rather than a preference
      (lesson 14.4)
- [ ] **You Kerberoasted a service account and cracked it offline**, and can
      explain why the domain controller cannot detect the cracking
      (lesson 14.5)
- [ ] You can say why gMSAs from lesson 8.8 defeat this, which is the reason
      they exist (lesson 14.5)
- [ ] **You authenticated with a hash, without ever knowing the password**
      (lesson 14.6)
- [ ] You can explain why NTLM has this property, and why the cloud-side
      rehashing from lesson 9.6 does not fix it (lesson 14.6, building on 9.6)
- [ ] You can name Protected Users and LAPS, and say what each one stops
      (lesson 14.6)

**Certificates and the crown jewels:**

- [ ] You audited your own certificate templates from lesson 7.7 and marked
      your own homework, whatever the answer was (lesson 14.7)
- [ ] You can name the three properties that together make a template
      dangerous (lesson 14.7)
- [ ] You can explain why the resulting attack does not look like an attack
      in the logs, and where you would move the detection instead
      (lesson 14.7)
- [ ] **You ran DCSync and understand that no file was touched and nothing
      was exploited** (lesson 14.8, building on 5.5)
- [ ] You can say what the `krbtgt` hash is, and why its theft is not fixed
      by resetting user passwords (lesson 14.8)
- [ ] You listed who holds replication rights on your domain and can account
      for every entry (lesson 14.8)
- [ ] All credential output was shredded, not merely deleted (lesson 14.8)

**The part that matters most:**

- [ ] **The detection coverage table is complete**, with a row per attack
      (lesson 14.9)
- [ ] You can name the four different meanings of "nothing fired", and give
      an example of each from your own results (lesson 14.9)
- [ ] You determined whether the DCSync event is **collected** before writing
      a rule for it (lesson 14.9, building on 12.4)
- [ ] At least one new detection is written, tested, and in Git
      (lesson 14.9, building on 12.4 and 12.5)
- [ ] **You reassessed the KALI01 exception from lesson 12.6 in light of how
      much of this module ran from that host**, and updated its comment with
      what you learned (lesson 14.9)
- [ ] `Projects/lab-assessment-2026.md` is written, including the "what I
      could not test" section (lesson 14.9)
- [ ] `Projects/lab-attacks.md` written, cleanup checklist ticked, journal
      committed and pushed, Module 14 ticked (lesson 14.10)

All green? Then you have attacked infrastructure you built, defended with
detections you wrote, and produced an honest account of where the gaps were.
Very few people applying for security roles have done that, and fewer still
can talk about the gaps without getting defensive.

Module 15 turns to operating this environment properly: backups that actually
restore, patching on purpose, and the unglamorous habits that separate a lab
from an environment.

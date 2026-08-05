---
title: "14.8 The crown jewels"
sidebar_position: 8
---

# 14.8 The crown jewels

Lesson 5.5 told you where the directory actually lives:

> the directory is a database file called `ntds.dit`, in `C:\Windows\NTDS`,
> and you cannot open or copy it while the service is running. Every password
> hash in your domain lives in that file, which is why domain controllers are
> the crown jewels, why their backups are as sensitive as they are, and why
> **Module 14 spends its time trying to reach exactly this machine**.

It also said: "Don't go poking at it. Do remember it's there."

You may now poke at it, on your own lab, having written the authorisation in
14.1.

## Why this is the end of the assessment

Every technique so far has been about getting *a* credential. This one is
about getting *all* of them.

`ntds.dit` contains the password hash of every account in the domain. Every
user, every service account, every computer, and the `krbtgt` account whose
hash signs every Kerberos ticket in existence. An attacker who reads that
file does not need to attack anything else, ever. They can authenticate as
anybody, using lesson 14.6's technique, indefinitely.

**This is why "we detected them before they reached the domain controller" is
the sentence incident responders want to be able to say**, and why everything
in Module 12 pointed at DC01.

## The thing that makes it worse than a file

You cannot copy `ntds.dit` while the service runs, as lesson 5.5 said. That
sounds like protection. It is not, because **you do not need the file.**

Domain controllers replicate to each other. Lesson 5.9 had you build DC02 and
watch an object created on one appear on the other; that is the Directory
Replication Service doing its job, and part of its job is transferring
password hashes, because a second DC needs them to authenticate people.

So there is a supported, documented protocol whose entire purpose is *"send
me the password hashes"*. An attacker with the right privileges simply asks
DC01 to replicate to them, pretending to be a domain controller. **The
directory complies, because the request is legitimate and correctly
authorised.** No file is touched, no service is stopped, nothing is exploited.

That is **DCSync**, and it is the clearest example in this entire course of a
theme you have now met four times: the attack is the feature.

## Do it

You did a limited version in lesson 14.6 with `-just-dc-user`. This is the
same tool without the restraint.

From KALI01, with Domain Admin credentials:

```bash
# -just-dc asks for the domain's credential material. This is
# the whole domain's hashes. Treat the output accordingly.
impacket-secretsdump lab.internal/sokoth.adm@10.10.10.10 -just-dc
```

**How you know it worked:** a list of every account in your domain, each with
its NTLM hash, ending with the Kerberos keys.

**Look for `krbtgt` in that output.** That account's hash is what signs
Kerberos tickets. An attacker holding it can forge a ticket claiming to be
anybody, in any group, that every machine in the domain will accept, and that
remains valid until the `krbtgt` password is changed **twice**. Recovering
from that is genuinely difficult, which is why it has a name people say with
a slight wince: a **golden ticket**.

I am not going to walk you through forging one. You do not need to perform it
to understand the consequence, and the consequence is the lesson: **there is a
credential in your domain whose theft is not recoverable by resetting user
passwords.**

:::warning[Delete this output]
What is on your screen is every credential in your domain. Do not save it, do
not paste it anywhere, and if you redirected it to a file, `shred -u` that
file now.

If this were a real engagement, handling of this data would be specified in
the rules of engagement you wrote in 14.1, and mishandling it is how testers
end up in court despite having permission to test.
:::

## Getting there without being an admin

You supplied Domain Admin credentials, which rather assumes the conclusion.
The honest question is how an attacker reaches this point, and the answer is
the previous four lessons in sequence:

1. Phish one ordinary user (lesson 14.4's starting position)
2. Map the domain and find a path (14.4)
3. Kerberoast a service account with more rights than it needs (14.5)
4. Or find a certificate template that issues you somebody else's identity
   (14.7)
5. Reuse credentials found on machines along the way (14.6)
6. Reach an account with replication rights, and DCSync (this lesson)

**Notice that step 6 does not require Domain Admin.** It requires the
replication rights specifically, which are held by Domain Admins but can also
be granted directly to accounts, and frequently are, by well-meaning
administrators wiring up a synchronisation tool. Entra Connect from Module 9
is exactly such a tool.

Check your own domain for who holds them:

```powershell
# Who has replication rights on the domain object? These are the
# accounts that can DCSync, whether or not they are admins.
(Get-Acl "AD:\DC=lab,DC=internal").Access |
  Where-Object { $_.ObjectType -match "1131f6a[ad]-9c07-11d1-f79f-00c04fc2dcd2" } |
  Select-Object IdentityReference, ActiveDirectoryRights
```

**How you know it worked:** you get a list of identities. Expect
`Domain Admins`, `Enterprise Admins`, `Administrators`, and the domain
controllers themselves.

**Anything else in that list is worth explaining.** If you installed Entra
Connect in Module 9, its account may well be there, and that is the concrete
version of lesson 9.7's warning about direction of authority: a sync account
with replication rights is a Domain-Admin-equivalent credential living on a
member server.

## What it looked like from the defensive side

**This one is detectable, and the detection is one of the highest-value rules
in any Windows environment.**

Look for **Event ID 4662** on DC01, an operation performed on a directory
object, where the properties include the replication GUIDs above.

The reason it works so well is the reason it is worth understanding rather
than copying: **replication requests should only ever come from domain
controllers.** DC02 asking DC01 to replicate is routine. A workstation, or
any account that is not a DC, making that request has no legitimate
explanation at all.

That gives you something rare in this module: a detection with a genuinely
low false positive rate, because the normal population is small and known.

**Write this rule.** Use lesson 12.4's process, and lesson 12.5's discipline
about testing it before trusting it. Then re-run the DCSync above and confirm
it fires. If your Module 12 stack is collecting 4662 events, this is the most
valuable detection you will build in the entire course.

If it does not fire, work the same triage question as lesson 14.5: **not
collected, or not detected?** 4662 requires object access auditing to be
enabled, which is not on by default, and discovering that is itself a finding
worth writing down.

## And the defence

**Assume the hash file is readable and protect the paths to it.** Tiered
administration from 14.6, so no privileged credential lands on a machine an
attacker can reach. Monitoring for 4662 so the request is noticed. And
reviewing who holds replication rights, which you just did.

**Also: backups.** Lesson 5.5 said domain controller backups "are as
sensitive as they are". Now you know why literally: a DC backup contains
`ntds.dit`, so it contains every credential. A backup system that can restore
a domain controller is a system that can hand somebody the domain. Treat its
access controls as though they were the domain controller's own, because
effectively they are.

## What you take from this

You reached the machine this module has been walking toward since lesson 5.5
promised it would, using a supported replication protocol rather than an
exploit, and you have one detection worth building and one access list worth
reviewing.

Next lesson is the point of all of it: what noticed, and what did not.

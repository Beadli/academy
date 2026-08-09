---
title: "14.6 Pass-the-hash, finally"
sidebar_position: 6
---

# 14.6 Pass-the-hash, finally

Lesson 9.6 introduced this by name and promised you would "meet that idea
properly in Module 14". Here it is properly.

It is worth reading the original passage again, because you now have the
context to hear what it was actually saying:

> The hash Active Directory keeps for this is an old one, and it has known
> weaknesses. If an attacker steals it they can often attack it offline, and
> **in some protocols they can use it directly without ever cracking it.**

That last clause is the whole lesson, and it is the part that surprises
people.

## The idea that breaks people's mental model

Everybody learns early that systems store hashes rather than passwords, and
everybody concludes that a stolen hash is therefore much less useful than a
stolen password, because you would have to crack it first.

**For NTLM authentication in Windows, that conclusion is wrong.**

NTLM stands for NT LAN Manager, and it is the older of the two ways a Windows
network authenticates people. Kerberos from lesson 5.1 is the one your domain
prefers, but NTLM is still enabled underneath it, and Windows falls back to
NTLM whenever Kerberos cannot be used: connecting to a machine by IP address
rather than by name, or to one that was never joined to the domain. That
fallback is what the rest of this lesson depends on.

Here is why. When you authenticate over NTLM, the protocol never uses your
password directly. It uses the hash of your password to answer a challenge.
Your Windows client takes your typed password, hashes it, and uses the hash.

So an attacker holding the hash can skip a step you cannot: they do not need
your password, because **the hash is the thing the protocol actually
consumes**. They feed it in directly and authenticate as you.

The hash is not a scrambled version of the credential. For this protocol,
**the hash is the credential.**

## Why this is worse in Active Directory specifically

Lesson 9.6 made the comparison and it is worth making concrete.

The NTLM hash is **a single unsalted MD4 of the password**. No salt, and one
fast pass. Two consequences follow:

**No salt means identical passwords produce identical hashes**, everywhere,
for every user, on every domain in the world. That is what makes precomputed
lookups viable and why the same hash tells you two accounts share a password.

**One fast hash means cracking is cheap.** Modern hardware tries staggering
numbers of NTLM candidates per second. Compare that to what lesson 9.6 said
Entra Connect does when it syncs: it takes that hash and hashes it again,
with a deliberately slow algorithm and many iterations, precisely because the
original is so weak.

**And now the part that closes lesson 9.6's loop.** It told you the
on-premises hash keeps its original weaknesses no matter what syncs to the
cloud. This is the
demonstration: the slow, salted, cloud-side hash protects the cloud copy. The
on-premises hash on your domain controller is unchanged, still fast, still
unsalted, still directly usable against every machine in your domain. **Cloud
identity did not fix your on-premises credential problem, and the whole
technique below works exactly as well on a synced domain.**

## Get a hash

You need one to pass. In a real intrusion this comes from a compromised
machine's memory or from the directory database, which is lesson 14.8. For
today, take the legitimate route: read it from the directory as an
administrator, so the mechanics are the lesson rather than the theft.

Create a target account on DC01, as your `.adm` account:

```powershell
# A normal member of a group with local admin rights on something.
New-ADUser -Name "svc-backup" `
           -SamAccountName "svc-backup" `
           -UserPrincipalName "svc-backup@lab.internal" `
           -Path "OU=Users,OU=Lab,DC=lab,DC=internal" `
           -AccountPassword (Read-Host -AsSecureString "Password") `
           -Enabled $true
```

Then, from KALI01 with **Domain Admin credentials** (this step is the
privileged one, and 14.8 is where an attacker gets here without them):

```bash
# Ask the directory for account hashes. -just-dc-user limits it
# to the one account, which is the polite version.
impacket-secretsdump lab.internal/sokoth.adm@10.10.10.10 \
  -just-dc-user svc-backup
```

**How you know it worked:** you get a line in the shape
`svc-backup:1234:aad3b435b51404eeaad3b435b51404ee:<32 hex characters>:::`

The second long field is the **LM hash**, and on any modern domain it is
always that same constant, which means "no LM hash stored". The third is the
**NTLM hash**, and that is what you are about to use.

## Use it without cracking it

```bash
# -hashes takes LMHASH:NTHASH. Note there is no password here,
# anywhere, and none is needed.
impacket-smbclient -hashes :<the NTLM hash> lab.internal/svc-backup@10.10.10.20
```

Some tools want the empty LM field before the colon, which is what the bare
`:` is doing.

**How you know it worked:** you get an SMB prompt and can run `shares` to
list the shares on the target.

**You authenticated as an account whose password you do not know and never
learned.** No cracking, no wordlist, no guessing. You had the hash, and the
hash was enough.

That is pass-the-hash, and once you have seen it work the industry's
obsession with credential theft over password cracking makes complete sense.

## What actually defends against this

**Do not let hashes accumulate on machines.** They arrive in memory when
somebody authenticates, so the control is the same one as lesson 14.4: do not
log privileged accounts into ordinary machines. This is lesson 5.6's habit
appearing for the third time in this module, which should tell you something
about how central it is.

**Prefer Kerberos over NTLM, and disable NTLM where you can.** Kerberos does
not have this property in the same way. Real environments struggle to disable
NTLM entirely because old applications depend on it, which is why this
technique still works in 2026, twenty-odd years after it was published.

**Tiered administration.** The industry answer, and the one large
organisations actually implement: domain administrator accounts may only log
into domain controllers, server administrators only into servers, and never
downward. It stops a compromised workstation yielding a hash that opens a
domain controller. It is organisationally painful and it works.

**Protected Users, and LAPS.** The `Protected Users` group prevents members'
credentials being cached in the ways this attack relies on. LAPS gives every
machine a different local administrator password, so one stolen local hash
opens exactly one machine. If you take two names away from this lesson to
look up later, make it those two.

## What it looked like from the defensive side

Look for **Event ID 4624**, a successful logon, on the target machine.

The tell is in the fields rather than the event:

- **Logon Type 3** (network logon), with
- **Authentication Package: NTLM** in an environment where almost everything
  else uses Kerberos, and
- an account logging into a machine it has no business touching.

**That last one is the real signal**, and it is not a signature. It is
knowing what normal looks like. `svc-backup` authenticating to UBNT01 is only
suspicious if you know `svc-backup` never does that.

Search your dashboard for 4624 events with NTLM around your test.

**This is where the module's argument arrives.** Almost every detection worth
having in this module has turned out to be behavioural rather than
signature-based: an account doing something it does not normally do. That is
why the useful defensive skill is knowing your environment, and it is why the
course made you build it before attacking it.

## Clean up

```powershell
Remove-ADUser -Identity svc-backup -Confirm:$false
```

**How you know it worked:** `Get-ADUser -Identity svc-backup` errors saying
it cannot find it.

:::warning[A hash you generated is a real credential]
If you saved that `secretsdump` output to a file, delete it. It is not a
souvenir, it is a working credential for your domain, and it does not stop
working because the exercise ended.

`shred -u <file>` on Linux if you want it gone properly.
:::

## What you take from this

The clause from lesson 9.6 that sounded abstract is now something you have
done: you authenticated with a hash and never knew the password. You can
explain why NTLM has this property, why cloud sync does not fix it, and what
the four real defences are.

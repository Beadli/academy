---
title: "5.10 Checkpoint: a working domain"
sidebar_position: 10
---

# 5.10 Checkpoint: a working domain

Run these on DC01, in an administrator PowerShell window.

```powershell
# Identity and role.
hostname
Get-ADDomain | Select-Object DNSRoot, NetBIOSName, DomainMode
Get-ADDomainController | Select-Object Name, IPv4Address, IsGlobalCatalog

# Network: static address, and DNS pointing at itself.
Get-NetIPConfiguration

# The directory you built.
Get-ADOrganizationalUnit -Filter * | Select-Object Name
Get-ADUser -Filter * -SearchBase "OU=Lab,DC=lab,DC=cyber,DC=internal" |
    Select-Object Name, SamAccountName
Get-ADGroupMember -Identity "Domain Admins" | Select-Object Name

# Authentication is working, and you're holding the proof.
klist

# The policy applied.
gpresult /r /scope:computer

# The evaluation clock (opens a dialog).
slmgr /dli
```

And from KALI01, on the lab network:

```bash
dig @10.10.10.10 -t SRV _ldap._tcp.lab.cyber.internal +short
sudo nmap -Pn 10.10.10.10
```

## Pass criteria

- [ ] DC01 answers to that name, sits at `10.10.10.10` statically, and
      its DNS points at itself (lessons 5.3, 5.5)
- [ ] `Get-ADDomain` reports `lab.cyber.internal` with NetBIOS name
      `LAB` (lesson 5.4)
- [ ] You can explain what the DSRM password is and why it isn't the
      Administrator password (lesson 5.4)
- [ ] You can say why the DNS delegation warning during promotion was
      expected and safe to continue past (lesson 5.4)
- [ ] DNS Manager shows service records under `_tcp` in your zone, and
      you can say what a machine uses them for (lessons 5.1, 5.5)
- [ ] `klist` shows a ticket for `krbtgt`, and you can explain in one
      sentence what a ticket-granting ticket does (lesson 5.5)
- [ ] Your `Lab` OU tree exists, with `Users`, `Servers`, and `Groups`
      inside it (lesson 5.6)
- [ ] You have **two** accounts: an everyday one with no privileges and
      a separate admin one, and only the admin one is in Domain Admins
      (lesson 5.6)
- [ ] You can explain why permissions go to groups rather than to
      people (lesson 5.6)
- [ ] `Lab - Logon Notice` exists, is linked, appears in `gpresult`,
      and you have seen the banner at sign-in (lesson 5.7)
- [ ] From KALI01, the SRV lookup names DC01 and `nmap` shows the
      domain controller's signature ports, and you can name what 88 and
      389 are (lesson 5.8)
- [ ] Tier 2: Kali is back on the NAT segment and can no longer reach
      `10.10.10.10` (lesson 5.8)
- [ ] You know your evaluation's remaining days, and the command that
      extends it (lesson 5.3)
- [ ] `Projects/lab-domain.md` written, journal committed and pushed,
      DC01 snapshotted as `domain-built` (lesson 5.9)

## What you just finished

That's the end of the first arc. Take a second with it: from a bare
laptop you have built a hypervisor, a designed and segmented network, a
domain controller running a directory and DNS, real accounts under
governance, and a policy that configures machines centrally. Plenty of
working sysadmins have never built one from scratch.

Module 6 gives your lab its Linux half: Ubuntu, Docker, and a Git server
of your own that your journal will move to.

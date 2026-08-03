---
title: "5.6 Create users, groups, and an OU structure"
sidebar_position: 6
---

# 5.6 Create users, groups, and an OU structure

An empty directory is a directory nobody can use. Time to put structure
and people in it, and to adopt one habit that separates administrators
who get hired from administrators who get breached.

## Build an OU structure first

Open **Active Directory Users and Computers**, right-click
`lab.internal`, and choose **New > Organizational Unit**. Create
`Lab`. Then right-click `Lab` and create three OUs inside it: `Users`,
`Servers`, and `Groups`.

Or, since you already met PowerShell in Module 2:

```powershell
# The parent OU, directly under the domain. The -Path is written
# in LDAP's own notation: DC=lab,DC=internal is
# lab.internal, read right to left.
New-ADOrganizationalUnit -Name "Lab" -Path "DC=lab,DC=internal"

# Three children inside it.
foreach ($ou in "Users", "Servers", "Groups") {
    New-ADOrganizationalUnit -Name $ou -Path "OU=Lab,DC=lab,DC=internal"
}
```

That `foreach` loop is Module 2 earning its keep: you read it, you know
what it does, and typing one loop beats clicking the same wizard three
times.

**Why not use the built-in `Users` container?** Because you cannot
link a Group Policy to it. Containers and OUs look almost identical in
the console and behave differently in the one way that matters most, and
this catches out a remarkable number of people who wonder why their
policy isn't applying. Put your objects in OUs you created. Always.

## Create your accounts, and the habit

Two accounts, and the reason for two is the actual lesson.

```powershell
# 1. Your everyday user. This is the account you'd read mail and
#    browse the web with. It has no special privileges at all.
New-ADUser -Name "Sam Okoth" `
           -GivenName "Sam" -Surname "Okoth" `
           -SamAccountName "sokoth" `
           -UserPrincipalName "sokoth@lab.internal" `
           -Path "OU=Users,OU=Lab,DC=lab,DC=internal" `
           -AccountPassword (Read-Host -AsSecureString "Password") `
           -Enabled $true

# 2. Your admin account, separate, and obviously named as one.
New-ADUser -Name "Sam Okoth (admin)" `
           -SamAccountName "sokoth.adm" `
           -UserPrincipalName "sokoth.adm@lab.internal" `
           -Path "OU=Users,OU=Lab,DC=lab,DC=internal" `
           -AccountPassword (Read-Host -AsSecureString "Password") `
           -Enabled $true

# Only the second one gets privilege.
Add-ADGroupMember -Identity "Domain Admins" -Members "sokoth.adm"
```

Use your own name rather than Sam's. Note `Read-Host -AsSecureString`:
it prompts you rather than putting a password in the script, which is
lesson 1.6's "keep secrets out of places they'll be read" applied to
code instead of chat windows.

**The habit:** one human, two accounts. The everyday one for everyday
things, the privileged one only when you need it. This exists because of
what an attacker gets when they land on a machine you're logged into. If
that session is a Domain Admin session, they inherit the whole domain
in one step. If it's `sokoth` with no privileges, they've got a foothold
and a lot more work ahead. Module 14 makes this uncomfortably concrete
by doing it to your lab.

And stop using the built-in `Administrator` for daily work from here on.
It's the account every attacker assumes exists, and shared accounts mean
your logs can't tell you *which person* did something.

:::tip[Least privilege]
What you just did has a name, and it's worth knowing because you'll be
asked about it in interviews and you'll meet it in every framework:
**least privilege**. Give an account, a service, or a person the minimum
rights needed to do the job, and nothing more.

Two accounts is least privilege applied to you. Permissions on groups
rather than people, below, is the same idea applied to how rights are
handed out.

The reason it's a principle rather than a rule is that it has no natural
stopping point. There's always a way to hold less privilege, so the
question is never "am I compliant" but "what would this account be able
to do if someone else were driving it?" Ask that and the answer usually
suggests the next change.

Boxes like this one will point out the principle whenever the lab hits it
again. You've already used it once without knowing: back in lesson 2.1
you allowed scripts to run with `-Scope CurrentUser` rather than for the
whole machine. Same instinct, applied to a laptop.
:::

## Groups, and why permissions go to groups

```powershell
# A group, in the OU you made for groups.
New-ADGroup -Name "Lab Engineers" `
            -GroupScope Global -GroupCategory Security `
            -Path "OU=Groups,OU=Lab,DC=lab,DC=internal"

Add-ADGroupMember -Identity "Lab Engineers" -Members "sokoth"

# Read it back.
Get-ADGroupMember -Identity "Lab Engineers"
```

`GroupScope Global` and `GroupCategory Security` are the everyday
defaults: a security group holds permissions, a distribution group is
just a mailing list, and scope decides where the group can be used
across domains. In a single-domain forest like yours, Global is the
right answer nearly always. Module 8 goes deeper when trusts make scope
suddenly matter.

The rule underneath, and it's one of the few genuinely universal rules
in administration: **grant permissions to groups, never to individual
people.** When Sam changes teams you edit one membership. When
permissions were granted to Sam directly, you're hunting through file
shares and applications for years afterwards. Every organization has an
archaeology layer of permissions granted to people who left in 2019.

:::tip[In cloud terms]
These are the objects Module 9 will synchronise. Your `sokoth` becomes a
user in a cloud directory, `Lab Engineers` becomes a cloud group, and
the on-premises directory stays the authority for both. Cloud identity
platforms use the same group-based model for exactly the same reason, so
the habits you're building here transfer directly. What changes is the
console, not the thinking.
:::

## Check your work

```powershell
# Everyone you created, with which OU they landed in.
Get-ADUser -Filter * -SearchBase "OU=Lab,DC=lab,DC=internal" |
    Select-Object Name, SamAccountName, DistinguishedName

# Who holds the keys to the kingdom? Should be Administrator and
# your admin account, and nothing else.
Get-ADGroupMember -Identity "Domain Admins" | Select-Object Name
```

That second command is worth remembering. "Who is in Domain Admins" is
one of the first questions asked in any security assessment, and the
answer in real organizations is depressingly often "more people than
anyone realised."

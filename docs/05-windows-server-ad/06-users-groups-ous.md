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

**How you know it worked:**

```powershell
# Every OU in the domain, with its full path. -Filter * means
# "no filter, show me all of them"; the parameter is not optional,
# which is a quirk of these commands worth meeting once.
Get-ADOrganizationalUnit -Filter * | Select-Object Name, DistinguishedName
```

You are looking for four rows of your own: `Lab`, and then `Users`,
`Servers` and `Groups` whose `DistinguishedName` each contain
`OU=Lab,DC=lab,DC=internal`. That nesting is the thing to check. An OU
called `Users` sitting directly under the domain rather than inside `Lab`
means the `-Path` was wrong, and every command later in this lesson that
targets `OU=Users,OU=Lab` will fail to find it.

**If you see `Domain Controllers` in that list and did not create it**,
nothing is wrong. Active Directory builds that one itself during
promotion.

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

**Expect to be stopped at least once here.** Active Directory enforces a
password policy by default, and `New-ADUser` rejects anything that fails it
with *"The password does not meet the length, complexity, or history
requirement for the domain"*. The default asks for at least seven
characters and three of the four categories: uppercase, lowercase, digits,
symbols. This is not you doing it wrong. Pick something that satisfies it
and move on; you will meet this policy properly in lesson 5.7.

Also note that when the account is rejected, **nothing is created**, so
just run that block again. There is no half-made user to clean up.

**How you know it worked:**

```powershell
# 1. Both accounts exist, and they are in the OU you meant.
Get-ADUser -Filter * -SearchBase "OU=Users,OU=Lab,DC=lab,DC=internal" |
    Select-Object Name, SamAccountName, Enabled

# 2. The privilege landed on the right one, and only that one.
#    This is the check that matters most in this lesson.
Get-ADGroupMember -Identity "Domain Admins" | Select-Object Name
```

The first should list both of your accounts with `Enabled` showing `True`.
The second should list `Administrator` (built in, expected) and your `.adm`
account, and **not** your everyday account. If your everyday account appears
in that second list, the whole point of the next paragraph is undone;
remove it with
`Remove-ADGroupMember -Identity "Domain Admins" -Members "sokoth"`.


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
across domains.

There are three scopes, and the difference only bites once a forest holds
more than one domain: **Domain Local** groups can hold members from
anywhere but only grant access inside their own domain, **Global** groups
can hold members only from their own domain but grant access anywhere in
the forest, and **Universal** groups do both at the cost of replicating
their membership forest-wide.

**In a single-domain forest like yours, Global is the right answer nearly
always**, and this course never builds a second domain, so you will not
feel the difference here. Say so plainly rather than pretending: the
scenario where scope genuinely matters is a multi-domain or multi-forest
estate, and if you join one you'll meet the rule that governs it, which
administrators shorten to **AGDLP**. Accounts go into Global groups,
Global groups go into Domain Local groups, and permissions are granted to
the Domain Local group. It sounds fussy until an acquisition doubles your
forest count.

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

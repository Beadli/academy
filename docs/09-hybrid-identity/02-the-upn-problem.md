---
title: "9.2 The UPN problem, and why lab.internal will never be enough"
sidebar_position: 2
---

# 9.2 The UPN problem, and why `lab.internal` will never be enough

**No cloud account needed for this lesson.** This is work on your own domain,
and it is the single most common thing that blocks a real hybrid rollout.

In Module 5 you created Sam Okoth with this:

```powershell
New-ADUser -Name "Sam Okoth" `
           -SamAccountName "sokoth" `
           -UserPrincipalName "sokoth@lab.internal"
```

That `sokoth@lab.internal` is her **User Principal Name**, or UPN. It is the
modern way to identify a user in Active Directory: it looks like an email
address, and it is what she would type into a sign-in box.

It is also about to become a problem.

## Microsoft will not accept a domain you cannot prove you own

When you sync to a cloud directory, users arrive carrying their UPNs. Microsoft
will only accept a UPN whose domain part you have **verified**, and verifying a
domain means adding a DNS record to it that only its owner could add.

You cannot do that for `lab.internal`. Nobody can. It is not a domain anyone
owns, it exists only inside your lab, and there is no public DNS zone to add a
record to.

So Microsoft does something you should see coming rather than discover: it
accepts the user anyway, and **replaces the unverifiable UPN with one of its
own**, in the form `sokoth@yourtenant.onmicrosoft.com`.

The user syncs. Nothing errors. And Sam now signs in to the cloud with an
identity that has nothing to do with the one she uses at her desk.

:::warning[This is not a lab quirk, it is the classic migration wall]
For fifteen years the standard advice for naming an Active Directory domain
was to use something non-routable, and a whole generation of domains got names
like `contoso.local`, `company.internal`, or `ad.corp`.

Then those organisations moved to Microsoft 365 and hit exactly this. Their
users' UPNs were unverifiable, so everybody would have signed in as
`someone@contoso.onmicrosoft.com`, which is unusable in front of real people.

Fixing it is the work below. Every consultant who did Office 365 migrations
has done this dozens of times, and being able to say you understand why it is
necessary is a genuinely marketable thing.
:::

## The fix: give the domain a second name for sign-in

You do **not** rename your domain. Renaming an AD domain is possible and it is
one of the most disruptive operations available to you; nobody does it for
this.

Instead you add an **alternative UPN suffix**. Active Directory lets a domain
offer more than one suffix for user sign-in names, so `lab.internal` can keep
its own name while offering `beadli-lab.com` as a suffix users' UPNs can use.

Two things become true at once: the domain is still `lab.internal` for
everything internal, and Sam can have a UPN in a domain you can actually prove
you own.

### Pick the suffix

Use a real domain you control, if you have one. A domain costs a few pounds a
year and is a reasonable thing to own anyway.

If you do not have one and do not want one, use the example below and follow
along conceptually. You will not be able to verify it, so you will end up on
`onmicrosoft.com` in the cloud, and knowing *why* is most of the value.

For the rest of this module, the examples use `beadli-lab.com`. Substitute
your own domain wherever it appears.

### Add the suffix to the forest

On DC01, open **Active Directory Domains and Trusts** (`domain.msc`, opened
the same way you opened `dsa.msc` in Module 5). Right-click **Active Directory
Domains and Trusts** at the very top of the left pane, not the domain beneath
it, and choose **Properties**. Add your suffix to the list and apply.

Right-clicking the wrong node is the usual stumble here: the domain node's
properties has no UPN suffix tab at all, and people conclude the feature is
missing.

Or do it in PowerShell, which is less ambiguous:

```powershell
# Add an alternative UPN suffix to the forest.
Get-ADForest | Set-ADForest -UPNSuffixes @{Add="beadli-lab.com"}

# Confirm it took. Your new suffix should be listed.
(Get-ADForest).UPNSuffixes
```

### Repoint your users

Adding the suffix makes it *available*. It does not move anyone.

```powershell
# One user, so you can see what changes.
Set-ADUser -Identity sokoth -UserPrincipalName "sokoth@beadli-lab.com"

# Check.
Get-ADUser sokoth -Properties UserPrincipalName |
  Select-Object SamAccountName, UserPrincipalName
```

For a handful of users, do them in a loop. In a real migration this is the
same shape, over thousands, and it is where the care goes:

```powershell
# Everyone in the Staff OU from lesson 5.6. Read it before running it:
# it rewrites the sign-in name of every user it matches.
Get-ADUser -Filter * -SearchBase "OU=Staff,DC=lab,DC=internal" |
  ForEach-Object {
    $new = "$($_.SamAccountName)@beadli-lab.com"
    Set-ADUser -Identity $_ -UserPrincipalName $new
    Write-Host "$($_.SamAccountName) -> $new"
  }
```

:::tip[Adjust the SearchBase to your own OU]
`OU=Staff,DC=lab,DC=internal` assumes the structure from lesson 5.6. If you
named your OU differently, `Get-ADOrganizationalUnit -Filter *` lists what you
actually have. Running the loop against a SearchBase that does not exist
errors harmlessly, which is the good outcome; running it against the wrong OU
does not.
:::

### What this does not break

Worth stating, because it looks alarming to change everyone's sign-in name.

Their **SamAccountName** is untouched. `LAB\sokoth` still works, and that is
what the older sign-in prompts and most internal systems actually use. Their
password is untouched. Their group memberships, permissions and profile are
untouched. Their SID, the security identifier that is what Windows genuinely
uses for access control underneath every name you see, is untouched.

What changes is the name they type in a modern sign-in box, and the name that
will cross into the cloud.

## Prove it

```powershell
# The forest now offers the suffix.
(Get-ADForest).UPNSuffixes

# And your users carry it.
Get-ADUser -Filter * -Properties UserPrincipalName |
  Select-Object SamAccountName, UserPrincipalName | Format-Table -AutoSize
```

Every user you intend to sync should show a UPN in a domain you can prove you
own. Any that still say `@lab.internal` will arrive in the cloud as
`onmicrosoft.com`, and you will know exactly why.

That is the wall dealt with before you hit it, which is the whole point of
doing this lesson before you have a tenant to hit it against.

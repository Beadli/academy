---
title: "9.7 Disable an account and follow it"
sidebar_position: 7
---

# 9.7 Disable an account and follow it

Lesson 9.1 claimed your Active Directory is authoritative and the cloud is a
copy. This lesson makes you prove it, in the two directions, and the second
one is the interesting one.

This is also the single most operationally important thing in the module.
Offboarding is the identity task organisations get wrong most often, and it is
the one auditors ask about first.

## Direction one: disable on-premises

On DC01:

```powershell
# Disable the account, the way you would when somebody leaves.
Disable-ADAccount -Identity sokoth

# Confirm.
Get-ADUser sokoth -Properties Enabled | Select-Object SamAccountName, Enabled

# Do not wait thirty minutes.
Start-ADSyncSyncCycle -PolicyType Delta
```

Give it a minute, then look at Sam in the cloud portal. Her sign-in is blocked
there too.

**Nobody touched the cloud.** One command on a domain controller, and access to
every cloud service backed by that directory stopped. That is the entire
argument for hybrid identity, demonstrated in about ninety seconds.

Sit with it for a moment, because the alternative is what most organisations
had before: a list of systems, a person working through it, and an account
somewhere on that list still live six months later.

## Direction two: try it the other way

Now the instructive failure. In the cloud portal, find Sam and try to change
something that came from your directory. Her job title, or her name.

The portal will not let you. The field is not editable, and the reason given is
that the object is mastered on-premises.

That is not a bug and it is not a licensing limit. It is the direction of
authority made concrete: an attribute has one owner, and for synced users that
owner is your domain. If the cloud let you edit it, the next sync would
overwrite your change anyway, so it declines to let you waste the effort.

:::warning[This surprises people at exactly the wrong moment]
The pattern is: someone leaves, an administrator opens the cloud portal
because that is where they live day to day, and cannot delete or fully disable
the account. In the pressure of the moment this reads as broken tooling.

It is the system working. The account is a copy, and copies do not get to
decide. **Go to the domain controller.**

Knowing this in advance turns a confusing ten minutes into a five-second
diagnosis, and it is the sort of thing that gets you a reputation for being
calm in incidents.
:::

## Put her back

```powershell
Enable-ADAccount -Identity sokoth
Start-ADSyncSyncCycle -PolicyType Delta
```

Confirm she is enabled again in both places. Leaving your own lab account
disabled is a fine way to confuse yourself in Module 14.

## What happens if you delete instead

Do not do this to your only user, but know the shape of it.

Deleting a synced user on-premises removes them from the cloud on the next
sync, into a recycle bin that holds them for a limited window before they are
gone permanently. Restoring within that window brings back the same object,
with its identity intact.

That window matters more than it sounds. Restoring the *same* object returns
their access to files and applications, because those permissions point at an
identifier rather than a name. Recreating an account with the same name after
the window closes produces a **different** object with a different identifier,
which looks identical to a human and has none of the same access.

That is the same lesson as the **security identifier (SID)** behind every
Windows account, which Module 5 met when it explained why domain controllers
hand out identifiers from a pool. Windows decides access by SID rather than
by name, which is exactly why a recreated account inherits none of the old
one's access. Same idea, different product.
Once you have seen it twice you will start expecting it everywhere, which is
what learning infrastructure actually feels like.

## The operational summary

<div className="labTable">

| Action | Where you do it | What happens in the cloud |
|---|---|---|
| Create a user | On-premises | Appears at the next sync |
| Change a synced attribute | On-premises | Follows at the next sync |
| Disable an account | On-premises | Sign-in blocked at the next sync |
| Change a synced attribute | Cloud | Refused |
| Assign a cloud licence | Cloud | Cloud-only, does not come back down |

</div>

That last row is worth noticing. **The sync is one way for identity, but the
cloud has its own attributes that never travel back**: licences, cloud-only
group memberships, service settings. So the cloud is a copy, and also
genuinely has state of its own.

If you can hold both those ideas at once, you understand hybrid identity
better than the average person administering it.

---
title: "5.7 Write your first Group Policy"
sidebar_position: 7
---

# 5.7 Write your first Group Policy

Group Policy is how one administrator configures thousands of machines
without touching any of them. You define a setting once, attach it to
part of the directory, and every machine and user underneath picks it up
and keeps picking it up, forever, including machines built next year.

It's also the single most useful thing on a Windows administrator's CV,
and today you'll write one that you can see working.

## The model, in four sentences

A **Group Policy Object (GPO)** is a bundle of settings. You **link** it
to a site, a domain, or an OU, and it applies to everything underneath
that link. Machines re-check for policy every 90 minutes or so, and at
boot and login. Where several policies collide, the one linked closest
to the object wins.

That's genuinely most of it. The complexity in real environments comes
from having four hundred GPOs and no documentation, which is a people
problem wearing a technology costume.

## Write one: a system use notice

You're going to configure the message that appears before anyone logs
in. It's a good first policy for three reasons: it's harmless, you can
*see* it working within minutes, and it's a real control that real
auditors really ask about.

Open **Group Policy Management** (`gpmc.msc`).

1. Expand **Forest > Domains > lab.internal**.
2. Right-click the domain name and choose **Create a GPO in this domain,
   and Link it here**. Name it `Lab - Logon Notice`.

   Linking at the domain root is deliberate here rather than sloppy: a
   legal notice is one of the few things that genuinely should apply to
   every machine in the organization, including the domain controllers.
   Most policies you write later should attach to a specific OU
   instead, which is what your `Lab` OU structure from 5.6 is for.
3. Right-click your new GPO and choose **Edit**. The Group Policy
   Management Editor opens.
4. Navigate to **Computer Configuration > Policies > Windows Settings >
   Security Settings > Local Policies > Security Options**.
5. Find **Interactive logon: Message title for users attempting to log
   on**. Double-click, tick **Define this policy setting**, and enter
   something like `Authorised use only`.
6. Find **Interactive logon: Message text for users attempting to log
   on**, define it, and write a sentence: `This system is for
   authorised users. Activity may be monitored.`
7. Close the editor. There's no save button; policy edits are written as
   you make them, which surprises everyone once.

## Make it apply, and prove it did

Policy refreshes on its own schedule, and waiting is for people without
a command line:

```powershell
# Fetch and apply policy now. /force reapplies everything rather
# than only what changed.
gpupdate /force
```

Then ask the machine what it thinks applies to it:

```powershell
# A summary of which GPOs applied to this computer and to you.
# Look for "Lab - Logon Notice" under Computer Settings.
gpresult /r /scope:computer
```

Now sign out. Before the login screen appears you should see your
notice, with your title and your text, waiting for someone to
acknowledge it.

You configured a machine by editing a directory object. Nothing was
installed, nothing was copied, and the same edit would have hit ten
thousand machines identically.

:::tip[In GRC language]
That notice has a control number. It's **AC-8, System Use
Notification** in NIST 800-53, and it's a common audit finding precisely
because it's easy to skip. Notice what you can now produce as evidence:
the policy object, where it's linked, and `gpresult` output proving it
reached a machine. Auditors ask for exactly that trio, and "we told
everyone to configure it" is not one of them. In Module 16 you'll
assess this control on this lab, using this evidence.
:::

## When a policy doesn't apply

It will happen, so here's the order to check, which is most of what
troubleshooting Group Policy consists of:

- **Is it linked where you think?** The link, not the GPO, decides who
  gets it. A GPO with no link does nothing at all.
- **Is the object inside that scope?** Remember lesson 5.6: your domain
  controller lives in the `Domain Controllers` OU, not in your `Lab` OU.
  A policy linked to `Lab` will never touch it.
- **Computer setting or user setting?** Computer settings apply to
  machines and user settings to accounts. Putting one where the other
  belongs is the most common mistake by a distance.
- **Has it refreshed?** `gpupdate /force`, then `gpresult /r` to see
  what the machine actually believes.

Work that list top to bottom and you'll find it. It's the same
discipline as the network ladder in lesson 4.4: check each layer in
order rather than guessing which one is broken.

## One honest caveat about what you just proved

You verified this on a domain controller, because at this point in the
course it's the only Windows machine you have. A domain controller is
close to the worst machine in the estate to test a policy against: it
sits in its own OU, with its own policies, and it's the one machine
you'd never deploy a workstation setting to.

In production you verify on a machine that represents the estate, and
you check that policies you scoped *out* stayed out. That second half is
the one almost nobody practises, and it's how a policy linked one level
too high goes unnoticed.

Drill [DEF-11](/drills/def-11-prove-policy-applied) does it properly once
you have somewhere to do it.

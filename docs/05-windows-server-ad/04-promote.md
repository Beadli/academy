---
title: "5.4 Promote DC01 to a domain controller"
sidebar_position: 4
---

# 5.4 Promote DC01 to a domain controller

Now the moment. Two steps: install the role, then run the wizard that
turns the server into the first domain controller of a brand new forest.

You'll do this in the graphical tools rather than by script, deliberately.
The wizard's screens are the concepts, and reading them once is worth
more than pasting a one-liner you can't explain. The PowerShell
equivalent is at the bottom for when you've done it and want to see what
the same thing looks like as code.

## Install the role

In **Server Manager**: **Manage > Add Roles and Features**.

1. Next through the start screen. Installation type: **Role-based or
   feature-based**.
2. Server selection: your machine, already highlighted.
3. Server roles: tick **Active Directory Domain Services**. A box pops
   up offering to add the management tools with it; accept, you want
   them.
4. Next through features, next through the AD DS information screen,
   then **Install**. It takes a couple of minutes.

Installing the role does not make it a domain controller. It puts the
software on disk. The promotion is a separate, deliberate act, which is
a distinction worth noticing because it's the same everywhere in Windows
Server: install the role, then configure it.

## Promote it

When the install finishes, Server Manager shows a notification flag with
**Promote this server to a domain controller**. Click it. If you closed
it, the same link lives under the yellow warning triangle at the top of
Server Manager.

Now read each screen, because each one is a decision:

**Deployment configuration.** Choose **Add a new forest**. The other
options join an existing domain, and there isn't one. Root domain name:
`lab.internal`, exactly, from your course conventions in lesson
0.4.

**Domain controller options.** Leave the forest and domain functional
levels at their defaults. These set the minimum Windows version a future
domain controller can run, and defaults are right for a new build.
**DNS server** is ticked and effectively mandatory here, which is
lesson 5.1's point made concrete. Then it asks for a **Directory
Services Restore Mode password**, and this is where people get caught:
it is **not** your Administrator password, it's a separate recovery
password used when starting the directory in repair mode. Set it,
write it in your journal clearly labelled `DSRM`, and hope you never
need it.

**DNS options.** You'll see a warning that a delegation for this DNS
server could not be created. **This is expected. Continue.** It's
telling you there's no parent DNS zone anywhere that knows about
`lab.internal`, which is entirely correct, because you invented
this domain and nothing outside your lab has heard of it. The wizard
would say the same thing in most real greenfield builds.

**Additional options.** It proposes a NetBIOS name, derived from your
domain: `LAB`. Accept it. NetBIOS names are the short, old-style form
of the domain, and you'll see this one every time you log in as
`LAB\Administrator`.

**Paths.** Defaults. In production these sometimes go on separate disks
for performance; in your lab they don't need to.

**Review, then Prerequisites Check.** Read the results. Warnings here
are normal, particularly ones about DNS delegation and about security
settings for older protocols. Errors are not, and would stop you. When
it says the checks passed, click **Install**.

The server promotes itself and reboots on its own.

## Log in to your domain

When it comes back, the login screen has changed: it now offers
`LAB\Administrator` rather than a local account. That's the first
visible proof that this machine is no longer a standalone server. Log
in with the Administrator password you set at install.

You are now signed in to a domain, on the domain controller that
authenticated you.

## The same thing as code

Now that you've seen what each screen asked, here's the whole promotion
as three commands. You'd use this on the tenth domain controller, or in
a build pipeline, or in Module 10 when Ansible does it for you:

```powershell
# 1. Install the role and its management tools.
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools

# 2. Promote to the first DC of a new forest. -InstallDns matches the
#    ticked box in the wizard; the NetBIOS name matches what it
#    proposed. It will prompt for the DSRM password.
Install-ADDSForest -DomainName "lab.internal" `
                   -DomainNetbiosName "LAB" `
                   -InstallDns

# 3. It reboots by itself, as the wizard did.
```

Compare those eight lines against the eight screens you just clicked
through. Nothing is hidden in either version, and that's the point: the
wizard taught you what the parameters mean, so now the code is readable
instead of magic. That relationship, GUI to learn and script to repeat,
is the shape of the rest of this course.

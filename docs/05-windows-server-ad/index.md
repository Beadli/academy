---
title: "Module 5: Windows Server and Active Directory"
sidebar_position: 0
---

# Module 5: Windows Server and Active Directory

This is the one. Everything so far has been groundwork; today
`lab.internal` stops being a string in a planning document and
becomes a real domain, with a real directory, holding real accounts that
really authenticate.

It matters more than any other single module because of how much rests
on it. Active Directory is still the identity backbone of the large
majority of organizations you could go work for, the thing their email,
file shares, VPN, and applications all ultimately ask "is this person
who they say they are?" Module 7's certificate authority issues
certificates to its members. Module 8's single sign-on federates its
identities. Module 9 syncs it to the cloud. Module 14 attacks it. All of
that starts here, with one server and one wizard.

What's in it:

- **5.1** what Active Directory is, and why DNS is inseparable from it
- **5.2** build DC01 and install Windows Server
- **5.3** before you promote: name, address, and that 180-day clock
- **5.4** promote DC01 to a domain controller
- **5.5** what just happened: the database, DNS, and Kerberos
- **5.6** create users, groups, and an OU structure
- **5.7** write your first Group Policy
- **5.8** add a second domain controller
- **5.9** watch replication work, then break it on purpose
- **5.10** FSMO roles, and a script to move them
- **5.11** see your domain from the network
- **5.12** journal entry
- **5.13** checkpoint

**Tier 1 and up.** DC01 wants 3 GB of RAM and stays running for the rest
of the course. DC02 wants another 3 GB but is only powered on for lessons
5.8 to 5.10, so it costs you nothing the rest of the time. Budget three
evenings: one to install and promote DC01, one for the directory work in
5.6 and 5.7, and one for the second controller and what it teaches. Don't
rush the promotion; read what each screen is asking.

Lessons 5.8 to 5.10 are the part most beginner AD material skips
entirely, and they're the difference between "I set up a domain
controller once" and being able to talk about a real directory. Every
organization running AD runs more than one DC, and the questions that
come with that (what replicates, what only one server may do, and what
happens when it dies) are standard interview ground.

One promise from Module 3 gets kept here. That 180-day evaluation clock
starts ticking the moment this install finishes, and lesson 5.3 shows
you how to check it and how to push it back.

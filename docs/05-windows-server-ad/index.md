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
- **5.8** see your domain from the network
- **5.9** journal entry
- **5.10** checkpoint

**Tier 1 and up.** DC01 wants 4 GB of RAM, and it's the machine that
stays running for the rest of the course. Budget two evenings: one to
install and promote, one for the directory work in 5.6 through 5.8.
Don't rush the promotion; read what each screen is asking.

One promise from Module 3 gets kept here. That 180-day evaluation clock
starts ticking the moment this install finishes, and lesson 5.3 shows
you how to check it and how to push it back.

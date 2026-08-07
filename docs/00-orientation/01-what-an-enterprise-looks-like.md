---
title: "0.1 What an enterprise actually looks like"
sidebar_position: 1
---

# 0.1 What an enterprise actually looks like

Job postings for junior infrastructure and security roles ask for identity
and access management (IAM), public key infrastructure (PKI), virtualization,
and a security information and event management platform (SIEM). Strip the
acronyms and they are asking whether you have run Active Directory and the
policies that configure every machine on it, issued certificates, built
virtual machines, and read the logs when something looked wrong.

College courses teach you Java and how to subnet on paper. The space between
those two things is where this course lives. Not because nobody teaches these
subjects, plenty of people do, but because they are almost always taught one
at a time, as separate tools with separate tutorials. The job is where they
connect, and that is the part nobody hands you.

## The morning login, unpacked

Watch what happens when an employee turns on their computer at a mid-size
company. It takes about forty seconds and touches more services than most
juniors realize exist.

The machine asks DHCP for an address. It asks DNS where the domain
controllers are. The user types a password, and Kerberos (not the password
itself) travels the network to prove who they are. The domain controller
answers with tickets. Group Policy applies: drive mappings, security
settings, maybe a new wallpaper someone in IT regrets. The laptop joins the
wifi using a certificate it enrolled for automatically from an internal
certificate authority. The user opens a browser and lands on an internal
app, which never asks for a password because single sign-on already
vouched for them. And every one of those steps left a log line that flowed
into a SIEM, where a rule decided it was normal and stayed quiet.

Each hop in that chain is a service. Each service is somebody's job. When
one hop breaks, the user says "the internet is down," and someone has to
know the chain well enough to find the broken link.

That someone is rare. That someone gets hired.

## Why understanding the chain beats knowing the tools

A story from my own lab, details filed off. One day my endpoint security
flagged a known attack toolkit executing on a domain controller. On a DC.
That's about the worst place you can see one, and every instinct says
breach, isolate, panic.

The investigation ended somewhere much less dramatic: the "attacker" was my
own vulnerability scanner, logging in with credentials I'd given it, doing
exactly what I'd scheduled it to do. Its credentialed checks look nearly
identical to a real attacker's lateral movement, because they use the same
protocols. The alert wasn't wrong. It just wasn't the whole story.

The tool said attack. Knowing the environment said scanner. If you only
know tools, you'd have pulled the plug on a healthy domain controller in
the middle of a workday. This course is built to give you the second kind
of knowledge, which is why you'll spend it building the environment rather
than memorizing tool menus.

## What you take from this

Enterprise IT isn't a pile of products. It's an interlocking system, and
the interlocks are the hard part: the CA that the wifi depends on, the DNS
that Kerberos depends on, the time sync that everything depends on. You're
going to build every link of the login chain yourself, in your own lab.
After that, none of it is magic, and "the internet is down" becomes a
puzzle you know how to start solving.

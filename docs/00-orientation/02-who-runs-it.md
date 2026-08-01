---
title: "0.2 The people who run it"
sidebar_position: 2
---

# 0.2 The people who run it

At a big company, the environment from lesson 0.1 is run by teams. At a
small one, it's run by two exhausted people. Either way the work divides
into a few recognizable roles, and it helps to know them now, because this
course will sit you in every one of these chairs at some point.

**Helpdesk / desktop support** is where most careers start. Password
resets, broken printers, "the internet is down." Underrated, because it's
where you learn what users really do all day, which is knowledge the other roles
quietly depend on.

**Systems administrator** runs the servers: the domain controllers, file
shares, Group Policy, patching, backups. When this course has you promote a
domain controller or write a GPO, you're doing sysadmin work.

**Network engineer** owns switches, routers, firewalls, and the question
"can host A reach host B, and should it?" Your OPNsense firewall and the
segmentation around it belong to this chair.

**Identity engineer** is a specialization most people discover by accident:
who are you, how do you prove it, what are you allowed to touch. Active
Directory, Kerberos, certificates, single sign-on. Modules 5, 7, and 8 are
identity work, and it's some of the best-paid, least-crowded territory in
IT because so few people can explain it end to end.

**Security analyst** watches the SIEM, triages alerts, and decides what's
real. The scanner-on-the-domain-controller story from lesson 0.1 is a day
in this person's life. Module 11 puts you here.

**Detection engineer** builds and tunes what the analyst watches. Writing a
rule is easy; writing a rule that doesn't cry wolf four hundred times a day
is a craft. You'll feel this personally when your own lab starts paging you
about nothing.

**Penetration tester / red team** attacks all of the above, with written
permission, to find the gaps first. Module 13 gives you a taste, aimed
strictly at your own lab.

There's no module-per-role mapping to memorize. The point is the opposite:
in your lab you are all of these people at once, which is exactly what the
first job at a small company feels like. When you later join a bigger org
and meet these roles as separate humans, you'll already speak each of their
languages, and you'll know which chair fits you best. I came in through the
sysadmin door and got pulled toward identity and detection. You'll find
your own gravity.

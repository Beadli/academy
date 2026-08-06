---
title: About
description: Who makes Beadli Lab Academy, why it exists, and how to use it.
---

# About

Beadli Lab Academy is a free course that teaches enterprise infrastructure
and security by having you build one. Not read about one, and not click
through somebody else's pre-broken environment: eighteen modules that start
with an empty computer and end with a segmented, monitored, documented lab
that you then attack yourself.

It costs nothing, it has no ads, and it never asks you to buy hardware.

## Why it exists

Most people arrive at their first IT or security job having never seen a
domain controller. They have certifications, or a degree, or a stack of
video courses, and no experience of a system that has to keep working.

The gap isn't knowledge. It's that nobody let them build anything.

Meanwhile the material that does exist splits badly. Attack-focused labs
ship a broken Active Directory to practise against, teaching nothing about
how it was built or defended. Build-focused guides stop the moment the
service starts, leaving out monitoring, backups, certificates and every
other thing that decides whether it survives contact with reality.

This course does the whole arc, on one machine, in one environment that
grows: hypervisor, directory, PKI, single sign-on, Linux, containers,
automation, monitoring, then offensive testing against what you built, then
GRC, assessing it for compliance the way an auditor would.

## Who makes it

Beadli Lab Academy is written by one person who runs the lab it's modelled
on.

That matters more than a biography would. The architecture in these modules
is a scaled-down version of an environment that actually runs: the same
directory design, the same certificate authority arrangement, the same
monitoring and detection stack. When a module explains why something is
done a particular way, the reason is usually that the other way caused a
problem once.

The war stories in the course are real and sanitised. No production
addresses, hostnames or customer detail appears anywhere, and the student
lab deliberately uses a different domain name so nothing you build can
collide with anything real.

**AI is part of how the course is written**, using the workflow
[Module 11](/course/engineering-with-ai) teaches: I decide what a lesson has
to do and what is true, drafting is delegated, and I check the result against
the lab. That is the division of labour Module 11 argues for, and it would be
strange to teach it and hide it.

## How to use it

**Start at [Module 0](/course/intro).** It takes an evening, needs no
software, and it's where the tier system is explained so you can work out
which parts your machine can run.

You need a computer you already own with 16 GB of memory. That covers most
of the course. Two later stretches want more, and every module says at the
top which tier it needs, so you'll never be surprised halfway through.

If you want to build physical hardware eventually, there's a whole
[CyberRack](/cyberrack) section for that. It is not required for any part
of the course.

## Using the material yourself

The course text is **CC BY-NC-SA 4.0**. You can copy it, adapt it and teach
from it, provided you credit Beadli Lab Academy, don't sell it, and share
your version under the same terms. The scripts and code are **MIT**, which
means you can use those however you like, including commercially.

Teachers and training providers: the non-commercial clause is about selling
the material, not about using it in a classroom. If you want to run this
course with students, that's exactly what it's for.

## Getting in touch


- **Questions about the course:**
  [GitHub Discussions](https://github.com/Beadli/academy/discussions)
- **Corrections and bug reports:** open an issue on
  [the repository](https://github.com/Beadli/academy), or send a pull
  request. Errors in the material are treated as defects and get fixed.
- **Email:** steve@beadli.com

If something in a lesson doesn't work, that's worth telling me. The course
is verified by one person on one set of hardware, and the failures that
matter most are the ones that only appear on somebody else's.

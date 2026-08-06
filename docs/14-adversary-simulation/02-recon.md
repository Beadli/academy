---
title: "14.2 Reconnaissance, against your own baseline"
sidebar_position: 2
---

# 14.2 Reconnaissance, against your own baseline

Real intrusions do not start with an exploit. They start with somebody
quietly working out what is there, and that phase is usually the longest one.

You have done pieces of this already. Lesson 5.11 pointed `nmap` and
`ldapsearch` at DC01 and I told you that was "the reconnaissance step of
Module 14 against your own machine". Lesson 4.9's checkpoint had you record
the commands "as the baseline Module 14 will compare against". This lesson
does it properly, and the baseline is what makes it an assessment rather than
poking.

**Boot KALI01** and put it on the lab segment, as lesson 4.6 described. Your
rules of engagement from 14.1 say testing comes from this machine.

## Find your own baseline first

Before you scan anything, open your journal and find what you recorded in
Module 4 and lesson 5.11. You are looking for the list of open ports you saw
then.

**This is the discipline that separates an assessment from a scan.** A scan
tells you what is open. A comparison tells you **what changed**, and change
is where findings live. Somebody who scans monthly and diffs the results
finds the forgotten test service that appeared in March. Somebody who scans
monthly and reads each report fresh does not.

If you did not record it, that is a lesson rather than a failure, and today's
scan becomes the baseline for next time.

## Sweep the network

```bash
# What is alive on the lab network? -sn means "ping scan, no port
# scan": fast, and the first question an attacker asks.
# Substitute your own range if it differs.
nmap -sn 10.10.10.0/24
```

**How you know it worked:** you should see a host line for each machine you
built, and you should be able to name every single one.

**An address you cannot account for is the most interesting possible
result.** It is probably your own phone or laptop holding a DHCP lease from
lesson 4.5. Work out which. "There is a device on my network and I do not
know what it is" is exactly the finding this exercise exists to produce, and
in a company it is how people discover the test server somebody built in
2019.

## Fingerprint what is listening

```bash
# -sV asks each open port what software it is. --version-light
# keeps it quick. -Pn skips the ping check, because Windows hosts
# often do not answer pings while happily serving on port 445.
nmap -Pn -sV --version-light 10.10.10.10
```

Expect the domain controller ports from lesson 5.11: 53, 88, 135, 445, 389,
636, 3268, 3269. **Seeing 88 and 389 on one host is how anyone concludes
"domain controller" in about two seconds**, which you already know, and it is
worth noticing you now read that output fluently.

Run it against UBNT01 too:

```bash
nmap -Pn -sV --version-light 10.10.10.20
```

**Compare against your baseline.** Anything open now that was not open in
Module 4 is something you added, and you should be able to say what and why.
Lesson 13.4's scanner on port 9392 is a good example: you opened that, you
know why, and it should not be a surprise.

:::warning[This is the loud part]
Service fingerprinting is not subtle. It connects to every port and tries to
make each one talk.

Leave your Wazuh dashboard open. You detected exactly this in lesson 12.6, so
your rules should be firing right now. **If they are not, that is the first
real finding of this module**, and lesson 14.9 is where you deal with it.

Notice also that this scan comes from KALI01, which is the source address you
suppressed in 12.6. You may have just silenced your own test. That is the
blind spot working exactly as designed and exactly as warned.
:::

## Ask the directory politely

Lesson 5.11 had you run this once. Run it again, and this time think about
what an attacker does with it:

```bash
# Anonymous LDAP. No credentials at all.
ldapsearch -x -H ldap://10.10.10.10 -s base -b "" namingContexts
```

**How you know it worked:** you get a line reading
`namingContexts: DC=lab,DC=internal`, with your own domain in it.

That came back **unauthenticated**. You supplied no username and no password;
`-x` means simple authentication and you gave it nothing to authenticate with.
From that an attacker learns the domain name, and from the domain name they
can start guessing usernames, because most organisations use a predictable
format.

**If you get `Can't contact LDAP server`**, the address is wrong or DC01 is
not running. That is a connectivity problem rather than a security control;
port 389 is open on a domain controller by design, as lesson 5.11's port
table showed.

**This is not a vulnerability and there is nothing to fix.** The protocol
works this way on purpose. It is here to make a point that lesson 5.11 also
made: "the network is inside the firewall" is not a security model, and
everything meaningful past this point requires credentials.

Which is what the rest of this module is about.

## Test your boundary, from a position of knowledge

Lesson 4.6 promised this: "In Module 14 you'll run these again from a
position of having compromised something, and having today's baseline to
compare against is what turns 'I poked at it' into an assessment."

You have not compromised anything yet. But you can already ask the more
interesting version of the segmentation question. From KALI01, on the lab
segment:

```bash
# Can the lab reach the internet? Probably yes, by design.
ping -c 3 1.1.1.1
```

Now the harder question: can the lab reach your **home** network? Before you
answer it, notice that you already ruled that network out of scope an hour
ago, in the document you wrote in 14.1. "My home network, my router, my
internet provider's equipment" and "any machine I do not personally own"
are both on your out-of-scope list.

**Reaching a network and scanning it are different acts**, and the
distinction is the professional one. Scanning your home range touches
whatever else lives there: a housemate's laptop, a landlord's router, a
device your internet provider owns and you merely rent. None of that is
yours to test, and your own rules of engagement say so.

You do not need a scan to answer the question. **One address you personally
own answers it completely:**

```bash
# Find your home router's address from your own computer first:
# "ipconfig" on Windows, "ip route" on Linux or macOS. Then, from
# KALI01, try that ONE address. Not the range.
ping -c 3 192.168.1.1
```

**What you want here is failure**, and lesson 4.6 said the same thing:
failure is the pass condition. Your lab is about to contain a deliberately
vulnerable machine. If KALI01 can reach your home network, so can anything
that compromises that machine.

If the ping succeeds, you have your answer and you still have no business
enumerating what else is over there. **A reachable boundary is the finding.**
What sits behind it is somebody else's estate, even when the somebody else
is your family.

If it succeeds, stop and fix your segmentation before lesson 14.3. That is
not a detour from the module; it is the module doing its job before you have
run a single exploit.

## Record it

In your journal, write the scan results next to the Module 4 baseline, with
the differences called out. Three columns is enough: port, was it open in
Module 4, is it open now.

That table is what a real assessment's appendix looks like, and it is the
artefact Module 16 wants.

## What you take from this

A current picture of your own network, compared against a recorded past one,
and a boundary test run before you introduce something dangerous rather than
after.

You also have your first detection finding, whether or not you wanted one.

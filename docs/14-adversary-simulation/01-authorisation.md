---
title: "14.1 The authorisation gate"
sidebar_position: 1
---

# 14.1 The authorisation gate

Lesson 4.7 said this module "formalises this with an authorization gate
before any offensive work", and lesson 13.5 said Module 14 "makes you write
one properly". This is that lesson, and it is a real one rather than a
warning label.

## The uncomfortable part first

Every technique in this module is legal to perform on your own lab and a
criminal offence to perform on somebody else's network. In the UK that is
the Computer Misuse Act, in the US the Computer Fraud and Abuse Act, and
most countries have an equivalent. **None of them contain an exception for
curiosity, for good intentions, or for not causing damage.**

Two things people get wrong, both worth stating plainly:

**"I only scanned it" is not a defence.** Port scanning has been prosecuted.
Whether it will be in your jurisdiction is not a bet worth taking on
somebody else's infrastructure.

**Your employer's network is not your network.** Working somewhere does not
authorise you to test it. This one catches genuinely well-meaning people who
find something on a work system, poke at it to confirm, and turn a good deed
into a disciplinary meeting. The correct move is always to report the
observation, not to prove it.

The professional version of this is not caution. It is paperwork.

## What rules of engagement actually are

Before a real engagement, somebody with authority signs a document. It is
usually short. It answers six questions, and once you have seen the list you
will notice that every one exists because of something that went wrong once.

| Question | Why it exists |
|---|---|
| **What may I test?** Exact addresses and hostnames | Testers have hit the wrong subnet. "The whole /16" has taken down a hospital's neighbour |
| **What may I not test?** Named exclusions | Production databases, medical devices, anything with a safety function |
| **When?** Dates and hours | So somebody is awake when something breaks |
| **Which techniques are allowed?** | Denial of service, password spraying against real accounts, and social engineering all need explicit permission |
| **Who do I phone?** Name and number | The single most important line. When something falls over at 2am, this is what stops a test becoming an incident response |
| **Who authorised it?** Signature, and their authority to give it | Somebody who does not own the system cannot authorise testing of it |

That last row is the one juniors miss. **The person signing must actually
have the authority to sign.** A friendly system administrator saying "yeah,
go ahead" is not authorisation. In an engagement, if the person's authority
is unclear, the work does not start.

## Write yours

Your lab is genuinely yours, so this is an exercise. Do it anyway, because
the format is the point and you will be asked to work inside one of these
within a week of any security job.

Create `Projects/lab-rules-of-engagement.md` in your vault. Fill in your own
real values:

```markdown
# Rules of engagement: Beadli lab

**Authorised by:** [your name], owner and operator of this environment
**Date authorised:** [today]
**Valid until:** [a date, not "ongoing"]

## In scope
- 10.10.10.0/24, the lab LAN, in its entirety
- Specifically: DC01 (10.10.10.10), DC02 (10.10.10.11),
  UBNT01 (10.10.10.20), FW01 (10.10.10.254)
- Testing is performed from KALI01 (10.10.10.50 on Tier 1; on Tier 2 use the
  outer-segment address you recorded in lesson 4.4)

## Out of scope
- Every address outside 10.10.10.0/24 without exception
- My home network, my router, my internet provider's equipment
- Any cloud tenant, including the Entra tenant from Module 9
- Any machine I do not personally own

## Permitted techniques
- Port and service scanning
- Vulnerability scanning, including credentialed
- Exploitation of findings against lab machines
- Credential attacks against lab accounts I created

## Prohibited techniques
- Denial of service, including resource exhaustion
- Anything targeting a third-party service, including the internet
  connection itself

## Contact
- [your name], [your phone or email]

## Rollback plan
- All lab VMs snapshotted before testing begins
- Snapshot names and timestamps recorded in the journal
```

**Commit it.** This document is the first evidence in the folder Module 16
turns into an audit package.

```bash
cd ~/git/lab-journal
git add Projects/lab-rules-of-engagement.md
git commit -m "rules of engagement for module 14 testing"
git push
```

## Now the practical safety net

Two things before any offensive work, and they are what makes the rest of
this module relaxing rather than nerve-wracking.

**Snapshot everything.** Lesson 3.5 taught you this, and this is the module
it was for. Snapshot DC01, DC02 and UBNT01 while they are healthy.

**How you know it worked:** open your hypervisor's snapshot manager for each
VM and confirm a snapshot exists with today's date. Write the names in your
journal, which your rules-of-engagement document just promised you would do.

**Know which routes into your lab exist.** Lesson 4.6 asked you to write down
that the Tailscale overlay reaches your lab, and said "you'll want that note
in Module 14 when you're testing which routes into your lab you actually
know about."

Go and read that note now. Then ask the question it was written for: **if
your lab contains a deliberately vulnerable machine from lesson 14.3, what
else can reach it?** If your tailnet includes your phone, your phone can
reach your vulnerable machine. That is probably fine, and it should be a
decision rather than a surprise.

If you would rather close that path for the duration of this module, on FW01
go to **Firewall > Rules > TLSCL** and disable the permissive rule, or shut
the Tailscale service off. Turn it back on afterwards.

:::tip[In GRC terms]
Rules of engagement are a **control** in their own right, and an auditor will
ask to see them before asking about a single finding.

The reason is that testing without documented scope is itself a risk to the
organisation. The document is not there to protect the systems. It is there
to protect everyone from the test.
:::

## What you take from this

A signed scope, snapshots you can roll back to, and a clear head about which
machines are yours. Every remaining lesson in this module assumes all three.

Next lesson you start looking, which is where every real attack starts too.

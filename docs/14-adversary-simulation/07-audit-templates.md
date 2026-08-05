---
title: "14.7 Audit your own certificate templates"
sidebar_position: 7
---

# 14.7 Audit your own certificate templates

Lesson 7.7 made you a promise three separate times. It said misconfigured
templates "are one of the most reliable ways to take over an Active Directory
environment", that you would meet this "in Module 14 from the other side",
and, most importantly:

> Write down what you configured today, because in Module 14 you'll audit it
> and I'd like you to be able to check your own homework.

Go and find that note. This lesson is the marking.

## Why certificates are such a good way in

Lesson 7.1 taught you that a certificate binds an identity to a key, and that
a CA vouches for that binding. Lesson 7.7 built a template controlling who
may request what.

Put those together from an attacker's point of view.

**A certificate is a credential.** In an Active Directory environment, a
certificate with the right purpose can be used to authenticate, exactly like
a password or a hash. So a template that lets the wrong person request the
wrong certificate is a template that issues credentials to the wrong person.

The dangerous combination is specific, and lesson 7.7 named all three parts
without assembling them:

1. **A low-privileged group has Enrol rights** on a template, and
2. **the template permits the requester to supply their own subject name**,
   and
3. **the certificate is valid for client authentication.**

Any ordinary user can then request a certificate saying *they are somebody
else*, and use it to authenticate as that person. Point it at a Domain Admin
and the domain is gone.

**And here is the part that makes it genuinely nasty**, which lesson 7.7 said
plainly:

> it doesn't look like an attack in the logs, because nothing was broken. A
> certificate was issued, exactly as configured.

There is no exploit. The CA did its job. Your logs show a successful,
authorised issuance, because it was one.

## Audit yours

From KALI01, as your unprivileged user. **Certipy** enumerates certificate
templates and flags dangerous configurations:

```bash
sudo apt update
sudo apt install -y certipy-ad
```

**How you know it worked:** `certipy-ad --help` prints usage rather than
"command not found".

**If the package is not found**, the tool's packaging name has changed
between Kali releases. Search the Certipy project's own documentation for
current installation instructions rather than following an older command.

Now enumerate:

```bash
# Ask the CA what templates exist and who may use them.
# -vulnerable asks it to flag the dangerous combinations.
certipy-ad find -u sokoth@lab.internal -p 'yourpassword' \
  -dc-ip 10.10.10.10 -vulnerable -stdout
```

**How you know it worked:** you get a list of certificate authorities and
templates, with a section at the end for anything it considers vulnerable.

## Mark your own homework

Two possible outcomes, and **the boring one is the good one**.

**If it reports nothing vulnerable:** your lesson 7.7 configuration was
sound. Specifically, your `Lab Computer` template did not let requesters
supply their own subject name, and enrolment rights were not granted to
everybody. That is what you were supposed to do and you did it.

Do not skip past this. Open your 7.7 note and check the three properties
above against what you wrote down. **Being able to say "I checked, and here
is why it is safe" is the audit skill.** "The tool said nothing" is not the
same statement.

**If it reports something vulnerable:** excellent, genuinely. You have found
a real misconfiguration in infrastructure you built, using the same tool an
attacker would, and you can now fix it and verify the fix. That is the entire
loop this module exists to teach, and it is worth more than a clean result.

Read what it flagged, then go to the **Certificate Templates** console on
SUBCA01 and look at that template's **Security** tab and its **Subject Name**
tab. The setting that matters most is **"Supply in the request"** versus
**"Build from this Active Directory information"**. The second is the safe
one, and it is safe precisely because it removes the requester's ability to
claim an identity.

## Do not stop at the tool's opinion

Certipy flags known patterns. It does not know your environment, which is the
same limitation lesson 13.1 identified in vulnerability scanners and lesson
12.6 identified in detection rules. **This is the third time the same idea has
appeared, and it is not a coincidence:** every tool in security tells you
about the artefact and nothing about the intent or context around it.

Two questions Certipy cannot answer, that you should:

**Who is actually in the groups with Enrol rights?** A template restricted to
"Domain Computers" sounds narrow until you remember every machine in the
domain is in it, including the one an attacker just landed on.

**Does the CA require manager approval for anything?** Approval turns an
instant automated issuance into a human decision. It is friction, it is
frequently worth it for high-value templates, and it is the certificate
world's version of the least-privilege trade you have been making since
lesson 5.6.

## What it looked like from the defensive side

Check for **Event ID 4886** (certificate services received a request) and
**4887** (approved and issued) on SUBCA01.

Your enumeration probably produced nothing at all, because reading templates
is an LDAP query, not a request. That is the same invisibility as lesson
14.4, for the same reason.

**And if you had actually requested a certificate**, the event would show a
successful issuance that looks entirely legitimate, which brings us back to
lesson 7.7's warning.

So what do you actually do? **The detection here is not about the request. It
is about the template.** The valuable control is monitoring for *changes to
templates and to their permissions*, because the dangerous state is created
by a change, and that change is far rarer and far more suspicious than any
individual certificate request.

That is a genuinely different way to think about detection, and it is worth
holding onto: **when the attack is indistinguishable from normal operation,
move your detection to the configuration that made it possible.**

Write that in your detection-gap list as a control to build, not a rule to
write.

## What you take from this

You audited infrastructure you configured six modules ago, with an attacker's
tool, against a note you wrote to your future self. Whichever answer you got,
you can now explain what makes a certificate template dangerous and why the
resulting attack does not look like one.

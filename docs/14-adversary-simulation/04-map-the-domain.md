---
title: "14.4 Map the domain"
sidebar_position: 4
---

# 14.4 Map the domain

Lesson 5.6 taught you two accounts, one human, and said "Module 14 makes this
uncomfortably concrete by doing it to your lab". This is where that starts.

Everything from here needs a domain, so **Tier 2 and up**. You also need one
valid set of domain credentials, which you have, because you created them:
your everyday `sokoth` account with no privileges at all.

**That is the point of this lesson.** An attacker who phishes one ordinary
employee has exactly what you have now. What can they see?

## The insight this lesson is built on

Active Directory is a database that, by design, **every authenticated user
can read**.

Not the passwords. But the users, the groups, who is in which group, which
computers exist, who can administer what, and how all of it connects. That is
not a misconfiguration; the directory would not function if ordinary
machines and users could not look up its structure.

The consequence took the industry an embarrassingly long time to appreciate:
**a low-privileged account can compute the entire map of how to become a
Domain Admin**, without touching anything privileged, because the map is
public to members.

That is what this lesson does.

## Ask the directory yourself first

Before the tool, do it by hand once. From KALI01, with your unprivileged
account:

```bash
# Ask the directory who is in Domain Admins, as an ordinary user.
# Substitute your domain and username.
ldapsearch -x -H ldap://10.10.10.10 \
  -D "sokoth@lab.internal" -W \
  -b "DC=lab,DC=internal" \
  "(&(objectClass=user)(memberOf=CN=Domain Admins,CN=Users,DC=lab,DC=internal))" \
  sAMAccountName
```

`-W` prompts for the password rather than putting it in your shell history,
which is lesson 1.6's rule applied to an attack tool.

**How you know it worked:** you get back the accounts that are in Domain
Admins, including the `.adm` account you made in lesson 5.6.

**Now register what just happened.** An account with no privileges
successfully asked the directory to name every administrator in the domain,
and the directory answered, because that is its job. You have just built an
attacker's target list using a normal feature, and nothing in any log will
look like an attack, because nothing was.

## Now the tool that does it properly

**BloodHound** collects everything the directory will tell an authenticated
user, then draws it as a graph and answers one question: *from where I am,
what is the shortest path to Domain Admin?*

It changed this field. Before it, finding attack paths was manual and people
missed them; after it, both attackers and defenders could see in seconds that
"the helpdesk group can reset the password of an account that administers the
server that a Domain Admin logs into."

**Install it on KALI01**, which is the machine your rules of engagement name
as the testing host:

```bash
sudo apt update
sudo apt install -y bloodhound
```

**How you know it worked:** `bloodhound --version` or launching it from the
applications menu opens a window asking for a database connection.

:::info[If the package will not install]
BloodHound's packaging changes between major versions and Kali sometimes
carries a different edition than the project's current one.

If `apt` cannot find it, go to the **BloodHound project's own documentation**
and follow their current installation guide rather than an older blog post.
Search their docs for "installation"; the community edition is the one you
want. This is lesson 5's evergreen problem, and the honest instruction is to
use the source rather than a command I pinned in a course.
:::

**Collect the data.** The collector runs as your unprivileged user and asks
the directory the questions above, thousands of times:

```bash
# The Python collector, which runs from Linux. Substitute your
# domain, username and DC address.
bloodhound-python -u sokoth -p 'yourpassword' \
  -d lab.internal -ns 10.10.10.10 -c All
```

**How you know it worked:** several `.json` files appear in the current
directory, named for what they contain (users, groups, computers). Import
them into BloodHound by dragging them into its window.

## Read the graph

Use the built-in query **Shortest Paths to Domain Admins**.

On a lab as small as yours the answer may be short and boring: your `.adm`
account is a Domain Admin, and that is the whole path. **Boring is the
correct result and worth understanding as a result**, not a failure of the
exercise. Your domain is small, you built it deliberately, and you applied
least privilege in lesson 5.6. This is what good looks like.

Then look at the things that are interesting anyway:

**Find where your accounts can go.** Select your `sokoth` account and use
**Reachable High Value Targets**. For a properly unprivileged account this
should be very short.

**Look at what the scanner can reach.** Lesson 13.6 warned that a scanner
with Domain Admin is a standard intrusion path, and asked you to scope its
account deliberately. If you created a domain account for scanning, find it
in BloodHound and check its reachable targets. **This is how you verify that
your least-privilege decision actually held**, rather than trusting the
intention behind it.

**Look at group nesting.** BloodHound draws groups inside groups. Nesting is
how real environments accumulate privilege nobody intended: somebody adds a
group to a group for a good reason, and three years later that chain grants
administrative rights to forty people who could not tell you why.

## The uncomfortable concrete bit

Lesson 5.6 said this, about logging into a machine with a privileged account:

> If that session is a Domain Admin session, they inherit the whole domain in
> one step. If it's `sokoth` with no privileges, they've got a foothold and a
> lot more work ahead.

BloodHound's `HasSession` edge is that sentence rendered as a line on a
graph. It records **which accounts are currently logged into which
machines**, and it is the single most valuable thing the tool collects,
because it turns "compromise this workstation" into "become that
administrator".

If you have ever logged into DC01 or a member server with your `.adm`
account and left the session open, that edge exists in your own graph. Look
for it.

**The defence is exactly the habit lesson 5.6 taught**, and now you can see
why it is a habit rather than a preference: a privileged session is a
credential sitting on a machine, and an attacker on that machine collects it.
Use the privileged account for the task, then log out. Not "when convenient".
That is the whole control.

## What it looked like from the defensive side

Check your Wazuh dashboard, and be ready for a disappointing answer.

**BloodHound collection is very difficult to detect, and you should
understand why rather than assume your monitoring is bad.** The collector
made a large number of ordinary LDAP queries, using valid credentials, that
any domain-joined machine makes all day. There is no malformed packet, no
failed login, no privilege escalation. It is a normal user doing normal
things, quickly.

This is the same structural point as lesson 12.6, one level deeper: **the
only difference between reconnaissance and normal operation is intent, and
intent is not in the protocol.** Detection here is possible but it is
statistical (this account made ten thousand LDAP queries in ninety seconds,
which it has never done before), not signature-based.

That is genuinely what the industry does about this, and knowing that a
technique is hard to detect is more useful than believing you would catch it.

**Write it in your detection-gap list.** "Directory enumeration by a valid
low-privileged account" belongs there, with the honest note that catching it
needs behavioural baselines rather than a rule.

## What you take from this

The map of your own domain, drawn from the position of an ordinary user, and
a concrete understanding of why privileged sessions are the thing attackers
actually hunt.

Next lesson, an ordinary user asks the directory for something rather more
alarming than a group membership.

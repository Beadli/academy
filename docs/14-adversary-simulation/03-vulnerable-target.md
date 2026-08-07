---
title: "14.3 A deliberately vulnerable target"
sidebar_position: 3
---

# 14.3 A deliberately vulnerable target

Lesson 4.6 warned you that by this module your lab would contain deliberately
vulnerable machines. Here is the first one.

Lesson 6.9 taught you SQL injection as a concept, ending with: "Defence in
depth means the second control matters precisely because the first one
sometimes fails. You will meet this idea again in Module 14, from the other
side." This is that lesson, and the other side turns out to be more
interesting than it sounds.

**This lesson needs only UBNT01.** No domain, so Tier 1 students get all of
it.

## Why you have to install a target at all

Module 13 said Module 14 would take your findings and attack them. Look at
what your lesson 13.5 network scan actually produced: very little, and
probably nothing in the KEV catalog. I told you at the time that an empty
result was a good result and a real one.

**That is still true, and it is inconvenient here.** You built this lab from
current software a few modules ago and patched it in 13.7. There is no
neglected 2019 web application on it to break into, because you have not
neglected anything yet.

So rather than pretend, this lesson installs a target on purpose. **Be clear
about what that changes:** you are learning the technique, not discovering a
weakness in your own environment. Those are different activities, and
conflating them is how people come away from a lab believing they have
assessed something.

The genuine findings about your lab in this module come from lessons 14.2
(what is on your network that you cannot account for), 14.4 (what your
existing accounts can reach), 14.7 (whether your own certificate templates
hold up) and 14.9 (what your monitoring missed). Those are the assessment.
This lesson is the practice.

## What you are about to run, and the rule that goes with it

**DVWA**, the Damn Vulnerable Web Application, is a PHP application built on
purpose to be broken. It is the standard teaching target, it is deliberately
awful, and it is genuinely dangerous to expose.

:::warning[This machine is a liability while it runs]
You are about to start software that is designed to be exploitable, on a
server that sits on your lab network next to your domain controllers.

Three rules, and they are not negotiable:

1. **It binds to the lab network only**, never through your reverse proxy,
   never with a DNS name, never through Tailscale.
2. **It runs while you are working on it and stops afterwards.** The last
   step of this lesson removes it. Do that step.
3. **If your segmentation test in 14.2 failed, fix that first.** A
   deliberately vulnerable machine that can reach your home network is how a
   learning exercise becomes a real incident.

This is the same reasoning as lesson 13.4's warning about the scanner, one
notch more serious, because this thing is meant to lose.
:::

## Run it

On UBNT01, following the stack convention from lesson 6.5:

```bash
mkdir -p ~/docker/dvwa
cd ~/docker/dvwa
```

Create `compose.yaml`:

```yaml
services:
  dvwa:
    image: vulnerables/web-dvwa
    container_name: dvwa
    # Port 8081 on the host, 80 in the container. Deliberately
    # NOT behind the reverse proxy and NOT given a DNS name:
    # this one stays awkward to reach on purpose.
    ports:
      - "8081:80"
    restart: "no"
```

Note `restart: "no"`. Every other stack you have built uses
`restart: unless-stopped`, because you want those services back after a
reboot. **You want the opposite here.** If UBNT01 restarts, this should stay
down until you deliberately start it.

```bash
docker compose up -d
```

**How you know it worked:**

```bash
# Running, with the port mapped.
docker compose ps

# The application answers. Expect 302, a redirect to the login page.
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8081/

# And the login page itself. Expect 200.
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8081/login.php
```

**A 302 on the first one is correct, not an error.** The application is
redirecting you to `login.php`, which is what the second check confirms.

Then from your own computer, browse to `http://10.10.10.20:8081`. If `ufw`
from lesson 6.3 blocks it, allow it **temporarily** and remember you did:

```bash
sudo ufw allow 8081/tcp
```

DVWA's own first-run page has a **Create / Reset Database** button; click it,
then log in. The default credentials are printed on the login page and are
`admin` / `password`, which is itself a finding of the kind lesson 13.1 called
configuration.

Set **DVWA Security** to **Low** in the security tab. You are going to raise
it later, and the difference is the lesson.

## Now break it

Go to **SQL Injection**. There is a box asking for a User ID. Type `1` and
you get one user back.

Now type what lesson 6.9 taught you:

```text
' OR '1'='1
```

You get every user in the database.

**Sit with that for a moment, because you predicted it three modules ago.**
The query became `SELECT ... WHERE user_id = '' OR '1'='1'`, the condition is
always true, and your input stopped being data and became part of the
command. You have now done the thing you read about, and it worked exactly as
described.

Try the escalation:

```text
' UNION SELECT user, password FROM users #
```

That returns password hashes. Not passwords, hashes, for the reason lesson
9.6 explained: the application never stored the passwords. **Notice that
what you have stolen is exactly what Module 9 told you was worth stealing**,
and lesson 14.6 is about what an attacker does with hashes.

## The other defect class, briefly

Go to **XSS (Reflected)** and enter:

```text
<script>alert('xss')</script>
```

A dialog box appears. That is trivial, and the triviality is misleading:
what you just proved is that **you can make somebody else's browser run code
of your choosing** when they visit a page from this site. In a real
application that is how session cookies get stolen.

**Now notice that this is the same defect as the SQL injection.** Different
language, different destination, identical shape: input crossed a boundary
and became instructions. Lesson 6.9 said this in advance, and here it is
demonstrated twice:

> Somewhere, a boundary between data and instructions was not enforced. The
> same shape turns up in command injection, in cross-site scripting, and in
> places that have not been invented yet.

**This is the single most valuable generalisation in application security.**
People learn ten separate vulnerabilities and miss that they are one defect
wearing different hats. The fix is also the same shape every time: keep the
structure and the values separate, and never build one out of the other.

## Naming what you just did

Lesson 13.1 taught you CVE and CVSS: names and scores for *specific flaws in
specific software*. Neither fits what you just exploited, because DVWA's SQL
injection is not a numbered flaw in a product. It is a category of mistake.

The application security world uses two other systems for that, and you
should be able to tell all four apart:

- **CWE, Common Weakness Enumeration.** A catalogue of *kinds* of defect.
  SQL injection is CWE-89, cross-site scripting is CWE-79. Where a CVE says
  "this product, this flaw", a CWE says "this class of mistake, anywhere".
  A CVE usually cites the CWE it is an instance of.
- **The OWASP Top 10.** A periodically updated list of the categories causing
  the most real harm in web applications. It is not a standard, it is a
  priority list, and it is what people mean by "we test against OWASP".

**Now the promise lesson 8.7 made.** When you decoded a JWT it said that an
application accepting a token without verifying the signature, or without
checking `aud` and `exp`, "has no security at all while appearing to work
perfectly", and that both are "common enough to have their own entries in
vulnerability classifications, and Module 14 will look at what that costs".

Here is what it costs, and you have everything you need to work it out.

A JWT is readable by anyone holding it, as you saw. The signature is the only
thing making it trustworthy. So:

- **No signature check** means anybody can edit the token. Change
  `"role": "user"` to `"role": "admin"`, send it, and a server that does not
  verify will believe it. **The cost is total authorisation bypass**, with no
  exploit, no malformed input, and nothing in any log that looks wrong,
  because the request is perfectly well formed.
- **No `exp` check** means a token stolen once works forever. Revocation
  stops meaning anything, and the incident you contained last year is still
  open.
- **No `aud` check** means a token issued for one service is accepted by
  another. A low-value application's tokens open a high-value one.

**Notice the shape**, because it is the same one as the injections above: a
value that should have been treated as untrusted data was treated as
authoritative instruction. The boundary was not enforced. Different layer,
identical mistake.

That is the generalisation worth carrying out of this module, and it is why
these categories exist as categories rather than a list of products.

## Defence in depth, from the other side

Now the part lesson 6.9 promised.

Set **DVWA Security** to **Impossible** and run the exact same SQL injection
again.

Nothing happens. You get one user back, or none. The input is treated as a
value, because that version uses the parameterised query you saw in 6.9:

```php
// The value is passed separately and can never be code.
$data = $db->prepare('SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;');
$data->bindParam(':id', $id, PDO::PARAM_INT);
```

**Here is what defence in depth feels like from the attacking side, and it
is not what people expect.**

It is not dramatic. There is no alarm, no block page, no message. The attack
simply **does nothing**, and you cannot tell from the outside whether the
application is well written, whether your payload was wrong, or whether you
have the wrong idea entirely. You try a variation. That does nothing either.

That ambiguity is the control working. An attacker's time is finite, and a
target that returns nothing interesting for twenty minutes is a target they
leave for an easier one. **The value of the second control is not that it
announces itself. It is that it is boring**, and boring is expensive to
attack.

Set the security level back to **Low** for the moment; lesson 14.9 wants one
more thing from this machine.

## What it looked like from the defensive side

Open your Wazuh dashboard. Two questions:

**Did anything at all fire?** A web application under attack produces
distinctive log entries: unusual query strings, `UNION SELECT` in a URL,
angle brackets where a username belongs.

**Almost certainly nothing fired, and here is why**: you never told Wazuh
about this container. Lesson 12.2 enrolled an agent on UBNT01 and pointed it
at the system's logs. DVWA's web logs live *inside a container*, which is a
separate filesystem the agent is not reading.

**That is a real and extremely common gap.** Organisations move applications
into containers and quietly lose the log sources their detections were built
on. Nobody decides to do this; it happens because the logs moved and the
monitoring did not follow.

You do not have to fix it today. **Write it down as a finding**, in the
detection-gap list lesson 12.11 had you start. It is a better finding than
any of the injection results, because the injections were guaranteed to work
and this one you discovered.

## Take it down

```bash
cd ~/docker/dvwa

# Stop and remove the container and its network.
docker compose down

# And close the hole you opened in the firewall.
sudo ufw delete allow 8081/tcp
```

**How you know it worked:**

```bash
# No dvwa container. Expect it to be absent from the list.
docker ps -a --format '{{.Names}}' | grep dvwa || echo "gone, as intended"

# And the port is closed again.
sudo ufw status | grep 8081 || echo "rule removed"
```

**Do not skip this.** A deliberately vulnerable application left running on a
lab you eventually stop paying attention to is exactly how home labs end up
in other people's botnets.

The `compose.yaml` stays in Git, so bringing it back for ten minutes is one
command. That is the right shape: the definition is permanent, the running
service is not.

## What you take from this

You exploited two vulnerabilities you had already been taught the theory of,
watched a properly written control make both of them boring, and found a
detection gap that nobody planted for you.

You also removed the vulnerable machine when you finished, which is a habit
worth more than any of the exploits.

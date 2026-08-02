---
title: "6.7 Give it a real name: DNS and a reverse proxy"
sidebar_position: 7
---

import ReverseProxy from '@site/static/img/module6-reverse-proxy.svg';

# 6.7 Give it a real name: DNS and a reverse proxy

Right now your Git server is reachable at `127.0.0.1:3000` on one
machine and nowhere else. By the end of this lesson it answers to
`git.lab.internal` from anywhere in your lab, and you'll have
built the pattern every service in this course uses from here on.

## Two problems, one shape

**Problem one: names.** Nobody remembers `10.10.10.20:3000`. You have a
domain and a DNS server; use them.

**Problem two: ports.** Your next service will want a port too, and the
one after that. You'd end up with a machine exposing a dozen numbered
doors, each one something to remember and secure.

A **reverse proxy** solves both. It's a web server that listens on the
normal ports, looks at which *name* the browser asked for, and forwards
the request to the right service on loopback. One front door, many rooms
behind it. It's also the natural place to terminate TLS, which is why
Module 7 comes back here.

<ReverseProxy role="img" aria-label="Request flow: your laptop asks DC01's DNS who git.lab.internal is and gets 10.10.10.20, then sends the request to that address on port 443. On UBNT01, nginx is the only thing listening on ports 80 and 443; it reads the name requested and forwards to services bound to 127.0.0.1 only, which are unreachable from the network: Gitea on port 3000, and step-ca on port 9000 arriving in Module 7." style={{width: '100%', height: 'auto'}} />

### What that picture is showing

Follow one request through it, in the four numbered steps.

**1. Your laptop asks DNS a question.** You type `git.lab.internal` and
your machine has no idea what that means, so it asks its DNS server,
which is DC01, the domain controller you built in Module 5. DC01 holds
the record you're about to create and answers `10.10.10.20`. Nothing
about this step involves nginx or Gitea; it's pure name lookup, and if
it fails nothing else in the picture ever happens.

**2. The request goes to that address, on port 443.** Your browser
connects to UBNT01. Notice what it does *not* do: it never mentions port
3000, and it doesn't know Gitea exists. From the outside, this machine
appears to offer one website.

**3. nginx reads which name you asked for.** This is the part that makes
the whole arrangement work. A single HTTPS request carries the hostname
inside it, so nginx can look at "this person asked for
`git.lab.internal`" and match it against the `server_name` lines in its
configuration. One listener, many sites, chosen by name.

**4. nginx forwards the request to a service on loopback.** Gitea is
listening on `127.0.0.1:3000`, which means it accepts connections *from
the machine itself and nowhere else*. That's the dashed box in the
diagram. nginx is on that machine, so it can reach Gitea; your laptop
cannot, and neither can an attacker on your network. The reply travels
back the same way.

The dimmed `step-ca` box is the next service to arrive, in Module 7. It
gets its own name, its own file in `sites-available`, and its own
loopback port, and the network-facing surface of this server does not
grow by a single port. That's the property worth remembering: **adding a
service should not mean opening a door.**

## Create the DNS record

On **DC01**, in an administrator PowerShell window. This is the DNS
server you built in Module 5, and now you're adding your first record to
it by hand:

```powershell
# An A record maps a name to an address. This creates
# git.lab.internal pointing at UBNT01.
Add-DnsServerResourceRecordA -Name "git" `
                            -ZoneName "lab.internal" `
                            -IPv4Address "10.10.10.20"

# Read it back.
Get-DnsServerResourceRecord -ZoneName "lab.internal" -Name "git"
```

Then test resolution from UBNT01, which proves the whole chain: your
Linux server asking your Windows DNS server about a name you invented.

```bash
dig +short git.lab.internal      # expect 10.10.10.20
```

If that returns nothing, your DNS settings from lesson 6.1 are the
suspect, not the record.

## Install nginx and write a site

```bash
sudo apt install -y nginx
```

Browse to `http://10.10.10.20` from your laptop and you'll get nginx's
default welcome page. That's the front door, currently opening onto
nothing useful.

```bash
sudo nano /etc/nginx/sites-available/gitea
```

```nginx
server {
    listen 80;
    server_name git.lab.internal;

    # Gitea pushes repositories over HTTP, and nginx's default 1 MB
    # body limit will reject anything larger. This is the setting
    # people discover the hard way on their first real push.
    client_max_body_size 512M;

    location / {
        proxy_pass http://127.0.0.1:3000;

        # Without these the application sees every request as coming
        # from nginx on localhost, and builds its links wrongly.
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

That `server_name` line is the whole trick: nginx serves this block only
when the browser asked for that name. Add another service later and it
gets its own file with its own name, on the same two ports.

Enable it and check your work before reloading:

```bash
# Debian and Ubuntu use a two-directory pattern: sites-available
# holds every site you've written, sites-enabled holds symlinks to
# the ones that are live. Disabling a site is deleting a link, not
# a file.
sudo ln -s /etc/nginx/sites-available/gitea /etc/nginx/sites-enabled/

# Remove the default welcome page so it stops answering for
# anything that doesn't match a name.
sudo rm /etc/nginx/sites-enabled/default

# ALWAYS test before reloading. This catches typos while the old
# config is still serving traffic.
sudo nginx -t

# Reload, which applies the config without dropping connections.
sudo systemctl reload nginx
```

`nginx -t` before every reload is a habit worth building now. A syntax
error caught by `-t` costs you five seconds; the same error found by
`restart` takes the site down until you fix it.

## Use it

From your own computer, browse to **`http://git.lab.internal`**.

Your laptop resolved that name from your domain controller, reached
nginx on UBNT01, and nginx handed the request to a container listening
only on loopback. Four things you built, cooperating.

Complete the Gitea setup page now if you haven't: confirm the URLs it
shows use your new name, keep SQLite, and create your admin account.

:::note[Your browser will say this is not secure]
It's HTTP, so it is saying something true. Everything you push, and your
password, crosses the network in the clear. On a lab network you own,
today, that's an acceptable trade for one module.

Module 7 fixes it properly: you'll build a certificate authority, issue
this server a certificate, and teach your machines to trust it. Then
this address turns into `https://` with no warning at all, which is the
same path a real organization takes, and a much more satisfying one
than clicking "accept the risk" forever.
:::

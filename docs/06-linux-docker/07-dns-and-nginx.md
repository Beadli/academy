---
title: "6.7 Give it a real name: DNS and a reverse proxy"
sidebar_position: 7
---

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

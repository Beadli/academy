---
title: "7.6 HTTPS at last, issued automatically"
sidebar_position: 6
---

# 7.6 HTTPS at last, issued automatically

Time to collect on the promise from lesson 6.7. Gitea gets a real
certificate, from your own CA, and your browser stops complaining.

You could do this by hand: generate a key, build a CSR, submit it, wait,
install the result, and put a reminder in your calendar for when it
expires. People did that for years, and the reason certificate outages
were common is that reminders get missed and people leave.

You're going to do it the modern way instead, with **ACME**: the server
proves it controls the name, gets a certificate automatically, and
renews itself forever without anyone remembering anything. Same protocol
Let's Encrypt uses. Your CA already speaks it, because you turned it on
in lesson 7.4.

## Install an ACME client

`acme.sh` is a shell script with no dependencies, which makes it a good
fit for a server you want to keep simple. On **UBNT01**:

```bash
# Fetch it, look at what it does, then run it. Same rule as the
# Docker install in lesson 6.4.
curl -fsSL https://get.acme.sh -o get-acme.sh
less get-acme.sh
sh get-acme.sh --home /root/.acme.sh --accountemail "you@example.com"
```

You'll need it as root, since it writes certificates nginx must read.

## Point it at your own CA

```bash
sudo -i        # the rest of this lesson runs as root

# Tell acme.sh to use YOUR certificate authority instead of a public
# one. That URL is your step-ca's ACME directory endpoint.
~/.acme.sh/acme.sh --set-default-ca \
  --server https://ca.lab.internal:9000/acme/acme/directory
```

This is the step worth pausing on. The client is unchanged, the protocol
is unchanged, and the only difference between issuing from your lab CA
and issuing from Let's Encrypt is that URL. Everything you learn here
transfers directly to public certificates.

## Issue the certificate

step-ca needs to verify that the machine asking for `git.lab.internal`
actually controls it. The simplest proof is HTTP: the CA asks for a file
at a known path, nginx serves it, and the CA is satisfied.

```bash
# --webroot points acme.sh at the directory nginx serves from, so
# the challenge file lands where the CA will look for it.
~/.acme.sh/acme.sh --issue -d git.lab.internal --webroot /var/www/html
```

If that fails, the usual causes in order: the CA can't resolve
`git.lab.internal` (check DNS from the container's point of view), nginx
isn't serving `/var/www/html` on port 80, or the firewall from lesson 6.3
is blocking port 80.

## Install it where nginx will find it

Never point nginx directly at acme.sh's internal directory. Use the
install command, which copies the files where you want them **and**
records how to reload nginx after every future renewal:

```bash
mkdir -p /etc/nginx/certs

~/.acme.sh/acme.sh --install-cert -d git.lab.internal \
  --key-file       /etc/nginx/certs/git.key \
  --fullchain-file /etc/nginx/certs/git.crt \
  --reloadcmd      "systemctl reload nginx"
```

The `--fullchain-file` matters, and it's lesson 7.1's chain-of-trust
point in practice. That file contains your server's certificate *and*
the CA's intermediate. Install only the server certificate and browsers
that already have your root may still fail, because they can't complete
the chain. "Works on my machine, fails on my colleague's" is almost
always a missing intermediate.

## Turn on HTTPS

```bash
nano /etc/nginx/sites-available/gitea
```

```nginx
# Anything arriving on port 80 gets sent to HTTPS, except the ACME
# challenge path, which must stay on HTTP for renewals to work.
server {
    listen 80;
    server_name git.lab.internal;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name git.lab.internal;

    ssl_certificate     /etc/nginx/certs/git.crt;
    ssl_certificate_key /etc/nginx/certs/git.key;

    client_max_body_size 512M;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then the habit from lesson 6.7, which matters more now that a mistake
takes the site down:

```bash
nginx -t && systemctl reload nginx
```

Tell Gitea its address changed, so the clone URLs it displays are right:

```bash
exit                                 # back to your normal user
cd ~/docker/gitea
sed -i 's|http://git.lab.internal/|https://git.lab.internal/|' compose.yaml
docker compose up -d
```

## The payoff

Browse to **`https://git.lab.internal`**.

No warning. A padlock. A certificate issued by a certificate authority
you built, trusted by a machine you configured, for a name in a domain
you created, on a network you designed. Nothing in that sentence existed
eight modules ago.

Prove it from the command line too:

```bash
# Full validation against the system trust store. "Verify return
# code: 0 (ok)" is the line you want.
openssl s_client -connect git.lab.internal:443 -servername git.lab.internal </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates

# And the chain verdict.
curl -sI https://git.lab.internal | head -1
```

Compare the issuer against what you saw in lesson 7.1. It's your CA now.

## Renewal, which is the actual point

```bash
# acme.sh installed a cron job when you set it up. This is it.
sudo crontab -l | grep acme

# Force a renewal now to prove the whole path works unattended,
# including the nginx reload.
sudo ~/.acme.sh/acme.sh --renew -d git.lab.internal --force
```

Watch it issue a new certificate and reload nginx without you touching
anything. That's the difference between having a certificate and having
a certificate *process*. Certificate expiry is one of the most common
causes of self-inflicted outages in real organizations, and it happens
almost exclusively where somebody was supposed to remember.

Now do the same for OPNsense if you're on Tier 2, and collect the other
warning you've been carrying since Module 4. Its web interface has a
certificate import page under **System > Trust > Certificates**; import
the certificate and key, then select it under **System > Settings >
Administration**.

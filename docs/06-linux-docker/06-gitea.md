---
title: "6.6 Gitea: your own Git server"
sidebar_position: 6
---

# 6.6 Gitea: your own Git server

In lesson 1.4 you pushed your journal to GitHub because you had nowhere
else to put it, and I said you'd build your own once you could host
things. You can host things now.

**Gitea** is a Git server: repositories, a web interface, issues, pull
requests. It's a single container, it's genuinely pleasant, and it's what
I run for my own lab's repositories. Self-hosting your source control is
also a real organizational decision with real reasons behind it, which
this lesson gets to at the end.

## Deploy it

```bash
mkdir -p ~/docker/gitea
cd ~/docker/gitea
nano compose.yaml
```

```yaml
services:
  gitea:
    image: gitea/gitea:1
    container_name: gitea
    restart: unless-stopped
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__server__ROOT_URL=http://git.lab.cyber.internal/
    volumes:
      - ./data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "127.0.0.1:3000:3000"
```

Three things in there are worth stopping on.

**`gitea/gitea:1`** pins the major version. Not `latest`, which can
upgrade across a major release overnight and change things underneath
you, and not a full version number, which would freeze you out of
security patches. Major-version tags are the sensible middle for
self-hosted services.

**`./data:/data`** is the volume from lesson 6.5, and it's where every
repository will actually live. That directory, next to this file, *is*
your Git server's data. Back that up and you have everything.

**`GITEA__server__ROOT_URL`** tells Gitea the address people will reach
it at, so the clone URLs it displays are correct. That name doesn't
exist yet; lesson 6.7 creates it. Those double underscores are Gitea's
way of expressing a config file's sections as environment variables,
which is a pattern you'll meet in a lot of containerised software.

Start it and open the firewall for the web traffic that lesson 6.7 will
send:

```bash
docker compose up -d
docker compose logs -f      # watch it initialise, then Ctrl+C

# Nginx will need these shortly.
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## Complete the setup

Gitea is on loopback only, so you can't reach it from your laptop yet.
Prove it's alive from the server:

```bash
curl -I http://127.0.0.1:3000
```

An HTTP response means it's running. The web installer needs a browser,
so finish this part **after** lesson 6.7 gives it a reachable name. If
you'd rather see it now, an SSH tunnel forwards the port to your own
machine for one session:

```bash
# Run on YOUR computer. Then browse to http://localhost:3000
ssh -L 3000:127.0.0.1:3000 sam@10.10.10.20
```

That tunnel trick is worth keeping. It's how you reach an admin
interface that has no business being exposed, without exposing it.

When you do get to the installer, take the defaults with two changes:
keep the built-in SQLite database (fine for a lab, and one less
container), and **create the administrator account at the bottom of the
page** rather than skipping it. Skipping means the first person to
register becomes the admin, which on a private lab is you, and in the
wild is whoever finds it first.

## Why organizations do this

Gitea is small, but the reasoning behind running it is not.

Code and infrastructure definitions are among the most sensitive things
an organization owns. They describe how everything works, they routinely
contain configuration nobody meant to publish, and they're a map for
anyone attacking you. Plenty of organizations are entirely happy on
hosted services, and plenty have regulatory or contractual reasons they
can't be. Both are defensible. What isn't defensible is not having
decided.

You're about to move your engineering journal here, and your journal
contains your lab's addresses, its hostnames, and the "what broke"
notes that read like a penetration test report of your own environment.
That's a good reason for it to live on a machine you control, and a
good reason to think about who could reach it.

Next lesson: give this thing a name and a front door.

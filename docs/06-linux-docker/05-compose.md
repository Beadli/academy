---
title: "6.5 Compose: a stack described in a file"
sidebar_position: 5
---

# 6.5 Compose: a stack described in a file

The `docker run` command in lesson 6.4 was already getting long, and it
only had three options. Real services need volumes, environment
variables, restart policies, and often several containers that have to
find each other. Nobody remembers that as a command, and a command isn't
something you can put in Git.

**Docker Compose** is that command written down as a file. One `.yaml`
describing what should be running, and two words to make it so.

## Where data lives: volumes

First, the question lesson 6.4 ended on.

A container's filesystem dies with it. To keep anything, you map a
directory on the host into the container, so writes land on UBNT01's
disk instead of inside the disposable box. That mapping is a **volume**,
and it's the line most likely to matter when you're reading somebody
else's compose file: it tells you where the real data is.

The rule of thumb: **containers are disposable, volumes are not.** Back
up the volumes, and you can throw the containers away as often as you
like. Get that backwards and you will eventually delete something you
wanted.

## A place for stacks

Give yourself a predictable layout, for the same reason lesson 3.3 gave
every VM its own folder:

```bash
# One directory per stack, all in one place.
mkdir -p ~/docker/whoami
cd ~/docker/whoami
```

## Write one

```bash
nano compose.yaml
```

```yaml
services:
  whoami:
    image: traefik/whoami
    container_name: whoami
    restart: unless-stopped
    ports:
      - "127.0.0.1:8081:80"
```

Read it as four answers. **image**: what to run. **container_name**: what
to call it, instead of a random name. **restart: unless-stopped**: bring
it back after a reboot or a crash, unless I stopped it deliberately,
which is what you want for anything that matters. **ports**: publish it,
and note the `127.0.0.1:` prefix, which is doing real work.

That prefix means the service listens **only on the server itself**, not
on the network. Compare it to lesson 6.4, where `-p 8080:80` exposed
nginx to your whole LAN. From here on, services in this lab are published
to loopback and reached through a reverse proxy, which lesson 6.7 builds.
One front door, not a scattering of open ports, is how you keep track of
what a machine actually exposes.

## Run it

```bash
# Read the file, pull what's missing, start everything. -d detaches.
docker compose up -d

# What did that create?
docker compose ps

# Prove it's listening on loopback only.
curl http://127.0.0.1:8081
```

That last command prints the container's view of the request. Now try it
from your own computer at `http://10.10.10.20:8081`, and watch it fail:
the port is bound to loopback, so nothing outside the server can reach
it. The failure is the lesson.

The other verbs, which are all you need:

```bash
docker compose logs -f      # follow the logs, Ctrl+C to stop
docker compose restart      # bounce it
docker compose pull         # fetch newer images
docker compose down         # stop and remove the containers
```

`down` removes containers but leaves volumes alone, which is exactly the
disposable-containers, durable-data split from earlier in this lesson.

## Why this file is the point

You now have a text file that fully describes a running service. Put it
in Git and you have the service's history: what changed, when, and why.
Copy it to another machine and you get the same service. Hand it to a
colleague and they can read what you deployed without logging into
anything.

That's infrastructure as code, in its smallest useful form, and it's the
same idea Module 10 scales up with Ansible. Which is a good reason to
start now:

**This is a different machine, so Git does not know you here.** In lesson
1.3 you told Git your name and email on your laptop. That setting lives in
your home directory, not in Git itself, and UBNT01 has never met you. Skip
this and `git commit` refuses with *"Author identity unknown"*:

```bash
# Same two values you used in lesson 1.3. Every commit is stamped
# with them, which is how history says who did what.
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# And the branch-name setting from 1.3, for the same reason: this
# server would otherwise create branches called "master" while
# lesson 6.8 pushes "main", and the error you would get names
# neither cause.
git config --global init.defaultBranch main
```

```bash
# Your stacks belong in version control from the first one.
cd ~/docker

# -b main names the first branch explicitly. The setting above would
# do it anyway; writing it here means this block works even if you
# skipped a line.
git init -b main
git add whoami/compose.yaml
git commit -m "whoami: first compose stack"
```

**How you know it worked:**

```bash
# One commit, by you, on a branch called main. That last part
# matters in 6.8, so check it now rather than debugging a push.
git log --oneline --decorate
```

Expect a single line ending in your commit message, with `(HEAD -> main)`
in it. **If it says `master` instead of `main`**, the repository was created
before the config took. Rename the branch, which is safe and instant:

```bash
git branch -M main
```

Leave it local for now. In lesson 6.8 it gets a remote, on a Git server
you're about to build.

Tidy up before moving on:

```bash
cd ~/docker/whoami && docker compose down
```

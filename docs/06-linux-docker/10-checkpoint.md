---
title: "6.10 Checkpoint: a server that hosts things"
sidebar_position: 10
---

# 6.10 Checkpoint: a server that hosts things

Run these on UBNT01, over SSH, inside tmux.

```bash
# Identity and address.
hostname
ip -brief addr
ip route

# DNS points at the domain controller, and the domain answers.
resolvectl status | head -20
dig +short lab.internal
dig -t SRV _ldap._tcp.lab.internal +short
dig +short git.lab.internal

# The server is hardened.
sudo sshd -T | grep -E "^(passwordauthentication|permitrootlogin|pubkeyauthentication)"
sudo ufw status verbose

# Containers are running and restart on their own.
docker ps
docker compose -f ~/docker/gitea/compose.yaml ps

# The proxy is healthy and the site answers by name.
sudo nginx -t
curl -I http://git.lab.internal

# tmux is where you're working.
tmux ls
```

## Pass criteria

- [ ] UBNT01 answers to that name at `10.10.10.20`, statically, with
      DNS pointing at DC01 (lesson 6.1)
- [ ] The SRV lookup for the domain succeeds from this Linux machine,
      proving it can find the domain (lesson 6.1)
- [ ] You can SSH in from your own computer, and you have an
      `~/.ssh/config` entry so it's one short command (lesson 6.2)
- [ ] You started a tmux session, closed your terminal on purpose, and
      reattached to find your work still running (lesson 6.2)
- [ ] `sshd -T` reports `passwordauthentication no`, and you got in
      with a key (lesson 6.3)
- [ ] `ufw` is active, SSH and web are allowed, everything else
      inbound is denied (lesson 6.3)
- [ ] You can explain what a container is, and how it differs from a
      VM, without using the phrase "lightweight VM" (lesson 6.4)
- [ ] You can say why the `docker` group is effectively root
      (lesson 6.4)
- [ ] Your compose stacks live in `~/docker/<name>/compose.yaml`, are
      published to `127.0.0.1`, and are under Git (lesson 6.5)
- [ ] You can say what a volume is for, and which directory holds
      Gitea's real data (lessons 6.5, 6.6)
- [ ] `git.lab.internal` resolves from DNS you configured, and
      loads Gitea through nginx (lessons 6.6, 6.7)
- [ ] You ran `nginx -t` before reloading, and you know why that order
      matters (lesson 6.7)
- [ ] Your journal's `origin` is now your own Gitea, the GitHub remote
      is kept as `github`, and you have pushed to both (lesson 6.8)
- [ ] You cloned the journal from a second machine and it matched
      (lesson 6.8)
- [ ] Journal written and pushed, Module 6 ticked, UBNT01 snapshotted
      (lesson 6.9)

## What you have now

Two servers, one Windows and one Linux, on a network you designed, with
a domain, a directory, containers, a reverse proxy, and your own source
control holding the record of how you built all of it.

Module 7 is where the lab stops looking improvised. You'll build a
certificate authority, issue certificates your own machines trust, and
turn every one of those "not secure" browser warnings into a padlock,
including the two you've collected so far on OPNsense and Gitea.

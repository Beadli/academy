---
title: "6.3 Operate and harden a Linux server"
sidebar_position: 3
---

# 6.3 Operate and harden a Linux server

Four things you'll do on every Linux server for the rest of your career:
install software, control services, read logs, and make it harder to
break into. This lesson is all four, and then Docker in 6.4 assumes you
have them.

## Software: apt

Ubuntu's package manager fetches software from repositories that are
signed and maintained, which is why you almost never download an
installer from a website on Linux.

```bash
# Refresh the catalogue of what's available. This changes nothing
# on your system; it just updates the list.
sudo apt update

# Install what's newer. -y answers yes to the confirmation.
sudo apt upgrade -y

# Install something specific.
sudo apt install -y htop

# What is this package, and is it installed?
apt policy htop
```

Run `htop` and press `q` to quit. You've just installed and used
software without visiting a single website, which is the point.

**`sudo`** runs one command as the administrator, `root`. Linux's model
is that you work as yourself and borrow privilege per command, and it's
the same discipline as the two-account habit from lesson 5.6, enforced by
the operating system rather than by your good intentions.

## Services: systemd

Anything that runs in the background is a **service**, managed by
`systemctl`:

```bash
# Is SSH running, and did it start cleanly?
systemctl status ssh

# The four verbs you'll use constantly.
sudo systemctl restart ssh
sudo systemctl stop ssh      # don't, right now: you're connected over it
sudo systemctl start ssh
sudo systemctl enable ssh    # start automatically at boot
```

`enable` versus `start` catches people out, so learn the difference now:
**start** runs it right now, **enable** makes it come back after a
reboot. A service that's started but not enabled works perfectly until
the machine restarts at 3am, which is a memorable way to learn it.

## Logs: journalctl

When something fails, the answer is almost always in the logs, and
systemd collects them all in one place:

```bash
# Everything this service has said, newest at the bottom.
journalctl -u ssh

# The last 50 lines, which is usually what you want.
journalctl -u ssh -n 50

# Follow live, like watching a log scroll. Ctrl+C to stop.
journalctl -u ssh -f

# Everything since boot, at error level or worse. Start here when
# a machine is misbehaving and you don't know where to look.
journalctl -b -p err
```

That last command is worth memorising. "What has gone wrong since this
machine started" is the right first question, and it's one line.

## Hardening, part one: keys instead of passwords

Password authentication over SSH is the single most attacked thing on
the internet. You saw what that looks like in lesson 2.2, in a log full
of failed root logins. The fix is to stop accepting passwords at all.

An SSH key is a pair of files: a private key that never leaves your
machine, and a public key you hand out. Anyone holding the public key
can verify you without ever learning your secret.

**On your own computer**, not the server:

```bash
# Generate a key pair. ed25519 is the modern default: short, fast,
# and strong. -C is just a label so you can tell keys apart later.
ssh-keygen -t ed25519 -C "sam@laptop"
```

Accept the default location. It offers a passphrase, and you should set
one: it encrypts the private key on disk, so a stolen laptop isn't a
stolen server.

Now copy the public half to the server:

```bash
# Linux and macOS have a tool for exactly this.
ssh-copy-id sam@10.10.10.20
```

```powershell
# Windows has no ssh-copy-id, so do it by hand. This reads your
# public key and appends it to the server's authorized_keys file.
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh sam@10.10.10.20 `
  "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Test it before you go further. Open a **new** terminal and connect:

```bash
ssh sam@10.10.10.20
```

It should let you in without asking for your account password. (It may
ask for your key's passphrase, which is a different thing.)

:::warning[Keep the old session open]
Do not close your working SSH session until key login is proven in a
second one. The next step switches passwords off entirely, and if your
key isn't working you'll have locked yourself out of a machine whose
console you'd then have to open in the hypervisor. Two windows, always,
when changing how you authenticate.
:::

Now turn passwords off:

```bash
sudo nano /etc/ssh/sshd_config
```

Find and set these three, removing any leading `#`:

```text
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
```

Then reload and test from your second window:

```bash
# Check the file for syntax errors BEFORE restarting. If this
# prints nothing, the config is valid.
sudo sshd -t

sudo systemctl restart ssh
```

## Hardening, part two: the firewall

Your server should answer only for things it's actually offering.
Ubuntu's `ufw` is a friendly front end to the kernel's firewall:

```bash
# Allow SSH FIRST. Enabling a firewall that blocks your own
# connection is a classic, and it locks you out instantly.
sudo ufw allow OpenSSH

sudo ufw enable
sudo ufw status verbose
```

Read the status output: everything inbound is denied except what you
allowed, everything outbound is permitted. That's the same default-deny
shape your OPNsense firewall uses at the network edge, applied at the
host. Defence in layers means the boundary isn't the only thing standing
between an attacker and this machine.

You'll open more ports as you add services, and each time it should feel
like a decision.

:::tip[In GRC language]
The two changes you just made are among the most-audited controls in any
framework. Key-based authentication with passwords disabled speaks to
**IA-2** (identification and authentication) and **IA-5** (authenticator
management); restricting who may connect and from where is **AC-17**,
remote access. The host firewall is **SC-7** again, one layer in from
where you met it in lesson 4.6.

Notice what makes them assessable: `sshd_config` states the policy,
`ufw status` shows the enforcement, and your journal records when and
why you changed them. Configuration plus evidence plus rationale is what
an assessor is asking for, and Module 16 will have you produce exactly
that for this machine.
:::

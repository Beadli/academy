---
title: "6.2 SSH in, and live in tmux"
sidebar_position: 2
---

# 6.2 SSH in, and live in tmux

Working at a VM's console window is fine for installing an operating
system and miserable for everything else: no copy and paste worth having,
a fixed window size, and you have to keep the hypervisor in front of you.
Real server work happens over SSH, from your own machine.

This is also where lesson 1.5 finally pays off. I promised you'd meet
tmux for real once your lab had a server in it. It does now.

## Connect

SSH is built into Windows, macOS, and Linux, so open a terminal on your
own computer. On Windows that's PowerShell or Terminal, and no extra
software is needed.

```bash
# ssh <username>@<address>, using the account you created during the
# Ubuntu install.
ssh sam@10.10.10.20
```

The first time, it warns that the host's authenticity can't be
established and shows a fingerprint. That's not a fault: SSH is telling
you it has never seen this server before and can't vouch for it. Type
`yes`. It records the fingerprint, and from now on it will warn you
loudly if the answer ever changes, which is how you'd notice something
impersonating your server.

You're in. Same shell, better window.

## Start living in tmux

Before you do anything substantial, start a tmux session. This is the
habit lesson 1.5 asked you to file away:

```bash
# Ubuntu Server usually ships with tmux. This installs it if yours
# didn't, and does nothing if it's already there.
sudo apt install -y tmux

# Start a named session. The name matters when you have more than one.
tmux new -s lab
```

Now do something long-running, and interrupt yourself deliberately:

```bash
# A slow command, so there's something to lose.
ping -c 300 1.1.1.1
```

While it runs, **close your terminal window entirely.** Not Ctrl+C, not
`exit`. Close the window, the way a dropped wifi connection would.

Then reconnect and look:

```bash
ssh sam@10.10.10.20

# What sessions are alive on this server?
tmux ls

# Reattach to yours.
tmux attach -t lab
```

Your ping is still counting. It never stopped, because it was never
attached to your terminal in the first place; it was attached to a
session living on the server. Press Ctrl+C to stop it.

That's the whole value, and it's why every long operation in the rest of
this course should start with `tmux attach -t lab` or `tmux new -s lab`.
Kernel upgrades, database restores, anything that takes twenty minutes:
inside tmux, a dropped connection costs you nothing.

The rest of tmux, when you want it:

```bash
# Detach on purpose, leaving everything running: Ctrl+b, then d
# Reattach:        tmux attach -t lab
# List sessions:   tmux ls
# Split the window into two panes: Ctrl+b, then %
# Move between panes:              Ctrl+b, then arrow keys
```

Ctrl+b is tmux's "listen to me" key. Everything else is one keystroke
after it.

## Make the connection yours

Two small things that make daily use pleasant enough that you'll
actually do it.

**Give the server a short name on your own machine.** On your computer,
not the server, create or edit `~/.ssh/config` (on Windows that's
`C:\Users\you\.ssh\config`):

```text
Host ubnt01
    HostName 10.10.10.20
    User sam
```

Now `ssh ubnt01` is the whole command. Add entries as your lab grows and
you'll never type an address again.

**Know how to get out.** `exit` closes the SSH session. If a connection
freezes and won't respond to anything, press `Enter`, then `~`, then
`.` which is SSH's own escape sequence, and it kills the connection when
Ctrl+C can't.

From here on, assume every lesson means "over SSH, inside tmux" unless
it says otherwise.

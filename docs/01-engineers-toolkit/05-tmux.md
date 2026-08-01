---
title: "1.5 tmux, the terminal that survives"
sidebar_position: 5
---

# 1.5 tmux, the terminal that survives

Here's a disaster you haven't had yet, described so you'll recognize it
later. You're connected over SSH to a server, forty minutes into a
system upgrade, and your wifi hiccups. The connection drops, and the
shell you were working in dies with it, taking the half-finished
upgrade with it. I've had a kernel upgrade over SSH saved from exactly
this fate by the tool in this lesson, and that single save justified
every minute I'd spent learning it.

tmux fixes this by cutting the cord between "your terminal window" and
"the session doing the work." The session runs on the machine itself,
inside tmux. Your window is just a view of it. Close the laptop, lose
the wifi, drive home, reconnect: the session is still there, still
working, exactly where you left it.

## The five keystrokes

```bash
# Start a named session.
tmux new -s lab

# You're now inside tmux. Work normally. Then detach, leaving
# everything running: press Ctrl+b, release, then press d.

# Later (even from a different machine), see what's running
# and reattach:
tmux ls
tmux attach -t lab
```

Ctrl+b is the "attention, tmux" prefix; whatever you press next is the
command. `d` detaches. That plus `new`, `ls`, and `attach` is a
complete working knowledge. tmux can also split panes and juggle
windows, and you'll pick that up naturally or never need it.

## Practicing today, and an honest note for Windows users

tmux is a Linux and macOS tool.

On **macOS**, install and try it now: `brew install tmux`, start a
session, run `ping -c 100 example.com`, detach, reattach, and watch the
ping still going. That detach-while-running moment is the lesson.

On **Linux**, same thing: `sudo apt install tmux`.

On **Windows**, there's no native tmux, and I'm not sending you on a
WSL side quest for a tool you can't fully use until your lab exists.
Read this lesson, understand the idea, and file it. In Module 6 you'll
be SSHing from Windows into your own Ubuntu server, tmux will be
installed there, and the first thing you'll do after connecting is
`tmux new -s lab`. The habit starts the day the server does.

Why teach it now, then? Because the day you first need tmux is the
worst day to learn it. You'll be mid-disaster, and "I know exactly what
to type" beats "I remember there was a thing for this."

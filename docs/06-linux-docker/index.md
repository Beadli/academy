---
title: "Module 6: Linux server and Docker"
sidebar_position: 0
---

# Module 6: Linux server and Docker

<div className="stackLine">

Ubuntu Server · Docker · Compose · Gitea · Nginx · PostgreSQL

</div>

Your lab has a Windows half. Now it gets its Linux half, and by the end
of this module that machine will be doing real work: running containers,
serving a website, and hosting the Git server your engineering journal
lives on.

That last part is the one I'd point at. In Module 1 you pushed your
journal to somebody else's server because you didn't have one. Today you
build your own, move your notes onto it, and stop renting. It's the same
progression every organization goes through in reverse, and doing it
yourself is how the words "self-hosted" stop being abstract.

What's in it:

- **6.1** build UBNT01 and put it on the domain's network
- **6.2** SSH in from your own machine, and live in tmux
- **6.3** operate and harden a Linux server
- **6.4** Docker: what a container actually is
- **6.5** Compose: a stack described in a file
- **6.6** Gitea: your own Git server
- **6.7** give it a real name: DNS and a reverse proxy
- **6.8** move your journal home
- **6.9** open the database your Git server is running on
- **6.10** journal entry
- **6.11** checkpoint

**Tier 1 and up.** UBNT01 wants 6 GB of RAM and, like DC01, it stays
running for the rest of the course. Modules 10, 12, and 13 all install
things onto this machine, so it's worth building carefully.

Budget two evenings. The Linux fundamentals in 6.2 and 6.3 are the part
worth slowing down for if this is your first server; everything after
them assumes you can move around a machine without a graphical desktop.

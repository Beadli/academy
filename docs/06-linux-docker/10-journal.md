---
title: "6.10 Journal: the Linux half exists"
sidebar_position: 10
---

# 6.10 Journal: the Linux half exists

Lesson 0.4 predicted that by about now you'd be writing these without
being told. If that's true, write yours and skip the prompts below. If
it isn't yet, that's fine, and here they are.

**Permanent note.** Add to `Projects/lab-network.md`, or start
`Projects/ubnt01.md`:

- UBNT01 at `10.10.10.20`, its username, and that it authenticates by
  SSH key with passwords disabled
- Where `~/docker` lives and which stacks are in it
- The Gitea URL, your admin account, and where the data directory sits
- The DNS record you added, so future-you knows records are added on
  DC01 and not somewhere on the Linux box

**Daily note**, four headings.

Under **what I did**: the server built, hardened, containerised, and
turned into the home for your own notes.

Under **what broke**: netplan indentation is the classic, and so is
enabling `ufw` before allowing SSH. If you locked yourself out and
recovered through the hypervisor console, write down exactly how,
because that's the recovery path for every future lockout.

Under **what I learned**: explain the difference between a container and
a virtual machine in your own words, and why services in this lab
publish to `127.0.0.1` instead of `0.0.0.0`. Those two answers come up
in interviews constantly.

Under **open questions**: "how do I get a certificate my machines
actually trust" is the right one to be sitting with, and Module 7 is
entirely about it.

Then commit and push, and notice that this push goes somewhere new:

```bash
cd ~/git/lab-journal
git add -A
git commit -m "journal: module 6, UBNT01 built and hosting my notes"
git push                 # to your own server now
git push github main     # and the off-lab copy
```

Tick Module 6 in `Projects/lab-progress.md`, and snapshot UBNT01 as
`docker-and-gitea`. Unlike DC01, this machine is safe to snapshot
freely; the warning in lesson 5.12 was specific to domain controllers.

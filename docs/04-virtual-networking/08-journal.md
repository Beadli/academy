---
title: "4.8 Journal: the network exists"
sidebar_position: 8
---

# 4.8 Journal: the network exists

This entry is different from the others: part of it is reference
material you'll come back to for the rest of the course, so give it a
little more care than usual.

**Make a permanent note, not a daily one.** In your vault, create
`Projects/lab-network.md` and put in it:

- The addressing table from lesson 4.3, edited to match what you
  actually built
- Which hypervisor network is which segment, by its real name
  (`VMnet8`, `VMnet2`, `lab-nat`, whatever yours are called), and
  whether DHCP is on or off for each
- Your gateway address, read from `ip route` rather than assumed
- Tier 2: the firewall's addresses on both sides, and where you wrote
  its root password
- Tier 3: whether you set up Tailscale, and what it can reach

Then today's daily note, four headings as usual:

Under **what I did**: the networks you created, Kali imported, and for
Tier 2 the firewall built and both segmentation tests run.

**Save the capture from lesson 4.7.** Paste the Follow-TCP-Stream text of
your plaintext HTTP request into the entry, under a heading you'll be able
to find again. Lesson 7.6 asks you to run the same capture against your
own HTTPS site and put the two side by side, and that comparison is much
more convincing when the first half is your own traffic from weeks
earlier rather than a screenshot from a book.

Under **what broke**: something in this module usually does. A VM on the
wrong virtual switch, DHCP handing out an address from the range you
thought you'd disabled, the firewall's interfaces assigned backwards.
Write the symptom *and* how you worked out which of the four questions
from 4.1 was unanswered. That reasoning is the actual skill.

Under **what I learned**: explain, in your own words, the difference
between NAT and host-only, and why this course refuses to use bridged.
If you can teach it to the page you'll be able to teach it in an
interview.

Under **open questions**: "what happens to my lab's DNS when the domain
controller arrives" is an excellent one, and Module 5 answers it
directly.

```bash
cd ~/git/lab-vault
git add -A
git commit -m "journal: module 4, lab network built"
git push
```

Tick Module 4 in `Projects/lab-progress.md`.

---
title: "3.6 Journal: the lab exists"
sidebar_position: 6
---

# 3.6 Journal: the lab exists

Daily note, four headings, and this one deserves a good entry, because
today the lab stopped being theoretical.

Under **what I did**: hypervisor and version installed, which ISOs you
collected, and the full arc of `practice01`: built, installed,
snapshotted, destroyed, restored, deleted. Write the arc out; it reads
like a story because it was one.

Under **what broke**: the Broadcom portal counts, and so does anything
the Ubuntu installer did that surprised you, any Hyper-V or
performance warning, any checksum that didn't match on the first try.
If the reboot-after-rm failed differently than the lesson described,
write down the exact error you saw; that's your version of the truth,
and it's worth more than mine.

Under **what I learned**: explain in your own words why the snapshot
revert brought back a machine you'd destroyed. Where was the intact
copy living? If you can answer that, you understand what a snapshot
is; if you can't, that's a fine open question.

Under **open questions**: how the VM got an IP address without you
configuring one is an excellent thing to wonder about, and Module 4
exists to answer it. So is "what's the difference between reverting a
snapshot and restoring a backup," which Module 15 takes seriously.

Commit and push:

```bash
cd ~/git/lab-journal
git add -A
git commit -m "journal: module 3, first VM built, killed, and resurrected"
git push
```

Tick Module 3 in `Projects/lab-progress.md`.

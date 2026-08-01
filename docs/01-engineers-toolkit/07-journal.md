---
title: "1.7 Journal: first entry in the vault"
sidebar_position: 7
---

# 1.7 Journal: first entry in the vault

This is the first journal entry that lives where journal entries will
live from now on. Create today's daily note in Obsidian (calendar icon,
or Ctrl+P then "daily note") and fill in the four sections about this
module. Some prompts, if the blank headings stare back:

Under **what I did**: which tools you installed, in what order, and the
one that took longest.

Under **what broke**: something did. An installer, an auth flow, a
command that failed the first time. Write what happened and how it
ended, even if the ending was "typo, found it in five minutes." You're
building the reflex of recording failure without embarrassment, because
in this field failure is data.

Under **what I learned**: one thing about Git's mental model, in your
own words. Explaining it to the page is how you find out whether you
understood it.

Under **open questions**: anything that still feels like magic. Candid
entries here become satisfying to cross off later. "Why does Git need a
staging step at all?" is a great one; Module 9 makes the answer obvious.

Then close the loop with the rhythm from this module:

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 1 complete"
git push
```

Also tick Module 1 in `Projects/lab-progress.md` while you're in there.
Watching that list fill up is a feature, not vanity.

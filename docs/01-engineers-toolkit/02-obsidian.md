---
title: "1.2 Obsidian and the starter vault"
sidebar_position: 2
---

# 1.2 Obsidian and the starter vault

Obsidian is a Markdown editor with two properties that matter for us: it
stores notes as ordinary `.md` files in an ordinary folder (no database,
no cloud lock-in), and it can link notes to each other, which slowly
turns a pile of notes into a personal reference manual. I keep my entire
lab's knowledge in it, and the number of times a six-month-old note has
saved my evening is the reason this lesson exists.

Fair warning: Obsidian's out-of-box experience is a blank purple void,
and its community will cheerfully bury you in plugin recommendations.
Ignore all of that. You're starting from a working vault I set up for
you, shaped like my real one, and we enable exactly two plugins.

## Install Obsidian

Download it from [obsidian.md](https://obsidian.md) for your OS and
install it like any app. It's free for personal use, no account needed.
Skip the sync and publish upsells; Git will do our syncing, for free,
with skills you need anyway.

## Get the starter vault

Download the vault from the course repository:
[github.com/beadli/starter-vault](https://github.com/beadli/starter-vault),
green **Code** button, **Download ZIP**. Unzip it somewhere sensible and
rename the folder to `lab-journal`. On my machine that's
`~/git/lab-journal`; `Documents\lab-journal` is fine on Windows.

In Obsidian: **Open folder as vault**, pick `lab-journal`, and say yes to
trusting the vault. Have a look around. The README explains what goes
where, and there's an example daily note in `Journal/` showing what a
filled-in day looks like.

## Turn on the two plugins

Settings (the gear, bottom left) > **Core plugins**. Make sure these two
are on:

- **Daily notes**, which creates today's note with one click
- **Templates**, which fills it from `Templates/Daily.md`

The vault ships with both already configured to use the right folders,
so there's nothing else to set. Click the calendar icon (or Ctrl+P, then
"daily note") and today's note should appear in `Journal/`, pre-filled
with four headings: what I did, what broke, what I learned, open
questions.

Those four headings are the whole method. The example note shows why
"what broke" is the section future-you reads most.

## Move your Module 0 entry in

Copy the `module-0.md` file from lesson 1.1 into the `Journal/` folder.
Congratulations, your journal has history. Then open
`Projects/lab-progress.md`, tick Module 0, and fill in the "My setup"
section from it. That page becomes your progress map for the whole
course.

Delete `Journal/example-day.md` once you've written a real entry of your
own. It's scaffolding, not furniture.

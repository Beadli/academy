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

Download the starter vault from GitHub:
[github.com/Beadli/starter-vault](https://github.com/Beadli/starter-vault),
green **Code** button, **Download ZIP**.

You'll get a file called `starter-vault-main.zip`. That `-main` is the
branch name, which GitHub tacks on to every ZIP it makes; it means
nothing here. Unzip it somewhere sensible and you'll have a folder
called `starter-vault-main`.

**Rename that folder to `lab-journal`.** On my machine it ends up at
`~/git/lab-journal`; `Documents\lab-journal` is fine on Windows. The name
is yours to choose, but the rest of the course says `lab-journal` when it
needs to name your vault, so following along is easier if you match it.

In Obsidian: **Open folder as vault**, pick `lab-journal`, and say yes to
trusting the vault.

Open `Home` first. It's the landing page: what each folder is for, what
the four daily headings mean, and links through to the rest. The coloured
boxes in it are Obsidian *callouts*, which are just Markdown with a
marker on the first line, and you'll meet them again in your own notes
whenever something deserves to stand out.

Then have a look around. There's an example daily note in `Journal/`
showing what a filled-in day looks like, including the wrong turn its
author took before finding the answer.

## Turn on the two plugins

Settings (the gear, bottom left) > **Core plugins**. Make sure these two
are on:

- **Daily notes**, which creates today's note with one click
- **Templates**, which fills it from `Templates/Daily.md`

The vault ships with both already configured to use the right folders,
so there's nothing else to set. Click the calendar icon (or Ctrl+P, then
"daily note") and today's note should appear in `Journal/`, named for
today's date and pre-filled with four headings: what I did, what broke,
what I learned, open questions.

Those four headings are the whole method. The example note shows why
"what broke" is the section future-you reads most.

Above them sits a small panel with **date**, **module** and **tags**.
That's Obsidian's *properties*, and in the file itself it's a block of
plain text at the very top between two `---` lines. Fill in the module
number as you go. It costs a second and it means that in Module 17 you
can pull up every note from the week you built the domain, instead of
scrolling through months by date.

You'll notice the note has no heading of its own. That's deliberate:
Obsidian already shows the filename as the title, so a `# 2026-03-14` at
the top would just say it twice.

## Move your Module 0 entry in

Copy the `module-0.md` file from lesson 1.1 into the `Journal/` folder.
Congratulations, your journal has history. Then open
`Projects/lab-progress.md`, tick Module 0, and fill in the "My setup"
section from it. That page becomes your progress map for the whole
course.

Delete `Journal/example-day.md` once you've written a real entry of your
own. It's scaffolding, not furniture.

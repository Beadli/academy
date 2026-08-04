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

## Later: making Obsidian yours

:::note[Not today]
Everything below this line is optional and none of the course depends on
it. Come back in a few weeks, once you've written enough notes to know
what actually annoys you. That order matters, and the next paragraph
explains why.
:::

I told you at the top of this lesson to ignore the plugin firehose, and I
meant it. Here's the reasoning, because "ignore it" without a reason is
just another opinion to argue with.

A plugin is a solution. Installing one before you have the problem gives
you settings to maintain, a thing that can break on update, and no
benefit. Almost everyone who quits Obsidian in week two quit because they
spent week one configuring it instead of writing in it. So: write first.
When something starts to grate, come back and fix that specific thing.

### First, the security decision you're about to make

Obsidian ships with **Restricted mode** turned on, which disables every
community plugin. To install one you have to turn it off, and Obsidian
will make you confirm.

That prompt is not a formality, and since you're taking a security
course, it's worth reading it as one:

**Community plugins are third-party code that runs inside Obsidian with
full access to your vault and to the network.** Not a sandboxed
extension. A plugin can read every note you've written, including the
lab addresses and the "what broke" entries, and it can make outbound
connections. The Obsidian team reviews submissions, but review is not
the same as a guarantee, and a plugin that was fine last year has a new
owner this year.

This is your first **supply chain** decision in the course and it will
not be your last. The term means the chain of other people's code that
ends up running on your machine: every container image you pull, every
package you install, every bit of automation you copy off the internet.
You will do all three before Module 7, and the question is the same one
you're answering right now. Module 13 makes it explicit, when you meet a
scanner and have to work out what it's really telling you.

:::tip[Four questions before you install anything]
1. **How many people use it?** The plugin browser shows a download count.
   Very low numbers mean very few eyes on the code.
2. **When was it last updated?** An abandoned plugin breaks on the next
   Obsidian release, and nobody will fix it.
3. **What happens to my notes if I remove it?** This is the important
   one. Prefer plugins that read and write ordinary Markdown, so
   uninstalling leaves plain text behind. Avoid anything that stores your
   content in a format only it can read.
4. **Do I have the problem it solves?** If you can't name the annoyance
   in one sentence, you don't need it yet.
:::

Question 3 is the one people skip, and it's the difference between a tool
and a trap. Everything I suggest below passes it.

### Turning restricted mode off

Settings (the gear, bottom left) > **Community plugins**. Turn restricted
mode off, then **Browse**, search, **Install**, and then **Enable**,
which is a separate click people miss. An installed-but-not-enabled
plugin does nothing and looks broken.

### The shortlist

Roughly in the order the problems tend to show up. Add one, use it for a
week, then consider the next. Installing all six in one evening is the
failure mode this whole section is trying to prevent.

| Plugin | The annoyance it fixes | When it usually bites |
| --- | --- | --- |
| **Calendar** | You want to see the month, and jump to a day, without hunting through the file list | Once `Journal/` has thirty-odd notes in it |
| **Obsidian Git** | Committing by hand at the end of every session, and forgetting | After Module 1, and read the warning below first |
| **Tasks** | Your open questions are scattered across dozens of daily notes with no way to see them together | Around Module 4 or 5 |
| **Dataview** | You want your progress page to build itself from what's already in your notes | When maintaining `lab-progress.md` by hand starts feeling silly |
| **Code Styler** | Code blocks are hard to read and you can't copy them cleanly | Module 2, once you're pasting real scripts in |
| **Tag Wrangler** | You want to rename a tag you've used ninety times without editing ninety files | Whenever your tags have drifted |

:::warning[Obsidian Git, and why not yet]
It automates exactly the rhythm lesson 1.3 teaches you by hand, so it
looks like an obvious shortcut. Take the shortcut too early and you never
learn what `git status` is telling you, and the first time it reports a
conflict you'll have no idea what it wants.

Learn the commands first. Automate them once they're boring. That order
is not me being purist about it: automation you don't understand is
something you can't fix, and you'll meet that lesson properly in Module
10 with Ansible.
:::

Two of these pay off immediately because of choices already made in your
vault. **Tasks** reads the `- [ ]` checkboxes under "Open questions",
which is why the template uses checkboxes there rather than bullets.
**Dataview** reads the `module:` and `tags:` properties at the top of
each daily note, which is why they're there. Fill those in as you go and
the tools have something to work with when you arrive.

### Modifications, no plugins required

These are settings, so nothing to install and nothing to trust. All of
them are under the gear.

**Appearance.** Set light or dark to taste, and there's a font size
slider. If your notes look like a wall of text stretching the full width
of a wide monitor, the setting you want is **Readable line length** under
Editor, which caps the column at something a human eye can track.

**Editor.** Turn on **line numbers** if you're pasting scripts in and
want to talk about them. **Fold headings** and **fold indent** let you
collapse sections, which is what stops a long project note becoming
unnavigable.

**Files and links.** Set where new notes are created, so a stray Ctrl+N
doesn't scatter files into the vault root. Point attachments at a folder
too, or every screenshot you paste lands beside your notes.

**Hotkeys.** The one worth setting on day one is a key for the daily
note, so you never go looking for the calendar icon. Search the hotkey
list for "daily" and assign whatever your hands like.

**Core plugins.** You turned on two. The list has more, they're written
by the Obsidian team rather than third parties, and they're free of the
trust question above. **Outline** gives you a table of contents for long
notes, **Bookmarks** pins the pages you open constantly, and **Word
count** is quietly motivating. Newer versions also ship **Bases**, which
turns notes into a table view you can filter; if your Settings list has
it, it's worth ten minutes once your `Projects/` folder has a few pages
in it.

### What I'd actually do

If you want one recommendation rather than a menu: install nothing today.
Set Readable line length, give the daily note a hotkey, and go write
notes. When you hit the first genuine annoyance, come back to the table
and fix that one thing.

That's the same instinct the rest of this course runs on. Understand the
problem, then reach for the tool.

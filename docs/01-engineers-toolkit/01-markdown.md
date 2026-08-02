---
title: "1.1 Note-taking with Markdown"
sidebar_position: 1
---

# 1.1 Note-taking with Markdown

Everything you write for the rest of this course goes into notes: what
you built, what broke, and how you fixed it. Before the note-taking app
arrives in the next lesson, you need the format those notes are written
in, and it takes about twenty minutes to learn all of it.

That format is **Markdown**: plain text with a little punctuation that
means something. `**bold**` renders as **bold**, a line starting with
`#` becomes a heading, and the file stays perfectly readable even if
nothing is rendering it. That last property is why it won. Your notes,
this course, GitHub READMEs, and half the documentation on the internet
are all Markdown.

You don't need any special software today. Notepad, TextEdit, or
whatever editor you already have is fine; the app that makes these
notes searchable and linkable comes in lesson 1.2.

## The whole syntax you need

````markdown
# A heading
## A smaller heading

Plain text is just plain text. Leave a blank line between paragraphs.

- A bullet point
- Another one
  - Indent two spaces for a sub-point

1. Numbered lists
2. Number themselves, mostly

**bold** and *italic*

[a link](https://example.com)

`inline code` for commands and filenames mid-sentence

```bash
# A fenced code block, for anything longer than one command.
# The word after the backticks (bash, powershell) turns on
# syntax coloring.
echo "like this"
```
````

That's it. There are more features (tables, quotes, footnotes) and you'll
absorb them when you meet them. Don't study Markdown; use it.

## Why plain text, though

Because in this field, plain text survives everything. Word documents
need Word. Notion needs Notion's servers to stay in business. A `.md`
file opens on any machine you'll ever touch, diffs cleanly in Git (which
matters in lesson 1.3), and will still open in thirty years. Every config
file, every script, and every log you'll meet in this course is plain
text too, so you might as well live there.

## Do this now

Take the Module 0 journal entry you wrote in lesson 0.5 and rewrite it as
a Markdown file called `module-0.md`. Give it a heading, put your four
facts (why, machine, tier, hours) under sub-headings, and format your RAM
and disk numbers as `inline code`. Any text editor works; Notepad works.

Keep the file next to your original notes. In the next lesson it gets a
proper home.

---
title: "11.3 Context: teaching it your environment once"
sidebar_position: 3
---

# 11.3 Context: teaching it your environment once

Lesson 11.2 said an agent is a widely-read colleague with no memory of your
environment. This lesson fixes the second half.

Every agent has some notion of a **context file**: a document it reads at the
start of every session, describing the project it is working on. In Claude Code
that file is `CLAUDE.md`. Other tools name it differently and do the same job.

Without one, you re-explain your lab every session. With one, you explain it
once.

## Generate a starting point, then rewrite it

Claude Code will draft one for you:

```text
/init
```

It reads the directory and writes a `CLAUDE.md` describing what it found.

**Then rewrite it, because the generated version describes structure and the
useful version describes decisions.** An agent can see your folder layout by
looking. What it cannot see is why you did things the way you did.

## What actually belongs in it

Here is a context file for your journal vault, in the shape that works:

```markdown
# Lab journal

My engineering journal for the Beadli Lab Academy course. Plain Markdown,
in an Obsidian vault, under Git.

## Structure

- `Journal/` daily notes, one per working day, four fixed headings
- `Projects/` notes about a thing rather than a day, edited over months
- `Resources/` cheatsheets and scripts

## Conventions

- Daily notes use the template in `Templates/Daily.md`. Do not change
  the four headings.
- Machine names are uppercase: DC01, UBNT01. Addresses are 10.10.10.x.
- Never put passwords or keys in these files, even in examples.

## How I want you to work here

- Ask before creating new top-level folders.
- When you edit a note, keep my wording. Do not rewrite my sentences
  to be tidier.
- If I ask for a summary of a lab session, write it in first person,
  past tense, and keep the dead ends in. The mistakes are the useful part.
```

Read that back. Almost none of it is structure. It is **conventions, boundaries
and preferences**, which is exactly the category an agent cannot infer and will
otherwise get wrong in a plausible-looking way.

:::tip[Write the rules you find yourself repeating]
The way to build a good context file is not to sit down and write one. It is to
notice, during a session, the moment you correct the same thing twice.

"No, keep my wording." "No, that machine is DC01 not dc-01." "No, do not put
that in the root."

Every one of those corrections is a line that belongs in the file. Add it while
you are annoyed, because that is when you know it matters.

Mine grew that way over months and it is the highest-value file in my setup.
:::

## Keep it short

A context file that is four screens long is one nobody maintains and the agent
weights poorly. Aim for something a new colleague could read in two minutes.

If it is getting long, that is usually a sign the content belongs in the
project's real documentation instead, with the context file pointing at it.

## Where it lives, and the scoping decision

Context files usually work at two levels, and the distinction matters:

**Project level**, committed to the repository. Conventions for this codebase,
shared with anyone who clones it. Your teammates get the same rules.

**Personal level**, in your home directory, applying everywhere. How *you* want
to be worked with, regardless of project.

The split is the same instinct as `.gitignore` versus your global git config.
Things about the project go in the project. Things about you go with you.

:::warning[A context file is instructions, and it is in your repository]
Anyone who can commit to the repository can edit the file that tells your agent
how to behave. On a shared project, that is a real consideration and lesson
11.7 comes back to it.

For now, the habit: **read the context file when you clone a repository**, the
same way you would read a Makefile before running `make`. It is executable
instruction, not documentation.
:::

## Prove it works

Add a deliberately checkable rule to your context file. Something like:

```markdown
- Always end a summary with a line beginning "Open questions:".
```

Then start a new session and ask for a summary of something. If the line
appears, the file is being read. If not, it is in the wrong place or the wrong
name, and better to find that out with a test than to spend a week wondering
why your conventions are being ignored.

## What this is really doing

You are writing down the tacit knowledge of your environment: the things you
know and have never said, because you have never had to say them to anyone.

That is a genuinely useful exercise even if you stop using agents tomorrow. A
new colleague needs exactly the same file, and most teams have never written
one.

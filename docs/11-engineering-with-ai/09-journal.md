---
title: "11.9 Journal: what you delegate and what you keep"
sidebar_position: 9
---

# 11.9 Journal: what you delegate and what you keep

**Make a permanent note.** In your vault, create `Projects/lab-ai.md` and
record:

- Which agent you are using, and where you run it from
- Where your context file lives, and the rules currently in it
- Which skills you have written, one line each on what they do
- Your deny list, and why each entry is on it
- **Your own line on what you will not delegate.** Lesson 11.7 gave mine.
  Yours should be yours, and writing it down before you need it is the point.

That last item is the one worth thinking about rather than copying. The moment
to decide what you will not hand over is not the moment you are tired and it
is offering to do it.

## Then today's daily note

Under **what I did**: what you set up, and one real task you used it for.

Under **what broke**: this module's failures are quieter than most. Nothing
crashes. What goes wrong is that something confidently wrong got past you, or
you caught it at the last second. Write down whichever happened, because that
is the calibration data.

If nothing went wrong, say so, and note how carefully you were actually
reading. Honest answers here are more useful than flattering ones.

Under **what I learned**: pick one.

- The gap between what you thought your lab looked like and what lesson 11.8
  found
- Where your reviewing attention actually goes, versus where you told yourself
  it goes
- Why prompt injection is the same shape as a problem you already met in
  Module 6

Under **open questions**: good ones here. Would you let this run unattended,
and what would have to be true first? What would you tell an employer who
asked whether you use these tools? Where is the line between using it to learn
faster and using it instead of learning?

That last question does not have a clean answer, and noticing that you are
somewhere on that line is more useful than deciding you are safely on one side.

## Write the entry with the agent, then read it properly

Fitting, and slightly uncomfortable, which is the point.

Use the skill from lesson 11.5 to draft this entry from your session. Then read
it against lesson 11.6's standard: does it sound like you, does it keep the
dead ends, does it contain any confident claim you have not checked?

**Notice how tempting it is to accept it.** That temptation is the single most
important thing this module has to teach you, and the only way to feel it is to
be in the situation.

Then close the loop:

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 11 complete"
git push
```

Tick Module 11 in `Projects/lab-progress.md`.

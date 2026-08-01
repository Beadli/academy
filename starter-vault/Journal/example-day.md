# Example day

This is what a filled-in daily note looks like. Delete this file once
you've written your own first entry.

## What I did

- Worked through Module 1, lessons 1.1 to 1.3
- Set up the vault and made my first three commits

## What broke (and how it ended)

- `git push` rejected with "authentication failed". The token I pasted
  had a trailing space from the clipboard. Re-pasted into a text editor
  first, trimmed it, worked.

## What I learned

- Git doesn't store versions of files, it stores snapshots of the whole
  folder. The mental model finally clicked.

## Open questions

- Why does Obsidian create a workspace.json that Git keeps flagging?
  (Answered in lesson 1.3: it's per-machine UI state, and it belongs in
  .gitignore.)

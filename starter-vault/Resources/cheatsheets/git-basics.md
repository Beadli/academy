# Git basics

The five commands that carry most of the daily work, from Module 1.

```bash
git status              # what changed since the last commit
git add -A              # stage everything that changed
git commit -m "note"    # take the snapshot, with a message
git log --oneline       # the history, one line per commit
git push                # send commits to the remote
```

And the two you need when something went sideways:

```bash
git diff                # exactly what changed, line by line
git restore <file>      # throw away uncommitted changes to a file
```

Write commit messages for future-you: "fix DNS forwarder note" beats
"update". Future-you is the only person who reads them, and they're
always in a hurry.

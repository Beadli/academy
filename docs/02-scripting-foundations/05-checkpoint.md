---
title: "2.5 Checkpoint: the toolbox test"
sidebar_position: 5
---

# 2.5 Checkpoint: the toolbox test

Prove the module stuck. Run these from your vault folder.

```bash
cd ~/git/lab-journal

# The three scripts exist where scripts live.
ls Resources/scripts/

# The PowerShell report landed in the vault (Windows students).
ls Resources/machine-report.md

# The bash script runs and ranks IPs. The top line of its output
# should be:   5 203.0.113.42
./Resources/scripts/failed-logins.sh Resources/scripts/auth.log

# The Python script reaches the live catalog and prints a count
# plus five dated entries. Windows: "python", per lesson 2.3.
python3 Resources/scripts/kev-check.py

# Committed and pushed, so the toolbox leaves the building too.
git status
git log --oneline -3
```

The bash check has a known-good answer on purpose: the sample log is
fixed, so `5 203.0.113.42` on top means your pipeline is correct, and
anything else means a stage is grabbing the wrong thing. Debug it
stage by stage, the way you built it.

If that line fails with an error mentioning `bash\r` or a stray `^M`
rather than printing a ranking at all, that's the line-endings trap from
lesson 2.2 and not your pipeline. `sed -i 's/\r$//' Resources/scripts/failed-logins.sh`
and try again.

## Pass criteria

- [ ] `failed-logins.sh` from lesson 2.2 ranks the sample log with
      `5 203.0.113.42` on top
- [ ] You modified it to report accepted logins, lesson 2.2's closing
      exercise, and can say what the output means
- [ ] `kev-check.py` from lesson 2.3 runs and prints the live catalog
      count and five newest entries
- [ ] You made at least one "make it yours" change to the Python
      script, as lesson 2.3 asked
- [ ] Windows students: `machine-report.md` is in the vault and the
      script survived lesson 2.1's execution-policy wall
- [ ] Linux/macOS students: you read the PowerShell script in lesson
      2.1 and can explain what `$disk.Free` is (an object property,
      not text)
- [ ] All three scripts are committed and pushed with your journal
      entry, the rhythm from lesson 1.3
- [ ] Module 2 is ticked in `lab-progress.md`, the habit from 1.7

All green? Then you read scripts now. Module 3 finally starts the lab:
hypervisor installed, first VM booted, and the fun begins.

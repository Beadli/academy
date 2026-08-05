---
title: "15.3 Restore it"
sidebar_position: 3
---

# 15.3 Restore it

**A backup you have not restored is a hypothesis.**

That sentence is the most useful thing in this module. Everybody agrees with
it and almost nobody acts on it, which is why "we had backups" appears so
often in incident write-ups, always followed by a reason they did not help.

This lesson is short, and it is the one that makes the previous one mean
something.

## Why untested backups fail

The failure modes are boring, which is exactly why they survive undetected
for years:

- The job was backing up an empty directory after somebody moved the data.
- It excluded the one folder that mattered, via a pattern nobody re-read.
- The database copy is a file that cannot be opened, which is lesson 15.4.
- The restore needs a password nobody wrote down.
- The restore works but takes eleven hours, and the RTO was two.
- The drive was full for six months and the job kept reporting success.

**Not one of those is detectable by looking at the backup job.** Every one is
obvious within minutes of an actual restore.

## The drill

Do it properly: destroy something, then bring it back, then prove the thing
you brought back is identical to what you lost.

**Record what you have first.** This is the step people skip, and without it
you cannot prove anything afterwards:

```bash
# A checksum of every file in a directory you are about to lose.
# Sorted, so the comparison later is meaningful.
cd ~
find docker -type f -exec sha256sum {} \; | sort -k2 > ~/before.txt

# How many files, so a truncated restore is obvious.
wc -l ~/before.txt
```

**Back it up:**

```bash
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password backup /home
```

Confirm you got `snapshot <id> saved`.

**Now break it.** Genuinely, not symbolically:

```bash
# Move it aside rather than deleting, the first time you do this.
# Lesson 15.8's instinct: leave yourself a way back that does
# not depend on the thing you are testing.
mv ~/docker ~/docker.moved-aside
```

**How you know the disaster happened:**

```bash
# Expect: No such file or directory
ls ~/docker
```

## Restore

```bash
# --target says where to write. Restoring somewhere OTHER than
# the original location is the safe habit: you compare first,
# then move it into place.
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password \
  restore latest --target /tmp/restore-test
```

**How you know it worked:**

```text
restoring <Snapshot 80d70c9c of [/home] at 2026-08-05 15:31:41 by root@ubnt01> to /tmp/restore-test
Summary: Restored 6 files/dirs (195.382 KiB) in 0:00
```

**Note where the files actually landed.** restic recreates the original
directory structure underneath your target, so a backup of `/home` restored
to `/tmp/restore-test` appears at `/tmp/restore-test/home/...`, not directly
in the target.

```bash
# Look, rather than assuming. This trips people up under
# pressure, which is exactly when you do not want surprises.
find /tmp/restore-test -maxdepth 3 | head
```

## Now prove it

This is the step that separates a restore from a successful restore.

```bash
cd /tmp/restore-test/home/sam    # substitute your username
find docker -type f -exec sha256sum {} \; | sort -k2 > ~/after.txt

# Compare. NO OUTPUT means every file is byte-for-byte identical.
diff ~/before.txt ~/after.txt && echo "IDENTICAL"
```

**Expect `IDENTICAL` and nothing else.** When I ran this drill, the checksums
before and after matched exactly:

```text
dc7df279f13d...  data/blob.bin
2a6c34228767...  data/docker/whoami/compose.yaml
535df1f76123...  data/notes.md
```

Same three hashes, before the deletion and after the restore.

**If `diff` prints anything**, read it carefully, because you have just found
a real defect in your backup strategy before it cost you anything:

- **Lines only in `before.txt`**: those files were not backed up. Check your
  paths and exclusions.
- **Lines only in `after.txt`**: you restored an older snapshot than you
  meant to, or files were created after the backup.
- **Same filename, different hash**: the content changed. If it is a database
  file, go straight to lesson 15.4, because that is exactly the problem it
  covers.

## Put it back

```bash
# Move the restored copy into place, then remove the aside copy
# once you are satisfied.
rm -rf ~/docker
mv /tmp/restore-test/home/sam/docker ~/docker
rm -rf ~/docker.moved-aside
```

**How you know it worked:**

```bash
# Your stacks are back and Docker can still read them.
ls ~/docker
cd ~/docker/whoami && docker compose config > /dev/null && echo "compose file valid"
```

## Time it, because RTO is a number

Lesson 15.1 had you write down an RTO. You have now performed a restore, so
you have data rather than an opinion.

```bash
# Run the restore again, timed.
time sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password \
  restore latest --target /tmp/restore-timing
```

Write the number in your journal next to your RTO.

**This is how RTO conversations actually go in a job.** Somebody asserts a
four-hour recovery target; somebody else points out the last full restore
took nine hours; and the gap between those is either a budget request or a
revised target. You cannot have that conversation without having timed a
restore.

Clean up: `sudo rm -rf /tmp/restore-timing /tmp/restore-test`

## Make this a habit, not an event

A restore test that happens once is a restore test that was true once.

Put a recurring reminder somewhere you will see it: **restore one thing,
monthly.** Not everything. One directory, chosen differently each time,
restored to a scratch location and checksummed. It takes five minutes and it
is the only evidence that any of this works.

**Write the date of each test in your journal.** That log is what an auditor
asks for in Module 16, and it is the difference between "we have backups" and
"we have backups and here is the evidence they restore".

## What you take from this

You destroyed real data, brought it back, and proved byte-for-byte that it
was the same data. You also have a measured restore time to check your RTO
against.

Your backups have stopped being a hypothesis. For files, at least: the next
lesson is about the data that needs more than a file copy.

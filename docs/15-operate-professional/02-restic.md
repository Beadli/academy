---
title: "15.2 A real backup, with restic"
sidebar_position: 2
---

# 15.2 A real backup, with restic

**restic** is a backup tool that does the three things that matter: it
encrypts everything before it leaves the machine, it deduplicates so repeat
backups are cheap, and it can write to a local disk or to cloud storage with
the same commands.

It is a single binary with no server component, which is why it suits a lab
and why plenty of small companies run it in production.

## Decide where the backup goes

This is the decision, and the tool is the easy part.

**It must not be UBNT01.** A backup on the machine it protects is a snapshot
with extra steps, which is lesson 15.1's whole argument.

| Option | Good for | Honest downside |
|---|---|---|
| **USB drive or spare disk** | Free, simple, genuinely off-machine | Only off-site if you unplug it and take it somewhere. Easy to forget |
| **Another machine on your LAN** | Automatic, no cost | Same building, same power, same ransomware blast radius |
| **Cloud object storage** | Genuinely off-site, cheap at lab scale | Costs a little money and needs an account |

**For this course, use a USB drive or a second disk**, because it costs
nothing and every step works identically. Where cloud storage differs is one
line, and this lesson shows it.

Mount your drive on UBNT01. If it appears as `/dev/sdb1`:

```bash
# Make a mount point and mount it. lsblk first, to find the
# right device: picking the wrong one is how people format
# the disk they meant to keep.
lsblk
sudo mkdir -p /mnt/backup
sudo mount /dev/sdb1 /mnt/backup
```

**How you know it worked:**

```bash
# Your drive, with its free space. Confirm the size matches
# the drive you plugged in, which is the check that you
# mounted what you thought you did.
df -h /mnt/backup
```

:::warning[Get the device right]
`lsblk` lists every disk. **`/dev/sda` is almost certainly UBNT01's own
system disk.** Formatting or mounting over that ruins the machine.

Look at the SIZE column and match it against the drive you physically
plugged in. If two disks are the same size, unplug the USB one, run `lsblk`,
plug it back in, run it again, and take the device that appeared.
:::

## Install restic

```bash
sudo apt update
sudo apt install -y restic
```

**How you know it worked:**

```bash
# Any version. Expect something like "restic 0.16.4".
restic version
```

## Create the repository

A restic **repository** is the encrypted store your backups live in. It is
initialised once.

**The password is not recoverable.** restic encrypts everything with it, and
there is no reset. Lose it and your backups are permanently unreadable, which
is working as designed and is nonetheless how people lose their backups.

Put it in your password manager **before** you run the next command.

```bash
# You will be asked for a password twice.
restic -r /mnt/backup/lab-repo init
```

**How you know it worked:**

```text
created restic repository 09449fe9cb at /mnt/backup/lab-repo

Please note that knowledge of your password is required to access
the repository. Losing your password means that your data is
irrecoverably lost.
```

Your repository ID will differ. That warning is not boilerplate.

**For cloud storage instead**, the only change is the `-r` value, which
becomes something like `s3:s3.amazonaws.com/your-bucket` plus credentials in
environment variables. Every other command in this module is identical. That
is the property that makes restic worth learning.

## Stop typing the password

Being prompted every time makes automation impossible, and lesson 15.6
automates this.

```bash
# A file only you can read, holding the repository password.
# The chmod is the whole security of this arrangement.
echo 'your-repository-password' | sudo tee /root/.restic-password > /dev/null
sudo chmod 600 /root/.restic-password
```

**How you know it worked:**

```bash
# Expect exactly: -rw------- and root root
sudo ls -l /root/.restic-password
```

**Anything other than `-rw-------` means other users can read your backup
password.** This is lesson 5.6's least privilege applied to a file, and the
reason it lives in `/root` is that the backup job will run as root, because
backing up a whole system requires reading files your user cannot.

## Back something up

Start with the things that would genuinely hurt to lose:

```bash
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password \
  backup /home /etc /var/lib/docker/volumes
```

Those three cover your home directories, this machine's configuration, and
**the Docker volumes from lesson 6.5**, which is where your actual service
data lives. A container is disposable; its volume is not.

**How you know it worked:**

```text
Files:        1234 new,     0 changed,     0 unmodified
Dirs:          567 new,     0 changed,     0 unmodified
Added to the repository: 197.574 KiB (196.952 KiB stored)

processed 1234 files, 195.374 KiB in 0:03
snapshot dbd28800 saved
```

Your numbers will be much larger. **The line that matters is the last one:
`snapshot <id> saved`.** No snapshot ID means no backup, whatever else the
output said.

:::tip[What this is called at work]
restic is doing what **Veeam, Commvault, Rubrik and Cohesity** do: a
repository, deduplicated snapshots, a retention policy, and encryption.

**What enterprise backup adds is mostly awareness of what it is backing up.**
It can quiesce a database or a domain controller so the copy is consistent
rather than merely recent, which is the problem lesson 15.4 is about. It backs
up virtual machines through the hypervisor rather than from inside them. And
it schedules and reports across thousands of jobs, because at that scale the
question is not "did it work" but "which twelve of last night's four thousand
jobs failed".

**The feature everybody is buying right now is immutability**: backups that
cannot be deleted or encrypted even by an administrator, because ransomware
operators go for the backups first and often succeed. Your restic repository
does not have that, and knowing the gap exists is more useful than pretending
it does not.

The thing that does not change is lesson 15.3. **An untested backup is not a
backup**, at any price.
:::

## Now run it again, and watch why restic is worth it

```bash
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password \
  backup /home /etc /var/lib/docker/volumes
```

The second run is dramatically faster and adds almost nothing. In my test,
backing up 195 KiB of data where **one small file had changed** added this:

```text
Files:           0 new,     1 changed,     2 unmodified
Added to the repository: 1.479 KiB (870 B stored)
```

**870 bytes**, to protect the current state of everything.

That is **deduplication**: restic splits files into chunks, and only stores
chunks it has never seen. Identical data is stored once no matter how many
times it appears or how many snapshots reference it.

The practical consequence is the one to take away: **because each backup is
nearly free, you can afford to run them often**, and running them often is
what makes your RPO from lesson 15.1 small. Cheap backups and frequent
backups are the same conversation.

## See what you have

```bash
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password snapshots
```

```text
ID        Time                 Host        Tags        Paths
--------------------------------------------------------------------
dbd28800  2026-08-05 15:31:41  ubnt01                  /home
80d70c9c  2026-08-05 15:34:02  ubnt01                  /home
--------------------------------------------------------------------
2 snapshots
```

Each snapshot is a complete, independently restorable point in time. There is
no "full versus incremental" distinction to manage, which is the other reason
this tool is pleasant.

## Check that the repository itself is sound

Backups can rot. Disks develop bad sectors, and a repository that has been
quietly corrupting for a year is worse than no repository, because you
believed in it.

```bash
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password check
```

**How you know it worked:**

```text
check all packs
check snapshots, trees and blobs
[0:00] 100.00%  2 / 2 snapshots

no errors were found
```

**`no errors were found` is the only acceptable output.** Anything else means
investigate now rather than at restore time.

Note what `check` does and does not do: it verifies the repository's
structure and metadata are intact. It does **not** prove your data restores
correctly, and it is not a substitute for lesson 15.3. Tools that report
their own health are still tools reporting on themselves.

## Do not keep everything forever

```bash
# Keep a week of dailies and a month of weeklies. --dry-run
# shows what WOULD be removed without removing anything.
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password \
  forget --keep-daily 7 --keep-weekly 4 --dry-run
```

**Run the dry run first, every time, and read it.** `forget` deletes
snapshots. The `--dry-run` habit here is the same instinct as `apt list
--upgradable` in lesson 13.7 and Ansible's `--check` in lesson 10.5: see what
would change before changing it.

When the output looks right, run it again without `--dry-run`, then add
`--prune` to actually reclaim the disk space. `forget` removes the snapshot
references; `prune` deletes the now-unreferenced data.

## What you take from this

An encrypted, deduplicating backup repository on storage that is not the
machine it protects, with a retention policy and a password you have stored
somewhere you will still have it after the machine dies.

None of which proves you can get your data back. That is the next lesson, and
it is the one that counts.

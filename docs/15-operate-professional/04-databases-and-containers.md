---
title: "15.4 The hard ones: databases and containers"
sidebar_position: 4
---

# 15.4 The hard ones: databases and containers

Lesson 15.1 named three kinds of restore and said the third one,
**application-consistent**, is where people go wrong. This is that lesson,
and it contains the most surprising demonstration in the module.

## Why copying a database file is not backing it up

A running database is not a file sitting still. It is a program holding a
file open, with data in memory, transactions part-written, and often
*additional* files alongside the main one holding recent changes.

Copy the main file while all that is happening and you get a copy of
something that was never in a consistent state.

**Here is the part that makes this urgent rather than theoretical.**

Your Gitea database from lesson 6.9 is SQLite. SQLite in its common WAL mode
(write-ahead logging) keeps recent committed data in a **separate file**
alongside the database, named `<database>-wal`. While the application is
running, the files on disk look like this:

```text
gitea.db      gitea.db-shm      gitea.db-wal
```

I set up exactly that situation, with a table containing two committed rows,
and copied **only the main `.db` file**, which is what a naive backup script
does. Then I opened the copy and asked it for the rows:

```text
rows in the real database: 2
naive copy (main file only): sqlite3.OperationalError: no such table: t
```

**Not "fewer rows". No table at all.** The entire schema and every row lived
in the `-wal` file that was not copied. The backup completed successfully,
produced a file of plausible size, and contained nothing usable.

That is the failure mode, and it is silent. Your backup job reports success
every night for a year.

## The correct way

Databases provide their own backup commands, and the whole reason they exist
is this problem. They coordinate with the running engine to produce a copy
that is internally consistent.

For SQLite:

```bash
# .backup coordinates with the running database. Safe to run
# while the application is using it, which cp is not.
sqlite3 /path/to/gitea.db ".backup '/tmp/gitea-backup.db'"
```

**How you know it worked:**

```bash
# The copy opens, and its structure is sound. Expect: ok
sqlite3 /tmp/gitea-backup.db "PRAGMA integrity_check;"

# And it has your data. Expect a plausible number, not 0.
sqlite3 /tmp/gitea-backup.db "SELECT COUNT(*) FROM user;"
```

When I ran the same test with `.backup` instead of a file copy, against the
same live database:

```text
rows in the .backup copy:  2
integrity of .backup copy: ok
```

Two rows and a clean integrity check, from a database that was open and in
use at the time.

**`PRAGMA integrity_check` returning `ok` is the verification that matters**,
and it is the database equivalent of the checksum comparison in lesson 15.3.
A copy that opens is not the same as a copy that is sound.

The same pattern holds everywhere. PostgreSQL has `pg_dump`, MySQL has
`mysqldump`, and both exist for exactly this reason. **The rule generalises:
if a running program owns a file, ask that program for the copy.**

## Now do it for Gitea properly

Gitea is more than its database: there are repositories on disk too, and a
database restored without matching repositories is a database describing
things that are not there.

```bash
# Find where Gitea's data lives. This is the volume from
# lesson 6.5, and the name depends on your stack directory.
docker volume ls
```

The professionally correct order, and the reason for each step:

```bash
# 1. Stop the application. A backup of a stopped service is
#    trivially consistent, and for a lab the downtime is free.
cd ~/docker/gitea && docker compose stop

# 2. Back up its volume, now that nothing is writing to it.
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password \
  backup /var/lib/docker/volumes/gitea_data \
  --tag gitea

# 3. Start it again.
docker compose start
```

**How you know it worked:**

```bash
# The snapshot exists and carries your tag.
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password \
  snapshots --tag gitea

# And Gitea came back. Expect 200.
curl -s -o /dev/null -w '%{http_code}\n' https://git.lab.internal
```

**Stopping the service is a legitimate professional answer**, not a
shortcut. It is the simplest way to guarantee consistency, and plenty of real
systems are backed up in a nightly maintenance window for exactly this
reason. The alternative, backing up live, is what the database's own tools
are for, and you use those when downtime is not acceptable.

**Tag your backups.** `--tag gitea` lets you find and restore one service's
snapshots without wading through everything, which matters when you are
restoring under pressure.

## What a container backup actually needs

This is worth being precise about, because containers change the shape of the
question.

**You do not back up containers.** A container is disposable by design; that
is the entire point of Module 6. If you lose one, you recreate it.

**You back up three things:**

1. **The volumes**, which hold the data. Nothing else is unique.
2. **The compose files**, which describe how to recreate the service. These
   are in Git already, from lesson 6.5, which is a backup.
3. **Any configuration outside the volume**, such as the nginx configuration
   and certificates from Module 7.

**And the image is not your responsibility to preserve, until it is.** You
pull `gitea/gitea` from the internet, so it is not in your backup. That is
normal and it introduces a dependency worth naming: if that image disappears
or you need a version that is no longer published, your restore stalls.
Lesson 13.8's supply chain point, arriving in an operations context.

Recording the exact image tag in your compose file, rather than `latest`, is
what makes a restore reproducible. Pinning a version is usually a maintenance
debt, because a pin stops being current the day after you write it. This is
the exception: here the pin is part of what you are restoring, and `latest`
means you get whichever version exists on the day you restore rather than the
one that was running when the backup was taken.

## The restore drill for a service

Same discipline as lesson 15.3. Prove it rather than assuming it.

```bash
# 1. Record what is in there now.
sudo sqlite3 /var/lib/docker/volumes/gitea_data/_data/gitea/gitea.db \
  "SELECT COUNT(*) FROM user;"

# 2. Stop the service.
cd ~/docker/gitea && docker compose down

# 3. Restore the volume to a scratch location and look at it
#    BEFORE overwriting anything real.
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password \
  restore latest --tag gitea --target /tmp/gitea-restore

# 4. Prove the restored database is sound and complete.
sudo find /tmp/gitea-restore -name 'gitea.db' -exec \
  sqlite3 {} "PRAGMA integrity_check; SELECT COUNT(*) FROM user;" \;
```

**Expect `ok` and the same user count as step 1.** If the count differs, your
backup captured a different moment than you thought; if `integrity_check`
returns anything else, you have reproduced the WAL problem from the top of
this lesson and your backup method needs fixing rather than your restore.

Then bring the service back with `docker compose up -d` and confirm it
answers.

Clean up: `sudo rm -rf /tmp/gitea-restore`

## What you take from this

A demonstrated understanding that copying a live database file can produce a
backup containing nothing, the habit of asking the owning program for the
copy, and a service-level restore drill that verifies the data rather than
the file.

You also know that the thing you actually protect in a container world is the
volume, and that the image is a dependency you do not control.

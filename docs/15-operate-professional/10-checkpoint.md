---
title: "15.10 Checkpoint: you can put it back"
sidebar_position: 10
---

# 15.10 Checkpoint: you can put it back

The test for this module is not that backups run. It is that you have put
data back and proved it was the same data.

Run these on UBNT01.

```bash
# The repository exists and is reachable, from 15.2.
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password snapshots

# It is structurally sound. Expect: no errors were found
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password check

# The password file is readable only by root, from 15.2.
# Expect: -rw------- and root root
sudo ls -l /root/.restic-password

# Backup storage is not the machine it protects, from 15.2.
# The mount point should be a separate device from /.
df -h /mnt/backup /
```

```bash
# The playbooks parse, from 15.6.
cd ~/ansible
ansible-playbook --syntax-check patch-linux.yml
ansible-playbook --syntax-check patch-dcs.yml

# The domain_controllers group exists, which serial: 1 depends on.
ansible-inventory --graph | grep -A3 domain_controllers
```

## Pass criteria

**Concepts, any tier:**

- [ ] You can state the difference between reverting a snapshot and restoring
      a backup, in terms of what each is *for* (lesson 15.1, answering 3.6)
- [ ] Your RPO and RTO are written down **with reasoning**, not just numbers
      (lesson 15.1)
- [ ] You can recite 3-2-1 and say which part your journal already satisfied
      since lesson 6.8 (lesson 15.1)
- [ ] You can name the three things "restore" can mean and say which one your
      RTO is really about (lesson 15.1)

**A backup that exists:**

- [ ] A restic repository exists on storage that is **not** UBNT01
      (lesson 15.2)
- [ ] The repository password is in your password manager, and you understand
      it is not recoverable (lesson 15.2)
- [ ] `/root/.restic-password` is mode 600 (lesson 15.2)
- [ ] You ran a second backup and can explain why it added almost nothing,
      and why that makes frequent backups affordable (lesson 15.2)
- [ ] `restic check` reports `no errors were found`, and you can say why that
      is **not** the same as proving a restore works (lesson 15.2)
- [ ] A retention policy is set, and you ran `forget` with `--dry-run` first
      (lesson 15.2)

**A backup that restores, which is the actual test:**

- [ ] **You deleted real data, restored it, and `diff` on the checksums
      printed nothing** (lesson 15.3)
- [ ] You know restic restores into the original path structure under your
      target, because you looked rather than assumed (lesson 15.3)
- [ ] You **timed** a restore and compared it against your RTO (lesson 15.3)
- [ ] A monthly restore-test reminder exists somewhere you will see it
      (lesson 15.3)

**The hard ones:**

- [ ] You can explain why copying a live SQLite database can produce a file
      with no table in it at all (lesson 15.4)
- [ ] You backed up Gitea using `.backup` or by stopping the service, and
      verified with `PRAGMA integrity_check` returning `ok` (lesson 15.4)
- [ ] You can say what you actually protect for a containerised service, and
      why the image is a dependency you do not control (lesson 15.4,
      building on 13.8)
- [ ] Your backups are tagged, so one service can be found without wading
      through everything (lesson 15.4)

**Tier 2 and up, the domain:**

- [ ] You can explain **USN rollback**, and what lesson 5.12's "snapshot both
      DCs together or not at all" rule was protecting you from (lesson 15.5)
- [ ] A system state backup exists, and you understand it contains every
      password hash in your domain (lesson 15.5, building on 14.8)
- [ ] You can state the difference between authoritative and non-authoritative
      restore, and the test for choosing (lesson 15.5)
- [ ] You can explain why, with two healthy DCs, the fastest recovery from
      one dying is usually **not** a restore (lesson 15.5, building on 5.9)
- [ ] You seized the FSMO roles onto DC02 and transferred them back cleanly
      (lesson 15.5, building on 5.10)

**Automation:**

- [ ] `patch-linux.yml` runs, and reports a needed reboot rather than
      performing one (lesson 15.6)
- [ ] **You can explain what `serial: 1` does and why it is the whole safety
      property of the domain controller playbook** (lesson 15.6, building on
      13.7)
- [ ] The DC playbook asserts replication health before changing anything and
      asserts the directory services are running after (lesson 15.6,
      building on 5.9 and 13.7)
- [ ] **The rescan step exists**, so the loop from lesson 13.7 actually
      closes (lesson 15.6)
- [ ] Scheduled jobs use absolute paths and log somewhere, and you checked
      the log after the first run (lesson 15.6, building on 10.9)
- [ ] You decided how the rescan result reaches a human, rather than
      scheduling it and never looking (lesson 15.6)

**The unglamorous half:**

- [ ] One real runbook exists, with all six sections including **Impact** and
      **If it goes wrong** (lesson 15.7)
- [ ] You can say why you cannot test your own runbook, and what the two next
      best options are (lesson 15.7)
- [ ] `Projects/lab-changes.md` exists with the five fields per entry
      (lesson 15.8)
- [ ] You can answer "when did this last change, and why" for your compose
      files, and you know **where you cannot** answer it (lesson 15.8)
- [ ] You can name the four questions to ask before a change, and say which
      one most changes behaviour (lesson 15.8)
- [ ] You worked through the stolen-laptop exercise and wrote the gaps down
      as findings (lesson 15.9)
- [ ] `Projects/lab-operations.md` written, journal committed and pushed,
      Module 15 ticked (lesson 15.9)

All green? Then you can lose data and get it back, patch a pair of domain
controllers without taking the domain down, and hand somebody else a
procedure they can follow.

That combination is what "operate" means, and it is the part of the job that
keeps existing long after the building phase is over.

Module 16 turns to proving all of it: mapping what you built to a control
framework, and producing the documents an auditor asks for. Almost everything
you wrote down in this module is evidence, which is why it comes next.

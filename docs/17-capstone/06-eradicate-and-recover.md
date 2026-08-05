---
title: "17.6 Eradicate and recover"
sidebar_position: 6
---

# 17.6 Eradicate and recover

Containment stopped it. Eradication removes it. Recovery gets you back to
normal and proves you are there.

The distinction between the last two is worth stating, because it is where
incidents get reopened: **eradication is about the intruder, recovery is
about the system.** You can remove every artefact and still have a machine
you cannot vouch for.

## The question that decides how much work this is

**Do you trust this machine?**

That question has a real answer and it is not always yes. The honest test:
**can you enumerate everything that was done to it?**

- **Yes** and the list is short and reversible: clean up in place.
- **No**, or the intruder had root for an unknown period, or a rootkit is
  plausible: **rebuild from known-good.**

**Rebuild is the safe answer and professionals reach for it more often than
beginners expect.** The reason is that a sufficiently privileged intruder
can modify anything, including the tools you would use to look for them, and
"I checked and found nothing" from a compromised system is not evidence.

**For this incident, in-place cleanup is defensible**, and you should be able
to say why: the timeline in 17.4 accounts for every change, the window is
bounded and short, and the artefacts are all in configuration rather than in
binaries.

**Say that in your report.** "Cleaned in place because the change set was
fully enumerated over a bounded window" is a justified decision. "Cleaned in
place" alone is not.

:::tip[When you cannot enumerate, rebuild]
This is one of the genuinely useful things Module 15 bought you. You have
backups you proved restore in lesson 15.3, and compose files in Git from
lesson 6.5.

**That is what makes "rebuild it" a decision rather than a catastrophe.** An
organisation that cannot rebuild is an organisation that has to trust a
machine it cannot vouch for, and that is how intrusions persist for months.
:::

## Eradicate

You wrote and read the cleanup script in lesson 17.2. Now is when it runs.

```bash
cd ~/capstone
sudo ./cleanup.sh
```

**How you know it worked**, and note the script verifies rather than
assuming:

```text
[*] Removing scenario artefacts.
  - cron job
  - sudoers rule
  - account and home
  - generated key
[*] Verifying removal:
  ok: account gone
  ok: cron gone
  ok: sudoers gone
```

**Do not stop at the script's own report.** A removal tool reporting success
is exactly the thing lesson 15.2 warned about with `restic check`: tools
reporting on themselves are weaker evidence than an independent check.

## Verify independently

Run the same commands you used to find the problem, and expect nothing:

```bash
# The account is gone from the passwd database.
getent passwd svc-update || echo "no such account"

# Its home directory is gone.
ls -d /home/svc-update 2>/dev/null || echo "home directory removed"

# No scheduled job.
ls /etc/cron.d/ | grep -i health || echo "no cron job"

# No sudoers rule.
sudo ls /etc/sudoers.d/ | grep -i svc-update || echo "no sudoers rule"

# No keys anywhere you did not put there.
sudo find /home /root -name authorized_keys -exec ls -l {} \; \
     -exec cat {} \; 2>/dev/null
```

**Then the check that actually matters: compare against your baseline.**

```bash
# The same command from lesson 17.1. Compare the output to what
# you saved then. It should match exactly.
awk -F: '$3>=1000 && $3<65534 {print $1, $3, $6}' /etc/passwd
```

**This is why you captured a baseline.** "Nothing suspicious found" is a
judgement; "the account list is identical to the pre-incident baseline" is a
comparison, and it is much stronger.

**One thing the cleanup does not remove**, deliberately:

```bash
# Your evidence, which should still be there.
sudo ls -l /var/tmp/incident-2026-01/
sudo sha256sum -c /var/tmp/incident-2026-01-hashes.txt 2>/dev/null || \
  (cd /var/tmp/incident-2026-01 && sudo sha256sum -c ../incident-2026-01-hashes.txt)
```

**Expect every line to say `OK`.** That proves your evidence has not changed
since you collected it, which is the point of having hashed it.

## Recover: prove the machine still works

Eradication proved the bad things are gone. **Recovery proves the good things
still work**, and it is a separate check because cleanup can break things.

```bash
# Your services are running.
cd ~/docker/gitea && docker compose ps

# And answering. Expect 200.
curl -s -o /dev/null -w '%{http_code}\n' https://git.lab.internal

# Monitoring is still collecting.
cd ~/docker/wazuh && docker compose ps

# You can still log in as yourself, and sudo still works.
sudo -v && echo "sudo works"

# The host firewall is as it should be.
sudo ufw status
```

**Check `ufw status` against your expectations specifically**, because
lesson 14.3 opened port 8081 and lesson 13.4 opened 9392. If either is open
and should not be, that is a finding, and it is the kind that survives from
one module to the next unnoticed.

## Now do the one thing everybody skips

**Change the credentials that were exposed.**

The intruder had root-equivalent access on UBNT01. Ask what that machine
holds, and you already know from Module 15:

- **The restic backup password** in `/root/.restic-password`, from lesson
  15.2
- **SSH keys** for reaching other machines
- **Any credentials in your compose files or environment files**
- **The Wazuh agent's key**, and Gitea's data

**On a real incident you would rotate all of it.** In your lab, decide
deliberately and record what you decided, which is the transferable part.

At minimum, rotate the backup repository password, because it protects
everything else:

```bash
# restic supports changing the password without re-encrypting
# the whole repository.
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password key passwd
```

Then update `/root/.restic-password` with the new value and **verify the
repository still opens**:

```bash
sudo restic -r /mnt/backup/lab-repo \
  --password-file /root/.restic-password snapshots
```

**How you know it worked:** your snapshot list appears. **If it does not, fix
it now**, because a backup you cannot open is worse than no backup and you
have just made this mistake in a situation where you can still recover from
it.

**Write down what you rotated and what you deliberately did not.** "Decided
not to rotate X because Y" is a legitimate entry; silence is not.

## Take the second snapshot

```text
Snapshot UBNT01 again, named something like
"post-incident-clean-2026-08-05".
```

**Two snapshots, before and after, are a genuinely useful pair.** If a
question comes up next week about what the machine looked like during the
incident, you have it.

## Update your note

```markdown
## Eradication and recovery
| Time | Action | Verified by |
|---|---|---|
| 16:30 | Ran cleanup.sh | Script self-verified; independent checks below |
| 16:32 | Confirmed account, cron, sudoers, keys all absent | getent, ls, find: all negative |
| 16:33 | Compared account list against pre-incident baseline | Identical |
| 16:35 | Verified evidence hashes unchanged | sha256sum -c: all OK |
| 16:38 | Confirmed Gitea and Wazuh running and answering | docker compose ps; curl 200 |
| 16:42 | Rotated restic repository password | snapshots listed successfully with new password |
| 16:45 | Snapshot post-incident-clean-2026-08-05 | Visible in hypervisor |

**Rebuild considered?** Yes. In-place cleanup chosen because the
change set was fully enumerated over a bounded window and all
changes were configuration rather than binaries.

**Credentials rotated:** restic repository password.
**Deliberately not rotated:** [list, with reasons].
```

## What you take from this

A machine verified clean against a baseline rather than against your
judgement, evidence proven unchanged since collection, services confirmed
working, credentials rotated deliberately, and a recorded decision about
rebuild-versus-clean that you could defend.

Next lesson you write it up.

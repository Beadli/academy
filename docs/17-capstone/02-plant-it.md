---
title: "17.2 Plant it"
sidebar_position: 2
---

# 17.2 Plant it

Two scripts, printed in full, because lesson 1.6's rule applies to me as much
as to anybody else: understand a command before you run it.

**Read both before running either.** If you would rather type the actions
yourself than run somebody's script, do that. The module works identically.

## Before anything

**Snapshot UBNT01.** Lesson 3.5's habit, reinforced in 14.1. The cleanup
script removes everything, and a snapshot means you do not have to trust it.

**Confirm you captured the baseline** from lesson 17.1. If you skipped it, go
back; the investigation is dramatically harder without it and the difficulty
is artificial rather than instructive.

**Make sure your Module 12 stack is running**, if you have one:

```bash
cd ~/docker/wazuh && docker compose ps
```

## The scenario script

Create `~/capstone/scenario.sh` on UBNT01:

```bash
#!/usr/bin/env bash
# scenario.sh: plants a capstone incident in your own lab.
# Everything it does is reversible by cleanup.sh. Read both before running.
set -euo pipefail

STAGE="${1:-}"
MARK="/var/tmp/.capstone-marker"

if [[ $EUID -ne 0 ]]; then echo "Run with sudo."; exit 1; fi
if [[ "$STAGE" != "--i-have-read-this" ]]; then
  echo "Read the script first, then run: sudo ./scenario.sh --i-have-read-this"
  exit 1
fi

# A randomised delay so the timeline is not one you memorised.
DELAY=$(( (RANDOM % 90) + 30 ))
echo "[*] Scenario will unfold over the next few minutes. Do not watch."
echo "[*] Record the time you started: $(date '+%F %T %Z')"
: > "$MARK"

(
  sleep "$DELAY"

  # 1. A new local account, of the kind a real intrusion creates.
  useradd -m -s /bin/bash -c "" svc-update 2>/dev/null || true
  echo "svc-update:$(head -c 18 /dev/urandom | base64)" | chpasswd

  sleep $(( (RANDOM % 40) + 10 ))

  # 2. Persistence: an SSH key the operator did not add.
  install -d -m 700 /home/svc-update/.ssh
  ssh-keygen -q -t ed25519 -N '' -C 'capstone-scenario' -f /tmp/.cap_key
  cat /tmp/.cap_key.pub > /home/svc-update/.ssh/authorized_keys
  chmod 600 /home/svc-update/.ssh/authorized_keys
  chown -R svc-update:svc-update /home/svc-update/.ssh

  sleep $(( (RANDOM % 40) + 10 ))

  # 3. Persistence: a cron job that beacons on a schedule.
  cat > /etc/cron.d/system-health <<'CRON'
*/5 * * * * root /usr/bin/curl -s -m 5 -o /dev/null https://example.com/health
CRON
  chmod 644 /etc/cron.d/system-health

  sleep $(( (RANDOM % 40) + 10 ))

  # 4. Privilege: sudo rights granted outside your usual process.
  echo 'svc-update ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/svc-update
  chmod 440 /etc/sudoers.d/svc-update

  sleep $(( (RANDOM % 40) + 10 ))

  # 5. Some ordinary noise, so not everything you find is hostile.
  logger -p auth.info "Accepted publickey for sam from 10.10.10.99 port 51234 ssh2"
  apt-get -qq update >/dev/null 2>&1 || true
) >/dev/null 2>&1 &

echo "[*] Started. Go and do something else for ten minutes."
```

## What it actually does, since you should know before running it

Five actions, over roughly three to six minutes, in a randomised rhythm:

1. **Creates a local account** called `svc-update` with a random password.
   The name is chosen to look plausible, which is the point: real intrusions
   do not create accounts called `hacker`.
2. **Adds an SSH key** to that account's `authorized_keys`. This is
   persistence: a way back in that does not need the password.
3. **Writes a cron job** that runs `curl` to `example.com` every five
   minutes. This is the shape of **beaconing**, a compromised host checking
   in on a schedule. It contacts a harmless documentation domain.
4. **Grants passwordless sudo** to the new account via `/etc/sudoers.d/`.
   This is privilege escalation and it is the most serious of the five.
5. **Generates ordinary noise**: a benign log line and an `apt update`, so
   that not everything you find is hostile and you have to tell the
   difference.

**Nothing is encrypted, deleted, exfiltrated or sent anywhere.** The only
outbound traffic is the beacon to `example.com`, which is a domain reserved
by the standards bodies for exactly this kind of use.

**Note what the randomisation gives you.** You know these five things
happened. You do not know the order, the timing, or the exact artefacts, and
reconstructing those is the investigation.

## The cleanup script

Write this **before** you run the scenario, so it exists when you want it.
Create `~/capstone/cleanup.sh`:

```bash
#!/usr/bin/env bash
# cleanup.sh: undoes everything scenario.sh did. Run when finished.
set -uo pipefail
if [[ $EUID -ne 0 ]]; then echo "Run with sudo."; exit 1; fi

echo "[*] Removing scenario artefacts."
rm -f  /etc/cron.d/system-health         && echo "  - cron job"
rm -f  /etc/sudoers.d/svc-update         && echo "  - sudoers rule"
userdel -r svc-update 2>/dev/null        && echo "  - account and home" || echo "  - account: not present"
rm -f  /tmp/.cap_key /tmp/.cap_key.pub   && echo "  - generated key"
rm -f  /var/tmp/.capstone-marker

echo "[*] Verifying removal:"
id svc-update            >/dev/null 2>&1 && echo "  STILL PRESENT: account" || echo "  ok: account gone"
[[ -f /etc/cron.d/system-health ]]       && echo "  STILL PRESENT: cron"    || echo "  ok: cron gone"
[[ -f /etc/sudoers.d/svc-update ]]       && echo "  STILL PRESENT: sudoers" || echo "  ok: sudoers gone"
```

**Notice that cleanup verifies rather than assuming.** This is lesson 15.3's
discipline: a removal script that reports success is not the same as a
machine that is clean. **Do not run it yet**; lesson 17.6 covers when.

## Run it

```bash
cd ~/capstone
chmod +x scenario.sh cleanup.sh

# Check they parse before running anything, per lesson 2.2.
bash -n scenario.sh && bash -n cleanup.sh && echo "both parse"

sudo ./scenario.sh --i-have-read-this
```

**How you know it worked:**

```text
[*] Scenario will unfold over the next few minutes. Do not watch.
[*] Record the time you started: 2026-08-05 15:42:11 EDT
[*] Started. Go and do something else for ten minutes.
```

**Write that start time in your investigation note**, then close the
terminal.

**Now genuinely go away for ten minutes.** Watching it happen defeats the
exercise, and the temptation to run `watch ls /etc/cron.d/` is real. Make
tea. The randomised delays mean the last action lands somewhere between three
and six minutes after the first.

## While you wait, one thing worth thinking about

You are about to investigate an incident where **you know roughly what
category of thing happened.** A real analyst usually knows less.

But notice what you still do not know, and what you will have to establish
from evidence alone:

- What time each thing happened
- In what order
- Which artefacts exist and where
- Whether anything *else* on the machine was affected
- Whether your monitoring saw any of it

**That last one is the real test of Modules 12 through 15**, and it is the
first thing the next lesson asks.

## What you take from this

An incident in progress on your own machine, planted by a script you read
first, with a start time recorded and a cleanup script already written.

Next lesson you find out whether anything noticed.

---
title: "17.4 Investigate: build a timeline"
sidebar_position: 4
---

# 17.4 Investigate: build a timeline

**A timeline is the deliverable of an investigation.** Not a list of bad
things found: an ordered account of what happened, when, with the evidence
for each entry.

The reason is practical rather than aesthetic. Ordering events is what tells
you which was the *first* one, and the first one is how they got in. Without
a timeline you have a pile of symptoms and no idea which is the cause.

**Keep rule one in front of you**: everything below must be established from
the machine, not from having read the script.

## Find the new account, and date it

```bash
# Accounts that can log in. Compare against the baseline you
# captured in lesson 17.1.
awk -F: '$3>=1000 && $3<65534 {print $1, $3, $6}' /etc/passwd
```

**How you know it worked:** you get a short list, and one entry is not in
your baseline. That difference is your first finding, and **it is a finding
because you had a baseline**, which is the entire argument for capturing one.

Now date it, which is the part that turns a finding into a timeline entry:

```bash
# Field 3 of /etc/shadow is the date the password was last
# changed, in days since 1 January 1970. For an account created
# and never touched since, that is its creation date.
sudo awk -F: '$1=="svc-update" {print $3}' /etc/shadow
```

Convert it:

```bash
# Substitute the number from above.
date -d "@$(( 20671 * 86400 ))" +%F
```

**Expect today's date.** That gives you the day but not the time, which is
why the log line from lesson 17.3 matters more:

```bash
# The precise moment, with the UID.
sudo journalctl --no-pager | grep 'new user' | tail -5
```

**That log line is your best evidence for entry one of the timeline**: an
exact timestamp, the account name, and the UID.

## Find the persistence

An intruder who only creates an account has done nothing durable. **Look for
the ways back in**, and look in all of them rather than the first one you
think of.

```bash
# 1. SSH keys, in every home directory. A key you did not add
#    is one of the clearest persistence indicators there is.
sudo find /home /root -name authorized_keys -exec ls -l {} \; \
     -exec cat {} \; 2>/dev/null
```

**How you read it:** each file is listed with its timestamp, then its
contents. **The comment field at the end of a key is chosen by whoever
generated it**, and is worth reading; ordinary keys carry `user@hostname`.

```bash
# 2. Scheduled tasks, in all the places they live. People check
#    crontab and forget /etc/cron.d, which is where this one is.
ls -la /etc/cron.d/
sudo crontab -l 2>/dev/null
for u in $(awk -F: '$3>=1000 && $3<65534 {print $1}' /etc/passwd); do
  echo "--- $u"; sudo crontab -u "$u" -l 2>/dev/null || echo "(none)"
done
```

```bash
# 3. Sudo rights granted outside the defaults.
sudo ls -la /etc/sudoers.d/
sudo cat /etc/sudoers.d/* 2>/dev/null
```

**Compare every one of those against your baseline.** Anything present now
and absent then is a timeline entry.

## Date the files, which is where the timeline comes together

Every file has timestamps, and they answer different questions:

```bash
sudo stat /etc/cron.d/system-health /etc/sudoers.d/svc-update \
          /home/svc-update/.ssh/authorized_keys
```

**Three timestamps, and the third is the one investigators care about:**

- **Modify (`%y`)**: when the contents last changed.
- **Access (`%x`)**: when it was last read. Often useless, because many
  systems do not update it by default.
- **Change (`%z`)**: when the inode last changed, meaning contents,
  permissions or ownership. **This one is harder to fake**, because `touch`
  alters modify time but updating change time requires more effort.

**A file whose modify time is older than its change time is worth a second
look**, because that pattern is what backdating looks like.

## Sweep the whole window

You have found things you went looking for. Now find the things you did not
know to look for:

```bash
# Everything under /etc changed in your incident window.
# Substitute your real start time and now.
sudo find /etc -newermt "2026-08-05 15:40" ! -newermt "2026-08-05 16:10" \
     -type f 2>/dev/null
```

**How you know it worked:** a short list of paths. **Read every one**, and
expect some innocent entries: an `apt update` touches files under `/etc`
legitimately, and the script deliberately generated ordinary noise so that
you would have to distinguish.

**Those innocent entries go in the "Ruled out" section of your note**, with
one line each on why. That section is rule three from lesson 17.1, and it is
what makes an investigation credible.

Widen it if you want the fuller picture:

```bash
# The same window, across the filesystem, excluding the noisy
# virtual filesystems. This produces a lot; skim it.
sudo find / -xdev -newermt "2026-08-05 15:40" ! -newermt "2026-08-05 16:10" \
     -type f 2>/dev/null | grep -vE '^/(proc|sys|run|var/log|var/lib/docker)' | head -40
```

## Look for the beacon

The cron job says what should be happening. Confirm it actually is, because
a scheduled job and a running one are different claims:

```bash
# Has cron run it? Look for the job executing.
sudo journalctl -u cron --no-pager --since "2026-08-05 15:40" | tail -20

# And is there outbound traffic on that rhythm? Watch for a
# couple of minutes. Ctrl+C to stop.
sudo ss -tnp | grep -i curl
```

**Expect the cron log to show the job running every five minutes.** Catching
the connection with `ss` is luck, because it lasts under a second; **failing
to catch it is not evidence of absence**, and saying so in your report is
better than implying you proved something you did not.

**The honest write-up** is: the schedule is confirmed from cron's own logs,
the destination is known from the job definition, and the traffic content is
unknown because it is HTTPS, per lesson 12.7.

## Now build the timeline

In your investigation note:

```markdown
## Timeline
All times [your timezone]. Evidence in the right column.

| Time | Event | Evidence |
|---|---|---|
| 15:43:12 | Local account `svc-update` created, UID 1002 | journalctl: `useradd[...]: new user: name=svc-update` |
| 15:44:05 | SSH key added to svc-update authorized_keys | stat change time; key comment `capstone-scenario` |
| 15:44:51 | Cron job `/etc/cron.d/system-health` created, beaconing to example.com every 5 min | stat; file contents |
| 15:45:30 | Passwordless sudo granted to svc-update | stat on /etc/sudoers.d/svc-update; file contents |
| 15:46:02 | First beacon executed | journalctl -u cron |

**First observed event:** account creation at 15:43:12.
**Initial access:** NOT ESTABLISHED. See below.
```

## The question you cannot answer, and should say so

**How did they get in?**

Look for it honestly: check `last`, check `/var/log/auth.log` for successful
logins before your first event, check whether any service was exploited.

```bash
sudo last -20
sudo journalctl --since "2026-08-05 15:30" | grep -iE 'accepted|failed|session opened' | head -20
```

**You will not find an initial access vector, because there was not one.**
The script ran locally as root; nobody broke in.

**Write that down as an unknown, not as an absence.** The correct entry is:

> **Initial access: not established.** No successful remote authentication
> was observed before the first event, and no evidence of service
> exploitation was found. The earliest observed activity is already
> privileged. This is consistent with either local execution or an access
> vector that left no evidence in the sources examined.

**That paragraph is the most professionally realistic thing in this module.**
Real investigations frequently cannot establish initial access, and the
difference between a good report and a bad one is whether it says so, or
quietly implies the first thing found was the beginning.

Note also what that entry *enables*: "the earliest observed activity is
already privileged" is a genuine analytical observation with a consequence,
which is that everything before it is missing from your evidence.

## What you take from this

A timeline with evidence for every entry, a ruled-out list, and an honest
unknown recorded as an unknown.

Next lesson you stop it.

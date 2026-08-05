---
title: "17.10 Checkpoint: the course, finished"
sidebar_position: 10
---

# 17.10 Checkpoint: the course, finished

Two checkpoints in one. The incident, and the course.

Run these on UBNT01.

```bash
# The machine is clean: every artefact gone, from 17.6.
getent passwd svc-update            || echo "ok: no account"
ls -d /home/svc-update 2>/dev/null   || echo "ok: no home directory"
ls /etc/cron.d/ | grep -i health     || echo "ok: no cron job"
sudo ls /etc/sudoers.d/ | grep -i svc-update || echo "ok: no sudoers rule"

# The account list matches the pre-incident baseline, from 17.1.
awk -F: '$3>=1000 && $3<65534 {print $1, $3, $6}' /etc/passwd

# Evidence preserved and unchanged, from 17.5.
sudo ls -l /var/tmp/incident-2026-01/
cd /var/tmp/incident-2026-01 && sudo sha256sum -c ../incident-2026-01-hashes.txt

# Services recovered, from 17.6.
curl -s -o /dev/null -w '%{http_code}\n' https://git.lab.internal
```

```bash
# The documents exist and are committed.
ls ~/git/lab-journal/Projects/incident-2026-01*.md
cd ~/git/lab-journal && git status --short Projects/

# And the portfolio is a separate, public repository.
cd ~/git/lab-portfolio && git remote -v && ls
```

Expect `OK` on every hash line, `200` from Gitea, and no output from
`git status`.

## Pass criteria: the incident

- [ ] A baseline of accounts, cron, sudoers and listening ports was captured
      **before** the incident (lesson 17.1)
- [ ] You can name the six incident phases and say which one you did in
      Modules 12 to 16 (lesson 17.1)
- [ ] You read both scripts before running either (lesson 17.2)
- [ ] **You wrote an honest detection assessment before investigating the
      host**, while you could still be objective (lesson 17.3)
- [ ] You distinguished collection gaps from detection gaps (lesson 17.3,
      building on 14.9)
- [ ] You checked whether the gaps you found were already POA&M items from
      lesson 16.7 (lesson 17.3)
- [ ] A timeline exists with **evidence in every row**, not just events
      (lesson 17.4)
- [ ] The "ruled out" section is populated, including at least one innocent
      change you investigated and dismissed (lesson 17.4)
- [ ] **"Initial access: not established" is recorded as an unknown**, rather
      than the first event being implied as the beginning (lesson 17.4)
- [ ] Evidence was collected and hashed **before** anything was changed
      (lesson 17.5)
- [ ] You can explain why containment and eradication are separate phases
      (lesson 17.5)
- [ ] The account was **locked, not deleted**, during containment, and you
      can say why (lesson 17.5)
- [ ] You checked other lab systems for the same indicators and recorded the
      result either way (lesson 17.5)
- [ ] You made a deliberate contain-now versus observe-first decision and
      wrote the reason (lesson 17.5)
- [ ] Cleanup was verified **independently**, not by trusting the script's
      own report (lesson 17.6, building on 15.2)
- [ ] The clean state was confirmed by **comparison against the baseline**,
      not by judgement (lesson 17.6)
- [ ] Evidence hashes still verify after eradication (lesson 17.6)
- [ ] Services were confirmed working after cleanup, separately from
      confirming the bad things were gone (lesson 17.6)
- [ ] Exposed credentials were rotated, or a deliberate decision not to was
      recorded (lesson 17.6)
- [ ] You can say why in-place cleanup was defensible here, and when you
      would rebuild instead (lesson 17.6, building on 15.3)
- [ ] The report leads with a summary written last (lesson 17.7)
- [ ] It contains **"what did not work"** and **"unknowns and limitations"**
      sections (lesson 17.7)
- [ ] Recommendations are prioritised, and at least one honestly rated low
      despite sounding serious (lesson 17.7, building on 14.4)
- [ ] **The recommendations were added to the GSS-1 POA&M**, updating
      existing items rather than duplicating them (lesson 17.7, building on
      16.7)
- [ ] The risk register was updated for any risk that materialised
      (lesson 17.7, building on 16.6)

## Pass criteria: the portfolio

- [ ] A **separate public repository** exists, distinct from the private
      journal (lesson 17.8)
- [ ] Three sanitised documents are in it, with a README that frames them
      (lesson 17.8)
- [ ] The README says what this **is not**, including that it is a
      self-assessment (lesson 17.8, building on 16.8)
- [ ] You grepped for addresses, hostnames and credential references, and
      read the output rather than trusting it (lesson 17.8)
- [ ] The reasoning and honest failures survived sanitisation; only
      identifying specifics were removed (lesson 17.8)
- [ ] You can answer "tell me about your lab" with a decision rather than a
      technology list (lesson 17.8)

## Pass criteria: the course

- [ ] `Projects/lab-progress.md` has all eighteen modules ticked
      (lesson 17.9)
- [ ] **You can explain your whole lab in one page with no diagram**, the
      test lesson 0.1 set on your first evening (lesson 17.9)
- [ ] You wrote what you would do differently if you started over
      (lesson 17.9)
- [ ] You named at least one module you completed without really
      understanding (lesson 17.9)
- [ ] The monthly restore test is in a calendar, not just an intention
      (lesson 17.9, building on 15.3)
- [ ] Journal committed and pushed, Module 17 ticked (lesson 17.9)

## That is the course

You started with an empty computer and a journal file. You now have a
segmented network, a two-controller Active Directory domain, a certificate
authority with an offline root, single sign-on, a hybrid cloud identity
bridge, a container host, configuration management, a monitoring and
detection stack, a vulnerability management programme, a penetration test of
your own environment, an operations practice with proven backups, a full
control assessment, and an incident you investigated end to end.

**More usefully than any of that: you know what you do not know about it, and
you have written that down.**

Lesson 0.1 said the person who can follow the whole chain, rather than
knowing one tool, is rare and gets hired. You can follow the whole chain.
You built every link in it.

**[Drills](/drills)** is next, when it opens. Same lab, no more instructions:
exercises with an objective and a way to tell whether you succeeded.

The lab was never the point. Using it is.

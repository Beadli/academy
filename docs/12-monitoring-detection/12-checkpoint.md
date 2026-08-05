---
title: "12.12 Checkpoint: it notices, and you can explain why"
sidebar_position: 12
---

# 12.12 Checkpoint: it notices, and you can explain why

Prove the module stuck. The test is that you can attack your own lab, watch it
be noticed, and explain both why it fired and why it was not real.

## The end-to-end test

1. From KALI01, scan a lab machine.
2. Watch the alert arrive on UBNT01.
3. Triage it: what fired, from where, when, and is there a benign explanation
   that fits all of it.
4. Write the triage note in your journal.
5. Add a documented exception, and confirm the same activity from a different
   source still alerts.

Step five is the one that separates tuning from silencing.

## Commands

On UBNT01:

```bash
# The whole stack is up: manager, indexer, dashboard.
sudo systemctl is-active wazuh-manager
docker compose ps    # from the single-node directory

# The manager is running and agents are reporting.
sudo systemctl is-active wazuh-manager
sudo /var/ossec/bin/agent_control -l

# Your custom rules are valid.
sudo /var/ossec/bin/wazuh-logtest -t

# What is firing, most frequent first. The tuning backlog.
sudo cat /var/ossec/logs/alerts/alerts.json | \
  jq -r '[.rule.id, .rule.level, .rule.description] | @tsv' | \
  sort | uniq -c | sort -rn | head -10

# Your own rules exist and have fired at least once.
sudo cat /var/ossec/logs/alerts/alerts.json | \
  jq -r 'select(.rule.id | tonumber >= 100000) | .rule.description' | sort -u
```

## Pass criteria

- [ ] UBNT01 has at least 8 GB and the Wazuh manager is running (lesson 12.2)
- [ ] Every machine you intended to monitor shows `Active` in
      `agent_control -l` (lesson 12.2)
- [ ] Sysmon is installed on DC01 and its events reach the manager
      (lesson 12.3)
- [ ] You can explain what a decoder does versus a rule, and have used
      `wazuh-logtest` to see both (lesson 12.4)
- [ ] At least one custom rule of your own exists, with a comment saying what
      it detects and why that is suspicious here (lesson 12.4)
- [ ] You have counted your noisiest rules and tuned at least one, using level,
      condition or aggregation (lesson 12.5)
- [ ] You scanned your own lab, triaged the alert, and wrote the triage note
      (lesson 12.6)
- [ ] You can explain why a credentialed scan is indistinguishable from lateral
      movement (lesson 12.6)
- [ ] You can name three things visible about encrypted traffic without
      decrypting it (lesson 12.7)
- [ ] An agent going quiet raises an alert, and you tested it by stopping one
      (lesson 12.8)
- [ ] Detection rules are in Git, in Gitea, with messages explaining changes
      (lessons 12.4, 12.10)
- [ ] `Projects/lab-detection.md` lists every tuning exception and what each one
      silences (lesson 12.10)
- [ ] The indexer and dashboard are running with a tuned heap, and you changed
      the default credentials (lesson 12.9)
- [ ] You investigated one alert in the dashboard and found the **first** event
      in the sequence, not just the one that alerted (lesson 12.9)
- [ ] You can explain the difference between an event and a metric, and why
      they need different tools (lesson 12.10)
- [ ] Tier 3: Grafana shows alert volume over time, agents reporting, and your
      noisiest rules (lesson 12.10)

## What you can now say

That you built detection, not just collection, and that you can tell the
difference.

Three sentences worth having ready, because they are the ones that separate
someone who has run a SIEM from someone who has installed one:

**"An alert queue nobody reads is worse than none, because it also carries the
belief that you are covered."** Then the counting command, and what you tuned.

**"A credentialed vulnerability scan is indistinguishable from lateral
movement, because it is the same protocols with valid credentials. The
difference is authorisation, and authorisation is not in the packet."** Then
the exception you wrote, and the blind spot you accepted.

**"The detections most people are missing are the ones that fire on absence."**
Then the agent-disconnect rule, and the fact that you tested it by stopping an
agent rather than assuming.

Module 13 turns to vulnerability management, where the scanner you have just
learned to detect becomes a tool you operate on purpose.

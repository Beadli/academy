---
title: "10.11 Checkpoint: it runs twice and changes nothing"
sidebar_position: 11
---

# 10.11 Checkpoint: it runs twice and changes nothing

Prove the module stuck. The test that matters is idempotence: your automation
describes a state, and running it against a machine already in that state does
nothing at all.

## Commands

On UBNT01, in the virtual environment:

```bash
cd ~/ansible
source .venv/bin/activate

# The tool is installed and reachable from inside the environment.
ansible --version

# Every Linux host answers.
ansible linux -m ansible.builtin.ping

# The playbook reports no changes needed. This is the one that matters.
ansible-playbook harden.yml --check --diff

# And for real: changed=0.
ansible-playbook harden.yml

# The repository is clean and pushed.
git status --short
git log --oneline
```

Tier 2 and up:

```bash
# A live Kerberos ticket.
klist

# Windows answers over WinRM.
ansible windows -m ansible.windows.win_ping
```

## Pass criteria

- [ ] Ansible runs from a virtual environment at `~/ansible/.venv`, and you
      know it must be activated in a new shell (lesson 10.2)
- [ ] `ansible linux -m ansible.builtin.ping` returns `pong` for every Linux
      host in your inventory (lesson 10.2)
- [ ] `harden.yml` runs and reports `changed=0` on a second run (lessons 10.3,
      10.4)
- [ ] You broke a setting by hand, saw `--check --diff` detect the drift, and
      corrected it by re-running the playbook (lesson 10.4)
- [ ] `webserver.yml` deploys a templated config and restarts nginx **only**
      when the file changed (lesson 10.5)
- [ ] `requirements.yml` lists your collections, and `requirements.txt` your
      Python dependencies (lessons 10.2, 10.6)
- [ ] Tier 2: `klist` shows a current ticket and
      `ansible.windows.win_ping` succeeds (lesson 10.7)
- [ ] You destroyed a machine, rebuilt it from playbooks, and wrote down what
      the playbooks did not cover (lesson 10.8)
- [ ] The repository is in Gitea, `.venv/` is ignored, and no secrets are
      committed (lesson 10.9)
- [ ] `Projects/lab-automation.md` exists and includes the rebuild gap list
      (lesson 10.10)

## What you can now say

That you have automated a mixed Windows and Linux estate from one control
node, and tested a rebuild rather than assuming one.

The specific thing worth saying in an interview is the second half. Plenty of
people have written a playbook. **Far fewer have deliberately destroyed a
working machine, rebuilt it from their own automation, and written down the
gap between what they recovered and what they had.** That is a disaster
recovery test, and being able to describe what it revealed is a much better
answer than "yes, we use Ansible".

The other one is the rule this module opened with. You can explain why
automation you cannot read is worse than doing it by hand, and you can say it
from experience rather than as a slogan.

Module 11 turns to working with AI, which is the fourth rung of the ladder
lesson 1.6 described. It depends on this one for the same reason this one
depended on Module 6: **you can only safely delegate what you can verify.**

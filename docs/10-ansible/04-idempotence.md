---
title: "10.4 Idempotence, and why running it twice proves something"
sidebar_position: 4
---

# 10.4 Idempotence, and why running it twice proves something

:::note[Activate first]
Every command in this lesson runs on **UBNT01**, inside the virtual environment
from lesson 10.2.

```bash
cd ~/ansible
source .venv/bin/activate
```
:::

Run yesterday's playbook again.

```bash
ansible-playbook harden.yml
```

```text
PLAY RECAP ****************************************************
ubnt01   : ok=5  changed=0  unreachable=0  failed=0  skipped=0
```

**`changed=0`.** Nothing happened, and that is the most important output in
this module.

## The word

**Idempotent**: an operation you can perform repeatedly and get the same result
as performing it once.

Compare two ways of saying the same thing.

A script says `apt install htop`. Run it twice and it runs twice. It is
probably harmless here, but the script does not know or care whether it needed
to do anything.

A playbook says `state: present`. Ansible checks whether htop is installed. If
it is, it reports `ok` and moves on without touching the machine.

The script describes an **action**. The playbook describes a **state**. That is
the whole difference between scripting and configuration management, and it is
why lesson 2.4's "why Python over Bash?" has a third answer: for this kind of
work, often neither, because you want to describe the destination rather than
the journey.

## Why it changes what automation is for

If running your automation is safe, you can run it constantly.

**It becomes a check, not just a change.** `--check` against your whole fleet
answers "is everything still as we said?" without touching anything.
`changed=0` everywhere means no drift. Any `changed` is a machine that has
wandered, or a change somebody made by hand and did not tell you about.

**It becomes safe to re-run after a failure.** A task fails halfway through,
you fix it, you run the whole thing again. No unpicking, no "which bits already
happened". That is not true of a shell script, where re-running the first half
may do damage.

**It becomes the source of truth.** If the playbook is authoritative and runs
regularly, the file *is* the configuration. A server that disagrees is wrong,
and running the playbook corrects it. Organisations run this on a schedule and
call it enforcement.

:::tip[Idempotence is everywhere once you have the word]
You have already met it several times without a name.

`mkdir -p` succeeds whether or not the directory exists, which is exactly why
it is the idempotent version of `mkdir`. `git checkout` of a branch you are
already on does nothing. A DNS record set to the value it already has is not a
change. Terraform, Kubernetes and Puppet are all built on the same idea.

Once you have the word you start noticing which tools have it and which do
not, and that turns out to be one of the more useful ways to judge a tool.
:::

## Prove it properly

Break something by hand, then let the playbook notice.

```bash
# Undo one of the hardening settings, the way a colleague "just testing
# something" would.
sudo sed -i 's/^PermitRootLogin no/PermitRootLogin yes/' /etc/ssh/sshd_config
grep '^PermitRootLogin' /etc/ssh/sshd_config
```

Now ask Ansible what it thinks, without letting it act:

```bash
ansible-playbook harden.yml --check --diff
```

It reports one task as `changed`, and `--diff` shows you the exact line. You
have just detected configuration drift on a machine, from a file, without
logging in to look.

Put it right:

```bash
ansible-playbook harden.yml
```

`changed=1`. Run it once more and you are back to `changed=0`.

**That loop is what configuration management is.** Describe the state, detect
the drift, correct it, confirm. Everything else is detail.

## Where idempotence leaks

Honesty matters more than the tidy version, and the tidy version is not quite
true.

**`command` and `shell` are not idempotent.** They run whatever you give them,
every time, and Ansible cannot know what the command does.

```yaml
# Ansible has no idea what this does. It will run on every play.
- name: Do a thing
  ansible.builtin.command: /usr/local/bin/something.sh
```

The fix is to tell it when to bother, either with `creates:` (skip if this file
exists) or a `when:` condition. If you find yourself with a playbook full of
`command` tasks, you are writing a shell script in YAML, and you have lost the
property that makes this worth doing.

**Modules vary in quality.** Most core modules are properly idempotent. Some
community ones report `changed` every run because checking properly is hard.
`--check` is how you find out which you are dealing with.

**Some things genuinely cannot be.** Rebooting a machine is not idempotent in
any useful sense. Ansible handles this with handlers, which is lesson 10.5.

The rule of thumb: **prefer a module over `command`, always, and if you must
use `command`, tell it when to skip.**

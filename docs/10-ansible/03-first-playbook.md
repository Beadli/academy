---
title: "10.3 Your first playbook: Module 6's hardening, done properly"
sidebar_position: 3
---

# 10.3 Your first playbook: Module 6's hardening, done properly

:::note[Activate first]
Every command in this lesson runs on **UBNT01**, inside the virtual environment
from lesson 10.2. A fresh shell is always outside it:

```bash
cd ~/ansible
source .venv/bin/activate
```
:::

In lesson 6.3 you hardened a server by hand. This lesson writes that down as a
file, and the file is the point: it is documentation that executes.

## What a playbook is

A YAML file listing **tasks**, each saying what state something should be in,
against a group of **hosts** from your inventory.

Create `~/ansible/harden.yml`:

```yaml
---
- name: Baseline hardening for Linux servers
  hosts: linux
  become: true          # do it as root, via sudo

  tasks:
    - name: Package list is up to date
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600

    - name: Useful tools are present
      ansible.builtin.apt:
        name:
          - htop
          - curl
          - unattended-upgrades
        state: present

    - name: Root cannot log in over SSH
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PermitRootLogin'
        line: 'PermitRootLogin no'
        validate: 'sshd -t -f %s'

    - name: SSH is running and starts at boot
      ansible.builtin.systemd_service:
        name: ssh
        state: started
        enabled: true
```

## Read it before you run it

That is the rule from 10.1, and this is the first chance to apply it. Every
line above is something you did by hand in Module 6.

**`hosts: linux`** points at the group in your inventory, not at a machine.
Add ten servers to that group and this file covers them without changing.

**`become: true`** is `sudo`. Ansible connects as your normal user and elevates
per task, which is the same least-privilege instinct lesson 5.6 taught.

**`update_cache` with `cache_valid_time`** is `apt update`, but only if the
cache is older than an hour. Already the declarative habit: not "run apt
update", but "the package list should be current".

**`state: present`** on a package means "installed". Not "install it". If it
is already there, Ansible does nothing at all. Lesson 10.4 is about why that
distinction is the most important idea in the module.

**`lineinfile` with `validate`** is the interesting one. It ensures a line
exists in a file, and `validate` runs `sshd -t` against the *proposed* file
before replacing the real one. If your change would produce a broken SSH
configuration, Ansible refuses to install it.

Sit with that for a second. You are editing the configuration of the service
you are connected over. Getting it wrong locks you out of the machine. The
`validate` line is what makes that safe, and it is the sort of thing you only
think to add after you have locked yourself out once.

## Run it, but not really

Ansible has a mode that reports what *would* change without changing anything.
Use it every time.

```bash
# --check is a dry run. --diff shows the actual file changes it would make.
ansible-playbook harden.yml --check --diff
```

Read the output. Tasks are `ok` (already correct), `changed` (would be
altered), or `failed`. On a machine you hardened by hand in Module 6, several
should already be `ok`, which is quietly satisfying.

:::tip[`--check` is the habit that separates the confident from the lucky]
This is the practical form of "never run automation you cannot read". You read
it, then you have the machine tell you what it thinks the file means.

It is not perfect. A task whose result depends on an earlier task's change
cannot always be predicted in check mode, and Ansible will say so. But it
catches the class of mistake that matters: the task pointed at the wrong
group, the setting inverted, the file path wrong.

Run `--check --diff` first. Every time. It costs seconds.
:::

## Now run it for real

```bash
ansible-playbook harden.yml
```

The recap at the bottom is the bit to read:

```text
PLAY RECAP ****************************************************
ubnt01   : ok=5  changed=2  unreachable=0  failed=0  skipped=0
```

`changed=2` means two things were not as described and now are. `ok=3` means
three already matched.

## The thing you just gained

You now have a file that describes what a hardened server looks like in your
lab. It is readable by a colleague, it lives in Git from lesson 10.9, and it
answers "what is our hardening standard?" with a file rather than a person's
memory.

That is the drift problem from 10.1, solved. Not by being careful. By writing
it down in a form that executes.

## When it fails

**`Missing sudo password`.** Your user needs passwordless sudo, or you need to
pass `--ask-become-pass`. The second is the safer default for a lab.

**`Failed to connect to the host via ssh`.** The connection worked in 10.2, so
something changed: wrong user in the inventory, a key not loaded, or the host
key changed. Test it the plain way first, `ssh sam@10.10.10.20`, because
Ansible's error is a wrapper around whatever SSH said.

**A task fails and the play stops.** That is deliberate. Ansible stops on the
first failure for a host rather than continuing into an unknown state. Read
the error, fix the task, run again. Because the tasks are declarative, running
it again from the top is safe, which is exactly what 10.4 is about.

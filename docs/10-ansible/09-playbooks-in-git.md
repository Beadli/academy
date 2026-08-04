---
title: "10.9 Playbooks belong in Git"
sidebar_position: 9
---

# 10.9 Playbooks belong in Git

:::note[Activate first]
Commands run on **UBNT01**, inside the virtual environment from lesson 10.2.

```bash
cd ~/ansible
source .venv/bin/activate
```
:::

You have a directory of files that describe how your servers are configured.
Right now it exists on one machine, with no history, and if UBNT01 dies it goes
with it.

## Put it under version control

The rhythm is the one from lesson 1.3, on different content.

```bash
cd ~/ansible
git init -b main

# Confirm .venv is ignored, from lesson 10.2. If it is not, fix that first:
# committing thousands of generated files is a mess to undo.
cat .gitignore
git status --short
```

```bash
git add -A
git commit -m "ansible: baseline hardening and reverse proxy"
```

Push it to the Gitea server you built in lesson 6.6, alongside your journal:

```bash
git remote add origin http://git.lab.internal/sam/ansible.git
git push -u origin main
```

Lesson 6.8 said that when Module 10 automated deployments they would land in
the same place as everything else. They have.

## Now the question from lesson 1.7

Lesson 1.7 suggested "why does Git need a staging step at all?" as a good open
question, and said this module would make the answer obvious. Here it is.

Staging exists so a commit can be a **deliberate unit of change** rather than
a snapshot of whatever happened to be on disk.

That distinction is abstract when you are writing notes. It stops being
abstract when the files decide what runs on your servers.

Picture the state you are in half an hour from now. You have edited
`harden.yml` to add a firewall rule, which is tested and ready. You have also
started rewriting `webserver.yml`, which is half-finished and would break if
it ran. And you fixed a typo in a template.

Without staging, `git commit` takes all three. Your history now contains one
commit that says "add firewall rule" and also contains a broken web server
config. When something breaks next week and you look for the change that
caused it, that commit lies to you.

With staging, you choose:

```bash
# Just the finished work.
git add harden.yml templates/site.conf.j2
git commit -m "harden: allow monitoring from the SIEM host"

# The half-finished rewrite stays on disk, uncommitted, until it works.
git status --short
```

Two commits, each doing one thing, each honest about what it contains.

:::tip[Why this matters more for playbooks than for notes]
A commit against a repository that configures machines is a **change record**.
It is the thing you read during an incident to answer "what did we change?".

That is why the discipline is worth having: not because Git demands it, but
because a history of clean, single-purpose commits is the difference between
answering that question in thirty seconds and reading a diff of nine unrelated
edits hoping something jumps out.

In organisations this becomes formal. A change goes in a branch, someone else
reviews the diff, it merges, and *then* it runs. **The review is only possible
because the diff is small and about one thing.** Staging is where that starts.
:::

## What not to commit

**Never commit secrets.** Not passwords, not API keys, not the Kerberos
password from 10.7. Lesson 1.6's rule about keeping secrets out of places they
will be read applies with force here, because this repository is *designed* to
be shared with colleagues.

Ansible's answer is **Ansible Vault**, which encrypts a file so it can live in
the repository safely:

```bash
# Create an encrypted variables file. It will ask for a password.
ansible-vault create group_vars/windows_secret.yml

# Edit it later.
ansible-vault edit group_vars/windows_secret.yml

# Playbooks that use it need the password at run time.
ansible-playbook windows-baseline.yml --ask-vault-pass
```

The file in Git is ciphertext. The password is not in the repository, which
means it has to live somewhere else, and "somewhere else" is a real decision
rather than a detail. In a lab, your password manager. In an organisation, a
secrets manager the automation can authenticate to.

**Do not commit `.venv/`**, which 10.2 already handled, or generated inventory
files that contain live addresses you would rather not publish.

## What this repository is now

Read back what you have.

`harden.yml` is your hardening standard. `webserver.yml` is how your reverse
proxy is configured. `requirements.yml` and `requirements.txt` are what your
automation depends on. The Git history is every change, when, and why.

**That is documentation that cannot go stale**, because it is the thing that
runs. Every other kind of infrastructure documentation drifts from reality the
moment someone makes a change in a hurry. This kind cannot, because a change
that is not in here does not happen.

That is the strongest argument for infrastructure as code, and it is worth
being able to make it in an interview. Not "it is faster". It is that the
documentation and the system stop being two things that can disagree.

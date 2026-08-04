---
title: "10.6 Roles and Galaxy: other people's automation"
sidebar_position: 6
---

# 10.6 Roles and Galaxy: other people's automation

:::note[Activate first]
Every command in this lesson runs on **UBNT01**, inside the virtual environment
from lesson 10.2.

```bash
cd ~/ansible
source .venv/bin/activate
```
:::

Your playbooks work and they are getting long. This lesson is about
structuring them, and then about the more interesting question of whether to
use somebody else's.

## Roles: a playbook with a filing system

A **role** is a directory layout Ansible understands. Put tasks in
`tasks/main.yml`, templates in `templates/`, variables in `defaults/main.yml`,
handlers in `handlers/main.yml`, and Ansible finds them without being told.

```bash
# Scaffold one. This creates the directory structure for you.
ansible-galaxy init roles/webserver
```

Look at what it made:

```bash
find roles/webserver -type d | sort
```

Move lesson 10.5's work into it: the tasks into `roles/webserver/tasks/main.yml`
(without the `hosts:` and `tasks:` wrapper), the template into
`roles/webserver/templates/`, the handler into
`roles/webserver/handlers/main.yml`, and the variables into
`roles/webserver/defaults/main.yml`.

The playbook then becomes almost nothing:

```yaml
---
- name: Reverse proxy configuration
  hosts: linux
  become: true
  roles:
    - webserver
```

**Why bother.** A role is reusable across playbooks, testable on its own, and
the structure means a stranger knows where to look. `defaults/main.yml` is
specifically the file that says "here are the knobs", which is how you use a
role you did not write without reading all of it.

## Galaxy: the shared library

**Ansible Galaxy** is the public repository of roles and collections other
people have written. There is one for almost everything: databases, web
servers, monitoring agents, cloud providers.

```bash
# Install a collection, the same way you will install ansible.windows in 10.7.
ansible-galaxy collection install community.general

# What do you have?
ansible-galaxy collection list
```

Pinning what you depend on belongs in a file, not in your shell history.
Create `~/ansible/requirements.yml`:

```yaml
---
collections:
  - name: community.general
  - name: ansible.windows
```

```bash
ansible-galaxy collection install -r requirements.yml
```

That file goes into Git in 10.9, next to your `requirements.txt` from 10.2.
Same instinct both times: **describe the dependency, do not commit the
dependency.**

## The decision lesson 1.2 warned you about

Here is the part that matters more than the syntax.

When you install a role from Galaxy and run it with `become: true`, you are
executing code you did not write, as root, on every machine in the group.

Lesson 1.2 made you evaluate an Obsidian plugin before installing it, and
called it your first supply chain decision. This is the same decision with
considerably more blast radius. A bad Obsidian plugin reads your notes. A bad
Ansible role owns your servers.

:::tip[The same four questions, asked of a role]
1. **How many people use it?** Galaxy shows download counts. A role with a
   handful is one nobody else has checked.
2. **When was it last updated?** An unmaintained role targets an OS release
   that has moved on, and the failure will be confusing rather than clean.
3. **Can I read what it does?** This is the one that changes here. Roles are
   YAML, and YAML is readable. **You can actually open it and check**, which is
   not true of a compiled binary or a minified script. `ansible-galaxy` puts
   roles in `~/.ansible/roles/`; go and look.
4. **Do I need it?** A role that installs a package and writes a config file is
   twenty lines you could write and fully understand. Reach for other people's
   work when it encapsulates something genuinely fiddly, not to save yourself
   an afternoon's reading.
:::

Question three is the one to lean on. Because the format is human-readable, the
honest position is not "trust it" or "avoid it", it is **read it, then decide**.
That is a luxury you rarely get with dependencies, and it is worth using.

```bash
# Where installed roles land, and what is in them.
ls ~/.ansible/roles/
```

**And run it against one machine first**, in `--check` mode, reading the diff.
Everything in 10.1 and 10.3 applies double when the tasks are not yours.

## Where I would draw the line

Not a rule, an opinion you are free to disagree with once you have your own.

**Write your own** for anything that encodes your organisation's decisions:
hardening standards, application deployments, the specific way you lay out a
server. That knowledge is the valuable part and it should be readable in your
own repository.

**Use somebody else's** for things that are genuinely intricate and widely
solved, where the role encodes hard-won knowledge about a product's quirks and
you would get it subtly wrong.

**Read either way.** The difference between the two is not trust, it is how
much reading you have to do before you understand what will run.

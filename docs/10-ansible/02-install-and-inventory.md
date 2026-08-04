---
title: "10.2 Install Ansible, describe your lab, run your first command"
sidebar_position: 2
---

# 10.2 Install Ansible, describe your lab, run your first command

Everything in this module happens **on UBNT01**, over SSH from your own
machine. That is the control node, and it is the only machine that needs
Ansible installed.

## First, the Python problem nobody warned you about

Ansible is a Python application, and installing Python applications is where
people meet a problem the language has spent twenty years arguing about.

Module 2.3 had you install Python and write a script. It did not have you
install any **libraries**, which is where it gets interesting.

If you `pip install` something system-wide, it goes into the same place every
other Python program on the machine looks. Two applications wanting different
versions of the same library cannot both be satisfied, and on Ubuntu there is
a worse version of this: parts of the operating system are written in Python,
and installing libraries system-wide can break them. Modern Ubuntu will
actually refuse and tell you the environment is "externally managed".

The answer, and the thing every Python developer does without thinking, is a
**virtual environment**: a private directory holding its own copy of Python and
its own libraries, belonging to one project. Install what you like into it, and
nothing outside it notices.

## Create one for your automation

```bash
# A home for this module's work. Everything here goes into Git in 10.9.
mkdir -p ~/ansible
cd ~/ansible

# Ubuntu ships venv as a separate package.
sudo apt update
sudo apt install -y python3-venv

# Create the environment. The dot makes it hidden, and keeping it inside
# the project is the convention: the environment belongs to this work,
# not to you.
python3 -m venv .venv
```

Look at what that made:

```bash
ls .venv
```

`bin`, `lib`, and a few others. It is a small, self-contained Python
installation sitting in your project folder.

### Activate it

```bash
source .venv/bin/activate
```

Your prompt changes to show `(.venv)`. That prefix is the whole user
interface: it is telling you which Python you are currently talking to.

```bash
# Confirm. This should now point inside your project, not to /usr/bin.
which python3
```

### Install Ansible into it

```bash
pip install ansible
```

No `sudo`. That is the point: you are writing into a directory you own, not
into the system. If you find yourself typing `sudo pip`, stop and work out
which environment you meant.

```bash
# Confirm. Expect a version, and a path inside .venv.
ansible --version
```

:::warning[The failure you will hit, probably next week]
You will come back to this in a few days, type `ansible`, and get:

```text
ansible: command not found
```

Nothing is broken. **You did not activate the environment.** A new shell starts
outside it, every time, by design.

```bash
cd ~/ansible
source .venv/bin/activate
```

This catches everybody once. The prompt prefix exists precisely so you can
see, at a glance, whether you are inside. When a Python tool vanishes, that is
the first thing to check.

To leave deliberately: `deactivate`.
:::

:::tip[The other way, and why the docs suggest it]
Ansible's own installation guide recommends **pipx**, which installs Python
*applications* into their own environments automatically and puts them on your
PATH so there is nothing to activate.

It is genuinely nicer for tools you use everywhere, and pipx is built on venv:
it is a convenience layer over the thing you just did by hand.

We are doing it the manual way because **venv is the transferable skill**.
Every Python project you ever touch will want one, most of them will not be
applications pipx can install, and "the environment was not activated" is one
of the most common confusions in the language. Meeting it here, on purpose, is
worth the extra command.

If you would rather use pipx afterwards, `sudo apt install pipx` then
`pipx install --include-deps ansible` gets you there.
:::

### Keep it out of Git

A virtual environment is generated, not authored. It contains thousands of
files, it is specific to this machine's architecture, and it is rebuilt from
one command. It has no business in a repository.

You will put this directory under version control in lesson 10.9. Set the rule
now, while you are thinking about it:

```bash
# The ignore file for this project, using the mechanism from lesson 1.3.
echo ".venv/" > ~/ansible/.gitignore
```

The reproducible part is not the environment, it is the *list of what goes in
it*, which is why Python projects commit a requirements file and not the
libraries:

```bash
# What is installed, in a form another machine can rebuild from.
pip freeze > requirements.txt
```

Anyone cloning your repository runs `python3 -m venv .venv`,
`source .venv/bin/activate`, `pip install -r requirements.txt`, and has what
you have. That is the same instinct as the Docker Compose file in lesson 6.5:
describe it, do not ship it.

## Describe your lab

Ansible needs to know what machines exist. That list is the **inventory**, and
it is just a file.

Create `~/ansible/inventory.ini`, alongside the environment you just made:

```ini
# Linux machines Ansible reaches over SSH.
[linux]
ubnt01 ansible_host=10.10.10.20

# Windows machines. Lesson 10.7 makes these work; they are listed now
# so the shape of the file is clear.
[windows]
dc01 ansible_host=10.10.10.10
subca01 ansible_host=10.10.10.30

# Variables that apply to every host in the [linux] group.
[linux:vars]
ansible_user=sam
ansible_python_interpreter=/usr/bin/python3
```

Substitute your own username and addresses. The addresses come from the plan
you wrote in lesson 4.3, which is exactly why that lesson made you write one
down.

**The square brackets are groups.** A group is a name for a set of machines,
and you point a playbook at a group rather than at a list of addresses. That
is the whole idea: you write automation for "web servers", not for
"10.10.10.20 and 10.10.10.21 and the new one Dave added".

## Reach out and touch something

Before any playbook, prove the connection works. Ansible can run a single
command without a playbook at all, which is called an **ad hoc** command and is
genuinely useful for answering questions across a fleet.

```bash
# The simplest possible test: are you there?
ansible linux -i inventory.ini -m ansible.builtin.ping
```

Expect `"ping": "pong"` and `SUCCESS`. If you get that, the plumbing works.

That is not an ICMP ping. It is Ansible connecting over SSH, running a small
Python module on the far end, and getting a structured answer back. It proves
SSH works, the user is right, and Python is present on the target, which are
the three things that break.

```bash
# Something more useful: what is actually running out there?
ansible linux -i inventory.ini -m ansible.builtin.setup -a "filter=ansible_distribution*"

# Run an arbitrary command on every machine in the group.
ansible linux -i inventory.ini -m ansible.builtin.command -a "uptime"
```

:::tip[Those dotted names are collections, and they matter]
`ansible.builtin.ping` looks verbose next to `ping`, and the short form still
works. Use the long one anyway.

Ansible's functionality is packaged into **collections**, each with a
namespace. `ansible.builtin` ships with Ansible itself. `ansible.windows`, which
you install in 10.7, is separate. `community.general` is a large collection
maintained by the community.

Writing the full name makes it obvious where a module comes from and therefore
who maintains it, which is exactly the question lesson 10.6 is about. Short
names also become ambiguous the moment two collections offer something
similarly named, and the resulting error is not one you want to debug.
:::

## Stop typing `-i inventory.ini`

Create `~/ansible/ansible.cfg`:

```ini
[defaults]
inventory = inventory.ini
host_key_checking = True
interpreter_python = auto_silent
```

Now the commands get shorter:

```bash
ansible linux -m ansible.builtin.ping
```

:::warning[Do not turn off host key checking]
You will find `host_key_checking = False` in a great many blog posts and
example configurations, because it makes a warning go away.

That warning is SSH telling you it cannot confirm the machine is the one you
connected to last time, which is the entire mechanism protecting you from
connecting to an impostor. Turning it off across a fleet means your automation
will happily authenticate to anything answering on that address.

You met the same idea in lesson 6.2 when SSH asked you to confirm a
fingerprint. The answer then was to look at it rather than dismiss it. It is
still the answer.
:::

## What you have

A control node, a description of your lab, and a proven connection to it. No
agent was installed on anything.

Lesson 10.3 turns that connection into something worth having.

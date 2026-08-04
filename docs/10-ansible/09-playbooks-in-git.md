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

## Running it without you

Sooner or later you will want a playbook to run on a schedule rather than
because you typed something. There is a trap waiting there, and it is
specific to how you installed Ansible.

**Activation does not survive into automation.** `source .venv/bin/activate`
edits the PATH of *one interactive shell*. Cron and systemd do not read your
shell profile, do not run `.bashrc`, and start with a minimal PATH. A scheduled
job that says `ansible-playbook harden.yml` fails with `command not found`, and
the error tells you nothing about why.

**The fix is to stop relying on PATH at all.** Every executable inside a
virtual environment carries a shebang naming that environment's own Python:

```bash
# Look at the top line. It is an absolute path into .venv.
head -1 ~/ansible/.venv/bin/ansible-playbook
```

Because of that line, calling the binary by its full path works with no
activation and no PATH:

```bash
/home/sam/ansible/.venv/bin/ansible-playbook /home/sam/ansible/harden.yml
```

That is the form to use in anything scheduled. Activation is a convenience for
humans; the shebang is what actually makes the environment work.

:::info[This is not a venv problem]
Worth knowing, because it looks like one.

If you had installed Ansible with pipx instead, its binaries land in
`~/.local/bin`, which is on your PATH only because your shell profile puts it
there. A non-interactive shell does not have it either, and cron has less
still. The same job fails the same way.

**Anything installed per-user needs an absolute path in automation.** Using
the full path is arguably better here anyway: reading the crontab or unit file
tells you exactly which environment ran, which matters the day two projects
need different Ansible versions.
:::

### The cron version

Cron is what most people reach for, so here is the working form:

```bash
# Edit your own crontab.
crontab -e
```

```cron
# Run the hardening playbook at 03:00 daily.
0 3 * * * cd /home/sam/ansible && ./.venv/bin/ansible-playbook harden.yml >> /home/sam/ansible/logs/harden.log 2>&1
```

Three parts of that line are doing necessary work, and leaving any of them out
is a different failure:

**`cd /home/sam/ansible` first.** Ansible looks for `ansible.cfg` in the
current directory, and cron starts you in your home directory. Without the
`cd`, your config is not found, the inventory setting from 10.2 is not applied,
and the run fails with "no hosts matched" rather than anything about config.

**`./.venv/bin/ansible-playbook`, not `ansible-playbook`.** The absolute-path
rule. Having done the `cd`, the relative form works and reads clearly.

**`>> ... 2>&1` to a log file.** Cron mails output to the local user by
default, which on a lab machine means it goes nowhere anyone reads. Send it
somewhere you can look:

```bash
mkdir -p ~/ansible/logs
echo "logs/" >> ~/ansible/.gitignore
```

An alternative that avoids the `cd`, if you prefer absolute paths throughout:

```cron
0 3 * * * ANSIBLE_CONFIG=/home/sam/ansible/ansible.cfg /home/sam/ansible/.venv/bin/ansible-playbook /home/sam/ansible/harden.yml >> /home/sam/ansible/logs/harden.log 2>&1
```

:::tip[Test it the way cron will run it, not the way you run it]
The reason these jobs fail mysteriously is that you test them in a shell that
has your PATH, your working directory and your environment, and cron has none
of those.

Reproduce cron's conditions before scheduling anything:

```bash
# env -i strips the environment completely, which is closer to cron
# than your shell will ever be.
env -i /bin/sh -c 'cd /home/sam/ansible && ./.venv/bin/ansible-playbook harden.yml --check'
```

If that works, the crontab line will work. If it does not, you have found the
problem at a keyboard rather than at 3am in a log nobody was reading.
:::

### A systemd timer, rather than cron

You met systemd in lesson 6.3, where you used `systemctl` to start and enable
services. A **timer** is the same system's answer to scheduled jobs, and it is
a better answer than cron for this.

Two files. First `/etc/systemd/system/ansible-harden.service`, which describes
the work:

```ini
[Unit]
Description=Apply baseline hardening playbook
After=network-online.target

[Service]
Type=oneshot
User=sam
WorkingDirectory=/home/sam/ansible
ExecStart=/home/sam/ansible/.venv/bin/ansible-playbook harden.yml
```

Then `/etc/systemd/system/ansible-harden.timer`, which describes when:

```ini
[Unit]
Description=Run baseline hardening daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ansible-harden.timer

# When does it next run, and when did it last?
systemctl list-timers ansible-harden.timer

# What happened last time? This is the part cron makes hard.
journalctl -u ansible-harden.service -n 50
```

Three reasons to prefer this over a crontab line. **The output goes to the
journal**, so lesson 6.3's `journalctl` shows you exactly what the last run
did, rather than cron mailing it somewhere nobody reads. **`Persistent=true`**
runs a missed job after the machine comes back up, which cron does not.
And **the failure is visible**: a failed service shows in `systemctl` rather
than being silent.

### Should you, though?

A playbook that runs unattended is **enforcement**. Drift gets corrected
without anyone deciding, which is exactly what you want for a hardening
baseline and exactly what you do not want for something you have not read
carefully.

The rule from lesson 10.1 does not soften here, it hardens. Scheduling
automation you have not read means it does the thing you did not check, on a
timer, while you are asleep.

A reasonable progression, and the one most organisations arrive at eventually:

1. Run it by hand, with `--check --diff`, until the output is boring
2. Schedule it in `--check` mode only, so it **reports** drift without
   correcting it
3. Once you trust both the playbook and the reporting, let it enforce

Step two is the one people skip, and it is the valuable one. A daily job that
tells you which machines have drifted, changing nothing, is genuinely useful
long before you are ready to let anything change itself.

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

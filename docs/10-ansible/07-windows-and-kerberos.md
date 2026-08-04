---
title: "10.7 Windows: WinRM, Kerberos, and the traps"
sidebar_position: 7
---

# 10.7 Windows: WinRM, Kerberos, and the traps

:::note[Activate first, and this one is Tier 2 and up]
Commands run on **UBNT01** inside the virtual environment from 10.2, unless a
step says otherwise. You need the domain from Module 5.

```bash
cd ~/ansible
source .venv/bin/activate
```
:::

The Linux half of this module went quickly. This half will not, and it is
worth saying why up front rather than letting you conclude you are doing
something wrong.

Ansible reaches Linux over SSH, which was already working before you started.
Windows has no SSH by default. It has **WinRM**, short for Windows Remote
Management: Microsoft's protocol for running commands on a machine from
somewhere else. It is what PowerShell remoting uses, so if you have ever run
`Enter-PSSession`, you have used it. It has its own authentication story, and the good version of that story is
**Kerberos**, which is exquisitely sensitive to things being slightly wrong.

The payoff is real: managing Windows and Linux from one tool, with one
inventory, is a genuinely valuable thing to be able to say you have done.

## What has to be true

Four things, and every failure in this lesson is one of them.

**WinRM is listening on the Windows host.** On Windows Server it is enabled by
default, which is one thing in your favour.

**The control node speaks Kerberos.** UBNT01 needs Kerberos client libraries
and a configuration file naming your realm.

**Names resolve, forwards and backwards.** Kerberos identifies services by
name. If UBNT01 cannot resolve `dc01.lab.internal`, or resolves it to an
address that does not resolve back to the same name, authentication fails in a
way whose error message will not mention DNS.

**Clocks agree, within five minutes.** Kerberos tickets are timestamped, and
excessive skew is rejected as a replay defence.

:::warning[The clock one will get you, and Module 3 warned you]
Lesson 3.3 made a point about virtual machine clocks drifting, particularly
after a snapshot restore or a suspended host waking up. This is where that
comes due.

Kerberos rejects tickets outside a five-minute window. The error you get says
nothing useful about time; you will chase DNS and credentials for an hour first.

**Check the clocks before you debug anything else.** It costs one command and
it is the single most common cause.
:::

## Prepare the control node

```bash
# Kerberos client libraries, from Ubuntu.
sudo apt update
sudo apt install -y krb5-user libkrb5-dev

# Python bindings, into your virtual environment. No sudo: this goes in .venv.
pip install "pywinrm[kerberos]"

# The Windows modules.
ansible-galaxy collection install ansible.windows
```

Installing `krb5-user` prompts for a default realm. Enter your domain in
**capitals**: `LAB.INTERNAL`. If you get it wrong, edit `/etc/krb5.conf`
afterwards.

Check `/etc/krb5.conf` looks roughly like this:

```ini
[libdefaults]
    default_realm = LAB.INTERNAL

[realms]
    LAB.INTERNAL = {
        kdc = dc01.lab.internal
        admin_server = dc01.lab.internal
    }

[domain_realm]
    .lab.internal = LAB.INTERNAL
    lab.internal = LAB.INTERNAL
```

:::warning[The capitals are not a style choice]
`LAB.INTERNAL` and `lab.internal` are different strings to Kerberos. The realm
is conventionally uppercase and the DNS domain is lowercase, and they appear
within two lines of each other in this file doing different jobs.

Getting this wrong produces `Cannot find KDC for realm "lab.internal"`, which
at least names the problem, so it is one of the kinder failures here.
:::

## Get a ticket

```bash
# Ask the domain controller for a ticket, as your admin account from 5.6.
kinit sokoth.adm@LAB.INTERNAL

# What have you got, and when does it expire?
klist
```

`klist` should show a ticket for `krbtgt/LAB.INTERNAL@LAB.INTERNAL`. That is
your ticket-granting ticket, and having one means Kerberos works independently
of Ansible. **Get this working before involving Ansible at all**, because it
halves the number of things that can be wrong.

If `kinit` fails:

- `Cannot find KDC` means `/etc/krb5.conf` or DNS
- `Clock skew too great` is the timing trap, named plainly for once
- `Preauthentication failed` is a wrong password
- `Client not found in Kerberos database` is a wrong username or realm case

## Tell Ansible about Windows

Add to `~/ansible/inventory.ini`:

```ini
[windows:vars]
ansible_connection=winrm
ansible_winrm_transport=kerberos
ansible_port=5985
ansible_user=sokoth.adm@LAB.INTERNAL
```

**Change the Windows hosts from addresses to names.** Lesson 10.2 wrote them
as `dc01 ansible_host=10.10.10.10`, which is fine for SSH and wrong here:
Kerberos authenticates against a service's *name*, so an address will fail
authentication even though the machine is perfectly reachable.

```ini
[windows]
dc01 ansible_host=dc01.lab.internal
subca01 ansible_host=subca01.lab.internal
```

That is the distinction 10.2 flagged: the inventory name is the label, and
`ansible_host` is where to connect. Here the connection target has to be a
name your DNS resolves. Confirm UBNT01 can:

```bash
# Both should work, and the second should return the name you started with.
dig +short dc01.lab.internal
dig +short -x 10.10.10.10
```

That reverse lookup is the one people skip. Lesson 6.7 had you set up DNS in
this lab, which is why you have somewhere to fix it if the second command
comes back empty.

## Try it

```bash
ansible windows -m ansible.windows.win_ping
```

Expect `"ping": "pong"`. That is a different module from `ansible.builtin.ping`
and the difference is real: one runs Python on the target, the other does not,
because Windows has no Python and does not need any.

Something more useful:

```bash
ansible windows -m ansible.windows.win_shell -a "Get-Service W32Time | Select-Object Status"
```

## A Windows playbook

Create `~/ansible/windows-baseline.yml`:

```yaml
---
- name: Windows baseline
  hosts: windows
  gather_facts: true

  tasks:
    - name: Time service is running and starts at boot
      ansible.windows.win_service:
        name: W32Time
        state: started
        start_mode: auto

    - name: Report the last boot time
      ansible.windows.win_shell: |
        (Get-CimInstance Win32_OperatingSystem).LastBootUpTime
      register: boot
      changed_when: false

    - name: Show it
      ansible.builtin.debug:
        var: boot.stdout_lines
```

```bash
ansible-playbook windows-baseline.yml --check
ansible-playbook windows-baseline.yml
```

Note `changed_when: false` on the shell task. `win_shell` runs a command, and
Ansible cannot know whether reading the boot time changed anything, so by
default it reports `changed`. Telling it otherwise keeps `changed=0` meaningful,
which is the property lesson 10.4 spent a whole lesson on.

No `become:` here. Windows privilege works differently: you connect *as* an
account that already has the rights, which is why the inventory names your
admin account.

## The debugging order

When it fails, and it will, work through it in this order rather than
searching the error text. These are cheap to check and they are the actual
causes.

1. **Clocks.** `date` on UBNT01, `Get-Date` on the Windows host. Within five
   minutes?
2. **Ticket.** Does `klist` show a current, unexpired ticket? They expire.
3. **Names.** Forward and reverse resolution, from UBNT01, using the exact name
   in your inventory.
4. **Case.** Realm uppercase everywhere it appears.
5. **Only then** turn up Ansible's own verbosity: `-vvv`.

:::info[Windows now has an SSH option, and it is worth knowing]
Recent Windows Server versions can run an OpenSSH server, and Ansible can use
it, which sidesteps WinRM and Kerberos entirely.

This lesson teaches WinRM with Kerberos because it is what you will find in
existing environments, it is what domain-joined Windows expects, and the
Kerberos knowledge transfers to everything else Windows authenticates.

If you meet a greenfield Windows estate someday, SSH may well be the simpler
answer. Knowing both exist, and why one is common, is the useful position.
:::

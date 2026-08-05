---
title: "15.6 Automate the vulnerability loop"
sidebar_position: 6
---

# 15.6 Automate the vulnerability loop

Lesson 13.7 ended with this:

> One round of patching is a task. Vulnerability management is the loop:
> scan, prioritise, fix, **scan again to prove it**, repeat on a schedule.
> That loop is what you will automate in Module 15.

Here it is. **This lesson needs the Ansible from Module 10**, and it is where
that module stops being a demonstration and becomes something you run.

## What you should and should not automate

Start with the judgement, because the automation is easy and the judgement is
what stops it hurting you.

**Automate the tedious and repeatable:** refreshing package lists, reporting
what would change, applying updates on machines where a mistake is cheap,
running the scan, collecting the results.

**Do not automate the irreversible without a human**: rebooting domain
controllers on a schedule, applying updates to the machine your automation
runs from, or anything where "it went wrong at 3am and nobody knew" is
unacceptable.

**And note the specific trap in this module.** Lesson 13.7 taught an ordering
that exists to protect you: check FSMO roles, move them off the machine going
down, patch one DC, verify it came back, verify replication, only then patch
the second. **Automation that ignores that ordering does not save you time,
it removes the safeguard.** The playbook below is built around it rather than
in spite of it, which is the point of the lesson.

## The easy half: Linux

Create `~/ansible/patch-linux.yml`:

```yaml
- name: Patch Linux hosts and report what changed
  hosts: linux
  become: true

  tasks:
    - name: Refresh the package lists
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600

    - name: Which packages would be upgraded
      ansible.builtin.command: apt list --upgradable
      register: upgradable
      # This only reads state, so it must never report "changed".
      # Lesson 10.4's idempotence rule applied by hand.
      changed_when: false

    - name: Show them before doing anything
      ansible.builtin.debug:
        var: upgradable.stdout_lines

    - name: Apply security updates
      ansible.builtin.apt:
        upgrade: dist
      register: upgrade_result

    - name: Does this host need a reboot
      ansible.builtin.stat:
        path: /var/run/reboot-required
      register: reboot_required

    - name: Say so, rather than rebooting without being asked
      ansible.builtin.debug:
        msg: "{{ inventory_hostname }} needs a reboot"
      when: reboot_required.stat.exists
```

**Note the last two tasks.** The playbook detects that a reboot is needed and
**tells you** rather than doing it. That is a deliberate choice: lesson 13.7
pointed out that a patched-but-unrebooted kernel produces a false clean scan,
so the information matters, and the decision to take a machine down stays
with a person.

**Check it before you run it**, the habit from lesson 10.5:

```bash
cd ~/ansible

# Does it parse? This catches YAML errors without touching anything.
ansible-playbook --syntax-check patch-linux.yml

# What would it do? --check makes no changes, --diff shows them.
ansible-playbook --check --diff patch-linux.yml
```

**How you know it worked:**

```text
playbook: patch-linux.yml
```

for the syntax check, with no error, and a task-by-task report from the check
run. Then run it for real without the flags.

## The careful half: domain controllers

This is the one that has to respect lesson 13.7's ordering. Create
`~/ansible/patch-dcs.yml`:

```yaml
- name: Patch domain controllers, one at a time
  hosts: domain_controllers
  # serial: 1 is the whole safety property of this playbook. It
  # means "finish this host completely before starting the next",
  # rather than the default of doing all hosts in parallel.
  serial: 1
  gather_facts: true

  tasks:
    - name: Confirm replication is healthy BEFORE touching this one
      ansible.windows.win_command: repadmin /replsummary
      register: replsummary
      changed_when: false

    - name: Stop if replication is already broken
      ansible.builtin.assert:
        that:
          - "'error' not in replsummary.stdout | lower"
        fail_msg: >-
          Replication problems already exist. Fix those before patching.
        success_msg: "Replication healthy, safe to proceed."

    - name: Where are the FSMO roles
      ansible.windows.win_shell: |
        (Get-ADDomain).PDCEmulator
      register: pdc_holder
      changed_when: false

    - name: Warn if this host holds the PDC Emulator
      ansible.builtin.debug:
        msg: >-
          {{ inventory_hostname }} holds the PDC Emulator. Transfer the
          roles before continuing, per lesson 13.7.
      when: inventory_hostname in pdc_holder.stdout

    - name: Install updates, but do not reboot yet
      ansible.windows.win_updates:
        category_names:
          - SecurityUpdates
          - CriticalUpdates
        reboot: false
      register: update_result

    - name: Reboot only this one, and wait for it to come back
      ansible.windows.win_reboot:
        post_reboot_delay: 60
      when: update_result.reboot_required

    - name: Confirm the directory services are actually running
      ansible.windows.win_service_info:
        name: "{{ item }}"
      loop: [adws, kdc, netlogon, ntds]
      register: dc_services

    - name: Fail loudly if any directory service is not running
      ansible.builtin.assert:
        that:
          - item.services[0].state == "running"
        fail_msg: "{{ item.item }} is not running. Stop. Do not patch the next DC."
      loop: "{{ dc_services.results }}"
      loop_control:
        label: "{{ item.item }}"
```

**Read what this playbook is really doing**, because the structure is the
lesson and the modules are incidental.

- **`serial: 1`** enforces one at a time. Without it, Ansible's default
  behaviour is to work on all hosts in parallel, which would reboot both
  domain controllers simultaneously. **That single line is the difference
  between this automation and an outage**, and it is exactly the mistake
  lesson 13.7 warned about.
- **The assert before any change** refuses to start if replication is already
  unhealthy. Automation that plows ahead regardless is worse than no
  automation.
- **The assert at the end fails the play** if the directory did not come
  back, which stops `serial: 1` from moving on to the second controller.
  "The machine pings" is not "the directory is answering", which is 13.7's
  point encoded as a check.
- **The PDC warning is a warning, not an action.** Moving FSMO roles
  automatically is a judgement call I am deliberately not making for you.

You need the group in your inventory. Add it to `~/ansible/inventory.ini`:

```ini
[domain_controllers]
dc01
dc02
```

**How you know it worked:**

```bash
# The group exists and contains both machines.
ansible-inventory --graph

# And the playbook parses.
ansible-playbook --syntax-check patch-dcs.yml
```

Expect `@domain_controllers:` in the graph with both hosts under it.

:::warning[Verified as syntax, not as behaviour]
Both playbooks above have been syntax-checked, and the Linux one uses modules
you already ran in Module 10.

The Windows tasks use `ansible.windows` collection modules against WinRM and
Kerberos, which lesson 10.7 set up. **I have not executed these against a
live domain controller**, so treat the first run as a test: run it with
`--check` first, run it against DC02 alone before both, and have the
snapshots from lesson 14.1 in place.

That is the honest status, and it is also just good practice for any
automation that reboots a domain controller.
:::

## Close the loop: rescan

**This is the part lesson 13.7 specifically asked for**, and the part people
leave out. Patching without rescanning means you believe you fixed something.

The rescan is the same image scan from lesson 13.2, plus the KEV join from
13.3. Create `~/ansible/rescan.yml`:

```yaml
- name: Rescan container images and report anything in KEV
  hosts: linux
  become: true

  tasks:
    - name: Pull the current vulnerability data and scan the image
      ansible.builtin.shell: |
        docker run --rm \
          -v /var/run/docker.sock:/var/run/docker.sock \
          -v trivycache:/root/.cache \
          aquasec/trivy:latest image --scanners vuln -f json {{ scan_image }} \
          > /tmp/rescan.json
      args:
        creates: /tmp/rescan.json

    - name: Refresh the CISA catalogue
      ansible.builtin.get_url:
        url: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
        dest: /tmp/kev.json
        mode: "0644"

    - name: How many findings are in the KEV catalogue
      ansible.builtin.shell: |
        set -o pipefail
        comm -12 \
          <(jq -r '.Results[].Vulnerabilities[].VulnerabilityID' /tmp/rescan.json | sort -u) \
          <(jq -r '.vulnerabilities[].cveID' /tmp/kev.json | sort -u) \
        | wc -l
      args:
        executable: /bin/bash
      register: kev_count
      changed_when: false

    - name: Report it
      ansible.builtin.debug:
        msg: "{{ scan_image }}: {{ kev_count.stdout }} findings in the KEV catalogue"
```

Run it with the image you care about:

```bash
ansible-playbook rescan.yml -e scan_image=nginx:latest
```

**How you know it worked:** a message naming the image and a number. **Zero
is the result you want**, and it is what lesson 13.3 measured for
`nginx:latest`.

`comm -12` prints only the lines present in both sorted lists, which is the
command-line version of the SQL join from 13.3. Same question, different
tool, and worth seeing both ways.

## Schedule it, carefully

```bash
# Edit root's crontab, since these need privilege.
sudo crontab -e
```

```cron
# 04:00 Sunday: patch Linux hosts. Absolute paths, because cron
# has almost no PATH, which is lesson 10.9's warning.
0 4 * * 0 /home/sam/ansible/.venv/bin/ansible-playbook -i /home/sam/ansible/inventory.ini /home/sam/ansible/patch-linux.yml >> /var/log/patch-linux.log 2>&1

# 05:00 Sunday: rescan and record the result.
0 5 * * 0 /home/sam/ansible/.venv/bin/ansible-playbook -i /home/sam/ansible/inventory.ini /home/sam/ansible/rescan.yml -e scan_image=nginx:latest >> /var/log/rescan.log 2>&1
```

**Substitute your own username and check the venv path.** Lesson 10.9
established that the venv's `ansible-playbook` works from cron with no PATH
at all, because the shebang points at the venv's Python. That is why the
absolute path is sufficient and no activation is needed.

**Notice what is not in that crontab: the domain controllers.** Rebooting
those stays a thing you start deliberately, having read the output. You can
schedule the *report* and keep the *action* manual, which is usually the
right split for anything irreversible.

**How you know it worked**, after the first Sunday:

```bash
# The log exists and ends with a play recap rather than a traceback.
sudo tail -20 /var/log/patch-linux.log
```

Expect Ansible's `PLAY RECAP` with `failed=0`. **An empty or missing log
means cron did not run it at all**, which is usually a path problem, and
`grep CRON /var/log/syslog` will show whether it tried.

## The bit that makes it management

**A scheduled job nobody reads is not a control.** If nothing ever looks at
`/var/log/rescan.log`, you have automated the work and removed the attention,
which is a net loss.

Two honest options, and pick one:

- **Have it tell you.** Send the result somewhere you actually look. Your
  Wazuh stack from Module 12 already reads log files; pointing an agent at
  `/var/log/rescan.log` and alerting when the KEV count is not zero is a
  genuinely good use of what you built.
- **Put reading it in a runbook** with a date, which is lesson 15.7.

The failure to avoid is the third option, which is what most people
accidentally choose: schedule it, feel organised, and never look again.

## What you take from this

The loop from lesson 13.7 running on a schedule, with the domain controller
ordering encoded as `serial: 1` and two asserts rather than left to memory,
and the rescan step included so the loop actually closes.

You also have a clear line between what you automated and what you
deliberately did not.

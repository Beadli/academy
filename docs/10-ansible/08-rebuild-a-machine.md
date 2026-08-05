---
title: "10.8 Rebuild a machine on purpose"
sidebar_position: 8
---

# 10.8 Rebuild a machine on purpose

:::note[Activate first]
Commands run on **UBNT01**, inside the virtual environment from lesson 10.2.

```bash
cd ~/ansible
source .venv/bin/activate
```
:::

Lesson 3.5 told you servers are cattle, not pets, and that every permanent
machine in your lab would eventually die and be rebuilt, some of them on
purpose in this module.

This is that lesson. You are going to destroy a working machine and rebuild it
from files, and the point is not the rebuilding. It is finding out what you had
forgotten to write down.

## Pick your victim

**Do not use UBNT01.** It is your control node, it holds your playbooks, and
destroying it means destroying the thing doing the rebuilding.

Use a machine you can lose. If you have a spare Linux VM, use that. If not,
build one now. It does not need to match UBNT01; it needs to exist, be
reachable, and be worth rebuilding:

- **New VM**, Ubuntu Server, minimal install. 2 GB of memory and 20 GB of disk
  is plenty.
- **Same LAN segment** as the rest of the lab, so Ansible can reach it. Give it
  a free address from your lesson 4.3 plan, or let it take one from DHCP and
  note what it got.
- **Install OpenSSH** when the installer offers it. Without this, Ansible has
  no way in.
- **Same username** you use elsewhere, so your inventory's `ansible_user`
  works unchanged.

Then add it to `~/ansible/inventory.ini` under `[linux]`:

```ini
rebuild01 ansible_host=10.10.10.21
```

```bash
# Reachable before you go further.
ansible rebuild01 -m ansible.builtin.ping
```

Now make it a real machine rather than an empty one, so the rebuild has
something to reproduce:

```bash
ansible-playbook harden.yml --limit rebuild01
ansible-playbook webserver.yml --limit rebuild01
```

Take a snapshot first, so this is an experiment rather than a commitment.

## Write down what it should be

Before destroying anything, answer this honestly: **if this machine vanished
now, what would you have to remember?**

Write the answer in your journal. Not the playbook, the list. Packages,
configuration, users, firewall rules, anything on disk that matters, anything
another machine expects it to provide.

Then compare that list to what your playbooks actually cover. The gap between
them is the real output of this lesson, and it is usually larger than people
expect.

## Destroy it

```bash
# From your own machine, not from UBNT01.
# In the hypervisor: power off the VM, delete it, confirm.
```

Delete it properly. Not "revert to snapshot", not "shut down". Gone.

That will feel wrong, which is precisely the instinct lesson 3.5 said this
would remove. The machine was never the valuable thing.

## Rebuild it

Create the VM again, minimal install, same name and address, SSH reachable.
That part is still manual, and lesson 10.9 has something to say about why.

Then:

```bash
# Confirm Ansible can reach the new machine. Its host key changed, so
# SSH will ask; that is the mechanism from 10.2 working correctly.
ansible rebuild01 -m ansible.builtin.ping

ansible-playbook harden.yml --limit rebuild01 --check --diff
ansible-playbook harden.yml --limit rebuild01

ansible-playbook webserver.yml --limit rebuild01
```

`--limit` restricts a play to a subset of its hosts. Get comfortable with it:
it is how you test a change on one machine before letting it near thirty, and
it is the practical form of "run it against one machine first" from 10.1.

## Now the actual lesson

The machine is back. Compare it to the list you wrote.

**What did the playbooks miss?**

Almost certainly something. The things people forget are consistent:

**Data.** Playbooks describe configuration, not content. Anything the machine
*held* is gone unless it was backed up. If that catches you here, it would have
caught you in an outage, and the lab is a better place to find out.

**Things installed by hand months ago.** A package you added while debugging.
A cron job. A file dropped in `/usr/local/bin`. These are invisible until the
rebuild does not reproduce them.

**Things that were never on this machine.** The DNS record pointing at it. The
firewall rule permitting it. Configuration on *other* machines that names this
one. A rebuild reveals how much of a server's identity lives elsewhere.

Write the gaps into your playbooks now, while you can see them. Then rebuild
once more and check that pass two is cleaner than pass one.

:::tip[This is a disaster recovery test, and that is the vocabulary to use]
You have just done in a lab what organisations pay consultants to run: destroy
a system and attempt recovery from documented process, then measure the gap.

Two numbers come out of a real one. **Recovery Time Objective (RTO)** is how
long you are prepared to be down. **Recovery Point Objective (RPO)** is how
much data you are prepared to lose. Your rebuild has a real RTO you could
measure with a stopwatch, and its RPO is "everything since the last backup",
which for this machine may be "everything".

Being able to say you have tested a rebuild rather than assumed one is
unusual. Most organisations discover their gaps during the outage.
:::

## What about the Windows server?

Lesson 5.3 raised this, when it pointed out that your evaluation copy of
Windows Server has an expiry date, and said this module would rebuild it for
you.

Here is the honest position, which is more useful than the promise.

**The configuration half transfers directly.** Everything you did in 10.7 is
the same work: a rebuilt Windows machine can be brought to a described state
by playbooks, using the same modules, from the same control node.

**The build half does not.** Installing Windows, promoting a domain
controller, and restoring Active Directory are not configuration management
problems. Promotion is a one-time operation that changes what the machine *is*,
and a domain controller carries a database whose contents are the valuable
part. Rebuilding one properly is a restore, not a redeploy, and it belongs to
backup and recovery rather than to Ansible.

So: if your evaluation licence expires, expect to install Windows again by
hand, and expect your playbooks to do the configuration afterwards. That is a
genuinely shorter evening than the first time, which is what 5.3 was really
promising.

**The distinction is worth carrying**, because it applies to every stateful
system you will meet. A web server is cattle. A domain controller, a database,
and a certificate authority hold state, and state is restored rather than
rebuilt. Knowing which of your machines is which is most of a disaster recovery
plan.

## What is still manual, and why that is the next thing

You created the VM by hand. That is the remaining gap, and it has a name.

**Configuration management**, which is what you have been doing, assumes a
machine exists and makes it correct. **Provisioning** creates the machine in
the first place. Tools like Terraform and OpenTofu do that half, and in a cloud
they do it completely: the VM, its disk, its network, its firewall rules, all
from a file.

In a hypervisor lab it is fiddlier and worth less, which is why this course
stops here. But you can now say precisely where the boundary is, and that is
the useful thing.

The two halves together are what people mean by **infrastructure as code**: the
existence of the machine and the state of the machine, both described in files,
both in version control. You have the second half working, and lesson 10.9 puts
it where it belongs.

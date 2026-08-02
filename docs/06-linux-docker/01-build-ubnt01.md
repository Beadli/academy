---
title: "6.1 Build UBNT01 and put it on the network"
sidebar_position: 1
---

# 6.1 Build UBNT01 and put it on the network

You installed Ubuntu Server once already, on `practice01` in Module 3,
and then deliberately destroyed it. This time it stays.

## Create the VM

Same wizard, same Ubuntu Server ISO from lesson 3.3:

- **Name and location:** `UBNT01`, in `C:\VMs\UBNT01`
- **RAM:** 6 GB. It looks generous for a machine with no desktop, and
  it isn't: Module 12 puts a SIEM on here, and those are hungry.
- **CPU:** 2 cores. **Disk:** 60 GB, grow-as-used.
- **Network:** the lab LAN, same as DC01.
- Decline any offer to install automatically.

Walk the installer exactly as in lesson 3.4, with two differences that
matter:

- **Hostname:** `ubnt01`, not `practice01`.
- **Tick "Install OpenSSH server"** when it offers. Lesson 3.4 told you
  to do this out of habit; today you'll actually use it, in 6.2.

Let it install and reboot, then log in at the console.

## Give it a fixed address

Servers get static addresses, for the reasons lesson 4.1 gave. On Ubuntu
that's configured by **netplan**, in a YAML file, which is a pleasant
change from the days of editing three different files.

First, find out what your network interface is called, because it varies
by hypervisor and version and guessing wastes an evening:

```bash
# The -brief flag gives one line per interface. You want the one
# that isn't "lo" and currently has an address from DHCP.
ip -brief addr
```

Note the name (`ens33`, `ens160`, `enp0s3`, something like that). Now
find the file netplan already wrote for you:

```bash
# The installer leaves one file here. Names vary between releases,
# so list the directory rather than assuming.
ls /etc/netplan/
```

Edit it, substituting your interface name. `nano` is the editor that
comes with everything and asks the least of you; Ctrl+O saves, Ctrl+X
exits:

```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

Replace its contents with this, keeping the indentation exactly (YAML
cares, and two spaces per level is the convention):

```yaml
network:
  version: 2
  ethernets:
    ens33:
      dhcp4: false
      addresses:
        - 10.10.10.20/24
      routes:
        - to: default
          via: 10.10.10.254
      nameservers:
        addresses:
          - 10.10.10.10
        search:
          - lab.cyber.internal
```

Read what you just wrote, because it's the four questions from lesson
4.1 in file form: the address, the `/24` mask, the gateway on the
`routes` line, and DNS pointing at **DC01**, not at your firewall and
not at a public resolver. That last one is lesson 5.1's rule made
concrete: this machine has to ask the domain controller, or it will
never find the domain.

:::note[Substitute your own gateway]
`10.10.10.254` is FW01, the Tier 2 firewall. On Tier 1 your gateway is
the hypervisor's NAT device, which lesson 4.3 said is usually
`10.10.10.2`. Use whatever `ip route` showed you before you changed
anything.
:::

## Apply it without locking yourself out

Netplan has a command specifically for the mistake you're about to
nearly make:

```bash
# Applies the config, then asks you to confirm. If you don't answer
# within 120 seconds it puts everything back. If you have just cut
# your own connection, doing nothing is the fix.
sudo netplan try
```

Press Enter to accept when it asks. Then verify:

```bash
ip -brief addr           # expect 10.10.10.20/24
ip route                 # expect your gateway on the default line
resolvectl status | head -20   # expect DNS server 10.10.10.10

# If resolvectl prints nothing, this machine isn't using
# systemd-resolved. Check the old-fashioned way instead:
cat /etc/resolv.conf
```

If something is wrong, edit and `sudo netplan try` again. Once you're
happy, `sudo netplan apply` makes it permanent without the countdown.

## Prove it can find the domain

This is the test that matters, and it's why Module 5 had you point the
firewall's DHCP at the domain controller.

```bash
# Can this machine resolve the domain, and reach the DC?
ping -c 3 10.10.10.10
dig +short lab.cyber.internal

# The service record from lesson 5.8. A machine that can answer this
# question is a machine that could join the domain.
dig -t SRV _ldap._tcp.lab.cyber.internal +short

# And the internet still works, through the same path.
ping -c 3 1.1.1.1
dig +short ubuntu.com
```

All five working means your Linux server sits inside your domain's
world: it uses the domain's DNS, it can find the domain's services, and
it can still reach the outside. If the SRV lookup fails but the ping
works, your DNS setting didn't take, which is the single most likely
fault here.

Finally, bring it up to date and take a snapshot called `base-install`:

```bash
sudo apt update && sudo apt upgrade -y
```

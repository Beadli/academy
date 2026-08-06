---
title: "EXT-07 Add a Windows workstation to the domain"
sidebar_position: 7
---

# EXT-07: Add a Windows workstation to the domain

|  |  |
|---|---|
| **What it is** | A build, not a drill. An ordinary Windows client machine, domain-joined |
| **Unlocks** | DEF-11, DEF-02, DEF-03, DEF-04, DEF-06, DET-05, OFF-05, OFF-10, IR-02 |
| **Needs** | Module 5 complete, so the domain exists and DC01 is running |
| **Costs you** | 4 GB of RAM while it runs, around 30 GB of disk, and a 90-day clock |
| **Effort** | An evening, most of which is the installer running |

## Why this machine exists

Your lab has domain controllers, a Linux host, some servers, and an attacker
box. What it does not have is the machine type that most of an organization
actually sits at, and that most attacks actually land on: **an ordinary
workstation.**

That gap is not an accident, it is a memory budget. The course never builds
one because a Windows client costs 4 GB, and forcing that on every student to
support drills some of them will never run would be a bad trade. So it lives
here instead, and you build it the day a drill needs it.

Nine drills need it. The one that probably sent you here is **DEF-11**, which
asks you to prove a group policy applied to a machine that is not a domain
controller, because a domain controller is the least representative machine in
the estate to test against.

**This is the extension to build first** if you are going to build any. More
drills point at it than at anything else in that list.

## What you are building

A single virtual machine:

| | |
|---|---|
| **Name** | WKS01 |
| **What it runs** | Windows 11 Enterprise, evaluation edition |
| **Memory** | 4 GB |
| **Disk** | 64 GB, growing as needed |
| **Address** | DHCP, from the `.100` to `.199` pool in your lesson 4.3 plan |
| **Where it sits** | The lab LAN, the same segment as DC01 |

**The name follows the convention you have been using.** DC01 is a domain
controller, SUBCA01 is an issuing CA, and WKS01 is a workstation. The pattern
is role then number, and the number exists so that WKS02 has somewhere
obvious to go.

**Why DHCP, when every server you have built took a static address.** Lesson
4.1 gave you the rule: infrastructure that other machines need to find gets a
fixed address, and everything else asks. A workstation is the "everything
else". Nothing looks WKS01 up by address, and a real estate has hundreds of
them, which is why nobody hand-assigns workstation addresses. Following the
convention here is the point rather than a detail: you are building the
machine type the convention was written for.

## Before you start

Four things, and the third is the one that ruins evenings.

1. **DC01 is running**, because you cannot join a domain that is not
   answering. Power it on now and leave it on for the whole build.
2. **You know your domain administrator password.** It is the Administrator
   password you set while installing DC01 in lesson 5.2, which became the
   *domain* administrator when you promoted the machine in 5.4. Not the DSRM
   password, which is a separate one for repair mode and is no use here.
3. **You have the memory free.** Tier 1, this is the tight one. Your normal
   day is DC01 and UBNT01 at 9 GB, and adding 4 GB puts you at 13 GB of your
   16. That works, but shut down KALI01 and DC02 first, and expect the host
   to feel it. If it hurts, run WKS01 only for the drill that needs it and
   power it off after.
4. **You have around 30 GB of free disk.** The virtual disk is defined as 64
   GB but only grows into what Windows actually uses.

## The 90-day clock, and how it differs from Module 5

Lesson 3.3 walked you through the Windows Server evaluation clock and talked
you down off it: 180 days, extendable in place, and by the time it matters
rebuilding is cheap. **Two of those three things are different here, so do not
carry the Module 5 reassurance across unexamined.**

**It is 90 days, not 180.** The client evaluation runs half as long.

**Do not count on extending it.** Microsoft's evaluation page for the client
does not document any way to reset the clock, and the `slmgr /rearm` behaviour
you met in Module 5 was for Windows Server. It may work here, it may work
fewer times, and building a lab plan around an undocumented behaviour is how
you get surprised. Assume 90 days and be pleased if you get more.

**What expiry looks like**, in Microsoft's own words, so it does not read as a
mystery fault when it happens: the desktop background turns black, a
persistent notice appears saying the system is not genuine, and **the machine
shuts down every hour.** It does not delete anything or lock you out. It
becomes annoying on purpose.

The third thing from lesson 3.3 still holds, and it is the one that matters.
This machine is not an heirloom. It is a workstation you can rebuild in an
evening, and by day 90 you will be able to do it faster than the first time.
If a drill matters more than the clock, rebuild and carry on.

## Step 1: Get the installer

Go to the [Microsoft Evaluation
Center](https://www.microsoft.com/evalcenter/) and find **Windows 11
Enterprise**. As in lesson 3.3, Microsoft asks for a name, email and company
before it releases the download. Give it something real enough to pass
validation.

**Four ways to take the wrong file, and they all sit on the same page.**

- **Enterprise, not Pro or Home.** Only the Enterprise edition is offered as
  a free evaluation, and it is also the edition with the management features
  the defensive drills use. If you find yourself on a page asking for a
  product key or a payment, you have wandered onto the retail side.
- **The dated release, not LTSC.** The page offers a normal versioned release
  and a **Long-Term Servicing Channel** build alongside it. LTSC is a
  stripped, slow-moving edition for machines like cash registers and medical
  equipment. It is a legitimate product and it is not what a workstation runs.
  Take the ordinary release the page leads with.
- **x64, not Arm64.** Both are offered. Arm64 is for Apple Silicon and Windows
  on ARM devices, neither of which can take this course (lesson 0.3 ruled
  Apple Silicon out honestly at the start). If your machine got you through
  Module 3, you want x64.
- **The newest build listed, whatever it is called this month.** Do not copy a
  version number from this page or any other. Take the top of the list on the
  day you download.

You will get an ISO of roughly 5 to 7 GB. Move it into the `ISOs` folder you
made in lesson 3.3, next to the Windows Server image, and give it a name you
will recognise in six months.

**There is no checksum to compare**, exactly as in lesson 3.3. Your assurance
is that the file came over HTTPS from microsoft.com and nowhere else. That is
a weaker guarantee than Ubuntu's published SHA256, and knowing which one you
have is the actual skill.

## Step 2: Create the virtual machine

This is lesson 3.4 again with different numbers, so it should feel familiar.
In VMware Workstation, **File > New Virtual Machine**, and take the typical
path.

- **Installer disc image:** the ISO you just downloaded.
- **Location:** `C:\VMs\WKS01` on Windows, or `~/VMs/WKS01` on Linux. One
  folder per machine, named after the machine, as lesson 3.3 established.
  Never inside OneDrive or any synced folder.
- **Disk size:** 64 GB, stored as a single file.
- **Memory:** 4096 MB.
- **Processors:** 2 cores if you can spare them, 1 if you cannot.
- **Network adapter:** the **lab LAN segment**, the same one DC01 is on. Tier
  1, that is your NAT network. Tier 2, that is the inner host-only segment
  behind FW01, not the outer one.

**Getting the network adapter wrong is the single most common way this build
fails**, and it fails confusingly: the machine installs perfectly, browses the
internet happily, and then cannot find the domain at all. If you are unsure
which segment is which, your journal from lesson 4.3 has the answer, because
that lesson told you to write it down for exactly this moment.

:::info[VirtualBox difference]
Create the VM with type **Microsoft Windows** and version **Windows 11
(64-bit)**. VirtualBox will also want **EFI enabled** and a **TPM** present,
both of which its Windows 11 profile normally sets for you. Attach the
network adapter to the same host-only or NAT network your other lab machines
use, and give it 4096 MB and 64 GB as above.
:::

**Windows 11 checks for a TPM and Secure Boot before it will install**, which
is a real wall people hit here and not a fault in your setup. A TPM is a small
security chip that Windows 11 requires; your hypervisor can pretend to have
one. In VMware Workstation the VM settings have an **Encrypt** step, because
Workstation requires the virtual disk be encrypted before it will add a
virtual TPM. Encrypt the VM, then add **Trusted Platform Module** under
Options. If the installer stops with "This PC can't run Windows 11", this is
almost always why.

## Step 3: Install Windows

Boot the machine and work through the installer. It is long and mostly
unattended, so start it and go and do something else.

Two decisions in the setup wizard matter, and everything else can take its
default.

**When it asks how you want to set the machine up, do not sign in with a
personal Microsoft account.** Windows 11 pushes hard toward one, and a
workstation joined to a personal account is not the machine you are trying to
build. On the Enterprise edition the path you want is the work or school
option, and then the domain-join choice underneath it. **The exact wording of
that screen moves between builds**, so rather than quoting a label that will
be wrong by next year: you are looking for the option that is not a personal
account, and then for the one that mentions a domain rather than a company
sign-in.

**Give the machine the name WKS01** when it asks, or rename it afterwards if
the installer never offers. You can check and fix the name later:

```powershell
# Run this in PowerShell on WKS01, as an administrator.
# It prints the machine's current name.
hostname
```

```powershell
# Only if the name is wrong. This reboots the machine.
Rename-Computer -NewName WKS01 -Restart
```

**How you know this step worked:** you reach a Windows desktop, and `hostname`
prints `WKS01`.

## Step 4: Point it at the domain's DNS

This is the step that decides whether the rest of the evening works, and it is
worth understanding rather than pasting.

Your machine has an address from DHCP by now. It also has a DNS server from
DHCP, and **whether that DNS server has ever heard of your domain depends on
your tier.** Check first rather than assuming:

```powershell
# On WKS01. Look at the DNS Servers line for your adapter.
ipconfig /all
```

**If it already says `10.10.10.10`, you are done with this step.** That is
the Tier 2 answer: in lesson 5.5 you told FW01 to hand out DC01 as the DNS
server, so every machine it addresses inherits the domain automatically. Skip
to step 5.

**If it says anything else, you are on Tier 1** and your DHCP server is the
hypervisor, which knows nothing about `lab.internal` and cannot be told about
it without editing hypervisor configuration files that differ by product and
version. Set the DNS server on this machine directly instead:

```powershell
# On WKS01, as administrator. Find the adapter name first rather than
# guessing it: it is "Ethernet" on some machines and "Ethernet0" on
# others, and hardcoding the wrong one is a lesson this course has
# already learned the hard way.
Get-NetAdapter | Where-Object Status -eq "Up"
```

```powershell
# Substitute the InterfaceAlias the previous command printed.
Set-DnsClientServerAddress -InterfaceAlias "Ethernet0" `
                           -ServerAddresses 10.10.10.10
```

```powershell
# Read it back, because a command that printed nothing has not told
# you it worked. Expect 10.10.10.10.
Get-DnsClientServerAddress -InterfaceAlias "Ethernet0"
```

**Be honest with yourself about what you just did.** In a real network the
DHCP server hands out the domain's DNS, and nobody touches a workstation to
configure it. You have set it by hand on one machine because your Tier 1 DHCP
server is a hypervisor. That works, and it does not scale, and noticing why it
does not scale is worth more than the command was.

**How you know it worked**, and this is the real test rather than reading
settings back:

```powershell
# Ask for the domain controller's service record. This is the lookup
# a machine performs to find a domain, so if it answers, joining will
# work. Expect a record naming DC01.
Resolve-DnsName -Name _ldap._tcp.lab.internal -Type SRV
```

**If that fails, stop here.** Do not attempt the join. Every domain-join error
message you are about to get is a DNS problem wearing a costume, and they are
far harder to read than the failure you are looking at right now. Check the
network adapter is on the right segment, that DC01 is powered on, and that
you can `ping 10.10.10.10`.

## Step 5: Join the domain

```powershell
# On WKS01, as administrator. This prompts for credentials: give it
# LAB\Administrator and the password from lesson 5.2. The machine
# reboots when it finishes.
Add-Computer -DomainName lab.internal -Restart
```

After the reboot, log in with a **domain** account rather than the local one
you created during setup. At the sign-in screen that usually means choosing
"Other user" and entering `LAB\yourusername`.

**How you know it worked:**

```powershell
# Three proofs, and each one answers a different question.

# 1. Does this machine believe it is in the domain?
(Get-CimInstance Win32_ComputerSystem).Domain

# 2. Does the domain agree, and is the secure channel healthy?
#    This is the one that catches a join that half-happened.
Test-ComputerSecureChannel

# 3. Are you holding a Kerberos ticket, as in lesson 5.5?
klist
```

Expect `lab.internal`, then `True`, then a ticket list containing
`krbtgt/LAB.INTERNAL`. **The second command is the one that matters.** A
machine can show the right domain name and still have a broken relationship
with it, and `Test-ComputerSecureChannel` returning `False` is what that looks
like before it turns into a login failure weeks later.

You can also confirm from the other side. On DC01:

```powershell
# On DC01. The computer account should now exist in the directory.
Get-ADComputer WKS01
```

## Step 6: Snapshot it, then write it down

Take a snapshot now, while the machine is clean and joined and nothing has
been broken by a drill yet. Lesson 3.5 made the case; this is the machine that
proves it, because several of the drills this unlocks are explicitly
destructive and you will want the way back.

Name the snapshot something a stranger could read, like `clean domain-joined
build`, rather than `snap1`.

Then add two lines to your journal:

- **WKS01 in your addressing plan**, with whichever address DHCP gave it and a
  note that it is a DHCP client rather than a reservation.
- **The date you installed it**, because that is day zero of the 90 and you
  will not remember it in month two.

## What this unlocks

Nine drills become possible. Three of them are worth naming, because they are
the reason the workstation matters rather than merely being another machine:

- **DEF-11** proves a group policy applied to a machine that represents the
  estate, and that a policy you scoped out stayed out. Lesson 5.7 could only
  ever check a domain controller against itself.
- **DET-05** puts file integrity monitoring somewhere files actually change in
  the ways attackers change them.
- **OFF-05** gives your attacker box an endpoint to attack that is not a
  domain controller, which is what real intrusions start with.

The rest are listed at the top of this page.

**Worth noticing before you move on.** Every drill this machine unlocks is a
defensive or detection exercise, and that is not a coincidence. You have added
the machine type an estate has hundreds of and an attacker usually reaches
first. The servers you spent five modules building are what they are trying to
get to.

---
title: "2.1 PowerShell: measure your machine"
sidebar_position: 1
---

# 2.1 PowerShell: measure your machine

In checkpoint 0.6 you ran three commands by hand and copied numbers into
a note. That worked once. In a real environment you'd do it for fifty
servers, and nobody types fifty times. Today you turn those commands into
a script that measures the machine and writes the report straight into
your vault, formatted and dated. Snapshotting a host before you change it
is a habit that has saved me real pain, and this script is the starter
version of it.

PowerShell is Microsoft's automation language, and from Module 5 onward
it's how you'll manage Active Directory, certificates, and everything
else on the Windows side. One design idea explains most of it: PowerShell
commands pass around *objects* with named properties, not text. When you
see `$disk.Free` below, that's asking the disk object for its `Free`
property. No text-chopping required.

**Linux and macOS readers:** this is your mirror of the tmux lesson.
PowerShell is Windows-first, and the hardware queries in this script only
exist on Windows, so read along, understand the script, and you'll run
PowerShell for real against Windows Server in Module 5. (PowerShell does
install on Linux and macOS, but a script that can't query your hardware
teaches you nothing today.)

## Running PowerShell, before you write any

You'll type PowerShell commands in this course far more often than
you'll write PowerShell files, so learn the console first.

**Open it as Administrator.** Right-click the Start button and choose
the **Windows PowerShell (Admin)** or **Terminal (Admin)** entry. Most
of what you'll do to a server needs administrator rights, and the
failure when you don't have them is a confusing "access denied" rather
than a helpful "run me as admin". You'll know it worked because the
window title says Administrator.

You get a prompt that looks like `PS C:\Users\you>`. Type a command,
press Enter, read what comes back. That's the whole interaction:

```powershell
# Try these one at a time. Type, Enter, read.
Get-Date
Get-Location
Get-ChildItem
```

**Code blocks in this course usually hold several separate commands.**
Run them one line at a time unless the lesson says otherwise. Pasting a
whole block works too and PowerShell will run each line in order, but
going one at a time means you see which command produced which output,
and when something fails you know exactly what failed.

### The backtick, and the trap that comes with it

Some commands are too long for one line, so you'll see them broken up
with a backtick at the end of each line:

```powershell
New-Item -ItemType Directory `
         -Path C:\Temp\example
```

That trailing `` ` `` means "this command continues on the next line."
When you meet one, **paste or type the whole thing including every
continued line**, then press Enter once at the end. It's one command
wearing several lines.

Here's the trap, and it catches everyone once: **nothing may follow the
backtick, not even a space.** One invisible space after it and
PowerShell treats the line as finished, then chokes on the next line as
if it were a new command. If you type these by hand rather than copying,
this is the single most likely thing to go wrong.

### When the prompt turns into `>>`

Sooner or later you'll press Enter and get this instead of your normal
prompt:

```text
>>
```

That's PowerShell saying "your command isn't finished, keep going." It
means something was left open: a backtick at the end, an unclosed quote,
an unmatched brace. It looks like a hang, and it isn't.

To get out: press **Ctrl+C**. Your prompt comes back and nothing was
run. Then look at what you pasted for the unclosed thing.

### Four keys that make this bearable

- **Tab** completes what you're typing. Type `Get-Chi` and press Tab.
  It also completes parameter names after a `-`, which is faster and
  more accurate than remembering them.
- **Up arrow** brings back your previous commands. Most of what you type
  is a small edit of something you already typed.
- **Ctrl+C** stops a command that's running or a line you've made a mess
  of.
- **`Get-Help`** is the built-in manual, and `-Examples` is the part
  worth reading:

```powershell
# What does this command do, with realistic examples?
Get-Help Get-ChildItem -Examples

# What commands exist for a thing I only half remember?
Get-Command *service*
```

Those last two are the self-rescue kit. Between them and lesson 1.6's
rule about understanding a command before running it, you can work out
almost anything without leaving the shell.

## The script

Save this as `machine-report.ps1` in `Resources/scripts/` in your vault.
Read every comment; the comments are the lesson.

```powershell
# machine-report.ps1
# Measures this machine and writes a Markdown report into the vault.

# A variable in PowerShell starts with $. This one holds the path to
# your vault. CHANGE THIS if your vault lives somewhere else.
$vault = "$HOME\git\lab-journal"

# Get-CimInstance asks Windows for management objects. Think of these
# as the OS's own record cards for hardware and system state.
$system = Get-CimInstance Win32_ComputerSystem
$os     = Get-CimInstance Win32_OperatingSystem
$cpu    = Get-CimInstance Win32_Processor
$disk   = Get-PSDrive C

# Raw values come in bytes, which no human wants to read.
# [math]::Round(x, 1) rounds to one decimal; 1GB is PowerShell
# shorthand for the number of bytes in a gigabyte.
$ramGB  = [math]::Round($system.TotalPhysicalMemory / 1GB, 1)
$freeGB = [math]::Round($disk.Free / 1GB, 1)

# A "here-string" (@" ... "@) holds a block of text. Anything with a
# $ inside it gets replaced with the variable's value, and $( ) lets
# you run an expression mid-text.
$report = @"
# Machine report: $($system.Name)

Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm")

- OS: $($os.Caption)
- RAM: $ramGB GB
- CPU: $($cpu.Name)
- Cores: $($cpu.NumberOfCores) physical / $($cpu.NumberOfLogicalProcessors) logical
- Free disk (C:): $freeGB GB
"@

# Write the report into the vault. -Encoding utf8 keeps Obsidian happy.
$report | Out-File -FilePath "$vault\Resources\machine-report.md" -Encoding utf8

# And say so, because silent scripts get re-run "just in case."
Write-Host "Report written to $vault\Resources\machine-report.md"
```

## The wall you will hit first

Run it:

```powershell
cd ~\git\lab-journal\Resources\scripts
.\machine-report.ps1
```

Odds are good Windows refuses with "running scripts is disabled on this
system." That's the execution policy, a default that stops users from
double-clicking hostile scripts from the internet. It's a reasonable
default and everyone in this field has cursed at it at least once. Allow
locally created scripts for your user account:

```powershell
# RemoteSigned: scripts you wrote locally run; scripts downloaded
# from the internet need a signature. Scoped to your user only.
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Run the script again, then open `Resources/machine-report.md` in
Obsidian and admire a report you didn't type.

## Make it yours

Reading was half the lesson; changing it is the other half. Two edits,
in rising order of effort:

1. Add the OS version number to the report. The object already has it:
   `$os.Version`. One line.
2. Add a line reporting how much RAM is *free* right now. Poke around
   with `$os | Get-Member` to see every property the object offers
   (look at `FreePhysicalMemory`, and note its unit is KB, not bytes).

If a property name or a line refuses to make sense, this is exactly what
lesson 1.6 was for: paste the line into Claude, ask what it does, and
save the explanation to your journal.

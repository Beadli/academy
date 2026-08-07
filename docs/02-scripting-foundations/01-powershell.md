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

### There are three of these, and you will meet all three

This confuses people for years, so take two minutes on it now. "PowerShell"
names three different things you will run into.

**Windows PowerShell 5.1** is what you just opened. It ships with every
version of Windows and Windows Server, it is already on every machine you are
about to build, and it is what this course uses on servers. Microsoft is not
adding features to it. That is fine: everything the course does works here,
and needing no installation on a fresh server is worth more than new features.

**PowerShell 7** is the current one, sometimes called PowerShell Core. It is a
separate program that installs alongside 5.1 rather than replacing it, its
command is `pwsh` instead of `powershell`, and it runs on Linux and macOS too.
It is where new automation should be written, and it is worth installing on
your own machine. **It is not on Windows Server by default**, and a handful of
older Windows-management commands were dropped from it, so this course does
not assume it.

**The PowerShell ISE**, for Integrated Scripting Environment, is an editor
that shipped with Windows for years. It only runs Windows PowerShell 5.1, it
cannot run PowerShell 7 at all, and Microsoft has stopped developing it in
favour of the editor you'll install further down this page.

**Learn that the ISE exists anyway, because one day it may be all you get.**
Plenty of organisations hand administrators a locked-down management server
with no editor installed, no package manager, and no permission to add
either. The ISE sitting in the Start menu is then the entire toolkit.
Somebody who has only ever written PowerShell in a modern editor arrives on
that machine and cannot work. Open it once, notice it has a script pane on
top and a console underneath, and file it away.

**Which one am I in?** Ask, rather than guessing:

```powershell
# 5.1 prints a version starting with 5. PowerShell 7 prints 7.
$PSVersionTable.PSVersion
```

For the rest of this course, "PowerShell" means Windows PowerShell 5.1 unless
a lesson says otherwise.

## Your first commands

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

## Something to write the script in

Everything so far has been typed straight into a shell, which runs one
line and forgets it. A script is a *file*, so it needs somewhere to be
written and saved. The shell is not that place.

**Linux and macOS readers, this part is yours too.** You're skipping the
PowerShell script below, but you write a real bash script in the very
next lesson, and it's less annoying to set this up now.

What you need is a **plain-text editor**. Not a word processor: Word,
Pages, and Google Docs quietly replace your straight quotes with curly
ones and save in their own formats, and a shell cannot read any of it.
The quotes are the cruel part, because the file looks right on screen and
still fails.

I'm going to point you at **Visual Studio Code**, free, on all three
operating systems, and open all day on a large fraction of this
industry's machines. The reason I'm picking it for beginners rather than
Notepad is narrow and practical: it shows you the two properties of a
file that Notepad hides, and one of them causes a failure in the next
lesson that looks exactly like a broken script.

### Install it

**The wrong turn to avoid:** *Visual Studio Code* and *Visual Studio* are
two different products from the same company with almost the same name.
Visual Studio is a multi-gigabyte suite for building applications and you
don't want it today. If your download is measured in gigabytes, you
clicked the wrong one. Code is a few hundred megabytes.

```powershell
# Windows. -e means "exact id", so you get Microsoft's package and not
# something similarly named.
winget install --id Microsoft.VisualStudioCode -e
```

```bash
# Ubuntu and other snap-capable Linux. --classic is required; without
# it the install fails with a confusing confinement error.
sudo snap install code --classic
```

On **macOS**, and on any Linux without snap, download it from
[code.visualstudio.com](https://code.visualstudio.com/). The site detects
your platform and offers the right build. On macOS you drag the app into
Applications yourself; nothing installs it for you.

Success looks like an editor that opens to a Welcome tab. If you want to
launch it from a terminal later, `code .` opens the current folder.
That works out of the box on Windows and Linux. On macOS it doesn't until
you press `Cmd+Shift+P`, type "shell command", and pick **Install 'code'
command in PATH**, which is a step nobody tells you about.

### Open the vault, not the file

Choose **File > Open Folder** and pick your vault (`lab-journal`), not an
individual file. You get a file tree down the left, and every file you
make lands inside the vault instead of in whatever folder the save dialog
happened to remember. Fighting a save dialog over where your scripts live
is a waste of a perfectly good evening.

To create the script: right-click `Resources/scripts` in that tree,
choose **New File**, and type the full name including the extension, so
`machine-report.ps1` rather than `machine-report`. Paste the contents,
then `Ctrl+S` (`Cmd+S` on macOS) to save.

### The two things in the bottom-right corner

Once the file has a real extension, look at the status bar along the
bottom of the window. On the right you'll see something like
`PowerShell` and `CRLF` or `LF`.

The first is the **language**, which VS Code guessed from your file
extension. Your script turning multicoloured is the signal that the
extension is right. A `.ps1` that stays plain grey text usually means the
file is actually named `machine-report.ps1.txt`, which is Notepad's
favourite trick and is why I'd rather you weren't using Notepad.

The second is the **line endings**, and it's the one that bites in lesson
2.2. Windows ends every line of a text file with two invisible
characters; Linux and macOS use one. Nothing in this lesson cares. Bash
cares enormously. You'll meet it properly next lesson, with the fix.

Later in the course, when you're editing files on a server over SSH with
no desktop at all, you'll use `nano` in the terminal instead. That
arrives in Module 6, where you'll need it. Two editors for two situations
is normal: one for files on the machine in front of you, one for files on
a machine somewhere else.

## The script

Create `machine-report.ps1` in `Resources/scripts/` in your vault, the
way you just practised, and paste this in. Read every comment; the
comments are the lesson.

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

**How you know it took:**

```powershell
# Should print RemoteSigned. This asks specifically about your user
# account, which is the scope you just changed.
Get-ExecutionPolicy -Scope CurrentUser
```

Now run the script again, then open `Resources/machine-report.md` in
Obsidian and admire a report you didn't type.

**If it still refuses**, you are probably on a computer managed by a school
or an employer, where an administrator sets the policy centrally and your
change is overridden. `Get-ExecutionPolicy -List` shows every scope at once,
and a `MachinePolicy` or `UserPolicy` row with a value set is the culprit.
You cannot override that, and you should not try to on someone else's
machine. Two honest options: run the script's commands one at a time by
pasting them into the shell, which the policy does not restrict, or do the
scripting parts of this course inside a virtual machine once you build one in
Module 3.

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

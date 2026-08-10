---
title: "DET-14 Catch a forged identity (Golden SAML)"
sidebar_position: 20
---

# DET-14: Catch a forged identity (Golden SAML)

|  |  |
|---|---|
| **Objective** | When someone lifts your AD FS token-signing key and forges a login token, get an alert that names it, and does not fire when you run a routine Defender command |
| **Success signal** | You run the key-theft and token-forge tooling and an alert that names the technique arrives; a benign Defender command you run straight after produces nothing |
| **Needs** | Modules 8, 12 and 14, and **[DET-13](/drills/detection/det-13-wire-a-host-into-detection) done first** (Tier 2: this uses the AD FS server) |
| **Effort** | More than one sitting |
| **Risk** | Reversible with care. You extract your own signing key on an isolated lab you own, then clean it up. Read the authorisation note below |
| **Check** | Mechanical: the rule fires on the technique and stays silent on the benign command |

:::warning[Do DET-13 first, or this drill will show you nothing]

DET-14 assumes ADFS01 is already sending its logs to your manager: an agent
enrolled, the Sysmon channel forwarded, and PowerShell script-block logging turned
on. Module 12 wired those up on DC01, **not on ADFS01**, which you built later in
Module 8. If you run this drill on an unwired ADFS01, the attack will produce total
silence in your SIEM, and you will not be able to tell whether your rule is wrong,
the attack failed, or the events simply never arrived. [DET-13](/drills/detection/det-13-wire-a-host-into-detection)
closes that gap in an evening. Do it first.

:::

## Why this drill exists

In Module 8 you built AD FS and made it the front door to your other apps. One
account, one login, and every federated service trusts the token AD FS hands
back. That trust is the whole point of single sign-on, and it is also the whole
problem. The token is trusted because it is signed by AD FS's **token-signing
key**. Anyone who steals that key can sign their own tokens, and every app will
honour them, because the signature is genuine.

That attack is called **Golden SAML**. SAML (Security Assertion Markup Language)
is the token format you met in lesson 8.2. "Golden" is the same idea as a golden
ticket in Kerberos: forge the thing that everyone trusts, and you are anyone you
like, with no password and no multi-factor prompt, because you never touched the
login page at all.

The course taught you to build AD FS (Module 8), to write a detection rule
(lesson 12.4), and to attack your lab and check what your monitoring noticed
(lesson 14.9). It never taught you to catch **this**, the attack that turns your
own SSO into a skeleton key. This drill closes that gap.

:::warning[Isolated lab only, and leave it vulnerable on purpose]

You are about to extract a real signing key and forge a real token. Do this
**only** on the lab you built and own, the one behind your own firewall, exactly
as lesson 14.1 framed authorisation. Never against anything you do not own.

And for this drill, **do not patch or harden ADFS01.** Leave it as Module 8 built
it. The whole point is to practise catching the technique, so the technique has
to work. In a real job you would patch, and a patched server also does more to
fight the tooling, which you will see and which is itself part of what you detect
here. When you are done, revert the snapshot you took of ADFS01 when you built it
in lesson 8.3, and you are back to clean.

:::

## The trap this drill is built around

Ask "would my SIEM catch someone stealing my signing key?" and the honest answer
on your lab is **it will log the attack and tell you nothing.**

You did the work that captures it. Sysmon from lesson 12.3 records the processes
the attack starts. PowerShell script-block logging records the commands it runs.
Both are already flowing into the manager you built in lesson 12.2. So the events
exist.

But they arrive **decoded as generic noise.** A process starting looks like every
other process. A key-theft command in PowerShell trips a rule that says
"PowerShell used base64," which is true and useless, at a low severity, in the
same pile as every benign script your admin work runs all day. The single most
incriminating artefact the attack leaves, a Windows service whose own name gives
the tool away, arrives as "a new service was created," severity 5, filed next to
a printer driver installing.

**So this is not a drill about turning logging on.** It is about the gap between a
thing being logged and an alert naming it and being loud enough to act on. That
gap is where real intrusions live for months, and closing it is what detection
engineering actually is.

## Your objective

**Make the key-theft-and-forge sequence produce an alert you would act on, and
make sure that alert does not cry wolf on normal Defender administration.**

Four things must be true when you finish:

1. Running the key-export tooling produces an alert whose text **names** it as AD
   FS key theft or Golden SAML, not "base64 PowerShell."
2. That alert is **severe enough to stand out**, not buried at severity 3 to 5
   with the daily churn.
3. It **fires again** on a repeat run. A detection that works once and not twice
   is not a detection.
4. It **stays silent** when you run a routine Defender command such as
   `Get-MpComputerStatus`. This is the one people fail, for a reason the drill
   will show you.

Point four is not a nice-to-have. A rule that fires on the attack **and** on your
own everyday admin gets muted within a week, and a muted rule catches nothing.
"Fires on the thing, silent on everything else" is the standard, and it is why
the detection section exists.

## How you will know

You run the attack in one session and watch an alert that names it arrive. Then
you run a harmless Defender command and watch **nothing** arrive. If the attack is
silent, or the harmless command also alerts, the drill is not finished, however
right the rule looks in the file.

```powershell
# On ADFS01, after you have built your rule. Run the harmless command
# and confirm your new rule does NOT fire on it.
Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled
```

The real check is the pair of outcomes together: loud on the attack, quiet on the
admin command.

<details>
<summary>Nudge, if you do not know where to start</summary>

Do not write a rule first. Attack first, and look at what your SIEM already says,
because the "before" is half the lesson.

Three questions worth answering before you touch a rule:

- **What does the attack physically do on the box** that is unusual? It runs a
  tool, that tool starts something to reach the key, and it runs some very
  specifically named commands. Each of those is a different kind of evidence, in
  a different log you already collect.
- **Which of your Module 12 collectors sees each one?** You turned on more than
  you may remember. One watches processes. One watches PowerShell command text.
  Map each unusual action to the collector that would see it.
- **Why is what fires today useless?** Look at the severity and the wording of
  what you get. The wording describes the *shape* of the command, not the
  *intent*. Your job is to add the intent.

The tool this attack uses is well known and openly documented. Search for how AD
FS token-signing certificates get exported, and you will find the tooling and the
exact command names. Those command names are your detection.

</details>

<details>
<summary>Fuller hint, if you know the direction but not the specifics</summary>

**The tooling** is the AADInternals family of PowerShell modules. The forging
half and the key-stealing half ship as two separate modules, and Defender flags
the key-stealing one as malicious, which is your first piece of signal and your
first obstacle at once.

**The three artefacts worth detecting**, each in a channel you already collect:

- **A service creation.** To read the protected key, the tool spins up a
  short-lived Windows service, and the service name and its binary path both
  carry the tool's name. That is a Windows **event ID 7045**, which your manager
  already decodes into a "new service created" rule. Find that rule's ID, because
  you are going to build on top of it.
- **The command text.** The export and forge commands run in PowerShell, so their
  literal names land in the **script-block** channel (event 4104) you enabled in
  Module 12. Matching on the command names is the most direct detection.
- **Defence evasion.** To get its tooling past Defender, an attacker often adds a
  Defender exclusion first. That is a very specific PowerShell command too, and
  almost nothing benign does it. It is worth its own rule.

**The false-positive trap in point 4**, spelled out because it is not obvious:
when you run *any* Defender cmdlet, even a harmless read like
`Get-MpComputerStatus`, PowerShell logs the Defender module's own internal
machinery, and that machinery contains the words your naive rule is matching on.
So a rule that greps for the exclusion command loosely will fire every time you or
your automation so much as reads Defender's status. The fix is to match the
**command as it is actually typed**, the verb and the parameter next to each
other, not the words scattered anywhere in a block. This is the difference between
matching an invocation and matching a definition, and it is a mistake you will
make in real products for years if you do not meet it once in a lab.

Lesson 12.4 already taught you how to read an alert and write a rule that chains
onto an existing one. This is that skill, pointed at three specific artefacts.

</details>

<details>
<summary>Full walkthrough</summary>

Everything here runs on **ADFS01**, in an **elevated Windows PowerShell** (Run as
administrator), signed in as a domain admin, because that is who an attacker who
has already reached your federation server would be. Windows PowerShell 5.1, the
one that ships with the server, is fine and is what the tooling expects.

### 1. Attack first, so you can see the "before"

Get the forging module. It installs cleanly, because Defender does not object to
it on its own:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Install-Module AADInternals -Scope CurrentUser -Force
Import-Module AADInternals
```

**How you know it worked:** the banner prints and `Get-Command New-AADIntSAMLToken`
returns a command. Now try the key-stealing module:

```powershell
Install-Module AADInternals-Endpoints -Scope CurrentUser -Force
```

**Expect this to fail** with a message about the file containing a virus. That is
not you doing it wrong. That is Defender's real-time protection recognising the
key-theft tooling and refusing to install it, and it is the first thing worth
noticing: **one of your defences already reacted, and you should check in a
moment whether your SIEM heard it react.** An attacker's next move is to disable
that defence, so do what they would:

```powershell
# Defence evasion: tell Defender to ignore where the tool installs.
# An attacker does exactly this. So will you, so the rest can proceed.
Add-MpPreference -ExclusionPath "$env:USERPROFILE\Documents\WindowsPowerShell\Modules"
Install-Module AADInternals-Endpoints -Scope CurrentUser -Force
Import-Module AADInternals-Endpoints
```

Now steal the signing key and forge a token with it:

```powershell
# Export the token-signing certificate. On the AD FS server itself this
# reads the protected key material and writes the private key to disk.
New-Item -ItemType Directory -Force -Path C:\Temp\gs-drill | Out-Null
Set-Location C:\Temp\gs-drill
Export-AADIntADFSCertificates
```

```powershell
# Forge a signed SAML token with the stolen key. If a parameter name differs
# on your module version, that is fine: the command name is already logged,
# which is what your detection needs.
New-AADIntSAMLToken -PfxFileName C:\Temp\gs-drill\ADFSSigningCertificate.pfx `
    -Issuer "http://sso.lab.internal/adfs/services/trust" -ImmutableID "gs-drill" -ByPassID
```

**Failure is expected and is still a success for this drill.** Depending on your
Windows build and how hardened ADFS01 is, the export may stop partway with a
service error. It does not matter. Creating the service, adding the exclusion, and
naming the commands all happened, and all three are logged. The point is the
telemetry, not a working forged token.

### 2. Look at what your SIEM said, and write down how little it was

Go to your Wazuh dashboard and filter to ADFS01 over the last few minutes. Read
what fired.

**What are we doing, and why:** capturing the "before" state honestly, because the
gap between it and the "after" is the entire drill, and it is far more convincing
when it is your own screen than when I assert it.

You will see a handful of rules, and they will share three properties: generic
wording ("PowerShell used base64," "a new service was created"), low severity
(single digits), and no hint that these three events are one attack. Nothing says
"someone stole your signing key."

**Write two facts in your journal now:** the highest severity anything reached,
and whether a single one of the alerts named the technique. That is your baseline.

### 3. Find the three artefacts

You are going to detect three things. Find each in the raw events first, because a
rule you write against a field you have not seen is a guess.

- **The service.** Filter ADFS01 to Windows event ID **7045**. You are looking for
  a service whose name and whose `imagePath` both contain the tool's name. Note
  the exact field the manager decoded it into, and note the ID of the built-in
  rule that fired ("new service created"). You will chain onto it.
- **The commands.** Filter to event ID **4104**, the PowerShell script-block
  channel. Find the events carrying the export and forge command names. Note the
  field the command text lives in.
- **The exclusion.** In the same 4104 channel, find the `Add-MpPreference` command
  you ran. That is your defence-evasion artefact.

### 4. Write the rules, and make them name the attack

This is lesson 12.4's skill, three times. For each artefact, write a local rule
that chains onto the base rule for its channel, matches the specific evidence, and
carries a description that says what it **is**, at a severity that stands out.

The shape, without the answer, because writing it is the drill:

- **Chain, do not re-catch.** Each of your rules should sit on top of the existing
  rule that already decodes that channel, using the `if_sid` you noted in step 3,
  and add the one condition that makes it specific. You are not re-parsing the
  event, you are adding meaning to one the manager already understood.
- **Match the evidence you actually saw**, in the field you actually noted. For
  the service, the tool's name in the service name or its binary path. For the
  commands, the export and forge command names in the script-block text.
- **Name it in the description.** "Golden SAML: AD FS signing-key export" is a
  rule you can act on at 3am. "PowerShell used base64" is not.
- **Set a severity that escalates.** Look at how lesson 12.4's rule chose its
  level, and pick one that your alerting treats as worth waking up for, not one
  that dies in a daily digest.

Test each rule the way lesson 12.4 taught, before you rely on it, then re-run the
attack from step 1 and confirm your rules fire with your wording and your
severity.

### 5. The false-positive test, which is the real exam

Run the harmless command from the top of this drill:

```powershell
Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled
```

**How you know it worked:** your exclusion rule does **not** fire.

If it does fire, you have met the trap the fuller hint warned about: reading
Defender's status makes PowerShell log Defender's own internal code, which mentions
the very words a loose rule matches. Your rule matched a definition, not an
attacker's invocation. Tighten it so it only matches the command **as typed**, the
verb and its exclusion parameter directly next to each other, then run both the
attack and the harmless command again. Loud on one, silent on the other.

**Why this is the exam and not a footnote:** in step 4 you proved your rules can
fire. Only step 5 proves they are usable. A detection that also fires on your own
routine work is a detection your team turns off, and a rule nobody keeps on
catches nothing at all.

### 6. Clean up

```powershell
# Remove the Defender exclusion you added. Leaving it is a real hole.
Remove-MpPreference -ExclusionPath "$env:USERPROFILE\Documents\WindowsPowerShell\Modules"
```

```powershell
# Delete the stolen key and the tooling.
Remove-Item -Recurse -Force C:\Temp\gs-drill
Get-Service AADInternals* -ErrorAction SilentlyContinue | ForEach-Object { sc.exe delete $_.Name }
Uninstall-Module AADInternals-Endpoints -AllVersions -Force -ErrorAction SilentlyContinue
Uninstall-Module AADInternals -AllVersions -Force -ErrorAction SilentlyContinue
```

**How you know it worked:** `Get-MpPreference | Select-Object -ExpandProperty ExclusionPath`
no longer lists the module path, and `C:\Temp\gs-drill` is gone. The cleanest
finish, if you snapshotted ADFS01, is to revert the snapshot, which also undoes
anything the tooling touched that you did not think to.

</details>

## Going further

- **Detect the forged token in use, not only its making.** Everything above
  catches the key theft on ADFS01. A patient attacker steals the key on one day
  and uses it weeks later from somewhere else. What would a forged sign-in look
  like in your AD FS logs, and could you tell it from a real one? This is a harder
  and more honest question, and it is worth an evening.
- **Ask why the malware alert was quiet.** When Defender blocked the tooling in
  step 1, did your SIEM record that block? On many builds the Defender channel is
  collected but a single stalled event can stop it forwarding. Chase whether your
  own antivirus's reaction reached your dashboard. A defence that acts and tells no one
  is only half a control.
- **Rank your three rules.** You wrote three. Which one would survive an attacker
  who knew you were watching? The command-name rule breaks if they rename their
  copy of the tool; the service rule breaks the same way; the behaviour underneath
  does not. Write down which of your detections are brittle and why.

## What this proves

You can detect an identity-forgery attack that leaves no failed login, no locked
account, and no password anywhere, the kind that a "watch for brute force" mindset
never sees. And you did it with logs you were already collecting, by adding meaning
and urgency the manager's defaults did not.

You also met the discipline that separates a detection engineer from someone who
writes rules: **fires on the thing, silent on everything else.** Getting a rule to
fire is the easy half. Getting it to stay quiet on your own daily work is the half
that decides whether anyone leaves it switched on.

:::note[Write this down before you close the tab]

In your own words, in your journal, while it is fresh:

- What your SIEM said about the attack **before** you touched it, the highest
  severity and whether anything named it, so future-you can see how ordinary a
  real intrusion looks in the raw logs.
- The false positive in step 5: what your loose rule was really matching, and why
  a security product's own commands are a classic source of self-inflicted noise.

Six months from now you will remember writing a Golden SAML rule. You will not
remember that reading Defender's status nearly set it off, unless you write down
why.

:::

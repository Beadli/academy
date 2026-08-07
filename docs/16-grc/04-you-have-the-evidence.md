---
title: "16.4 You already have the evidence"
sidebar_position: 4
---

# 16.4 You already have the evidence

This is the lesson where fifteen modules of journal entries pay off.

Every module ended with a journal entry and a permanent note, and several
lessons told you specifically that what you were writing would be needed
here. Lesson 5.9 told you that "we tested DC failure and here is the
evidence" was exactly the kind of thing this module would ask you to produce
for real. Lesson 15.3 said the restore-test log is what an auditor asks for.
Lesson 14.1 called your rules of engagement the first item in the folder that
becomes an audit package.

Time to collect the folder.

## Three kinds of evidence, and why the third one is rare

Assessors distinguish between these, and the distinction decides whether a
control passes.

**Evidence of design.** A document saying what you intend. A policy, a
configuration standard, a runbook. It proves you thought about it.

**Evidence of implementation.** The thing existing and configured. A
`sshd_config`, a firewall rule, a GPO. It proves you did it.

**Evidence of operation.** The control working over time, repeatedly. A log
of restore tests, a change history, alert triage records. **It proves you are
still doing it.**

**Almost everybody produces the first two and almost nobody produces the
third**, which is why it carries the most weight. A backup script is design
plus implementation. A log of twelve monthly restore tests with dates and
outcomes is operation, and it is what makes an assessor stop asking.

This is exactly what lesson 13.7 was pointing at when it said Module 16 "is
where an auditor asks you to show evidence that it runs".

## Inventory what you have

Open your vault. You have been writing these since Module 1:

| Note | Module | Evidence it provides |
|---|---|---|
| `lab-network.md` | 4 | Addressing plan, segmentation test results |
| `lab-hosts.md` / `ubnt01.md` | 3, 6 | What exists, how it is configured |
| `lab-domain.md` | 5 | Directory design, OU structure, DC failure test |
| `lab-identity.md` | 8 | SSO design, federation trust |
| `lab-pki.md` | 7 | Key protection answers, certificate lifetimes |
| `lab-cloud.md` | 9 | Hybrid sync, what crosses the boundary |
| `lab-automation.md` | 10 | Playbooks, what is automated |
| `lab-ai.md` | 11 | How AI is used, what is not sent to it |
| `lab-detection.md` | 12 | Rules, tuning exceptions, coverage gaps |
| `lab-vulnerabilities.md` | 13 | Scan scope, prioritisation rule, accepted risks |
| `lab-attacks.md` | 14 | Techniques run, results, detection coverage table |
| `lab-assessment-2026.md` | 14 | The penetration test report |
| `lab-rules-of-engagement.md` | 14 | Authorisation for testing |
| `lab-operations.md` | 15 | RPO/RTO, backup scope, **restore test log** |
| `lab-changes.md` | 15 | Change history with rationale |
| `runbooks/` | 15 | Documented procedures |
| Daily notes | all | Dated record of what was done and what broke |
| Git history | all | Timestamped, attributed change record |

**Sit with that for a second.** Eighteen sources, accumulated as a side
effect of doing the work properly, covering design, implementation and
operation. Most people starting a first assessment have none of this and
spend weeks reconstructing it from memory, badly.

**If yours are thin, this is the moment that costs you.** Reconstruct what
you can from Git history and daily notes, and **be honest in the assessment
about which evidence was reconstructed after the fact**. Reconstructed
evidence is weaker than contemporaneous evidence, and pretending otherwise is
the kind of thing that ends careers in this field.

## The evidence that is genuinely strong

Three items in that list are unusually good, and you should know why so you
can say so in an interview.

**The detection coverage table from lesson 14.9.** It is evidence of
operation for AU-6, and more than that, it is evidence of *honest*
self-assessment: a table listing the attacks your own monitoring missed. An
assessor reading that trusts the rest of your document more, not less.

**The restore test from lesson 15.3.** Not "backups are configured" but "I
deleted data, restored it, and the checksums matched, on this date." That is
CP-9 and CP-10 evidenced to a standard most organisations cannot meet.

**The segmentation test from lesson 4.6.** Both directions tested, with the
exact commands and results recorded, which is precisely what SC-7 asks for.

## Build the evidence index

Do not copy everything into one document. Build an index that points at where
each thing lives, because that is what an assessor actually wants and it
stays current.

Create `Projects/gss1-evidence.md`:

```markdown
# GSS-1: evidence index

For each control, where the evidence lives and what kind it is.
D = design, I = implementation, O = operation.

| Control | Evidence | Kind | Location |
|---|---|---|---|
| AC-2 | Two-account model, sokoth / sokoth.adm | I | lab-domain.md |
| AC-2 | Domain Admins membership verified | I | lesson 5.6 output, lab-domain.md |
| AC-2 | Scanning account privilege justification, the one sentence lesson 13.6 asked you to write | D | lab-vulnerabilities.md |
| AC-8 | Logon banner GPO exists and is linked | I | lab-domain.md |
| AC-8 | gpresult output proving it reached a machine | O | lab-domain.md |
| AC-17 | sshd_config, PasswordAuthentication no | I | ubnt01.md |
| AC-17 | sshd -T output confirming enforcement | I | ubnt01.md |
| AU-2 | Wazuh agents enrolled, sources collected | I | lab-detection.md |
| AU-6 | Alert triage note from lesson 12.6 | O | daily note, dated |
| AU-6 | **Detection coverage table** | O | lab-attacks.md |
| CA-8 | Rules of engagement, authorised and dated. Lesson 14.1 called this "the first evidence in the folder Module 16 turns into an audit package" | D | lab-rules-of-engagement.md |
| CA-8 | Penetration test report | O | lab-assessment-2026.md |
| CM-3 | Change log with rationale and rollback | O | lab-changes.md |
| CM-3 | Git history of configs and playbooks | O | Gitea + GitHub |
| CP-9 | restic repository, retention policy | I | lab-operations.md |
| CP-9 | restic check output, no errors | O | lab-operations.md |
| CP-10 | **Restore test log with dates and outcomes** | O | lab-operations.md |
| CP-10 | Measured restore time vs stated RTO | O | lab-operations.md |
| CP-10 | DC failure test: DC01 powered off, logins and lookups still worked | O | lab-domain.md, lesson 5.9 |
| IA-2 | Kerberos in use, captured in lesson 5.5 | I | lab-domain.md |
| IA-5 | Key-based SSH, password policy in AD | I | ubnt01.md, lab-domain.md |
| RA-5 | Scan scope and schedule | D | lab-vulnerabilities.md |
| RA-5 | Scan results, KEV prioritisation | O | lab-vulnerabilities.md |
| RA-5 | Rescan proving remediation | O | rescan log, lesson 15.6 |
| SC-7 | Firewall policy stated | D | lab-network.md |
| SC-7 | FW01 rules implementing it | I | lab-network.md |
| SC-7 | **Both-direction segmentation test** | O | lab-network.md |
| SC-12 | Offline root; the four key-protection answers lesson 7.4 had you write, which it said would "become part of your system security plan" | D+I | lab-pki.md |
| SI-2 | Patching procedure and DC ordering | D | runbooks/, lesson 13.7 |
| SI-2 | Patch automation with serial: 1 | I | ansible repo |
| SI-2 | Patch log, dated | O | /var/log/patch-linux.log |
```

**Notice how many rows say O.** That is unusual and it is the strongest thing
about your position.

**Notice also which controls have only D or only I.** Those are the ones that
will assess as Partially Implemented in the next lesson, and spotting them
now saves you time.

## The evidence problem you cannot solve by writing more

One gap is worth naming before you assess, because it will come up.

**FW01's firewall rules are not in Git.** Lesson 15.8 identified this: the
things hardest to track are the things changed by clicking. So for SC-7 you
have design and implementation evidence, and your *change* evidence is
whatever you wrote in the change log by hand.

**Do not paper over that.** Write it as a limitation now, and it becomes a
POA&M item in lesson 16.7 with an obvious remediation: export the OPNsense
configuration into Git on a schedule.

That is what a real finding looks like. It is small, it is true, it has a
fix, and nobody had to attack anything to discover it.

## What you take from this

An evidence index covering fifteen controls, built from notes you already
wrote, with the three kinds of evidence distinguished and the gaps visible
before you start assessing.

Next lesson you grade yourself.

---
title: "14.10 Journal: what you proved, and what you assumed"
sidebar_position: 10
---

# 14.10 Journal: what you proved, and what you assumed

**Make a permanent note.** In your vault, create `Projects/lab-attacks.md`
and record:

- **Every technique you ran**, with the tool and one sentence on the
  mechanism. Not the command, the mechanism. "Kerberoasting: any user can
  request a service ticket, and it is encrypted with the service account's
  password hash, so it can be cracked offline."
- **Which ones worked, and which did not, and why.** A technique that failed
  because your configuration was sound is a *result*, and it belongs in the
  note with the reason.
- **The detection coverage table** from lesson 14.9.
- **Your three chosen improvements**, and their status.
- **The cleanup checklist below**, ticked.

Then link it to `Projects/lab-detection.md` from Module 12 and
`Projects/lab-vulnerabilities.md` from Module 13. Those three notes together
are the assessment half of your portfolio.

## Then today's daily note

Under **what I did**: the assessment, and one attack that surprised you.

Under **what broke**: this module breaks in a specific way, and it is worth
recording precisely. Tools that would not install. A technique that failed
because you had configured something correctly six modules ago. An attack
that worked instantly and taught you less than the one that did not. Write
down **which, and what you checked before you understood why**.

Under **what I learned**: pick one, and write it as though explaining it to
somebody who has not done this module.

- Why a stolen hash is a credential rather than a puzzle to solve
- Why the most dangerous techniques in this module were the ones that used
  features exactly as designed
- Why "nothing fired" has four different meanings and they need four
  different fixes

Under **open questions**: the good ones here are about coverage and about
honesty. Which of your machines would tell you if somebody were on it right
now? Which technique in this module do you understand well enough to explain
in an interview, and which did you only manage to run? What did you not test,
and would you be comfortable saying "untested" out loud about it?

## The exercise worth doing before you close

Answer this in writing:

**If you had to give somebody else's organisation one recommendation based on
what you learned this week, what would it be, and how would you justify it to
somebody who did not want to hear it?**

The justification is the hard part and it is the actual job. "Use gMSAs for
service accounts" is easy to say. Explaining it to a manager whose team owns
forty service accounts with hardcoded passwords in scripts, in terms of what
it costs them not to, is the skill that gets people promoted.

## The cleanup checklist, which is not optional

Run through this before you close the module. Every item is something that
makes your lab less safe if you leave it.

```bash
# On UBNT01: the deliberately vulnerable application is gone.
docker ps -a --format '{{.Names}}' | grep dvwa || echo "dvwa removed"

# The firewall hole you opened for it is closed.
sudo ufw status | grep 8081 || echo "8081 closed"

# No credential dumps left on KALI01. Check your home directory
# and anywhere you redirected tool output.
ls ~/*.txt ~/*.json 2>/dev/null || echo "nothing obvious"
```

On DC01:

```powershell
# The deliberately weak accounts from 14.5 and 14.6 are gone.
# Expect errors saying they cannot be found. Errors are success.
Get-ADUser -Identity svc-sql
Get-ADUser -Identity svc-backup
```

And by hand:

- [ ] Any `secretsdump` output shredded, not just deleted
- [ ] KALI01 back on its normal segment, per lesson 4.6
- [ ] The Tailscale rule from 14.1 restored, if you changed it
- [ ] Snapshots from 14.1 either kept deliberately or removed deliberately

**Do not restore the pre-attack snapshots** unless something is genuinely
broken. You changed real things in this module (rules you wrote, auditing you
enabled, accounts you removed) and rolling back throws that away too.

## Close the loop

```bash
cd ~/git/lab-journal
git status
git add -A
git commit -m "journal: module 14 complete"
git push
```

And your detections repository, which gained real rules this module:

```bash
cd ~/detections
git add -A
git commit -m "detections: dcsync, kerberoasting, and coverage notes from module 14"
git push
```

Tick Module 14 in `Projects/lab-progress.md`.

:::warning[What not to commit, and what not to publish]
Your assessment note describes exactly how to attack a real environment that
you own. Keep the journal repository private, as lesson 1.4 set it up to be.

More importantly: **the techniques in this module are portable and the
authorisation is not.** Everything you learned works against any Active
Directory environment. Your rules of engagement cover exactly one, on
`10.10.10.0/24`, and they expire on the date you wrote in them.

That is not a caution about getting caught. It is the professional boundary
this whole module was built around, and it is the thing that makes you
employable rather than a liability.
:::

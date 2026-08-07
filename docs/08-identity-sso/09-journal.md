---
title: "8.9 Journal: identity that travels"
sidebar_position: 9
---

# 8.9 Journal: identity that travels

Part of this entry is reference material you'll come back to, so give it
the same care as the network note in lesson 4.8.

**Make a permanent note.** In your vault, create
`Projects/lab-identity.md` and record:

- Which identity provider you built, or both, and at what addresses
- The client ID and redirect URI for each federation you configured. Not
  the client secret: that goes wherever you keep secrets, and lesson 1.6's
  rule about keeping them out of places they'll be read applies to notes
  as much as to chat windows.
- The realm name, if you used Keycloak, and why it isn't `master`
- The service account AD FS runs as, and whether it's a gMSA yet

Then today's daily note, four headings as usual.

Under **what I did**: the federation you built, and which application now
trusts which identity provider.

Under **what broke**: something did. This module's failures are unusually
uniform, so name yours specifically. A redirect URI that differed by a
character, a realm in a URL, a certificate the browser didn't trust, a
group membership that needed a reboot. Write the symptom *and* how you
found it, because the finding is the transferable part. "Compared the two
URLs character by character" is a technique you'll use for the rest of your
career.

Under **what I learned**: explain in your own words the difference between
authentication and authorisation, using what you saw in lesson 8.4 when
AD FS proved who you were and Gitea still gave you an ordinary account.
People conflate these two constantly, including in job interviews, and
being able to separate them cleanly marks you out.

Under **open questions**: "what happens to my federated logins if the
identity provider is down" is an excellent one, and worth thinking about
before Module 12 makes you monitor things. The answer is uncomfortable.

**Paste the decoded token from lesson 8.7 into the entry.** Redact the
signature if you like, but keep the payload. It's the most concrete
artefact this module produces, and in six months it will remind you what a
claim actually looks like far better than a description would.

```bash
cd ~/git/lab-journal
git add -A
git commit -m "journal: module 8, single sign-on working"
git push
```

Tick Module 8 in `Projects/lab-progress.md`.

Snapshot ADFS01 if you built it, and remember the rule from lesson 5.13:
domain controllers are the machines that need care with snapshots, and
ADFS01 is not one. Snapshot it freely.

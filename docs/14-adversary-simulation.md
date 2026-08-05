---
sidebar_position: 14
title: "Module 14: Adversary simulation"
---

# Module 14: Adversary simulation

:::warning[Not yet published]
This module is under construction.
:::

Only against your own lab. The authorization gate comes first, and it isn't
optional. Then: recon, AD attack paths from Kali, watching your own
detections fire, and tuning what didn't.

{/* AUTHORING NOTE, not rendered.
     Promises made by Module 9:
     - 9.6 introduces pass-the-hash by name and says "you will meet that idea
       properly in Module 14". Owed: the actual technique against the domain,
       and why the AD hash being fast to compute is what makes it viable.
     - 9.6 also states that syncing to the cloud does not improve the
       on-premises hash's weaknesses. Demonstrating that closes the loop.
     Module 12 is owed the other half: 9.8 argues that a stalled sync is more
     dangerous than a failed one, and that the thing worth alerting on is the
     absence of an expected event rather than an error. */}

{/* AUTHORING NOTE, not rendered.
     Promise added 2026-08-04 by lesson 6.9's new SQL injection section:
     "Defence in depth means the second control matters precisely because
     the first one sometimes fails. You will meet this idea again in
     Module 14, from the other side." Owed: the attacker's view of layered
     controls, and what it feels like when the first one holds. 
     Promises made by Module 13 (added 2026-08-05):
     - index and 13.10 both say Module 14 "takes that list and attacks it",
       so the findings become a way into a machine. Owed: at least one
       attack that starts from a finding the student produced in 13.5,
       rather than a vulnerability introduced for the purpose.
     - 13.5 says "Module 14 makes you write one properly", referring to a
       scope / rules-of-engagement document. Owed: the real version, with
       addresses, dates, techniques and a contact.
     - 13.6 has the student scope a scanning account and warns that a
       scanner with Domain Admin is a standard intrusion path. Worth
       demonstrating from the attacker's side if a path exists.
*/}

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
     controls, and what it feels like when the first one holds. */}

---
sidebar_position: 9
title: "Module 9: Hybrid identity with Entra ID"
---

# Module 9: Hybrid identity with Entra ID

:::warning[Not yet published]
This module is under construction.
:::

Almost no enterprise runs purely on-premises anymore, and almost none
runs purely in the cloud either. What they run is hybrid: the Active
Directory you built in Module 5 remains the source of truth for
identity, and it synchronizes to a cloud directory that fronts email,
SaaS applications, and everything else the business logs into. This
module builds that bridge with your own domain.

You'll create a cloud tenant, install the sync agent against your own
domain controller, watch your lab's users appear in the cloud, and sign
in to a cloud service with the same credentials you created in Module
5. Then the parts that make it worth understanding: what actually
crosses the wire (password hashes, not passwords), what happens to a
disabled account, and why the direction of authority matters so much
in an outage.

There's a reason this comes after eight modules of on-premises work
rather than before them. Cloud identity is a synchronization *of*
something. Students who start here learn to click through a portal that
manages users they don't understand the origin of. You'll be syncing a
directory you built, from a domain controller you promoted, using
accounts you created, which is the difference between operating a
system and operating a UI.

---
title: "Module 7: PKI and certificates"
sidebar_position: 0
---

# Module 7: PKI and certificates

You have collected two browser warnings so far. OPNsense threw one in
Module 4, Gitea threw another in Module 6, and both times I told you to
click through and that Module 7 would fix it properly. This is that
module, and by the end of it those warnings are gone because your
machines genuinely trust the certificates, not because you told them to
stop complaining.

That distinction is the whole subject. Anyone can make a warning go away
by clicking "accept the risk" forever. Building the thing that makes the
warning wrong in the first place is public key infrastructure, and it's
one of those areas where the number of people who can explain it end to
end is much smaller than the number of job postings that ask for it.

What's in it:

- **7.1** what a certificate is, and why yours isn't trusted
- **7.2** the offline root (Tier 2)
- **7.3** the issuing CA (Tier 2)
- **7.4** a CA that issues certificates automatically
- **7.5** teach your machines to trust it
- **7.6** HTTPS at last, issued automatically
- **7.7** templates and autoenrollment: certificates nobody requests (Tier 2)
- **7.8** revocation, CRLs, and the day it all stops (Tier 2)
- **7.9** journal entry
- **7.10** checkpoint

The module builds one hierarchy, top down, which is the order a real
organization builds in. **Tier 2 starts at 7.2** with the offline root
and the issuing CA beneath it. **Tier 1 starts building at 7.4**, where
step-ca gives you a real certificate authority in a container with no
extra virtual machines, and finishes with the same working HTTPS.

Tier 1 should still read 7.2 and 7.3. They're short, they're the PKI
most Windows employers actually run, and the offline-root idea in 7.2 is
the concept the rest of the module hangs off. This is the same
arrangement Module 4 used for the firewall lessons.

The payoff is shared: by 7.6 everyone has certificates issued
automatically and renewed without a human, and both browser warnings are
gone. Tier 2 then continues into templates, autoenrollment, and
revocation.

Budget an evening either side of 7.4. Nothing here is difficult; there's
just a lot of it, and the concepts in 7.1 carry the rest.

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
- **7.2** build a certificate authority you control
- **7.3** teach your machines to trust it
- **7.4** HTTPS at last, issued automatically
- **7.5** the enterprise pattern: an offline root and an issuing CA (Tier 2)
- **7.6** templates and autoenrollment: certificates nobody requests (Tier 2)
- **7.7** revocation, CRLs, and the day the lab stopped working (Tier 2)
- **7.8** journal entry
- **7.9** checkpoint

**Everyone does 7.1 through 7.4** and finishes with a real certificate
authority and real HTTPS, running in a container on UBNT01 with no extra
virtual machines. That's not a consolation prize: step-ca is production
software, it speaks the same protocol that issues certificates for most
of the public internet, and my own lab runs one.

**Tier 2 continues into 7.5 through 7.7**, which is the Microsoft
enterprise PKI most Windows shops actually run: an offline root, an
issuing CA, certificate templates, autoenrollment, and revocation. If
you're aiming at a Windows infrastructure or identity role, those three
lessons are the ones to read even if you can't build them.

Budget an evening for the first four lessons and a second evening for
the Tier 2 half. Nothing here is difficult; there's just a lot of it,
and the concepts in 7.1 carry the rest.

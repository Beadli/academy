---
title: "7.8 Journal: you are a certificate authority"
sidebar_position: 8
---

# 7.8 Journal: you are a certificate authority

The permanent note this time is closer to an operations runbook than a
set of facts, because PKI is the part of your lab most likely to break
long after you've forgotten how you built it.

**Create `Projects/lab-pki.md`** and record:

- Your CA's name, where it runs, and where the root private key lives
- The root certificate's fingerprint, and its expiry date
- Which machines trust it, and how they were told to (by hand, or by
  the Group Policy from lesson 7.3)
- Which certificates are currently issued, for which names, and by
  which CA
- How renewal happens, and how you would know if it stopped
- Tier 2: where ROOTCA01 is, that it is powered off deliberately, the
  CRL expiry date from lesson 7.7, and exactly what to do before then
- Tier 2: which templates exist and who may enrol for them

That list is close to what a real PKI runbook contains, and writing it
while the build is fresh is much easier than reconstructing it later.

**Daily note**, four headings.

Under **what I did**: the CA built, trust distributed, HTTPS issued and
automated, and on Tier 2 the two-tier structure and autoenrollment.

Under **what broke**: certificate work generates specific and memorable
failures. A file that didn't end in `.crt` and was silently ignored. A
certificate installed in the user store instead of the machine store. An
ACME challenge that couldn't be reached because of the firewall from
lesson 6.3. A chain that validated on the server and failed on your
laptop because only the leaf was installed. Whichever one got you, write
the error text; certificate error messages are famously unhelpful and
searchable notes about them are gold.

Under **what I learned**: explain in your own words why a root CA goes
offline, and what a CRL is for. If you can also say why an expired CRL
is worse than an expired certificate, you understand this better than
most people who administer a PKI.

Under **open questions**: "how would I move step-ca under the enterprise
CA" is a good one, and so is "what happens to my domain if I lose the
root key". Both have real answers and both are worth sitting with.

```bash
cd ~/git/lab-journal
git add -A
git commit -m "journal: module 7, own CA and real HTTPS"
git push
git push github main
```

Notice that push went over HTTPS to your own server, with a certificate
you issued, validated by a root you created. Tick Module 7 in
`Projects/lab-progress.md`, and snapshot UBNT01 and SUBCA01.

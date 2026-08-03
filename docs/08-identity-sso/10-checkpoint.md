---
title: "8.10 Checkpoint: one account, two systems"
sidebar_position: 10
---

# 8.10 Checkpoint: one account, two systems

Prove the module stuck. The test that matters is behavioural rather than a
command: can you sign in to an application you built, with an identity from
a system you built, without the application ever seeing a password.

## The end-to-end test

1. Log out of Gitea completely, and open a private browser window.
2. Go to `https://git.lab.internal` and click the sign-in button for your
   identity provider.
3. Authenticate.
4. Land back in Gitea, signed in.

If that works in a window with no existing session, the whole chain works:
DNS, certificate, trust, redirect URIs, client credentials and claims.

## Prove nothing is being faked

```bash
# The discovery document your application relies on. Substitute your own
# identity provider's URL.
curl -s https://id.lab.internal/realms/lab/.well-known/openid-configuration |
  python3 -c "import sys,json; d=json.load(sys.stdin); print('issuer:', d['issuer'])"
```

```powershell
# Tier 2, the AD FS equivalent.
Invoke-RestMethod https://sso.lab.internal/adfs/.well-known/openid-configuration |
    Select-Object issuer
```

Neither should need a `-k` or `--insecure` flag. If they do, the
certificate chain isn't trusted, and that's a finding rather than an
inconvenience.

## Pass criteria

Everyone:

- [ ] You can name the three parties in a federation and say which is
      which in your own lab (lesson 8.1)
- [ ] You can explain why Kerberos alone doesn't solve this, in one
      sentence (lesson 8.1)
- [ ] You can say what OAuth 2.0 is actually for, and why it is not an
      authentication protocol on its own (lesson 8.2)
- [ ] You can say what OpenID Connect adds to OAuth 2.0 (lesson 8.2)
- [ ] Keycloak is reachable at `https://id.lab.internal` with a valid
      certificate and no browser warning (lesson 8.5)
- [ ] Your applications live in a realm that is **not** `master`, and you
      can say why (lesson 8.5)
- [ ] Gitea has an OAuth2 authentication source and the sign-in button
      appears (lesson 8.6)
- [ ] **The end-to-end test above passes in a private window**
      (lesson 8.6)
- [ ] You decoded an ID token and can point at `iss`, `aud`, `exp` and
      `sub`, and say what each is for (lesson 8.7)
- [ ] You can explain why a JWT must never contain a secret (lesson 8.7)
- [ ] You captured the login in Wireshark and can say what was visible
      and what was not (lessons 4.7, 7.6, 8.7)
- [ ] `Projects/lab-identity.md` written, journal committed and pushed,
      Module 8 ticked (lesson 8.9)

Tier 2 as well:

- [ ] `https://sso.lab.internal` serves the AD FS sign-in page with a
      certificate from your own CA (lesson 8.3)
- [ ] You can say why the federation service name must differ from the
      server's hostname (lesson 8.3)
- [ ] A relying party trust exists for Gitea and its redirect URI matches
      what Gitea generates, exactly (lesson 8.4)
- [ ] You disabled a domain account and confirmed the federated login
      stopped working (lesson 8.4)
- [ ] A KDS root key exists and `Test-ADServiceAccount` returns `True`
      for your gMSA (lesson 8.8)
- [ ] You can explain what a gMSA removes that a service account with a
      password does not (lesson 8.8)

## The one that matters most

The disabled-account test, if you're on Tier 2.

Everything else in this module is plumbing you could learn from
documentation. That test demonstrates the thing federation is actually
bought for: one change, in one place, and access disappears from systems
you never touched.

In an organization without it, an employee leaving means somebody
remembering every application they ever had an account on. That is not a
process, it's a hope, and it is why old accounts outlive the people who
owned them by years.

## What you just finished

Your lab now has an identity that travels. A person exists once, in one
directory, and applications trust a signed statement about them rather
than holding their password.

That is genuinely the hard part of enterprise IT, and you built it on
infrastructure you made yourself: your directory, your certificate
authority, your DNS, your reverse proxy.

Module 9 takes the same identity and syncs it to a cloud directory, which
is how nearly every organization actually runs now: on-premises directory
as the source of truth, cloud as a follower. You'll meet the arrow
direction from lesson 0.3's diagram again, and this time it will be your
arrow.

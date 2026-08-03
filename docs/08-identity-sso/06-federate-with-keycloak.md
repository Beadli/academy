---
title: "8.6 Federate Gitea with Keycloak"
sidebar_position: 6
---

# 8.6 Federate Gitea with Keycloak

Same job as lesson 8.4, different identity provider, and short because
OIDC's discovery document does most of the work.

If you did the AD FS version, notice as you go how little changes. That's
the point of a standard protocol: the console looks nothing alike, the
concepts are identical.

## Register Gitea as a client

In the Keycloak admin console, **with the `lab` realm selected** (check the
dropdown, this is easy to get wrong): **Clients → Create client.**

<div className="labTable">

| Field | Value |
|---|---|
| Client type | OpenID Connect |
| Client ID | `gitea` |
| Client authentication | **On** |
| Valid redirect URIs | `https://git.lab.internal/user/oauth2/keycloak/callback` |

</div>

**Client authentication On** makes this a confidential client, meaning
Keycloak issues a secret that Gitea must present. Leave it off and any
application claiming to be `gitea` could request tokens.

That redirect URI is the character-for-character one from lesson 8.1.
Gitea builds it as:

```text
https://<your gitea>/user/oauth2/<source name>/callback
```

So the source you create in Gitea must be named exactly **`keycloak`**. One
lowercase word, no spaces, or the URL gains a `%20` and stops matching.

Save, then go to the **Credentials** tab and copy the **Client secret**.
You need it in a moment.

## Point Gitea at Keycloak

In Gitea: **Site Administration → Identity & Access → Authentication
Sources → Add Authentication Source.**

<div className="labTable">

| Field | Value |
|---|---|
| Authentication Type | OAuth2 |
| Authentication Name | `keycloak` |
| OAuth2 Provider | OpenID Connect |
| Client ID (Key) | `gitea` |
| Client Secret | the value you just copied |
| Auto Discovery URL | `https://id.lab.internal/realms/lab/.well-known/openid-configuration` |

</div>

Note the realm name in that URL. Point it at `master` by mistake and
authentication will fail for a user who exists, which is a genuinely
confusing ten minutes.

Confirm the discovery document is reachable before saving:

```bash
curl -s https://id.lab.internal/realms/lab/.well-known/openid-configuration |
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['issuer']); print(d['authorization_endpoint'])"
```

Expect two URLs on `id.lab.internal`. If `curl` fails on the certificate,
the machine doesn't trust your CA yet.

**Read the callback URL Gitea shows you** and compare it to what you put in
Keycloak. Then save.

## Sign in

Log out fully, or use a private window.

Click **Sign in with keycloak**, authenticate as `sokoth`, and you should
land back in Gitea signed in.

When it fails, it's one of these:

- **Keycloak says "Invalid parameter: redirect_uri".** The two URLs differ.
  This is the failure lesson 8.1 promised you.
- **Gitea reports an error fetching the discovery document.** Wrong realm
  in the URL, or the certificate isn't trusted.
- **You reach Keycloak but the login is rejected.** The user exists in the
  wrong realm, or the password is still marked Temporary.
- **You get in but with no email address.** The Keycloak user has no email
  set. Gitea wants one; add it to the user.

## Compare the two

If you built both, this is the part worth pausing on.

<div className="labTable">

| | AD FS | Keycloak |
|---|---|---|
| Runs on | a Windows Server VM | a container |
| Users come from | Active Directory, directly | its own store, or a federated directory |
| Configured by | PowerShell, or a console | a web console, or an API |
| Costs | a Windows licence and a VM | nothing |
| You'll meet it | Microsoft-centric organizations | most other places |

</div>

**The protocol did not change.** Same discovery document, same client ID
and secret, same redirect URI, same ID token. Gitea's configuration screen
was identical apart from which URL you pasted.

That's worth internalising, because it's the actual transferable skill.
Products come and go, and the interview question "have you used Okta?" is
really asking whether you understand the three parties from lesson 8.1.
Once you can configure one, the next one is an afternoon of finding where
the same five fields are hiding.

## Make it yours

1. Add a second user in the `lab` realm and sign in as them. Then delete
   that user in Keycloak and try again, watching the failure happen from
   the identity provider's side rather than the application's.
2. Turn on **Require SSL** or session timeout settings in the realm and
   observe the effect. Policy applied in one place, felt in every
   application behind it, which is the second selling point from 8.1.
3. Harder, and genuinely useful: point Keycloak at your Active Directory
   as a **user federation** source, so the accounts come from the
   directory instead of Keycloak's own store. That's the arrangement many
   real deployments use, and it puts every concept in this module into one
   pipeline: directory holds the people, Keycloak speaks the protocol,
   Gitea trusts the token.

---
title: "8.4 Federate Gitea with AD FS (Tier 2)"
sidebar_position: 4
---

# 8.4 Federate Gitea with AD FS (Tier 2)

Now the payoff. Gitea currently has its own accounts, stored in the SQLite
database you opened in lesson 6.9. By the end of this lesson it will stop
checking passwords and start trusting your domain instead.

This is the lesson where you'll meet the URL-mismatch failure from 8.1. Go
slowly at the two places that mention addresses.

## Tell AD FS about the application

AD FS calls an application a **relying party**, and teaching it about one
is creating a **relying party trust**. In OIDC terms, which is what you're
using, it's registering a client.

```powershell
# On ADFS01.
# -Name is for your own reference in the console.
# -ClientId is the identifier Gitea will send. Any unique string works;
#   a GUID is conventional, but a readable name is easier to debug.
# -RedirectUri is the exact address AD FS will send the browser back to
#   after login. This is the one that has to match, character for
#   character, what Gitea expects.
Add-AdfsNativeClientApplication `
    -Name "Gitea" `
    -ApplicationGroupIdentifier "Gitea" `
    -Identifier "gitea" `
    -RedirectUri "https://git.lab.internal/user/oauth2/adfs/callback"
```

Look hard at that redirect URI. Gitea builds its callback address from the
**name you give the authentication source**, in this format:

```text
https://<your gitea>/user/oauth2/<source name>/callback
```

So if you name the source `adfs` in Gitea, the URL ends `/adfs/callback`.
Name it `AD FS` with a space and the URL contains `%20` and no longer
matches what you just registered. **Use a single lowercase word with no
spaces.** This course uses `adfs`.

Now create the application group and permit the OIDC scopes:

```powershell
# openid asks for an ID token, which is the who-are-you part from 8.2.
# profile and email carry the name and address claims Gitea wants.
Grant-AdfsApplicationPermission `
    -ClientRoleIdentifier "gitea" `
    -ServerRoleIdentifier "https://git.lab.internal" `
    -ScopeNames @("openid","profile","email")
```

## Find the discovery document

Everything Gitea needs to know about AD FS lives at one well-known
address, which is the OIDC feature that makes this configuration short:

```powershell
Invoke-RestMethod https://sso.lab.internal/adfs/.well-known/openid-configuration |
    Select-Object issuer, authorization_endpoint, token_endpoint
```

That should return three URLs. Keep the discovery address itself; it's the
single value you paste into Gitea next.

## Tell Gitea about AD FS

In Gitea, as an administrator: **Site Administration → Identity &
Access → Authentication Sources → Add Authentication Source.**

<div className="labTable">

| Field | Value |
|---|---|
| Authentication Type | OAuth2 |
| Authentication Name | `adfs` |
| OAuth2 Provider | OpenID Connect |
| Client ID (Key) | `gitea` |
| Client Secret | leave blank for a native client |
| OpenID Connect Auto Discovery URL | `https://sso.lab.internal/adfs/.well-known/openid-configuration` |

</div>

**Before you save, read the callback URL Gitea displays on that page.** It
generates it live from the name you typed. It must be identical to the
`-RedirectUri` you registered with AD FS. If they differ, fix it now
rather than debugging it in a minute.

Save, and a "Sign in with adfs" button appears on the login page.

## Try it, and expect the first attempt to fail

Log out of Gitea entirely. Use a private browser window, because a
half-signed-in session is its own confusing failure.

Click **Sign in with adfs**. You should be redirected to
`sso.lab.internal`, authenticate as `sokoth`, and land back in Gitea signed
in as a new user.

If it fails, work through these in order. They cover nearly every case:

- **"Invalid redirect URI" or an AD FS error page.** The two URLs disagree.
  Compare them character by character, including `https` versus `http` and
  any trailing slash.
- **A certificate warning, or an error about a signature.** The machine you
  are browsing from does not trust the CA. Domain-joined machines got the
  root automatically in lesson 7.5; anything else needs it installed.
- **You are signed in but the account has a strange name.** That's not a
  failure, it's the claims. See below.
- **AD FS says the application is unknown.** The client ID Gitea sends does
  not match the `-Identifier` you registered.

## What just happened, and what didn't

You are signed in to Gitea with a domain account, and **Gitea never saw the
password.** It received a signed token, checked the signature against AD
FS's published key, and trusted the contents.

Two things are worth noticing before you move on.

**Gitea created a new user.** Federated login does not merge with the local
account you made in lesson 6.6. They are separate identities as far as
Gitea is concerned, one local and one federated. In a real migration, that
mapping is the hard part of the project, not the protocol.

**Authentication is not authorisation.** AD FS proved who you are. It said
nothing about what you may do, and Gitea defaulted you to an ordinary user.
Gitea can read group membership from a claim and map it to teams, which is
how a real deployment grants admin rights from a directory group rather
than by hand. That's the natural next step, and it's a good "make it yours"
exercise once the login works.

## Make it yours

1. Sign in with a second domain account and confirm it also gets in. One
   working login can be luck; two is a system.
2. Disable `sokoth` in Active Directory, then try to sign in. This is the
   central-control point from lesson 8.1, and feeling it is the lesson:
   one change in the directory locked an application you never touched.
3. Harder: configure Gitea's group claim mapping so that members of a
   directory group become Gitea administrators. You'll need AD FS to emit
   a group claim and Gitea's group settings to consume it. This is exactly
   how it's done in production.

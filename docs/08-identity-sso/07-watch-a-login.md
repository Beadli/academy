---
title: "8.7 Watch a login happen"
sidebar_position: 7
---

# 8.7 Watch a login happen

You have a working single sign-on and no idea what it did. This lesson
fixes that, and it's the one that turns federation from magic into
mechanism.

Two tools, and the difference between what each can see is itself the
lesson.

## First, the shape: Wireshark

Start a capture as you did in lesson 4.7, filter for your identity
provider, and sign in to Gitea.

```text
ip.addr == 10.10.10.20 && tcp.port == 443
```

Stop the capture and look at what you collected. You will see TLS
handshakes to two different hosts and a good deal of traffic, and you will
be able to read **none of it**, exactly as lesson 7.6 promised.

That's not a failure of the exercise. It's the finding:

**You can see the shape of the conversation but not its contents.** The
sequence of hosts contacted, the timing, the fact that a login occurred at
all. Not the username, not the token, not the password. Encryption did its
job, on infrastructure you built.

The visible SNI field from lesson 7.6 is why you can tell which host is
which. That distinction, metadata visible and payload hidden, is the whole
basis of the detection work in Module 12.

## Then, the contents: browser developer tools

To see inside, you have to be an endpoint. Your browser is one.

Open developer tools with **F12**, go to the **Network** tab, and tick
**Preserve log**. Without it the redirects wipe the list before you can
read them. Then sign in.

You'll see a chain something like this:

```text
git.lab.internal/user/oauth2/keycloak    302  →  redirect to the IdP
id.lab.internal/realms/lab/protocol/...  200  →  the login page
id.lab.internal/.../login-actions/...    302  →  you posted credentials
git.lab.internal/user/oauth2/.../callback 302 →  back with a code
git.lab.internal/                        200  →  signed in
```

Read that as a story. Gitea didn't know you, so it sent your browser to
the identity provider. You proved yourself there. The identity provider
sent your browser back to Gitea carrying a **code**. Gitea then exchanged
that code for tokens in a direct call you cannot see in this list, because
it happened server-to-server rather than through your browser.

That last step is deliberate in OIDC's design. The valuable token never
travels through the browser at all, so a hostile browser extension or a
leaked URL doesn't hand over the keys.

Notice also that **your password appears exactly once**, in a POST to the
identity provider. Gitea never saw it. That's the claim from lesson 8.1,
now visible rather than asserted.

## Read the token

The ID token is signed JSON, and signed does not mean secret. Anyone
holding one can read it. Proving that to yourself is worth five minutes,
because a lot of people assume otherwise and build accordingly.

Get a token to look at. Keycloak's admin console will issue you one, or
you can decode any JWT you find in the network tab. A JWT is three
base64url segments separated by dots: header, payload, signature.

```bash
# Paste a JWT into the variable, then decode the middle segment.
# tr converts base64url to standard base64; the printf pads it to a
# multiple of four characters, which base64 requires.
TOKEN='paste.the.jwt'
echo "$TOKEN" | cut -d. -f2 | tr '_-' '/+' |
  { read -r p; printf '%s%s' "$p" "$(printf '=%.0s' $(seq $(( (4 - ${#p} % 4) % 4 ))))"; } |
  base64 -d 2>/dev/null | python3 -m json.tool
```

You'll get something like:

```json
{
  "exp": 1785690000,
  "iss": "https://id.lab.internal/realms/lab",
  "aud": "gitea",
  "sub": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
  "preferred_username": "sokoth",
  "email": "sokoth@lab.internal"
}
```

Four of those fields are doing the security work, and they're worth
knowing by name because every token you ever debug has them:

- **`iss`** (issuer). Who made this. Gitea checks it matches the identity
  provider it was configured to trust.
- **`aud`** (audience). Who it's for. A token minted for a different
  application must be rejected, and forgetting this check is a real
  vulnerability class.
- **`exp`** (expiry). A Unix timestamp, usually minutes away. Short life
  is the mitigation for a stolen token.
- **`sub`** (subject). The stable, permanent identifier for the user.
  Note it is not the username. Usernames change; this doesn't, which is
  why applications should key off it.

```bash
# When does that token die?
date -d @1785690000
```

**The signature is the only thing that makes any of this trustworthy.** The
payload is readable and trivially editable by anyone. Change one character
and the signature no longer verifies, which is what the receiving
application checks and why it needs the issuer's public key.

## The security point people miss

Because a JWT is readable, **never put anything secret in one**. They
routinely travel through browsers, get logged by proxies, and end up in
error reports.

And because the signature is the whole defence, an application that
accepts a token without verifying the signature, or without checking `aud`
and `exp`, has no security at all while appearing to work perfectly. Both
are common enough to have their own entries in vulnerability
classifications, and Module 14 will look at what that costs.

## Make it yours

1. Sign in, then decode the token and check `exp`. Wait for it to pass and
   see what Gitea does. Most applications hold their own session well past
   token expiry, which is worth knowing before you assume expiry logs
   people out.
2. Capture the login again in Wireshark, this time filtering only on
   `tls.handshake.type == 1` (Client Hello) and note the SNI values. That's
   the metadata trail a network monitor sees for every federated login,
   without decrypting anything.
3. Compare `sub` across two different logins for the same user. It should
   be identical. Then compare it with `preferred_username` after renaming
   the user, and you'll see why applications are told to key on `sub`.

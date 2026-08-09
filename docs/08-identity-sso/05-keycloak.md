---
title: "8.5 Keycloak: the same job, in a container"
sidebar_position: 5
---

# 8.5 Keycloak: the same job, in a container

**Every tier does this one.** If you're on Tier 1 and skipped the AD FS
lessons, this is where your hands-on federation starts. If you're on Tier
2 and already have AD FS running, do it anyway: comparing the two is worth
more than either alone, and Keycloak is what you'll meet outside Microsoft
shops.

Keycloak is an open-source identity provider. It speaks SAML, OAuth 2.0 and
OIDC, it runs in a container, and it needs no Windows server. It's also in
wide production use, so this isn't a toy substitute for the real thing.

Everything you need is already on UBNT01: Docker from lesson 6.4, the
compose pattern from 6.5, nginx from 6.7, and certificates from 7.6.

## The stack

Keycloak keeps its data in a database, exactly as Gitea does. Create the
project folder and secrets:

```bash
mkdir -p ~/docker/keycloak && cd ~/docker/keycloak

printf 'KC_ADMIN_PASSWORD=%s\n' "$(openssl rand -hex 16)" > .env
printf 'DB_PASSWORD=%s\n' "$(openssl rand -hex 16)" >> .env
chmod 600 .env
cat .env
```

Expect two long random values. Keep this file; the admin password is the
only way into the console.

**You just wrote two live passwords into a Git repository**, because `~/docker`
has been under version control since lesson 6.5 and gets pushed to Gitea.
Check that the rule you wrote back then is doing its job:

```bash
cd ~/docker

# -uall names untracked files individually, the flag from lesson 1.3.
# Without it Git collapses the folder to "keycloak/" and you learn
# nothing. Expect keycloak/compose.yaml. Do NOT expect .env.
git status --short -uall

# The direct question, the same one lesson 1.3 asked about the vault.
# Printing the path back means "yes, ignored".
git check-ignore keycloak/.env
```

That silence in `git status` is the whole point of writing the rule three
modules before you had a file to put in it.

Now record what the file *contains* without recording the values, because a
repository that cannot rebuild the stack is not doing its job either:

```bash
# The keys, with the values deliberately left out. This one IS committed.
printf 'KC_ADMIN_PASSWORD=\nDB_PASSWORD=\n' > keycloak/.env.example

git add keycloak/.env.example
git commit -m "keycloak: document the required environment variables"
```

**That pairing is the convention**, and it is worth carrying to every project
you ever touch: `.env` is ignored and holds the secrets, `.env.example` is
committed and holds the shape. Six months from now the example file is what
tells you the stack needs two passwords, and nothing anywhere tells anyone
what they were.

Write `~/docker/keycloak/compose.yaml`:

```yaml
services:
  keycloak:
    image: quay.io/keycloak/keycloak:26
    restart: unless-stopped
    # start-dev is deliberate for a lab: it skips the production
    # hostname and TLS checks that would otherwise need configuring
    # before you can see anything. nginx provides the real TLS.
    command: start-dev --http-port=8080 --proxy-headers=xforwarded
    environment:
      KC_BOOTSTRAP_ADMIN_USERNAME: admin
      KC_BOOTSTRAP_ADMIN_PASSWORD: ${KC_ADMIN_PASSWORD}
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://db:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: ${DB_PASSWORD}
    ports:
      # Loopback only, as with every service since lesson 6.5.
      - "127.0.0.1:8080:8080"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - keycloak-db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U keycloak"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  keycloak-db:
```

Two directives deserve a sentence.

**`--proxy-headers=xforwarded`** tells Keycloak it sits behind a reverse
proxy and should believe the `X-Forwarded-*` headers nginx sends. Without
it, Keycloak builds its redirect URLs from the address it can see, which
is `localhost:8080`, and every login bounces the browser somewhere that
doesn't exist. This is the single most common Keycloak-behind-nginx
failure.

**`start-dev`** skips production hostname and TLS strictness. For a lab
where nginx terminates TLS that's the right trade. A production deployment
uses `start` and configures those properly, which the Keycloak
documentation covers well.

Start it:

```bash
docker compose up -d
docker compose logs -f keycloak    # watch for "Listening on", then Ctrl-C
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/
```

Expect `200` or `302`. First boot runs database migrations and takes a
minute or two.

## Give it a name and a certificate

Same two steps as Gitea in lessons 6.7 and 7.6, so this should feel
familiar rather than new.

**DNS.** On DC01, or in your hypervisor's DNS if you're Tier 1 without a
domain yet:

```powershell
Add-DnsServerResourceRecordA -ZoneName "lab.internal" `
                             -Name "id" `
                             -IPv4Address "10.10.10.20"
```

That points `id.lab.internal` at UBNT01, where the container runs.

Confirm it resolves before going further, because everything below depends
on the name working:

```bash
# On UBNT01. Expect 10.10.10.20.
dig +short id.lab.internal
```

**Certificate.** Same acme.sh client you installed in lesson 7.6, pointed at
the same CA, for a new name. You do not need to reread that lesson; the two
commands are here:

```bash
# Issue it from your own CA.
~/.acme.sh/acme.sh --issue -d id.lab.internal --standalone

# Put it where nginx will read it, and register the reload for renewals.
mkdir -p /etc/nginx/certs
~/.acme.sh/acme.sh --install-cert -d id.lab.internal \
  --key-file       /etc/nginx/certs/id.key \
  --fullchain-file /etc/nginx/certs/id.crt \
  --reloadcmd      "systemctl reload nginx"
```

The certificate and key must be a pair, which is lesson 7.6's check and is
worth repeating whenever you issue a new one:

```bash
# These two hashes must match.
openssl x509 -noout -modulus -in /etc/nginx/certs/id.crt | openssl md5
openssl rsa  -noout -modulus -in /etc/nginx/certs/id.key | openssl md5
```

**Vhost.** Now create `/etc/nginx/sites-available/keycloak`:

```nginx
server {
    listen 80;
    server_name id.lab.internal;
    include snippets/acme-challenge.conf;
    location / { return 301 https://$host$request_uri; }
}

server {
    listen 443 ssl http2;
    server_name id.lab.internal;

    ssl_certificate     /etc/nginx/ssl/id.lab.internal/id.lab.internal.crt;
    ssl_certificate_key /etc/nginx/ssl/id.lab.internal/id.lab.internal.key;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;

        # Keycloak builds every redirect URL from these. Get them wrong
        # and logins bounce to localhost. This is what --proxy-headers
        # in the compose file is trusting.
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host  $host;
        proxy_set_header X-Forwarded-Port  443;
    }
}
```

Enable it, and remember the order from lesson 6.7: test before reloading.

```bash
sudo ln -s /etc/nginx/sites-available/keycloak /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Browse to **`https://id.lab.internal`**. Padlock, no warning, Keycloak's
welcome page.

:::tip[What this is called at work]
Keycloak's commercial equivalents are **Okta, Auth0, Ping and Entra ID**, and
Keycloak itself is genuinely used in production, usually where an organisation
wants to own its identity layer rather than rent it.

The concepts you are about to meet are the ones those products charge for:
**realms** are tenants, **clients** are applications, and mappers decide which
attributes an application is told about. Every one of those exists in Okta and
Auth0 under a slightly different name.

**The paid ones mostly sell you not operating it**, plus the integration
catalogue. Thousands of pre-built application connectors is a real feature and
the reason procurement chooses them, and it is worth knowing that is what the
money buys rather than better protocol support.
:::

## First login and a realm

Sign in to the administration console with `admin` and the password from
your `.env`.

**Change nothing else until you've made a realm.** A **realm** is an
isolated tenant: its own users, its own clients, its own signing keys.
Keycloak ships with one called `master`, and its only job should be
administering Keycloak itself.

Putting your applications in `master` is the beginner mistake, because it
gives every application's users a path to the system that controls all
your applications. It's the same instinct as the two accounts in lesson
5.6, one layer up.

Create one: the realm dropdown at the top left → **Create realm** → name
it **`lab`** → Create.

Then create a user in it: **Users → Add user**, username `sokoth` to match
the domain account, and set a password under the **Credentials** tab with
**Temporary** switched off.

:::tip[Least privilege]
The realm split is the principle again. `master` administers Keycloak;
`lab` holds the people who use your applications. A compromise of an
application account in `lab` reaches nothing in `master`.

The same reasoning produced the offline root in 7.2 and the read-only
database connection in 6.9. Once you start seeing it, it's everywhere in
well-built systems, and its absence is one of the fastest ways to spot a
system that was assembled rather than designed.
:::

Keycloak now knows who `sokoth` is. Next lesson makes Gitea trust it.

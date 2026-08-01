# Beadli Lab Academy

**Build the enterprise yourself — then defend it.**

A free, hands-on infrastructure & security curriculum. Students build,
operate, defend, and attack their own mock enterprise environment — Active
Directory, PKI, SSO, Docker, Ansible, monitoring & detection — on VMware
Workstation or VirtualBox, from a bare laptop to a full homelab.

**Live site:** <https://academy.beadli.com>

## Repo layout

- `docs/` — course content (MkDocs Material)
- `mkdocs.yml` — site configuration
- `.github/workflows/deploy.yml` — builds and deploys to GitHub Pages on
  every push to `main`

## Local development

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve -a 127.0.0.1:8001   # live preview at http://127.0.0.1:8001
```

(The non-default port avoids collisions with other services; on devserver,
8000 is taken by SO-CRATES.)

## Licensing

- **Course text** (everything under `docs/`): [CC BY-NC-SA 4.0](LICENSE-CONTENT.md)
- **Code samples, scripts, and playbooks:** [MIT](LICENSE)

## Status

Structure is live; modules are being authored and published in order.
See the [site](https://academy.beadli.com) for what's currently available.

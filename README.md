# Beadli Lab Academy

**Build the enterprise yourself — then defend it.**

A free, hands-on infrastructure & security curriculum. Students build,
operate, defend, and attack their own mock enterprise environment — Active
Directory, PKI, SSO, Docker, Ansible, monitoring & detection — on VMware
Workstation or VirtualBox, from a bare laptop to a full homelab.

**Live site:** <https://academy.beadli.com>

## Repo layout

- `docs/` — course modules (Docusaurus, MDX-capable Markdown)
- `src/` — landing page and theme components
- `docusaurus.config.js` — site configuration
- `.github/workflows/deploy.yml` — builds and deploys to GitHub Pages on
  every push to `main`

## Local development

```bash
npm ci
npm start -- --port 8002        # live-reload dev server at http://127.0.0.1:8002
npm run build                    # production build into build/
npm run serve -- --port 8002    # serve the production build
```

(The non-default port avoids collisions with other services on the dev host.)

## Licensing

- **Course text** (everything under `docs/`): [CC BY-NC-SA 4.0](LICENSE-CONTENT.md)
- **Code samples, scripts, and playbooks:** [MIT](LICENSE)

## Status

Structure is live; modules are being authored and published in order.
See the [site](https://academy.beadli.com) for what's currently available.

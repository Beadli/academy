---
title: "10.5 Templates, variables and handlers"
sidebar_position: 5
---

# 10.5 Templates, variables and handlers

:::note[Activate first]
Every command in this lesson runs on **UBNT01**, inside the virtual environment
from lesson 10.2.

```bash
cd ~/ansible
source .venv/bin/activate
```
:::

Lesson 10.3 set individual lines in existing files. That works until the file
is mostly yours, at which point you want to own the whole thing.

In lesson 6.7 you wrote an nginx configuration by hand. This lesson generates
it, from a template, with values that differ per machine, and restarts nginx
only when the file actually changed.

## Variables: stop hardcoding

Values that differ between machines belong outside the playbook.

Create `~/ansible/group_vars/linux.yml`. That filename is not arbitrary:
Ansible automatically loads `group_vars/<groupname>.yml` for hosts in that
group, which is a convention worth knowing because it means variables land
without being wired up.

```yaml
---
site_name: git.lab.internal
proxy_upstream: "http://127.0.0.1:3000"
admin_email: sam@lab.internal
```

## Templates: a config file with holes in it

A template is a file with placeholders, filled in when it is deployed.
Ansible uses **Jinja2**, which you will also meet in Python web frameworks and
in a dozen other tools.

Create `~/ansible/templates/site.conf.j2`:

```jinja
# Managed by Ansible. Local edits will be overwritten.
# Source: {{ ansible_managed }}

server {
    listen 80;
    server_name {{ site_name }};

    location / {
        proxy_pass {{ proxy_upstream }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

`{{ site_name }}` gets replaced. `$host` does not, because that is nginx's own
syntax and Jinja leaves it alone.

:::tip[The comment at the top is not decoration]
"Managed by Ansible. Local edits will be overwritten." is the most valuable
line in that file.

Without it, someone eventually SSHs in at 2am, fixes something by hand, and
goes to bed pleased. The next playbook run silently reverts them, and the
outage comes back with no obvious cause. That person is usually you, six
months later.

`{{ ansible_managed }}` expands to a string identifying the source file, so
the comment tells the reader not just that it is managed, but *where the real
version lives*. Put it at the top of every file you generate.
:::

## Handlers: do something only if something changed

Restarting nginx on every run is wasteful and breaks idempotence. You want to
restart it *only* when the configuration actually changed.

That is a **handler**: a task that runs at the end of the play, only if
something notified it, and only once no matter how many tasks notified it.

Create `~/ansible/webserver.yml`:

```yaml
---
- name: Reverse proxy configuration
  hosts: linux
  become: true

  tasks:
    - name: nginx is installed
      ansible.builtin.apt:
        name: nginx
        state: present

    - name: Site configuration is deployed
      ansible.builtin.template:
        src: templates/site.conf.j2
        dest: /etc/nginx/sites-available/{{ site_name }}.conf
        owner: root
        group: root
        mode: '0644'
        validate: 'nginx -t -c /etc/nginx/nginx.conf'
      notify: Restart nginx

    - name: Site is enabled
      ansible.builtin.file:
        src: /etc/nginx/sites-available/{{ site_name }}.conf
        dest: /etc/nginx/sites-enabled/{{ site_name }}.conf
        state: link
      notify: Restart nginx

  handlers:
    - name: Restart nginx
      ansible.builtin.systemd_service:
        name: nginx
        state: restarted
```

Two tasks notify the same handler. If both change, nginx restarts **once**, at
the end. If neither changes, it does not restart at all.

```bash
ansible-playbook webserver.yml --check --diff
ansible-playbook webserver.yml
```

Run it twice. The second time: `changed=0`, and no restart. That is the
property from 10.4, preserved through a change that would otherwise break it.

## What you just automated

Compare this to lesson 6.7, where you wrote that config by hand and ran
`nginx -t` yourself before reloading.

The playbook does the same things, in the same order, for the same reasons.
What it adds is that it does them the same way every time, on every machine in
the group, and tells you when a machine had drifted.

The declarative instinct is the same one lesson 6.5 introduced with Docker
Compose: describe the desired state in a file, let something else work out how
to get there. Compose does it for containers on one host; Ansible does it for
anything, across many hosts. Same idea, wider scope.

## The traps

**Undefined variables.** A typo in a variable name fails at deploy time with
`'site_nme' is undefined`. Annoying, but it fails loudly rather than deploying
a config with a blank in it, which is the right trade.

**Templates without `validate`.** You can generate a syntactically invalid
config and restart the service into a broken state. `validate` runs the
service's own checker before the file is put in place. Use it whenever the
service offers one, exactly as you used `sshd -t` in 10.3.

**Handlers not running after a failure.** If a later task fails, handlers that
were notified earlier do not run by default. So a config file can be updated
while the service is still running the old one. `--force-handlers` overrides
this, but the better instinct is to notice that a failed run leaves the machine
in a state you have not described, and re-run once you have fixed it.

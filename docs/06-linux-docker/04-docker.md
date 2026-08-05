---
title: "6.4 Docker: what a container actually is"
sidebar_position: 4
---

# 6.4 Docker: what a container actually is

Before you install it, understand what you're installing, because
"container" is a word people use confidently and define badly.

## Not a small virtual machine

A virtual machine, like the ones you've been building, virtualises
*hardware*. Each one boots its own kernel and runs a complete operating
system, which is why DC01 needs 4 GB and forty minutes to install.

A container virtualises the *operating system*. Every container on this
machine shares UBNT01's single Linux kernel and gets its own isolated
view of the filesystem, processes, and network. There's no boot, no
second kernel, no forty minutes. A container starts in about the time it
takes to run a program, because that's essentially what it is: a program,
running in a box, with its dependencies packaged alongside it.

The trade is real and worth stating: containers are lighter, and the
isolation is thinner. Virtual machines separate more strongly, which is
why your domain controller is a VM and your web applications will be
containers.

Two more words you need:

**Image.** The packaged, read-only template: an application plus
everything it needs to run. You download images.

**Container.** A running instance of an image. You start, stop, and
delete containers. Deleting one throws away everything it wrote unless
you deliberately stored that somewhere, which is lesson 6.5's problem.

The reason this took over the industry: an image runs identically on your
laptop, on UBNT01, and on a cloud provider's machine, because it carries
its own dependencies. "Works on my machine" stops being an argument.

## Install it, without pasting a script you haven't read

Docker's install instructions famously tell you to pipe a script from
the internet straight into a shell. Lesson 1.6 gave you a rule about
that, so here's the same install with the rule intact:

```bash
# Fetch the script to a file rather than running it blind.
curl -fsSL https://get.docker.com -o get-docker.sh

# Look at what it intends to do. It's long; skim for what it adds
# and what it runs with sudo. Press q to quit the pager.
less get-docker.sh

# Now run it, having seen it.
sudo sh get-docker.sh
```

That's thirty seconds of reading, and it's the difference between
running software and obeying it. The habit matters more than this
particular script, which is fine.

Then let your own account use Docker:

```bash
# Add yourself to the docker group.
sudo usermod -aG docker $USER
```

Log out and back in for that to take effect (`exit`, then `ssh` again).
**Group membership is decided at login**, so a session that was already open
when you ran that command still has the old memberships, no matter how long
you wait.

**How you know both parts worked:**

```bash
# 1. Docker is installed. Expect a version number.
docker --version

# 2. Your account may talk to it without sudo. Expect an empty
#    table with column headings, because nothing is running yet.
docker ps
```

**If step 2 says `permission denied while trying to connect to the Docker
daemon socket`**, that is not a broken install. It is the log-out-and-back-in
above, not done. `groups` will confirm it: if `docker` is missing from that
output, close the session and reconnect.

:::warning[The docker group is root, wearing a different hat]
Anyone who can talk to the Docker daemon can start a container that
mounts the whole filesystem and edits anything on it. Adding yourself to
the `docker` group is therefore equivalent to giving yourself permanent
root, and it's fine on your own lab server. On a shared machine at work
it's a decision with consequences, and "why is this person in the docker
group" is a fair question at any security review.
:::

## Run something

```bash
# The traditional first container. Docker downloads the image,
# runs it, it prints a message, and it exits.
docker run hello-world
```

Now something you can visit:

```bash
# -d detaches, so it runs in the background.
# --name gives it a name instead of a random one.
# -p publishes a port: <host port>:<container port>.
docker run -d --name web -p 8080:80 nginx
```

From your own computer, browse to `http://10.10.10.20:8080`. That's a
web server, running in a container, that you did not install or
configure. It took a second to start.

Look around:

```bash
# What's running?
docker ps

# What's running or stopped?
docker ps -a

# What images have I downloaded?
docker images

# What is this container saying? Same idea as journalctl.
docker logs web

# Run a command inside the container. -it gives you an interactive
# terminal, and you land in a shell inside its isolated filesystem.
docker exec -it web bash
```

Inside that shell, run `ls /` and notice it looks like a Linux system
that isn't yours. Run `ps aux` and notice it can only see its own
processes. That's the isolation. Type `exit` to leave.

## Whose code did you just run?

Stop and look at what happened there. You typed one word, `nginx`, and a
machine you administer downloaded a complete Linux filesystem from the
internet and executed it. You didn't say where from. You didn't read
anything. It worked, and that is exactly what makes it worth a section.

Lesson 1.2 had you evaluate an Obsidian plugin before installing it, and
called that your first supply chain decision. This is the same decision
with more at stake, because of the warning further up this page: you're
in the `docker` group, so anything that can talk to the daemon is
effectively root on UBNT01.

**Where it came from.** With no registry named, Docker goes to Docker
Hub. The name you type tells you who published it:

| What you type | Who published it |
| --- | --- |
| `nginx` | A **Docker Official Image**. Bare names with no slash resolve to the `library` namespace, which Docker curates and builds itself. |
| `gitea/gitea` | The `gitea` organisation's own namespace. The project publishing its own software. |
| `someperson/nginx` | Anybody at all. An account created five minutes ago can publish this. |

That middle case is the common one and it's where judgement is needed.
`gitea/gitea` is trustworthy because the Gitea project controls the
`gitea` account, not because the word appears twice. Docker Hub marks
some of these as **Verified Publisher**, which means Docker confirmed the
account belongs to the organisation it claims to.

**The tag is not a version.** In lesson 6.6 you'll pull `gitea/gitea:1`,
and the `:1` is deliberate. A tag is just a label a publisher sticks on
an image, and they can move it whenever they like. `latest` is the worst
offender: it sounds like "the newest stable release" and it means nothing
of the sort. It's the tag Docker assumes when you don't specify one, and
plenty of projects don't keep it current at all.

Open the **Tags** tab on any image's Docker Hub page and the fiction
collapses. You'll find a long list of names: a full version number, the
same version with `-alpine` on the end, a bare major version, `stable`,
and others the publisher invented. If `latest` is in there at all, it
sits among them as one more label with no special powers.

Pinning to a major version, `:1` rather than `latest`, means you get
security fixes without waking up to a rewritten application because
upstream shipped version 2 overnight.

:::tip[Reading a Docker Hub page in thirty seconds]
Before running an image you haven't used before, open its page and check
four things:

1. **The namespace.** Official, a verified publisher, or a stranger?
2. **The pull count.** Compare it to what you'd expect for something this
   widely used. A popular project with a few hundred pulls means you're
   probably looking at somebody's copy, not the real thing.
3. **When it was last updated.** An image untouched for two years is
   carrying two years of unpatched libraries.
4. **Whether you can see how it was built.** Good publishers link the
   Dockerfile. If nobody will show you what went in, that is the answer.

Typosquatting is real, and it works the same way here as it does with
package managers: a name one character off a popular one, riding on
people not looking.
:::

None of this means being paranoid about `nginx`. It means knowing the
difference between an image you chose and an image you typed, and being
able to say which one you're running when somebody asks.

You'll meet the other half of this in Module 13, where a scanner reads
the packages inside an image and tells you what's in it that you didn't
know you'd installed. Right now the useful habit is smaller: look at the
page before you pull.

## Throw it away

```bash
docker stop web
docker rm web
docker ps -a        # gone
```

The container is deleted and UBNT01 is exactly as it was. Nothing was
installed, no configuration was left behind, and there's no uninstaller
to run. That disposability is the other half of why containers won, and
it's the same cattle-not-pets idea from lesson 3.5 applied one level
down.

Which raises the obvious question: if deleting a container throws away
everything it wrote, how does anything keep data? That's lesson 6.5.

:::tip[In cloud terms]
Containers are the unit cloud platforms are built around. The image you
just pulled would run unchanged on Azure Container Instances, App
Service, or a Kubernetes cluster; what changes is who starts it and how
it gets a network. Learning the `run`, `logs`, `exec` loop here means
the cloud consoles later are a different interface onto commands you
already understand. Kubernetes, when you meet it, is a scheduler for
exactly these things across many machines.
:::

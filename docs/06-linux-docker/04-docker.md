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

---
title: "4.7 Watch the traffic: your first packet capture"
sidebar_position: 7
---

# 4.7 Watch the traffic: your first packet capture

You've spent this module building a network and arguing about what can
reach what. Everything you've proved so far was proved indirectly: a ping
worked, a rule blocked something, a name resolved. Today you look at the
actual packets.

This matters more than it sounds. Networking stays abstract until the
first time you watch a connection being set up in front of you, and then
it stops being abstract permanently. I still open a capture when a
problem has survived two hours of theorising, because packets don't have
opinions. They show you what happened, not what should have happened.

The tool is **Wireshark**, and it is the single most useful diagnostic
program in infrastructure work. Network engineers use it, security
analysts live in it, and developers reach for it the day an API "just
stops working." You'll use it again in Module 7, Module 12, and Module 14.

:::warning[Capture only on networks you own]
Packet capture shows you other people's traffic as readily as your own.
On your lab, that's yours to look at. On a workplace, campus, or coffee
shop network it can be a sackable offence or a crime depending on where
you live, regardless of intent.

The rule for this course is the rule from lesson 0.1 and it doesn't bend:
your lab, your machines, your traffic. Module 14 formalises this with an
authorization gate before any offensive work.
:::

## Install it

```powershell
# Windows. Accept the Npcap installer that comes bundled with it;
# that's the driver that actually does the capturing.
winget install --id WiresharkFoundation.Wireshark -e
```

```bash
# Debian and Ubuntu
sudo apt install wireshark

# macOS, if you have Homebrew. Otherwise download from wireshark.org.
brew install --cask wireshark
```

KALI01 already has it. That's the one machine in your lab where you don't
need to install anything.

**Linux asks you a question during install** that people get wrong:
"Should non-superusers be able to capture packets?" Say **yes**. Then add
yourself to the group it creates and log out and back in:

```bash
sudo usermod -aG wireshark $USER
```

If you answered no, or you skip this, Wireshark opens with no interfaces
listed at all and no useful explanation why. That empty interface list is
the most common "Wireshark is broken" report in existence, and it isn't
broken. It just can't see the network card.

**How you know it worked.** Two checks, and the second is the one that
matters, because Wireshark installs perfectly well in a state where it
cannot capture anything:

1. **It is installed.** Launch Wireshark from your applications menu, or
   run `wireshark --version` in a terminal. Any version number is fine.
2. **It can see the network.** On the screen Wireshark opens to, you should
   see a **list of interfaces**, each with a small jagged line beside it
   that twitches when traffic moves. Names vary by platform: `eth0`,
   `ens33`, `Ethernet`, `Wi-Fi`, `en0`. What you need is at least one entry
   with a moving line, because that is the one carrying your traffic.

**An empty list, or a list with no moving lines, means stop here and fix
it.** On Linux that is the group question above: run `groups` and confirm
`wireshark` appears in the output. If it does not, you either answered no
to the installer's question (`sudo dpkg-reconfigure wireshark-common` asks
again) or you have not logged out and back in since running `usermod`.
Group membership is decided when you log in, so the change does nothing to
a session that was already open.

:::tip[Least privilege]
That question is the principle from lesson 5.6 showing up in an installer.
Capturing packets needs privileged access to the network card. The lazy
answer is to run the whole graphical application as root. The right answer
is the one the installer offers: a dedicated `wireshark` group that holds
exactly that one capability, and your normal user joins it.

Same shape as `sudo` on the server and two accounts in the domain. Take
the narrow permission, not the wide one.
:::

## Drive the tool before you need it

Open Wireshark. You get a list of network interfaces with little activity
graphs beside them. **Pick the one that's moving.** On a laptop that's
usually your Wi-Fi or Ethernet adapter; the rest are virtual adapters
belonging to your hypervisor.

Double-click it and the screen fills immediately. This is normal and it's
the first thing that overwhelms people. A quiet machine still produces
hundreds of packets a minute of background chatter you never asked for.

Four controls are all you need today:

- **The blue shark fin** starts a capture. **The red square** stops it.
  Stop it before you try to read anything; a scrolling list is unreadable.
- **The filter bar** at the top is where you cut the noise down. Type a
  filter, press Enter, and only matching packets show. This is the whole
  skill.
- **Three panes**, top to bottom: the packet list, the selected packet
  broken into layers, and the raw bytes. The middle pane is the one that
  matters.
- **Ctrl+Shift+X** clears a capture and starts fresh when you've made a
  mess.

Now look at that middle pane for any packet. It's a set of expandable
rows, and they are the layers from lesson 4.1, stacked in order:

```text
Frame 12: 74 bytes on wire
Ethernet II, Src: ..., Dst: ...          <- layer 2
Internet Protocol Version 4, Src: ...    <- layer 3
Transmission Control Protocol, Src Port  <- layer 4
Hypertext Transfer Protocol              <- layer 7
```

That's the OSI model, not as a diagram in a book, but as the actual
structure of an actual message on your actual network. Expand each row
and you can read the addresses and ports you configured by hand earlier
in this module. This is the moment the layers stop being trivia.

## Capture one: a DNS lookup

Start a capture, then type `dns` in the filter bar and press Enter. From a
terminal, look something up:

```bash
nslookup wireshark.org
```

You should see two packets appear: a **Standard query** and a **Standard
query response**. Click the query and read the middle pane.

Three things worth noticing, all of which lesson 4.1 predicted:

1. The protocol column says **UDP**, not TCP. A question and an answer,
   no connection set up, nothing acknowledged. Exactly as described.
2. The destination port is **53**, and the destination address is the DNS
   server from your four answers. If it isn't the server you expected,
   you've just found a real misconfiguration.
3. Expand the response and the addresses are sitting there in plain text.
   Anyone capturing this sees every name you look up.

That third point is worth sitting with. DNS was designed in an era that
assumed the network was friendly, and lookups are unencrypted by default
to this day. It is the reason DNS logging is such a rich source for the
detection work in Module 12.

## Capture two: the TCP three-way handshake

This is the one to actually watch, because it's the thing everyone
describes and few people have seen.

You'll serve a page from KALI01 and fetch it from your own machine, so
both ends belong to you. **On KALI01**, in a terminal:

```bash
# Make something to serve, then serve it. Python is from Module 2;
# http.server is built in, so there's nothing to install.
echo "hello from the lab" > index.html
python3 -m http.server 8000
```

Expect it to print `Serving HTTP on 0.0.0.0 port 8000` and then sit
there. Leave it running.

**On your own machine**, start a fresh capture and set this filter,
substituting KALI01's address:

```text
ip.addr == 10.10.10.50 && tcp.port == 8000
```

Then fetch the page:

```bash
curl http://10.10.10.50:8000/
```

```text
hello from the lab
```

Now stop the capture and read the first three packets. The **Info**
column tells the story:

```text
[SYN]          you -> KALI01    "can we talk?"
[SYN, ACK]     KALI01 -> you    "yes, and can we talk?"
[ACK]          you -> KALI01    "yes"
```

That is the three-way handshake, and it happens before a single byte of
your actual request is sent. It's what "connection-oriented" means in
lesson 4.1: TCP agrees that both ends are present and listening before
trusting anything to the wire. UDP skips all three, which is exactly why
your DNS lookup was two packets and this is not.

Every TCP connection you have ever made began this way. Web pages, SSH,
Git pushes, database queries, all of it.

### Read the conversation

Right-click any packet in this exchange and choose **Follow > TCP
Stream**. Wireshark reassembles every packet in both directions and shows
you the conversation as text:

```text
GET / HTTP/1.1
Host: 10.10.10.50:8000
User-Agent: curl/8.5.0
Accept: */*

HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.12.3
Content-type: text/html
Content-Length: 19

hello from the lab
```

Your request and the server's answer, in full, in plain text, reconstructed
by somebody who was merely present on the network.

Nothing here was hacked. That is simply what HTTP looks like to anyone who
can see the traffic. If that had been a login form, the password would be
sitting in that pane exactly as legibly as `hello from the lab` is.

This is the single best argument for the entire PKI module, and in lesson
7.6 you will run this exact capture again against your own HTTPS site and
find nothing readable in it at all. Same tool, same filter, same
conversation, and this time it's gibberish. Keep this capture in your
journal so you can put the two side by side.

Stop the server on KALI01 with **Ctrl+C** when you're done.

## When it doesn't work

- **No interfaces listed.** The permissions question above. On Linux,
  fix the group and log out and back in. On Windows, reinstall and let
  Npcap install too.
- **The filter bar turns red.** Your filter has a syntax error and
  Wireshark will not run it. Green means valid. Note that `ip.addr` uses
  `==`, not `=`.
- **You captured nothing at all.** You almost certainly picked the wrong
  interface. If your traffic goes to a VM, capture on the adapter that
  faces the lab network, not your Wi-Fi.
- **You see the request but no response.** That's a real finding, not a
  tool problem. Something in between dropped it, and if you're Tier 2 the
  firewall from lesson 4.5 is the first suspect.

## Make it yours

1. Capture a `ping` between two lab machines, filter on `icmp`, and find
   the reply that matches each request. Notice there's no handshake and no
   ports, because ICMP lives at layer 3 and never reaches layer 4.
2. Filter on `arp` and watch machines ask "who has this address?" on the
   local wire. That's layer 2 doing the job that lets layer 3 work at all.
3. Tier 2: run a capture while you re-test one of the blocked paths from
   lesson 4.6. A request that leaves and is never answered looks very
   different from one that is refused, and telling those apart on sight is
   a genuinely useful diagnostic skill.

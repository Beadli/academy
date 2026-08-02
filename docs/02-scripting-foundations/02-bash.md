---
title: "2.2 Bash: find the attacker in auth.log"
sidebar_position: 2
---

# 2.2 Bash: find the attacker in auth.log

Bash is the shell on effectively every Linux server on earth, which
means it's the language of your Ubuntu box, your Kali box, and every
mid-incident moment of your future career. Its superpower is the pipe:
small tools chained together, each one transforming the text and passing
it along, like an assembly line where every station does one job.

Today's task is the classic first job of a security analyst: a server's
`auth.log` is full of failed logins, and you want to know who's knocking.
During a tuning project where my SIEM was producing six figures of alerts
a day, the triage that found the worst offenders was exactly the pipeline
you're about to build. This one-liner family has never stopped earning
its keep.

**Windows users, you're in this lesson.** When you installed Git in
lesson 1.3 you quietly got Git Bash with it (find it in the Start menu).
It's a real bash shell, and everything below works in it.

## Set the scene

You need a log to dig through. Real `auth.log` files come from SSH
servers you don't have yet, so plant this sample. Paste the whole block
into your terminal; it writes a file called `auth.log` in your current
directory. (The `cat > file << 'EOF'` trick is called a here-document,
and it means "everything until the line EOF goes into the file.")

```bash
cd ~/git/lab-journal/Resources/scripts

cat > auth.log << 'EOF'
Aug  1 03:11:01 web01 sshd[812]: Failed password for root from 203.0.113.42 port 52144 ssh2
Aug  1 03:11:04 web01 sshd[812]: Failed password for root from 203.0.113.42 port 52144 ssh2
Aug  1 03:11:07 web01 sshd[812]: Failed password for admin from 203.0.113.42 port 52190 ssh2
Aug  1 03:12:13 web01 sshd[820]: Failed password for invalid user oracle from 198.51.100.7 port 40022 ssh2
Aug  1 03:12:19 web01 sshd[820]: Failed password for invalid user postgres from 198.51.100.7 port 40025 ssh2
Aug  1 06:30:44 web01 sshd[955]: Accepted password for steve from 192.0.2.10 port 51820 ssh2
Aug  1 07:02:11 web01 sshd[990]: Failed password for root from 203.0.113.42 port 53001 ssh2
Aug  1 07:02:15 web01 sshd[990]: Failed password for root from 203.0.113.42 port 53003 ssh2
Aug  1 07:15:33 web01 sshd[1003]: Accepted publickey for steve from 192.0.2.10 port 51944 ssh2
Aug  1 08:41:09 web01 sshd[1100]: Failed password for invalid user test from 198.51.100.7 port 41888 ssh2
EOF
```

(Those addresses are from ranges reserved for documentation, so nobody's
real server is being accused of anything.)

## The pipeline, one station at a time

Build it up a piece at a time and run each stage. Watching the text
transform is the lesson.

```bash
# Stage 1: keep only the lines about failed passwords.
# grep prints lines matching a pattern and drops the rest.
grep "Failed password" auth.log

# Stage 2: keep only the attacker's IP from each line.
# awk splits each line into fields. $NF means "the last field",
# so $(NF-3) is "three fields before the last one", where the IP
# sits in this log format.
grep "Failed password" auth.log | awk '{print $(NF-3)}'

# Stage 3: count them.
# sort groups identical lines together; uniq -c collapses each
# group and prefixes it with a count; sort -rn puts the biggest
# count first. This trio is the most useful ten characters in
# log analysis.
grep "Failed password" auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn
```

That final output is a ranked list of who's attacking you. Five tries
from `203.0.113.42` and three from `198.51.100.7`, discovered in one
line, from a log you could never have read by eye at real size. Real
auth logs run to millions of lines, and this pipeline doesn't care.

## Now make it a script

One-liners evaporate; scripts accumulate. In VS Code, which you set up in
lesson 2.1, right-click `Resources/scripts` in the file tree, choose
**New File**, and name it `failed-logins.sh`, extension included. Paste
this in and save it next to the log you planted a moment ago:

```bash
#!/usr/bin/env bash
# failed-logins.sh: rank source IPs by failed SSH login attempts.
# Usage: ./failed-logins.sh <logfile>

# The first line above is the "shebang": it tells the system which
# program runs this file.

# $1 is the first argument given on the command line. We store it
# in a named variable so the script reads like a sentence.
logfile="$1"

# A safety check. [ -z ... ] tests for an empty value; if nobody
# gave us a file, explain and stop rather than fail confusingly.
if [ -z "$logfile" ]; then
  echo "Usage: $0 <logfile>"
  exit 1
fi

echo "Failed login attempts by source IP for: $logfile"
echo

grep "Failed password" "$logfile" | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn
```

### Windows users: the invisible character that breaks this

Before you run it, look at the bottom-right of the VS Code window, at the
`LF` or `CRLF` indicator from lesson 2.1. If it says **CRLF**, click it
and choose **LF**, then save again.

That indicator is worth understanding, because this is a genuinely
confusing failure and you'll meet it for years. Windows ends each line of a text file with two
invisible characters, carriage return plus line feed, written `\r\n`.
Linux and macOS use just the line feed, `\n`. Windows editors default to
the Windows convention, quite reasonably.

Bash does not forgive it. The first line of your script says the file
should be run by `bash`, but with Windows line endings it actually says
run this with a program called `bash\r`, and no such program exists. The
error is spectacularly unhelpful:

```text
/usr/bin/env: ‘bash\r’: No such file or directory
```

The exact wording varies between Git Bash and Linux; the meaning doesn't.
Any error naming a command you did type, with something odd stuck to the
end of it, is this. It is not your pipeline, your quoting, or your typing.

If it already happened, fix the file in place from the terminal:

```bash
# Delete a carriage return at the end of every line. The $ means
# "at end of line", so it only removes the ones causing trouble.
sed -i 's/\r$//' failed-logins.sh

# Confirm. A healthy script says "Bourne-Again shell script"; a sick
# one adds "with CRLF line terminators".
file failed-logins.sh
```

Linux and macOS students: nothing above applies to you today. Read it
anyway. The day you're handed a script that somebody wrote on Windows,
you'll recognise it in five seconds instead of an hour.

## Make it executable and run it

`chmod` changes a file's permissions, and `+x` adds "may be executed":

```bash
chmod +x failed-logins.sh
./failed-logins.sh auth.log
```

A file you can execute is not the same as a file you can read, which is
why this step exists at all. Bash refuses to run a script that nobody
gave permission to run, and `Permission denied` here means you skipped
the `chmod`.

Run it with no argument as well, to watch the safety check you wrote do
its job:

```bash
./failed-logins.sh
```

```text
Usage: ./failed-logins.sh <logfile>
```

You just wrote a program with an argument, a variable, a conditional,
and a pipeline in it. That's most of daily bash, and you met each piece
inside a job worth doing.

## Make it yours

1. Change the script to report **accepted** logins instead. One word.
   Notice what it tells you: which IPs successfully got in, which is the
   list you check *after* seeing a brute-force attempt.
2. Harder: make it report the *usernames* being guessed instead of
   the IPs. Try `awk '{print $9}'` first, counting fields from the
   front, and watch it work on the root lines but fall apart on the
   "invalid user" lines, which shove the name two fields to the
   right. Then count from the end instead: `$(NF-5)`. Working out why
   the second one lands on the name in both kinds of line is the
   exercise, and it's the same trick the IP stage was quietly using
   all along.

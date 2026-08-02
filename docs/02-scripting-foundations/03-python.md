---
title: "2.3 Python: query the KEV catalog"
sidebar_position: 3
---

# 2.3 Python: query the KEV catalog

PowerShell owns Windows, Bash owns Linux, and Python owns everything in
between: talking to APIs, chewing on JSON, and gluing tools together.
When a task involves "fetch data from a service and make sense of it,"
Python is usually the shortest path, and that's exactly today's job.

The data source is worth knowing on its own. CISA (the US cybersecurity
agency) publishes the **Known Exploited Vulnerabilities catalog**: not
every CVE ever filed, just the ones attackers are *confirmed to be using
right now*. When vulnerability counts get overwhelming (and in Module 13
you'll see scanners hand you hundreds per host), KEV is the shortlist
that tells you what to fix first. A bigger cousin of today's script runs
in my lab every morning and compares this exact feed against my own
machines; the day it matches something, I want to know before breakfast.

## Install Python

```powershell
# Windows. Python's winget package id has the version baked into it
# (Python.Python.3.12, 3.13, ...), and any specific number printed in
# a course goes stale. So ask winget what's current, then install the
# newest 3.x it lists:
winget search Python.Python.3

winget install --id Python.Python.3.13 -e   # use the newest id FROM YOUR SEARCH, not this line
```

(If you'd rather click than search, the installer at
[python.org/downloads](https://www.python.org/downloads/) always offers
the current version. Tick "Add python.exe to PATH" during install.)

```bash
# Debian/Ubuntu (usually already present; this makes sure)
sudo apt install python3

# macOS ships python3; check with: python3 --version
```

Reopen your terminal and confirm `python3 --version` (plain `python` on
Windows) prints a version.

## The script

Same routine as the last two lessons: **New File** in
`Resources/scripts`, named `kev-check.py` with the extension, paste, save.
Everything it uses comes with Python; nothing extra to install. The line
endings that mattered in lesson 2.2 don't bite here, because you hand
this file to `python3` yourself rather than asking the system to find an
interpreter from the first line.

```python
#!/usr/bin/env python3
# kev-check.py: fetch CISA's Known Exploited Vulnerabilities catalog
# and show how big it is and what's newest.

# "import" pulls in a library. These two ship with Python: one for
# fetching URLs, one for reading JSON.
import urllib.request
import json

URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# "with" opens something and guarantees it gets closed afterward,
# even if things go wrong. The response object behaves like a file.
with urllib.request.urlopen(URL) as response:
    catalog = json.load(response)

# The JSON is now a nested Python structure. catalog["vulnerabilities"]
# is a list, and each entry is a dictionary of named fields.
vulns = catalog["vulnerabilities"]

# An f-string: put an f before the quotes and anything in {braces}
# gets evaluated and dropped into the text.
print(f"KEV catalog: {len(vulns)} vulnerabilities known to be exploited")
print()

# "def" defines a function: a named, reusable piece of logic. This
# one takes a catalog entry and returns its dateAdded field. We hand
# it to sorted() so Python knows WHAT to sort the entries by.
def added_date(vuln):
    return vuln["dateAdded"]

newest = sorted(vulns, key=added_date, reverse=True)[:5]

# A for loop: run the indented block once per item in the list.
print("Five most recently added:")
for v in newest:
    print(f'  {v["dateAdded"]}  {v["cveID"]:<16} {v["vendorProject"]} {v["product"]}')
```

Run it:

```bash
python3 kev-check.py     # "python kev-check.py" on Windows
```

Give it a second; the catalog is a real file on a real government
server, and you just made your first API call. Look at what came back:
the newest entries are usually days old, sometimes hours. That list is
this week's actual attacker shopping list, live in your terminal.

## What you just used

One pass back through the comments: an import, a `with` block, a
dictionary, a list, a function, a sort with a custom key, a slice
(`[:5]`), and a for loop. That's a substantial chunk of working Python,
and every piece earned its place in forty lines. When these show up
again in later modules, they'll be familiar instead of new.

## Make it yours

1. Change the `[:5]` to show ten. Trivial on purpose; feel how slices
   work.
2. Print each entry's `shortDescription` on a second, indented line.
   You'll need another `print` inside the loop.
3. Harder: count how many entries were added this year. You'll want an
   `if` statement inside a loop, checking whether `dateAdded` starts
   with `"2026"` (strings have a `.startswith()` method). If you get
   stuck, you know the drill: ask Claude to explain, not to write it,
   then journal what you learned.

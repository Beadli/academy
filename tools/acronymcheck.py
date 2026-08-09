#!/usr/bin/env python3
"""Verify every acronym is tied to its expansion at first use.

  python3 acronymcheck.py [docs_dir]

Reports two failures:
  UNTIED  an acronym whose expansion appears nowhere beside the letters
  LATE    an acronym tied to its expansion in a later lesson than its first use

The rule this enforces is not "the expansion exists somewhere". It is the tie:
the letters and the words in one sentence, at first use. KEV shipped with
"Known Exploited Vulnerabilities catalog" seven lines above "KEV is the
shortlist", and a grep for the expansion called that taught. It wasn't: the
reader still has to guess that the two name the same thing.
"""
import re, sys, pathlib

docs = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'docs')

# An acronym has to be used enough to matter. A single passing mention is a
# judgement call for a human, not a build failure.
MIN_USES = 3

# Universal computing vocabulary. A course at this level can open with these
# the way it opens with "file" or "network", so they are not teachable terms.
ASSUMED = {
    'IP', 'PC', 'OS', 'IT', 'CPU', 'RAM', 'GB', 'MB', 'TB', 'KB', 'USB', 'PDF',
    'URL', 'URI', 'HTTP', 'HTTPS', 'SSH', 'DNS', 'DHCP', 'VPN', 'LAN', 'WAN',
    'NAT', 'GUI', 'CLI', 'API', 'JSON', 'YAML', 'XML', 'CSV', 'HTML', 'CSS',
    'SQL', 'TLS', 'SSL', 'ISO', 'TV', 'AM', 'PM', 'US', 'UK', 'USA', 'AI', 'ID',
    'MAC', 'TCP', 'UDP', 'ICMP', 'NTP', 'RDP', 'SMB', 'CD', 'DVD', 'BIOS',
    'UEFI', 'SSD', 'HDD', 'NIC', 'VLAN', 'MTU', 'ARP', 'FTP', 'SMTP', 'IMAP',
    'LTS', 'EOL', 'FAQ', 'AMD', 'CV', 'OK', 'SRV', 'README',
}

# Shouted words and literal command output, which look like acronyms and are
# not. CRITICAL comes out of a Trivy scan, SELECT out of a SQL lesson.
NOT_ACRONYM = {
    'CRITICAL', 'SELECT', 'HIGH', 'LOW', 'MEDIUM', 'NONE', 'TRUE', 'FALSE',
    'NULL', 'YES', 'NO', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'FAIL', 'PASS',
    'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'RUN', 'CMD', 'ENV', 'ADD', 'COPY',
    'FROM', 'USER', 'ALL', 'AND', 'OR', 'NOT', 'IF', 'THEN', 'ELSE', 'END',
    'LAB', 'BEADLI', 'NEW', 'OLD', 'ANY', 'FOR', 'FIRST', 'FULL', 'FREE',
    # Not acronyms: an environment variable, a product name, and the literal
    # label OPNsense gives a tunnel interface.
    'PATH', 'VS', 'TLSCL',
}

# Cleared by hand, with the reason, because this check cannot see them and a
# tool that reports twenty things a human has already judged gets ignored.
# Anything added here is a decision, so it prints in the summary rather than
# disappearing. Delete an entry and the check will argue with you again.
ACCEPTED = {
    'NTLM':  'NT LAN Manager: NT is itself an abbreviation, so the initials do not line up',
    'OIDC':  'OpenID Connect: two words, four letters',
    'SYSVOL': 'system volume: two words, six letters',
    'SID':   'security identifier: the D comes from inside a word',
    'SPAN':  'Switched Port Analyzer: the N comes from inside a word',
    'SAML':  'expanded under its own section heading in 8.2, one line from the letters',
    'CISA':  'glossed as "the US cybersecurity agency", which is what a beginner needs',
    'VM':    'module 0 is orientation, not instruction; tied in 3.3 where it is taught',
    'DC':    'module 0 orientation; tied in 4.5',
    'CA':    'module 0 orientation; tied in 7.1',
    'GPO':   'module 0 orientation; tied in 5.7',
    'CVE':   'passing mention in 2.3; tied in 13.1 where vulnerabilities are the subject',
    'SIEM':  'module index overview; tied in 0.1',
    'UPN':   'module index overview; tied in 9.2',
    'SSP':   'module index overview; tied in 16.1',
    'POA&M': 'module index overview; tied in 16.1',
    'ACME':  'module index overview; tied in 7.4',
}

# Words allowed to sit between initials in an expansion, because nobody counts
# them: "Plan of Action and Milestones" is still POA&M. Commas count as
# separators too, or "governance, risk, and compliance" fails to read as GRC.
FILLER = r'(?:of|and|the|for|to|in|a|an)[,\s-]+'


def reading_order():
    """Every lesson page, in the order a student meets it."""
    out = []
    for mod in sorted(p for p in docs.iterdir() if p.is_dir()):
        if not (m := re.match(r'(\d+)-', mod.name)):
            continue
        for f in sorted(mod.glob('*.md')):
            text = f.read_text(errors='ignore')
            pos = re.search(r'^sidebar_position:\s*(\d+)', text, re.M)
            pos = int(pos.group(1)) if pos else (0 if f.name == 'index.md' else 99)
            out.append(((int(m.group(1)), pos), f, text))
    out.sort(key=lambda t: t[0])
    return out


def sentences(text, drop_lesson_list=False):
    """Prose sentences only: no frontmatter, code, tables, JSX or admonition
    markers. Periods inside `inline code` are masked so they can't split a
    sentence."""
    lines, fence, fm = [], False, False
    for i, ln in enumerate(text.split('\n')):
        s = ln.strip()
        if i == 0 and s == '---':
            fm = True
            continue
        if fm:
            fm = s != '---'
            continue
        if s.startswith('```'):
            fence = not fence
            continue
        if fence or s.startswith((':::', '<', '|', 'import ')):
            continue
        # A module index lists its own lesson titles. That is a table of
        # contents, not the place a term gets taught, so a term appearing
        # there first is not a defect.
        if drop_lesson_list and re.match(r'^-\s+\*\*\d+\.\d+\*\*', s):
            continue
        lines.append(s)

    for para in re.split(r'\n\s*\n', '\n'.join(lines)):
        para = ' '.join(para.split())
        if not para:
            continue
        masked = re.sub(r'`[^`]*`', lambda m: 'x' * len(m.group(0)), para)
        last = 0
        for m in re.finditer(r'[.!?]["\')]?\s+(?=[A-Z(*`"])', masked):
            yield para[last:m.end()].strip()
            last = m.end()
        if last < len(para):
            yield para[last:].strip()


TOKEN = re.compile(r'\b([A-Z][A-Z0-9&]{1,5})(s?)\b')


def acronyms(sent):
    """All-caps tokens that are plausibly teachable acronyms."""
    plain = re.sub(r'`[^`]*`', ' ', sent)
    for m in TOKEN.finditer(plain):
        a = m.group(1)
        if a in ASSUMED or a in NOT_ACRONYM:
            continue
        # DC01, SUBCA01, FW01: hostnames the course names, not acronyms.
        if re.fullmatch(r'[A-Z]+\d+', a):
            continue
        # SC-7, AU-6, CP-9: NIST control family identifiers, not acronyms.
        if plain[m.end():m.end() + 2].startswith('-') and plain[m.end() + 1:m.end() + 2].isdigit():
            continue
        yield a


def tie_finder(a):
    """Matches a phrase whose initials spell the acronym, filler words allowed.

    The filler group is optional, and has to be wrapped to stay that way: a
    bare `?` after FILLER binds to the `[\\s-]+` inside it and makes the filler
    word mandatory instead, which silently reports every correctly tied
    acronym as untied."""
    letters = [c for c in a if c.isalpha()]
    if len(letters) < 2:
        return None
    step = r'\w*[,\s-]+(?:' + FILLER + r')?'
    return re.compile(r'\b' + step.join(re.escape(c) for c in letters) + r'\w*', re.I)


def main():
    pages = reading_order()

    corpus = []          # (sort key, file, sentence) in reading order
    first_use = {}
    counts = {}
    for key, f, text in pages:
        for sent in sentences(text, drop_lesson_list=(f.name == 'index.md')):
            corpus.append((key, f, sent))
            for a in acronyms(sent):
                counts[a] = counts.get(a, 0) + 1
                first_use.setdefault(a, (key, f, sent))

    untied, late, cleared = [], [], []
    for a, n in counts.items():
        if n < MIN_USES:
            continue
        if a in ACCEPTED:
            cleared.append((a, n))
            continue
        rx = tie_finder(a)
        if rx is None:
            continue
        ra = re.compile(r'\b' + re.escape(a) + r's?\b')
        tie = None
        for key, f, sent in corpus:
            if not (ma := ra.search(sent)):
                continue
            for me in rx.finditer(sent):
                phrase = me.group(0)
                # An expansion that contains the acronym is the acronym plus
                # whatever words happen to follow it. Two-letter acronyms are
                # where this bites: "the CA and a certificate" reads as a
                # perfect C-A initials match and means nothing.
                if ra.search(phrase):
                    continue
                if abs(me.start() - ma.start()) < 120:
                    tie = (key, f, sent, phrase)
                    break
            if tie:
                break
        fk, ff, fs = first_use[a]
        if tie is None:
            untied.append((a, n, ff, fs))
        elif tie[0] > fk:
            late.append((a, n, ff, fs, tie))

    def lid(f):
        return f"{f.parent.name.split('-')[0]}/{f.name}"

    for a, n, ff, fs in sorted(untied, key=lambda r: -r[1]):
        print(f"UNTIED  {a:8} {n:3} uses  first: {lid(ff)}")
        print(f"                          {fs[:120]}")
    for a, n, ff, fs, tie in sorted(late, key=lambda r: -r[1]):
        print(f"LATE    {a:8} {n:3} uses  first: {lid(ff)}  tied: {lid(tie[1])} ({tie[3]})")
        print(f"                          {fs[:120]}")

    for a, n in sorted(cleared, key=lambda r: -r[1]):
        print(f"cleared {a:8} {n:3} uses  {ACCEPTED[a]}")

    fails = len(untied) + len(late)
    print(f"\n{len(counts)} acronyms seen, {sum(1 for c in counts.values() if c >= MIN_USES)} "
          f"used {MIN_USES}+ times, {len(cleared)} cleared by hand. {fails} failure(s).")
    return 1 if fails else 0


sys.exit(main())

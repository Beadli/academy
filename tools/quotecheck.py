#!/usr/bin/env python3
"""Verify every cross-lesson reference and every quote attributed to one.

  python3 quotecheck.py [docs_dir]

Reports two failures:
  UNRESOLVED  a "lesson X.Y" / "Module N" reference with no such file
  MISQUOTE    quoted text attributed to a lesson that does not contain it
"""
import re, sys, pathlib

docs = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'docs')

def norm(s):
    """Compare meaning, not markup. A source sentence carries **bold** the
    quoting lesson drops, and a nested quote correctly flips " to ', so
    neither difference is a misquote."""
    s = re.sub(r'[*_`]', '', s)
    s = re.sub(r'["\'’‘“”]', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

# lesson number -> file, module number -> folder, from frontmatter titles
lesson, module = {}, {}
for f in docs.rglob('*.md'):
    m = re.search(r'^title:\s*"?(.+?)"?\s*$', f.read_text(errors='ignore'), re.M)
    if not m:
        continue
    if n := re.match(r'(\d+)\.(\d+)\s', m.group(1)):
        lesson[f"{int(n.group(1))}.{int(n.group(2))}"] = f
    if n := re.match(r'Module (\d+):', m.group(1)):
        module[int(n.group(1))] = f.parent

def body(key):
    """Full text a reference points at: one lesson, or a whole module folder."""
    if key in lesson:
        return norm(lesson[key].read_text(errors='ignore'))
    if key.isdigit() and int(key) in module:
        return norm(' '.join(p.read_text(errors='ignore')
                             for p in module[int(key)].glob('*.md')))
    return None

REF = re.compile(r'\blessons?\s+(\d+\.\d+)|\bModule\s+(\d+)\b', re.I)
QUOTE = re.compile(r'"([^"]{3,200})"')
# Only quotes ATTRIBUTED to a reference are checked. Without a reporting verb
# between the two, a nearby lesson number is context, not a source, and every
# hypothetical utterance in the course ("root did it.") becomes a false alarm.
VERB = re.compile(r'\b(said|says|called|calls|left|introduced|noted|described'
                  r'|promised|warned|told|put it|quoted|ended (?:on|with))\b', re.I)
fails = 0

for f in sorted(docs.rglob('*.md')):
    text = re.sub(r'```.*?```', '', f.read_text(errors='ignore'), flags=re.S)
    # paragraphs, so a sentence wrapped across lines is searchable as one string
    for para in re.split(r'\n\s*\n', text):
        para = ' '.join(l.strip().lstrip('>').strip() for l in para.splitlines())
        refs = [(m.start(), m.group(1) or m.group(2)) for m in REF.finditer(para)]
        for pos, key in refs:
            if body(key) is None:
                print(f"UNRESOLVED {f.relative_to(docs)}: {para[pos:pos+40]!r}")
                fails += 1
        for q in QUOTE.finditer(para):
            prior = [(p, k) for p, k in refs if p < q.start()]
            if not prior:
                continue                      # not attributed to a lesson
            pos, key = prior[-1]              # nearest preceding reference
            gap = para[pos:q.start()]
            if len(gap) > 130 or not VERB.search(gap):
                continue                      # context, not an attribution
            prior = [key]
            src = body(key)
            if src is None:
                continue                      # already reported as UNRESOLVED
            if norm(q.group(1)) in src:
                continue
            # the file may be quoting itself; that is not a cross-reference
            if norm(q.group(1)) in norm(text):
                own = re.match(r'^(\d+)-', f.parent.name)
                if own and prior[-1].startswith(own.group(1)):
                    continue
            print(f"MISQUOTE   {f.relative_to(docs)} -> {prior[-1]}: \"{q.group(1)[:70]}\"")
            fails += 1

print(f"\n{len(lesson)} lessons, {len(module)} modules indexed. {fails} failure(s).")
sys.exit(1 if fails else 0)

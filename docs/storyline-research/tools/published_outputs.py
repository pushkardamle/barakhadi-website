"""Read title/activity id of every published Storyline output (tincan.xml / imsmanifest.xml / meta.xml), loose or in zips. READ-ONLY."""
import csv, re, zipfile, pathlib, json, os, collections
HERE = pathlib.Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(HERE / '_work/files.csv', encoding='utf-8')))
out = []
def grab(txt):
    t = re.search(r'<name[^>]*>([^<]+)</name>', txt) or re.search(r'<title>([^<]+)</title>', txt) or re.search(r'title="([^"]+)"', txt)
    a = re.search(r'<activity id="([^"]+)"', txt) or re.search(r'identifier="([^"]+)"', txt)
    return (t.group(1).strip() if t else ''), (a.group(1) if a else '')
for r in rows:
    fn = os.path.basename(r['path']).lower()
    if fn in ('tincan.xml', 'imsmanifest.xml'):
        txt = open(r['path'], encoding='utf-8', errors='replace').read()
        t, a = grab(txt)
        out.append({'where': 'loose', 'container': os.path.dirname(r['path']), 'kind': fn, 'title': t, 'activity': a, 'mtime': r['mtime']})
zm = list(csv.DictReader(open(HERE / '_work/zip_members.csv', encoding='utf-8')))
for z in sorted({m['zip'] for m in zm if m['member'].lower().split('/')[-1] in ('tincan.xml', 'imsmanifest.xml')}):
    try:
        with zipfile.ZipFile(z) as zf:
            for n in zf.namelist():
                if n.lower().split('/')[-1] in ('tincan.xml', 'imsmanifest.xml') and n.count('/') <= 1:
                    t, a = grab(zf.read(n).decode('utf-8', 'replace'))
                    out.append({'where': 'zip', 'container': z + ' :: ' + n, 'kind': n.split('/')[-1].lower(), 'title': t, 'activity': a,
                                'mtime': next(r['mtime'] for r in rows if r['path'] == z)})
    except Exception as e:
        out.append({'where': 'zip', 'container': z, 'kind': 'ERR', 'title': str(e), 'activity': '', 'mtime': ''})
with open(HERE / '_work/published.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), collections.Counter(o['kind'] for o in out), 'distinct titles', len({o['title'] for o in out}))

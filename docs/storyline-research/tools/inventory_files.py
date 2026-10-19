"""Step 1a: READ-ONLY inventory of the Newgen source folder (and other local published outputs).

Opens every file with mode 'rb' only. Never writes, renames or touches anything under the source roots.
Outputs (under docs/storyline-research/): _work/files.csv, _work/zip_members.csv
"""
import os, sys, csv, hashlib, zipfile, pathlib, time
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).resolve().parents[1]
ROOTS = {'newgen': r'B:\My Documents\Marathi Shala\Source Files from Newgen',
         'local': r'B:\My Documents\Marathi Shala'}           # 'local' skips the Newgen subfolder
OUT = HERE / '_work'
for r in ROOTS.values():
    assert not str(OUT).lower().startswith(r.lower()), 'output must not be inside a source root'

def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def walk():
    newgen = os.path.normcase(ROOTS['newgen'])
    for label, root in ROOTS.items():
        for d, dirs, files in os.walk(root):
            if label == 'local' and os.path.normcase(d).startswith(newgen):
                dirs[:] = []; continue
            for f in files:
                yield label, os.path.join(d, f)

def row(item):
    label, p = item
    st = os.stat(p)
    try: h = sha1(p)
    except OSError as e: h = f'ERR {e}'
    return [label, p, os.path.splitext(p)[1].lower(), st.st_size, time.strftime('%Y-%m-%d %H:%M', time.localtime(st.st_mtime)), h]

t0 = time.time()
items = list(walk())
print('files', len(items), flush=True)
rows = []
with ThreadPoolExecutor(4) as ex:
    for i, r in enumerate(ex.map(row, items)):
        rows.append(r)
        if i % 500 == 0: print(i, f'{time.time()-t0:.0f}s', flush=True)
with open(OUT / 'files.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['root', 'path', 'ext', 'bytes', 'mtime', 'sha1']); w.writerows(rows)

# zip members (listing only, nothing extracted)
zrows = []
for label, p, ext, *_ in rows:
    if ext != '.zip': continue
    try:
        with zipfile.ZipFile(p) as z:
            for m in z.infolist():
                zrows.append([label, p, m.filename, m.file_size, f'{m.CRC:08x}'])
    except Exception as e:
        zrows.append([label, p, f'ERR {e}', 0, ''])
with open(OUT / 'zip_members.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['root', 'zip', 'member', 'bytes', 'crc']); w.writerows(zrows)
print('done', len(rows), 'files', len(zrows), 'zip members', f'{time.time()-t0:.0f}s')

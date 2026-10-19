"""Step 2: catalogue every .story project, READ-ONLY.

Each .story is opened as a zip and its XML is read in memory; nothing is extracted next to the source.
Writes: _work/projects/<pid>.json (full detail) and catalogue/projects.csv (one row per .story file).
"""
import io, os, re, sys, csv, html, json, zipfile, hashlib, pathlib, collections
import xml.etree.ElementTree as ET
from multiprocessing import Pool

SRC = r'B:\My Documents\Marathi Shala'          # whole tree, read-only (includes 'Source Files from Newgen')
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE / '_work' / 'projects'
DEVA = re.compile(r'[\u0900-\u097F]')
CODE = re.compile(r'\bL\d[- ]?\d{2,3}(?:[- ]\d{3})?f?\b', re.I)
INTERACTIONS = ['dragDrop', 'multiChoiceIntr', 'freePickOneIntr', 'freePickManyIntr', 'intrFreeChoice', 'textEntry',
                'dialData', 'rsltsIntr', 'clkAreaRect', 'clkAreaOval', 'clkAreaFree', 'web', 'markers', 'dragDropIntr']
OBJS = ['pic', 'textBox', 'btn', 'movie', 'sound', 'rect', 'roundRect', 'oval', 'group', 'star', 'checkMark', 'freeForm', 'line']
PATHS = ['linePath', 'customPath', 'arcPath']
STOCK = ('shutterstock', 'freepik', 'vecteezy', 'istock', 'dreamstime', 'clipart', 'pixabay', 'depositphotos', '123rf', 'fotolia', 'bigstock')


def local(t):
    return t.split('}')[-1]


def text_spans(raw):
    """Storyline stores rich text as an escaped XML 'Document' inside <text>; pull Block text + fonts."""
    try:
        doc = ET.fromstring(raw)
    except ET.ParseError:
        return [], []
    texts, fonts = [], []
    for blk in doc.iter('Block'):
        t = ''.join(s.get('Text', '') for s in blk.iter('Span'))
        if t.strip():
            texts.append(t.strip())
    for s in doc.iter('Span'):
        st = s.find('Style')
        if st is not None and st.get('FontFamily'):
            fonts.append(st.get('FontFamily'))
    return texts, fonts


def classify_origin(p):
    if not p:
        return 'unknown'
    q = p.lower()
    if q == 'recorded':
        return 'recorded-in-storyline'
    for s in STOCK:
        if s in q:
            return 'stock:' + s
    if 'stock photo' in q or '\\stock' in q:
        return 'stock-folder'
    if '\\temp\\articulate' in q or '\\appdata\\local\\temp' in q:
        return 'storyline-temp'
    m = re.match(r'[a-z]:\\users\\([^\\]+)', q)
    if m:
        return 'user:' + m.group(1)
    return 'path:' + '\\'.join(p.split('\\')[:2])


def agg(slides, key):
    c = collections.Counter()
    for s in slides:
        c.update(s[key])
    return dict(c)


def parse(path):
    member = None
    if isinstance(path, (tuple, list)):          # a .story stored inside a zip: read it into memory only
        path, member = path
    rel = os.path.relpath(path, SRC) + (f' :: {member}' if member else '')
    pid = hashlib.md5(rel.lower().encode()).hexdigest()[:10]
    rec = {'pid': pid, 'rel': rel, 'name': os.path.splitext(os.path.basename(member or path))[0]}
    media_list = []
    try:
        if member:
            with zipfile.ZipFile(path) as outer:
                data = outer.read(member)
            rec['bytes'] = len(data)
            z = zipfile.ZipFile(io.BytesIO(data))
        else:
            rec['bytes'] = os.path.getsize(path)
            z = zipfile.ZipFile(path)
    except Exception as e:
        rec['error'] = f'{type(e).__name__}: {e}'
        return rec
    try:
        with z:
            names = set(z.namelist())
            app = z.read('docProps/app.xml').decode('utf-8-sig', 'replace') if 'docProps/app.xml' in names else ''
            m = re.search(r'<AppVersion>([\d.]+)', app)
            rec['sl_version'] = m.group(1) if m else ''
            raw = z.read('story/story.xml').decode('utf-8-sig', 'replace')
            st = ET.fromstring(raw.encode('utf-8'))
            if 'story/playerProps.xml' in names:   # player title = what learners (and TalentLMS unit names) see
                pp = z.read('story/playerProps.xml').decode('utf-8-sig', 'replace')
                m = re.search(r'name="title_text"[^>]*value="([^"]*)"', pp)
                rec['player_title'] = html.unescape(m.group(1)).strip() if m else ''
            un = html.unescape(raw)
            m = re.search(r'<lms [^>]*type="([^"]+)"', un); rec['lms_type'] = m.group(1) if m else ''
            m = re.search(r'<lesson><title>([^<]*)</title><id>([^<]*)</id>', un); rec['lms_title'] = m.group(1) if m else ''
            m = re.search(r'<prop id="23">([^<]*)</prop>', raw); rec['project_id_prop'] = m.group(1) if m else ''
            m = re.search(r'<prop id="5">([^<]*)</prop>', raw); rec['project_title_prop'] = html.unescape(m.group(1)) if m else ''
            sz = st.find('.//sz')
            rec['size'] = f'{sz.get("w")}x{sz.get("h")}' if sz is not None else ''
            rec['scenes'] = [s.get('name') for s in st.iter('scene') if s.get('name')]
            rec['vars'] = [{'name': v.get('name'), 'type': v.get('dataType'), 'val': v.get('val')}
                           for v in st.iter('var') if v.get('type') == 'user']
            med, origins, media_bytes = collections.Counter(), collections.Counter(), 0
            for tag in ('media', 'audio'):
                for mm in st.iter(tag):
                    if not mm.get('g') or not mm.get('type'):
                        continue
                    t = mm.get('type'); b = int(mm.get('bytes') or 0)
                    med[t] += 1; media_bytes += b
                    o = classify_origin(mm.get('origFile') or '')
                    origins[o] += 1
                    media_list.append({'kind': tag, 'type': t, 'name': mm.get('displayName'), 'orig': mm.get('origFile'),
                                       'source': mm.get('source'), 'bytes': b, 'origin': o})
            rec['media_types'] = dict(med); rec['media_origins'] = dict(origins); rec['media_bytes'] = media_bytes
            rec['zip_media_files'] = dict(collections.Counter(os.path.splitext(n)[1].lower() for n in names if n.startswith('story/media/')))
            rec['quiz_banks'] = len(list(st.iter('bankProps')))
            try:
                rels = ET.fromstring(z.read('story/_rels/story.xml.rels'))
                order = ['story/slides/' + r.get('Target').split('/')[-1] for r in rels if r.get('Type') == 'slide']
            except KeyError:
                order = sorted(n for n in names if n.startswith('story/slides/') and n.endswith('.xml'))
            slides, all_texts, fonts = [], [], collections.Counter()
            for fn in order:
                if fn not in names:
                    continue
                root = ET.fromstring(z.read(fn))
                sld = root if local(root.tag) == 'sld' else root.find('.//sld')
                tags = collections.Counter(local(e.tag) for e in root.iter())
                trig = collections.Counter()
                for d in root.iter('data'):
                    if d.get('event') and d.get('action'):
                        trig[f"{d.get('event')}>{d.get('action')}"] += 1
                anims = collections.Counter()
                for kind in ('entr', 'exit'):
                    for e in root.iter(kind):
                        for c in e:
                            anims[f'{kind}:{local(c.tag)}'] += 1
                for p_ in PATHS:
                    if tags[p_]:
                        anims[f'motion:{p_}'] += tags[p_]
                states = collections.Counter(s.get('name') for s in root.iter('state')
                                             if s.get('name') and s.get('name') not in ('Normal', '_default'))
                texts = []
                for t in root.iter('text'):
                    if t.text and t.text.lstrip().startswith('<'):
                        tx, fo = text_spans(t.text)
                        texts += tx; fonts.update(fo)
                slides.append({'file': fn.split('/')[-1], 'name': sld.get('name') if sld is not None else '',
                               'layout': sld.get('layoutType') if sld is not None else '',
                               'layers': [l.get('name') for l in root.iter('sldLayer') if l.get('name')],
                               'feedback_layers': len(list(root.iter('feedBackLayer'))),
                               'objs': {k: tags[k] for k in OBJS if tags[k]},
                               'interactions': {k: tags[k] for k in INTERACTIONS if tags[k]},
                               'triggers': dict(trig), 'anims': dict(anims), 'states': dict(states.most_common(15)),
                               'texts': texts})
                all_texts += texts
            rec['slides'] = slides
            rec['n_slides'] = len(slides); rec['n_layers'] = sum(len(s['layers']) for s in slides)
            rec['fonts'] = dict(fonts.most_common(12))
            mr = [t for t in all_texts if DEVA.search(t)]
            rec['marathi_strings'] = len(mr); rec['english_strings'] = len(all_texts) - len(mr)
            rec['interactions'] = agg(slides, 'interactions'); rec['triggers'] = agg(slides, 'triggers')
            rec['anims'] = agg(slides, 'anims'); rec['objs'] = agg(slides, 'objs')
            blob = ' '.join([rel] + [v['val'] or '' for v in rec['vars']] + all_texts[:50])
            rec['codes'] = sorted(set(c.upper().replace(' ', '-') for c in CODE.findall(blob)))
            cn = [v['val'] for v in rec['vars'] if v['name'] and v['name'].lower() == 'coursename']
            rec['coursename_var'] = cn[0] if cn else ''
            rec['has_thumbnail'] = 'docProps/thumbnail.jpg' in names
    except Exception as e:
        rec['error'] = f'{type(e).__name__}: {e}'
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / f'{pid}.json').write_text(json.dumps({**rec, 'media': media_list}, ensure_ascii=False, indent=1), encoding='utf-8')
    return rec


COLS = ['pid', 'rel', 'name', 'bytes', 'sl_version', 'size', 'player_title', 'lms_type', 'lms_title', 'project_id_prop', 'project_title_prop', 'n_slides', 'n_layers', 'marathi_strings', 'english_strings',
        'codes', 'coursename_var', 'interactions', 'anims', 'media_types', 'media_origins', 'media_bytes', 'fonts', 'error']

if __name__ == '__main__':
    files = [os.path.join(d, f) for d, _, fs in os.walk(SRC) for f in fs if f.lower().endswith('.story')]
    # .story files that exist only inside zips (no loose copy of the same size)
    zm = list(csv.DictReader(open(HERE / '_work' / 'zip_members.csv', encoding='utf-8')))
    loose = {int(r['bytes']) for r in csv.DictReader(open(HERE / '_work' / 'files.csv', encoding='utf-8')) if r['ext'] == '.story'}
    files += [(m['zip'], m['member']) for m in zm if m['member'].lower().endswith('.story') and int(m['bytes']) not in loose]
    with Pool(6) as pool:
        recs = pool.map(parse, files, chunksize=4)
    out = HERE / 'catalogue' / 'projects.csv'
    out.parent.mkdir(exist_ok=True)
    with open(out, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for r in sorted(recs, key=lambda r: r['rel']):
            w.writerow([json.dumps(r.get(c), ensure_ascii=False) if isinstance(r.get(c), (dict, list)) else r.get(c, '') for c in COLS])
    print('parsed', len(recs), 'errors', sum(1 for r in recs if r.get('error')))

"""Step 3: pick final versions and match Storyline projects to TalentLMS SCORM/xAPI units (all local data, no API calls).

Outputs: catalogue/units.csv (one row per TalentLMS SCORM/xAPI unit + matched project)
         catalogue/projects_final.csv (one row per final project + matched units)
         _work/match.json (everything, for later steps)
"""
import csv, json, re, glob, pathlib, difflib, collections, unicodedata

HERE = pathlib.Path(__file__).resolve().parents[1]
W = HERE / '_work'
BS = chr(92)

# ---------- projects ----------
files = {r['path'].lower(): r for r in csv.DictReader(open(W / 'files.csv', encoding='utf-8'))}
BASE = r'B:\My Documents\Marathi Shala' + BS
projects = []
for r in csv.DictReader(open(HERE / 'catalogue/projects.csv', encoding='utf-8-sig')):
    path = r['rel'].split(' :: ')[0]
    f = files.get((BASE + path).lower(), {})
    r['sha1'] = f.get('sha1', '') + (('#' + r['rel'].split(' :: ')[1]) if ' :: ' in r['rel'] else '')
    r['mtime'] = f.get('mtime', '')
    r['format'] = 'SL1 (2014, binary)' if 'not a zip' in r['error'] else ('SL' + r['sl_version'][:1] if r['sl_version'] else '?')
    low = r['rel'].lower()
    r['is_backup'] = bool(re.search(r'backup|bkp|\bold\b|old sl|orig source|copy|\btemp\b|test zone|trial|try\b|for saurabh|\bwip\b', low))
    r['area'] = r['rel'].split(BS)[0]
    projects.append(r)


def norm(s):
    s = unicodedata.normalize('NFC', s or '').lower()
    s = re.sub(r'[\u2013\u2014_\-–:()/,.]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def rank(p):  # higher = better candidate for "final version"
    v = p['sl_version'] or '0'
    return (not p['is_backup'], p['format'] != 'SL1 (2014, binary)', v.split('.')[0], p['mtime'])


# ---------- TalentLMS ----------
cats = {c['id']: c for c in json.load(open(W / 'tlms/categories.json', encoding='utf-8'))}


def catpath(i):
    out = []
    while i and i in cats:
        out.append(cats[i]['name']); i = cats[i].get('parent_category_id')
    return ' > '.join(reversed(out))


units = []
courses = []
for fn in glob.glob(str(W / 'tlms/course_*.json')):
    c = json.load(open(fn, encoding='utf-8'))
    cp = catpath(c['category_id'])
    code = re.search(r'\((L\d[^)]*)\)', c['name'])
    trial = bool(code and code.group(1).lower().endswith('f')) or 'free trial' in cp.lower()
    types = collections.Counter(u['type'] for u in c.get('units', []))
    courses.append({'course_id': c['id'], 'course': c['name'], 'category': cp, 'status': c['status'], 'created': c['creation_date'][:10],
                    'year': c['creation_date'][6:10], 'code': code.group(1) if code else '', 'free_trial_copy': trial,
                    'unit_types': dict(types), 'users': len(c.get('users', []))})
    for u in c.get('units', []):
        if u['type'] == 'SCORM | xAPI | cmi5':
            units.append({'unit_id': u['id'], 'unit': u['name'], 'course_id': c['id'], 'course': c['name'], 'category': cp,
                          'status': c['status'], 'year': c['creation_date'][6:10], 'code': code.group(1) if code else '',
                          'free_trial_copy': trial, 'learners': len(c.get('users', []))})

# f-trial rule: skip "...f" copies unless no non-f course with the same base code exists
base_codes = {u['code'] for u in units if u['code'] and not u['free_trial_copy']}
for u in units:
    u['skip_trial'] = u['free_trial_copy'] and u['code'][:-1] in base_codes

# ---------- matching (scored) ----------
DEV = re.compile(r'[ऀ-ॿ]+')
GOOD = [p for p in projects if p['format'] != 'SL1 (2014, binary)' or True]


def toks(s):
    return set(t for t in norm(s).split() if len(t) > 1 or DEV.match(t))


def sim(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    ta, tb = toks(a), toks(b)
    jac = len(ta & tb) / max(1, len(ta | tb))
    sm = difflib.SequenceMatcher(None, a, b)
    r = sm.ratio() if sm.real_quick_ratio() > 0.5 else 0
    return max(jac, r)


def level_of(s):
    m = re.search(r'level ?0?(\d)', s.lower())
    return m.group(1) if m else None


def sem_of(s):
    m = re.search(r'sem(?:ester|ister)? ?_?(\d)', s.lower())
    return m.group(1) if m else None


SWAR = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ', 'अं', 'अः', 'ॲ', 'ऑ']
VY36 = ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ',
        'म', 'य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह', 'ळ', 'क्ष', 'ज्ञ']
VY34 = [x for x in VY36 if x not in ('ङ', 'ञ')]          # Level 0 "Vocabulary Module 16..49" order (verified on folder names)
LAT = {'a': 'अ', 'aa': 'आ', 'i': 'इ', 'ee': 'ई', 'u': 'उ', 'uu': 'ऊ', 'oo': 'ऊ', 'ru': 'ऋ', 'ae': 'ए', 'e': 'ए', 'ai': 'ऐ', 'aei': 'ऐ',
       'o': 'ओ', 'au': 'औ', 'ou': 'औ', 'am': 'अं', 'aha': 'अः', 'ah': 'अः', 'aya': 'ॲ',
       'k': 'क', 'ka': 'क', 'kh': 'ख', 'kha': 'ख', 'g': 'ग', 'ga': 'ग', 'gh': 'घ', 'gha': 'घ', 'gna': 'ङ', 'ch': 'च', 'cha': 'च',
       'chh': 'छ', 'chha': 'छ', 'j': 'ज', 'ja': 'ज', 'z': 'झ', 'za': 'झ', 'jh': 'झ', 'jha': 'झ', 'yna': 'ञ', 'T': 'ट', 'Ta': 'ट',
       'Tha': 'ठ', 'D': 'ड', 'Da': 'ड', 'Dha': 'ढ', 'N': 'ण', 'Na': 'ण', 't': 'त', 'ta': 'त', 'tha': 'थ', 'th': 'थ', 'd': 'द',
       'da': 'द', 'dha': 'ध', 'n': 'न', 'na': 'न', 'p': 'प', 'pa': 'प', 'ph': 'फ', 'pha': 'फ', 'b': 'ब', 'ba': 'ब', 'bh': 'भ',
       'bha': 'भ', 'm': 'म', 'ma': 'म', 'y': 'य', 'ya': 'य', 'r': 'र', 'ra': 'र', 'l': 'ल', 'la': 'ल', 'v': 'व', 'va': 'व',
       'sh': 'श', 'sha': 'श', 'Sh': 'ष', 'Sha': 'ष', 's': 'स', 'sa': 'स', 'h': 'ह', 'ha': 'ह', 'L': 'ळ', 'La': 'ळ',
       'ksha': 'क्ष', 'dnya': 'ज्ञ'}


def letter_from_name(rel, name):
    m = re.search(r'L1[- ](?:01[- ])?0(\d\d)', name)
    if m and 1 <= int(m.group(1)) <= 15:
        return SWAR[int(m.group(1)) - 1]
    m = re.search(r'L1[- ]1(\d\d)', name)
    if m and 1 <= int(m.group(1)) <= 36:
        return VY36[int(m.group(1)) - 1]
    m = re.search(r'Vocabulary Module (\d+)', name)
    if m and 'level 0' in rel.lower():
        n = int(m.group(1))
        if 1 <= n <= 15: return SWAR[n - 1]
        if 16 <= n <= 49: return VY34[n - 16]
    m = re.search(r'(?:Module|Trace)\s*\d*\s*[-_ ]?\s*([A-Za-z]+)\s*(?:[-_ ].*)?$', name)
    if m:
        w = m.group(1)
        return LAT.get(w) or LAT.get(w.lower()) or LAT.get(w[:1].upper() + w[1:].lower())
    return None


def nums(s):
    return set(int(x) for x in re.findall(r'\d+', s or '') if int(x) <= 1000)


for p in projects:
    parts = p['rel'].split(' :: ')[0].split(BS)
    p['_file'] = p['name']
    p['_folder'] = ' '.join(parts[-3:-1])
    p['_level'] = level_of(p['rel']); p['_sem'] = sem_of(p['rel'])
    lt = letter_from_name(p['rel'], p['name'])
    p['_dev'] = {lt} if lt else (set(DEV.findall(p.get('player_title') or '')) | set(DEV.findall(p['name'])))
    p['_num'] = nums(p['name']) | nums(p.get('player_title'))
    m = re.search(r'(conversation|vocabulary|writing)\w* modules? (\d+)', p['rel'].lower())
    p['_mod'] = (m.group(1), int(m.group(2))) if m else None


def score(u, p):
    s = 3 * max(sim(u['unit'], p.get('player_title')), sim(u['course'], p.get('player_title')))
    s += 2 * max(sim(u['unit'], p['_file']), sim(u['course'], p['_file']), 0.7 * sim(u['course'], p['_folder']))
    lv = level_of(u['category'])
    if lv and p['_level']:
        s += 0.6 if lv == p['_level'] else -0.6
    sm = sem_of(u['category'])
    if sm and p['_sem']:
        s += 0.6 if sm == p['_sem'] else -0.8
    ud = {t for t in DEV.findall(u['unit'] + ' ' + u['course']) if len(t) <= 3}   # single letters (akshara)
    pd = {t for t in p['_dev'] if len(t) <= 3}
    if ud and pd:
        s += 1.5 if ud & pd else -2.5
    # Gappa Goshti: "Week W" of a module course <-> "<Module> Module W" in the same semester folder
    wk = re.search(r'week (\d+)', u['course'].lower())
    kind = re.search(r'(conversation|vocabulary|writing)', u['category'].lower())
    if wk and kind and p['_mod'] and p['_sem']:
        if p['_mod'][0] == kind.group(1):
            s += 2.0 if p['_mod'][1] == int(wk.group(1)) else -1.5
    un = nums(u['unit'] + ' ' + u['course']) - ({int(wk.group(1))} if wk else set())
    if un and p['_num'] and not wk:
        s += 0.8 if un & p['_num'] else -1.0
    uk = 'vocab' if ('words with' in (u['unit'] + u['course']).lower() or 'vocab' in u['category'].lower()) else          ('write' if re.search(r'trace|writ', (u['unit'] + u['course'] + u['category']).lower()) else None)
    pr = p['rel'].lower()
    pk = 'vocab' if 'vocab' in pr else ('write' if re.search(r'trace|writ', pr) else None)
    if uk and pk:
        s += 1.0 if uk == pk else -1.0
    era2020 = u['year'] >= '2020'
    if era2020 and p['area'] == 'Republished Activities':
        s += 0.5
    if not era2020 and p['area'] in ('Source Files from Newgen', 'Gappa Goshti Class'):
        s += 0.5
    if p['is_backup']:
        s -= 0.4
    if p['format'] == 'SL1 (2014, binary)':
        s -= 0.6
    return s


for u in units:
    u['is_test'] = u['category'].lower().startswith('test') or u['course'].lower().startswith('*** coming')
    # Gappa Goshti: semester from category, week from course name, module kind from category
    sc = sorted(((score(u, p), p) for p in projects), key=lambda x: x[0], reverse=True)
    seen, top = set(), []
    for v, p in sc:
        if p['sha1'] in seen:
            continue
        seen.add(p['sha1']); top.append((v, p))
        if len(top) == 3:
            break
    v, p = top[0]
    margin = v - top[1][0] if len(top) > 1 else v
    u['match_score'] = round(v, 2); u['match_margin'] = round(margin, 2)
    u['match_conf'] = 'high' if v >= 4.5 else ('medium' if v >= 3.2 else 'low')
    u['match_pid'] = p['pid']; u['match_rel'] = p['rel']; u['match_title'] = p.get('player_title', '')
    u['match_alt'] = [(round(x, 2), q['rel']) for x, q in top[1:]]

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    live = [u for u in units if not u['skip_trial'] and not u['is_test']]
    print('units', len(units), 'live (no tests, f-rule)', len(live), collections.Counter(u['match_conf'] for u in live))
    for u in sorted(live, key=lambda u: u['match_score']):
        if u['match_conf'] != 'high':
            print(f"  {u['match_conf'][:3]} {u['match_score']:.1f} | {u['course'][:42]} | {u['unit'][:38]} -> {u['match_rel'][-70:]} [{u['match_title'][:30]}]")
    json.dump({'units': units, 'courses': courses, 'projects': projects}, open(W / 'match.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, default=sorted)
    cat = HERE / 'catalogue'
    with open(cat / 'units.csv', 'w', newline='', encoding='utf-8-sig') as f:
        cols = ['unit_id', 'unit', 'course_id', 'course', 'category', 'year', 'status', 'learners', 'code', 'free_trial_copy', 'skip_trial',
                'is_test', 'match_conf', 'match_score', 'match_pid', 'match_rel', 'match_title']
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
        w.writerows(sorted(units, key=lambda u: (u['category'], u['course'])))
    with open(cat / 'courses.csv', 'w', newline='', encoding='utf-8-sig') as f:
        cols = ['course_id', 'course', 'category', 'status', 'created', 'code', 'free_trial_copy', 'users', 'unit_types']
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
        w.writerows(sorted(({**c, 'unit_types': json.dumps(c['unit_types'], ensure_ascii=False)} for c in courses), key=lambda c: c['category']))
    used = collections.defaultdict(list)
    for u in live:
        used[u['match_pid']].append(u)
    with open(cat / 'projects_live.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['pid', 'rel', 'player_title', 'format', 'lms_type', 'n_slides', 'n_layers', 'units', 'unit_names', 'best_conf'])
        for pid, us in sorted(used.items(), key=lambda kv: kv[1][0]['match_rel']):
            pr = next(p for p in projects if p['pid'] == pid)
            w.writerow([pid, pr['rel'], pr.get('player_title', ''), pr['format'], pr['lms_type'], pr['n_slides'], pr['n_layers'], len(us),
                        ' | '.join(u['course'] + ' / ' + u['unit'] for u in us), max((u['match_conf'] for u in us), key=['low', 'medium', 'high'].index)])
    print('live units', len(live), 'distinct source projects used', len(used))

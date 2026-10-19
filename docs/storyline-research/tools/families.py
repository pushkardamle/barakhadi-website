"""Step 4: group the live source projects into activity families (candidate engines) and build agent dossiers."""
import csv, json, re, sys, pathlib, collections

HERE = pathlib.Path(__file__).resolve().parents[1]
W = HERE / '_work'

# (key, label, regex on "player title | file name | unit names") — first match wins
RULES = [
    ('word-games', 'Word games (crossword, word search, picture-word pairs)', r'crossword|word search|chitra.?shabd|treasure'),
    ('grammar-translation', 'Grammar & translation (nouns, pronouns, prepositions, translation)', r'noun|pronoun|preposition|translation|भाषांतर'),
    ('numbers-time', 'Numbers & time (numerals, number words, ordinals, songs, clock)', r'number|numeral|ordinal|अंक|clock|show the time|counting'),
    ('books-comprehension', 'Books & comprehension (stories, listening/reading comprehension, picture description)',
     r'\bbook\b|lion|sinha|farm|sharir|parts of body|comprehension|picture description|story of'),
    ('conversation', 'Conversation scenes (dialogue modules)', r'conversation'),
    ('letter-trace', 'Letter learn & trace (full letter lessons: puzzle, stroke video, trace, word hunt, barakhadi)',
     r'learn and (trace|practice) - (स्वर|व्यंजन)|L1[- ]?(01[- ])?0\d\d|L1[- ]1\d\d'),
    ('trace-write', 'Trace & write / handwriting practice (stroke video, join dots, write words)',
     r'trace and write|optional writ|writing module|write letter|writing simple|join the dots|color the letter|bonus writing|learn and trace'),
    ('vocab-letter', 'Words with a letter (vocabulary cards) & alphabet intros/songs',
     r'words with|vocabulary module|vyanjanmala|akshar|alphabet|swar song|barakhadi'),
]


def family_of(text):
    for key, label, rx in RULES:
        if re.search(rx, text, re.I):
            return key
    return 'other'


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    live = list(csv.DictReader(open(HERE / 'catalogue' / 'projects_live.csv', encoding='utf-8-sig')))
    fams = collections.defaultdict(list)
    for r in live:
        d = json.load(open(W / 'projects' / f"{r['pid']}.json", encoding='utf-8'))
        text = ' | '.join([r['player_title'], r['rel'].split('\\')[-1], r['unit_names']])
        k = family_of(text)
        r['family'] = k
        fp = {k2: d.get(k2) for k2 in ('n_slides', 'n_layers', 'interactions', 'anims', 'media_types', 'media_origins', 'fonts',
                                      'marathi_strings', 'english_strings', 'sl_version', 'lms_type', 'vars')}
        fams[k].append({**r, 'fingerprint': fp})
    (W / 'families').mkdir(exist_ok=True)
    labels = {k: l for k, l, _ in RULES} | {'other': 'Other / unclassified'}
    with open(HERE / 'catalogue' / 'families.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['family', 'label', 'pid', 'rel', 'player_title', 'units', 'unit_names', 'n_slides', 'n_layers'])
        for k, items in sorted(fams.items()):
            for it in items:
                w.writerow([k, labels[k], it['pid'], it['rel'], it['player_title'], it['units'], it['unit_names'], it['n_slides'], it['n_layers']])
            json.dump({'family': k, 'label': labels[k], 'projects': items}, open(W / 'families' / f'{k}.json', 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
    for k, items in sorted(fams.items(), key=lambda kv: -len(kv[1])):
        print(f'{len(items):4} projects {sum(int(i["units"]) for i in items):4} units  {k}')
    for it in fams.get('other', []):
        print('   other:', it['rel'][-60:], '|', it['player_title'])

"""Step 1b: TalentLMS courses and units, GET only (via tlms_readonly.get). Saves raw JSON to _work/tlms/."""
import json, pathlib, time, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from tlms_readonly import get

OUT = pathlib.Path(__file__).resolve().parents[1] / '_work' / 'tlms'
OUT.mkdir(parents=True, exist_ok=True)
courses = get('courses')
(OUT / 'courses.json').write_text(json.dumps(courses, ensure_ascii=False, indent=1), encoding='utf-8')
print('courses', len(courses), flush=True)
for i, c in enumerate(courses):
    f = OUT / f'course_{c["id"]}.json'
    if f.exists(): continue
    f.write_text(json.dumps(get(f'courses/id:{c["id"]}'), ensure_ascii=False, indent=1), encoding='utf-8')
    if i % 50 == 0: print(i, flush=True)
    time.sleep(0.25)
for name in ('categories', 'branches', 'groups'):
    try: (OUT / f'{name}.json').write_text(json.dumps(get(name), ensure_ascii=False, indent=1), encoding='utf-8')
    except SystemExit as e: print(name, e)
print('done')

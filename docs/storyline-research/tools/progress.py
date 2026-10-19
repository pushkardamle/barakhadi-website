"""Progress tracker: keeps state in _work/progress.json and renders progress.html + PROGRESS.md.

Usage (CLI):  python progress.py step <n> <status> [note]      status: todo|running|done
              python progress.py log "<message>"
              python progress.py stat "<label>" "<value>"
              python progress.py finding "<text>"
              python progress.py next "<text>"
"""
import json, sys, html, datetime, pathlib

HERE = pathlib.Path(__file__).resolve().parents[1]
STATE = HERE / '_work' / 'progress.json'
STEPS = ['Inventory: files, hashes, duplicates, TalentLMS courses & units',
         'Catalogue: parse every .story, previews',
         'Matching: projects ↔ TalentLMS courses/units',
         'Grouping: activity families → candidate engines',
         'Deep dives: engine specs (agent workflow) + web-content review',
         'Report: report.html, published privately for phone reading']

def load():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding='utf-8'))
    return {'steps': [{'title': t, 'status': 'todo', 'note': ''} for t in STEPS],
            'stats': {}, 'findings': [], 'log': [], 'next': '', 'started': now()}

def now():
    return datetime.datetime.now().strftime('%a %d %b, %I:%M %p')

def save(s):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    s['updated'] = now()
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding='utf-8')
    render(s)

def render(s):
    e = html.escape
    icon = {'done': '✔', 'running': '●', 'todo': '○'}
    steps = ''.join(f'<li class="{x["status"]}"><span class="i">{icon[x["status"]]}</span><div><b>Step {i+1}.</b> {e(x["title"])}'
                    f'{"<div class=n>" + e(x["note"]) + "</div>" if x["note"] else ""}</div></li>' for i, x in enumerate(s['steps']))
    stats = ''.join(f'<div class="stat"><div class="v">{e(str(v))}</div><div class="l">{e(k)}</div></div>' for k, v in s['stats'].items())
    finds = ''.join(f'<li>{e(f)}</li>' for f in s['findings']) or '<li class=muted>None yet</li>'
    log = ''.join(f'<li><time>{e(t)}</time> {e(m)}</li>' for t, m in reversed(s['log'][-40:]))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="30"><title>Storyline research progress</title><style>
:root{{--bg:#f7f8f6;--card:#fff;--fg:#1d2420;--mut:#66706a;--acc:#2f7d4f;--run:#d07a12;--line:#e2e6e3}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151917;--card:#1e2421;--fg:#e8ece9;--mut:#9aa59f;--acc:#5fc28a;--run:#f0a24a;--line:#2d3530}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,Segoe UI,sans-serif}}
main{{max-width:880px;margin:auto;padding:24px max(16px,env(safe-area-inset-left))}}
h1{{font-size:1.5rem;margin:0}} h2{{font-size:1rem;margin:28px 0 10px;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}}
.sub{{color:var(--mut);font-size:.9rem}} ol{{list-style:none;padding:0;margin:0;display:grid;gap:8px}}
ol li{{display:flex;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px}}
.i{{width:1.2em;text-align:center}} .done .i{{color:var(--acc)}} .running{{border-color:var(--run)}} .running .i{{color:var(--run)}} .todo{{color:var(--mut)}}
.n{{color:var(--mut);font-size:.88rem}} .stats{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px}} .v{{font-size:1.35rem;font-weight:700}} .l{{color:var(--mut);font-size:.82rem}}
ul{{padding-left:20px;margin:0}} ul.log{{list-style:none;padding:0;font-size:.88rem}} ul.log li{{border-bottom:1px solid var(--line);padding:4px 0}}
time{{color:var(--mut);margin-right:6px}} .muted{{color:var(--mut)}} .next{{background:var(--card);border-left:4px solid var(--run);padding:10px 14px;border-radius:6px}}
</style></head><body><main>
<h1>Storyline → HTML5 research</h1><div class="sub">Started {e(s["started"])} · last update {e(s["updated"])} · this page refreshes every 30 s · read-only on Newgen &amp; TalentLMS</div>
<h2>Steps</h2><ol>{steps}</ol>
<h2>Numbers so far</h2><div class="stats">{stats or '<div class=muted>Counting…</div>'}</div>
<h2>Next</h2><div class="next">{e(s["next"] or "—")}</div>
<h2>Findings</h2><ul>{finds}</ul>
<h2>Activity log</h2><ul class="log">{log}</ul>
</main></body></html>'''
    (HERE / 'progress.html').write_text(page, encoding='utf-8')
    md = [f'# Storyline research progress\n\nLast update: {s["updated"]}\n\n## Steps\n']
    md += [f'{i+1}. [{ {"done":"x","running":"~","todo":" "}[x["status"]] }] {x["title"]}' + (f' — {x["note"]}' if x['note'] else '') for i, x in enumerate(s['steps'])]
    md += ['\n## Numbers\n'] + [f'- {k}: {v}' for k, v in s['stats'].items()]
    md += [f'\n## Next\n\n{s["next"]}\n\n## Findings\n'] + [f'- {f}' for f in s['findings']]
    md += ['\n## Log\n'] + [f'- {t} {m}' for t, m in s['log']]
    (HERE / 'PROGRESS.md').write_text('\n'.join(md) + '\n', encoding='utf-8')

def cli(a):
    s = load()
    cmd = a[0]
    if cmd == 'step':
        n = int(a[1]) - 1; s['steps'][n]['status'] = a[2]
        if len(a) > 3: s['steps'][n]['note'] = a[3]
        s['log'].append([now(), f'Step {n+1} {a[2]}' + (f': {a[3]}' if len(a) > 3 else '')])
    elif cmd == 'log': s['log'].append([now(), a[1]])
    elif cmd == 'stat': s['stats'][a[1]] = a[2]
    elif cmd == 'finding': s['findings'].append(a[1])
    elif cmd == 'next': s['next'] = a[1]
    save(s)

if __name__ == '__main__':
    cli(sys.argv[1:])

"""Render a contact sheet (PNG) of every slide + layer of one .story project, READ-ONLY on the source.

Usage: python render_preview.py <pid> [<pid> ...]
Images are read from the .story zip in memory and written under previews/<pid>/ (git-ignored); the sheet is
drawn as SVG and screenshotted with headless Chrome -> previews/<pid>/sheet-1.png (more pages if large).
"""
import io, os, re, sys, json, html, zipfile, pathlib, subprocess
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parents[1]
BASE = r'B:\My Documents\Marathi Shala'
SHOT = pathlib.Path(__file__).with_name('shoot.mjs')
OBJ = {'pic', 'rect', 'roundRect', 'textBox', 'btn', 'star', 'oval', 'line', 'multiply', 'checkMark', 'shape', 'feedBackBtn',
       'group', 'dragDropIntr', 'triangle', 'arc', 'freeForm', 'sound', 'movie'}
PER_PAGE = 24


def open_story(rel):
    path, _, member = rel.partition(' :: ')
    full = os.path.join(BASE, path)
    if member:
        with zipfile.ZipFile(full) as o:
            return zipfile.ZipFile(io.BytesIO(o.read(member)))
    return zipfile.ZipFile(full)


def spans(el):
    t = el.find('text')
    if t is None or not t.text:
        return ''
    try:
        doc = ET.fromstring(t.text)
    except ET.ParseError:
        return ''
    return ' / '.join(''.join(s.get('Text', '') for s in b.iter('Span')) for b in doc.iter('Block')).strip(' /')


def render(pid):
    meta = json.load(open(HERE / '_work' / 'projects' / f'{pid}.json', encoding='utf-8'))
    out = HERE / 'previews' / pid
    (out / 'media').mkdir(parents=True, exist_ok=True)
    z = open_story(meta['rel'])
    names = z.namelist()
    sizes = {}
    for i in z.infolist():
        if i.filename.startswith('story/media/'):
            sizes.setdefault(i.file_size, []).append(i.filename)
    st = ET.fromstring(z.read('story/story.xml'))
    media = {}
    for m in list(st.iter('media')):
        g, b, nm = m.get('g'), m.get('bytes'), m.get('displayName', '')
        ext = os.path.splitext(nm)[1].lower()
        c = sizes.get(int(b or -1), [])
        pick = [x for x in c if x.lower().endswith(ext)] or c
        if pick and ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.emf', '.wmf', '') and pick[0].lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            dest = out / 'media' / os.path.basename(pick[0])
            if not dest.exists():
                dest.write_bytes(z.read(pick[0]))
            media[g] = 'media/' + dest.name

    def draw(objs, parts):
        for el in sorted(objs, key=lambda e: int(e.get('zOrder') or 0)):
            loc = el.find('loc')
            hidden = (el.find('tmProps') is not None and el.find('tmProps').get('visible') == 'false')
            if loc is not None:
                l, t, r, b = (float(loc.get(k)) for k in ('l', 't', 'r', 'b'))
                w, h = max(r - l, 1), max(b - t, 1)
                op = 0.35 if hidden else 1
                if el.get('assetG') in media:
                    parts.append(f'<image href="{media[el.get("assetG")]}" x="{l}" y="{t}" width="{w}" height="{h}" preserveAspectRatio="none" opacity="{op}"/>')
                elif el.tag in ('rect', 'roundRect', 'oval', 'shape', 'btn', 'star', 'textBox', 'triangle', 'freeForm'):
                    parts.append(f'<rect x="{l}" y="{t}" width="{w}" height="{h}" fill="none" stroke="#9aa" stroke-dasharray="4 3" opacity="{op}"/>')
                elif el.tag == 'movie':
                    parts.append(f'<rect x="{l}" y="{t}" width="{w}" height="{h}" fill="#000" opacity=".25"/><text x="{l+6}" y="{t+18}" font-size="16" fill="#fff">▶ video</text>')
                if el.tag == 'dragDropIntr' or el.find('.//dragDrop') is not None and el.tag == 'group':
                    pass
                txt = spans(el)
                if txt:
                    fs = max(11, min(h * 0.6, 34))
                    parts.append(f'<text x="{l + w/2}" y="{t + h/2}" font-size="{fs:.0f}" text-anchor="middle" dominant-baseline="middle" '
                                 f'font-family="Nirmala UI, Mangal, sans-serif" fill="#b00" opacity="{op}">{html.escape(txt[:48])}</text>')
            kids = el.find('childLst')
            if kids is not None:
                draw([c for c in kids if c.tag in OBJ], parts)

    try:
        rels = ET.fromstring(z.read('story/_rels/story.xml.rels'))
        order = ['story/slides/' + r.get('Target').split('/')[-1] for r in rels if r.get('Type') == 'slide']
    except KeyError:
        order = sorted(n for n in names if n.startswith('story/slides/') and n.endswith('.xml'))
    cells = []
    for si, fn in enumerate(o for o in order if o in names):
        root = ET.fromstring(z.read(fn))
        sld = root if root.tag == 'sld' else root.find('.//sld')
        if sld is None:
            continue
        layers = []
        base = sld.find('shapeLst')
        layers.append(('base', [c for c in base if c.tag in OBJ] if base is not None else []))
        for lay in sld.iter('sldLayer'):
            if lay.get('name') is None:
                continue
            sl = lay.find('shapeLst')
            layers.append((lay.get('name'), [c for c in sl if c.tag in OBJ] if sl is not None else []))
        for lj, (lname, objs) in enumerate(layers):
            parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 640">', '<rect width="960" height="640" fill="#fff"/>']
            if lj:
                parts.append('<g opacity="0.22">'); draw(layers[0][1], parts); parts.append('</g>')
            draw(objs, parts)
            parts.append('</svg>')
            cells.append((f'S{si+1} {html.escape(sld.get("name") or "")} · {html.escape(lname)}', ''.join(parts)))
    pages = [cells[i:i + PER_PAGE] for i in range(0, len(cells), PER_PAGE)] or [[]]
    pngs = []
    for pi, page in enumerate(pages):
        doc = ['<!doctype html><meta charset="utf-8"><style>body{margin:0;font:13px Segoe UI,sans-serif;background:#eef}'
               'h1{font-size:15px;margin:8px 12px}.g{display:grid;grid-template-columns:repeat(4,320px);gap:10px;padding:0 12px 12px}'
               '.c{background:#fff;border:1px solid #ccd}.c div{padding:3px 6px;color:#235;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
               'svg{display:block;width:320px;height:213px}</style>',
               f'<h1>{html.escape(meta["rel"][-110:])} — page {pi+1}/{len(pages)} · {len(cells)} slide-layers</h1><div class="g">']
        doc += [f'<div class="c"><div>{lbl}</div>{svg}</div>' for lbl, svg in page]
        doc.append('</div>')
        hp = out / f'sheet-{pi+1}.html'
        hp.write_text(''.join(doc), encoding='utf-8')
        pngs.append((hp, out / f'sheet-{pi+1}.png'))
    for hp, png in pngs:
        subprocess.run(['node', str(SHOT), hp.as_uri(), str(png)], check=True, capture_output=True)
    thumb = 'docProps/thumbnail.jpg'
    if thumb in names:
        (out / 'thumbnail.jpg').write_bytes(z.read(thumb))
    z.close()
    return [str(p) for _, p in pngs]


if __name__ == '__main__':
    for pid in sys.argv[1:]:
        print(pid, render(pid))

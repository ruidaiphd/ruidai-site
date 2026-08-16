#!/usr/bin/env python3
"""
Build the site.

    python3 build.py

Reads  content/*.yml, content/*.md, assets/*
Writes docs/            <- this folder is what gets deployed

Everything on the site comes from content/. Nothing is edited in docs/.
"""
import base64, html, json, pathlib, re, shutil, sys

try:
    import yaml, markdown
except ImportError:
    sys.exit("Missing deps. Run:  pip install pyyaml markdown")

ROOT = pathlib.Path(__file__).parent
SRC, TPL, ASSETS, OUT = ROOT/'content', ROOT/'templates', ROOT/'assets', ROOT/'docs'

# ---------------------------------------------------------------- load
site   = yaml.safe_load((SRC/'site.yml').read_text())
record = yaml.safe_load((SRC/'papers.yml').read_text())
TOPICS = site['topics']
LISTS  = site['lists']

KEYMAP = {'title':'t','year':'y','venue':'j','volume':'v','status':'s',
          'lists':'L','topics':'k','coauthors':'a','url':'u','notes':'n'}

def compact(p):
    """long field names in YAML -> short keys the page script expects"""
    o = {KEYMAP[k]: v for k, v in p.items() if k in KEYMAP}
    o.setdefault('v', ''); o.setdefault('L', []); o.setdefault('n', [])
    o['L'] = o['L'] or []; o['n'] = o['n'] or []
    return o

papers  = [compact(p) for p in record.get('papers') or []]
working = [compact(p) for p in record.get('working') or []]

# ---------------------------------------------------------------- checks
fatal, warn = [], []
for p in papers + working:
    for k in p['k']:
        if k not in TOPICS: fatal.append(f"unknown topic {k!r} in {p['t'][:44]!r}")
    for l in p['L']:
        if l not in LISTS: fatal.append(f"unknown list {l!r} in {p['t'][:44]!r}")
    if not str(p.get('u', '')).startswith(('http', '#')):
        warn.append(f"missing or odd url in {p['t'][:44]!r}")
    if p['s'] not in ('Published', 'Forthcoming', 'Working paper'):
        fatal.append(f"status {p['s']!r} in {p['t'][:44]!r} (use Published/Forthcoming/Working paper)")
names = {a for q in papers + working for a in q['a']}
for n in sorted(names):
    if ' ' not in n: warn.append(f"coauthor {n!r} has no first name")
surn = {}
for n in names: surn.setdefault(n.split()[-1], []).append(n)
for k, v in surn.items():
    if len(v) > 1: warn.append(f"surname {k!r} appears as {v} — two network nodes")
for w in warn:  print("  warn  " + w)
if fatal:
    for f in fatal: print("  ERROR " + f)
    sys.exit(f"\nBuild stopped: {len(fatal)} error(s) in content/papers.yml. Nothing was written.")

# ---------------------------------------------------------------- helpers
def b64(name):
    f = ASSETS/name
    return f"data:image/jpeg;base64,{base64.b64encode(f.read_bytes()).decode()}" if f.exists() else ""

def esc(s): return html.escape(str(s), quote=True)

def fontcss():
    """@font-face rules with the woff2 files embedded, so the pages need no font host (works offline / in China)."""
    out = []
    for f in sorted((TPL/'fonts').glob('*.woff2')):
        fam, wt = ('Barlow Condensed' if f.name.startswith('barlow') else 'Inter'), re.search(r'-(\d{3})-', f.name).group(1)
        data = base64.b64encode(f.read_bytes()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:swap;"
                   f"src:url(data:font/woff2;base64,{data}) format('woff2');}}")
    return '\n'.join(out)
FONTS = fontcss()

def row(p, n):
    marks = ''.join(
        f'<span class="mark" onclick="setF(\'list\',\'{l}\')">{LISTS[l]["label"]}</span>'
        for l in ('utd24','ft50') if l in p['L'])
    tags = ''.join(
        f'<span class="tag" style="background:{TOPICS[k]["color"]}22;color:{TOPICS[k]["color"]}" '
        f'onclick="setF(\'topic\',\'{k}\')">{TOPICS[k]["name"]}</span>' for k in p['k'])
    auth = ', '.join(f'<span onclick="setF(\'author\',&quot;{esc(a)}&quot;)">{esc(a)}</span>' for a in p['a'])
    notes = ''.join(f'<span class="badge">{esc(x)}</span>' for x in p['n'])
    vol = f", {esc(p['v'])}" if p['v'] else ''
    fc = ', forthcoming' if p['s'] == 'Forthcoming' else ''
    return (f'<div class="item"><div class="num">{n}</div><div class="bd">'
            f'<div class="ttl"><a href="{esc(p["u"])}" target="_blank" rel="noopener">{esc(p["t"])}</a></div>'
            f'<div class="au">{auth}</div>'
            f'<div class="ven">{esc(p["j"])}{vol} <em>({p["y"]}{fc})</em></div>'
            f'<div class="marks">{marks}{tags}</div>'
            + (f'<div>{notes}</div>' if notes else '') + '</div></div>')

def projects(md_text, start=0):
    """markdown -> alternating text/panel blocks"""
    md = markdown.Markdown()
    blocks, out = re.split(r'^## ', md_text, flags=re.M)[1:], []
    for i, b in enumerate(blocks):
        lines = b.strip().split('\n')
        title, body = lines[0].strip(), lines[1:]
        kick = url = ''
        while body and (body[0].startswith(('kick:', 'url:')) or not body[0].strip()):
            ln = body.pop(0).strip()
            if ln.startswith('kick:'): kick = ln[5:].strip()
            elif ln.startswith('url:'): url = ln[4:].strip()
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        img = next((f'{slug}{e}' for e in ('.jpg','.png') if (ASSETS/f'{slug}{e}').exists()), None)
        panel = (f'<img src="{b64(img)}" alt="{esc(title)}" '   # embedded, like banner/portrait
                 f'style="width:100%;height:100%;object-fit:cover">' if img else
                 f'<svg viewBox="0 0 400 300"><rect width="400" height="300" fill="#e9e6de"/>'
                 f'<g id="ph{start+i}"></g></svg>')
        out.append(
            f'  <div class="proj"><div class="txt">'
            + (f'<div class="kick">{esc(kick)}</div>' if kick else '')
            + f'<h3><a href="{esc(url) or "#"}">{esc(title)}</a></h3>'
            + md.reset().convert('\n'.join(body).strip())
            + f'</div><div class="shot">{panel}</div></div>')
    return '\n'.join(out), len(blocks)

# ---------------------------------------------------------------- render
OUT.mkdir(exist_ok=True)
work_html, nwork = projects((SRC/'work.md').read_text())
teach_html, _    = projects((SRC/'teaching.md').read_text(), start=nwork)

bnote = {'all': 'All peer-reviewed output, newest first. '
                'Every UTD24 journal is also on the FT50, so those two counts overlap.',
         'other': 'Peer-reviewed journals and conference proceedings outside both lists.'}
bnote.update({k: v['note'] for k, v in LISTS.items()})

r = (TPL/'research.html').read_text()
r = (r.replace('__FONTS__', FONTS).replace('__BANNER__', b64('banner.jpg'))
      .replace('__TOPICS__', json.dumps({k: {'name': v['name'], 'c': v['color']} for k, v in TOPICS.items()}, ensure_ascii=False))
      .replace('__LISTS__',  json.dumps({'all':'All', **{k: v['label'] for k, v in LISTS.items()}, 'other':'Other'}, ensure_ascii=False))
      .replace('__BNOTE__',  json.dumps(bnote, ensure_ascii=False))
      .replace('__DATA__',   json.dumps({'papers': papers, 'working': working}, ensure_ascii=False))
      .replace('__PUBS__',   ''.join(row(p, len(papers)-i) for i, p in enumerate(papers)))
      .replace('__WPS__',    ''.join(row(p, len(working)-i) for i, p in enumerate(working)))
      .replace('__WORK__',   work_html)
      .replace('__TEACHING__', teach_html)
      .replace('__PLACEHOLDERS__', (TPL/'placeholders.js').read_text())
      .replace('__D3__', (TPL/'d3-slim.min.js').read_text()))
(OUT/'research.html').write_text(r)

roles = '<div class="roles">' + ''.join(
    f'<div class="role"><b>{esc(x["title"])}</b><span>'
    + '<br>'.join(esc(l) for l in x['org'].strip().split('\n')) + '</span></div>'
    for x in site['roles']) + '</div>'
links = ''.join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in site['links'])
study = markdown.Markdown().convert((SRC/'home.md').read_text()).replace('<p>','').replace('</p>','')

stats_html = ''
if (SRC/'stats.yml').exists():
    st = yaml.safe_load((SRC/'stats.yml').read_text()) or {}
    sc, ss = st.get('scholar') or {}, st.get('ssrn') or {}
    fmt = lambda n: f"{int(n):,}"
    tiles = []
    if sc.get('citations'):
        tiles.append(f'<a class="stat" href="{esc(sc.get("url","#"))}" target="_blank" rel="noopener"><b>{fmt(sc["citations"])}</b><span>Scholar citations</span></a>')
    if ss.get('downloads'):
        tiles.append(f'<a class="stat" href="{esc(ss.get("url","#"))}" target="_blank" rel="noopener"><b>{fmt(ss["downloads"])}</b><span>SSRN downloads</span></a>')
    asof = st.get('as_of')
    if tiles:
        import datetime
        d = asof if isinstance(asof, datetime.date) else None
        stats_html = '<div class="stats">' + ''.join(tiles) + (f'<span class="asof">as of {d.strftime("%b %Y")}</span>' if d else '') + '</div>'

h = (TPL/'home.html').read_text()
h = (h.replace('__FONTS__', FONTS).replace('__PORTRAIT__', b64('portrait.jpg'))
      .replace('__ROLES__', roles).replace('__STUDY__', study).replace('__LINKS__', links).replace('__STATS__', stats_html))
(OUT/'home.html').write_text(h)

shutil.copytree(ASSETS, OUT/'assets', dirs_exist_ok=True)
cv = ASSETS/'cv.pdf'
if cv.exists():
    shutil.copy(cv, OUT/'cv.pdf')   # keep assets/cv.pdf current; the "cv.pdf" link serves from docs/
    shutil.os.remove(OUT/'assets'/'cv.pdf')  # avoid a duplicate copy under docs/assets/
(OUT/'index.html').write_text('<meta http-equiv="refresh" content="0;url=home.html">')
(OUT/'.nojekyll').touch()          # stop GitHub Pages running Jekyll over the output
dom = site.get('domain')
if dom: (OUT/'CNAME').write_text(dom + '\n')   # set `domain:` in site.yml when you're ready

print(f"built  {len(papers)} publications  {len(working)} working  "
      f"{nwork} projects  ->  docs/")
for f in sorted(OUT.glob('*.html')):
    print(f"       {f.name:16} {f.stat().st_size//1024:>4} KB")

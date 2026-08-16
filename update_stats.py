#!/usr/bin/env python3
"""
Refresh content/stats.yml from Google Scholar and SSRN, then rebuild:

    python3 update_stats.py && python3 build.py

Fetches are best-effort. Google Scholar in particular often blocks scripted access;
if a fetch fails the old number is kept and a note is printed. You can always edit
content/stats.yml by hand — the numbers on the home page are just what's in that file.
"""
import datetime, pathlib, re, sys, urllib.request
try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml")

P = pathlib.Path(__file__).parent / 'content' / 'stats.yml'
st = yaml.safe_load(P.read_text())
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
      'Accept-Language': 'en-US,en;q=0.9'}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20).read().decode('utf-8', 'ignore')

changed = []
# --- Google Scholar: the "Cited by" table
try:
    h = get(st['scholar']['url'])
    nums = [int(x) for x in re.findall(r'<td class="gsc_rsb_std">(\d+)</td>', h)]
    if len(nums) >= 6:                       # citations(all, since), h(all, since), i10(all, since)
        if nums[0] != st['scholar'].get('citations'): changed.append(f"citations {st['scholar'].get('citations')} -> {nums[0]}")
        st['scholar']['citations'], st['scholar']['h_index'] = nums[0], nums[2]
    else:
        print("  note  Google Scholar returned no table (probably a bot check) — kept old numbers")
except Exception as e:
    print(f"  note  Google Scholar fetch failed ({e.__class__.__name__}) — kept old numbers")

# --- SSRN author page: DOWNLOADS / SCHOLARLY PAPERS
try:
    h = re.sub(r'<[^>]+>', ' ', get(st['ssrn']['url']))
    m = re.search(r'DOWNLOADS\s+([\d,]+)', h); n = re.search(r'SCHOLARLY PAPERS\s+(\d+)', h)
    if m:
        d = int(m.group(1).replace(',', ''))
        if d != st['ssrn'].get('downloads'): changed.append(f"downloads {st['ssrn'].get('downloads')} -> {d}")
        st['ssrn']['downloads'] = d
        if n: st['ssrn']['papers'] = int(n.group(1))
    else:
        print("  note  SSRN page had no download count — kept old numbers")
except Exception as e:
    print(f"  note  SSRN fetch failed ({e.__class__.__name__}) — kept old numbers")

st['as_of'] = datetime.date.today()
P.write_text("# Impact numbers shown on the home page. Refresh with:  python3 update_stats.py   (or edit by hand)\n"
             + yaml.safe_dump(st, sort_keys=False, allow_unicode=True))
print("updated stats.yml:", "; ".join(changed) if changed else "no changes", f"(as of {st['as_of']})")

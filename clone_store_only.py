"""Clone just the Apple Store page."""
import os, re, sys, urllib.request, urllib.parse, ssl
from pathlib import Path

BASE_URL = 'https://www.apple.com'
OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def dl(url, lp):
    lp = Path(lp)
    lp.parent.mkdir(parents=True, exist_ok=True)
    if lp.exists():
        return True
    try:
        r = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(r, context=ctx, timeout=20) as resp:
            d = resp.read()
        lp.write_bytes(d)
        print(f'  OK: {lp.name}')
        return True
    except Exception as e:
        print(f'  FAIL: {url} -> {e}')
        return False

def resolve(href):
    if href.startswith('//'):  return 'https:' + href
    if href.startswith('/'):   return BASE_URL + href
    if href.startswith('http'): return href
    return urllib.parse.urljoin(BASE_URL, href)

def url2local(href):
    p = urllib.parse.urlparse(resolve(href)).path.lstrip('/')
    return OUT_DIR / (p or 'index.html')

def get_assets(html):
    s = set()
    for m in re.finditer(r'href="([^"]+\.css[^"]*)"', html):
        s.add(m.group(1).split('?')[0])
    for m in re.finditer(r'src="([^"]+\.js[^"]*)"', html):
        s.add(m.group(1).split('?')[0])
    for m in re.finditer(r'src="([^"]+\.(jpg|png|svg|webp|gif|avif)[^"]*)"', html, re.I):
        s.add(m.group(1).split('?')[0])
    for m in re.finditer(r'srcset="([^"]+)"', html, re.I):
        for part in m.group(1).split(','):
            u = part.strip().split(' ')[0].split('?')[0]
            if re.search(r'\.(jpg|png|svg|webp|gif|avif)$', u, re.I):
                s.add(u)
    return s

print('Downloading Apple Store page...')
req = urllib.request.Request('https://www.apple.com/store', headers=HEADERS)
with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    html = resp.read().decode('utf-8', 'ignore')

a = get_assets(html)
print(f'Found {len(a)} assets')
for x in a:
    dl(resolve(x), url2local(x))

# Fix font reference
html = html.replace('/wss/fonts?families=SF+Pro,v3|SF+Pro+Icons,v3', '/wss/fonts.css')

out = OUT_DIR / 'store' / 'index.html'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding='utf-8')
print(f'\nDone! Saved to: {out}')

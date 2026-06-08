"""
Clone every internal Apple page linked from the local homepage index.html.
This script downloads HTML pages and their CSS/JS/image assets into the
local project tree so homepage clicks resolve to local files instead of 404.
"""
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://www.apple.com"
OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

PAGE_LINK_EXTENSIONS = {
    '.html',
}
ASSET_EXTENSIONS = {
    '.css', '.js', '.jpg', '.jpeg', '.png', '.svg', '.webp', '.gif', '.avif', '.mp4', '.mov', '.webm', '.woff2', '.woff', '.ttf', '.otf', '.eot', '.json', '.pdf', '.xml'
}

SKIP_SCHEMES = ('javascript:', 'mailto:', 'tel:', 'data:')


def normalize_url(href):
    href = href.strip()
    if not href or href.startswith(SKIP_SCHEMES) or href.startswith('#'):
        return None
    if href.startswith('//'):
        return 'https:' + href
    if href.startswith('/'):
        return urllib.parse.urljoin(BASE_URL, href)
    if href.startswith('http://') or href.startswith('https://'):
        return href
    return None


def is_internal_html_link(href):
    url = normalize_url(href)
    if not url:
        return False
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc and 'apple.com' not in parsed.netloc:
        return False
    path = parsed.path or ''
    ext = os.path.splitext(path)[1].lower()
    if ext and ext not in PAGE_LINK_EXTENSIONS:
        return False
    return True


def link_save_path(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc and 'apple.com' not in parsed.netloc:
        return None

    path = parsed.path.lstrip('/')
    if not path:
        path = 'index.html'
    elif path.endswith('/'):
        path = path + 'index.html'
    elif not os.path.splitext(path)[1]:
        path = path + '/index.html'

    if path.endswith('/fonts') or path.endswith('wss/fonts'):
        path = path + '.css'

    return OUT_DIR / path


def download(url, local_path, skip_existing=True):
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if skip_existing and local_path.exists() and local_path.stat().st_size > 0:
        print(f'  SKIP: {local_path.relative_to(OUT_DIR)}')
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = resp.read()
        local_path.write_bytes(data)
        print(f'  OK: {local_path.relative_to(OUT_DIR)} ({len(data):,} bytes)')
        return True
    except Exception as exc:
        print(f'  FAIL: {url} -> {exc}')
        return False


def extract_assets(html, page_url):
    assets = set()

    # Stylesheets and font CSS endpoints.
    for m in re.finditer(r'<link[^>]+href="([^"]+)"', html, re.I):
        href = m.group(1).strip()
        if href.endswith('.css') or 'wss/fonts' in href or href.endswith('.woff2') or href.endswith('.woff') or href.endswith('.ttf') or href.endswith('.otf') or href.endswith('.eot'):
            assets.add(href)

    # Scripts
    for m in re.finditer(r'src="([^"]+\.js[^"]*)"', html, re.I):
        assets.add(m.group(1).split('?')[0])

    # Images
    for m in re.finditer(r'src="([^"]+\.(jpg|jpeg|png|svg|webp|gif|avif)[^"]*)"', html, re.I):
        assets.add(m.group(1).split('?')[0])

    # Srcset images
    for m in re.finditer(r'srcset="([^"]+)"', html, re.I):
        for part in m.group(1).split(','):
            url = part.strip().split(' ')[0].split('?')[0]
            if re.search(r'\.(jpg|jpeg|png|svg|webp|gif|avif)$', url, re.I):
                assets.add(url)

    # Video sources
    for m in re.finditer(r'src="([^"]+\.(mp4|mov|m4v|webm)[^"]*)"', html, re.I):
        assets.add(m.group(1).split('?')[0])

    # Inline style urls
    for m in re.finditer(r'url\(([
"""
Clone all Apple.com subpages (nav links) and save them locally.
Re-uses assets already downloaded; only fetches new ones.
"""
import os
import re
import sys
import urllib.request
import urllib.parse
import ssl
from pathlib import Path

BASE_URL = "https://www.apple.com"
OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# All Apple nav subpages: (remote_url, local_save_path)
PAGES = [
    ("https://www.apple.com/mac/",               "mac/index.html"),
    ("https://www.apple.com/ipad/",              "ipad/index.html"),
    ("https://www.apple.com/iphone/",            "iphone/index.html"),
    ("https://www.apple.com/watch/",             "watch/index.html"),
    ("https://www.apple.com/apple-vision-pro/",  "apple-vision-pro/index.html"),
    ("https://www.apple.com/airpods/",           "airpods/index.html"),
    ("https://www.apple.com/tv-home/",           "tv-home/index.html"),
    ("https://www.apple.com/entertainment/",     "entertainment/index.html"),
    ("https://www.apple.com/store",              "store/index.html"),
    # These redirect to support.apple.com - we download as-is
]

def download(url, local_path, skip_existing=True):
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if skip_existing and local_path.exists():
        print(f"  SKIP: {local_path.name}")
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            data = resp.read()
        local_path.write_bytes(data)
        print(f"  OK ({len(data)} bytes): {local_path}")
        return True
    except Exception as e:
        print(f"  FAIL: {url} -> {e}")
        return False

def resolve_url(href, page_url=BASE_URL):
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return BASE_URL + href
    if href.startswith("http"):
        return href
    return urllib.parse.urljoin(page_url, href)

def url_to_local(href):
    parsed = urllib.parse.urlparse(resolve_url(href))
    path = parsed.path.lstrip("/")
    if not path or path.endswith("/"):
        path = path + "index.html"
    return OUT_DIR / path

def extract_assets(html):
    assets = set()
    for m in re.finditer(r'href="([^"]+\.css[^"]*)"', html):
        assets.add(m.group(1).split("?")[0])
    for m in re.finditer(r'src="([^"]+\.js[^"]*)"', html):
        assets.add(m.group(1).split("?")[0])
    for m in re.finditer(r'src="([^"]+\.(jpg|jpeg|png|svg|webp|gif|avif)[^"]*)"', html, re.I):
        assets.add(m.group(1).split("?")[0])
    for m in re.finditer(r'srcset="([^"]+)"', html, re.I):
        for part in m.group(1).split(","):
            url = part.strip().split(" ")[0].split("?")[0]
            if re.search(r'\.(jpg|jpeg|png|svg|webp|gif|avif)$', url, re.I):
                assets.add(url)
    for m in re.finditer(r'url\((["\']?)([^)]+?)\1\)', html):
        url = m.group(2).split("?")[0]
        if not url.startswith("data:") and url.strip():
            assets.add(url)
    return assets

def extract_css_assets(css_content, css_url):
    assets = set()
    for m in re.finditer(r'url\((["\']?)([^)]+?)\1\)', css_content):
        ref = m.group(2).split("?")[0].strip()
        if ref.startswith("data:") or not ref:
            continue
        resolved = urllib.parse.urljoin(resolve_url(css_url), ref)
        assets.add(resolved)
    return assets

def clone_page(page_url, save_path):
    print(f"\n{'='*60}")
    print(f"Cloning: {page_url}")
    print(f"  -> {save_path}")
    print('='*60)

    # Download the HTML
    html_path = OUT_DIR / save_path
    temp_path = OUT_DIR / f"_temp_{save_path.replace('/', '_')}.html"

    try:
        req = urllib.request.Request(page_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            html_bytes = resp.read()
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path.write_bytes(html_bytes)
        html = html_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  FAILED to download HTML: {e}")
        return

    # Extract all assets
    assets = extract_assets(html)
    css_files = [a for a in assets if a.endswith(".css")]
    js_files = [a for a in assets if a.endswith(".js")]
    img_files = [a for a in assets if not a.endswith(".css") and not a.endswith(".js")]

    print(f"  Found: {len(css_files)} CSS, {len(js_files)} JS, {len(img_files)} images")

    # Download CSS and parse for sub-assets
    css_sub_assets = set()
    for css in css_files:
        local = url_to_local(css)
        if download(resolve_url(css), local):
            try:
                css_content = local.read_text(encoding="utf-8", errors="ignore")
                css_sub_assets.update(extract_css_assets(css_content, css))
            except Exception:
                pass

    # Download JS
    for js in js_files:
        download(resolve_url(js), url_to_local(js))

    # Download images
    for img in img_files:
        download(resolve_url(img), url_to_local(img))

    # Download CSS sub-assets (fonts, icons, bg images)
    print(f"  Downloading {len(css_sub_assets)} CSS sub-assets...")
    for asset in css_sub_assets:
        download(asset, url_to_local(asset))

    # Fix font CSS reference and save
    font_url = "/wss/fonts?families=SF+Pro,v3|SF+Pro+Icons,v3"
    html = html.replace(font_url, "/wss/fonts.css")

    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")

    # Clean up temp file
    if temp_path.exists():
        os.remove(temp_path)

    print(f"  Saved: {html_path}")

def main():
    try:
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass

    print(f"Apple Clone - Downloading {len(PAGES)} subpages")
    print(f"Output directory: {OUT_DIR}")

    for page_url, save_path in PAGES:
        clone_page(page_url, save_path)

    print("\n\nAll pages cloned successfully!")
    print("Serve with: python -m http.server 8001")

if __name__ == "__main__":
    main()

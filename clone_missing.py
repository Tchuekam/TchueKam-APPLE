"""
Clone all MISSING Apple.com subpages and their assets.
Skips pages already downloaded. Handles video sources too.
"""
import os
import re
import sys
import urllib.request
import urllib.parse
import ssl
import time
from pathlib import Path

BASE_URL = "https://www.apple.com"
OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}

# Pages to clone: (remote_url, local_save_path)
# Only pages that are MISSING or incomplete
PAGES = [
    ("https://www.apple.com/iphone/",            "iphone/index.html"),
    ("https://www.apple.com/watch/",             "watch/index.html"),
    ("https://www.apple.com/apple-vision-pro/",  "apple-vision-pro/index.html"),
    ("https://www.apple.com/airpods/",           "airpods/index.html"),
    ("https://www.apple.com/tv-home/",           "tv-home/index.html"),
    ("https://www.apple.com/entertainment/",     "entertainment/index.html"),
    ("https://www.apple.com/shop/buy-iphone/",   "shop/buy-iphone/index.html"),
    ("https://www.apple.com/us/shop/goto/store", "us/shop/goto/store/index.html"),
]


def download(url, local_path, skip_existing=True):
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if skip_existing and local_path.exists() and local_path.stat().st_size > 0:
        print(f"  SKIP: {local_path.relative_to(OUT_DIR)}")
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            data = resp.read()
        local_path.write_bytes(data)
        print(f"  OK ({len(data):,} bytes): {local_path.relative_to(OUT_DIR)}")
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
    # Only handle apple.com assets
    if parsed.netloc and "apple.com" not in parsed.netloc:
        return None
    path = parsed.path.lstrip("/")
    if not path or path.endswith("/"):
        path = path + "index.html"
    # Remove query strings
    return OUT_DIR / path


def extract_assets(html, page_url=BASE_URL):
    """Extract ALL asset URLs from HTML including video sources."""
    assets = set()

    # CSS
    for m in re.finditer(r'href="([^"]+\.css[^"]*)"', html):
        assets.add(m.group(1).split("?")[0])

    # JS
    for m in re.finditer(r'src="([^"]+\.js[^"]*)"', html):
        assets.add(m.group(1).split("?")[0])

    # Images (src attribute)
    for m in re.finditer(r'src="([^"]+\.(jpg|jpeg|png|svg|webp|gif|avif)[^"]*)"', html, re.I):
        assets.add(m.group(1).split("?")[0])

    # Images (srcset)
    for m in re.finditer(r'srcset="([^"]+)"', html, re.I):
        for part in m.group(1).split(","):
            url = part.strip().split(" ")[0].split("?")[0]
            if re.search(r'\.(jpg|jpeg|png|svg|webp|gif|avif)$', url, re.I):
                assets.add(url)

    # Video sources
    for m in re.finditer(r'src="([^"]+\.(mp4|mov|m4v|webm)[^"]*)"', html, re.I):
        assets.add(m.group(1).split("?")[0])

    # data-src (lazy-loaded)
    for m in re.finditer(r'data-src="([^"]+\.(jpg|jpeg|png|svg|webp|gif|avif|mp4|mov|webm)[^"]*)"', html, re.I):
        assets.add(m.group(1).split("?")[0])

    # Inline style url()
    for m in re.finditer(r'url\((["\']?)([^)]+?)\1\)', html):
        url = m.group(2).split("?")[0]
        if not url.startswith("data:") and url.strip():
            assets.add(url)

    # JSON data-attributes with image URLs (Apple uses these heavily)
    for m in re.finditer(r'"src":"([^"]+\.(jpg|jpeg|png|webp|avif)[^"]*)"', html, re.I):
        assets.add(m.group(1).split("?")[0])
    for m in re.finditer(r'"url":"(https?://[^"]+\.(jpg|jpeg|png|webp|avif|mp4|mov)[^"]*)"', html, re.I):
        assets.add(m.group(1).split("?")[0])

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
    html_path = OUT_DIR / save_path

    # Check if already fully cloned
    if html_path.exists() and html_path.stat().st_size > 10000:
        print(f"\n  ALREADY DONE: {save_path} ({html_path.stat().st_size:,} bytes)")
        return

    print(f"\n{'='*65}")
    print(f"  Cloning: {page_url}")
    print(f"  Saving to: {save_path}")
    print('='*65)

    # Download the HTML
    temp_path = OUT_DIR / f"_temp_{save_path.replace('/', '_')}.html"

    try:
        req = urllib.request.Request(page_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            html_bytes = resp.read()
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path.write_bytes(html_bytes)
        html = html_bytes.decode("utf-8", errors="ignore")
        print(f"  HTML downloaded: {len(html_bytes):,} bytes")
    except Exception as e:
        print(f"  FAILED to download HTML: {e}")
        return

    # Extract all assets
    assets = extract_assets(html, page_url)
    css_files = [a for a in assets if a.endswith(".css")]
    js_files = [a for a in assets if a.endswith(".js")]
    video_files = [a for a in assets if re.search(r'\.(mp4|mov|m4v|webm)$', a, re.I)]
    img_files = [a for a in assets if not a.endswith(".css") and not a.endswith(".js") and not re.search(r'\.(mp4|mov|m4v|webm)$', a, re.I)]

    print(f"  Found: {len(css_files)} CSS, {len(js_files)} JS, {len(img_files)} images, {len(video_files)} videos")

    # Download CSS and parse for sub-assets
    css_sub_assets = set()
    print(f"\n  --- CSS ({len(css_files)}) ---")
    for css in sorted(css_files):
        local = url_to_local(css)
        if local is None:
            continue
        if download(resolve_url(css), local):
            try:
                css_content = local.read_text(encoding="utf-8", errors="ignore")
                css_sub_assets.update(extract_css_assets(css_content, css))
            except Exception:
                pass

    # Download JS
    print(f"\n  --- JS ({len(js_files)}) ---")
    for js in sorted(js_files):
        local = url_to_local(js)
        if local is None:
            continue
        download(resolve_url(js), local)

    # Download images
    print(f"\n  --- Images ({len(img_files)}) ---")
    for img in sorted(img_files):
        local = url_to_local(img)
        if local is None:
            continue
        download(resolve_url(img), local)

    # Download videos
    if video_files:
        print(f"\n  --- Videos ({len(video_files)}) ---")
        for vid in sorted(video_files):
            local = url_to_local(vid)
            if local is None:
                continue
            download(resolve_url(vid), local)

    # Download CSS sub-assets (fonts, icons, bg images)
    print(f"\n  --- CSS Sub-assets ({len(css_sub_assets)}) ---")
    for asset in sorted(css_sub_assets):
        local = url_to_local(asset)
        if local is None:
            continue
        download(asset, local)

    # Fix font CSS reference
    font_url_param = "/wss/fonts?families=SF+Pro,v3|SF+Pro+Icons,v3"
    html = html.replace(font_url_param, "/wss/fonts.css")

    # Save final HTML
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")
    print(f"\n  Saved HTML: {html_path.relative_to(OUT_DIR)}")

    # Clean temp file
    if temp_path.exists():
        try:
            os.remove(temp_path)
        except Exception:
            pass

    time.sleep(0.5)  # Be polite to Apple's servers


def ensure_font_css():
    """Make sure font CSS and fonts are downloaded."""
    font_css_path = OUT_DIR / "wss" / "fonts.css"
    if font_css_path.exists():
        return

    print("\n=== Downloading Apple Font CSS ===")
    font_url = BASE_URL + "/wss/fonts?families=SF+Pro,v3|SF+Pro+Icons,v3"
    try:
        req = urllib.request.Request(font_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            font_css = resp.read()
        font_css_path.parent.mkdir(parents=True, exist_ok=True)
        font_css_path.write_bytes(font_css)
        print(f"  OK: wss/fonts.css")

        font_css_text = font_css.decode("utf-8", errors="ignore")
        font_assets = set()
        for m in re.finditer(r'url\((["\']?)([^)]+?)\1\)', font_css_text):
            ref = m.group(2).split("?")[0].strip()
            if not ref.startswith("data:") and ref:
                resolved = urllib.parse.urljoin(BASE_URL + "/wss/fonts.css", ref)
                font_assets.add(resolved)

        print(f"  Found {len(font_assets)} font files")
        for fa in sorted(font_assets):
            local = url_to_local(fa)
            if local:
                download(fa, local)
    except Exception as e:
        print(f"  Font download failed: {e}")


def main():
    try:
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass

    print("Apple Clone - Missing Pages Downloader")
    print(f"Output: {OUT_DIR}")
    print(f"Pages to check: {len(PAGES)}")

    ensure_font_css()

    for page_url, save_path in PAGES:
        clone_page(page_url, save_path)

    # Clean up any leftover temp files
    print("\n=== Cleaning up temp files ===")
    for tmp in OUT_DIR.glob("_temp_*.html"):
        print(f"  Removing: {tmp.name}")
        tmp.unlink()

    print("\n\nAll missing pages cloned!")
    print("Serve with: python -m http.server 8001")
    print(f"Then open: http://localhost:8001/")


if __name__ == "__main__":
    main()

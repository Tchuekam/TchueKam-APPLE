"""
Clone a subpage of Apple (like Apple Store) and save it to a specific local path.
Downloads new assets relative to the root apple-clone folder.
"""
import os
import re
import sys
import urllib.request
import urllib.parse
import ssl
from pathlib import Path

# Target details
PAGE_URL = "https://www.apple.com/store"
SAVE_PATH = "us/shop/goto/store/index.html"

BASE_URL = "https://www.apple.com"
OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Skip SSL verification
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download(url, local_path):
    """Download a URL to a local path, creating directories as needed."""
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    if local_path.exists():
        print(f"  SKIP (exists): {local_path}")
        return True
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = resp.read()
        local_path.write_bytes(data)
        print(f"  OK: {local_path} ({len(data)} bytes)")
        return True
    except Exception as e:
        print(f"  FAIL: {url} -> {e}")
        return False

def resolve_url(href, base=PAGE_URL):
    """Turn a relative URL into an absolute one."""
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return BASE_URL + href
    if href.startswith("http"):
        return href
    return urllib.parse.urljoin(base, href)

def url_to_local(href):
    """Convert a URL to a local file path inside the main project directory."""
    parsed = urllib.parse.urlparse(resolve_url(href))
    path = parsed.path.lstrip("/")
    if not path:
        path = "index.html"
    return OUT_DIR / path

def extract_assets(html):
    """Extract CSS, JS, image, and font URLs from HTML."""
    assets = set()
    
    # CSS files
    for m in re.finditer(r'href="([^"]+\.css[^"]*)"', html):
        assets.add(m.group(1).split("?")[0])
    
    # JS files  
    for m in re.finditer(r'src="([^"]+\.js[^"]*)"', html):
        assets.add(m.group(1).split("?")[0])
    
    # Images (src and srcset)
    for m in re.finditer(r'src="([^"]+\.(jpg|jpeg|png|svg|webp|gif|avif)[^"]*)"', html, re.I):
        assets.add(m.group(1).split("?")[0])
    for m in re.finditer(r'srcset="([^"]+)"', html, re.I):
        for part in m.group(1).split(","):
            url = part.strip().split(" ")[0].split("?")[0]
            if re.search(r'\.(jpg|jpeg|png|svg|webp|gif|avif)$', url, re.I):
                assets.add(url)
    
    # Background images in inline styles
    for m in re.finditer(r'url\((["\']?)([^)]+?)\1\)', html):
        url = m.group(2).split("?")[0]
        if not url.startswith("data:"):
            assets.add(url)
    
    return assets

def extract_css_assets(css_content, css_url):
    """Extract image/font URLs referenced inside CSS files."""
    assets = set()
    for m in re.finditer(r'url\((["\']?)([^)]+?)\1\)', css_content):
        ref = m.group(2).split("?")[0].strip()
        if ref.startswith("data:") or not ref:
            continue
        resolved = urllib.parse.urljoin(resolve_url(css_url), ref)
        assets.add(resolved)
    return assets

def main():
    # Setup console encoding
    try:
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass

    target_html_path = OUT_DIR / SAVE_PATH
    print(f"Downloading {PAGE_URL} ...")
    temp_path = OUT_DIR / "temp_store.html"
    download(PAGE_URL, temp_path)
    
    if not temp_path.exists():
        print("Failed to download store page HTML")
        return
        
    html = temp_path.read_text(encoding="utf-8", errors="ignore")
    
    print("\n=== Extracting asset URLs from Store HTML ===")
    assets = extract_assets(html)
    print(f"Found {len(assets)} assets in HTML")
    
    css_files = [a for a in assets if a.endswith(".css")]
    js_files = [a for a in assets if a.endswith(".js")]
    img_files = [a for a in assets if not a.endswith(".css") and not a.endswith(".js")]
    
    print(f"\n=== Downloading {len(css_files)} CSS files ===")
    css_sub_assets = set()
    for css in css_files:
        full_url = resolve_url(css)
        local = url_to_local(css)
        if download(full_url, local):
            try:
                css_content = local.read_text(encoding="utf-8", errors="ignore")
                sub = extract_css_assets(css_content, css)
                css_sub_assets.update(sub)
            except Exception as e:
                print(f"  Error parsing CSS {css}: {e}")
    
    print(f"\n=== Downloading {len(js_files)} JS files ===")
    for js in js_files:
        download(resolve_url(js), url_to_local(js))
    
    print(f"\n=== Downloading {len(img_files)} images from HTML ===")
    for img in img_files:
        download(resolve_url(img), url_to_local(img))
    
    print(f"\n=== Downloading {len(css_sub_assets)} assets from CSS (fonts, bg images) ===")
    for asset in css_sub_assets:
        download(resolve_url(asset), url_to_local(asset))
        
    # Re-write the font references
    font_url = "/wss/fonts?families=SF+Pro,v3|SF+Pro+Icons,v3"
    html = html.replace(font_url, "/wss/fonts.css")
    
    # Save the file
    target_html_path.parent.mkdir(parents=True, exist_ok=True)
    target_html_path.write_text(html, encoding="utf-8")
    
    # Clean up temp file
    if temp_path.exists():
        os.remove(temp_path)
        
    print(f"\nClone complete! Store subpage is now at: {target_html_path}")

if __name__ == "__main__":
    main()

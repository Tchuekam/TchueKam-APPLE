"""
Script to rewrite all absolute or relative links to apple.com in the downloaded
HTML files so that they point to their corresponding local files on localhost.
"""
import os
import re
from pathlib import Path

OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the mapping from Apple.com URLs/paths to local files
MAPPING = {
    # Home/Root
    r'https?://(?:www\.)?apple\.com/?$': '/index.html',
    r'^/$': '/index.html',

    # Main categories
    r'https?://(?:www\.)?apple\.com/store/?$': '/store/index.html',
    r'^/store/?$': '/store/index.html',
    
    r'https?://(?:www\.)?apple\.com/mac/?$': '/mac/index.html',
    r'^/mac/?$': '/mac/index.html',
    
    r'https?://(?:www\.)?apple\.com/ipad/?$': '/ipad/index.html',
    r'^/ipad/?$': '/ipad/index.html',
    
    r'https?://(?:www\.)?apple\.com/iphone/?$': '/iphone/index.html',
    r'^/iphone/?$': '/iphone/index.html',
    
    r'https?://(?:www\.)?apple\.com/watch/?$': '/watch/index.html',
    r'^/watch/?$': '/watch/index.html',
    
    r'https?://(?:www\.)?apple\.com/apple-vision-pro/?$': '/apple-vision-pro/index.html',
    r'^/apple-vision-pro/?$': '/apple-vision-pro/index.html',
    
    r'https?://(?:www\.)?apple\.com/airpods/?$': '/airpods/index.html',
    r'^/airpods/?$': '/airpods/index.html',
    
    r'https?://(?:www\.)?apple\.com/tv-home/?$': '/tv-home/index.html',
    r'^/tv-home/?$': '/tv-home/index.html',
    
    r'https?://(?:www\.)?apple\.com/entertainment/?$': '/entertainment/index.html',
    r'^/entertainment/?$': '/entertainment/index.html',
    
    # Store sub links
    r'https?://(?:www\.)?apple\.com/us/shop/goto/store/?$': '/us/shop/goto/store/index.html',
    r'^/us/shop/goto/store/?$': '/us/shop/goto/store/index.html',
    
    r'https?://(?:www\.)?apple\.com/shop/buy-iphone/?$': '/shop/buy-iphone/index.html',
    r'^/shop/buy-iphone/?$': '/shop/buy-iphone/index.html',
}

def rewrite_html_file(file_path):
    print(f"Processing: {file_path.relative_to(OUT_DIR)}")
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  Failed to read file: {e}")
        return

    original = content

    # Find href="..." attributes
    def replacer(match):
        href = match.group(1)
        # Check against our mapping
        for pattern, local_path in MAPPING.items():
            if re.match(pattern, href):
                # We need to make the path relative to the file_path to support running from any directory level,
                # or absolute from the root (e.g. starting with /). Since we serve from python -m http.server 8001,
                # absolute paths starting with / work perfectly because / is the directory where the server started.
                return f'href="{local_path}"'
        
        # If it's another apple.com link that we didn't map, let's redirect it if we have it locally,
        # or leave it if we don't.
        if href.startswith('https://www.apple.com/') or href.startswith('/'):
            path_part = href.replace('https://www.apple.com', '').split('?')[0].split('#')[0].strip('/')
            potential_local = OUT_DIR / path_part / 'index.html'
            if potential_local.exists():
                return f'href="/{path_part}/index.html"'
                
        return match.group(0)

    # Rewrite href attributes
    content = re.sub(r'href="([^"]+)"', replacer, content)

    if content != original:
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  SUCCESS: Rewrote links in {file_path.name}")
        except Exception as e:
            print(f"  Failed to write file: {e}")
    else:
        print(f"  No changes needed in {file_path.name}")

def main():
    # Find all index.html files in the directory tree
    html_files = list(OUT_DIR.glob('**/index.html'))
    if (OUT_DIR / 'index.html') not in html_files and (OUT_DIR / 'index.html').exists():
        html_files.append(OUT_DIR / 'index.html')
        
    # Deduplicate
    html_files = list(set(html_files))

    print(f"Found {len(html_files)} HTML files to rewrite.")
    for f in html_files:
        rewrite_html_file(f)

    print("\nLink rewriting completed!")

if __name__ == "__main__":
    main()

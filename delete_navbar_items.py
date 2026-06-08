import os
import re
from pathlib import Path

OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Pattern to match <div class="... globalnav-item-mac ...">...</div> or <li class="...">...</li>
NAV_ITEM_PATTERN = r'<(div|li)\b[^>]*?globalnav-item-(mac|ipad|watch|accessories|support)\b[^>]*?>.*?</\1>'

def remove_items_from_file(file_path):
    print(f"Removing navbar items in: {file_path.relative_to(OUT_DIR)}")
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  Failed to read file: {e}")
        return

    original = content

    # Perform the deletion
    content, count = re.subn(NAV_ITEM_PATTERN, '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Also clean up the injected style block we added earlier (if present)
    style_pattern = r'\s*<style>\s*\.globalnav-item-mac,\s*\.globalnav-item-ipad,\s*\.globalnav-item-watch,\s*\.globalnav-item-accessories,\s*\.globalnav-item-support\s*{\s*display:\s*none\s*!important;\s*}\s*</style>'
    content, style_count = re.subn(style_pattern, '', content, flags=re.IGNORECASE)

    if count > 0 or style_count > 0:
        print(f"  Removed {count} navbar tags and {style_count} style blocks.")

    if content != original:
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  SUCCESS: Updated {file_path.name}")
        except Exception as e:
            print(f"  Failed to write file: {e}")
    else:
        print(f"  No updates needed for {file_path.name}")

def main():
    html_files = list(OUT_DIR.glob('**/index.html'))
    if (OUT_DIR / 'index.html') not in html_files and (OUT_DIR / 'index.html').exists():
        html_files.append(OUT_DIR / 'index.html')
        
    html_files = list(set(html_files))

    print(f"Found {len(html_files)} HTML files to update.")
    for f in html_files:
        remove_items_from_file(f)

if __name__ == "__main__":
    main()

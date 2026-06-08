import os
import re
from pathlib import Path

OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

def clean_file(file_path):
    print(f"Cleaning placeholders in: {file_path.relative_to(OUT_DIR)}")
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  Failed to read file: {e}")
        return

    original = content

    # Regex to remove <source> elements whose srcset contains data:image/gif;base64
    # This matches both single and double quotes, and matches across multiple lines/attributes inside the tag.
    pattern = r'<source\b[^>]*?srcset=["\']data:image/gif;base64,[^"\']*?["\'][^>]*?>'
    content, count = re.subn(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)

    if count > 0:
        print(f"  Removed {count} placeholder <source> elements.")

    if content != original:
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  SUCCESS: Cleaned {file_path.name}")
        except Exception as e:
            print(f"  Failed to write file: {e}")
    else:
        print(f"  No placeholders found in {file_path.name}")

def main():
    html_files = list(OUT_DIR.glob('**/index.html'))
    if (OUT_DIR / 'index.html') not in html_files and (OUT_DIR / 'index.html').exists():
        html_files.append(OUT_DIR / 'index.html')
        
    html_files = list(set(html_files))

    print(f"Found {len(html_files)} HTML files to scan.")
    for f in html_files:
        clean_file(f)

if __name__ == "__main__":
    main()

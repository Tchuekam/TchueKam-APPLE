"""
Script to remove specific footer disclaimer paragraphs across all cloned HTML files.
"""
import os
import re
import sys
from pathlib import Path

OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# List of text pieces or sentences to search for and remove.
# We will check if any paragraph or element contains these and remove them.
TARGETS = [
    "Subject to credit approval. The cost of AirPods Pro 3",
    "Goldman Sachs will share certain Apple transaction information",
    "Offer not available to Apple Card Family members",
    "You can choose to direct Daily Cash to a Savings account",
    "Apple Payments Services LLC",
    "To access and use all Apple Card features and products",
    "All communications from Apple and Goldman Sachs Bank USA",
    "Trade-in values will vary based on the condition",
    "Trade\u2011in values will vary based on the condition",
    "A subscription is required for Apple Arcade",
    "Features are subject to change. Some features, applications"
]

def clean_html_file(file_path):
    # Print to console using UTF-8 to handle dash characters
    sys.stdout.write(f"Cleaning: {file_path.relative_to(OUT_DIR)}\n")
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        sys.stdout.write(f"  Failed to read file: {e}\n")
        return

    original = content

    for target in TARGETS:
        # Construct search regex using the first few words to identify the container block
        words = target.split()
        if not words:
            continue
        
        # Build flexible regex matching tags containing these words
        escaped_words = [re.escape(w) for w in words[:4]]
        regex_pattern = r'<(p|li|span|div)[^>]*?>[^<]*?' + r'[^<]*?'.join(escaped_words) + r'.*?<\/\1>'
        
        try:
            content, count = re.subn(regex_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
            if count > 0:
                sys.stdout.write(f"  Removed {count} elements matching pattern.\n")
        except Exception as e:
            sys.stdout.write(f"  Regex error: {e}\n")

    if content != original:
        try:
            file_path.write_text(content, encoding='utf-8')
            sys.stdout.write(f"  SUCCESS: Saved cleaned {file_path.name}\n")
        except Exception as e:
            sys.stdout.write(f"  Failed to write file: {e}\n")
    else:
        sys.stdout.write(f"  No changes made in {file_path.name}\n")

def main():
    try:
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass

    html_files = list(OUT_DIR.glob('**/index.html'))
    if (OUT_DIR / 'index.html') not in html_files and (OUT_DIR / 'index.html').exists():
        html_files.append(OUT_DIR / 'index.html')
        
    html_files = list(set(html_files))

    sys.stdout.write(f"Found {len(html_files)} HTML files to scan and clean.\n")
    for f in html_files:
        clean_html_file(f)

    sys.stdout.write("\nFooter disclaimer text cleaning completed!\n")

if __name__ == "__main__":
    main()

import os
from pathlib import Path

OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

HIDE_STYLE = """\t<style>
\t\t.globalnav-item-mac,
\t\t.globalnav-item-ipad,
\t\t.globalnav-item-watch,
\t\t.globalnav-item-accessories,
\t\t.globalnav-item-support {
\t\t\tdisplay: none !important;
\t\t}
\t</style>
</head>"""

def modify_file(file_path):
    print(f"Modifying navbar in: {file_path.relative_to(OUT_DIR)}")
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  Failed to read file: {e}")
        return

    if ".globalnav-item-mac" in content:
        print("  Style already applied to this file.")
        return

    original = content
    # Replace the closing </head> tag with our custom styles and the tag
    content = content.replace("</head>", HIDE_STYLE)

    if content != original:
        try:
            file_path.write_text(content, encoding='utf-8')
            print(f"  SUCCESS: Updated navbar in {file_path.name}")
        except Exception as e:
            print(f"  Failed to write file: {e}")
    else:
        print(f"  No changes made to {file_path.name}")

def main():
    html_files = list(OUT_DIR.glob('**/index.html'))
    if (OUT_DIR / 'index.html') not in html_files and (OUT_DIR / 'index.html').exists():
        html_files.append(OUT_DIR / 'index.html')
        
    html_files = list(set(html_files))

    print(f"Found {len(html_files)} HTML files to update.")
    for f in html_files:
        modify_file(f)

if __name__ == "__main__":
    main()

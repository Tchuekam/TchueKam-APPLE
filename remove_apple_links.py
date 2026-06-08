"""
Script to remove all Apple external links and replace them with user's links
"""
import os
import re
from pathlib import Path

OUT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# User's links
USER_LINKS = {
    'linkedin': 'https://www.linkedin.com/in/tchuekam-rostand/',
    'youtube': 'https://www.youtube.com/@Giantech-Empire',
    'phone': '+237659248952',
    'phone_alt': '+237653683174',
    'portfolio1': 'https://tchuekam-agent.netlify.app/',
    'portfolio2': 'https://tchuekamui-sovereign.vercel.app/',
}

def remove_apple_links(content):
    """Remove or replace all Apple links"""
    
    # 1. Remove all hreflang alternate links (they're huge and point to apple.com)
    content = re.sub(r'<link rel="alternate" href="https://www\.apple\.com/[^"]*" hreflang="[^"]*" />', '', content)
    
    # 2. Remove multiple whitespace that was left behind
    content = re.sub(r'\s+', ' ', content)
    
    # 3. Replace Apple social media links with user's
    # Instagram/Facebook/X/Twitter links pointing to @apple
    content = re.sub(
        r'href=["\']https://(?:www\.)?(?:instagram|facebook|twitter|x)\.com/apple["\']',
        f'href="{USER_LINKS["linkedin"]}"',
        content,
        flags=re.IGNORECASE
    )
    
    # 4. Replace YouTube Apple channel with user's YouTube
    content = re.sub(
        r'href=["\']https://(?:www\.)?youtube\.com/(?:channel/|@)?apple[^"\']*["\']',
        f'href="{USER_LINKS["youtube"]}"',
        content,
        flags=re.IGNORECASE
    )
    
    # 5. Replace support.apple.com links with #
    content = re.sub(
        r'href=["\']https://support\.apple\.com/[^"\']*["\']',
        'href="#"',
        content,
        flags=re.IGNORECASE
    )
    
    # 6. Replace icloud.com with #
    content = re.sub(
        r'href=["\']https://(?:www\.)?icloud\.com/[^"\']*["\']',
        'href="#"',
        content,
        flags=re.IGNORECASE
    )
    
    # 7. Replace apps.apple.com (App Store) with #
    content = re.sub(
        r'href=["\']https://apps\.apple\.com/[^"\']*["\']',
        'href="#"',
        content,
        flags=re.IGNORECASE
    )
    
    # 8. Replace any remaining apple.com links with #
    content = re.sub(
        r'href=["\']https://(?:www\.)?apple\.com/[^"\']*["\']',
        'href="#"',
        content,
        flags=re.IGNORECASE
    )
    
    # 9. Remove Apple's tracking/analytics scripts
    content = re.sub(
        r'<script[^>]*src=["\']https://[^"\']*apple[^"\']*["\'][^>]*></script>',
        '',
        content,
        flags=re.IGNORECASE
    )
    
    # 10. Remove Apple Privacy/Terms links that might be in footer
    content = re.sub(
        r'<a[^>]*href=["\']https://www\.apple\.com/(?:privacy|terms|legal)[^"\']*["\'][^>]*>.*?</a>',
        '',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    return content

def process_html_file(file_path):
    print(f"Processing: {file_path.relative_to(OUT_DIR)}")
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  ❌ Failed to read file: {e}")
        return False

    original = content
    modified = remove_apple_links(content)

    if modified != original:
        try:
            file_path.write_text(modified, encoding='utf-8')
            # Count replacements
            removed_hreflang = len(re.findall(r'<link rel="alternate" href="https://www\.apple\.com/', original))
            print(f"  ✅ Cleaned {removed_hreflang} hreflang links + other Apple references")
            return True
        except Exception as e:
            print(f"  ❌ Failed to write file: {e}")
            return False
    else:
        print(f"  ⏭️  No Apple links found")
        return False

def main():
    # Find all index.html files
    html_files = list(OUT_DIR.glob('**/index.html'))
    if (OUT_DIR / 'index.html') not in html_files and (OUT_DIR / 'index.html').exists():
        html_files.append(OUT_DIR / 'index.html')
    
    html_files = list(set(html_files))
    
    print(f"🔍 Found {len(html_files)} HTML files\n")
    print("=" * 60)
    print("User's Links to Use:")
    print("=" * 60)
    for key, value in USER_LINKS.items():
        print(f"  {key}: {value}")
    print("=" * 60)
    print()
    
    success_count = 0
    for f in html_files:
        if process_html_file(f):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ Completed! Modified {success_count}/{len(html_files)} files")
    print("=" * 60)

if __name__ == "__main__":
    main()

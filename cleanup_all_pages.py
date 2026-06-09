#!/usr/bin/env python3
"""
Comprehensive Apple Link Cleanup Script
Removes all Apple-specific links and metadata from cloned HTML files
"""

import os
import re
from pathlib import Path

# Configuration
PERSON_NAME = "Tchuekam Rostand"
LINKEDIN = "https://www.linkedin.com/in/tchuekam-rostand/"
YOUTUBE = "https://www.youtube.com/@Giantech-Empire"
PORTFOLIO1 = "https://tchuekam-agent.netlify.app/"
PORTFOLIO2 = "https://tchuekamui-sovereign.vercel.app/"
PHONE1 = "+237659248952"
PHONE2 = "+237653683174"

def find_html_files(root_dir="."):
    """Find all index.html files recursively"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if "index.html" in files:
            html_files.append(os.path.join(root, "index.html"))
    return sorted(html_files)

def remove_hreflang_links(content):
    """Remove all hreflang alternate links except en-US"""
    # Remove all hreflang links
    content = re.sub(
        r'<link rel="alternate" href="https://www\.apple\.com/[^"]*" hreflang="[^"]*" */?>\s*',
        '',
        content
    )
    # Keep single en-US hreflang
    content = re.sub(
        r'<link rel="alternate" href="\./[^"]*" hreflang="en-US" />(\s*<link rel="alternate")',
        r'<link rel="alternate" href="./index.html" hreflang="en-US" />\n\1',
        content
    )
    return content

def replace_external_links(content):
    """Replace external Apple service links with #"""
    replacements = [
        (r'href="https://support\.apple\.com/[^"]*"', 'href="#"'),
        (r'href="https://www\.icloud\.com/[^"]*"', 'href="#"'),
        (r'href="https://apps\.apple\.com/[^"]*"', 'href="#"'),
        (r'href="https://www\.apple\.com/[^"]*"', 'href="#"'),
        (r'href="https://learn\.applecard\.apple/[^"]*"', 'href="#"'),
        (r'href="https://tv\.apple\.com/[^"]*"', 'href="#"'),
    ]
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    return content

def update_social_links(content):
    """Update social media links to personal profiles"""
    replacements = [
        (r'href="https://instagram\.com/apple"', f'href="{LINKEDIN}"'),
        (r'href="https://twitter\.com/apple"', f'href="{LINKEDIN}"'),
        (r'href="https://facebook\.com/apple"', f'href="{LINKEDIN}"'),
        (r'href="https://youtube\.com/@apple"', f'href="{YOUTUBE}"'),
        (r'href="https://www\.youtube\.com/@apple"', f'href="{YOUTUBE}"'),
        (r'href="https://instagram\.com/Apple"', f'href="{LINKEDIN}"'),
        (r'href="https://twitter\.com/Apple"', f'href="{LINKEDIN}"'),
        (r'href="https://facebook\.com/Apple"', f'href="{LINKEDIN}"'),
    ]
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    return content

def remove_tracking_scripts(content):
    """Remove Apple tracking and analytics scripts"""
    # Remove ac-target scripts
    content = re.sub(
        r'<script[^>]*src="[^"]*ac-target[^"]*"[^>]*></script>\s*',
        '',
        content,
        flags=re.IGNORECASE
    )
    # Remove metrics scripts
    content = re.sub(
        r'<script[^>]*src="[^"]*metrics/[^"]*"[^>]*></script>\s*',
        '',
        content,
        flags=re.IGNORECASE
    )
    return content

def update_og_metadata(content):
    """Update Open Graph metadata"""
    replacements = [
        (r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{PERSON_NAME}"'),
        (r'<meta property="og:site_name" content="Apple"', f'<meta property="og:site_name" content="{PERSON_NAME}"'),
        (r'<meta property="og:url" content="https://www\.apple\.com/[^"]*"', '<meta property="og:url" content="./"'),
    ]
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    return content

def update_page_title(content, filename):
    """Update page title if it's generic"""
    # Only update generic titles
    if re.search(r'<title>Apple</title>', content):
        content = re.sub(
            r'<title>Apple</title>',
            f'<title>{PERSON_NAME} - Tech Portfolio</title>',
            content
        )
    elif re.search(r'<title>([A-Za-z\s]+) - Apple</title>', content):
        content = re.sub(
            r'<title>([A-Za-z\s]+) - Apple</title>',
            f'<title>\\1 - {PERSON_NAME}</title>',
            content
        )
    return content

def cleanup_file(filepath):
    """Apply all cleanup operations to a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_size = len(content)
        
        # Apply all cleanup operations
        content = remove_hreflang_links(content)
        content = replace_external_links(content)
        content = update_social_links(content)
        content = remove_tracking_scripts(content)
        content = update_og_metadata(content)
        content = update_page_title(content, filepath)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        new_size = len(content)
        size_reduction = original_size - new_size
        
        print(f"✅ {filepath}")
        print(f"   Size: {original_size:,} → {new_size:,} bytes (-{size_reduction:,})")
        return True
    except Exception as e:
        print(f"❌ {filepath}: {str(e)}")
        return False

def main():
    print("\n" + "="*70)
    print("APPLE CLONE - COMPREHENSIVE CLEANUP SCRIPT")
    print("="*70 + "\n")
    
    html_files = find_html_files()
    
    if not html_files:
        print("❌ No HTML files found!")
        return
    
    print(f"Found {len(html_files)} HTML file(s) to process:\n")
    for f in html_files:
        print(f"  - {f}")
    
    print("\n" + "-"*70)
    print("PROCESSING FILES...")
    print("-"*70 + "\n")
    
    successful = 0
    for html_file in html_files:
        if cleanup_file(html_file):
            successful += 1
    
    print("\n" + "="*70)
    print(f"CLEANUP COMPLETE: {successful}/{len(html_files)} files processed successfully")
    print("="*70)
    print("\n📋 CHANGES MADE:")
    print("  ✓ Removed ~200+ hreflang links per file")
    print("  ✓ Replaced external Apple links with #")
    print("  ✓ Updated social media links to your profiles")
    print("  ✓ Removed tracking scripts")
    print("  ✓ Updated Open Graph metadata")
    print("  ✓ Updated page titles")
    print("\n📝 STILL NEEDS MANUAL UPDATE:")
    print("  - Page descriptions (meta name=\"Description\")")
    print("  - Page content/branding text")
    print("  - Footer with your contact info")
    print("  - Product descriptions")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()

# Apple Links Removal & Personalization Guide

## Overview
Your cloned Apple website contains many external links pointing to Apple's services. This guide shows what needs to be replaced and how to do it.

---

## What Needs to be Removed/Replaced

### 1. **Hreflang Alternate Language Links** (HUGE - ~3KB per file)
**Location:** `<head>` section  
**Pattern:** `<link rel="alternate" href="https://www.apple.com/[country-code]/" hreflang="[lang]" />`  
**Files Affected:** All 12 index.html files  
**Action:** ✅ **REMOVE** (or replace with your own domain)

**Example - BEFORE:**
```html
<link rel="alternate" href="/index.html" hreflang="en-US" />
<link rel="alternate" href="https://www.apple.com/ae-ar/" hreflang="ar-AE" />
<link rel="alternate" href="https://www.apple.com/ae/" hreflang="en-AE" />
<!-- ... 200+ more lines ... -->
```

**Example - AFTER:**
```html
<link rel="alternate" href="/index.html" hreflang="en-US" />
```

---

### 2. **Open Graph (OG) Metadata**
**Location:** `<head>` section  
**Files Affected:** All HTML files  
**Action:** Replace with your own branding

**Replace:**
```html
<meta property="og:image" content="https://www.apple.com/ac/structured-data/images/open_graph_logo.png?202604211141" />
<meta property="og:title" content="Apple" />
<meta property="og:description" content="Discover the innovative world of Apple..." />
<meta property="og:url" content="https://www.apple.com/" />
<meta property="og:site_name" content="Apple" />
```

**With:**
```html
<!-- Remove og:image or use your own logo -->
<meta property="og:title" content="Your Site Name" />
<meta property="og:description" content="Your site description" />
<meta property="og:url" content="/" />
<meta property="og:site_name" content="Your Site Name" />
```

---

### 3. **External Apple URLs** (throughout pages)
**Types to replace:**

| Type | Pattern | Replace With | Reason |
|------|---------|--------------|--------|
| Support | `https://support.apple.com/...` | `#` | Dead link without Apple's support |
| iCloud | `https://www.icloud.com/...` | `#` | External service |
| App Store | `https://apps.apple.com/...` | `#` | External service |
| Main site | `https://www.apple.com/...` | `#` or local path | External domain |

---

### 4. **Social Media Links**
**Files:** Check footer and social sections  
**Replace:**

| From | To |
|------|---|
| `https://instagram.com/apple` | `https://www.linkedin.com/in/tchuekam-rostand/` |
| `https://twitter.com/apple` | `https://www.linkedin.com/in/tchuekam-rostand/` |
| `https://youtube.com/@apple` | `https://www.youtube.com/@Giantech-Empire` |
| `https://facebook.com/apple` | `https://www.linkedin.com/in/tchuekam-rostand/` |

---

### 5. **Contact Information**
**Add to footer/contact pages:**
- 📧 Email: (add your email)
- 📱 Phone: `+237659248952` or `+237653683174`
- 💼 LinkedIn: `https://www.linkedin.com/in/tchuekam-rostand/`
- 🎥 YouTube: `https://www.youtube.com/@Giantech-Empire`

---

### 6. **Portfolio/Personal Brand Links**
**Add to appropriate sections:**
- **Portfolio 1:** `https://tchuekam-agent.netlify.app/`
- **Portfolio 2:** `https://tchuekamui-sovereign.vercel.app/`

---

## How to Apply Changes

### **Option 1: Automatic Script (Recommended)**
1. Open **Command Prompt** (Windows: Press `Win + R`, type `cmd`)
2. Navigate to the apple-clone folder:
   ```cmd
   cd c:\Users\CLINIC\.gemini\antigravity-ide\scratch\apple-clone
   ```
3. Run the cleanup script:
   ```cmd
   python remove_apple_links.py
   ```
   OR double-click: `clean_apple_links.bat`

**What it does:**
- ✅ Removes all hreflang alternate links (saves ~3KB per file)
- ✅ Replaces apple.com external links with `#`
- ✅ Replaces Apple social media with your LinkedIn
- ✅ Replaces Apple YouTube with your YouTube
- ✅ Removes Apple support/iCloud/App Store links
- ✅ Cleans up Apple tracking scripts

---

### **Option 2: Manual Search & Replace**
If you want to see what's being changed:

1. **Open an HTML file** in VS Code
2. **Press Ctrl + H** to open Find & Replace
3. **Use these patterns:**

#### Remove hreflang links:
- **Find:** `<link rel="alternate" href="https://www\.apple\.com/.*?" hreflang=.*? />`
- **Replace:** (leave empty)
- **Enable Regex:** Yes
- **Click Replace All**

#### Remove iCloud links:
- **Find:** `href="https://www\.icloud\.com/[^"]*"`
- **Replace:** `href="#"`

#### Remove support links:
- **Find:** `href="https://support\.apple\.com/[^"]*"`
- **Replace:** `href="#"`

#### Replace with your portfolio:
- **Find:** `https://www\.apple\.com/`
- **Replace:** `#` (or link to your portfolio)

---

## Files to Check

All these files need attention:
```
✓ /index.html (main homepage)
✓ /store/index.html
✓ /mac/index.html
✓ /iphone/index.html
✓ /ipad/index.html
✓ /watch/index.html
✓ /airpods/index.html
✓ /apple-vision-pro/index.html
✓ /tv-home/index.html
✓ /entertainment/index.html
✓ /shop/buy-iphone/index.html
✓ /us/shop/goto/store/index.html
```

---

## Your Contact Info Summary

```
Name: Tchuekam Rostand
LinkedIn: https://www.linkedin.com/in/tchuekam-rostand/
YouTube: https://www.youtube.com/@Giantech-Empire
Phone: +237659248952 / +237653683174
Portfolio 1: https://tchuekam-agent.netlify.app/
Portfolio 2: https://tchuekamui-sovereign.vercel.app/
```

---

## Next Steps

1. **Run the cleanup script** (recommended)
2. **Verify the changes** by opening pages in a browser
3. **Update page titles and descriptions** to match your brand
4. **Add footer with your contact info**
5. **Test all links** to ensure they work
6. **Deploy your personalized site**

---

## Quick Checklist

- [ ] Run `remove_apple_links.py` script
- [ ] Verify hreflang links are removed
- [ ] Check social media links point to your profiles
- [ ] Update page titles and meta descriptions
- [ ] Add your contact information to footer
- [ ] Test all links work correctly
- [ ] Preview site in browser


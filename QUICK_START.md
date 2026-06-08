# QUICK START: Remove Apple Links

## ⚡ Fastest Way (1 minute)

### Windows Command Prompt:
```cmd
cd c:\Users\CLINIC\.gemini\antigravity-ide\scratch\apple-clone
python remove_apple_links.py
```

OR double-click: `clean_apple_links.bat`

---

## 📋 What Gets Removed/Replaced

### ❌ REMOVED:
- All hreflang alternate language links (~200 per file)
- Apple support links
- Apple iCloud links  
- Apple App Store links
- Apple tracking scripts

### 🔄 REPLACED WITH:
- Apple social media → `https://www.linkedin.com/in/tchuekam-rostand/`
- Apple YouTube → `https://www.youtube.com/@Giantech-Empire`
- All other apple.com links → `#`

---

## 📞 Your Info (Use in footer/contact)
```
LinkedIn: https://www.linkedin.com/in/tchuekam-rostand/
YouTube: https://www.youtube.com/@Giantech-Empire
Phone: +237659248952 / +237653683174
Portfolio 1: https://tchuekam-agent.netlify.app/
Portfolio 2: https://tchuekamui-sovereign.vercel.app/
```

---

## ✅ Files Affected (12 total)
- index.html
- store/index.html
- mac/index.html
- iphone/index.html
- ipad/index.html
- watch/index.html
- airpods/index.html
- apple-vision-pro/index.html
- tv-home/index.html
- entertainment/index.html
- shop/buy-iphone/index.html
- us/shop/goto/store/index.html

---

## 🔍 Manual Check (VS Code)

Press Ctrl+F and search for:
- `apple.com` → Should not find any
- `hreflang="` → Should be minimal (only en-US)
- `support.apple` → Should not find any
- `icloud.com` → Should not find any

---

## 📖 Full Guide
See: `APPLE_LINKS_REMOVAL_GUIDE.md`

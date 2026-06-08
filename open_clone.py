import sys
import os
import time
import ctypes

try:
    import pygetwindow as gw
    import pyautogui
except ImportError:
    print("Error: libraries missing")
    sys.exit(1)

# Windows API Constants
SW_RESTORE = 9

def force_activate_chrome():
    # Find Chrome window
    windows = gw.getWindowsWithTitle('Google Chrome')
    if not windows:
        print("Chrome window not found")
        return False
        
    chrome_win = windows[0]
    hwnd = chrome_win._hWnd
    
    # Force window to foreground
    ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(1.0)
    
    # Clicks to focus address bar
    # Screen size is 1366x768. The address bar is at y=80. Let's click at x=400, y=80
    pyautogui.click(400, 80)
    time.sleep(0.3)
    
    # Enter URL
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.write('http://localhost:8001')
    time.sleep(0.2)
    pyautogui.press('enter')
    
    # Wait for page load
    time.sleep(3.0)
    
    # Take screenshot
    pyautogui.screenshot('screenshot_clone.png')
    print("Success")
    return True

if __name__ == "__main__":
    force_activate_chrome()

import time
import pyautogui

def open_url():
    # Click Chrome icon on the taskbar to focus it
    # Screen size is 1366x768. The Chrome taskbar icon is at x=645, y=750
    pyautogui.click(645, 750)
    time.sleep(1.0)
    
    # Focus Chrome's address bar using Ctrl+L
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.3)
    
    # Write the URL and press Enter
    pyautogui.write('http://localhost:8001')
    time.sleep(0.2)
    pyautogui.press('enter')
    
    # Wait for the page to render
    time.sleep(3.0)
    
    # Take a screenshot to verify
    pyautogui.screenshot('screenshot_clone.png')
    print("Navigation complete")

if __name__ == "__main__":
    open_url()

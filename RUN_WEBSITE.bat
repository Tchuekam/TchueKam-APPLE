@echo off
REM Apple Clone → Personal Website Startup Script
REM This script cleans Apple links and starts the web server

echo.
echo ════════════════════════════════════════════════════════════════
echo            APPLE CLONE - PERSONAL WEBSITE SERVER
echo ════════════════════════════════════════════════════════════════
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/2] Running cleanup script...
echo ─────────────────────────────────────────────────────────────────
python remove_apple_links.py
echo.

echo [2/2] Starting web server on port 8001...
echo ─────────────────────────────────────────────────────────────────
echo.
echo ✓ Server starting... 
echo ✓ Open browser and go to: http://localhost:8001
echo ✓ Press Ctrl+C to stop the server
echo.
echo ════════════════════════════════════════════════════════════════
echo.

python -m http.server 8001

pause

@echo off
REM Batch script to remove Apple links from all HTML files
REM Run this from Command Prompt in the apple-clone directory
REM Usage: clean_apple_links.bat

echo ========================================================
echo CLEANING APPLE LINKS FROM WEBSITE CLONE
echo ========================================================
echo.

cd /d "%~dp0"
python remove_apple_links.py

echo.
pause

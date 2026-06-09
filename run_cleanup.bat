@echo off
REM Comprehensive cleanup batch file for Windows
echo.
echo ============================================================
echo APPLE CLONE - CLEANUP SCRIPT
echo ============================================================
echo.
echo Running cleanup on all HTML files...
echo.

python cleanup_all_pages.py

echo.
echo Press any key to continue...
pause >nul

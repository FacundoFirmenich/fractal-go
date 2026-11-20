@echo off
cd /d "%~dp0"
py -3 launch.py all
if errorlevel 1 pause

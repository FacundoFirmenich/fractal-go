@echo off
cd /d "%~dp0"
py -3 launch.py figures
if errorlevel 1 pause

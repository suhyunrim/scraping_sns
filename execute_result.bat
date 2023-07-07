pyinstaller -F main.py

@echo off
for /f "delims=" %%# in ('powershell get-date -format "{yyMMdd_HHmm}"') do @set _date=%%#
echo %_date%

move .\dist\main.exe .\seyoung_project.exe
tar -a -c -f seyoung_project-%_date%.zip seyoung_project.exe execute_chrome.bat
rmdir /s /q build
rmdir /s /q dist
del main.spec
del seyoung_project.exe
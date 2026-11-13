@echo off
cd /d "%~dp0"
if not exist logs mkdir logs

rem Single-instance guard: never start a second watchdog process.
powershell -NoProfile -Command "if (Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'app\.telegram\.bot' }) { exit 0 } else { exit 1 }"
if not errorlevel 1 exit /b 0

:loop
.venv\Scripts\pythonw.exe -m app.telegram.bot >> logs\bot.log 2>&1
if errorlevel 3 exit /b 0
%SystemRoot%\System32\timeout.exe /t 5 /nobreak >nul
goto loop

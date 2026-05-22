@echo off
setlocal
set "PYTHON=d:\AI\hermes\venv\Scripts\python.exe"
cd /d "d:\AI\hermes\Projects\tws-stock-analysis"

if "%~1"=="" goto test
if /I "%~1"=="seed" goto seed
if /I "%~1"=="test" goto test
if /I "%~1"=="api" goto api
if /I "%~1"=="lint" goto lint

echo Usage: run.cmd [seed^|test^|api^|lint]
exit /b 1

:seed
"%PYTHON%" scripts\seed_db.py
exit /b %ERRORLEVEL%

:test
"%PYTHON%" -m pytest -q
exit /b %ERRORLEVEL%

:api
set "PORT=18888"
echo TWS API: http://127.0.0.1:%PORT%/  (docs: /docs)
echo If bind fails, close the previous api window or: taskkill /F /IM python.exe
"%PYTHON%" -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port %PORT%
exit /b %ERRORLEVEL%

:lint
"%PYTHON%" -m ruff check src tests scripts
if errorlevel 1 exit /b 1
"%PYTHON%" -m mypy .
exit /b %ERRORLEVEL%

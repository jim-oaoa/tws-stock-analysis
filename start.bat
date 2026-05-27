@echo off
chcp 65001 >nul
title TWS Stock Analysis Launcher

echo ============================================
echo   TWS Stock Analysis - Starting Servers
echo ============================================
echo.

echo [1/2] Starting Backend API on port 8001...
start "TWS-Backend" cmd /c wsl -- bash -c "cd /mnt/d/AI/hermes/Projects/tws-stock-analysis && python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend on port 5174...
start "TWS-Frontend" cmd /c wsl -- bash -c "cd /mnt/d/AI/hermes/Projects/tws-stock-analysis/frontend && npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo   Servers Started!
echo.
echo   Backend  API  :  http://localhost:8001/docs
echo   Frontend App  :  http://localhost:5174
echo ============================================
echo.
pause

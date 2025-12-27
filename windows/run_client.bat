@echo off
REM Hizli Client Calistirma (EXE olmadan)
echo.
echo Siber Guvenlik Client baslatiliyor...
echo.

python run_client.py

if errorlevel 1 (
    echo.
    echo [HATA] Python veya bagimliliklar eksik!
    echo Once build_client.bat calistirin.
    pause
)

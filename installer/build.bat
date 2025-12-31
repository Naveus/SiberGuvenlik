@echo off
REM =====================================================
REM Client EXE Olusturma Scripti (Windows)
REM Python ve PyInstaller kurulu olmali
REM =====================================================

echo.
echo ========================================
echo   Client EXE Olusturucu
echo ========================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi!
    echo Lutfen Python kurun: https://python.org
    pause
    exit /b 1
)

echo [OK] Python bulundu

REM PyInstaller kontrolu
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [*] PyInstaller kuruluyor...
    pip install pyinstaller
)

echo [OK] PyInstaller hazir

REM Gerekli paketler
echo [*] Gerekli paketler kontrol ediliyor...
pip install pillow pyautogui >nul 2>&1

REM Build scripti calistir
cd /d "%~dp0"
python build_exe.py --all

echo.
echo ========================================
echo Islem tamamlandi!
echo EXE dosyalari: ..\dist\ klasorunde
echo ========================================
pause

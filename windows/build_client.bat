@echo off
REM ========================================
REM Siber Guvenlik Client - Windows Build Script
REM Bu dosyayi Windows'ta calistirin
REM ========================================

echo.
echo =============================================
echo   SIBER GUVENLIK CLIENT - Windows Kurulum
echo =============================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi!
    echo Python 3.8+ yukleyin: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python bulundu.

REM Bagimliliklari yukle
echo [2/4] Bagimliliklar yukleniyor...
pip install PyQt5 Pillow pyautogui pyinstaller --quiet

if errorlevel 1 (
    echo [HATA] Bagimliliklar yuklenemedi!
    pause
    exit /b 1
)

echo [3/4] EXE olusturuluyor...

REM PyInstaller ile EXE olustur
pyinstaller --onefile --windowed --name "SiberGuvenlikClient" ^
    --add-data "client;client" ^
    --add-data "shared;shared" ^
    --hidden-import PyQt5 ^
    --hidden-import PIL ^
    --hidden-import pyautogui ^
    --uac-admin ^
    run_client.py

if errorlevel 1 (
    echo [HATA] EXE olusturulamadi!
    pause
    exit /b 1
)

echo [4/4] Tamamlandi!
echo.
echo =============================================
echo   BASARILI!
echo   EXE dosyasi: dist\SiberGuvenlikClient.exe
echo =============================================
echo.
echo Bu EXE dosyasini hedef Windows bilgisayara kopyalayip
echo cift tiklayarak calistirabilirsiniz.
echo.

pause

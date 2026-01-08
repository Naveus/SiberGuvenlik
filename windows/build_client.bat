@echo off
REM ========================================
REM Siber Guvenlik Client - Windows Build Script
REM Bu dosyayi Windows'ta calistirin
REM 
REM Ozellikler:
REM - Otomatik yonetici yetkisi (UAC)
REM - Retry mekanizmasi
REM - Tum bagimliliklari paketler
REM ========================================

echo.
echo =============================================
echo   SIBER GUVENLIK CLIENT - Windows Kurulum
echo   Yonetici Yetkili EXE Olusturucu
echo =============================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi!
    echo.
    echo Cozum 1: Python 3.8+ yukleyin: https://python.org
    echo Cozum 2: installer/ClientInstaller.exe kullanin
    echo.
    pause
    exit /b 1
)

echo [1/5] Python bulundu.

REM Bagimliliklari yukle (retry mekanizmali)
echo [2/5] Bagimliliklar yukleniyor...
set RETRY=0

:INSTALL_DEPS
echo [*] Pip guncelleniyor...
python -m pip install --upgrade pip
echo [*] Paketler yukleniyor...
pip install Pillow pyautogui pyinstaller PyQt5
if errorlevel 1 (
    set /a RETRY+=1
    if %RETRY% lss 3 (
        echo [!] Bagimlilik yukleme hatasi, tekrar deneniyor... (%RETRY%/3)
        timeout /t 2 /nobreak >nul
        goto INSTALL_DEPS
    )
    echo [HATA] Bagimliliklar yuklenemedi!
    pause
    exit /b 1
)

echo [3/5] Onceki build temizleniyor...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo [4/5] EXE olusturuluyor (Yonetici Yetkili)...

REM PyInstaller ile EXE olustur - UAC Admin ile
pyinstaller --onefile --windowed --name "SiberGuvenlikClient" ^
    --add-data "client;client" ^
    --add-data "shared;shared" ^
    --hidden-import PIL ^
    --hidden-import PIL.ImageGrab ^
    --hidden-import PIL.Image ^
    --hidden-import pyautogui ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --uac-admin ^
    --clean ^
    run_client.py

if errorlevel 1 (
    echo [HATA] EXE olusturulamadi!
    echo.
    echo Cozum: PyInstaller'i guncelleyin
    echo   pip install --upgrade pyinstaller
    pause
    exit /b 1
)

echo [5/5] Tamamlandi!
echo.
echo =============================================
echo   BASARILI!
echo   EXE: dist\SiberGuvenlikClient.exe
echo =============================================
echo.
echo ONEMLI: Bu EXE calistirildiginda otomatik olarak
echo yonetici yetkisi isteyecektir (UAC penceresi).
echo.
echo Hedef bilgisayara kopyalayip cift tiklayin.
echo Python yuklenmemis bilgisayarlarda da calisir!
echo.

pause

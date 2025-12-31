@echo off
REM =====================================================
REM Client Installer - Python Otomatik Kurulum
REM Python yoksa indirir ve kurar, sonra Client'i baslatir
REM =====================================================

echo.
echo =============================================
echo   SIBER GUVENLIK CLIENT - Otomatik Kurulum
echo   Python + Bagimliliklar + Client
echo =============================================
echo.

REM Yonetici yetkisi kontrolu
net session >nul 2>&1
if errorlevel 1 (
    echo [!] Yonetici yetkisi gerekli!
    echo [*] Yonetici olarak yeniden baslatiliyor...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo [OK] Yonetici yetkisi onaylandi.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python bulunamadi, kuruluyor...
    goto INSTALL_PYTHON
) else (
    echo [OK] Python bulundu.
    goto INSTALL_DEPS
)

:INSTALL_PYTHON
echo [1/4] Python indiriliyor...

REM Python indirme dizini
set TEMP_DIR=%TEMP%\python_install
mkdir "%TEMP_DIR%" 2>nul

REM Python 3.11 indir
set PYTHON_URL=https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
set PYTHON_INSTALLER=%TEMP_DIR%\python_installer.exe

echo [*] Indiriliyor: %PYTHON_URL%
powershell -Command "(New-Object Net.WebClient).DownloadFile('%PYTHON_URL%', '%PYTHON_INSTALLER%')"

if not exist "%PYTHON_INSTALLER%" (
    echo [HATA] Python indirilemedi!
    echo Lutfen manuel olarak kurun: https://python.org
    pause
    exit /b 1
)

echo [2/4] Python kuruluyor (bu birkaç dakika surebilir)...

REM Sessiz kurulum - PATH'e ekle
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

if errorlevel 1 (
    echo [HATA] Python kurulumu basarisiz!
    echo [*] Manuel kurulum deneniyor...
    "%PYTHON_INSTALLER%"
)

REM PATH'i yenile
set PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python kuruldu ama PATH'e eklenmedi!
    echo [*] Bilgisayari yeniden baslatin ve tekrar deneyin.
    pause
    exit /b 1
)

echo [OK] Python basariyla kuruldu!

:INSTALL_DEPS
echo [3/4] Bagimliliklar kuruluyor...

set RETRY=0
:RETRY_DEPS
pip install pillow pyautogui --quiet
if errorlevel 1 (
    set /a RETRY+=1
    if %RETRY% lss 3 (
        echo [!] Kurulum hatasi, tekrar deneniyor... (%RETRY%/3)
        timeout /t 2 /nobreak >nul
        goto RETRY_DEPS
    )
    echo [UYARI] Bazi paketler kurulamadi, devam ediliyor...
)

echo [OK] Bagimliliklar kuruldu.

:RUN_CLIENT
echo [4/4] Client baslatiliyor...

REM Client script'i calistir
if exist "run_client.py" (
    python run_client.py
) else if exist "client\client_gui.py" (
    python -c "import sys; sys.path.insert(0,'.'); from client.client_gui import main; main()"
) else (
    echo [HATA] Client dosyalari bulunamadi!
    pause
    exit /b 1
)

echo.
echo [OK] Kurulum tamamlandi!
pause

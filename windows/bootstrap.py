#!/usr/bin/env python3
"""
Bootstrap/Installer Script
Python yüklü olmayan bilgisayarlarda Client'ı çalıştırmak için
Otomatik yönetici yetkisi alır ve gerekli kurulumları yapar
"""

import os
import sys
import subprocess
import ctypes
import time
import tempfile
import urllib.request
import zipfile

# Sabitler
PYTHON_VERSION = "3.11.7"
PYTHON_DOWNLOAD_URL = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-embed-amd64.zip"
GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"
REQUIRED_PACKAGES = ["pillow", "pyautogui"]
MAX_RETRY = 3


def is_admin():
    """Yönetici yetkisi kontrolü"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """Yönetici olarak yeniden çalıştır"""
    if sys.platform != 'win32':
        return False
    
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        return True
    except:
        return False


def log(message, level="INFO"):
    """Log mesajı yazdır"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def show_error(message):
    """Hata mesajı göster"""
    if sys.platform == 'win32':
        ctypes.windll.user32.MessageBoxW(0, message, "Kurulum Hatası", 0x10)
    else:
        print(f"HATA: {message}")


def show_info(message):
    """Bilgi mesajı göster"""
    if sys.platform == 'win32':
        ctypes.windll.user32.MessageBoxW(0, message, "Kurulum Bilgisi", 0x40)
    else:
        print(f"BİLGİ: {message}")


def download_file(url, dest_path, retry=MAX_RETRY):
    """Dosya indir (retry mekanizmalı)"""
    for attempt in range(retry):
        try:
            log(f"İndiriliyor: {url} (Deneme {attempt + 1}/{retry})")
            urllib.request.urlretrieve(url, dest_path)
            log(f"İndirildi: {dest_path}")
            return True
        except Exception as e:
            log(f"İndirme hatası: {e}", "ERROR")
            if attempt < retry - 1:
                time.sleep(2)
    return False


def check_python():
    """Python kurulu mu kontrol et"""
    try:
        result = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            log(f"Python bulundu: {result.stdout.strip()}")
            return True
    except:
        pass
    
    try:
        result = subprocess.run(
            ["py", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            log(f"Python bulundu: {result.stdout.strip()}")
            return True
    except:
        pass
    
    return False


def install_embedded_python():
    """Gömülü Python indir ve kur"""
    log("Gömülü Python kuruluyor...")
    
    install_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'EmbeddedPython')
    os.makedirs(install_dir, exist_ok=True)
    
    python_zip = os.path.join(tempfile.gettempdir(), 'python_embed.zip')
    
    # Python indir
    if not download_file(PYTHON_DOWNLOAD_URL, python_zip):
        return None
    
    # Zip'i çıkar
    try:
        with zipfile.ZipFile(python_zip, 'r') as zip_ref:
            zip_ref.extractall(install_dir)
        log(f"Python çıkarıldı: {install_dir}")
    except Exception as e:
        log(f"Zip çıkarma hatası: {e}", "ERROR")
        return None
    
    # python311._pth dosyasını düzenle (pip için gerekli)
    pth_file = os.path.join(install_dir, 'python311._pth')
    if os.path.exists(pth_file):
        with open(pth_file, 'a') as f:
            f.write('\nimport site\n')
    
    # pip kur
    get_pip = os.path.join(tempfile.gettempdir(), 'get-pip.py')
    if download_file(GET_PIP_URL, get_pip):
        python_exe = os.path.join(install_dir, 'python.exe')
        try:
            subprocess.run([python_exe, get_pip], check=True, timeout=120)
            log("pip kuruldu")
        except Exception as e:
            log(f"pip kurulum hatası: {e}", "ERROR")
    
    # Temizlik
    try:
        os.remove(python_zip)
        os.remove(get_pip)
    except:
        pass
    
    return install_dir


def install_packages(python_exe):
    """Gerekli paketleri kur"""
    log("Gerekli paketler kuruluyor...")
    
    for package in REQUIRED_PACKAGES:
        for attempt in range(MAX_RETRY):
            try:
                log(f"Kuruluyor: {package} (Deneme {attempt + 1}/{MAX_RETRY})")
                result = subprocess.run(
                    [python_exe, "-m", "pip", "install", package],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode == 0:
                    log(f"Kuruldu: {package}")
                    break
                else:
                    log(f"Kurulum çıktısı: {result.stderr}", "WARNING")
            except Exception as e:
                log(f"Paket kurulum hatası ({package}): {e}", "ERROR")
                if attempt < MAX_RETRY - 1:
                    time.sleep(2)


def run_client(python_exe):
    """Client uygulamasını çalıştır"""
    # Client dosyasının konumu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    client_script = os.path.join(script_dir, '..', 'run_client.py')
    
    if not os.path.exists(client_script):
        # Aynı dizinde olabilir
        client_script = os.path.join(script_dir, 'run_client.py')
    
    if not os.path.exists(client_script):
        log("Client scripti bulunamadı!", "ERROR")
        return False
    
    try:
        log(f"Client başlatılıyor: {client_script}")
        subprocess.Popen([python_exe, client_script])
        return True
    except Exception as e:
        log(f"Client başlatma hatası: {e}", "ERROR")
        return False


def main():
    """Ana fonksiyon"""
    log("=" * 50)
    log("Client Installer Başlatıldı")
    log("=" * 50)
    
    # Windows kontrolü
    if sys.platform != 'win32':
        show_error("Bu installer sadece Windows'ta çalışır!")
        return
    
    # Yönetici yetkisi kontrolü
    if not is_admin():
        log("Yönetici yetkisi isteniyor...")
        if run_as_admin():
            log("Yönetici olarak yeniden başlatılıyor...")
            sys.exit(0)
        else:
            show_error("Yönetici yetkisi alınamadı!\nLütfen programı sağ tıklayıp 'Yönetici olarak çalıştır' seçin.")
            return
    
    log("Yönetici yetkisi onaylandı ✓")
    
    python_exe = None
    
    # Python kontrol
    if check_python():
        # Sistem Python'u kullan
        python_exe = "python"
    else:
        log("Python bulunamadı, kuruluyor...")
        
        install_dir = install_embedded_python()
        if install_dir:
            python_exe = os.path.join(install_dir, 'python.exe')
        else:
            show_error("Python kurulumu başarısız!\nLütfen manuel olarak Python kurun: https://python.org")
            return
    
    # Paketleri kur
    install_packages(python_exe)
    
    # Client'ı çalıştır
    if run_client(python_exe):
        log("Client başarıyla başlatıldı!")
        show_info("Kurulum tamamlandı!\nClient uygulaması başlatılıyor...")
    else:
        show_error("Client başlatılamadı!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        show_error(f"Beklenmeyen hata: {e}")
        sys.exit(1)

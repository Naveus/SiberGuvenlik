"""
Client EXE Olusturma Scripti
Windows'ta calistirin: python build_client.py
"""

import subprocess
import sys
import os

def build():
    # PyInstaller kontrol
    try:
        import PyInstaller
        print("[OK] PyInstaller kurulu")
    except ImportError:
        print("[!] PyInstaller kuruluyor...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Build komutu
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Tek dosya
        "--windowed",          # Konsol penceresi yok
        "--name", "Client",    # Exe adi
        "--clean",             # Onceki build temizle

        # Icon eklemek istersen (Windows icin .ico dosyasi gerekli):
        # "--icon", "client_icon.ico",

        # Gizli importlar
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.ImageGrab",

        # Ana dosya
        "run_client.py"
    ]

    print("\n[*] Client.exe olusturuluyor...\n")
    subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))

    print("\n" + "="*50)
    print("[OK] Tamamlandi!")
    print("[*] EXE dosyasi: dist/Client.exe")
    print("="*50)

if __name__ == "__main__":
    build()

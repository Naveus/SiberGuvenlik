"""
Client EXE Oluşturma Scripti
Windows'ta çalıştırın: python build_client.py

Yeni özellikler:
- Otomatik yönetici yetkisi isteme (UAC)
- Tüm bağımlılıkları paketleme
- İsteğe bağlı installer EXE oluşturma
"""

import subprocess
import sys
import os

def build():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # PyInstaller kontrol
    try:
        import PyInstaller
        print("[OK] PyInstaller kurulu")
    except ImportError:
        print("[!] PyInstaller kuruluyor...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Build komutu - UAC admin desteği ile
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Tek dosya
        "--windowed",          # Konsol penceresi yok
        "--name", "Client",    # Exe adı
        "--clean",             # Önceki build temizle
        "--uac-admin",         # OTOMATİK YÖNETİCİ YETKİSİ İSTE

        # Icon eklemek istersen (Windows için .ico dosyası gerekli):
        # "--icon", "client_icon.ico",

        # Gizli importlar
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.ImageGrab",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "pyautogui",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.messagebox",

        # Ana dosya
        "run_client.py"
    ]

    print("\n[*] Client.exe oluşturuluyor (YÖNETİCİ YETKİSİ AKTİF)...\n")
    result = subprocess.run(cmd, cwd=script_dir)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("[OK] Tamamlandı!")
        print("[*] EXE dosyası: dist/Client.exe")
        print("")
        print("[!] NOT: Bu EXE çalıştırıldığında otomatik olarak")
        print("    yönetici yetkisi isteyecektir (UAC penceresi)")
        print("=" * 60)
    else:
        print("\n[HATA] Build başarısız!")
        return False
    
    return True

def show_help():
    print("""
Client EXE Oluşturucu
=====================

Kullanım:
  python build_client.py              Normal build (sadece Client.exe)
  python build_client.py --installer  Installer EXE'yi de oluştur
  python build_client.py --help       Bu yardım mesajı

Gelişmiş build için:
  cd installer
  python build_exe.py --all

Daha fazla bilgi için: installer/README.md
""")

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
    elif "--installer" in sys.argv:
        # Installer modunu kullan
        installer_script = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "installer", "build_exe.py"
        )
        if os.path.exists(installer_script):
            subprocess.run([sys.executable, installer_script, "--all"])
        else:
            print("[!] installer/build_exe.py bulunamadı")
            build()
    else:
        build()

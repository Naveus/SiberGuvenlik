#!/usr/bin/env python3
"""
Gelişmiş Client EXE Oluşturma Scripti
- Yönetici yetkisi isteyen manifest ekler
- Tek dosya EXE oluşturur
- Tüm bağımlılıkları paketler
"""

import subprocess
import sys
import os
import shutil

def build():
    # Script dizini
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Ana proje dizini
    
    # PyInstaller kontrol
    try:
        import PyInstaller
        print("[OK] PyInstaller kurulu")
    except ImportError:
        print("[!] PyInstaller kuruluyor...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Manifest dosyasını .manifest uzantısıyla kopyala (geçici)
    manifest_src = os.path.join(script_dir, "client_admin.xml")
    manifest_dest = os.path.join(script_dir, "client_temp.manifest")
    
    if os.path.exists(manifest_src):
        shutil.copy(manifest_src, manifest_dest)
        print("[OK] Manifest dosyası hazırlandı")
    
    # Build komutu
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Tek dosya
        "--windowed",          # Konsol penceresi yok  
        "--name", "Client",    # Exe adı
        "--clean",             # Önceki build temizle
        "--uac-admin",         # UAC yönetici yetkisi iste
        
        # Gizli importlar
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.ImageGrab",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "pyautogui",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.messagebox",
        
        # Çalışma dizini
        "--distpath", os.path.join(project_root, "dist"),
        "--workpath", os.path.join(project_root, "build"),
        "--specpath", os.path.join(project_root, "build"),
        
        # Ana dosya
        os.path.join(project_root, "run_client.py")
    ]
    
    # Manifest varsa ekle
    if os.path.exists(manifest_dest):
        cmd.insert(-1, "--manifest")
        cmd.insert(-1, manifest_dest)
    
    print("\n[*] Client.exe oluşturuluyor...\n")
    print(f"[*] Komut: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=project_root)
    
    # Geçici manifest dosyasını sil
    if os.path.exists(manifest_dest):
        os.remove(manifest_dest)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("[OK] Build başarılı!")
        print(f"[*] EXE dosyası: {os.path.join(project_root, 'dist', 'Client.exe')}")
        print("=" * 60)
        print("\n[!] NOT: Bu EXE otomatik olarak yönetici yetkisi isteyecektir.")
    else:
        print("\n[HATA] Build başarısız!")
        return False
    
    return True


def build_installer():
    """Bootstrap installer'ı da EXE'ye çevir"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    bootstrap_script = os.path.join(script_dir, "bootstrap.py")
    
    if not os.path.exists(bootstrap_script):
        print("[!] bootstrap.py bulunamadı, sadece Client.exe oluşturuldu")
        return
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "ClientInstaller",
        "--clean",
        "--uac-admin",  # Yönetici yetkisi iste
        
        "--distpath", os.path.join(project_root, "dist"),
        "--workpath", os.path.join(project_root, "build"),
        "--specpath", os.path.join(project_root, "build"),
        
        bootstrap_script
    ]
    
    print("\n[*] ClientInstaller.exe oluşturuluyor...\n")
    result = subprocess.run(cmd, cwd=project_root)
    
    if result.returncode == 0:
        print(f"[OK] Installer EXE: {os.path.join(project_root, 'dist', 'ClientInstaller.exe')}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Client EXE Builder")
    parser.add_argument("--installer", action="store_true", 
                       help="Installer EXE'yi de oluştur")
    parser.add_argument("--all", action="store_true",
                       help="Hem Client hem Installer EXE oluştur")
    
    args = parser.parse_args()
    
    # Client EXE oluştur
    if build():
        # Installer da isteniyorsa
        if args.installer or args.all:
            build_installer()
    
    print("\n[*] İşlem tamamlandı!")

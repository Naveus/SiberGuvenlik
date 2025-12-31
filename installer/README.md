# Client Installer

Bu klasör, Python yüklü olmayan Windows bilgisayarlarda Client uygulamasını çalıştırmak için gerekli dosyaları içerir.

## 📁 Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `bootstrap.py` | Otomatik kurulum scripti - Python yoksa kurar, yönetici yetkisi ister |
| `build_exe.py` | PyInstaller ile EXE oluşturma scripti |
| `build.bat` | Windows'ta tek tıkla EXE oluşturma |
| `client_admin.xml` | Yönetici yetkisi istemek için Windows manifest dosyası |

## 🚀 Kullanım

### 1. EXE Oluşturma (Geliştirici Bilgisayarında)

Windows'ta cmd veya PowerShell açın:

```batch
cd installer
build.bat
```

veya Python ile:

```bash
python build_exe.py --all
```

Bu komut iki EXE dosyası oluşturur:
- `dist/Client.exe` - Ana client uygulaması
- `dist/ClientInstaller.exe` - Otomatik kurulum yapan installer

### 2. Hedef Bilgisayarda Çalıştırma

#### Seçenek A: Client.exe (Python Kurulu Olan Bilgisayarlar)
- `Client.exe` çift tıklayın
- Otomatik olarak yönetici yetkisi isteyecektir
- UAC penceresi çıkacak, "Evet" deyin

#### Seçenek B: ClientInstaller.exe (Python Kurulu Olmayan Bilgisayarlar)
- `ClientInstaller.exe` çift tıklayın
- Otomatik olarak:
  1. Yönetici yetkisi isteyecek
  2. Python kurulu değilse gömülü Python indirecek
  3. Gerekli paketleri kuracak (pillow, pyautogui)
  4. Client uygulamasını başlatacak

## ⚙️ Özellikler

### Otomatik Yönetici Yetkisi
- EXE çalıştığında Windows UAC penceresi açılır
- Kullanıcı "Evet" demeden uygulama başlamaz
- Bu, sistem kontrolleri için gereklidir

### Retry Mekanizması
- İndirme başarısız olursa 3 kez denenir
- Paket kurulumu başarısız olursa 3 kez denenir
- Hata mesajları detaylı gösterilir

### Gömülü Python
- Python 3.11.7 Embedded sürümü kullanılır
- Sistem Python'una dokunmaz
- `%LOCALAPPDATA%\EmbeddedPython` klasörüne kurulur

## ⚠️ Gereksinimler

### EXE Oluşturmak İçin (Geliştirici Bilgisayarı)
- Python 3.8+
- PyInstaller (`pip install pyinstaller`)
- pillow (`pip install pillow`)
- pyautogui (`pip install pyautogui`)

### Hedef Bilgisayar
- Windows 7/8/10/11
- İnternet bağlantısı (ilk kurulum için)
- Yönetici yetkisi

## 🔧 Sorun Giderme

### "Python bulunamadı" Hatası
- Python'un PATH'e eklendiğinden emin olun
- veya `ClientInstaller.exe` kullanın

### UAC Penceresi Açılmıyor
- EXE'ye sağ tıklayıp "Yönetici olarak çalıştır" seçin

### Antivirüs Uyarısı
- Bazı antivirüsler PyInstaller EXE'lerini yanlış pozitif olarak işaretleyebilir
- Güvenilir kaynak olduğunu bildiğiniz için izin verin

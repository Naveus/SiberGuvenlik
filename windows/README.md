# 🖥️ Windows Client Kurulum Rehberi

Bu belge, Siber Güvenlik Eğitim Projesi'nin Windows Client bileşeninin kurulumunu açıklar.

---

## 📋 Gereksinimler

| Gereksinim | Minimum | Tavsiye |
|------------|---------|---------|
| **İşletim Sistemi** | Windows 10 | Windows 11 |
| **Python** | 3.8 (EXE için gerekli değil) | 3.11+ |
| **RAM** | 2 GB | 4 GB |
| **Ağ** | LAN bağlantısı | Aynı subnet |

---

## 🚀 Kurulum Yöntemleri

### 🔴 Yöntem 1: Hazır EXE Kullanma (En Kolay)

Python kurulu olmayan bilgisayarlarda direkt çalışır!

1. `dist/SiberGuvenlikClient.exe` dosyasını hedef bilgisayara kopyalayın
2. EXE'ye çift tıklayın
3. **UAC penceresi** açılacak → "Evet" deyin
4. IP ve kodu girin, bağlanın

> ⚠️ EXE dosyası yoksa önce build yapmanız gerekir (Yöntem 3)

---

### 🟡 Yöntem 2: Client Installer (Python Yoksa)

Python kurulu olmayan bilgisayarlar için otomatik kurulum:

1. `installer/ClientInstaller.exe` dosyasını çalıştırın
2. Otomatik olarak:
   - ✅ Yönetici yetkisi ister
   - ✅ Python yoksa indirir ve kurar
   - ✅ Gerekli paketleri kurar
   - ✅ Hata olursa 3 kez dener
   - ✅ Client'ı başlatır

> 💡 İnternet bağlantısı gereklidir (ilk kurulum için)

---

### 🟢 Yöntem 3: EXE Oluşturma (Geliştirici)

Kendi EXE dosyanızı oluşturmak için:

#### Hızlı Yol (Çift Tıkla)
```batch
build_client.bat
```

#### Manuel Yol
```batch
# Bağımlılıkları yükle
pip install -r requirements.txt

# EXE oluştur
pyinstaller --onefile --windowed --uac-admin --name "SiberGuvenlikClient" run_client.py
```

#### Gelişmiş Build (Installer dahil)
```batch
cd ..\installer
python build_exe.py --all
```

Bu komut iki EXE oluşturur:
- `dist/Client.exe` - Ana uygulama
- `dist/ClientInstaller.exe` - Otomatik kurulum

---

### 🔵 Yöntem 4: Python ile Doğrudan Çalıştırma

Geliştirme amaçlı:

```batch
# Bağımlılıkları yükle
pip install -r requirements.txt

# Client'ı başlat
python run_client.py
```

---

## 📖 Kullanım

### Bağlantı Kurma

1. **Admin Panel'i başlatın** (başka bir bilgisayarda)
   ```bash
   python run_admin.py
   ```

2. **Bağlantı bilgilerini not edin:**
   - IP Adresi (örn: `192.168.1.100`)
   - 4 haneli bağlantı kodu (örn: `1234`)

3. **Client'ta bağlanın:**
   - IP adresini girin
   - 4 haneli kodu girin
   - "Bağlan" butonuna tıklayın

### Bağlantı Sonrası

Bağlantı kurulduktan sonra Admin Panel aşağıdaki kontrollere sahip olur:

| Kontrol | Açıklama |
|---------|----------|
| 🔴 PC Kapat | Bilgisayarı kapatır |
| 🟡 Yeniden Başlat | Bilgisayarı yeniden başlatır |
| ⬛ Task Manager | Görev Yöneticisini aç/kapat |
| ⬛ CMD | Komut İstemi'ni aç/kapat |
| 📴 Ekran Gizle | Ekranı karartır |
| 🎹 Touchpad | Touchpad'i aç/kapat |
| ❌ Aktif Uygulamayı Kapat | Alt+F4 gönderir |
| 🖼️ Ekran Görüntüsü | Anlık görüntü alır |
| 📺 Canlı Akış | Ekranı gerçek zamanlı izler |
| 🖱️ Uzaktan Kontrol | Fare ve klavye kontrolü |

---

## ✨ Özellikler

- 🛡️ **Otomatik Yönetici Yetkisi** - UAC penceresi ile
- 🔄 **Retry Mekanizması** - Hata olursa 3 kez dener
- 🎨 **Modern Siber Tema** - Mavi-mor gradient tasarım
- 🔒 **Güvenli Bağlantı** - 4 haneli doğrulama kodu
- 💬 **Çift Yönlü Mesajlaşma** - Admin ile iletişim
- 📺 **Canlı Ekran Akışı** - 60 FPS, 720p
- 🖱️ **Uzaktan Kontrol** - Fare ve klavye desteği
- 📴 **Ekran Gizleme** - Fullscreen siyah overlay
- ⚡ **Düşük Kaynak Kullanımı** - Minimal sistem etkisi
- 📦 **Standalone EXE** - Python kurulu olmadan çalışır

---

## 📁 Dosya Yapısı

```
windows/
├── 📄 README.md            # Bu dosya
├── 📄 requirements.txt     # Python bağımlılıkları
├── 📄 build_client.bat     # EXE oluşturma scripti (UAC destekli)
├── 📄 run_client.bat       # Hızlı çalıştırma (Python gerekli)
├── 📄 run_client.py        # Ana giriş noktası
│
├── 📂 client/              # Client kaynak kodu
│   ├── __init__.py
│   ├── client.py          # Client mantığı
│   └── client_gui.py      # Arayüz
│
└── 📂 shared/              # Ortak modüller
    ├── __init__.py
    └── protocol.py        # İletişim protokolü

installer/                  # Otomatik kurulum dosyaları
├── 📄 bootstrap.py         # Akıllı kurulum scripti
├── 📄 build_exe.py         # Gelişmiş build scripti
├── 📄 build.bat            # Tek tıkla build
├── 📄 client_admin.xml     # Windows manifest (yönetici yetkisi)
└── 📄 README.md            # Installer kullanım rehberi
```

---

## 🔧 Sorun Giderme

### Python Bulunamadı

**Sorun:** `'python' is not recognized as an internal or external command`

**Çözüm:**
- **Seçenek 1:** `ClientInstaller.exe` kullanın (Python otomatik kurulur)
- **Seçenek 2:** Python'u yeniden yükleyin, **"Add Python to PATH"** işaretleyin
- **Seçenek 3:** Manuel PATH ekleme:
  - `Win + R` → `sysdm.cpl` → Gelişmiş → Ortam Değişkenleri
  - Path'e Python yolunu ekleyin (örn: `C:\Python311`)

### Bağlantı Başarısız

**Sorun:** `Bağlantı zaman aşımına uğradı`

**Kontrol Listesi:**
- [ ] Admin Panel çalışıyor mu?
- [ ] IP adresi doğru mu?
- [ ] 4 haneli kod doğru mu?
- [ ] Her iki cihaz aynı ağda mı?
- [ ] Firewall bağlantıyı engelliyor mu?

**Firewall Çözümü:**
```batch
# Windows Firewall'da port 5555'i açın
netsh advfirewall firewall add rule name="SiberGuvenlik" dir=in action=allow protocol=tcp localport=5555
```

### UAC Penceresi Açılmıyor

**Sorun:** EXE yönetici yetkisi istemiyor

**Çözüm:**
- EXE'ye sağ tıklayın → "Yönetici olarak çalıştır"
- veya EXE'yi `--uac-admin` flag'i ile yeniden build edin

### Antivirüs Engelliyor

**Sorun:** EXE virüs olarak algılanıyor

**Çözüm:**
- Bu bir **yanlış pozitif** (false positive)
- PyInstaller EXE'leri bazen yanlış algılanır
- Antivirüste istisna olarak ekleyin

### EXE Oluşturulamıyor

**Sorun:** PyInstaller hatası

**Çözüm:**
```batch
# PyInstaller'ı güncelleyin
pip install --upgrade pyinstaller

# Cache temizleyin
rmdir /s /q build
rmdir /s /q dist

# Tekrar deneyin
build_client.bat
```

### Ekran Akışı Çalışmıyor

**Sorun:** `PIL yuklu degil` hatası

**Çözüm:**
```batch
pip install Pillow
```

### Uzaktan Kontrol Çalışmıyor

**Sorun:** Fare/klavye komutları çalışmıyor

**Çözüm:**
```batch
pip install pyautogui
```

---

## ⚠️ Güvenlik Notları

1. **Yalnızca eğitim amaçlı kullanın**
2. **Yetkisiz sistemlerde çalıştırmayın**
3. **Bağlantı kodunu kimseyle paylaşmayın**
4. **Kurumsal ağlarda IT onayı alın**
5. **EXE dosyasını güvenilir kişilerle paylaşın**

---

## 📞 Destek

Sorunlar için GitHub Issues kullanın veya README'deki iletişim bilgilerine başvurun.

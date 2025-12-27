# 🖥️ Windows Client Kurulum Rehberi

Bu belge, Siber Güvenlik Eğitim Projesi'nin Windows Client bileşeninin kurulumunu açıklar.

---

## 📋 Gereksinimler

| Gereksinim | Minimum | Tavsiye |
|------------|---------|---------|
| **İşletim Sistemi** | Windows 10 | Windows 11 |
| **Python** | 3.8 | 3.11+ |
| **RAM** | 2 GB | 4 GB |
| **Ağ** | LAN bağlantısı | Aynı subnet |

---

## 🚀 Hızlı Kurulum

### Yöntem 1: EXE Oluşturma (Tavsiye Edilen)

1. **Python 3.8+ Yükleyin**
   - [Python İndir](https://www.python.org/downloads/)
   - Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin

2. **EXE Oluşturun**
   ```batch
   build_client.bat
   ```
   Bu dosyaya çift tıklayın. Script otomatik olarak:
   - ✅ Bağımlılıkları yükler (PyQt5, Pillow, pyautogui)
   - ✅ PyInstaller ile derler
   - ✅ `dist/SiberGuvenlikClient.exe` oluşturur

3. **Kullanın**
   - `dist/SiberGuvenlikClient.exe` dosyasını hedef bilgisayara kopyalayın
   - EXE'yi çalıştırın

### Yöntem 2: Python ile Doğrudan Çalıştırma

```batch
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Client'ı başlatın
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
| ❌ Aktif Uygulamayı Kapat | Alt+F4 gönderir |
| 🖼️ Ekran Görüntüsü | Anlık görüntü alır |
| 📺 Canlı Akış | Ekranı gerçek zamanlı izler |
| 🖱️ Uzaktan Kontrol | Fare ve klavye kontrolü |

---

## ✨ Özellikler

- 🎨 **Modern Siber Tema** - Mavi-mor gradient tasarım
- 🔒 **Güvenli Bağlantı** - 4 haneli doğrulama kodu
- 💬 **Çift Yönlü Mesajlaşma** - Admin ile iletişim
- 📺 **Canlı Ekran Akışı** - 60 FPS, 720p
- 🖱️ **Uzaktan Kontrol** - Fare ve klavye desteği
- 📴 **Ekran Gizleme** - Fullscreen siyah overlay
- ⚡ **Düşük Kaynak Kullanımı** - Minimal sistem etkisi

---

## 📁 Dosya Yapısı

```
windows/
├── 📄 README.md            # Bu dosya
├── 📄 requirements.txt     # Python bağımlılıkları
├── 📄 build_client.bat     # EXE oluşturma scripti
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
```

---

## 🔧 Sorun Giderme

### Python Bulunamadı

**Sorun:** `'python' is not recognized as an internal or external command`

**Çözüm:**
1. Python'u yeniden yükleyin
2. Kurulum sırasında **"Add Python to PATH"** seçeneğini işaretleyin
3. Veya manuel olarak PATH'e ekleyin:
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

### EXE Oluşturulamıyor

**Sorun:** PyInstaller hatası

**Çözüm:**
```batch
# PyInstaller'ı güncelleyin
pip install --upgrade pyinstaller

# Manuel olarak EXE oluşturun
pyinstaller --onefile --windowed --name SiberGuvenlikClient run_client.py
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

---

## 📞 Destek

Sorunlar için GitHub Issues kullanın veya README'deki iletişim bilgilerine başvurun.

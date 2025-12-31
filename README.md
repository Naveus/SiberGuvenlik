# 🛡️ Siber Güvenlik Eğitim Projesi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![UAC](https://img.shields.io/badge/UAC-Admin%20Required-red.svg)

**Eğitim amaçlı uzaktan yönetim ve siber güvenlik farkındalık aracı**

</div>

---

## 📋 İçindekiler

- [Hakkında](#-hakkında)
- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Proje Yapısı](#-proje-yapısı)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

---

## 🎯 Hakkında

Bu proje, **siber güvenlik eğitimi** amacıyla geliştirilmiş bir uzaktan yönetim aracıdır. Öğrencilere ve güvenlik uzmanlarına:

- Uzaktan bağlantı protokollerini
- Sistem güvenlik mekanizmalarını
- Ağ iletişim prensiplerini

uygulamalı olarak öğretmeyi hedefler.

> ⚠️ **UYARI:** Bu araç yalnızca eğitim amaçlıdır. Yetkisiz sistemlerde kullanımı yasalara aykırıdır.

---

## ✨ Özellikler

### Admin Panel (macOS/Windows/Linux)
| Özellik | Açıklama |
|---------|----------|
| 🖥️ Canlı Ekran Akışı | Client ekranını gerçek zamanlı izleme |
| 🖱️ Uzaktan Kontrol | Fare ve klavye kontrolü |
| 💬 Mesajlaşma | İki yönlü iletişim |
| ⚡ Sistem Kontrolleri | Kapatma, yeniden başlatma |
| 🔒 Güvenlik Kontrolleri | Task Manager, CMD aç/kapat |
| 🖼️ Ekran Görüntüsü | Anlık ekran yakalama |
| 📴 Ekran Gizleme | Client ekranını karartma |
| 🎹 Touchpad Kontrolü | Touchpad aç/kapat |

### Client (Windows)
| Özellik | Açıklama |
|---------|----------|
| 🔐 Güvenli Bağlantı | 4 haneli kod ile bağlantı |
| 🛡️ Otomatik Yönetici Yetkisi | UAC ile otomatik yetki isteme |
| 🎨 Modern Arayüz | Siber güvenlik temalı GUI |
| 📡 Otomatik Yeniden Bağlanma | Bağlantı koptuğunda otomatik |
| 🔄 Retry Mekanizması | Hata durumunda 3 kez deneme |
| 📦 Standalone EXE | Python kurulu olmadan çalışır |

---

## 🚀 Kurulum

### Gereksinimler

- **Python 3.8+** ([İndir](https://www.python.org/downloads/)) - Geliştirme için
- **Windows 10/11** (Client için)
- **Aynı ağda olma** (Admin ve Client)

### Admin Panel Kurulumu

```bash
# 1. Repoyu klonlayın
git clone https://github.com/KULLANICI_ADI/siber-guvenlik.git
cd siber-guvenlik

# 2. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 3. Admin Panel'i başlatın
python run_admin.py
```

### Windows Client Kurulumu

#### 🔴 Yöntem 1: Hazır EXE (Python Gereksiz - Tavsiye Edilen)

```batch
# EXE oluşturun (bir kez)
cd windows
build_client.bat

# Oluşan EXE: dist/SiberGuvenlikClient.exe
# Bu dosyayı hedef bilgisayara kopyalayın ve çift tıklayın
```

> 💡 EXE otomatik olarak **yönetici yetkisi** isteyecektir (UAC penceresi)

#### 🟡 Yöntem 2: Client Installer (Python Yoksa Otomatik Kurar)

```batch
cd installer
build.bat

# Oluşan dosyalar:
# - dist/Client.exe         (Ana uygulama)
# - dist/ClientInstaller.exe (Otomatik kurulum)
```

`ClientInstaller.exe` özellikleri:
- ✅ Python yoksa otomatik indirir ve kurar
- ✅ Gerekli paketleri kurar
- ✅ Hata olursa 3 kez dener
- ✅ Yönetici yetkisi ister

#### 🟢 Yöntem 3: Python ile Çalıştırma

```bash
# Windows klasörüne gidin
cd windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Client'ı başlatın
python run_client.py
```

---

## 📖 Kullanım

### 1. Admin Panel'i Başlatın
```bash
python run_admin.py
```

### 2. Bağlantı Kodunu Not Edin
- Admin Panel açıldığında **4 haneli bağlantı kodu** görüntülenir
- Bu kodu Client'a girmeniz gerekecek

### 3. Client'ı Bağlayın
1. Client uygulamasını başlatın (EXE veya Python)
2. **UAC penceresi** açılırsa "Evet" deyin
3. Admin Panel'in **IP adresini** girin
4. **4 haneli kodu** girin
5. "Bağlan" butonuna tıklayın

### 4. Uzaktan Yönetim
Bağlantı kurulduktan sonra Admin Panel'den:
- 🖥️ **EKRAN** sekmesinden canlı görüntü alın
- 🎮 **Uzaktan Kontrol** ile fare/klavye kullanın
- 💬 **MESAJLAŞMA** ile iletişim kurun
- ⚙️ **KONTROLLER** ile sistem ayarlarını değiştirin

---

## 📸 Ekran Görüntüleri

<details>
<summary>Admin Panel - Karşılama Ekranı</summary>

```
┌─────────────────────────────────────────┐
│            ADMIN PANELI                 │
│    Siber Güvenlik Eğitim Projesi       │
│                                         │
│         Sunucu IP: 192.168.1.x         │
│         Bağlantı Kodu: 1234            │
│                                         │
│       [SUNUCUYU BAŞLAT]                │
└─────────────────────────────────────────┘
```
</details>

<details>
<summary>Admin Panel - Kontrol Paneli</summary>

```
┌─────────────────────────────────────────┐
│  KONTROLLER | MESAJLAŞMA | EKRAN        │
├─────────────────────────────────────────┤
│  GÜÇ KONTROLLERİ                       │
│  [PC'yi Kapat] [Yeniden Başlat]        │
├─────────────────────────────────────────┤
│  SİSTEM KONTROLLERİ                    │
│  Task Manager: [ON/OFF]  CMD: [ON/OFF] │
│  Ekran Gizle: [ON/OFF]   TP: [ON/OFF]  │
└─────────────────────────────────────────┘
```
</details>

---

## 📁 Proje Yapısı

```
siber-guvenlik/
├── 📄 README.md              # Bu dosya
├── 📄 requirements.txt       # Python bağımlılıkları
├── 📄 run_admin.py          # Admin başlatıcı
├── 📄 run_client.py         # Client başlatıcı (geliştirme)
├── 📄 build_client.py       # EXE oluşturma (UAC destekli)
│
├── 📂 admin/                 # Admin Panel kodu
│   ├── __init__.py
│   ├── admin_gui.py         # Admin arayüzü
│   └── server.py            # Sunucu mantığı
│
├── 📂 client/                # Client kodu
│   ├── __init__.py
│   ├── client.py            # Client mantığı
│   └── client_gui.py        # Client arayüzü
│
├── 📂 shared/                # Ortak modüller
│   ├── __init__.py
│   └── protocol.py          # İletişim protokolü
│
├── 📂 installer/             # 🆕 Otomatik kurulum sistemi
│   ├── README.md            # Installer kullanım rehberi
│   ├── bootstrap.py         # Akıllı kurulum scripti
│   ├── build_exe.py         # Gelişmiş build scripti
│   ├── build.bat            # Tek tıkla build
│   └── client_admin.xml     # Windows manifest (yönetici yetkisi)
│
└── 📂 windows/               # Windows dağıtım paketi
    ├── README.md            # Windows kurulum rehberi
    ├── build_client.bat     # EXE oluşturma scripti (UAC destekli)
    ├── run_client.bat       # Hızlı çalıştırma
    ├── requirements.txt     # Windows bağımlılıkları
    └── ...
```

---

## 🔧 Kontrol Komutları

| Komut | Açıklama |
|-------|----------|
| `shutdown` | Client PC'yi kapatır |
| `restart` | Client PC'yi yeniden başlatır |
| `disable_taskmgr` | Görev Yöneticisini devre dışı bırakır |
| `enable_taskmgr` | Görev Yöneticisini etkinleştirir |
| `disable_cmd` | CMD'yi devre dışı bırakır |
| `enable_cmd` | CMD'yi etkinleştirir |
| `disable_touchpad` | Touchpad'i devre dışı bırakır |
| `enable_touchpad` | Touchpad'i etkinleştirir |
| `hide_screen` | Ekranı karartır |
| `show_screen` | Ekranı gösterir |
| `kill_active_app` | Aktif uygulamayı kapatır (Alt+F4) |
| `screenshot` | Ekran görüntüsü alır |
| `start_stream` | Canlı ekran akışı başlatır |
| `stop_stream` | Canlı ekran akışını durdurur |

---

## 🛡️ Yönetici Yetkisi (UAC)

Bu uygulama bazı sistem kontrolleri için **yönetici yetkileri** gerektirir:

- Görev Yöneticisi kontrolü
- CMD kontrolü
- Touchpad kontrolü
- Ekran gizleme

EXE dosyaları `--uac-admin` flag'i ile build edildiğinde:
1. Windows otomatik olarak UAC penceresi gösterir
2. Kullanıcı "Evet" derse uygulama yönetici olarak çalışır
3. Tüm sistem kontrolleri aktif olur

---

## 🤝 Katkıda Bulunma

1. Bu repoyu **fork** edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'i push edin (`git push origin feature/AmazingFeature`)
5. **Pull Request** açın

---

## 📜 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## ⚠️ Sorumluluk Reddi

Bu yazılım **yalnızca eğitim amaçlı** geliştirilmiştir. 

- ✅ Kendi sistemlerinizde test edebilirsiniz
- ✅ Eğitim ortamlarında kullanabilirsiniz
- ❌ Yetkisiz sistemlerde kullanmak **yasadışıdır**

Yazılımın kötüye kullanımından doğacak sonuçlardan **kullanıcı sorumludur**.

---

<div align="center">

**Siber Güvenlik Eğitim Projesi** © 2024

</div>

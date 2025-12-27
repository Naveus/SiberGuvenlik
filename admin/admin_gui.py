"""
Siber Guvenlik Egitim Projesi - Admin GUI
Ana yonetim paneli arayuzu (Pro Edition - v2)
"""

import sys
import os
import base64
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QGroupBox, QGridLayout,
    QMessageBox, QTabWidget, QFrame, QSizePolicy, QSpacerItem, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPixmap, QImage

# Path ayari
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin.server import AdminServer
from shared.protocol import CommandType, get_local_ip


class SignalHandler(QObject):
    client_connected = pyqtSignal(tuple)
    client_disconnected = pyqtSignal()
    message_received = pyqtSignal(object)
    log_received = pyqtSignal(str)


class ToggleSwitch(QWidget):
    """Modern toggle switch widget"""
    toggled = pyqtSignal(bool)

    def __init__(self, label="", parent=None):
        super().__init__(parent)
        self._checked = False
        self._label = label
        self.setFixedHeight(50)
        self.setMinimumWidth(200)
        self.setCursor(Qt.PointingHandCursor)
        
    def isChecked(self):
        return self._checked
    
    def setChecked(self, checked):
        self._checked = checked
        self.update()
        
    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.toggled.emit(self._checked)
        self.update()
        
    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
        from PyQt5.QtCore import QRectF
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Label
        if self._label:
            painter.setPen(QColor("#e0e8ff"))
            painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
            painter.drawText(0, 0, 120, 40, Qt.AlignVCenter | Qt.AlignLeft, self._label)
            offset = 130
        else:
            offset = 0
        
        # Track (arka plan)
        track_width = 56
        track_height = 28
        track_x = offset
        track_y = 6
        
        if self._checked:
            track_color = QColor("#00d4ff")
        else:
            track_color = QColor("#3a3a6a")
            
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(track_x, track_y, track_width, track_height, 14, 14)
        
        # Knob (yuvarlak düğme)
        knob_size = 22
        knob_y = track_y + 3
        if self._checked:
            knob_x = track_x + track_width - knob_size - 3
            knob_color = QColor("#0a0a1a")
        else:
            knob_x = track_x + 3
            knob_color = QColor("#8080aa")
            
        painter.setBrush(QBrush(knob_color))
        painter.drawEllipse(knob_x, knob_y, knob_size, knob_size)
        
        # Status text
        status_x = offset + track_width + 12
        if self._checked:
            painter.setPen(QColor("#00d4ff"))
            status_text = "ACIK"
        else:
            painter.setPen(QColor("#8080aa"))
            status_text = "KAPALI"
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(status_x, 0, 80, 40, Qt.AlignVCenter | Qt.AlignLeft, status_text)


class AdminGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.server = AdminServer()
        self.signals = SignalHandler()
        self.is_streaming = False
        self.is_remote_control_enabled = False

        self.signals.client_connected.connect(self._on_client_connected)
        self.signals.client_disconnected.connect(self._on_client_disconnected)
        self.signals.message_received.connect(self._on_message_received)
        self.signals.log_received.connect(self._add_log)

        self.server.on_client_connected = lambda addr: self.signals.client_connected.emit(addr)
        self.server.on_client_disconnected = lambda: self.signals.client_disconnected.emit()
        self.server.on_message_received = lambda msg: self.signals.message_received.emit(msg)
        self.server.on_log = lambda msg: self.signals.log_received.emit(msg)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Siber Guvenlik - Admin Paneli")
        self.setMinimumSize(1000, 750)
        self.setStyleSheet(self._get_stylesheet())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Stacked Widget - Sayfa geçişleri
        self.pages = QStackedWidget()
        self.pages.addWidget(self._create_welcome_page())  # Sayfa 0
        self.pages.addWidget(self._create_main_page())     # Sayfa 1
        self.pages.addWidget(self._create_logs_page())     # Sayfa 2
        main_layout.addWidget(self.pages)

    # ==================== SAYFA 0: KARSILAMA ====================
    def _create_welcome_page(self):
        page = QWidget()
        page.setObjectName("welcomePage")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        # Orta kutu
        box = QFrame()
        box.setObjectName("welcomeBox")
        box.setFixedSize(500, 450)
        box_layout = QVBoxLayout(box)
        box_layout.setSpacing(25)
        box_layout.setContentsMargins(50, 50, 50, 50)

        # Başlık
        title = QLabel("ADMIN PANELI")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(title)

        subtitle = QLabel("Siber Güvenlik Eğitim Projesi")
        subtitle.setObjectName("welcomeSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(subtitle)

        box_layout.addSpacing(20)

        # IP Adresi
        ip_label = QLabel(f"Sunucu IP: {get_local_ip()}")
        ip_label.setObjectName("ipDisplay")
        ip_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(ip_label)

        # Bağlantı Kodu
        self.welcome_code_label = QLabel("------")
        self.welcome_code_label.setObjectName("welcomeCodeLabel")
        self.welcome_code_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(self.welcome_code_label)

        # Durum
        self.welcome_status = QLabel("Sunucuyu başlatın...")
        self.welcome_status.setObjectName("welcomeStatus")
        self.welcome_status.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(self.welcome_status)

        box_layout.addSpacing(20)

        # Başlat butonu
        self.welcome_start_btn = QPushButton("SUNUCUYU BASLAT")
        self.welcome_start_btn.setObjectName("bigSuccessBtn")
        self.welcome_start_btn.setFixedHeight(60)
        self.welcome_start_btn.clicked.connect(self._start_server)
        box_layout.addWidget(self.welcome_start_btn)

        layout.addWidget(box)
        return page

    # ==================== SAYFA 1: ANA KONTROL ====================
    def _create_main_page(self):
        page = QWidget()
        page.setObjectName("mainPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Üst bar - minimal
        top_bar = QHBoxLayout()
        
        self.main_status = QLabel("Bagli: --")
        self.main_status.setObjectName("mainStatus")
        top_bar.addWidget(self.main_status)
        
        top_bar.addStretch()
        
        logs_btn = QPushButton("Loglar")
        logs_btn.setObjectName("secondaryBtn")
        logs_btn.setFixedHeight(35)
        logs_btn.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        top_bar.addWidget(logs_btn)
        
        stop_btn = QPushButton("Sunucuyu Durdur")
        stop_btn.setObjectName("dangerBtn")
        stop_btn.setFixedHeight(35)
        stop_btn.clicked.connect(self._stop_and_go_welcome)
        top_bar.addWidget(stop_btn)
        
        layout.addLayout(top_bar)

        # Tab widget - tam ekran
        tabs = QTabWidget()
        tabs.setObjectName("mainTabs")
        tabs.addTab(self._create_control_tab(), "  KONTROLLER  ")
        tabs.addTab(self._create_chat_tab(), "  MESAJLASMA  ")
        tabs.addTab(self._create_screen_tab(), "  EKRAN  ")
        layout.addWidget(tabs)

        return page

    # ==================== SAYFA 2: LOGLAR ====================
    def _create_logs_page(self):
        page = QWidget()
        page.setObjectName("logsPage")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Üst bar
        top_bar = QHBoxLayout()
        
        title = QLabel("SISTEM LOGLARI")
        title.setObjectName("pageTitle")
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        back_btn = QPushButton("Geri")
        back_btn.setObjectName("secondaryBtn")
        back_btn.setFixedHeight(35)
        back_btn.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        top_bar.addWidget(back_btn)
        
        layout.addLayout(top_bar)

        # Log alanı
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText("Loglar burada gorunecek...")
        layout.addWidget(self.log_display)

        # Temizle butonu
        clear_btn = QPushButton("Loglari Temizle")
        clear_btn.setObjectName("warningBtn")
        clear_btn.setFixedHeight(40)
        clear_btn.clicked.connect(lambda: self.log_display.clear())
        layout.addWidget(clear_btn)

        return page

    # ==================== KONTROLLER TAB ====================
    def _create_control_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ==================== 1. GÜÇ KONTROLLERİ ====================
        power_group = self._create_group("GUC KONTROLLERI")
        power_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        power_layout = power_group.layout()
        power_layout.addStretch()
        
        power_btn_layout = QHBoxLayout()
        power_btn_layout.setSpacing(15)
        
        shutdown_btn = QPushButton("PC'yi Kapat")
        shutdown_btn.setObjectName("dangerBtn")
        shutdown_btn.setMinimumHeight(50)
        shutdown_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        shutdown_btn.clicked.connect(self._shutdown_client)
        power_btn_layout.addWidget(shutdown_btn)

        restart_btn = QPushButton("Yeniden Baslat")
        restart_btn.setObjectName("warningBtn")
        restart_btn.setMinimumHeight(50)
        restart_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        restart_btn.clicked.connect(self._restart_client)
        power_btn_layout.addWidget(restart_btn)
        
        power_layout.addLayout(power_btn_layout)
        power_layout.addStretch()
        main_layout.addWidget(power_group, 1)

        # ==================== 2. TEHLİKELİ İŞLEMLER ====================
        danger_group = self._create_group("TEHLIKELI ISLEMLER")
        danger_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        danger_layout = danger_group.layout()
        danger_layout.addStretch()
        
        uninstall_btn = QPushButton("Client'i Tamamen Kaldir")
        uninstall_btn.setObjectName("dangerBtn")
        uninstall_btn.setMinimumHeight(50)
        uninstall_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        uninstall_btn.clicked.connect(self._uninstall_client)
        danger_layout.addWidget(uninstall_btn)
        
        danger_layout.addStretch()
        main_layout.addWidget(danger_group, 1)

        # ==================== 3. UYARI MESAJI ====================
        alert_group = self._create_group("UYARI MESAJI")
        alert_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        alert_layout = alert_group.layout()
        alert_layout.addStretch()
        
        self.alert_title_input = QLineEdit()
        self.alert_title_input.setPlaceholderText("Baslik")
        self.alert_title_input.setMinimumHeight(45)
        alert_layout.addWidget(self.alert_title_input)

        self.alert_msg_input = QLineEdit()
        self.alert_msg_input.setPlaceholderText("Mesaj")
        self.alert_msg_input.setMinimumHeight(45)
        alert_layout.addWidget(self.alert_msg_input)

        alert_btn_layout = QHBoxLayout()
        alert_btn_layout.setSpacing(15)
        
        alert_btn = QPushButton("Gonder")
        alert_btn.setObjectName("primaryBtn")
        alert_btn.setMinimumHeight(45)
        alert_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        alert_btn.clicked.connect(self._send_alert)
        alert_btn_layout.addWidget(alert_btn)

        spam_btn = QPushButton("Spam (5x)")
        spam_btn.setObjectName("warningBtn")
        spam_btn.setMinimumHeight(45)
        spam_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spam_btn.clicked.connect(self._spam_alert)
        alert_btn_layout.addWidget(spam_btn)
        
        alert_layout.addLayout(alert_btn_layout)
        alert_layout.addStretch()
        main_layout.addWidget(alert_group, 1)

        # ==================== 4. SİSTEM VE GİRİŞ KONTROLLERİ ====================
        toggle_group = self._create_group("SISTEM VE GIRIS KONTROLLERI")
        toggle_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toggle_layout = toggle_group.layout()
        toggle_layout.addStretch()

        # === İLK SATIR ===
        toggle_row1 = QHBoxLayout()
        toggle_row1.setSpacing(15)

        # Task Manager toggle box
        tm_box = QFrame()
        tm_box.setObjectName("toggleBox")
        tm_box_layout = QVBoxLayout(tm_box)
        tm_box_layout.setAlignment(Qt.AlignCenter)
        self.tm_toggle = ToggleSwitch("Task Manager")
        self.tm_toggle.toggled.connect(self._on_tm_toggle)
        tm_box_layout.addWidget(self.tm_toggle)
        toggle_row1.addWidget(tm_box, 1)

        # CMD toggle box
        cmd_box = QFrame()
        cmd_box.setObjectName("toggleBox")
        cmd_box_layout = QVBoxLayout(cmd_box)
        cmd_box_layout.setAlignment(Qt.AlignCenter)
        self.cmd_toggle = ToggleSwitch("CMD")
        self.cmd_toggle.toggled.connect(self._on_cmd_toggle)
        cmd_box_layout.addWidget(self.cmd_toggle)
        toggle_row1.addWidget(cmd_box, 1)

        # Aktif Uygulama Kapat box
        kill_box = QFrame()
        kill_box.setObjectName("toggleBox")
        kill_box_layout = QVBoxLayout(kill_box)
        kill_box_layout.setAlignment(Qt.AlignCenter)
        kill_btn = QPushButton("Aktif Uygulamayi Kapat")
        kill_btn.setObjectName("dangerBtn")
        kill_btn.setFixedHeight(40)
        kill_btn.clicked.connect(self._kill_active_app)
        kill_box_layout.addWidget(kill_btn)
        toggle_row1.addWidget(kill_box, 1)

        toggle_layout.addLayout(toggle_row1)

        # === İKİNCİ SATIR ===
        toggle_row2 = QHBoxLayout()
        toggle_row2.setSpacing(15)

        # Touchpad toggle box (Fn+F10)
        touchpad_box = QFrame()
        touchpad_box.setObjectName("toggleBox")
        touchpad_box_layout = QVBoxLayout(touchpad_box)
        touchpad_box_layout.setAlignment(Qt.AlignCenter)
        self.touchpad_toggle = ToggleSwitch("Touchpad")
        self.touchpad_toggle.toggled.connect(self._on_touchpad_toggle)
        touchpad_box_layout.addWidget(self.touchpad_toggle)
        toggle_row2.addWidget(touchpad_box, 1)

        # Klavye toggle box
        keyboard_box = QFrame()
        keyboard_box.setObjectName("toggleBox")
        keyboard_box_layout = QVBoxLayout(keyboard_box)
        keyboard_box_layout.setAlignment(Qt.AlignCenter)
        self.keyboard_toggle = ToggleSwitch("Klavye")
        self.keyboard_toggle.toggled.connect(self._on_keyboard_toggle)
        keyboard_box_layout.addWidget(self.keyboard_toggle)
        toggle_row2.addWidget(keyboard_box, 1)

        # Ekran Gizleme toggle box
        screen_box = QFrame()
        screen_box.setObjectName("toggleBox")
        screen_box_layout = QVBoxLayout(screen_box)
        screen_box_layout.setAlignment(Qt.AlignCenter)
        self.screen_toggle = ToggleSwitch("Ekran Gizle")
        self.screen_toggle.toggled.connect(self._on_screen_toggle)
        screen_box_layout.addWidget(self.screen_toggle)
        toggle_row2.addWidget(screen_box, 1)

        toggle_layout.addLayout(toggle_row2)
        toggle_layout.addStretch()
        main_layout.addWidget(toggle_group, 1)

        return widget

    # ==================== MESAJLASMA TAB ====================
    def _create_chat_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("Mesajlar burada gorunecek...")
        layout.addWidget(self.chat_display)

        send_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Mesajinizi yazin...")
        self.chat_input.setFixedHeight(50)
        self.chat_input.returnPressed.connect(self._send_chat_message)
        send_layout.addWidget(self.chat_input)

        send_btn = QPushButton("Gonder")
        send_btn.setObjectName("primaryBtn")
        send_btn.setFixedWidth(120)
        send_btn.setFixedHeight(50)
        send_btn.clicked.connect(self._send_chat_message)
        send_layout.addWidget(send_btn)

        layout.addLayout(send_layout)
        return widget

    # ==================== EKRAN TAB ====================
    def _create_screen_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Ekran alanı
        self.screen_label = QLabel("Canli ekran icin 'Akisi Baslat' butonuna basin")
        self.screen_label.setObjectName("screenLabel")
        self.screen_label.setAlignment(Qt.AlignCenter)
        self.screen_label.setMinimumHeight(400)
        self.screen_label.setMouseTracking(True)
        self.screen_label.mousePressEvent = self._on_screen_click
        layout.addWidget(self.screen_label)

        # Kontrol butonları
        controls = QHBoxLayout()
        
        self.start_stream_btn = QPushButton("Akisi Baslat")
        self.start_stream_btn.setObjectName("successBtn")
        self.start_stream_btn.setFixedHeight(45)
        self.start_stream_btn.clicked.connect(self._start_stream)
        controls.addWidget(self.start_stream_btn)

        self.stop_stream_btn = QPushButton("Akisi Durdur")
        self.stop_stream_btn.setObjectName("dangerBtn")
        self.stop_stream_btn.setFixedHeight(45)
        self.stop_stream_btn.setEnabled(False)
        self.stop_stream_btn.clicked.connect(self._stop_stream)
        controls.addWidget(self.stop_stream_btn)

        controls.addStretch()

        screenshot_btn = QPushButton("Ekran Goruntusu")
        screenshot_btn.setObjectName("primaryBtn")
        screenshot_btn.setFixedHeight(45)
        screenshot_btn.clicked.connect(self._request_screenshot)
        controls.addWidget(screenshot_btn)

        controls.addStretch()

        self.remote_control_btn = QPushButton("Uzaktan Kontrol: KAPALI")
        self.remote_control_btn.setObjectName("warningBtn")
        self.remote_control_btn.setFixedHeight(45)
        self.remote_control_btn.setCheckable(True)
        self.remote_control_btn.clicked.connect(self._toggle_remote_control)
        controls.addWidget(self.remote_control_btn)

        layout.addLayout(controls)

        # Klavye Kontrolü
        keyboard_layout = QHBoxLayout()
        keyboard_layout.setSpacing(10)
        
        keyboard_label = QLabel("Klavye:")
        keyboard_label.setStyleSheet("color: #00d4ff; font-weight: bold;")
        keyboard_layout.addWidget(keyboard_label)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Yazilacak metin veya tus (enter, tab, escape...)")
        self.key_input.setFixedHeight(40)
        self.key_input.returnPressed.connect(self._send_keyboard_input)
        keyboard_layout.addWidget(self.key_input)
        
        send_key_btn = QPushButton("Gonder")
        send_key_btn.setObjectName("primaryBtn")
        send_key_btn.setFixedHeight(40)
        send_key_btn.setFixedWidth(100)
        send_key_btn.clicked.connect(self._send_keyboard_input)
        keyboard_layout.addWidget(send_key_btn)
        
        layout.addLayout(keyboard_layout)

        # Durum
        status_layout = QHBoxLayout()
        self.stream_status = QLabel("Akis: Durduruldu")
        self.stream_status.setObjectName("streamStatus")
        status_layout.addWidget(self.stream_status)
        status_layout.addStretch()
        self.fps_label = QLabel("FPS: --")
        self.fps_label.setStyleSheet("color: #666;")
        status_layout.addWidget(self.fps_label)
        layout.addLayout(status_layout)

        return widget

    def _create_group(self, title):
        group = QGroupBox()
        group.setTitle(title)
        layout = QVBoxLayout(group)
        layout.setContentsMargins(20, 25, 20, 20)
        layout.setSpacing(12)
        return group

    # ==================== SUNUCU KONTROL ====================
    def _start_server(self):
        code = self.server.start()
        if code:
            self.welcome_code_label.setText(' '.join(code))
            self.welcome_status.setText("Baglanti bekleniyor...")
            self.welcome_status.setObjectName("waitingStatus")
            self.welcome_status.setStyle(self.welcome_status.style())
            self.welcome_start_btn.setEnabled(False)
            self.welcome_start_btn.setText("BEKLENIYOR...")
            self._add_log("Sunucu baslatildi")

    def _stop_and_go_welcome(self):
        if self.is_streaming:
            self._stop_stream()
        self.server.stop()
        self.welcome_code_label.setText("------")
        self.welcome_status.setText("Sunucuyu başlatın...")
        self.welcome_status.setObjectName("welcomeStatus")
        self.welcome_status.setStyle(self.welcome_status.style())
        self.welcome_start_btn.setEnabled(True)
        self.welcome_start_btn.setText("SUNUCUYU BASLAT")
        self.pages.setCurrentIndex(0)
        self._add_log("Sunucu durduruldu")

    # ==================== CALLBACKS ====================
    def _on_client_connected(self, addr):
        self.main_status.setText(f"Bagli: {addr[0]}")
        self._add_log(f"Client baglandi: {addr[0]}:{addr[1]}")
        self._add_chat("SISTEM", f"Client baglandi: {addr[0]}")
        # Sayfa 1'e geç
        self.pages.setCurrentIndex(1)

    def _on_client_disconnected(self):
        self.main_status.setText("Baglanti kesildi")
        self._add_log("Client baglantisi kesildi")
        self._add_chat("SISTEM", "Client baglantisi kesildi")
        if self.is_streaming:
            self._stop_stream()

    def _on_message_received(self, msg):
        if msg.command == CommandType.CHAT.value:
            self._add_chat("CLIENT", msg.data.get('text', ''))
        elif msg.command == CommandType.SCREENSHOT_RESPONSE.value:
            self._display_screenshot(msg.data.get('image', ''))
        elif msg.command == CommandType.STREAM_FRAME.value:
            self._display_stream_frame(msg.data.get('image', ''))
        elif msg.command == CommandType.LOG.value:
            self._add_log(f"[CLIENT] {msg.data.get('text', '')}")

    # ==================== KOMUTLAR ====================
    def _shutdown_client(self):
        if QMessageBox.question(self, 'Onay', 'Client PC kapatilacak. Emin misiniz?',
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.server.shutdown_client()

    def _restart_client(self):
        if QMessageBox.question(self, 'Onay', 'Client PC yeniden baslatilacak. Emin misiniz?',
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.server.restart_client()

    def _send_alert(self):
        title = self.alert_title_input.text() or "Uyari"
        message = self.alert_msg_input.text() or "Bu bir uyari mesajidir!"
        self.server.send_alert(title, message)

    def _spam_alert(self):
        title = self.alert_title_input.text() or "UYARI!"
        message = self.alert_msg_input.text() or "Bu bir spam uyaridir!"
        for i in range(5):
            QTimer.singleShot(i * 500, lambda t=title, m=message: self.server.send_alert(t, m))

    def _uninstall_client(self):
        if QMessageBox.question(self, 'Tehlikeli Islem',
                                'Client tamamen silinecek!\nBu islem geri alinamaz.\n\nDevam?',
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.server.uninstall_client()

    def _send_chat_message(self):
        text = self.chat_input.text()
        if text:
            self.server.send_message(text)
            self._add_chat("ADMIN", text)
            self.chat_input.clear()

    def _request_screenshot(self):
        self.server.request_screenshot()
        self.screen_label.setText("Ekran goruntusu isteniyor...")

    def _display_screenshot(self, image_data):
        try:
            image_bytes = base64.b64decode(image_data)
            image = QImage()
            image.loadFromData(image_bytes)
            pixmap = QPixmap.fromImage(image)
            scaled = pixmap.scaled(self.screen_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.screen_label.setPixmap(scaled)
        except Exception as e:
            self.screen_label.setText(f"Hata: {e}")

    # ==================== STREAM ====================
    def _start_stream(self):
        self.server.start_stream()
        self.is_streaming = True
        self.start_stream_btn.setEnabled(False)
        self.stop_stream_btn.setEnabled(True)
        self.stream_status.setText("Akis: Aktif")
        self.stream_status.setStyleSheet("color: #2ed573; font-weight: bold;")

    def _stop_stream(self):
        self.server.stop_stream()
        self.is_streaming = False
        self.start_stream_btn.setEnabled(True)
        self.stop_stream_btn.setEnabled(False)
        self.stream_status.setText("Akis: Durduruldu")
        self.stream_status.setStyleSheet("color: #ff4757;")
        self.fps_label.setText("FPS: --")

    def _on_tm_toggle(self, checked):
        if checked:
            self.server.disable_task_manager()
            self._add_log("Task Manager devre disi birakildi")
        else:
            self.server.enable_task_manager()
            self._add_log("Task Manager etkinlestirildi")

    def _on_cmd_toggle(self, checked):
        """CMD aç/kapat - Toggle AÇIK ise CMD KAPALI demek"""
        if checked:
            self.server.disable_cmd()
            self._add_log("CMD devre disi birakildi")
        else:
            self.server.enable_cmd()
            self._add_log("CMD etkinlestirildi")

    def _kill_active_app(self):
        """Aktif uygulamayı kapat"""
        self.server.kill_active_app()
        self._add_log("Aktif uygulama kapatma komutu gonderildi (Alt+F4)")

    def _on_touchpad_toggle(self, checked):
        """Touchpad aç/kapat - Fn+F10 gönder"""
        # Her durumda Fn+F10 gönder (toggle)
        self.server.send_key_press('fn+f10')
        if checked:
            self._add_log("Touchpad kapatma komutu gonderildi (Fn+F10)")
        else:
            self._add_log("Touchpad acma komutu gonderildi (Fn+F10)")

    def _on_keyboard_toggle(self, checked):
        if checked:
            self.server.disable_keyboard()
            self._add_log("Klavye devre disi birakildi")
        else:
            self.server.enable_keyboard()
            self._add_log("Klavye etkinlestirildi")

    def _on_screen_toggle(self, checked):
        """Ekranı gizle/göster"""
        if checked:
            self.server.hide_screen()
            self._add_log("Ekran gizleme komutu gonderildi")
        else:
            self.server.show_screen()
            self._add_log("Ekran gosterme komutu gonderildi")

    def _toggle_remote_control(self):
        self.is_remote_control_enabled = self.remote_control_btn.isChecked()
        if self.is_remote_control_enabled:
            self.remote_control_btn.setText("Uzaktan Kontrol: ACIK")
            self.remote_control_btn.setObjectName("successBtn")
        else:
            self.remote_control_btn.setText("Uzaktan Kontrol: KAPALI")
            self.remote_control_btn.setObjectName("warningBtn")
        self.remote_control_btn.setStyle(self.remote_control_btn.style())

    def _send_keyboard_input(self):
        text = self.key_input.text()
        if not text:
            return
        
        if not self.is_remote_control_enabled:
            self._add_log("Once Uzaktan Kontrol'u aciniz!")
            return
        
        # Tek tuş mu yoksa metin mi kontrol et
        special_keys = ['enter', 'tab', 'escape', 'backspace', 'delete', 'space',
                        'up', 'down', 'left', 'right', 'home', 'end', 'pageup', 'pagedown',
                        'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']
        
        if text.lower() in special_keys:
            # Tek özel tuş gönder
            self.server.send_key_press(text.lower())
            self._add_log(f"Tus gonderildi: {text}")
        else:
            # Her karakteri teker teker gönder
            for char in text:
                self.server.send_key_press(char)
            self._add_log(f"Metin gonderildi: {text}")
        
        self.key_input.clear()

    def _on_screen_click(self, event):
        if not self.is_remote_control_enabled or not self.is_streaming:
            return
        
        # Pixmap'in gerçek boyutunu ve konumunu hesapla
        pixmap = self.screen_label.pixmap()
        if not pixmap:
            return
            
        # Label ve pixmap boyutları
        label_w = self.screen_label.width()
        label_h = self.screen_label.height()
        pix_w = pixmap.width()
        pix_h = pixmap.height()
        
        # Pixmap'in label içindeki offset'i (ortalama nedeniyle)
        offset_x = (label_w - pix_w) // 2
        offset_y = (label_h - pix_h) // 2
        
        # Tıklama koordinatları
        click_x = event.pos().x()
        click_y = event.pos().y()
        
        # Pixmap sınırları içinde mi kontrol et
        if click_x < offset_x or click_x > offset_x + pix_w:
            return
        if click_y < offset_y or click_y > offset_y + pix_h:
            return
        
        # Pixmap içindeki koordinat
        rel_x = click_x - offset_x
        rel_y = click_y - offset_y
        
        from PyQt5.QtCore import Qt
        button = 'left' if event.button() == Qt.LeftButton else 'right'
        self.server.send_mouse_click(rel_x, rel_y, pix_w, pix_h, button)

    def _display_stream_frame(self, image_data):
        try:
            image_bytes = base64.b64decode(image_data)
            image = QImage()
            image.loadFromData(image_bytes)
            pixmap = QPixmap.fromImage(image)
            scaled = pixmap.scaled(self.screen_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.screen_label.setPixmap(scaled)
        except:
            pass

    def _add_chat(self, sender, message):
        ts = datetime.now().strftime("%H:%M:%S")
        color = "#00d4ff" if sender == "ADMIN" else "#2ed573" if sender == "CLIENT" else "#ffa502"
        self.chat_display.append(f'<span style="color:#555">[{ts}]</span> '
                                  f'<span style="color:{color};font-weight:bold">{sender}:</span> {message}')

    def _add_log(self, message):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_display.append(f'<span style="color:#555">[{ts}]</span> {message}')

    def closeEvent(self, event):
        if self.is_streaming:
            self._stop_stream()
        self.server.stop()
        event.accept()

    # ==================== STIL ====================
    def _get_stylesheet(self):
        return """
            /* ========== SIBER GUVENLIK - MAVI MOR TEMA ========== */
            
            /* GENEL - Derin lacivert arka plan */
            QMainWindow, QWidget { 
                background: #0a0a1a;
                color: #e0e8ff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }

            /* KARSILAMA SAYFASI */
            #welcomePage {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0a1a, stop:0.5 #151530, stop:1 #0a0a1a);
            }
            #welcomeBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a35, stop:1 #12122a);
                border: 2px solid #00d4ff;
                border-radius: 20px;
            }
            #welcomeTitle {
                font-size: 36px;
                font-weight: bold;
                color: #00d4ff;
                letter-spacing: 4px;
            }
            #welcomeSubtitle {
                font-size: 13px;
                color: #8080aa;
                letter-spacing: 2px;
            }
            #ipDisplay {
                font-size: 15px;
                color: #a0a0cc;
            }
            #welcomeCodeLabel {
                font-size: 64px;
                font-weight: bold;
                color: #00d4ff;
                font-family: 'Consolas', monospace;
                letter-spacing: 16px;
            }
            #welcomeStatus, #waitingStatus {
                font-size: 14px;
                color: #8080aa;
            }
            #waitingStatus {
                color: #bb86fc;
            }
            #bigSuccessBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099cc);
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 2px;
                color: #0a0a1a;
            }
            #bigSuccessBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #33ddff, stop:1 #00bbee);
            }
            #bigSuccessBtn:disabled {
                background: #2a2a4a;
                color: #5a5a7a;
            }

            /* ANA SAYFA */
            #mainPage, #logsPage {
                background: transparent;
            }
            #mainStatus {
                font-size: 15px;
                font-weight: bold;
                color: #00d4ff;
            }
            #pageTitle {
                font-size: 22px;
                font-weight: bold;
                color: #00d4ff;
                letter-spacing: 3px;
            }

            /* GRUPLAR */
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a35, stop:1 #12122a);
                border: 1px solid #3a3a6a;
                border-radius: 12px;
                margin-top: 18px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 18px; top: 6px;
                color: #00d4ff;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 2px;
            }

            /* BUTONLAR */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a4a, stop:1 #1a1a35);
                border: 1px solid #4a4a7a;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 12px;
                font-weight: bold;
                color: #c0c8e8;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a3a5a, stop:1 #2a2a45);
                border-color: #6a6a9a;
                color: #ffffff;
            }
            QPushButton:pressed { 
                background: #15152a; 
            }
            QPushButton:disabled { 
                background: #1a1a2a; 
                color: #4a4a6a; 
                border-color: #2a2a4a; 
            }

            #primaryBtn { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00d4ff, stop:1 #0099cc);
                border: none;
                color: #0a0a1a;
            }
            #primaryBtn:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #33ddff, stop:1 #00bbee);
            }
            
            #successBtn { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00cc88, stop:1 #009966);
                border: none;
                color: #0a0a1a;
            }
            #successBtn:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00eebb, stop:1 #00bb88);
            }
            
            #warningBtn { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #bb86fc, stop:1 #9966dd);
                border: none;
                color: #0a0a1a;
            }
            #warningBtn:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #cc99ff, stop:1 #aa77ee);
            }
            
            #dangerBtn { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #ff5566, stop:1 #cc3344);
                border: none;
                color: #ffffff;
            }
            #dangerBtn:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #ff7788, stop:1 #ee4455);
            }
            
            #secondaryBtn { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a4a, stop:1 #1a1a35);
                border: 1px solid #4a4a7a; 
            }
            #secondaryBtn:hover { 
                background: #3a3a5a;
                border-color: #00d4ff;
            }

            /* INPUT */
            QLineEdit {
                background: #12122a;
                border: 2px solid #3a3a6a;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #e0e8ff;
                selection-background-color: #00d4ff;
            }
            QLineEdit:focus { 
                border-color: #00d4ff;
                background: #1a1a35;
            }

            QTextEdit {
                background: #12122a;
                border: 2px solid #3a3a6a;
                border-radius: 10px;
                padding: 14px;
                font-size: 13px;
                color: #e0e8ff;
            }
            QTextEdit:focus {
                border-color: #00d4ff;
            }

            #screenLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #0a0a1a, stop:1 #050510);
                border: 2px solid #3a3a6a;
                border-radius: 12px;
            }

            /* TABS */
            QTabWidget::pane {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a35, stop:1 #12122a);
                border: 1px solid #3a3a6a;
                border-radius: 12px;
                top: -1px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a4a, stop:1 #1a1a35);
                border: 1px solid #3a3a6a;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
                padding: 12px 28px;
                margin-right: 4px;
                font-weight: bold;
                letter-spacing: 1px;
                color: #8080aa;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099cc);
                color: #0a0a1a;
                border-color: #00d4ff;
            }
            QTabBar::tab:hover:!selected { 
                background: #3a3a5a;
                color: #00d4ff;
            }

            /* SCROLLBAR */
            QScrollBar:vertical {
                background: #12122a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a4a7a, stop:1 #3a3a6a);
                border-radius: 6px;
                min-height: 40px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00d4ff;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }

            /* TOGGLE BOX */
            #toggleBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a35, stop:1 #12122a);
                border: 1px solid #3a3a6a;
                border-radius: 10px;
                padding: 15px;
            }
            #toggleBox:hover {
                border-color: #5a5a8a;
            }
        """


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = AdminGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

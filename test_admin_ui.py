"""
Siber Guvenlik - Test Admin UI
Bağlantı gerektirmeden sadece UI test etmek için
"""

import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QGroupBox, QGridLayout,
    QMessageBox, QTabWidget, QFrame, QSizePolicy, QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class ToggleSwitch(QWidget):
    """Modern toggle switch widget"""
    toggled = pyqtSignal(bool)
    
    def __init__(self, label="", parent=None):
        super().__init__(parent)
        self._checked = False
        self._label = label
        self.setFixedHeight(40)
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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self._label:
            painter.setPen(QColor("#e0e8ff"))
            painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
            painter.drawText(0, 0, 120, 40, Qt.AlignVCenter | Qt.AlignLeft, self._label)
            offset = 130
        else:
            offset = 0
        
        track_width, track_height = 56, 28
        track_x, track_y = offset, 6
        
        track_color = QColor("#00d4ff") if self._checked else QColor("#3a3a6a")
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(track_x, track_y, track_width, track_height, 14, 14)
        
        knob_size, knob_y = 22, track_y + 3
        knob_x = track_x + track_width - knob_size - 3 if self._checked else track_x + 3
        knob_color = QColor("#0a0a1a") if self._checked else QColor("#8080aa")
        painter.setBrush(QBrush(knob_color))
        painter.drawEllipse(knob_x, knob_y, knob_size, knob_size)
        
        status_x = offset + track_width + 12
        painter.setPen(QColor("#00d4ff") if self._checked else QColor("#8080aa"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(status_x, 0, 80, 40, Qt.AlignVCenter | Qt.AlignLeft, 
                        "ACIK" if self._checked else "KAPALI")


class TestAdminGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Siber Guvenlik - Test Admin Panel")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(self._get_stylesheet())

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Üst Bar
        top_bar = QHBoxLayout()
        status = QLabel("TEST MODU - Bagli: 192.168.1.xxx")
        status.setStyleSheet("color: #00d4ff; font-size: 15px; font-weight: bold;")
        top_bar.addWidget(status)
        top_bar.addStretch()
        
        logs_btn = QPushButton("Loglar")
        logs_btn.setObjectName("secondaryBtn")
        logs_btn.setFixedWidth(100)
        logs_btn.clicked.connect(lambda: self._add_log("Loglar butonu tiklandi"))
        top_bar.addWidget(logs_btn)
        layout.addLayout(top_bar)

        # Tab Widget
        tabs = QTabWidget()
        tabs.addTab(self._create_control_tab(), "KONTROLLER")
        tabs.addTab(self._create_chat_tab(), "MESAJLASMA")
        tabs.addTab(self._create_screen_tab(), "EKRAN")
        layout.addWidget(tabs)

        # Log alanı
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(120)
        self.log_area.setPlaceholderText("Loglar burada gorunecek...")
        layout.addWidget(self.log_area)
        
        self._add_log("Test Admin Panel baslatildi")

    def _create_group(self, title):
        group = QGroupBox(title)
        group.setLayout(QVBoxLayout())
        group.layout().setSpacing(10)
        group.layout().setContentsMargins(15, 25, 15, 15)
        return group

    def _create_control_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        top_grid = QGridLayout()
        top_grid.setSpacing(20)
        top_grid.setColumnStretch(0, 1)
        top_grid.setColumnStretch(1, 1)

        # Güç Kontrolleri
        power_group = self._create_group("GUC KONTROLLERI")
        power_grid = QGridLayout()
        power_grid.setSpacing(12)
        
        shutdown_btn = QPushButton("PC'yi Kapat")
        shutdown_btn.setObjectName("dangerBtn")
        shutdown_btn.setFixedHeight(48)
        shutdown_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        shutdown_btn.clicked.connect(lambda: self._add_log("PC kapatma komutu gonderildi"))
        power_grid.addWidget(shutdown_btn, 0, 0)

        restart_btn = QPushButton("Yeniden Baslat")
        restart_btn.setObjectName("warningBtn")
        restart_btn.setFixedHeight(48)
        restart_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        restart_btn.clicked.connect(lambda: self._add_log("Yeniden baslatma komutu gonderildi"))
        power_grid.addWidget(restart_btn, 0, 1)
        
        power_group.layout().addLayout(power_grid)
        top_grid.addWidget(power_group, 0, 0)

        # Tehlikeli
        danger_group = self._create_group("TEHLIKELI ISLEMLER")
        uninstall_btn = QPushButton("Client'i Tamamen Kaldir")
        uninstall_btn.setObjectName("dangerBtn")
        uninstall_btn.setFixedHeight(48)
        uninstall_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        uninstall_btn.clicked.connect(lambda: self._add_log("Kaldirma komutu gonderildi"))
        danger_group.layout().addWidget(uninstall_btn)
        top_grid.addWidget(danger_group, 0, 1)

        # Uyarı Mesajı
        alert_group = self._create_group("UYARI MESAJI")
        self.alert_title = QLineEdit()
        self.alert_title.setPlaceholderText("Baslik")
        self.alert_title.setFixedHeight(42)
        alert_group.layout().addWidget(self.alert_title)

        self.alert_msg = QLineEdit()
        self.alert_msg.setPlaceholderText("Mesaj")
        self.alert_msg.setFixedHeight(42)
        alert_group.layout().addWidget(self.alert_msg)

        alert_btn_grid = QGridLayout()
        alert_btn_grid.setSpacing(12)
        
        alert_btn = QPushButton("Gonder")
        alert_btn.setObjectName("primaryBtn")
        alert_btn.setFixedHeight(42)
        alert_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        alert_btn.clicked.connect(lambda: self._add_log(f"Uyari gonderildi: {self.alert_title.text()}"))
        alert_btn_grid.addWidget(alert_btn, 0, 0)

        spam_btn = QPushButton("Spam (5x)")
        spam_btn.setObjectName("warningBtn")
        spam_btn.setFixedHeight(42)
        spam_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        spam_btn.clicked.connect(lambda: self._add_log("Spam gonderildi (5x)"))
        alert_btn_grid.addWidget(spam_btn, 0, 1)
        
        alert_group.layout().addLayout(alert_btn_grid)
        top_grid.addWidget(alert_group, 1, 0)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        top_grid.addWidget(spacer, 1, 1)

        main_layout.addLayout(top_grid)

        # Toggle Switch Paneli
        toggle_group = self._create_group("SISTEM VE GIRIS KONTROLLERI")
        toggle_grid = QGridLayout()
        toggle_grid.setSpacing(20)
        for i in range(4):
            toggle_grid.setColumnStretch(i, 1)
        
        toggles = [("Task Manager", "tm"), ("CMD", "cmd"), ("Fare", "mouse"), ("Klavye", "keyboard")]
        for i, (label, name) in enumerate(toggles):
            toggle = ToggleSwitch(label)
            toggle.toggled.connect(lambda c, n=name: self._add_log(f"{n}: {'Kapali' if c else 'Acik'}"))
            toggle_grid.addWidget(toggle, 0, i, Qt.AlignCenter)
        
        toggle_group.layout().addLayout(toggle_grid)
        main_layout.addWidget(toggle_group)
        main_layout.addStretch()

        return widget

    def _create_chat_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        chat = QTextEdit()
        chat.setReadOnly(True)
        chat.setPlaceholderText("Mesajlar...")
        layout.addWidget(chat)
        
        row = QHBoxLayout()
        inp = QLineEdit()
        inp.setPlaceholderText("Mesaj yaz...")
        inp.setFixedHeight(45)
        row.addWidget(inp)
        
        btn = QPushButton("Gonder")
        btn.setObjectName("primaryBtn")
        btn.setFixedHeight(45)
        btn.setFixedWidth(100)
        btn.clicked.connect(lambda: self._add_log(f"Mesaj: {inp.text()}"))
        row.addWidget(btn)
        layout.addLayout(row)
        
        return widget

    def _create_screen_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        screen = QLabel("Ekran onizlemesi burada gorunecek")
        screen.setAlignment(Qt.AlignCenter)
        screen.setMinimumHeight(400)
        screen.setStyleSheet("background: #12122a; border: 2px solid #3a3a6a; border-radius: 12px;")
        layout.addWidget(screen)
        
        row = QHBoxLayout()
        for text, obj in [("Akisi Baslat", "successBtn"), ("Akisi Durdur", "dangerBtn"), ("Ekran Goruntusu", "primaryBtn")]:
            btn = QPushButton(text)
            btn.setObjectName(obj)
            btn.setFixedHeight(45)
            btn.clicked.connect(lambda _, t=text: self._add_log(f"{t} tiklandi"))
            row.addWidget(btn)
        layout.addLayout(row)
        
        return widget

    def _add_log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{ts}] {msg}")

    def _get_stylesheet(self):
        return """
            QMainWindow, QWidget { background: #0a0a1a; color: #e0e8ff; font-family: 'Segoe UI'; font-size: 13px; }
            QGroupBox { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a1a35, stop:1 #12122a); border: 1px solid #3a3a6a; border-radius: 12px; margin-top: 18px; padding-top: 15px; }
            QGroupBox::title { subcontrol-origin: margin; left: 18px; top: 6px; color: #00d4ff; font-size: 11px; font-weight: bold; }
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2a2a4a, stop:1 #1a1a35); border: 1px solid #4a4a7a; border-radius: 8px; padding: 12px 20px; font-weight: bold; color: #c0c8e8; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3a3a5a, stop:1 #2a2a45); border-color: #6a6a9a; color: #ffffff; }
            #primaryBtn { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d4ff, stop:1 #0099cc); border: none; color: #0a0a1a; }
            #successBtn { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00cc88, stop:1 #009966); border: none; color: #0a0a1a; }
            #warningBtn { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #bb86fc, stop:1 #9966dd); border: none; color: #0a0a1a; }
            #dangerBtn { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff5566, stop:1 #cc3344); border: none; color: #ffffff; }
            #secondaryBtn { background: #1a1a35; border: 1px solid #4a4a7a; }
            QLineEdit { background: #12122a; border: 2px solid #3a3a6a; border-radius: 8px; padding: 12px; color: #e0e8ff; }
            QLineEdit:focus { border-color: #00d4ff; }
            QTextEdit { background: #12122a; border: 2px solid #3a3a6a; border-radius: 10px; padding: 14px; color: #e0e8ff; }
            QTabWidget::pane { background: #1a1a35; border: 1px solid #3a3a6a; border-radius: 12px; }
            QTabBar::tab { background: #2a2a4a; border: 1px solid #3a3a6a; border-radius: 8px 8px 0 0; padding: 12px 28px; font-weight: bold; color: #8080aa; }
            QTabBar::tab:selected { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d4ff, stop:1 #0099cc); color: #0a0a1a; }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = TestAdminGUI()
    window.show()
    sys.exit(app.exec_())

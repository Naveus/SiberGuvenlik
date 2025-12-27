"""
Siber Guvenlik Egitim Projesi - Client GUI
Kullanici tarafindaki arayuz (Pro Edition)
"""

import sys
import os
import threading
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit, QGroupBox,
    QMessageBox, QTabWidget, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont

# Path ayari
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.client import Client
from shared.protocol import CommandType, get_local_ip


class SignalHandler(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    message_received = pyqtSignal(object)
    alert_received = pyqtSignal(str, str)
    command_executed = pyqtSignal(str, bool)
    log_received = pyqtSignal(str)


class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = Client()
        self.signals = SignalHandler()

        self.signals.connected.connect(self._on_connected)
        self.signals.disconnected.connect(self._on_disconnected)
        self.signals.message_received.connect(self._on_message_received)
        self.signals.alert_received.connect(self._show_alert_dialog)
        self.signals.command_executed.connect(self._on_command_executed)
        self.signals.log_received.connect(self._add_log)

        self.client.on_connected = lambda: self.signals.connected.emit()
        self.client.on_disconnected = lambda: self.signals.disconnected.emit()
        self.client.on_message_received = lambda msg: self.signals.message_received.emit(msg)
        self.client.on_alert_received = lambda t, m: self.signals.alert_received.emit(t, m)
        self.client.on_command_executed = lambda c, s: self.signals.command_executed.emit(c, s)
        self.client.on_log = lambda m: self.signals.log_received.emit(m)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Siber Guvenlik - Client")
        self.setMinimumSize(750, 650)
        self.setStyleSheet(self._get_stylesheet())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        title = QLabel("CLIENT UYGULAMASI")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)

        subtitle = QLabel("Siber Guvenlik Egitim Projesi")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)

        main_layout.addWidget(header)

        # Stacked widget
        self.stacked = QStackedWidget()
        self.stacked.addWidget(self._create_connect_page())
        self.stacked.addWidget(self._create_main_page())
        main_layout.addWidget(self.stacked)

    def _create_connect_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        # Connection Box
        conn_frame = QFrame()
        conn_frame.setObjectName("connectionBox")
        conn_frame.setFixedWidth(400)
        conn_layout = QVBoxLayout(conn_frame)
        conn_layout.setContentsMargins(30, 30, 30, 30)
        conn_layout.setSpacing(15)

        conn_title = QLabel("SUNUCUYA BAGLAN")
        conn_title.setObjectName("sectionTitle")
        conn_title.setAlignment(Qt.AlignCenter)
        conn_layout.addWidget(conn_title)

        # IP Input
        ip_label = QLabel("Sunucu IP Adresi")
        ip_label.setObjectName("inputLabel")
        conn_layout.addWidget(ip_label)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ornek: 192.168.1.100")
        self.ip_input.setFixedHeight(45)
        conn_layout.addWidget(self.ip_input)

        # Code Input
        code_label = QLabel("Baglanti Kodu")
        code_label.setObjectName("inputLabel")
        conn_layout.addWidget(code_label)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("4 haneli kod")
        self.code_input.setMaxLength(4)
        self.code_input.setAlignment(Qt.AlignCenter)
        self.code_input.setFixedHeight(50)
        self.code_input.setStyleSheet("font-size: 20px; letter-spacing: 8px; font-weight: bold;")
        self.code_input.returnPressed.connect(self._connect)
        conn_layout.addWidget(self.code_input)

        # Error Label
        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        conn_layout.addWidget(self.error_label)

        # Connect Button
        self.connect_btn = QPushButton("Baglan")
        self.connect_btn.setObjectName("primaryBtn")
        self.connect_btn.setFixedHeight(50)
        self.connect_btn.clicked.connect(self._connect)
        conn_layout.addWidget(self.connect_btn)

        layout.addWidget(conn_frame)
        return widget

    def _create_main_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)

        # Status Panel
        status_panel = QFrame()
        status_panel.setObjectName("statusPanel")
        status_layout = QHBoxLayout(status_panel)
        status_layout.setContentsMargins(20, 15, 20, 15)

        left = QVBoxLayout()
        left.setSpacing(3)

        status_title = QLabel("BAGLANTI DURUMU")
        status_title.setObjectName("sectionTitle")
        left.addWidget(status_title)

        self.status_label = QLabel("Bagli")
        self.status_label.setObjectName("statusConnected")
        left.addWidget(self.status_label)

        self.server_label = QLabel("")
        self.server_label.setObjectName("serverLabel")
        left.addWidget(self.server_label)

        status_layout.addLayout(left)
        status_layout.addStretch()

        disconnect_btn = QPushButton("Baglantivi Kes")
        disconnect_btn.setObjectName("dangerBtn")
        disconnect_btn.setFixedWidth(140)
        disconnect_btn.setFixedHeight(40)
        disconnect_btn.clicked.connect(self._disconnect)
        status_layout.addWidget(disconnect_btn)

        layout.addWidget(status_panel)

        # Tabs
        tabs = QTabWidget()
        tabs.setObjectName("mainTabs")
        tabs.addTab(self._create_chat_tab(), "  Mesajlasma  ")
        tabs.addTab(self._create_history_tab(), "  Komut Gecmisi  ")
        layout.addWidget(tabs)

        # Danger Zone
        danger_frame = QFrame()
        danger_frame.setObjectName("dangerZone")
        danger_layout = QHBoxLayout(danger_frame)
        danger_layout.setContentsMargins(15, 12, 15, 12)

        danger_label = QLabel("TEHLIKELI BOLGE")
        danger_label.setObjectName("dangerTitle")
        danger_layout.addWidget(danger_label)

        danger_layout.addStretch()

        uninstall_btn = QPushButton("Uygulamayi Kaldir")
        uninstall_btn.setObjectName("dangerBtn")
        uninstall_btn.setFixedHeight(35)
        uninstall_btn.clicked.connect(self._uninstall)
        danger_layout.addWidget(uninstall_btn)

        layout.addWidget(danger_frame)

        return widget

    def _create_chat_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("Mesajlar burada gorunecek...")
        layout.addWidget(self.chat_display)

        send_layout = QHBoxLayout()
        send_layout.setSpacing(10)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Mesajinizi yazin...")
        self.chat_input.setFixedHeight(42)
        self.chat_input.returnPressed.connect(self._send_message)
        send_layout.addWidget(self.chat_input)

        send_btn = QPushButton("Gonder")
        send_btn.setObjectName("primaryBtn")
        send_btn.setFixedWidth(100)
        send_btn.setFixedHeight(42)
        send_btn.clicked.connect(self._send_message)
        send_layout.addWidget(send_btn)

        layout.addLayout(send_layout)
        return widget

    def _create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        info_label = QLabel("Admin'den gelen komutlar ve sistem loglari:")
        info_label.setObjectName("infoLabel")
        layout.addWidget(info_label)

        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setPlaceholderText("Komut gecmisi burada gorunecek...")
        layout.addWidget(self.history_display)

        return widget

    def _get_stylesheet(self):
        return """
            /* ========== SIBER GUVENLIK - MAVI MOR TEMA - CLIENT ========== */
            
            QMainWindow { background: #0a0a1a; }
            QWidget { 
                color: #e0e8ff; 
                font-family: 'Segoe UI', Arial, sans-serif; 
                font-size: 12px; 
            }

            #titleLabel {
                font-size: 30px; 
                font-weight: bold; 
                color: #00d4ff;
                letter-spacing: 3px;
            }
            #subtitleLabel {
                font-size: 12px; 
                color: #8080aa;
                letter-spacing: 2px;
            }
            #sectionTitle {
                font-size: 11px; 
                font-weight: bold; 
                color: #00d4ff;
                letter-spacing: 2px;
            }
            #inputLabel {
                font-size: 12px; 
                color: #a0a0cc;
            }
            #errorLabel {
                font-size: 12px; 
                color: #ff5566;
            }
            #statusConnected { 
                font-size: 16px; 
                font-weight: bold; 
                color: #00d4ff; 
            }
            #serverLabel { 
                font-size: 12px; 
                color: #8080aa; 
            }
            #infoLabel { 
                font-size: 12px; 
                color: #8080aa; 
            }
            #dangerTitle { 
                font-size: 11px; 
                font-weight: bold; 
                color: #ff5566; 
                letter-spacing: 2px; 
            }

            #connectionBox, #statusPanel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a35, stop:1 #12122a);
                border: 2px solid #00d4ff;
                border-radius: 16px;
            }

            #dangerZone {
                background: rgba(255, 85, 102, 0.1);
                border: 1px solid #ff5566;
                border-radius: 10px;
            }

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
            QPushButton:pressed { background: #15152a; }
            QPushButton:disabled { background: #1a1a2a; color: #4a4a6a; border-color: #2a2a4a; }

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

            QLineEdit {
                background: #12122a;
                border: 2px solid #3a3a6a;
                border-radius: 8px;
                padding: 12px 15px; 
                font-size: 14px;
                color: #e0e8ff;
            }
            QLineEdit:focus { 
                border-color: #00d4ff;
                background: #1a1a35;
            }

            QTextEdit {
                background: #12122a;
                border: 2px solid #3a3a6a;
                border-radius: 10px;
                padding: 12px; 
                font-size: 13px;
                color: #e0e8ff;
            }

            QTabWidget::pane {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a35, stop:1 #12122a);
                border: 1px solid #3a3a6a;
                border-radius: 10px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a4a, stop:1 #1a1a35);
                border: 1px solid #3a3a6a;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
                padding: 10px 25px;
                margin-right: 3px;
                font-weight: bold;
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

            QScrollBar:vertical {
                background: #12122a;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a7a;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover { 
                background: #00d4ff; 
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { 
                height: 0px; 
            }
        """

    # Connection
    def _connect(self):
        ip = self.ip_input.text().strip()
        code = self.code_input.text().strip()

        if not ip:
            self.error_label.setText("Lutfen IP adresi girin!")
            return
        if not code or len(code) != 4:
            self.error_label.setText("Lutfen 4 haneli kodu girin!")
            return

        self.error_label.setText("")
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Baglaniyor...")

        def connect_thread():
            success = self.client.connect(ip, code)
            if not success:
                self.signals.log_received.emit("Baglanti basarisiz!")

        thread = threading.Thread(target=connect_thread, daemon=True)
        thread.start()

    def _disconnect(self):
        self.client.disconnect()

    def _on_connected(self):
        self.server_label.setText(f"Sunucu: {self.client.server_ip}")
        self.stacked.setCurrentIndex(1)
        self._add_history("SISTEM", "Sunucuya baglanildi")

    def _on_disconnected(self):
        self.stacked.setCurrentIndex(0)
        self.connect_btn.setEnabled(True)
        self.connect_btn.setText("Baglan")
        self.error_label.setText("Baglanti kesildi!")

    def _on_message_received(self, msg):
        if msg.command == CommandType.MESSAGE.value:
            text = msg.data.get('text', '')
            self._add_chat("ADMIN", text)
            self._add_history("MESAJ", text)

    def _show_alert_dialog(self, title, message):
        QMessageBox.warning(self, title, message)
        self._add_history("UYARI", f"{title}: {message}")

    def _on_command_executed(self, command, success):
        status = "Basarili" if success else "Basarisiz"
        self._add_history("KOMUT", f"{command} - {status}")

    def _add_log(self, message):
        if "Baglanti basarisiz" in message:
            self.error_label.setText("Baglanti basarisiz! IP veya kodu kontrol edin.")
            self.connect_btn.setEnabled(True)
            self.connect_btn.setText("Baglan")

    def _send_message(self):
        text = self.chat_input.text().strip()
        if text:
            self.client.send_chat(text)
            self._add_chat("BEN", text)
            self.chat_input.clear()

    def _add_chat(self, sender, message):
        ts = datetime.now().strftime("%H:%M:%S")
        color = "#ff6b6b" if sender == "ADMIN" else "#2ed573" if sender == "BEN" else "#ffa502"
        self.chat_display.append(f'<span style="color:#555">[{ts}]</span> '
                                  f'<span style="color:{color};font-weight:bold">{sender}:</span> {message}')

    def _add_history(self, type, message):
        ts = datetime.now().strftime("%H:%M:%S")
        colors = {"SISTEM": "#00d4ff", "KOMUT": "#ffa502", "MESAJ": "#2ed573", "UYARI": "#ff4757"}
        color = colors.get(type, "#ffffff")
        self.history_display.append(f'<span style="color:#555">[{ts}]</span> '
                                     f'<span style="color:{color};font-weight:bold">[{type}]</span> {message}')

    def _uninstall(self):
        if QMessageBox.question(self, 'Onayla', 'Uygulama tamamen kaldirilacak.\nEmin misiniz?',
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.client._uninstall()

    def closeEvent(self, event):
        self.client.disconnect()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ClientGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

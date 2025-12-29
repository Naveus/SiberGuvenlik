"""
Siber Guvenlik Egitim Projesi - Admin Server
Client baglantilarini yoneten sunucu modulu
"""

import socket
import threading
import time
from typing import Callable, Optional, Dict
import sys
import os

# Shared modulu icin path ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.protocol import (
    Protocol, Message, CommandType,
    generate_connection_code, get_local_ip, DEFAULT_PORT
)


class AdminServer:
    """Admin sunucu sinifi"""

    def __init__(self, port: int = DEFAULT_PORT):
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.client_socket: Optional[socket.socket] = None
        self.client_address: Optional[tuple] = None
        self.connection_code: str = ""
        self.is_running: bool = False
        self.is_connected: bool = False

        # Callback fonksiyonlari
        self.on_client_connected: Optional[Callable] = None
        self.on_client_disconnected: Optional[Callable] = None
        self.on_message_received: Optional[Callable] = None
        self.on_log: Optional[Callable] = None

        # Thread
        self.listen_thread: Optional[threading.Thread] = None
        self.receive_thread: Optional[threading.Thread] = None

    def log(self, message: str):
        """Log mesaji gonder"""
        if self.on_log:
            self.on_log(message)
        else:
            print(f"[SERVER] {message}")

    def start(self) -> str:
        """Sunucuyu baslat ve baglanti kodu dondur"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(1)

            self.connection_code = generate_connection_code()
            self.is_running = True

            # Baglanti dinleme thread'i
            self.listen_thread = threading.Thread(target=self._listen_for_connections, daemon=True)
            self.listen_thread.start()

            local_ip = get_local_ip()
            self.log(f"Sunucu baslatildi: {local_ip}:{self.port}")
            self.log(f"Baglanti kodu: {self.connection_code}")

            return self.connection_code

        except Exception as e:
            self.log(f"Sunucu baslatma hatasi: {e}")
            return ""

    def stop(self):
        """Sunucuyu durdur"""
        self.is_running = False
        self.is_connected = False

        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None

        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None

        self.log("Sunucu durduruldu")

    def _listen_for_connections(self):
        """Baglantilari dinle"""
        while self.is_running:
            try:
                self.server_socket.settimeout(1.0)
                try:
                    client_sock, client_addr = self.server_socket.accept()
                except socket.timeout:
                    continue

                self.log(f"Baglanti istegi: {client_addr}")

                # Ilk mesaji al (baglanti kodu kontrolu)
                msg = Protocol.receive_message(client_sock)
                if msg and msg.command == CommandType.CONNECT.value:
                    received_code = msg.data.get('code', '')
                    if received_code == self.connection_code:
                        self.client_socket = client_sock
                        self.client_address = client_addr
                        self.is_connected = True

                        # Onay mesaji gonder
                        response = Message(
                            command=CommandType.CONNECT.value,
                            data={'status': 'accepted'},
                            timestamp=time.time()
                        )
                        Protocol.send_message(client_sock, response)
                        
                        # Socket'i non-blocking yapma, timeout ile calis
                        client_sock.settimeout(None)
                        client_sock.setblocking(True)

                        self.log(f"Client baglandi: {client_addr}")

                        if self.on_client_connected:
                            self.on_client_connected(client_addr)

                        # Mesaj alma thread'i
                        self.receive_thread = threading.Thread(
                            target=self._receive_messages, daemon=True
                        )
                        self.receive_thread.start()
                    else:
                        # Yanlis kod
                        response = Message(
                            command=CommandType.CONNECT.value,
                            data={'status': 'rejected', 'reason': 'Invalid code'},
                            timestamp=time.time()
                        )
                        Protocol.send_message(client_sock, response)
                        client_sock.close()
                        self.log(f"Baglanti reddedildi (yanlis kod): {client_addr}")

            except Exception as e:
                if self.is_running:
                    self.log(f"Dinleme hatasi: {e}")

    def _receive_messages(self):
        """Client'tan mesajlari al"""
        while self.is_running and self.is_connected:
            try:
                if not self.client_socket:
                    break

                # Select kullanarak bekle
                import select
                ready = select.select([self.client_socket], [], [], 1.0)
                if not ready[0]:
                    continue

                msg = Protocol.receive_message(self.client_socket)

                if msg:
                    if msg.command == CommandType.DISCONNECT.value:
                        self._handle_disconnect()
                        break
                    elif self.on_message_received:
                        self.on_message_received(msg)
                else:
                    # Baglanti koptu
                    self._handle_disconnect()
                    break

            except Exception as e:
                if self.is_running and self.is_connected:
                    self.log(f"Mesaj alma hatasi: {e}")
                    self._handle_disconnect()
                break

    def _handle_disconnect(self):
        """Baglanti kopma durumu"""
        self.is_connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None

        self.log("Client baglantisi kesildi")

        if self.on_client_disconnected:
            self.on_client_disconnected()

    def send_command(self, command: CommandType, data: Dict = None) -> bool:
        """Client'a komut gonder"""
        if not self.is_connected or not self.client_socket:
            self.log("Client bagli degil!")
            return False

        try:
            msg = Message(
                command=command.value,
                data=data or {},
                timestamp=time.time()
            )
            success = Protocol.send_message(self.client_socket, msg)
            if success:
                self.log(f"Komut gonderildi: {command.value}")
            return success
        except Exception as e:
            self.log(f"Komut gonderme hatasi: {e}")
            return False

    # Hazir komut metodlari
    def shutdown_client(self):
        """Client PC'yi kapat"""
        return self.send_command(CommandType.SHUTDOWN)

    def restart_client(self):
        """Client PC'yi yeniden baslat"""
        return self.send_command(CommandType.RESTART)

    def send_message(self, message: str):
        """Client'a mesaj gonder"""
        return self.send_command(CommandType.MESSAGE, {'text': message})

    def send_alert(self, title: str, message: str):
        """Client'a uyari mesaji gonder"""
        return self.send_command(CommandType.ALERT, {'title': title, 'text': message})

    def request_screenshot(self):
        """Ekran goruntusu iste"""
        return self.send_command(CommandType.SCREENSHOT)

    def disable_task_manager(self):
        """Gorev yoneticisini kapat"""
        return self.send_command(CommandType.DISABLE_TASKMGR)

    def enable_task_manager(self):
        """Gorev yoneticisini ac"""
        return self.send_command(CommandType.ENABLE_TASKMGR)

    def disable_cmd(self):
        """CMD'yi kapat"""
        return self.send_command(CommandType.DISABLE_CMD)

    def enable_cmd(self):
        """CMD'yi ac"""
        return self.send_command(CommandType.ENABLE_CMD)

    def execute_command(self, command: str):
        """Komut calistir"""
        return self.send_command(CommandType.EXECUTE, {'command': command})

    def uninstall_client(self):
        """Client'i sil"""
        return self.send_command(CommandType.UNINSTALL)

    # Yeni metodlar - Fare/Klavye
    def disable_mouse(self):
        """Fareyi devre disi birak"""
        return self.send_command(CommandType.DISABLE_MOUSE)

    def enable_mouse(self):
        """Fareyi etkinlestir"""
        return self.send_command(CommandType.ENABLE_MOUSE)

    def disable_keyboard(self):
        """Klavyeyi devre disi birak"""
        return self.send_command(CommandType.DISABLE_KEYBOARD)

    def enable_keyboard(self):
        """Klavyeyi etkinlestir"""
        return self.send_command(CommandType.ENABLE_KEYBOARD)

    # Ekran akisi
    def start_stream(self):
        """Ekran akisini baslat"""
        return self.send_command(CommandType.START_STREAM, {'fps': 60, 'quality': 720})

    def stop_stream(self):
        """Ekran akisini durdur"""
        return self.send_command(CommandType.STOP_STREAM)

    # Uzaktan kontrol
    def send_mouse_click(self, x: int, y: int, label_w: int, label_h: int, button: str = 'left'):
        """Uzaktan fare tiklama"""
        return self.send_command(CommandType.MOUSE_CLICK, {
            'x': x, 'y': y,
            'label_w': label_w, 'label_h': label_h,
            'button': button
        })

    def send_mouse_move(self, x: int, y: int, label_w: int, label_h: int):
        """Uzaktan fare hareketi"""
        return self.send_command(CommandType.MOUSE_MOVE, {
            'x': x, 'y': y,
            'label_w': label_w, 'label_h': label_h
        })

    def send_key_press(self, key: str):
        """Uzaktan klavye tusu"""
        return self.send_command(CommandType.KEY_PRESS, {'key': key})

    # Gelişmiş kontroller
    def kill_active_app(self):
        """Aktif uygulamayı kapat"""
        return self.send_command(CommandType.KILL_ACTIVE_APP)

    def hide_screen(self):
        """Ekranı gizle (siyah overlay)"""
        return self.send_command(CommandType.HIDE_SCREEN)

    def show_screen(self):
        """Ekranı göster"""
        return self.send_command(CommandType.SHOW_SCREEN)

    def disable_touchpad(self):
        """Touchpad'i devre disi birak"""
        return self.send_command(CommandType.DISABLE_TOUCHPAD)

    def enable_touchpad(self):
        """Touchpad'i etkinlestir"""
        return self.send_command(CommandType.ENABLE_TOUCHPAD)


if __name__ == "__main__":
    # Test
    server = AdminServer()
    code = server.start()
    print(f"Baglanti kodu: {code}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop()


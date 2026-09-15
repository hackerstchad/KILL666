#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ██╗  ██╗██╗██╗     ██╗      ██████╗ ██████╗ ██████╗                         ║
║  ██║ ██╔╝██║██║     ██║     ██╔═══██╗██╔══██╗╚════██╗                        ║
║  █████╔╝ ██║██║     ██║     ██║   ██║██████╔╝  ▄███╔╝                        ║
║  ██╔═██╗ ██║██║     ██║     ██║   ██║██╔══██╗  ▀▀══╝                         ║
║  ██║  ██╗██║███████╗███████╗╚██████╔╝██║  ██║  ██╗                           ║
║  ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝  ╚═╝                           ║
║                                                                              ║
║        KILL666 — PRIVATE SECURE NETWORK COMMUNICATION INTERFACE              ║
║          Video · Voice · File Transfer · Live Chat · Profiles                ║
║                    Créé par : hackers_tchad                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import base64
import socket
import struct
import threading
import hashlib
import secrets
import io
import wave
import queue
import datetime
import random
import string
import subprocess
import webbrowser
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog, colorchooser
from tkinter.font import Font
import tkinter.font as tkfont

# === Auto-install missing dependencies ===
REQUIRED_LIBS = [
    ('PIL', 'Pillow'),
    ('cv2', 'opencv-python'),
    ('numpy', 'numpy'),
    ('pyaudio', 'pyaudio'),
    ('cryptography', 'cryptography'),
    ('requests', 'requests'),
    ('psutil', 'psutil'),
]
for mod, pkg in REQUIRED_LIBS:
    try:
        __import__(mod)
    except ImportError:
        print(f"[KILL666] Installing {pkg}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
import cv2
import numpy as np
import pyaudio
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ============================================================
# GLOBAL CONFIG
# ============================================================
APP_NAME = "KILL666"
APP_VERSION = "v666.0"
AUTHOR = "hackers_tchad"
DEFAULT_PORT = 6666
BROADCAST_PORT = 6667
VIDEO_PORT_OFFSET = 1
VOICE_PORT_OFFSET = 2
FILE_PORT_OFFSET = 3

THEMES = {
    "hacker_green": {
        "bg": "#050505", "fg": "#00ff41", "accent": "#00ff41",
        "secondary": "#003b00", "chat_bg": "#001100", "chat_fg": "#00ff41",
        "danger": "#ff0000", "info": "#00ffff", "warn": "#ffff00",
        "border": "#00ff41", "panel": "#0a0a0a", "input_bg": "#001a00",
        "cam_filter": "matrix_green"
    },
    "blood_red": {
        "bg": "#0a0000", "fg": "#ff1a1a", "accent": "#ff0000",
        "secondary": "#3b0000", "chat_bg": "#1a0000", "chat_fg": "#ff6666",
        "danger": "#ff0000", "info": "#ff9999", "warn": "#ffcc00",
        "border": "#ff0000", "panel": "#140000", "input_bg": "#2a0000",
        "cam_filter": "blood_red"
    },
    "cyber_blue": {
        "bg": "#000510", "fg": "#00d4ff", "accent": "#0099ff",
        "secondary": "#001a3d", "chat_bg": "#000d1f", "chat_fg": "#80e5ff",
        "danger": "#ff3366", "info": "#00ffff", "warn": "#ffcc00",
        "border": "#00d4ff", "panel": "#000a1a", "input_bg": "#00152e",
        "cam_filter": "cyber_blue"
    },
    "midnight_purple": {
        "bg": "#0a0010", "fg": "#d500ff", "accent": "#aa00ff",
        "secondary": "#240033", "chat_bg": "#12001a", "chat_fg": "#e580ff",
        "danger": "#ff0055", "info": "#ff80ff", "warn": "#ffcc00",
        "border": "#d500ff", "panel": "#0f0014", "input_bg": "#1f0029",
        "cam_filter": "purple_haze"
    },
    "ghost_white": {
        "bg": "#0a0a0a", "fg": "#e0e0e0", "accent": "#ffffff",
        "secondary": "#1a1a1a", "chat_bg": "#111111", "chat_fg": "#cccccc",
        "danger": "#ff3333", "info": "#66ccff", "warn": "#ffcc00",
        "border": "#666666", "panel": "#0f0f0f", "input_bg": "#1a1a1a",
        "cam_filter": "noir_white"
    }
}

DATA_DIR = Path.home() / f".{APP_NAME.lower()}"
DATA_DIR.mkdir(exist_ok=True)
PROFILE_FILE = DATA_DIR / "profile.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
LOGS_DIR = DATA_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
FILES_DIR = DATA_DIR / "received_files"
FILES_DIR.mkdir(exist_ok=True)

# ============================================================
# UTILS
# ============================================================
def generate_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def encrypt_payload(data: bytes, password: str = "KILL666_DEFAULT_KEY") -> bytes:
    try:
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b"KILL666_SALT", iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key).encrypt(data)
    except Exception:
        return data

def decrypt_payload(token: bytes, password: str = "KILL666_DEFAULT_KEY") -> bytes:
    try:
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b"KILL666_SALT", iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key).decrypt(token)
    except Exception:
        return token

def log_event(text):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOGS_DIR / "activity.log", "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {text}\n")
    except Exception:
        pass

# ============================================================
# PROFILE MANAGER
# ============================================================
class ProfileManager:
    def __init__(self):
        self.profile = self.load()

    def load(self):
        if PROFILE_FILE.exists():
            try:
                return json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "username": f"Agent_{generate_id()}",
            "status": "ONLINE",
            "avatar": None,
            "color": "#00ff41",
            "theme": "hacker_green",
            "bio": "Opérateur KILL666",
            "role": "Operative",
            "joined": datetime.datetime.now().isoformat()
        }

    def save(self):
        PROFILE_FILE.write_text(json.dumps(self.profile, indent=2), encoding="utf-8")

# ============================================================
# NETWORK CORE
# ============================================================
class NetworkCore:
    def __init__(self, app):
        self.app = app
        self.ip = self.get_local_ip()
        self.port = DEFAULT_PORT
        self.running = False
        self.server_socket = None
        self.peers = {}  # ip -> {"username", "status", "video", "voice", "socket"}
        self.lock = threading.Lock()

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def start_server(self):
        self.running = True
        threading.Thread(target=self._tcp_listener, daemon=True).start()
        threading.Thread(target=self._broadcast_listener, daemon=True).start()
        threading.Thread(target=self._heartbeat, daemon=True).start()
        log_event(f"Server started on {self.ip}:{self.port}")

    def _tcp_listener(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", self.port))
            self.server_socket.listen(50)
            while self.running:
                try:
                    client, addr = self.server_socket.accept()
                    threading.Thread(target=self._handle_client, args=(client, addr), daemon=True).start()
                except Exception:
                    break
        except Exception as e:
            self.app.log(f"[NET ERR] {e}")

    def _handle_client(self, client, addr):
        try:
            data = b""
            while not data.endswith(b"\n"):
                chunk = client.recv(4096)
                if not chunk:
                    break
                data += chunk
            if data:
                msg = json.loads(data.decode("utf-8"))
                self._route_message(msg, addr[0], client)
        except Exception as e:
            pass
        finally:
            try:
                client.close()
            except Exception:
                pass

    def _route_message(self, msg, ip, sock):
        mtype = msg.get("type")
        if mtype == "handshake":
            with self.lock:
                self.peers[ip] = {
                    "username": msg.get("username", "Unknown"),
                    "status": msg.get("status", "ONLINE"),
                    "color": msg.get("color", "#00ff41"),
                    "role": msg.get("role", "Operative"),
                    "bio": msg.get("bio", ""),
                    "avatar": msg.get("avatar"),
                    "last_seen": time.time()
                }
            self.app.log(f"[+] {msg.get('username')} connected from {ip}")
            self.app.update_users_list()
            self.send_handshake(ip)
        elif mtype == "chat":
            self.app.append_chat(msg.get("username", "Unknown"), msg.get("text", ""), msg.get("color", "#00ff41"), msg.get("avatar"))
        elif mtype == "private":
            self.app.append_chat(f"[PVT] {msg.get('username', 'Unknown')}", msg.get("text", ""), msg.get("color", "#ffcc00"), msg.get("avatar"), private=True)
        elif mtype == "file_offer":
            self.app.handle_file_offer(ip, msg)
        elif mtype == "signal":
            self.app.handle_signal(ip, msg)

    def send_handshake(self, ip):
        payload = {
            "type": "handshake",
            "username": self.app.profile["username"],
            "status": self.app.profile["status"],
            "color": self.app.profile["color"],
            "role": self.app.profile["role"],
            "bio": self.app.profile["bio"],
            "avatar": self.app.profile["avatar"],
            "app": APP_NAME,
            "version": APP_VERSION
        }
        self.send_json(ip, payload)

    def send_json(self, ip, obj):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, self.port))
            data = json.dumps(obj).encode("utf-8") + b"\n"
            sock.sendall(data)
            sock.close()
        except Exception as e:
            pass

    def broadcast_chat(self, text, private_to=None):
        msg = {
            "type": "private" if private_to else "chat",
            "username": self.app.profile["username"],
            "text": text,
            "color": self.app.profile["color"],
            "avatar": self.app.profile["avatar"],
            "timestamp": time.time()
        }
        if private_to:
            self.send_json(private_to, msg)
        else:
            with self.lock:
                for ip in list(self.peers.keys()):
                    threading.Thread(target=self.send_json, args=(ip, msg), daemon=True).start()

    def _broadcast_listener(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", BROADCAST_PORT))
            sock.settimeout(1)
            while self.running:
                try:
                    data, addr = sock.recvfrom(1024)
                    msg = json.loads(data.decode("utf-8"))
                    if msg.get("type") == "discovery" and addr[0] != self.ip:
                        self.send_handshake(addr[0])
                except socket.timeout:
                    continue
                except Exception:
                    pass
        except Exception:
            pass

    def send_discovery(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            msg = json.dumps({"type": "discovery", "username": self.app.profile["username"], "ip": self.ip}).encode()
            sock.sendto(msg, ("<broadcast>", BROADCAST_PORT))
            sock.close()
        except Exception:
            pass

    def _heartbeat(self):
        while self.running:
            self.send_discovery()
            time.sleep(10)

    def connect_to(self, ip):
        if ip == self.ip:
            return
        self.send_handshake(ip)

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass

# ============================================================
# VIDEO CORE
# ============================================================
class VideoCore:
    def __init__(self, app):
        self.app = app
        self.cap = None
        self.running = False
        self.filter_mode = "matrix_green"
        self.show_self = True
        self.recording = False
        self.writer = None
        self.fps = 20
        self.resolution = (640, 480)
        self.lock = threading.Lock()

    def start(self):
        if self.cap:
            return
        try:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            self.running = True
            threading.Thread(target=self._capture_loop, daemon=True).start()
            threading.Thread(target=self._video_server, daemon=True).start()
        except Exception as e:
            self.app.log(f"[CAM ERR] {e}")

    def _capture_loop(self):
        while self.running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            frame = self.apply_filter(frame)
            if self.recording and self.writer:
                self.writer.write(frame)
            self.app.update_self_video(frame)
            time.sleep(0.03)

    def apply_filter(self, frame):
        mode = self.filter_mode
        if mode == "matrix_green":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            green = np.zeros_like(frame)
            green[:, :, 1] = gray
            return green
        elif mode == "blood_red":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            red = np.zeros_like(frame)
            red[:, :, 2] = gray
            return red
        elif mode == "cyber_blue":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blue = np.zeros_like(frame)
            blue[:, :, 0] = gray
            return blue
        elif mode == "purple_haze":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            purp = np.zeros_like(frame)
            purp[:, :, 0] = gray // 2
            purp[:, :, 2] = gray
            return purp
        elif mode == "noir_white":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif mode == "scanlines":
            for y in range(0, frame.shape[0], 4):
                frame[y:y+2, :] = frame[y:y+2, :] // 2
            return frame
        elif mode == "edge":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 80, 150)
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        elif mode == "thermal":
            return cv2.applyColorMap(frame, cv2.COLORMAP_JET)
        return frame

    def _video_server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", DEFAULT_PORT + VIDEO_PORT_OFFSET))
            server.listen(10)
            while self.running:
                try:
                    client, addr = server.accept()
                    threading.Thread(target=self._stream_to_peer, args=(client,), daemon=True).start()
                except Exception:
                    break
        except Exception:
            pass

    def _stream_to_peer(self, client):
        try:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
            while self.running and self.cap:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                frame = cv2.flip(frame, 1)
                frame = self.apply_filter(frame)
                _, buf = cv2.imencode('.jpg', frame, encode_param)
                data = encrypt_payload(buf.tobytes())
                size = struct.pack('!I', len(data))
                try:
                    client.sendall(size + data)
                except Exception:
                    break
                time.sleep(0.05)
        except Exception:
            pass
        finally:
            try:
                client.close()
            except Exception:
                pass

    def connect_to_peer_video(self, ip):
        threading.Thread(target=self._receive_peer_video, args=(ip,), daemon=True).start()

    def _receive_peer_video(self, ip):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, DEFAULT_PORT + VIDEO_PORT_OFFSET))
            data_buffer = b""
            while self.running:
                while len(data_buffer) < 4:
                    chunk = sock.recv(4096)
                    if not chunk:
                        return
                    data_buffer += chunk
                size = struct.unpack('!I', data_buffer[:4])[0]
                data_buffer = data_buffer[4:]
                while len(data_buffer) < size:
                    chunk = sock.recv(4096)
                    if not chunk:
                        return
                    data_buffer += chunk
                frame_data = data_buffer[:size]
                data_buffer = data_buffer[size:]
                decrypted = decrypt_payload(frame_data)
                nparr = np.frombuffer(decrypted, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is not None:
                    self.app.update_peer_video(ip, frame)
        except Exception:
            pass

    def stop(self):
        self.running = False
        if self.writer:
            self.writer.release()
        if self.cap:
            self.cap.release()

# ============================================================
# VOICE CORE
# ============================================================
class VoiceCore:
    def __init__(self, app):
        self.app = app
        self.audio = pyaudio.PyAudio()
        self.running = False
        self.muted = False
        self.deafened = False
        self.input_device = None
        self.output_device = None
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        threading.Thread(target=self._voice_server, daemon=True).start()
        threading.Thread(target=self._capture_voice, daemon=True).start()

    def _capture_voice(self):
        try:
            stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=22050,
                                     input=True, frames_per_buffer=1024)
            while self.running:
                if self.muted:
                    time.sleep(0.1)
                    continue
                data = stream.read(1024, exception_on_overflow=False)
                with self.lock:
                    for ip in list(self.app.network.peers.keys()):
                        threading.Thread(target=self._send_voice, args=(ip, data), daemon=True).start()
        except Exception as e:
            self.app.log(f"[MIC ERR] {e}")

    def _send_voice(self, ip, data):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            enc = encrypt_payload(data)
            sock.sendto(enc, (ip, DEFAULT_PORT + VOICE_PORT_OFFSET))
            sock.close()
        except Exception:
            pass

    def _voice_server(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("0.0.0.0", DEFAULT_PORT + VOICE_PORT_OFFSET))
            sock.settimeout(1)
            while self.running:
                try:
                    data, addr = sock.recvfrom(4096)
                    if self.deafened:
                        continue
                    dec = decrypt_payload(data)
                    self.app.play_audio(dec)
                except socket.timeout:
                    continue
                except Exception:
                    pass
        except Exception as e:
            self.app.log(f"[VOICE SVR ERR] {e}")

    def play_audio(self, data):
        try:
            stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=22050,
                                     output=True, frames_per_buffer=1024)
            stream.write(data)
            stream.stop_stream()
            stream.close()
        except Exception:
            pass

    def stop(self):
        self.running = False
        self.audio.terminate()

# ============================================================
# FILE TRANSFER CORE
# ============================================================
class FileTransferCore:
    def __init__(self, app):
        self.app = app
        self.transfers = {}
        self.lock = threading.Lock()
        threading.Thread(target=self._server, daemon=True).start()

    def _server(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", DEFAULT_PORT + FILE_PORT_OFFSET))
            server.listen(10)
            while True:
                try:
                    client, addr = server.accept()
                    threading.Thread(target=self._receive_file, args=(client, addr), daemon=True).start()
                except Exception:
                    break
        except Exception as e:
            self.app.log(f"[FILE SVR ERR] {e}")

    def offer_file(self, ip, filepath):
        if not os.path.exists(filepath):
            return
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        tid = generate_id()
        self.transfers[tid] = {"path": filepath, "size": size, "sent": 0, "to": ip}
        self.app.network.send_json(ip, {
            "type": "file_offer",
            "filename": filename,
            "size": size,
            "tid": tid,
            "from": self.app.profile["username"]
        })

    def send_file(self, ip, filepath, tid):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((ip, DEFAULT_PORT + FILE_PORT_OFFSET))
            filename = os.path.basename(filepath).encode("utf-8")
            sock.sendall(struct.pack('!I', len(filename)) + filename)
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    sock.sendall(chunk)
                    self.transfers[tid]["sent"] += len(chunk)
            sock.close()
            self.app.log(f"[FILE] Sent {os.path.basename(filepath)}")
        except Exception as e:
            self.app.log(f"[FILE ERR] {e}")

    def _receive_file(self, client, addr):
        try:
            data = b""
            while len(data) < 4:
                data += client.recv(4 - len(data))
            namelen = struct.unpack('!I', data[:4])[0]
            data = data[4:]
            while len(data) < namelen:
                data += client.recv(namelen - len(data))
            filename = data[:namelen].decode("utf-8")
            data = data[namelen:]
            safe_name = f"{generate_id()}_{filename}"
            out_path = FILES_DIR / safe_name
            with open(out_path, 'wb') as f:
                while True:
                    chunk = client.recv(8192)
                    if not chunk:
                        break
                    f.write(chunk)
            self.app.log(f"[FILE] Received {safe_name}")
            self.app.append_chat("SYSTEM", f"Fichier reçu : {safe_name} → {out_path}", "#00ffff")
        except Exception as e:
            self.app.log(f"[FILE RECV ERR] {e}")
        finally:
            try:
                client.close()
            except Exception:
                pass

# ============================================================
# GUI
# ============================================================
class Kill666App:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} {APP_VERSION} | {AUTHOR}")
        self.root.geometry("1400x900")
        self.root.configure(bg="#050505")
        self.root.minsize(1200, 800)

        self.profile_manager = ProfileManager()
        self.profile = self.profile_manager.profile
        self.theme = THEMES.get(self.profile.get("theme", "hacker_green"), THEMES["hacker_green"])
        self.apply_theme()

        self.network = NetworkCore(self)
        self.video = VideoCore(self)
        self.voice = VoiceCore(self)
        self.files = FileTransferCore(self)

        self.chat_history = []
        self.video_labels = {}
        self.audio_queue = queue.Queue()

        self.build_ui()
        self.after_init()

    def apply_theme(self):
        t = self.theme
        self.root.configure(bg=t["bg"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=t["bg"])
        style.configure("TButton", background=t["secondary"], foreground=t["fg"], bordercolor=t["border"],
                        focuscolor=t["accent"], lightcolor=t["accent"], darkcolor=t["secondary"])
        style.map("TButton", background=[("active", t["accent"])], foreground=[("active", t["bg"])])
        style.configure("TLabel", background=t["bg"], foreground=t["fg"])
        style.configure("TEntry", fieldbackground=t["input_bg"], foreground=t["fg"], insertcolor=t["fg"])
        style.configure("TNotebook", background=t["bg"], tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab", background=t["secondary"], foreground=t["fg"], padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", t["accent"])], foreground=[("selected", t["bg"])])

    def build_ui(self):
        t = self.theme

        # Main container
        main = Frame(self.root, bg=t["bg"])
        main.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Header
        header = Frame(main, bg=t["bg"], highlightbackground=t["border"], highlightthickness=1)
        header.pack(fill=X, pady=(0, 5))
        Label(header, text=f"☠ {APP_NAME} {APP_VERSION} ☠", bg=t["bg"], fg=t["accent"],
              font=("Courier New", 22, "bold")).pack(side=LEFT, padx=10)
        Label(header, text=f"Réseau privé | {AUTHOR}", bg=t["bg"], fg=t["fg"],
              font=("Courier New", 10)).pack(side=LEFT, padx=20)
        self.status_label = Label(header, text="[ DISCONNECTED ]", bg=t["bg"], fg=t["danger"],
                                  font=("Courier New", 10, "bold"))
        self.status_label.pack(side=RIGHT, padx=10)
        self.ip_label = Label(header, text=f"IP: {self.network.ip}", bg=t["bg"], fg=t["info"],
                              font=("Courier New", 10))
        self.ip_label.pack(side=RIGHT, padx=10)

        # Notebook
        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill=BOTH, expand=True)

        # TAB 1: Chat
        self.chat_frame = Frame(self.notebook, bg=t["bg"])
        self.notebook.add(self.chat_frame, text=" 💬 CHAT LIVE ")
        self.build_chat_tab()

        # TAB 2: Video Room
        self.video_frame = Frame(self.notebook, bg=t["bg"])
        self.notebook.add(self.video_frame, text=" 📹 VIDEO ROOM ")
        self.build_video_tab()

        # TAB 3: Voice / File
        self.comm_frame = Frame(self.notebook, bg=t["bg"])
        self.notebook.add(self.comm_frame, text=" 🎙️ VOICE & FILES ")
        self.build_comm_tab()

        # TAB 4: Members
        self.members_frame = Frame(self.notebook, bg=t["bg"])
        self.notebook.add(self.members_frame, text=" 👤 MEMBRES ")
        self.build_members_tab()

        # TAB 5: Profile
        self.profile_frame = Frame(self.notebook, bg=t["bg"])
        self.notebook.add(self.profile_frame, text=" ⚙️ PROFIL ")
        self.build_profile_tab()

        # Footer
        footer = Frame(main, bg=t["bg"], highlightbackground=t["border"], highlightthickness=1)
        footer.pack(fill=X, pady=(5, 0))
        self.footer_label = Label(footer, text="[ Prêt ]", bg=t["bg"], fg=t["fg"], font=("Courier New", 9))
        self.footer_label.pack(side=LEFT, padx=10)

    def build_chat_tab(self):
        t = self.theme
        paned = PanedWindow(self.chat_frame, bg=t["border"], orient=HORIZONTAL)
        paned.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Chat area
        chat_container = Frame(paned, bg=t["bg"])
        paned.add(chat_container, width=900)

        self.chat_display = Text(chat_container, bg=t["chat_bg"], fg=t["chat_fg"], font=("Consolas", 11),
                                  wrap=WORD, state=DISABLED, padx=10, pady=10,
                                  insertbackground=t["accent"], relief=FLAT)
        self.chat_display.pack(fill=BOTH, expand=True)
        self.chat_display.tag_config("timestamp", foreground="#666666", font=("Consolas", 8))
        self.chat_display.tag_config("username", font=("Consolas", 11, "bold"))
        self.chat_display.tag_config("private", foreground=t["warn"], background="#333300")
        self.chat_display.tag_config("system", foreground=t["info"], font=("Consolas", 10, "italic"))

        scrollbar = ttk.Scrollbar(self.chat_display)
        self.chat_display.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.chat_display.yview)

        input_frame = Frame(chat_container, bg=t["bg"])
        input_frame.pack(fill=X, pady=5)
        self.msg_entry = Entry(input_frame, bg=t["input_bg"], fg=t["fg"], font=("Consolas", 12),
                               insertbackground=t["accent"], relief=FLAT)
        self.msg_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.msg_entry.bind("<Return>", lambda e: self.send_chat())
        Button(input_frame, text="ENVOYER", command=self.send_chat, bg=t["accent"], fg=t["bg"],
               font=("Courier New", 10, "bold"), relief=FLAT, padx=15).pack(side=LEFT, padx=5)
        Button(input_frame, text="FICHIER", command=self.send_file_dialog, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 10), relief=FLAT, padx=10).pack(side=LEFT, padx=5)

        # Side panel users + actions
        side = Frame(paned, bg=t["bg"], highlightbackground=t["border"], highlightthickness=1)
        paned.add(side, width=300)
        Label(side, text="👁 OPÉRATEURS EN LIGNE", bg=t["bg"], fg=t["accent"],
              font=("Courier New", 12, "bold")).pack(pady=10)
        self.users_listbox = Listbox(side, bg=t["chat_bg"], fg=t["chat_fg"], font=("Consolas", 10),
                                      selectbackground=t["accent"], selectforeground=t["bg"])
        self.users_listbox.pack(fill=BOTH, expand=True, padx=5, pady=5)
        Button(side, text="📹 Appel vidéo", command=self.call_selected, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 10), relief=FLAT).pack(fill=X, padx=5, pady=2)
        Button(side, text="🎙️ Appel vocal", command=self.voice_call_selected, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 10), relief=FLAT).pack(fill=X, padx=5, pady=2)
        Button(side, text="📁 Envoyer fichier", command=self.send_file_to_selected, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 10), relief=FLAT).pack(fill=X, padx=5, pady=2)
        Button(side, text="💬 Message privé", command=self.private_msg_selected, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 10), relief=FLAT).pack(fill=X, padx=5, pady=2)

    def build_video_tab(self):
        t = self.theme
        top = Frame(self.video_frame, bg=t["bg"])
        top.pack(fill=X, pady=5)
        Label(top, text="📹 SALLE VIDÉO CONFÉRENCE", bg=t["bg"], fg=t["accent"],
              font=("Courier New", 14, "bold")).pack(side=LEFT, padx=10)
        Button(top, text="🎥 Démarrer caméra", command=self.start_video, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 10), relief=FLAT).pack(side=LEFT, padx=5)
        Button(top, text="⏹ Arrêter caméra", command=self.stop_video, bg=t["danger"], fg="white",
               font=("Courier New", 10), relief=FLAT).pack(side=LEFT, padx=5)
        Button(top, text="🎨 Filtre", command=self.cycle_filter, bg=t["info"], fg=t["bg"],
               font=("Courier New", 10), relief=FLAT).pack(side=LEFT, padx=5)
        Button(top, text="⏺ REC", command=self.toggle_recording, bg=t["danger"], fg="white",
               font=("Courier New", 10), relief=FLAT).pack(side=LEFT, padx=5)

        self.video_grid = Frame(self.video_frame, bg=t["bg"])
        self.video_grid.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Self video
        self.self_video_label = Label(self.video_grid, bg="black", text="[ CAM OFF ]",
                                      fg=t["accent"], font=("Courier New", 12))
        self.self_video_label.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        self.filter_label = Label(top, text=f"Filtre: {self.video.filter_mode}", bg=t["bg"], fg=t["fg"],
                                   font=("Courier New", 10))
        self.filter_label.pack(side=RIGHT, padx=10)

    def build_comm_tab(self):
        t = self.theme
        paned = PanedWindow(self.comm_frame, bg=t["border"], orient=VERTICAL)
        paned.pack(fill=BOTH, expand=True, padx=5, pady=5)

        voice_panel = Frame(paned, bg=t["bg"], highlightbackground=t["border"], highlightthickness=1)
        paned.add(voice_panel, height=250)
        Label(voice_panel, text="🎙️ COMMUNICATION VOCALE", bg=t["bg"], fg=t["accent"],
              font=("Courier New", 14, "bold")).pack(pady=10)
        self.voice_status = Label(voice_panel, text="[ MICRO COUPÉ ]", bg=t["bg"], fg=t["danger"],
                                   font=("Courier New", 12, "bold"))
        self.voice_status.pack(pady=5)
        Button(voice_panel, text="🎤 Activer micro", command=self.start_voice, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 11), relief=FLAT, padx=20).pack(pady=3)
        Button(voice_panel, text="🔇 Couper micro", command=self.mute_voice, bg=t["warn"], fg=t["bg"],
               font=("Courier New", 11), relief=FLAT, padx=20).pack(pady=3)
        Button(voice_panel, text="🎧 Sourdine", command=self.deafen_voice, bg=t["info"], fg=t["bg"],
               font=("Courier New", 11), relief=FLAT, padx=20).pack(pady=3)

        file_panel = Frame(paned, bg=t["bg"], highlightbackground=t["border"], highlightthickness=1)
        paned.add(file_panel, height=400)
        Label(file_panel, text="📁 TRANSFERT DE FICHIERS", bg=t["bg"], fg=t["accent"],
              font=("Courier New", 14, "bold")).pack(pady=10)
        self.file_log = Text(file_panel, bg=t["chat_bg"], fg=t["chat_fg"], font=("Consolas", 10),
                             state=DISABLED, height=12)
        self.file_log.pack(fill=BOTH, expand=True, padx=10, pady=5)
        Button(file_panel, text="📤 Envoyer un fichier", command=self.send_file_dialog, bg=t["accent"], fg=t["bg"],
               font=("Courier New", 11), relief=FLAT, padx=20).pack(pady=5)
        Button(file_panel, text="📂 Ouvrir dossier reçus", command=self.open_received_folder, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 11), relief=FLAT, padx=20).pack(pady=5)

    def build_members_tab(self):
        t = self.theme
        Label(self.members_frame, text="👤 MEMBRES DU RÉSEAU PRIVÉ", bg=t["bg"], fg=t["accent"],
              font=("Courier New", 16, "bold")).pack(pady=10)
        self.members_text = Text(self.members_frame, bg=t["chat_bg"], fg=t["chat_fg"], font=("Consolas", 11),
                                  wrap=WORD, state=DISABLED, padx=10, pady=10)
        self.members_text.pack(fill=BOTH, expand=True, padx=10, pady=5)

    def build_profile_tab(self):
        t = self.theme
        Label(self.profile_frame, text="⚙️ CONFIGURATION PROFIL", bg=t["bg"], fg=t["accent"],
              font=("Courier New", 16, "bold")).pack(pady=10)

        form = Frame(self.profile_frame, bg=t["bg"])
        form.pack(pady=10)

        Label(form, text="PSEUDO:", bg=t["bg"], fg=t["fg"], font=("Consolas", 12)).grid(row=0, column=0, sticky=W, pady=5)
        self.username_entry = Entry(form, bg=t["input_bg"], fg=t["fg"], font=("Consolas", 12), insertbackground=t["accent"])
        self.username_entry.insert(0, self.profile["username"])
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        Label(form, text="STATUT:", bg=t["bg"], fg=t["fg"], font=("Consolas", 12)).grid(row=1, column=0, sticky=W, pady=5)
        self.status_entry = Entry(form, bg=t["input_bg"], fg=t["fg"], font=("Consolas", 12), insertbackground=t["accent"])
        self.status_entry.insert(0, self.profile["status"])
        self.status_entry.grid(row=1, column=1, pady=5, padx=10)

        Label(form, text="BIO:", bg=t["bg"], fg=t["fg"], font=("Consolas", 12)).grid(row=2, column=0, sticky=NW, pady=5)
        self.bio_entry = Text(form, bg=t["input_bg"], fg=t["fg"], font=("Consolas", 11), insertbackground=t["accent"],
                              height=4, width=30)
        self.bio_entry.insert("1.0", self.profile["bio"])
        self.bio_entry.grid(row=2, column=1, pady=5, padx=10)

        Label(form, text="RÔLE:", bg=t["bg"], fg=t["fg"], font=("Consolas", 12)).grid(row=3, column=0, sticky=W, pady=5)
        self.role_var = StringVar(value=self.profile.get("role", "Operative"))
        OptionMenu(form, self.role_var, "Operative", "Admin", "Spectator", "Hacker", "TchadSec").grid(row=3, column=1, sticky=W, pady=5, padx=10)

        Label(form, text="THÈME:", bg=t["bg"], fg=t["fg"], font=("Consolas", 12)).grid(row=4, column=0, sticky=W, pady=5)
        self.theme_var = StringVar(value=self.profile.get("theme", "hacker_green"))
        OptionMenu(form, self.theme_var, *THEMES.keys()).grid(row=4, column=1, sticky=W, pady=5, padx=10)

        Button(form, text="💾 Sauvegarder profil", command=self.save_profile, bg=t["accent"], fg=t["bg"],
               font=("Courier New", 11, "bold"), relief=FLAT).grid(row=5, column=1, pady=15, sticky=W)

        net_frame = Frame(self.profile_frame, bg=t["bg"], highlightbackground=t["border"], highlightthickness=1)
        net_frame.pack(fill=X, padx=20, pady=20)
        Label(net_frame, text="🔗 CONNEXION RÉSEAU", bg=t["bg"], fg=t["accent"],
              font=("Courier New", 14, "bold")).pack(pady=5)
        self.connect_entry = Entry(net_frame, bg=t["input_bg"], fg=t["fg"], font=("Consolas", 12), insertbackground=t["accent"])
        self.connect_entry.insert(0, "192.168.1.x")
        self.connect_entry.pack(side=LEFT, fill=X, expand=True, padx=10, pady=10)
        Button(net_frame, text="Se connecter", command=self.connect_to_peer, bg=t["secondary"], fg=t["fg"],
               font=("Courier New", 10), relief=FLAT).pack(side=LEFT, padx=5)
        Button(net_frame, text="🔄 Scanner réseau", command=self.scan_network, bg=t["info"], fg=t["bg"],
               font=("Courier New", 10), relief=FLAT).pack(side=LEFT, padx=5)

    def after_init(self):
        self.network.start_server()
        self.status_label.config(text="[ EN LIGNE ]", fg=self.theme["accent"])
        self.footer_label.config(text=f"[ IP locale: {self.network.ip} | Port: {DEFAULT_PORT} | Mode: PRIVE ]")
        self.log("Système KILL666 initialisé. Réseau privé actif.")
        self.update_users_list()

    # ------------------ ACTIONS ------------------
    def send_chat(self):
        text = self.msg_entry.get().strip()
        if not text:
            return
        self.msg_entry.delete(0, END)
        self.append_chat(self.profile["username"], text, self.profile["color"], self.profile.get("avatar"))
        self.network.broadcast_chat(text)
        log_event(f"CHAT {self.profile['username']}: {text}")

    def append_chat(self, username, text, color, avatar=None, private=False):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=NORMAL)
        tag = "private" if private else "normal"
        self.chat_display.insert(END, f"[{ts}] ", "timestamp")
        self.chat_display.insert(END, f"{username}: ", "username")
        self.chat_display.insert(END, f"{text}\n", tag)
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)

    def log(self, text):
        self.append_chat("SYSTEM", text, self.theme["info"])
        log_event(text)

    def update_users_list(self):
        self.users_listbox.delete(0, END)
        with self.network.lock:
            for ip, info in self.network.peers.items():
                self.users_listbox.insert(END, f"{info['username']} @ {ip} [{info['status']}]")
        self.update_members_tab()

    def update_members_tab(self):
        self.members_text.config(state=NORMAL)
        self.members_text.delete("1.0", END)
        self.members_text.insert(END, f"Opérateur local: {self.profile['username']} ({self.network.ip})\n")
        self.members_text.insert(END, "-" * 60 + "\n")
        with self.network.lock:
            for ip, info in self.network.peers.items():
                self.members_text.insert(END, f"\n👤 {info['username']}\n")
                self.members_text.insert(END, f"   IP      : {ip}\n")
                self.members_text.insert(END, f"   Statut  : {info['status']}\n")
                self.members_text.insert(END, f"   Rôle    : {info['role']}\n")
                self.members_text.insert(END, f"   Bio     : {info.get('bio','')}\n")
        self.members_text.config(state=DISABLED)

    def save_profile(self):
        self.profile["username"] = self.username_entry.get() or self.profile["username"]
        self.profile["status"] = self.status_entry.get() or "ONLINE"
        self.profile["bio"] = self.bio_entry.get("1.0", END).strip()
        self.profile["role"] = self.role_var.get()
        self.profile["theme"] = self.theme_var.get()
        self.profile_manager.save()
        self.theme = THEMES[self.profile["theme"]]
        self.apply_theme()
        messagebox.showinfo("KILL666", "Profil sauvegardé.")
        log_event("Profile updated")

    def connect_to_peer(self):
        ip = self.connect_entry.get().strip()
        if ip:
            self.network.connect_to(ip)
            self.log(f"Tentative de connexion à {ip}")
            self.video.connect_to_peer_video(ip)

    def scan_network(self):
        self.log("Scan du réseau local en cours...")
        base = ".".join(self.network.ip.split(".")[:3])
        def scan():
            for i in range(1, 255):
                ip = f"{base}.{i}"
                if ip == self.network.ip:
                    continue
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.3)
                    result = sock.connect_ex((ip, DEFAULT_PORT))
                    if result == 0:
                        self.network.connect_to(ip)
                except Exception:
                    pass
            self.log("Scan terminé.")
        threading.Thread(target=scan, daemon=True).start()

    def send_file_dialog(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        sel = self.users_listbox.curselection()
        if not sel:
            self.network.broadcast_chat(f"[FILE OFFER] {os.path.basename(path)}")
            return
        ip = list(self.network.peers.keys())[sel[0]]
        self.files.offer_file(ip, path)
        self.log(f"Offre de fichier envoyée à {ip}")

    def send_file_to_selected(self):
        sel = self.users_listbox.curselection()
        if not sel:
            messagebox.showwarning("KILL666", "Sélectionne un utilisateur d'abord.")
            return
        ip = list(self.network.peers.keys())[sel[0]]
        path = filedialog.askopenfilename()
        if path:
            self.files.offer_file(ip, path)

    def handle_file_offer(self, ip, msg):
        self.log(f"{msg.get('from')} propose {msg.get('filename')} ({msg.get('size')} bytes)")
        if messagebox.askyesno("KILL666", f"{msg.get('from')} veut envoyer {msg.get('filename')}. Accepter ?"):
            self.files.send_file(ip, self.files.transfers.get(msg.get("tid"), {}).get("path", ""), msg.get("tid"))

    def call_selected(self):
        sel = self.users_listbox.curselection()
        if not sel:
            return
        ip = list(self.network.peers.keys())[sel[0]]
        self.video.connect_to_peer_video(ip)
        self.log(f"Appel vidéo lancé vers {ip}")

    def voice_call_selected(self):
        self.start_voice()
        self.log("Canal vocal global ouvert.")

    def private_msg_selected(self):
        sel = self.users_listbox.curselection()
        if not sel:
            return
        ip = list(self.network.peers.keys())[sel[0]]
        text = simpledialog.askstring("Message privé", "Message :")
        if text:
            self.network.broadcast_chat(text, private_to=ip)

    # ------------------ VIDEO ------------------
    def start_video(self):
        self.video.start()
        self.log("Caméra activée.")

    def stop_video(self):
        self.video.stop()
        self.self_video_label.config(image="", text="[ CAM OFF ]")
        self.log("Caméra désactivée.")

    def cycle_filter(self):
        modes = ["matrix_green", "blood_red", "cyber_blue", "purple_haze", "noir_white",
                 "scanlines", "edge", "thermal", "normal"]
        idx = modes.index(self.video.filter_mode) if self.video.filter_mode in modes else 0
        self.video.filter_mode = modes[(idx + 1) % len(modes)]
        self.filter_label.config(text=f"Filtre: {self.video.filter_mode}")
        self.log(f"Filtre caméra: {self.video.filter_mode}")

    def toggle_recording(self):
        if not self.video.recording:
            filename = f"recording_{int(time.time())}.avi"
            path = DATA_DIR / filename
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video.writer = cv2.VideoWriter(str(path), fourcc, self.video.fps, self.video.resolution)
            self.video.recording = True
            self.log(f"Enregistrement démarré: {path}")
        else:
            self.video.recording = False
            if self.video.writer:
                self.video.writer.release()
                self.video.writer = None
            self.log("Enregistrement arrêté.")

    def update_self_video(self, frame):
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img.thumbnail((640, 480))
            imgtk = ImageTk.PhotoImage(image=img)
            self.self_video_label.imgtk = imgtk
            self.self_video_label.config(image=imgtk, text="")
        except Exception:
            pass

    def update_peer_video(self, ip, frame):
        if ip not in self.video_labels:
            lbl = Label(self.video_grid, bg="black", text=f"[ {ip} ]", fg=self.theme["accent"])
            lbl.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
            self.video_labels[ip] = lbl
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img.thumbnail((320, 240))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_labels[ip].imgtk = imgtk
            self.video_labels[ip].config(image=imgtk, text="")
        except Exception:
            pass

    # ------------------ VOICE ------------------
    def start_voice(self):
        self.voice.start()
        self.voice_status.config(text="[ MICRO ACTIF ]", fg=self.theme["accent"])
        self.log("Canal vocal activé.")

    def mute_voice(self):
        self.voice.muted = True
        self.voice_status.config(text="[ MICRO COUPÉ ]", fg=self.theme["danger"])

    def deafen_voice(self):
        self.voice.deafened = not self.voice.deafened
        text = "[ SOURDINE ON ]" if self.voice.deafened else "[ AUDIO ACTIF ]"
        self.voice_status.config(text=text, fg=self.theme["warn"] if self.voice.deafened else self.theme["accent"])

    def play_audio(self, data):
        self.voice.play_audio(data)

    def handle_signal(self, ip, msg):
        pass

    def open_received_folder(self):
        try:
            webbrowser.open(str(FILES_DIR))
        except Exception:
            pass

    def on_close(self):
        self.video.stop()
        self.voice.stop()
        self.network.stop()
        self.root.destroy()

# ============================================================
# SPLASH / MAIN
# ============================================================
def show_splash():
    splash = Tk()
    splash.overrideredirect(True)
    w, h = 700, 400
    sw, sh = splash.winfo_screenwidth(), splash.winfo_screenheight()
    x, y = (sw - w) // 2, (sh - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")
    splash.configure(bg="black")

    Label(splash, text=APP_NAME, fg="#00ff41", bg="black", font=("Courier New", 48, "bold")).pack(pady=30)
    Label(splash, text="PRIVATE SECURE NETWORK INTERFACE", fg="#00ff41", bg="black", font=("Courier New", 14)).pack()
    Label(splash, text=f"Créé par {AUTHOR}", fg="#00aa00", bg="black", font=("Courier New", 12)).pack(pady=10)

    canvas = Canvas(splash, width=600, height=20, bg="black", highlightthickness=0)
    canvas.pack(pady=40)
    bar = canvas.create_rectangle(0, 0, 0, 20, fill="#00ff41", outline="")
    status = Label(splash, text="[ Initialisation du noyau... ]", fg="#00ff41", bg="black", font=("Courier New", 10))
    status.pack()

    def load(i=0):
        if i > 100:
            splash.destroy()
            return
        canvas.coords(bar, 0, 0, i * 6, 20)
        msgs = ["Chargement modules...", "Scan réseau...", "Initialisation chiffrement...", "Connexion pair-à-pair...", "Prêt."]
        status.config(text=f"[ {msgs[min(i//20, len(msgs)-1)]} ]")
        splash.after(40, load, i + 1)

    splash.after(100, load)
    splash.mainloop()

def main():
    show_splash()
    root = Tk()
    app = Kill666App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()

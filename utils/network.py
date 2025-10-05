"""
Network utilities for chat client
"""

import socket
import threading
import time

class ConnectionManager:
    """Quản lý kết nối network cho client"""
    
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.socket = None
        self.connected = False
        
    def create_connection(self, host, port):
        """Tạo kết nối TCP đến server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((host, port))
            self.connected = True
            return True
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            return False
            
    def send_data(self, data):
        """Gửi dữ liệu qua socket"""
        if not self.connected or not self.socket:
            return False
            
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.socket.send(data)
            return True
        except Exception as e:
            print(f"Lỗi gửi dữ liệu: {e}")
            self.connected = False
            return False
            
    def receive_data(self, buffer_size=1024):
        """Nhận dữ liệu từ socket"""
        if not self.connected or not self.socket:
            return None
            
        try:
            data = self.socket.recv(buffer_size)
            if not data:
                self.connected = False
                return None
            return data.decode('utf-8')
        except Exception as e:
            print(f"Lỗi nhận dữ liệu: {e}")
            self.connected = False
            return None
            
    def close_connection(self):
        """Đóng kết nối"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

def ping_server(host, port, timeout=5):
    """Kiểm tra xem server có hoạt động không"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False
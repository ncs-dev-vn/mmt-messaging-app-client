import socket
import threading

try:
    from config import get_default_server_info, get_buffer_size
    from utils import validate_nickname
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

class ChatClient:
    def __init__(self, host=None, port=None):
        self.host = host or '127.0.0.1'
        self.port = port or 12345
        self.buffer_size = 1024
        self.client_socket = None
        self.is_connected = False
        
    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.is_connected = True
            print(f'Connected to {self.host}:{self.port}')
            return True
        except Exception as e:
            print(f'Connection failed: {e}')
            return False
            
    def send_message(self, message):
        if message.strip():
            self.client_socket.send(message.encode('utf-8'))
            
def main():
    print("Simple Chat Client")
    client = ChatClient()
    if client.connect():
        print("Connected successfully!")

if __name__ == "__main__":
    main()

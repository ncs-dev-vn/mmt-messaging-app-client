import socket
import threading
import sys

try:
    from config import get_default_server_info, get_buffer_size, get_connection_timeout, get_server_info_from_user
    from utils import validate_nickname, validate_message_content
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️ Config module không khả dụng, sử dụng giá trị mặc định")

class ChatClient:
    def __init__(self, host=None, port=None, buffer_size=None):
        # Sử dụng các tham số được truyền vào (từ user input)
        if CONFIG_AVAILABLE:
            self.host = host or '127.0.0.1'
            self.port = port or 12345
            self.buffer_size = buffer_size or get_buffer_size()
            self.timeout = get_connection_timeout()
        else:
            # Fallback khi không có config
            self.host = host or '127.0.0.1'
            self.port = port or 12345
            self.buffer_size = buffer_size or 1024
            self.timeout = 30
            
        self.client_socket = None
        self.is_connected = False
        self.nickname = ""
        self.running = False
        
    def connect(self):
        """Kết nối đến server với config system và timeout"""
        try:
            print(f'🔗 Đang kết nối đến {self.host}:{self.port}...')
            
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(self.timeout)
            self.client_socket.connect((self.host, self.port))
            self.client_socket.settimeout(None)  # Reset về blocking mode
            
            self.is_connected = True
            print(f'✅ Đã kết nối thành công với Server ({self.host}:{self.port})')
            return True
            
        except socket.timeout:
            print(f'❌ Kết nối timeout sau {self.timeout} giây')
            return False
        except ConnectionRefusedError:
            print(f'❌ Server từ chối kết nối. Kiểm tra server có đang chạy không?')
            return False
        except Exception as e:
            print(f'❌ Lỗi kết nối: {e}')
            return False
    
    def set_nickname(self):
        """Nhập và validate nickname"""
        while True:
            try:
                nickname = input("Nhập nickname của bạn: ").strip()
                
                if CONFIG_AVAILABLE:
                    is_valid, message = validate_nickname(nickname)
                    if not is_valid:
                        print(f'❌ {message}')
                        continue
                else:
                    # Basic validation khi không có config
                    if not nickname or len(nickname) > 20:
                        print('❌ Nickname không hợp lệ (1-20 ký tự)')
                        continue
                
                # Gửi nickname đến server với prefix đặc biệt
                nickname_command = f"SET_NICKNAME:{nickname}"
                self.client_socket.send(nickname_command.encode('utf-8'))
                self.nickname = nickname
                print(f'✅ Nickname "{nickname}" đã được đặt')
                return True
                
            except KeyboardInterrupt:
                print('\n👋 Đã hủy nhập nickname')
                return False
            except Exception as e:
                print(f'❌ Lỗi khi đặt nickname: {e}')
                return False
    
    def send_message(self, message):
        """Gửi tin nhắn với content validation"""
        if not message.strip():
            return False
            
        # Content moderation (luôn chạy để đảm bảo an toàn)
        try:
            is_valid, filtered_msg, reason = validate_message_content(message)
            if not is_valid:
                print(f'❌ {reason}')
                return False
            if reason != "OK" and "Cảnh báo" in reason:
                print(f'⚠️ {reason}')
            message = filtered_msg
        except ImportError:
            print("⚠️ Content moderation không khả dụng")
        except Exception as e:
            print(f"⚠️ Lỗi content moderation: {e}")
            pass  # Fallback nếu content moderation lỗi
        
        try:
            # Format tin nhắn chat với prefix đặc biệt
            chat_message = f"CHAT:{self.nickname}: {message}"
            self.client_socket.send(chat_message.encode('utf-8'))
            return True
        except Exception as e:
            print(f'❌ Không thể gửi tin nhắn: {e}')
            self.is_connected = False
            return False
            
    def receive_messages(self):
        """Nhận tin nhắn từ server (chạy trong thread)"""
        while self.running and self.is_connected:
            try:
                data = self.client_socket.recv(self.buffer_size)
                if not data:
                    print('\n💔 Mất kết nối với server')
                    self.is_connected = False
                    break
                    
                message = data.decode('utf-8')
                print(f'\n{message}')
                
            except socket.timeout:
                continue  # Timeout bình thường
            except Exception as e:
                if self.running:  # Chỉ in lỗi nếu client vẫn đang chạy
                    print(f'\n❌ Lỗi nhận tin nhắn: {e}')
                break
    
    def start_chat(self):
        """Bắt đầu chat session"""
        if not self.is_connected:
            print('❌ Chưa kết nối đến server')
            return False
            
        if not self.set_nickname():
            return False
        
        # Bắt đầu thread nhận tin nhắn
        self.running = True
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        print('\n💬 Bạn có thể bắt đầu chat! Gõ "quit" để thoát.')
        print('=' * 50)
        
        # Vòng lặp gửi tin nhắn
        try:
            while self.running and self.is_connected:
                message = input().strip()
                
                if message.lower() in ['quit', 'exit']:
                    break
                elif message:
                    success = self.send_message(message)
                    if not success:
                        break
                        
        except KeyboardInterrupt:
            print('\n👋 Đang thoát...')
        finally:
            self.disconnect()
        
        return True
    
    def disconnect(self):
        """Ngắt kết nối an toàn"""
        self.running = False
        self.is_connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        print('👋 Đã ngắt kết nối')

def main():
    """Entry point chính"""
    print("=== Multi-User Chat Client ===")
    
    try:
        # Lấy server info từ user input
        if CONFIG_AVAILABLE:
            host, port = get_server_info_from_user()
        else:
            print("⚠️ Config không khả dụng, sử dụng mặc định")
            host, port = '127.0.0.1', 12345
        
        # Tạo client với server info từ user
        client = ChatClient(host=host, port=port)
        
        # Kết nối
        if not client.connect():
            print("❌ Không thể kết nối đến server")
            return 1
        
        # Bắt đầu chat
        client.start_chat()
        
        return 0
        
    except KeyboardInterrupt:
        print('\n👋 Goodbye!')
        return 130
    except Exception as e:
        print(f'❌ Lỗi không mong đợi: {e}')
        return 1

if __name__ == "__main__":
    sys.exit(main())

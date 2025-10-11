"""
Chat Client - Core client implementation
"""

import socket
import threading

from config.settings import (
    get_buffer_size, get_connection_timeout, 
    DEFAULT_HOST, DEFAULT_PORT
)
from ui.formatters import MessageFormatter
from ui.ui_helpers import UIHelper
from utils.validators import validate_nickname
from utils.content_filter import validate_message_content, is_command, parse_command
from client.message_handler import MessageHandler

class ChatClient:
    """Main chat client class"""
    
    def __init__(self, host=None, port=None, buffer_size=None):
        self.host = host or DEFAULT_HOST
        self.port = port or DEFAULT_PORT
        self.buffer_size = buffer_size or get_buffer_size()
        self.timeout = get_connection_timeout()
        
        self.client_socket = None
        self.is_connected = False
        self.nickname = ""
        self.running = False
        self.in_waiting_queue = False
        
        # Message handler sẽ được khởi tạo sau khi có nickname
        self.message_handler = None
    
    def connect(self):
        """Kết nối đến server"""
        try:
            print(MessageFormatter.format_info_message(f'Đang kết nối đến {self.host}:{self.port}...'))
            
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(self.timeout)
            self.client_socket.connect((self.host, self.port))
            self.client_socket.settimeout(None)  # Reset về blocking mode
            
            self.is_connected = True
            print(MessageFormatter.format_success_message(f'Đã kết nối thành công với Server ({self.host}:{self.port})'))
            return True
            
        except socket.timeout:
            print(MessageFormatter.format_error_message(f'Kết nối timeout sau {self.timeout} giây'))
            return False
        except ConnectionRefusedError:
            print(MessageFormatter.format_error_message('Server từ chối kết nối. Kiểm tra server có đang chạy không?'))
            return False
        except Exception as e:
            print(MessageFormatter.format_error_message(f'Lỗi kết nối: {e}'))
            return False
    
    def set_nickname(self):
        """Nhập và validate nickname, chờ phản hồi từ server"""
        while True:
            try:
                nickname = input("Nhập nickname của bạn: ").strip()
                
                # Validate nickname
                is_valid, message = validate_nickname(nickname)
                if not is_valid:
                    print(MessageFormatter.format_error_message(message))
                    continue
                
                # Gửi nickname đến server và chờ phản hồi
                nickname_command = f"/nick {nickname}"
                self.client_socket.send(nickname_command.encode('utf-8'))
                
                print(MessageFormatter.format_info_message(f'Đang kiểm tra nickname "{nickname}"...'))
                
                # Chờ phản hồi từ server về nickname
                if self.wait_for_nickname_response(nickname):
                    # Khởi tạo message handler với nickname
                    self.message_handler = MessageHandler(self.nickname)
                    return True
                    
                print(MessageFormatter.format_warning_message("Vui lòng chọn nickname khác..."))
                
            except KeyboardInterrupt:
                print('\n👋 Đã hủy nhập nickname')
                return False
            except Exception as e:
                print(MessageFormatter.format_error_message(f'Lỗi khi đặt nickname: {e}'))
                return False
    
    def wait_for_nickname_response(self, nickname):
        """Chờ phản hồi từ server về việc nickname có hợp lệ không"""
        try:
            # Đặt timeout để chờ response từ server
            self.client_socket.settimeout(10)
            data = self.client_socket.recv(self.buffer_size)
            self.client_socket.settimeout(None)
            
            if data:
                response = data.decode('utf-8').strip()
                
                if response == "NICKNAME_ACCEPTED":
                    self.nickname = nickname
                    print(MessageFormatter.format_success_message(f'Nickname "{nickname}" đã được chấp nhận!'))
                    self.in_waiting_queue = False
                    return True
                    
                elif response == "NICKNAME_TAKEN":
                    print(MessageFormatter.format_error_message(f'Nickname "{nickname}" đã được sử dụng bởi người khác'))
                    return False
                    
                elif response.startswith("NICKNAME_REJECTED"):
                    parts = response.split(":", 1)
                    reason = parts[1] if len(parts) > 1 else "không hợp lệ"
                    print(MessageFormatter.format_error_message(f'Nickname "{nickname}" bị từ chối: {reason}'))
                    return False
                    
                elif "Phòng chat đã đầy" in response or "hàng chờ" in response:
                    print(MessageFormatter.format_server_message(response))
                    self.nickname = nickname
                    self.in_waiting_queue = True
                    return True
                    
                else:
                    # Response khác
                    self.nickname = nickname
                    if not (response in ["NICKNAME_ACCEPTED", "NICKNAME_TAKEN"] or response.startswith("NICKNAME_REJECTED")):
                        print(MessageFormatter.format_warning_message(response))
                    self.in_waiting_queue = False
                    return True
            else:
                print(MessageFormatter.format_error_message('Không nhận được phản hồi từ server'))
                return False
            
        except socket.timeout:
            print(MessageFormatter.format_warning_message('Timeout khi chờ phản hồi từ server'))
            return False
        except Exception as e:
            print(MessageFormatter.format_error_message(f'Lỗi khi chờ phản hồi server: {e}'))
            return False
    
    def send_message(self, message):
        """Gửi tin nhắn với content validation"""
        if not message.strip():
            return False
        
        # Kiểm tra nếu là command
        if is_command(message):
            return self.handle_command(message)
        
        # Content validation
        is_valid, filtered_msg, reason = validate_message_content(message)
        if not is_valid:
            print(MessageFormatter.format_error_message(reason))
            return False
        if reason != "OK" and "Cảnh báo" in reason:
            print(MessageFormatter.format_warning_message(reason))
        
        try:
            # Gửi tin nhắn
            chat_message = f"{self.nickname}: {filtered_msg}"
            self.client_socket.send(chat_message.encode('utf-8'))
            
            # Hiển thị tin nhắn của mình
            print(MessageFormatter.format_own_message(self.nickname, filtered_msg))
            return True
        except Exception as e:
            print(MessageFormatter.format_error_message(f'Không thể gửi tin nhắn: {e}'))
            self.is_connected = False
            return False
    
    def handle_command(self, message):
        """Xử lý các commands"""
        command, args = parse_command(message)
        
        if command == "help":
            UIHelper.print_help()
            return True
        elif command == "debug":
            self.debug_status()
            return True
        elif command == "quit" or command == "exit":
            return False
        elif command == "nick":
            print(MessageFormatter.format_info_message(f"Nickname hiện tại: {self.nickname}"))
            return True
        else:
            print(MessageFormatter.format_warning_message(f"Command không được hỗ trợ: /{command}"))
            return True
    
    def receive_messages(self):
        """Nhận tin nhắn từ server (chạy trong thread)"""
        while self.running and self.is_connected:
            try:
                data = self.client_socket.recv(self.buffer_size)
                if not data:
                    print(MessageFormatter.format_error_message('Mất kết nối với server'))
                    self.is_connected = False
                    break
                    
                raw_message = data.decode('utf-8')
                self.process_received_message(raw_message)
                        
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(MessageFormatter.format_error_message(f'Lỗi nhận tin nhắn: {e}'))
                break
    
    def process_received_message(self, raw_message):
        """Xử lý tin nhắn nhận được từ server"""
        if not self.message_handler:
            # Fallback nếu chưa có message handler
            print(MessageFormatter.format_server_message(raw_message))
            return
        
        # Parse message
        msg_type, sender, content, metadata = self.message_handler.parse_message(raw_message)
        
        # Update queue status nếu cần
        if self.message_handler.should_update_queue_status(msg_type, content, metadata):
            queue_status = self.message_handler.extract_queue_status(content, metadata)
            if queue_status[0] is not None:
                self.in_waiting_queue, queue_position = queue_status
                if not self.in_waiting_queue:
                    print(MessageFormatter.format_info_message('Bạn có thể bắt đầu chat! Gõ tin nhắn để bắt đầu...'))
        
        # Display message
        formatted_message = self.message_handler.format_message_for_display(msg_type, sender, content, metadata)
        if formatted_message:
            print(formatted_message)
    
    def start_chat(self):
        """Bắt đầu chat session"""
        if not self.is_connected:
            print(MessageFormatter.format_error_message('Chưa kết nối đến server'))
            return False
            
        if not self.set_nickname():
            return False
        
        # Bắt đầu thread nhận tin nhắn
        self.running = True
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Hiển thị hướng dẫn
        UIHelper.print_chat_guide()
        
        # Status message
        if not self.in_waiting_queue:
            print(MessageFormatter.format_success_message('Bạn có thể bắt đầu chat ngay!'))
        else:
            print(MessageFormatter.format_info_message('Đang chờ vào phòng chat...'))
        
        # Main chat loop
        try:
            while self.running and self.is_connected:
                message = input(UIHelper.get_colored_prompt()).strip()
                
                if message.lower() in ['quit', 'exit']:
                    break
                elif message:
                    # Kiểm tra queue status
                    if self.in_waiting_queue and not is_command(message):
                        print(MessageFormatter.format_warning_message('Bạn đang trong hàng chờ. Vui lòng đợi để vào phòng chat.'))
                        continue
                    
                    success = self.send_message(message)
                    if not success and not is_command(message):
                        break
                        
        except KeyboardInterrupt:
            print(MessageFormatter.format_info_message('Đang thoát...'))
        finally:
            self.disconnect()

        return True
    
    def debug_status(self):
        """Debug information"""
        print(MessageFormatter.format_info_message("Debug Info:"))
        print(f"  • Host: {self.host}:{self.port}")
        print(f"  • Connected: {self.is_connected}")
        print(f"  • Nickname: {self.nickname}")
        print(f"  • In Queue: {self.in_waiting_queue}")
        print(f"  • Running: {self.running}")
    
    def disconnect(self):
        """Ngắt kết nối an toàn"""
        self.running = False
        self.is_connected = False
        
        if self.client_socket:
            try:
                # Gửi quit command
                quit_command = "/quit"
                self.client_socket.send(quit_command.encode('utf-8'))
            except:
                pass
            finally:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None
        
        print(MessageFormatter.format_success_message('Đã ngắt kết nối'))
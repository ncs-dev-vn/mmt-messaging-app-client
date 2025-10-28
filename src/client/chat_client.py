"""
Chat Client - Core client implementation
"""

import socket
import threading
import time

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
        self.in_chat_room = False
        self.room_status_checked = False
        
        # Variables để handle nickname response
        self.waiting_for_nickname_response = False
        self.nickname_response = None
        self.nickname_response_lock = threading.Lock()
        
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
            
            # Check room status ngay sau khi kết nối
            self.check_initial_room_status()
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
    
    def check_initial_room_status(self):
        """Kiểm tra trạng thái phòng chat ngay sau khi kết nối"""
        try:
            print(MessageFormatter.format_info_message('Đang kiểm tra trạng thái phòng chat...'))
            
            # Bắt đầu thread nhận tin nhắn để lắng nghe response
            self.running = True
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Chờ một khoảng thời gian ngắn để nhận initial response từ server
            timeout_start = time.time()
            timeout_duration = 3  # 3 giây
            
            while not self.room_status_checked and time.time() - timeout_start < timeout_duration:
                time.sleep(0.1)
            
            # Nếu không nhận được response trong 3 giây, giả sử có thể vào phòng chat
            if not self.room_status_checked:
                print(MessageFormatter.format_info_message('Không nhận được thông báo từ server, giả sử có thể vào phòng chat'))
                self.in_chat_room = True
                self.in_waiting_queue = False
                self.room_status_checked = True
                
        except Exception as e:
            print(MessageFormatter.format_warning_message(f'Lỗi khi check room status: {e}'))
            # Fallback: cho vào phòng chat
            self.in_chat_room = True
            self.in_waiting_queue = False
            self.room_status_checked = True
    
    def wait_for_room_access(self):
        """Chờ để có thể vào phòng chat nếu đang trong hàng chờ"""
        if self.in_chat_room:
            return True
            
        if self.in_waiting_queue:
            print(MessageFormatter.format_info_message('Đang trong hàng chờ, chờ vào phòng chat...'))
            
            while self.running and self.is_connected and not self.in_chat_room:
                try:
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    print(MessageFormatter.format_info_message('Đang thoát...'))
                    return False
        
        return self.in_chat_room
    
    def set_nickname(self):
        """Nhập và validate nickname chỉ khi đã vào được phòng chat"""
        if not self.in_chat_room:
            print(MessageFormatter.format_error_message('Chưa vào được phòng chat. Không thể đặt nickname.'))
            return False
            
        while True:
            try:
                nickname = input("Nhập nickname của bạn: ").strip()
                
                # Validate nickname
                is_valid, message = validate_nickname(nickname)
                if not is_valid:
                    print(MessageFormatter.format_error_message(message))
                    continue
                
                # Set flag chờ nickname response
                with self.nickname_response_lock:
                    self.waiting_for_nickname_response = True
                    self.nickname_response = None
                
                # Gửi nickname đến server
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
        timeout_start = time.time()
        timeout_duration = 10  # 10 giây timeout
        
        while time.time() - timeout_start < timeout_duration:
            with self.nickname_response_lock:
                if not self.waiting_for_nickname_response and self.nickname_response is not None:
                    response = self.nickname_response
                    self.nickname_response = None
                    
                    if response == "NICKNAME_ACCEPTED":
                        self.nickname = nickname
                        print(MessageFormatter.format_success_message(f'Nickname "{nickname}" đã được chấp nhận!'))
                        return True
                        
                    elif response == "NICKNAME_TAKEN":
                        print(MessageFormatter.format_error_message(f'Nickname "{nickname}" đã được sử dụng bởi người khác'))
                        return False
                        
                    elif response.startswith("NICKNAME_REJECTED"):
                        parts = response.split(":", 1)
                        reason = parts[1] if len(parts) > 1 else "không hợp lệ"
                        print(MessageFormatter.format_error_message(f'Nickname "{nickname}" bị từ chối: {reason}'))
                        return False
                        
                    else:
                        # Response khác - có thể chấp nhận nickname
                        self.nickname = nickname
                        print(MessageFormatter.format_success_message(f'Server response: {response}'))
                        return True
            
            time.sleep(0.1)  # Chờ 100ms rồi check lại
        
        # Timeout
        with self.nickname_response_lock:
            self.waiting_for_nickname_response = False
        print(MessageFormatter.format_warning_message('Timeout khi chờ phản hồi từ server'))
        return False
    
    def send_message(self, message):
        """Gửi tin nhắn với content validation"""
        if not message.strip():
            return False
        
        # Kiểm tra nếu là command
        if is_command(message):
            return self.handle_command(message)
        
        # Kiểm tra đã có nickname chưa
        if not self.nickname:
            print(MessageFormatter.format_error_message('Vui lòng đặt nickname trước khi gửi tin nhắn'))
            return False
        
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
        # Đánh dấu đã nhận được response từ server về room status
        if not self.room_status_checked:
            self.room_status_checked = True
        
        # Xử lý nickname response trước tiên
        with self.nickname_response_lock:
            if self.waiting_for_nickname_response:
                # Kiểm tra xem có phải nickname response không
                if (raw_message.strip() in ["NICKNAME_ACCEPTED", "NICKNAME_TAKEN"] or
                    raw_message.strip().startswith("NICKNAME_REJECTED")):
                    self.nickname_response = raw_message.strip()
                    self.waiting_for_nickname_response = False
                    return  # Không process message này nữa
    
        # Kiểm tra các thông báo đặc biệt về room status
        if ("có thể vào phòng chat" in raw_message or 
            "welcome to chat room" in raw_message.lower() or
            "you can start chatting" in raw_message.lower() or
            "hiện đã kết nối với chat" in raw_message or
            "đã kết nối với chat" in raw_message.lower() or
            "connected to chat" in raw_message.lower()):
            self.in_chat_room = True
            self.in_waiting_queue = False
            print(MessageFormatter.format_success_message('🎉 Bạn đã vào được phòng chat!'))
            return
        
        if ("phòng chat đã đầy" in raw_message.lower() or 
            "hàng chờ" in raw_message.lower() or
            "room is full" in raw_message.lower() or
            "queue" in raw_message.lower()):
            self.in_waiting_queue = True
            self.in_chat_room = False
            print(MessageFormatter.format_server_message(raw_message))
            return
        
        # Nếu nhận được message bình thường và chưa set room status, 
        # có thể là server cho vào thẳng phòng chat
        if not self.room_status_checked and not self.in_chat_room and not self.in_waiting_queue:
            self.in_chat_room = True
            self.in_waiting_queue = False
            print(MessageFormatter.format_success_message('🎉 Được vào phòng chat ngay!'))
        
        # Nếu chưa có message handler
        if not self.message_handler:
            print(MessageFormatter.format_server_message(raw_message))
            return
        
        # Parse message với message handler
        msg_type, sender, content, metadata = self.message_handler.parse_message(raw_message)
        
        # Update queue status nếu cần
        if self.message_handler.should_update_queue_status(msg_type, content, metadata):
            queue_status = self.message_handler.extract_queue_status(content, metadata)
            if queue_status[0] is not None:
                old_queue_status = self.in_waiting_queue
                self.in_waiting_queue, queue_position = queue_status
                
                # Nếu vừa ra khỏi hàng chờ
                if old_queue_status and not self.in_waiting_queue:
                    self.in_chat_room = True
                    print(MessageFormatter.format_info_message('🎉 Bạn có thể vào phòng chat! Hãy đặt nickname để bắt đầu chat.'))
    
        # Display message
        formatted_message = self.message_handler.format_message_for_display(msg_type, sender, content, metadata)
        if formatted_message:
            print(formatted_message)
    
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
            if self.nickname:
                print(MessageFormatter.format_info_message(f"Nickname hiện tại: {self.nickname}"))
            else:
                print(MessageFormatter.format_warning_message("Chưa đặt nickname"))
            return True
        elif command == "setnick":
            if self.in_chat_room:
                self.set_nickname()
            else:
                print(MessageFormatter.format_error_message("Chưa vào được phòng chat"))
            return True
        elif command == "users":
            # Gửi command users đến server để lấy danh sách
            try:
                self.client_socket.send("/users".encode('utf-8'))
                print(MessageFormatter.format_info_message("Đang lấy danh sách người dùng hoạt động..."))
            except Exception as e:
                print(MessageFormatter.format_error_message(f'Không thể gửi lệnh users: {e}'))
            return True
        else:
            print(MessageFormatter.format_warning_message(f"Command không được hỗ trợ: /{command}"))
            return True
    
    def start_chat(self):
        """Bắt đầu chat session"""
        if not self.is_connected:
            print(MessageFormatter.format_error_message('Chưa kết nối đến server'))
            return False
        
        # Kiểm tra nếu đã ở trong phòng chat thì không cần chờ
        if self.in_chat_room:
            print(MessageFormatter.format_success_message('🎉 Đã vào phòng chat!'))
        else:
            # Chờ để có thể vào phòng chat nếu đang trong hàng chờ
            if not self.wait_for_room_access():
                return False
        
        # Hiển thị hướng dẫn
        UIHelper.print_chat_guide()
        
        # Thông báo có thể đặt nickname
        if self.in_chat_room:
            print(MessageFormatter.format_success_message('🎉 Bạn có thể đặt nickname và bắt đầu chat!'))
        
        # Đặt nickname ngay
        if not self.set_nickname():
            return False
        
        print(MessageFormatter.format_success_message('Bạn có thể bắt đầu chat ngay!'))
        
        # Main chat loop
        try:
            while self.running and self.is_connected:
                message = input(UIHelper.get_colored_prompt()).strip()
                
                # Clear input line after user presses Enter
                print('\033[1A\033[2K', end='', flush=True) 
                
                if message.lower() in ['quit', 'exit']:
                    break
                elif message:
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
        print(f"  • Room Status Checked: {self.room_status_checked}")
        print(f"  • In Chat Room: {self.in_chat_room}")
        print(f"  • In Queue: {self.in_waiting_queue}")
        print(f"  • Nickname: {self.nickname}")
        print(f"  • Running: {self.running}")
        print(f"  • Waiting for nickname: {self.waiting_for_nickname_response}")


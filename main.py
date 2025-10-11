#!/usr/bin/env python3
"""
Multi-User Chat Client
Entry point chính của ứng dụng
"""

import sys
import os

# Thêm src vào Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Entry point chính"""
    try:
        from client.chat_client import ChatClient 
        from config.settings import get_server_info_from_user
        from ui.formatters import MessageFormatter
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        print("Vui lòng kiểm tra cấu trúc dự án")
        return 1
    
    print("=== Multi-User Chat Client ===")
    
    try:
        # Lấy server info từ user input
        host, port = get_server_info_from_user()
        
        # Tạo client với server info từ user
        client = ChatClient(host=host, port=port)
        
        # Kết nối
        if not client.connect():
            print(MessageFormatter.format_error_message("Không thể kết nối đến server"))
            return 1
        
        # Bắt đầu chat
        client.start_chat()
        
        return 0
        
    except KeyboardInterrupt:
        print(MessageFormatter.format_info_message('Goodbye!'))
        return 130
    except Exception as e:
        print(f'❌ Lỗi không mong đợi: {e}')
        return 1

if __name__ == "__main__":
    sys.exit(main())

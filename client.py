#!/usr/bin/env python3
"""
Multi-User Chat Client - Main Entry Point
Kết nối đến server chat và cho phép gửi/nhận tin nhắn với tính năng tự động phát hiện server
"""

import sys
import os

# Thêm thư mục src vào path để import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chat_client import main

if __name__ == "__main__":
    # Chạy main function từ chat_client.py
    main()
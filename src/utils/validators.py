"""
Input validation utilities
"""

import re
import socket
from config.settings import MAX_NICKNAME_LENGTH, MAX_MESSAGE_LENGTH  # Thay đổi từ ..config.settings

def validate_nickname(nickname):
    """
    Validate nickname - simplified rules:
    - 3-20 ký tự
    - Chỉ chữ cái, số, _, -
    - Không toàn bộ là ký tự đặc biệt
    """
    if not nickname:
        return False, "Nickname không được để trống"
    
    if len(nickname) < 3 or len(nickname) > 20:
        return False, "Nickname phải từ 3-20 ký tự"

    # Check allowed characters
    if not re.match(r'^[a-zA-Z0-9_-]+$', nickname):
        return False, "Nickname chỉ được chứa chữ cái, số, _, -"
    
    # Must contain at least one alphanumeric character
    if not re.search(r'[a-zA-Z0-9]', nickname):
        return False, "Nickname phải chứa ít nhất một chữ cái hoặc số"
    
    # Kiểm tra banned nicknames
    banned_names = ['admin', 'server', 'system', 'bot', 'null', 'undefined']
    if nickname.lower() in banned_names:
        return False, f"Nickname '{nickname}' bị cấm sử dụng"
    
    return True, "OK"

def validate_port(port):
    """Validate port number"""
    try:
        port_num = int(port)
        if 1 <= port_num <= 65535:
            return True, port_num
        else:
            return False, "Port phải từ 1 đến 65535"
    except ValueError:
        return False, "Port phải là một số nguyên"

def validate_host(host):
    """Validate host address (IP hoặc hostname)"""
    if not host:
        return False, "Host không được để trống"
    
    # Kiểm tra độ dài
    if len(host) > 255:
        return False, "Host quá dài"
    
    # Kiểm tra IP address
    try:
        socket.inet_aton(host)
        return True, "Valid IP address"
    except socket.error:
        pass
    
    # Kiểm tra hostname
    if re.match(r'^[a-zA-Z0-9.-]+$', host):
        # Kiểm tra không có ký tự đặc biệt không hợp lệ
        if not host.startswith('.') and not host.endswith('.') and '..' not in host:
            return True, "Valid hostname"
    
    return False, "Host không hợp lệ (phải là IP address hoặc hostname)"

def validate_message_length(message):
    """Validate message length"""
    if len(message) > MAX_MESSAGE_LENGTH:
        return False, f"Tin nhắn không được vượt quá {MAX_MESSAGE_LENGTH} ký tự"
    return True, "OK"
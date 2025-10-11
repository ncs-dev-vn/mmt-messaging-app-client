"""
Input validation utilities
"""

import re
import socket
from config.settings import MAX_NICKNAME_LENGTH, MAX_MESSAGE_LENGTH  # Thay đổi từ ..config.settings

def validate_nickname(nickname):
    """
    Validate nickname theo các quy tắc:
    - Độ dài từ 1 đến MAX_NICKNAME_LENGTH ký tự
    - Chỉ chứa chữ cái, số, dấu gạch dưới và dấu gạch ngang
    - Không bắt đầu hoặc kết thúc bằng ký tự đặc biệt
    """
    if not nickname:
        return False, "Nickname không được để trống"
    
    if len(nickname) > MAX_NICKNAME_LENGTH:
        return False, f"Nickname không được vượt quá {MAX_NICKNAME_LENGTH} ký tự"
    
    if len(nickname) < 1:
        return False, "Nickname phải có ít nhất 1 ký tự"
    
    # Kiểm tra ký tự hợp lệ (chữ cái, số, _, -)
    if not re.match(r'^[a-zA-Z0-9_-]+$', nickname):
        return False, "Nickname chỉ được chứa chữ cái, số, dấu gạch dưới (_) và dấu gạch ngang (-)"
    
    # Không được bắt đầu hoặc kết thúc bằng ký tự đặc biệt
    if nickname.startswith(('_', '-')) or nickname.endswith(('_', '-')):
        return False, "Nickname không được bắt đầu hoặc kết thúc bằng dấu gạch dưới hoặc gạch ngang"
    
    # Kiểm tra từ cấm
    forbidden_names = ['admin', 'server', 'system', 'bot', 'null', 'undefined']
    if nickname.lower() in forbidden_names:
        return False, f"Nickname '{nickname}' không được phép sử dụng"
    
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
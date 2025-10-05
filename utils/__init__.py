"""
Utility functions for chat client
Bao gồm validation, network utilities và connection helpers
"""

import socket
import re
import threading
from datetime import datetime

def validate_ip_address(ip):
    """Validate IP address format"""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def validate_port(port):
    """Validate port number"""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False

def validate_nickname(nickname):
    """Validate nickname format with enhanced rules"""
    if not nickname or len(nickname.strip()) == 0:
        return False, "Nickname không được để trống"
    
    # Get max length from config (fallback to 20)
    try:
        from config import get_max_nickname_length
        max_length = get_max_nickname_length()
    except:
        max_length = 20
    
    if len(nickname) > max_length:
        return False, f"Nickname không được dài quá {max_length} ký tự"
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', nickname):
        return False, "Nickname chỉ được chứa chữ, số, _ và -"
    
    return True, "Valid"

def get_local_ip():
    """Get local IP address for network scanning"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unable to determine"

def test_server_connection(host, port, timeout=2):
    """Test if a server is running at host:port"""
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(timeout)
        result = test_socket.connect_ex((host, port))
        test_socket.close()
        return result == 0
    except:
        return False

def scan_network_for_servers(port=12345, timeout=2):
    """
    Scan local network for chat servers
    Returns list of found server IPs
    """
    local_ip = get_local_ip()
    if local_ip == "Unable to determine":
        return []
    
    # Extract network prefix
    ip_parts = local_ip.split('.')
    network_prefix = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
    
    found_servers = []
    
    def check_host(ip):
        if test_server_connection(ip, port, timeout):
            found_servers.append(ip)
    
    # Priority IPs first
    priority_ips = [f"{network_prefix}.1", f"{network_prefix}.100", 
                   f"{network_prefix}.101", f"{network_prefix}.10"]
    
    threads = []
    for ip in priority_ips:
        if ip != local_ip:
            thread = threading.Thread(target=check_host, args=(ip,))
            threads.append(thread)
            thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    return found_servers

def format_timestamp():
    """Format current timestamp for messages"""
    return datetime.now().strftime("%H:%M:%S")

def safe_decode(data):
    """Safely decode bytes to string"""
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('utf-8', errors='ignore')

def safe_encode(text):
    """Safely encode string to bytes"""
    try:
        return text.encode('utf-8')
    except UnicodeEncodeError:
        return text.encode('utf-8', errors='ignore')

def format_connection_info(host, port, status="connecting"):
    """Format connection information for display"""
    if status == "connecting":
        return f"🔗 Connecting to {host}:{port}..."
    elif status == "connected":
        return f"✅ Connected to {host}:{port}"
    elif status == "failed":
        return f"❌ Failed to connect to {host}:{port}"
    else:
        return f"{host}:{port}"

# ============================================
# CONTENT MODERATION & VALIDATION
# ============================================

# Danh sách từ khóa không phù hợp (có thể mở rộng)
INAPPROPRIATE_WORDS = [
    # Từ ngữ thô tục tiếng Việt
    'đ*m', 'đmm', 'dm', 'vcl', 'vl', 'cc', 'cl', 'đcm', 'dcm',
    'dit', 'đit', 'loz', 'lồn', 'buồi', 'cặc', 'đéo', 'deo',
    'cmn', 'cmm', 'fuck', 'shit', 'damn', 'bitch', 'ass',
    # Spam patterns
    'aaaa', 'hhhh', 'yyyy', '!!!!', '????', '###',
    # Hate speech keywords
    'thù địch', 'ghét bỏ', 'phân biệt', 'kỳ thị'
]

# Từ khóa spam (lặp lại ký tự)
SPAM_PATTERNS = [
    r'(.)\1{4,}',  # Lặp lại 1 ký tự >= 5 lần: aaaaaaa
    r'[!?]{3,}',   # Nhiều dấu hỏi chấm: !!!!, ????
    r'[A-Z]{10,}', # Chữ hoa liên tục >= 10 ký tự
    r'^[^a-zA-ZÀ-ỹ]*$',  # Chỉ toàn ký tự đặc biệt
]

def validate_message_content(message):
    """
    Validate và filter nội dung tin nhắn
    
    Args:
        message (str): Tin nhắn cần kiểm tra
        
    Returns:
        tuple: (is_valid, filtered_message, reason)
               - is_valid: True nếu tin nhắn hợp lệ
               - filtered_message: Tin nhắn sau khi filter (nếu có)
               - reason: Lý do từ chối (nếu không hợp lệ)
    """
    if not message or not message.strip():
        return False, "", "Tin nhắn không được để trống"
    
    message = message.strip()
    
    # 1. Kiểm tra độ dài tin nhắn
    try:
        from config import get_max_message_length
        max_length = get_max_message_length()
    except:
        max_length = 500  # Default max length
        
    if len(message) > max_length:
        return False, "", f"Tin nhắn không được dài quá {max_length} ký tự"
    
    # 2. Kiểm tra tin nhắn quá ngắn (chỉ 1-2 ký tự)
    if len(message.replace(' ', '')) < 2:
        return False, "", "Tin nhắn quá ngắn, vui lòng nhập ít nhất 2 ký tự có nghĩa"
    
    # 3. Kiểm tra spam patterns
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return False, "", "Tin nhắn có dấu hiệu spam (lặp lại ký tự, chữ hoa, ký tự đặc biệt)"
    
    # 4. Kiểm tra từ ngữ không phù hợp
    message_lower = message.lower()
    filtered_message = message
    found_inappropriate = []
    
    for word in INAPPROPRIATE_WORDS:
        if word.lower() in message_lower:
            found_inappropriate.append(word)
            # Thay thế bằng dấu sao
            filtered_message = re.sub(re.escape(word), '*' * len(word), 
                                    filtered_message, flags=re.IGNORECASE)
    
    # 5. Nếu có quá nhiều từ không phù hợp, từ chối
    if len(found_inappropriate) >= 3:
        return False, "", f"Tin nhắn chứa quá nhiều từ ngữ không phù hợp: {', '.join(found_inappropriate)}"
    
    # 6. Nếu có từ không phù hợp nhưng không quá nhiều, cảnh báo
    if found_inappropriate:
        return True, filtered_message, f"Cảnh báo: Đã lọc từ không phù hợp: {', '.join(found_inappropriate)}"
    
    # 7. Tin nhắn hợp lệ
    return True, message, "OK"

def validate_message_frequency(last_message_times, max_messages=5, time_window=30):
    """
    Kiểm tra tần suất gửi tin nhắn để tránh spam
    
    Args:
        last_message_times (list): Danh sách timestamp các tin nhắn gần đây
        max_messages (int): Số tin nhắn tối đa trong time_window
        time_window (int): Cửa sổ thời gian (giây)
        
    Returns:
        tuple: (is_allowed, reason)
    """
    from datetime import datetime, timedelta
    
    now = datetime.now()
    # Lọc tin nhắn trong time_window giây gần đây
    recent_messages = [t for t in last_message_times 
                      if (now - t).total_seconds() <= time_window]
    
    if len(recent_messages) >= max_messages:
        wait_time = time_window - (now - recent_messages[0]).total_seconds()
        return False, f"Gửi tin nhắn quá nhanh. Vui lòng chờ {int(wait_time)} giây"
    
    return True, "OK"

def clean_message_display(message):
    """
    Làm sạch tin nhắn để hiển thị an toàn
    
    Args:
        message (str): Tin nhắn gốc
        
    Returns:
        str: Tin nhắn đã được làm sạch
    """
    if not message:
        return ""
    
    # Xóa các ký tự điều khiển
    message = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', message)
    
    # Giới hạn độ dài hiển thị
    if len(message) > 200:
        message = message[:197] + "..."
    
    # Xóa khoảng trắng thừa
    message = ' '.join(message.split())
    
    return message

def get_message_statistics(message):
    """
    Thống kê thông tin tin nhắn
    
    Args:
        message (str): Tin nhắn
        
    Returns:
        dict: Thống kê tin nhắn
    """
    if not message:
        return {
            'length': 0,
            'word_count': 0,
            'has_special_chars': False,
            'has_uppercase': False,
            'has_numbers': False
        }
    
    return {
        'length': len(message),
        'word_count': len(message.split()),
        'has_special_chars': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', message)),
        'has_uppercase': bool(re.search(r'[A-Z]', message)),
        'has_numbers': bool(re.search(r'\d', message)),
        'char_repeat_count': len(re.findall(r'(.)\1{2,}', message))
    }
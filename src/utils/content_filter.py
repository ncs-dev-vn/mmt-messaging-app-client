"""
Content filtering and moderation utilities
"""

import re
from utils.validators import validate_message_length  # Thay đổi từ .validators

# Danh sách từ cấm cơ bản (có thể mở rộng)
PROFANITY_LIST = [
    # Basic profanity
    'spam', 'fuck', 'shit', 'damn', 'bitch', 'ass',
    # Vietnamese profanity (mild examples)
    'đéo', 'dmm', 'vcl', 'clmm', 'đm', 'vl'
]

# Pattern cho các loại content không mong muốn
SPAM_PATTERNS = [
    r'(.)\1{10,}',  # Lặp lại ký tự > 10 lần
    r'[A-Z]{20,}',  # Chữ in hoa liên tiếp > 20 ký tự
    r'(http|https|www\.)',  # Links
    r'(\d+[\s-]*){10,}',  # Nhiều số liên tiếp
]

def filter_profanity(text):
    """Lọc từ ngữ không phù hợp"""
    filtered_text = text
    found_profanity = []
    
    for word in PROFANITY_LIST:
        if word.lower() in text.lower():
            # Thay thế bằng dấu *
            filtered_text = re.sub(re.escape(word), '*' * len(word), filtered_text, flags=re.IGNORECASE)
            found_profanity.append(word)
    
    return filtered_text, found_profanity

def detect_spam(text):
    """Phát hiện spam patterns"""
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text):
            return True, f"Phát hiện spam pattern"
    return False, "OK"

def validate_message_content(message):
    """
    Validate và filter nội dung tin nhắn
    
    Returns:
        tuple: (is_valid, filtered_message, reason)
    """
    # Kiểm tra độ dài
    length_valid, length_msg = validate_message_length(message)
    if not length_valid:
        return False, message, length_msg
    
    # Kiểm tra spam
    is_spam, spam_reason = detect_spam(message)
    if is_spam:
        return False, message, f"Tin nhắn bị từ chối: {spam_reason}"
    
    # Filter profanity
    filtered_message, found_profanity = filter_profanity(message)
    
    if found_profanity:
        warning = f"Cảnh báo: Đã lọc {len(found_profanity)} từ không phù hợp"
        return True, filtered_message, warning
    
    return True, filtered_message, "OK"

def is_command(message):
    """Kiểm tra xem tin nhắn có phải là command không"""
    return message.strip().startswith('/')

def parse_command(message):
    """Parse command từ tin nhắn"""
    if not is_command(message):
        return None, []
    
    parts = message.strip().split()
    command = parts[0][1:]  # Bỏ dấu /
    args = parts[1:] if len(parts) > 1 else []
    
    return command.lower(), args
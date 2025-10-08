"""
Utility functions for chat client
Bao gồm validation, network utilities và connection helpers
"""

import re

def validate_nickname(nickname):
    """Validate nickname format with enhanced rules"""
    if not nickname or len(nickname.strip()) == 0:
        return False, "Nickname không được để trống"
    
    # Tự động trim spaces và whitespace
    nickname = nickname.strip()
    
    # Kiểm tra độ dài tối thiểu (ít nhất 2 ký tự)
    if len(nickname) < 2:
        return False, "Nickname phải có ít nhất 2 ký tự"
    
    # Get max length from config (fallback to 20)
    try:
        from config import get_max_nickname_length
        max_length = get_max_nickname_length()
    except:
        max_length = 20
    
    if len(nickname) > max_length:
        return False, f"Nickname không được dài quá {max_length} ký tự"
    
    # Kiểm tra pattern - chỉ cho phép: chữ cái (a-z, A-Z), số (0-9), gạch dưới (_), gạch ngang (-)
    if not re.match(r'^[a-zA-Z0-9_-]+$', nickname):
        return False, "Nickname chỉ được chứa chữ cái (a-z, A-Z), số (0-9), gạch dưới (_) và gạch ngang (-)"
    
    return True, "Valid"



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


"""
Message formatters cho các loại tin nhắn khác nhau
"""

from datetime import datetime
from ui.colors import Colors  # Thay đổi từ .colors thành ui.colors

class MessageFormatter:
    """Formatter cho các loại tin nhắn khác nhau"""
    
    @staticmethod
    def get_timestamp():
        """Lấy timestamp hiện tại"""
        return datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def format_own_message(nickname, message, timestamp=None):
        """Format tin nhắn của chính mình"""
        if not timestamp:
            timestamp = MessageFormatter.get_timestamp()
        if Colors.is_supported():
            return f"{Colors.CYAN}{Colors.BOLD}[{timestamp}] Bạn:{Colors.RESET} {Colors.WHITE}{message}{Colors.RESET}"
        else:
            return f"[{timestamp}] Bạn: {message}"
    
    @staticmethod
    def format_other_message(sender, message, timestamp=None):
        """Format tin nhắn của người khác"""
        if not timestamp:
            timestamp = MessageFormatter.get_timestamp()
        if Colors.is_supported():
            return f"{Colors.GREEN}[{timestamp}] {sender}:{Colors.RESET} {message}"
        else:
            return f"[{timestamp}] {sender}: {message}"
    
    @staticmethod
    def format_server_message(message, timestamp=None):
        """Format thông báo từ server"""
        if not timestamp:
            timestamp = MessageFormatter.get_timestamp()
            
        if not Colors.is_supported():
            return f"[{timestamp}] SERVER: {message}"
            
        if "[THÔNG BÁO]" in message:
            return f"{Colors.YELLOW}{Colors.BOLD}🔔 [{timestamp}] {message}{Colors.RESET}"
        elif "⏰" in message or "hàng chờ" in message:
            return f"{Colors.MAGENTA}⏰ [{timestamp}] {message}{Colors.RESET}"
        elif "✅" in message or "kết nối" in message:
            return f"{Colors.GREEN}{Colors.BOLD}✅ [{timestamp}] {message}{Colors.RESET}"
        else:
            return f"{Colors.GRAY}📢 [{timestamp}] {message}{Colors.RESET}"
    
    @staticmethod
    def format_error_message(message):
        """Format thông báo lỗi"""
        if Colors.is_supported():
            return f"{Colors.RED}❌ {message}{Colors.RESET}"
        else:
            return f"ERROR: {message}"
    
    @staticmethod
    def format_warning_message(message):
        """Format thông báo cảnh báo"""
        if Colors.is_supported():
            return f"{Colors.YELLOW}⚠️ {message}{Colors.RESET}"
        else:
            return f"WARNING: {message}"
    
    @staticmethod
    def format_success_message(message):
        """Format thông báo thành công"""
        if Colors.is_supported():
            return f"{Colors.GREEN}✅ {message}{Colors.RESET}"
        else:
            return f"SUCCESS: {message}"
    
    @staticmethod
    def format_info_message(message):
        """Format thông báo thông tin"""
        if Colors.is_supported():
            return f"{Colors.CYAN}ℹ️ {message}{Colors.RESET}"
        else:
            return f"INFO: {message}"
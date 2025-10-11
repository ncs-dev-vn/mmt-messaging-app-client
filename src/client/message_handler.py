"""
Message handling utilities
"""

import re
from ui.formatters import MessageFormatter  # Thay đổi từ ..ui.formatters

class MessageHandler:
    """Xử lý và phân loại các loại tin nhắn"""
    
    def __init__(self, client_nickname):
        self.client_nickname = client_nickname
    
    def parse_message(self, raw_message):
        """
        Phân tích và phân loại tin nhắn từ server
        
        Returns:
            tuple: (message_type, sender, content, metadata)
        """
        message = raw_message.strip()
        
        # Tin nhắn chat từ user (format: "nickname: message")
        if self._is_user_message(message):
            sender, content = self._parse_user_message(message)
            if sender != self.client_nickname:
                return "user_message", sender, content, {}
        
        # Thông báo server
        if self._is_server_message(message):
            return "server_message", "SERVER", message, self._parse_server_metadata(message)
        
        # System commands/responses
        if self._is_system_response(message):
            return "system_response", "SYSTEM", message, {}
        
        # Default: treat as server message
        return "server_message", "SERVER", message, {}
    
    def _is_user_message(self, message):
        """Kiểm tra có phải tin nhắn chat từ user không"""
        return (": " in message and 
                not message.startswith("[") and 
                not message.startswith("🔔") and 
                not message.startswith("⏰") and
                not message.startswith("📢"))
    
    def _parse_user_message(self, message):
        """Parse tin nhắn user thành sender và content"""
        parts = message.split(": ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return "Unknown", message
    
    def _is_server_message(self, message):
        """Kiểm tra có phải thông báo server không"""
        server_indicators = [
            "[THÔNG BÁO]", "⏰", "✅", "❌", "🔔", 
            "Phòng chat", "hàng chờ", "kết nối", "Server:", "📢"
        ]
        return any(indicator in message for indicator in server_indicators)
    
    def _is_system_response(self, message):
        """Kiểm tra có phải system response không"""
        system_responses = [
            "NICKNAME_ACCEPTED", "NICKNAME_TAKEN", "NICKNAME_REJECTED",
            "ROOM_ENTERED", "ROOM_FULL", "QUEUE_POSITION"
        ]
        return any(response in message for response in system_responses)
    
    def _parse_server_metadata(self, message):
        """Parse metadata từ server message"""
        metadata = {}
        
        # Parse queue position
        queue_match = re.search(r'Vị trí hàng chờ[:\s]*(\d+)', message)
        if queue_match:
            metadata['queue_position'] = int(queue_match.group(1))
        
        # Parse notification type
        if "[THÔNG BÁO]" in message:
            metadata['notification_type'] = 'announcement'
        elif "⏰" in message or "hàng chờ" in message:
            metadata['notification_type'] = 'queue'
        elif "✅" in message:
            metadata['notification_type'] = 'success'
        elif "❌" in message:
            metadata['notification_type'] = 'error'
        
        return metadata
    
    def format_message_for_display(self, message_type, sender, content, metadata=None):
        """Format tin nhắn để hiển thị"""
        if message_type == "user_message":
            return MessageFormatter.format_other_message(sender, content)
        elif message_type == "server_message":
            return MessageFormatter.format_server_message(content)
        elif message_type == "system_response":
            # System responses thường không hiển thị trực tiếp
            return None
        else:
            return MessageFormatter.format_server_message(content)
    
    def should_update_queue_status(self, message_type, content, metadata):
        """Kiểm tra có nên update queue status không"""
        if message_type == "server_message":
            return ("hàng chờ" in content or 
                    "kết nối với chat" in content or
                    metadata.get('notification_type') == 'queue')
        return False
    
    def extract_queue_status(self, content, metadata):
        """Extract queue status từ message"""
        if "hiện đã kết nối với chat" in content:
            return False, 0  # Not in queue, position 0
        elif "hàng chờ" in content and "kết nối với chat" not in content:
            position = metadata.get('queue_position', 1)
            return True, position  # In queue, with position
        return None, None  # No change
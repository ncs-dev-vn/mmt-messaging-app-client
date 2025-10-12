"""
Simplified Message Formatters - Only 5 color categories
"""

from datetime import datetime
from ui.colors import blue, green, yellow, red, orange, bold

class MessageFormatter:
    """Simplified message formatter with 5 colors only"""
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp"""
        return datetime.now().strftime("[%H:%M:%S]")
    
    # === YOUR MESSAGES (BLUE) ===
    @staticmethod  
    def format_own_message(nickname, message):
        """Your messages - BLUE"""
        timestamp = MessageFormatter.get_timestamp()
        return blue(f"{timestamp} Bạn: {message}")
    
    # === OTHER USERS (GREEN) ===
    @staticmethod
    def format_other_message(sender, message):
        """Other users' messages - GREEN"""
        timestamp = MessageFormatter.get_timestamp()
        return green(f"{timestamp} {sender}: {message}")
    
    # === SERVER MESSAGES (YELLOW) ===
    @staticmethod
    def format_server_message(message):
        """Server notifications - YELLOW"""
        timestamp = MessageFormatter.get_timestamp()
        return yellow(f"{timestamp} [SERVER] {message}")
    
    @staticmethod
    def format_info_message(message):
        """Info messages - YELLOW"""
        return yellow(f"ℹ️  {message}")
    
    @staticmethod
    def format_success_message(message):
        """Success messages - YELLOW"""
        return yellow(f"✅ {message}")
    
    # === WARNINGS (ORANGE) ===
    @staticmethod
    def format_warning_message(message):
        """Warning messages - ORANGE"""
        return orange(f"⚠️  {message}")
    
    # === ERRORS/REJECTED (RED) ===
    @staticmethod
    def format_error_message(message):
        """Error messages - RED"""
        return red(f"❌ {message}")
    
    @staticmethod
    def format_rejected_message(message):
        """Rejected messages - RED"""
        return red(f"🚫 {message}")
    
    # === UNIFIED MESSAGE PROCESSING ===
    @staticmethod
    def format_message_by_type(msg_type, sender, content, is_own_message=False):
        """
        Unified message formatting based on type
        
        Args:
            msg_type: 'user', 'server', 'system', 'error', 'warning'
            sender: Username or system identifier
            content: Message content
            is_own_message: Whether this is user's own message
        """
        if msg_type == 'user':
            if is_own_message:
                return MessageFormatter.format_own_message(sender, content)
            else:
                return MessageFormatter.format_other_message(sender, content)
        
        elif msg_type == 'server' or msg_type == 'system':
            return MessageFormatter.format_server_message(content)
        
        elif msg_type == 'error' or msg_type == 'rejected':
            return MessageFormatter.format_error_message(content)
        
        elif msg_type == 'warning':
            return MessageFormatter.format_warning_message(content)
        
        else:
            # Fallback
            return MessageFormatter.format_server_message(f"{sender}: {content}")

# Backward compatibility - map old method names
MessageFormatter.format_notification_message = MessageFormatter.format_server_message
MessageFormatter.format_queue_message = MessageFormatter.format_server_message
MessageFormatter.format_system_message = MessageFormatter.format_server_message
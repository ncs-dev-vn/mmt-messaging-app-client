"""
Simplified UI Helpers
"""

from ui.colors import blue, green, yellow, red, orange, bold

class UIHelper:
    """UI helper functions with simplified colors"""
    
    @staticmethod
    def print_chat_guide():
        """Print simplified chat guide"""
        print(yellow("=" * 50))
        print(yellow("💬 HƯỚNG DẪN CHAT:"))
        print(f"  • {blue('Tin nhắn của bạn')}: Màu xanh dương")
        print(f"  • {green('Tin nhắn người khác')}: Màu xanh lá") 
        print(f"  • {yellow('Thông báo server')}: Màu vàng")
        print(f"  • {orange('Cảnh báo')}: Màu cam")
        print(f"  • {red('Lỗi/Từ chối')}: Màu đỏ")
        print(yellow("  • Gõ \"/help\" để xem các lệnh"))
        print(yellow("  • Gõ \"quit\" hoặc \"exit\" để thoát"))
        print(yellow("=" * 50))
    
    @staticmethod
    def print_help():
        """Print help with simplified colors"""
        print(yellow("\n📋 CÁC LỆNH HỖ TRỢ:"))
        print(f"  {bold('/help')}     - Hiển thị trợ giúp")
        print(f"  {bold('/debug')}    - Thông tin debug")
        print(f"  {bold('/nick')}     - Hiển thị nickname hiện tại")  
        print(f"  {bold('/setnick')}  - Đặt lại nickname")
        print(f"  {bold('quit/exit')} - Thoát khỏi chat")
        print()
    
    @staticmethod
    def get_colored_prompt():
        """Get simple colored prompt"""
        return blue("> ")
    
    @staticmethod  
    def print_connection_info(host, port):
        """Print connection info"""
        print(yellow(f"🌐 Kết nối: {host}:{port}"))
    
    @staticmethod
    def print_app_header():
        """Print simplified app header"""
        print(bold(yellow("=" * 30)))
        print(bold(yellow("💬 MULTI-USER CHAT CLIENT")))
        print(bold(yellow("=" * 30)))
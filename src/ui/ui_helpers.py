"""
UI Helper Functions
"""

from ui.colors import blue, green, yellow, orange, red, bold, clear_input_line

class UIHelper:
    """UI utility functions"""
    
    @staticmethod
    def print_app_header():
        print(bold(yellow("=" * 50)))
        print(bold(yellow("💬 MULTI-USER CHAT CLIENT")))
        print(bold(yellow("=" * 50)))
    
    @staticmethod
    def print_chat_guide():
        print(yellow("=" * 50))
        print(yellow("💬 HƯỚNG DẪN CHAT:"))
        print(f"  • {blue('Tin nhắn của bạn')}: Màu xanh dương")
        print(f"  • {green('Tin nhắn người khác')}: Màu xanh lá") 
        print(f"  • {yellow('Thông báo server')}: Màu vàng")
        print(f"  • {orange('Cảnh báo')}: Màu cam")
        print(f"  • {red('Lỗi')}: Màu đỏ")
        print("  • Gõ \"quit\" để thoát")
        print(yellow("=" * 50))
    
    @staticmethod
    def get_colored_prompt():
        return blue("> ")
    
    @staticmethod  
    def get_clean_input(prompt_text=""):
        """
        Get user input và clear input line sau khi nhấn Enter
        
        Args:
            prompt_text: Custom prompt text (optional)
            
        Returns:
            User input string
        """
        if prompt_text:
            user_input = input(prompt_text)
        else:
            user_input = input(UIHelper.get_colored_prompt())
        
        # Clear the input line after user presses Enter
        clear_input_line()
        
        return user_input
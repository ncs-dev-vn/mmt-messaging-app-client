"""
UI Helper functions
"""

from ui.colors import Colors  # Thay đổi từ .colors thành ui.colors

class UIHelper:
    """Helper functions cho giao diện người dùng"""
    
    @staticmethod
    def print_separator(length=60, char="=", color=None):
        """In đường phân cách"""
        separator = char * length
        if color and Colors.is_supported():
            print(f"{color}{separator}{Colors.RESET}")
        else:
            print(separator)
    
    @staticmethod
    def print_header(title, length=60):
        """In header với title"""
        if Colors.is_supported():
            UIHelper.print_separator(length, "=", Colors.CYAN + Colors.BOLD)
            print(f"{Colors.CYAN}{Colors.BOLD}{title.center(length)}{Colors.RESET}")
            UIHelper.print_separator(length, "=", Colors.CYAN + Colors.BOLD)
        else:
            UIHelper.print_separator(length)
            print(title.center(length))
            UIHelper.print_separator(length)
    
    @staticmethod
    def print_help():
        """In thông tin trợ giúp"""
        if Colors.is_supported():
            print(f"\n{Colors.YELLOW}{Colors.BOLD}📖 TRỢ GIÚP:{Colors.RESET}")
            print(f"{Colors.GRAY}  /help     - Hiển thị trợ giúp{Colors.RESET}")
            print(f"{Colors.GRAY}  /debug    - Hiển thị thông tin debug{Colors.RESET}")
            print(f"{Colors.GRAY}  /nick     - Hiển thị nickname hiện tại{Colors.RESET}")
            print(f"{Colors.GRAY}  quit/exit - Thoát khỏi chat{Colors.RESET}")
            print(f"{Colors.YELLOW}{'─' * 40}{Colors.RESET}")
        else:
            print("\nTRỢ GIÚP:")
            print("  /help     - Hiển thị trợ giúp")
            print("  /debug    - Hiển thị thông tin debug")
            print("  /nick     - Hiển thị nickname hiện tại")
            print("  quit/exit - Thoát khỏi chat")
            print("─" * 40)
    
    @staticmethod
    def print_chat_guide():
        """In hướng dẫn chat"""
        if Colors.is_supported():
            UIHelper.print_separator(60, "=", Colors.CYAN + Colors.BOLD)
            print(f'{Colors.CYAN}{Colors.BOLD}💬 HƯỚNG DẪN CHAT:{Colors.RESET}')
            print(f'{Colors.GRAY}  • Tin nhắn của bạn: {Colors.CYAN}{Colors.BOLD}Màu xanh dương đậm{Colors.RESET}')
            print(f'{Colors.GRAY}  • Tin nhắn người khác: {Colors.GREEN}Màu xanh lá{Colors.RESET}')
            print(f'{Colors.GRAY}  • Thông báo server: {Colors.YELLOW}Màu vàng{Colors.RESET}')
            print(f'{Colors.GRAY}  • Gõ "/help" để xem các lệnh{Colors.RESET}')
            print(f'{Colors.GRAY}  • Gõ "quit" hoặc "exit" để thoát{Colors.RESET}')
            UIHelper.print_separator(60, "=", Colors.CYAN + Colors.BOLD)
        else:
            UIHelper.print_separator(60)
            print('💬 HƯỚNG DẪN CHAT:')
            print('  • Tin nhắn của bạn: Có prefix "Bạn:"')
            print('  • Tin nhắn người khác: Có tên người gửi')
            print('  • Thông báo server: Có prefix "SERVER:"')
            print('  • Gõ "/help" để xem các lệnh')
            print('  • Gõ "quit" hoặc "exit" để thoát')
            UIHelper.print_separator(60)
    
    @staticmethod
    def get_colored_prompt():
        """Trả về prompt có màu"""
        if Colors.is_supported():
            return f"{Colors.CYAN}> {Colors.RESET}"
        else:
            return "> "
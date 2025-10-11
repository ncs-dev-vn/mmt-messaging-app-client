"""
ANSI Color codes cho terminal
"""

import os
import sys

class Colors:
    """ANSI color codes cho terminal"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Background colors
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    
    @staticmethod
    def is_supported():
        """Kiểm tra xem terminal có hỗ trợ màu không"""
        return (os.getenv('TERM') != 'dumb' and 
                hasattr(sys.stdout, 'isatty') and 
                sys.stdout.isatty())

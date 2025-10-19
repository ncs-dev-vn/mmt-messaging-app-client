"""
Simplified ANSI Colors for Chat Client
Only 5 main colors to reduce visual clutter
"""

import sys
import os

def supports_color():
    """Check if terminal supports ANSI colors"""
    return (
        hasattr(sys.stderr, "isatty") and sys.stderr.isatty() and
        os.environ.get('TERM') != 'dumb'
    )

class Colors:
    """Simplified color palette"""
    
    if supports_color():
        # Main colors only
        BLUE = '\033[34m'        # Your messages (người gửi)
        GREEN = '\033[32m'       # Other users (người nhận)  
        YELLOW = '\033[33m'      # Server messages
        RED = '\033[31m'         # Errors/Rejected (từ chối)
        ORANGE = '\033[93m'      # Warnings (cảnh báo)
        
        # === TERMINAL CONTROL CODES ===
        CURSOR_UP = '\033[1A'        # Move cursor up 1 line
        CLEAR_LINE = '\033[K'        # Clear from cursor to end of line
        CLEAR_ENTIRE_LINE = '\033[2K' # Clear entire line
        CURSOR_TO_START = '\033[G'    # Move cursor to start of line
        
        RESET = '\033[0m'
        BOLD = '\033[1m'
    else:
        # No color support
        BLUE = GREEN = YELLOW = RED = ORANGE = ''
        RESET = BOLD = ''
        CURSOR_UP = CLEAR_LINE = CLEAR_ENTIRE_LINE = CURSOR_TO_START = ''

# Color functions - simplified
def blue(text):
    """Your messages - Blue"""
    return f"{Colors.BLUE}{text}{Colors.RESET}"

def green(text):
    """Other users - Green"""
    return f"{Colors.GREEN}{text}{Colors.RESET}"

def yellow(text):
    """Server messages - Yellow"""
    return f"{Colors.YELLOW}{text}{Colors.RESET}"

def red(text):
    """Errors/Rejected - Red"""
    return f"{Colors.RED}{text}{Colors.RESET}"

def orange(text):
    """Warnings - Orange"""
    return f"{Colors.ORANGE}{text}{Colors.RESET}"

def bold(text):
    """Bold text"""
    return f"{Colors.BOLD}{text}{Colors.RESET}"

# Legacy support - map old functions to new simplified ones
def cyan(text): return yellow(text)     # Server messages
def magenta(text): return yellow(text)  # Server messages
def white(text): return text            # Plain text
def gray(text): return text             # Plain text
def light_blue(text): return blue(text) # Your messages
def light_green(text): return green(text) # Other messages

# === TERMINAL CONTROL FUNCTIONS ===

def clear_input_line():
    """Clear the line where user just typed input"""
    if supports_color():
        # Move up one line, clear it completely, but don't move cursor back down
        print(f"{Colors.CURSOR_UP}{Colors.CLEAR_ENTIRE_LINE}", end='', flush=True)

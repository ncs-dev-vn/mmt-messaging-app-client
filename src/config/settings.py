"""
Configuration settings cho chat client
"""

from config.network_scanner import auto_discover_servers  # Thay đổi từ .network_scanner

# Default values
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 12345
DEFAULT_BUFFER_SIZE = 1024
DEFAULT_TIMEOUT = 30
MAX_NICKNAME_LENGTH = 20
MAX_MESSAGE_LENGTH = 500

def get_server_info_from_user():
    """Get server information from user input with auto-discovery option"""
    print("=== Cấu hình Server ===")
    print("1. Tự động quét mạng LAN")
    print("2. Nhập thủ công")
    
    while True:
        try:
            choice = input("Chọn phương thức (1/2) [mặc định: 2]: ").strip()
            if not choice or choice == '2':
                # Manual input
                break
            elif choice == '1':
                # Auto-discovery
                result = auto_discover_servers()
                if result:
                    return result
                # If auto-discovery fails or user cancels, fall back to manual
                print("\n🔄 Chuyển sang nhập thủ công...")
                break
            else:
                print("❌ Chọn 1 hoặc 2")
        except KeyboardInterrupt:
            print("\n🔄 Chuyển sang nhập thủ công...")
            break
    
    # Manual input
    print("\n--- Nhập thủ công ---")
    
    # Input host
    host_input = input(f"Nhập server host [mặc định: {DEFAULT_HOST}]: ").strip()
    host = host_input if host_input else DEFAULT_HOST
    
    # Input port with validation
    while True:
        port_input = input(f"Nhập server port [mặc định: {DEFAULT_PORT}]: ").strip()
        if not port_input:
            port = DEFAULT_PORT
            break
        try:
            port = int(port_input)
            if 1 <= port <= 65535:
                break
            else:
                print("❌ Port phải từ 1-65535")
        except ValueError:
            print("❌ Port phải là số")
    
    print(f"✅ Sẽ kết nối tới {host}:{port}")
    return host, port

def get_default_server_info():
    """Get default server information"""
    return DEFAULT_HOST, DEFAULT_PORT

def get_connection_timeout():
    """Get connection timeout"""
    return DEFAULT_TIMEOUT

def get_buffer_size():
    """Get buffer size"""
    return DEFAULT_BUFFER_SIZE

def get_max_nickname_length():
    """Get max nickname length"""
    return MAX_NICKNAME_LENGTH

def get_max_message_length():
    """Get maximum message length"""
    return MAX_MESSAGE_LENGTH
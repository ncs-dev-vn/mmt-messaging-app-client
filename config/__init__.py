"""
Configuration utilities for chat client
Cung cấp cấu hình linh hoạt với auto-detection và environment variables
"""

import configparser
import os

def load_config():
    """Load configuration from config file"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'client_config.ini')
    
    if os.path.exists(config_path):
        config.read(config_path)
    
    return config

def get_default_server_info():
    """Get default server information with environment variable support"""
    config = load_config()
    
    try:
        # Lấy từ config trước
        host = config.get('server', 'default_host', fallback='127.0.0.1')
        port = config.getint('server', 'default_port', fallback=12345)
        
        # Kiểm tra environment variables (ưu tiên cao nhất)
        env_host = os.getenv('CHAT_SERVER_HOST')
        if env_host:
            host = env_host
            
        env_port = os.getenv('CHAT_SERVER_PORT')
        if env_port:
            try:
                port = int(env_port)
            except ValueError:
                pass  # Giữ port từ config nếu env không hợp lệ
            
        return host, port
    except:
        return '127.0.0.1', 12345

def get_connection_timeout():
    """Get connection timeout from config"""
    config = load_config()
    return config.getint('server', 'timeout', fallback=30)

def get_buffer_size():
    """Get buffer size from config"""
    config = load_config()
    return config.getint('client', 'buffer_size', fallback=1024)

def get_max_nickname_length():
    """Get max nickname length from config"""
    config = load_config()
    return config.getint('client', 'max_nickname_length', fallback=20)

def get_max_message_length():
    """Get maximum message length from config"""
    config = load_config()
    return config.getint('client', 'max_message_length', fallback=500)
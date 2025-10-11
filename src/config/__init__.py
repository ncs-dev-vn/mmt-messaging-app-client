"""
Configuration Package
"""

from config.settings import (
    get_server_info_from_user,
    get_default_server_info,
    get_connection_timeout,
    get_buffer_size,
    get_max_nickname_length,
    get_max_message_length,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_BUFFER_SIZE,
    DEFAULT_TIMEOUT,
    MAX_NICKNAME_LENGTH,
    MAX_MESSAGE_LENGTH
)
from config.network_scanner import auto_discover_servers, scan_network_for_servers

__all__ = [
    'get_server_info_from_user',
    'get_default_server_info', 
    'get_connection_timeout',
    'get_buffer_size',
    'get_max_nickname_length',
    'get_max_message_length',
    'auto_discover_servers',
    'scan_network_for_servers',
    'DEFAULT_HOST',
    'DEFAULT_PORT',
    'DEFAULT_BUFFER_SIZE',
    'DEFAULT_TIMEOUT',
    'MAX_NICKNAME_LENGTH',
    'MAX_MESSAGE_LENGTH'
]
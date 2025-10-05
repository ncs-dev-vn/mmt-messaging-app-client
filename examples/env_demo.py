#!/usr/bin/env python3
"""
Demo Environment Variables Support
Minh họa cách sử dụng environment variables với chat client
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import get_default_server_info

def demo_environment_variables():
    """Demo các scenario sử dụng environment variables"""
    
    print("🌍 Environment Variables Demo")
    print("=" * 50)
    
    # 1. Default configuration
    print("\n1. 📋 Default Configuration (from config file):")
    host, port = get_default_server_info()
    print(f"   Host: {host}, Port: {port}")
    
    # 2. Override với CHAT_SERVER_HOST
    print("\n2. 🌍 Override with CHAT_SERVER_HOST:")
    os.environ['CHAT_SERVER_HOST'] = '192.168.1.100'
    host, port = get_default_server_info()
    print(f"   Host: {host}, Port: {port}")
    
    # 3. Override cả HOST và PORT  
    print("\n3. 🌍 Override with CHAT_SERVER_HOST + CHAT_SERVER_PORT:")
    os.environ['CHAT_SERVER_HOST'] = '10.0.0.50'
    os.environ['CHAT_SERVER_PORT'] = '8080'
    host, port = get_default_server_info()
    print(f"   Host: {host}, Port: {port}")
    
    # 4. Invalid port handling
    print("\n4. ❌ Invalid PORT handling:")
    os.environ['CHAT_SERVER_PORT'] = 'invalid_port'
    host, port = get_default_server_info()
    print(f"   Host: {host}, Port: {port} (fallback to config)")
    
    # Cleanup
    if 'CHAT_SERVER_HOST' in os.environ:
        del os.environ['CHAT_SERVER_HOST']
    if 'CHAT_SERVER_PORT' in os.environ:
        del os.environ['CHAT_SERVER_PORT']
    
    print("\n✅ Demo completed!")
    print("\n💡 Usage Examples:")
    print("   export CHAT_SERVER_HOST=192.168.1.100")
    print("   export CHAT_SERVER_PORT=8080")
    print("   python3 client.py")

if __name__ == "__main__":
    demo_environment_variables()
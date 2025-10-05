#!/usr/bin/env python3
"""
Simple Content Moderation Test Client
Chỉ test content moderation mà không cần server thật
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import validate_message_content, validate_message_frequency
from config import is_content_filter_enabled, get_message_rate_limits

class MockChatClient:
    """Mock client để test content moderation"""
    
    def __init__(self):
        self.message_times = []
        self.warning_count = 0
        
    def send_message(self, message):
        """Test send message với content validation"""
        
        # 1. Basic validation
        if not message or not message.strip():
            print('❌ Không gửi tin nhắn rỗng.')
            return False
        
        # 2. Content filtering
        if is_content_filter_enabled():
            is_valid, filtered_message, reason = validate_message_content(message)
            
            if not is_valid:
                print(f'❌ Tin nhắn bị từ chối: {reason}')
                return False
                
            if reason != "OK" and "Cảnh báo" in reason:
                print(f'⚠️ {reason}')
                self.warning_count += 1
                if self.warning_count >= 3:
                    print('⚠️ Bạn đã nhận quá nhiều cảnh báo. Vui lòng chú ý ngôn từ.')
                message = filtered_message
        
        # 3. Rate limiting
        try:
            max_msgs, time_window = get_message_rate_limits()
            is_allowed, rate_reason = validate_message_frequency(
                self.message_times, max_msgs, time_window)
            
            if not is_allowed:
                print(f'❌ {rate_reason}')
                return False
        except:
            pass
        
        # 4. "Send" message (just print for demo)
        print(f'✅ Tin nhắn đã gửi: "{message}"')
        
        # 5. Track message time
        self.message_times.append(datetime.now())
        if len(self.message_times) > 10:
            self.message_times = self.message_times[-5:]
            
        return True

def main():
    """Interactive content moderation test"""
    
    print("🛡️ Content Moderation Test Client")
    print("=" * 50)
    print("Type messages to test content filtering")
    print("Commands: 'quit' to exit, 'stats' for statistics")
    print("=" * 50)
    
    client = MockChatClient()
    
    while True:
        try:
            message = input("\nYour message: ").strip()
            
            if message.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break
                
            elif message.lower() == 'stats':
                print(f"\n📊 Statistics:")
                print(f"- Messages sent: {len(client.message_times)}")
                print(f"- Warnings: {client.warning_count}")
                print(f"- Content filter: {'ON' if is_content_filter_enabled() else 'OFF'}")
                max_msgs, time_window = get_message_rate_limits()
                print(f"- Rate limit: {max_msgs} messages per {time_window}s")
                continue
                
            elif not message:
                print("⚠️ Please enter a message")
                continue
            
            # Test the message
            client.send_message(message)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
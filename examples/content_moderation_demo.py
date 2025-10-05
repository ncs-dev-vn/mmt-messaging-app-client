#!/usr/bin/env python3
"""
Demo Content Moderation Features
Minh họa tính năng lọc nội dung và spam prevention
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import (validate_message_content, validate_message_frequency, 
                  clean_message_display, get_message_statistics)
from config import (is_content_filter_enabled, get_message_rate_limits,
                   get_max_message_length)
from datetime import datetime, timedelta

def demo_content_moderation():
    """Demo các tính năng content moderation"""
    
    print("🛡️ Content Moderation Demo")
    print("=" * 50)
    
    # Test cases
    test_messages = [
        "Hello everyone!",                    # Normal message
        "",                                   # Empty message
        "a" * 600,                           # Too long
        "dm vcl cc",                         # Inappropriate words
        "aaaaaaaaaa",                        # Spam (repeated chars)
        "HELLO WORLD!!!!!!",                 # Caps + many punctuation
        "Nice to meet you 😊",               # Normal with emoji
        "What the f*** is this?",            # Mild profanity
        "Hi! How are you doing today?",      # Normal question
        "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",           # Emoji spam
    ]
    
    print("\n1. 📝 Message Content Validation:")
    print("-" * 30)
    
    for i, message in enumerate(test_messages, 1):
        display_msg = message[:50] + "..." if len(message) > 50 else message
        print(f"\n{i:2d}. Testing: '{display_msg}'")
        
        is_valid, filtered_msg, reason = validate_message_content(message)
        
        if is_valid:
            print(f"    ✅ Valid: {reason}")
            if filtered_msg != message:
                print(f"    🔧 Filtered: '{filtered_msg}'")
        else:
            print(f"    ❌ Rejected: {reason}")
    
    # Rate limiting demo
    print(f"\n\n2. ⏱️ Rate Limiting Demo:")
    print("-" * 30)
    
    # Simulate rapid messages
    message_times = []
    now = datetime.now()
    
    # Simulate 6 messages in 10 seconds
    for i in range(6):
        msg_time = now - timedelta(seconds=10-i)
        message_times.append(msg_time)
    
    print("Simulating 6 messages in 10 seconds...")
    
    max_msgs, time_window = get_message_rate_limits()
    print(f"Rate limit: {max_msgs} messages per {time_window} seconds")
    
    is_allowed, rate_reason = validate_message_frequency(message_times, max_msgs, time_window)
    
    if is_allowed:
        print("✅ Rate limit OK")
    else:
        print(f"❌ Rate limit exceeded: {rate_reason}")
    
    # Message statistics demo
    print(f"\n\n3. 📊 Message Statistics:")
    print("-" * 30)
    
    sample_messages = [
        "Hello world!",
        "URGENT: CHECK THIS OUT!!!",
        "Nice 😊 to meet you! How are you doing today? 123",
        "aaaaaa bbbbbb cccccc",
    ]
    
    for msg in sample_messages:
        stats = get_message_statistics(msg)
        print(f"\nMessage: '{msg}'")
        print(f"  Length: {stats['length']}")
        print(f"  Words: {stats['word_count']}")
        print(f"  Has uppercase: {stats['has_uppercase']}")
        print(f"  Has numbers: {stats['has_numbers']}")
        print(f"  Has special chars: {stats['has_special_chars']}")
        print(f"  Repeated chars: {stats['char_repeat_count']}")
    
    # Configuration demo
    print(f"\n\n4. ⚙️ Configuration Settings:")
    print("-" * 30)
    
    print(f"Content filter enabled: {is_content_filter_enabled()}")
    print(f"Max message length: {get_max_message_length()}")
    
    max_msgs, time_window = get_message_rate_limits()
    print(f"Rate limiting: {max_msgs} messages per {time_window}s")
    
    print(f"\n✅ Demo completed!")
    
    print(f"\n💡 Tips for users:")
    print("- Keep messages under 500 characters")
    print("- Avoid repeated characters (aaaa, !!!!, ????)")
    print("- Use appropriate language")
    print("- Don't send too many messages quickly")
    print("- Emojis are OK in moderation")

if __name__ == "__main__":
    demo_content_moderation()
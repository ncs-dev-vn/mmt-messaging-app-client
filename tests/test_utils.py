"""
Unit tests for utility functions với tính năng mới
"""

import unittest
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import (validate_ip_address, validate_port, validate_nickname, 
                  test_server_connection, scan_network_for_servers, 
                  format_connection_info, get_local_ip)

class TestUtils(unittest.TestCase):
    
    def test_validate_ip_address(self):
        """Test IP address validation"""
        # Valid IPs
        self.assertTrue(validate_ip_address('127.0.0.1'))
        self.assertTrue(validate_ip_address('192.168.1.100'))
        self.assertTrue(validate_ip_address('0.0.0.0'))
        
        # Invalid IPs
        self.assertFalse(validate_ip_address('256.1.1.1'))
        self.assertFalse(validate_ip_address('192.168.1'))
        self.assertFalse(validate_ip_address('invalid'))
    
    def test_validate_port(self):
        """Test port validation"""
        # Valid ports
        self.assertTrue(validate_port('80'))
        self.assertTrue(validate_port('12345'))
        self.assertTrue(validate_port('65535'))
        
        # Invalid ports
        self.assertFalse(validate_port('0'))
        self.assertFalse(validate_port('65536'))
        self.assertFalse(validate_port('abc'))
    
    def test_validate_nickname(self):
        """Test nickname validation với enhanced rules"""
        # Valid nicknames
        valid, _ = validate_nickname('Alice')
        self.assertTrue(valid)
        
        valid, _ = validate_nickname('user123')
        self.assertTrue(valid)
        
        valid, _ = validate_nickname('test_user')
        self.assertTrue(valid)
        
        # Invalid nicknames
        valid, _ = validate_nickname('')
        self.assertFalse(valid)
        
        valid, _ = validate_nickname('a' * 25)  # Too long
        self.assertFalse(valid)
        
        valid, _ = validate_nickname('user@name')  # Invalid char
        self.assertFalse(valid)
    
    def test_test_server_connection(self):
        """Test server connection testing"""
        # Test invalid connection (should be false)
        result = test_server_connection('192.168.999.999', 12345, timeout=1)
        self.assertFalse(result)
        
        # Test with short timeout
        result = test_server_connection('1.1.1.1', 12345, timeout=1)
        self.assertFalse(result)
    
    def test_get_local_ip(self):
        """Test local IP detection"""
        ip = get_local_ip()
        self.assertIsInstance(ip, str)
        # Should be valid IP or error message
        self.assertTrue(validate_ip_address(ip) or ip == "Unable to determine")
    
    def test_scan_network_for_servers(self):
        """Test network scanning (should not crash)"""
        try:
            servers = scan_network_for_servers(port=12345, timeout=1)
            self.assertIsInstance(servers, list)
        except Exception as e:
            self.fail(f"Network scan failed: {e}")
    
    def test_format_connection_info(self):
        """Test connection info formatting"""
        info = format_connection_info('127.0.0.1', 12345, 'connecting')
        self.assertIn('127.0.0.1:12345', info)
        self.assertIn('🔗', info)
        
        info = format_connection_info('127.0.0.1', 12345, 'connected')
        self.assertIn('✅', info)
        
        info = format_connection_info('127.0.0.1', 12345, 'failed')
        self.assertIn('❌', info)

if __name__ == '__main__':
    unittest.main()
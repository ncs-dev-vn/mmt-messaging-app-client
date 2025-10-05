"""
Unit tests for ChatClient với tính năng mới
"""

import unittest
import sys
import os
import socket

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chat_client import ChatClient, _scan_for_servers

class TestChatClient(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = ChatClient()
    
    def test_client_initialization_default(self):
        """Test client initialization with default smart detection"""
        # Client sẽ tự động detect host
        self.assertEqual(self.client.port, 12345)
        self.assertEqual(self.client.buffer_size, 1024)
        self.assertEqual(self.client.nickname, "")
        self.assertFalse(self.client.is_connected)
    
    def test_client_initialization_with_params(self):
        """Test client initialization with custom parameters"""
        client = ChatClient(host='192.168.1.100', port=8080, buffer_size=2048)
        self.assertEqual(client.host, '192.168.1.100')
        self.assertEqual(client.port, 8080)
        self.assertEqual(client.buffer_size, 2048)
    
    def test_get_default_host(self):
        """Test default host detection"""
        host = self.client._get_default_host()
        self.assertIsInstance(host, str)
        # Should be valid IP or localhost
        self.assertTrue(host in ['127.0.0.1'] or self._is_valid_ip(host))
    
    def test_test_connection(self):
        """Test connection testing functionality"""
        # Test invalid connection
        result = self.client._test_connection('192.168.999.999', 12345, timeout=1)
        self.assertFalse(result)
        
        # Test timeout functionality
        result = self.client._test_connection('1.1.1.1', 12345, timeout=1)
        self.assertFalse(result)  # Should timeout
    
    def _is_valid_ip(self, ip):
        """Helper method to validate IP format"""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    def test_disconnect_safety(self):
        """Test disconnect method doesn't crash when no connection"""
        # Should not crash even when not connected
        try:
            self.client.disconnect()
        except SystemExit:
            pass  # Expected behavior

class TestNetworkScanning(unittest.TestCase):
    
    def test_scan_for_servers_no_crash(self):
        """Test network scanning doesn't crash"""
        try:
            result = _scan_for_servers(timeout=1)
            self.assertIsInstance(result, (str, type(None)))
        except Exception as e:
            self.fail(f"Network scanning crashed: {e}")

if __name__ == '__main__':
    unittest.main()
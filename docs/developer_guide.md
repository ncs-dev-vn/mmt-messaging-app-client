# Developer Guide - Multi-User Chat Client

## Tổng quan Kiến trúc

### Cấu trúc Dự án

```
mmt-messaging-app-client/
├── client.py                 # Entry point
├── src/
│   └── chat_client.py       # Core ChatClient class
├── config/
│   ├── __init__.py         # Config utilities
│   └── client_config.ini   # Configuration file
├── utils/
│   └── __init__.py         # Validation & network utilities
├── tests/
│   └── test_client.py      # Unit tests
└── docs/
    ├── project_description.md
    ├── api_documentation.md
    ├── user_guide.md
    └── developer_guide.md
```

### Design Patterns

#### 1. Singleton Pattern cho Config
```python
# config/__init__.py
_config_cache = None

def load_config():
    global _config_cache
    if _config_cache is None:
        _config_cache = configparser.ConfigParser()
        # Load logic...
    return _config_cache
```

#### 2. Strategy Pattern cho Connection
```python
# Các chiến lược kết nối khác nhau
def connect_local()      # Strategy 1
def connect_remote()     # Strategy 2  
def connect_quick()      # Strategy 3
def connect_auto_scan()  # Strategy 4
```

#### 3. Observer Pattern cho Messages
```python
# Thread riêng để observe messages
def receive_messages(self):
    while self.running:
        message = self.socket.recv(self.buffer_size)
        self._notify_message_received(message)
```

## Core Components

### 1. ChatClient Class

**Responsibilities:**
- TCP socket management
- Multi-threaded message handling
- Connection lifecycle management
- Configuration integration

**Key Methods:**

```python
class ChatClient:
    def __init__(self):
        self.config = load_config()
        self.socket = None
        self.running = False
        
    def connect(self, host, port):
        """Establish TCP connection with validation"""
        
    def send_message(self, message):
        """Thread-safe message sending"""
        
    def receive_messages(self):
        """Background thread for receiving"""
        
    def disconnect(self):
        """Clean shutdown with resource cleanup"""
```

**Threading Model:**
- **Main Thread:** User input handling
- **Receiver Thread:** Background message reception
- **Connection Thread:** Non-blocking connection attempts

### 2. Configuration System

**File Structure:**
```ini
[server]
default_host = 127.0.0.1
default_port = 12345
timeout = 5

[client]  
buffer_size = 1024
max_nickname_length = 20

[network]
auto_scan_enabled = true
scan_timeout = 3
scan_range = 192.168.1.1-254

[ui]
show_timestamps = false
color_enabled = true
```

**Loading Hierarchy:**
1. Environment variables (`CHAT_SERVER_HOST`)
2. Configuration file (`client_config.ini`)
3. Hard-coded defaults

```python
def get_default_server_info():
    # 1. Check environment
    host = os.getenv('CHAT_SERVER_HOST')
    if host:
        return host, get_default_port()
    
    # 2. Check config file
    config = load_config()
    host = config.get('server', 'default_host', fallback='127.0.0.1')
    port = config.getint('server', 'default_port', fallback=12345)
    
    return host, port
```

### 3. Network Utilities

**Network Utilities:**
```python
def get_local_ip():
    """Get local IP for network scanning"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "Unable to determine"
```

**Connection Testing:**
```python
def test_server_connection(host, port, timeout=5):
    """Test if server is available"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False
```

## Development Setup

### 1. Environment Setup

```bash
# Clone repository
git clone https://github.com/ncs-dev-vn/mmt-messaging-app-client.git
cd mmt-messaging-app-client

# Setup Python environment (recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install development dependencies (if any)
# pip install -r requirements-dev.txt  # Future use
```

### 2. Development Tools

**IDE Setup (VS Code):**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

**Debugging Configuration:**
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Chat Client",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/client.py",
            "console": "integratedTerminal"
        }
    ]
}
```

### 3. Code Quality Tools

**Linting dengan Pylint:**
```bash
# Install pylint
pip install pylint

# Run linting
pylint src/chat_client.py
pylint config/
pylint utils/
```

**Type Hints (Future Enhancement):**
```python
from typing import Optional, Tuple, Dict, Any

def connect(self, host: str, port: int) -> bool:
    """Connect to chat server with type hints"""
    
def get_default_server_info() -> Tuple[str, int]:
    """Return server info with type annotations"""
```

## Testing Strategy

### 1. Unit Tests Structure

```python
# tests/test_client.py
import unittest
from unittest.mock import Mock, patch, MagicMock
from src.chat_client import ChatClient

class TestChatClient(unittest.TestCase):
    
    def setUp(self):
        """Setup for each test"""
        self.client = ChatClient()
        
    def tearDown(self):
        """Cleanup after each test"""
        if self.client.socket:
            self.client.disconnect()
            
    def test_connection_success(self):
        """Test successful connection"""
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.connect.return_value = None
            result = self.client.connect('127.0.0.1', 12345)
            self.assertTrue(result)
            
    def test_connection_failure(self):
        """Test connection failure handling"""
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.connect.side_effect = ConnectionRefusedError()
            result = self.client.connect('127.0.0.1', 12345)
            self.assertFalse(result)
```

### 2. Integration Tests

```python
def test_end_to_end_chat_flow(self):
    """Test complete chat session"""
    # 1. Connect to test server
    # 2. Send nickname
    # 3. Send/receive messages
    # 4. Disconnect gracefully
```

### 3. Network Tests

```python
def test_network_scanning(self):
    """Test auto-scan functionality"""
    with patch('utils.test_server_connection') as mock_test:
        mock_test.return_value = True
        result = test_server_connection('127.0.0.1', 12345)
        self.assertTrue(result)
```

### 4. Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_client.py::TestChatClient::test_connection_success

# Run with coverage
pip install pytest-cov
python -m pytest --cov=src tests/

# Run unittest (alternative)
python -m unittest tests/test_client.py
```

## Performance Optimization

### 1. Connection Optimization

```python
# Non-blocking connection with timeout
def connect_with_timeout(self, host, port, timeout=5):
    """Non-blocking connection with proper timeout"""
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(timeout)
    
    try:
        self.socket.connect((host, port))
        self.socket.settimeout(None)  # Reset to blocking
        return True
    except socket.timeout:
        self._handle_connection_timeout()
        return False
```

### 2. Memory Management

```python
def cleanup_resources(self):
    """Proper resource cleanup"""
    if hasattr(self, 'receiver_thread') and self.receiver_thread.is_alive():
        self.running = False
        self.receiver_thread.join(timeout=2)
        
    if self.socket:
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        finally:
            self.socket.close()
            self.socket = None
```

### 3. Network Scanning Optimization

```python
# Optimized scanning with early termination
def quick_scan_for_servers(self, max_results=1):
    """Fast scan that stops after finding first server"""
    import threading
    
    found_servers = []
    stop_event = threading.Event()
    
    def scan_ip(ip):
        if stop_event.is_set():
            return
        if test_server_connection(ip, self.port, timeout=0.5):
            found_servers.append(ip)
            if len(found_servers) >= max_results:
                stop_event.set()
```

## Error Handling & Logging

### 1. Error Hierarchy

```python
class ChatClientError(Exception):
    """Base exception for chat client"""
    pass

class ConnectionError(ChatClientError):
    """Connection related errors"""
    pass

class ValidationError(ChatClientError):
    """Input validation errors"""
    pass

class NetworkError(ChatClientError):
    """Network scanning/discovery errors"""
    pass
```

### 2. Logging Setup (Future Enhancement)

```python
import logging

def setup_logging(level=logging.INFO):
    """Setup application logging"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/chat_client.log'),
            logging.StreamHandler()
        ]
    )
    
logger = logging.getLogger(__name__)

# Usage in code
logger.info(f"Connecting to {host}:{port}")
logger.error(f"Connection failed: {error}")
logger.debug(f"Received message: {message}")
```

### 3. Graceful Error Recovery

```python
def robust_receive_messages(self):
    """Message receiver with error recovery"""
    retry_count = 0
    max_retries = 3
    
    while self.running and retry_count < max_retries:
        try:
            message = self.socket.recv(self.buffer_size)
            if not message:
                break
            self._process_message(message)
            retry_count = 0  # Reset on success
            
        except socket.timeout:
            continue  # Normal timeout, continue
        except ConnectionResetError:
            logger.warning("Server disconnected, attempting reconnect...")
            if self._attempt_reconnect():
                continue
            break
        except Exception as e:
            logger.error(f"Receive error: {e}")
            retry_count += 1
            time.sleep(0.5)  # Brief pause before retry
```

## Contributing Guidelines

### 1. Code Standards

**PEP 8 Compliance:**
```python
# Good
def connect_to_server(host: str, port: int) -> bool:
    """Connect to chat server with proper formatting."""
    if not host or not isinstance(port, int):
        raise ValidationError("Invalid host or port")
    return True

# Bad  
def connectToServer(host,port):
    if not host:raise ValidationError("Invalid host")
    return True
```

**Docstring Standards:**
```python
def test_server_connection(host, port, timeout=2):
    """
    Test if a server is running at host:port.
    
    Args:
        host (str): Server IP address or hostname
        port (int): Port number to test
        timeout (int): Connection timeout in seconds
        
    Returns:
        bool: True if server is available, False otherwise
        
    Example:
        >>> available = test_server_connection('127.0.0.1', 12345)
        >>> if available:
        ...     print("Server is running!")
    """
```

### 2. Git Workflow

```bash
# Feature development
git checkout -b feature/new-encryption
git add .
git commit -m "feat: add message encryption support"
git push origin feature/new-encryption

# Bug fixes
git checkout -b fix/connection-timeout
git add .
git commit -m "fix: handle connection timeout gracefully"
git push origin fix/connection-timeout
```

**Commit Message Convention:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Build/config changes

### 3. Pull Request Process

1. **Fork & Branch:** Create feature branch from main
2. **Develop:** Implement changes with tests
3. **Test:** Run full test suite
4. **Document:** Update relevant documentation
5. **Submit:** Create PR with clear description

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Future Enhancements

### 1. Security Features

```python
# Message encryption
import cryptography
from cryptography.fernet import Fernet

class SecureChatClient(ChatClient):
    def __init__(self):
        super().__init__()
        self.encryption_key = None
        
    def enable_encryption(self, key):
        """Enable message encryption"""
        self.cipher_suite = Fernet(key)
        
    def send_encrypted_message(self, message):
        """Send encrypted message"""
        encrypted = self.cipher_suite.encrypt(message.encode())
        self.send_message(encrypted)
```

### 2. GUI Development

```python
# tkinter GUI wrapper
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatGUI:
    def __init__(self):
        self.client = ChatClient()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup GUI components"""
        self.window = tk.Tk()
        self.window.title("Multi-User Chat Client")
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.window)
        
        # Message input
        self.message_entry = tk.Entry(self.window)
        self.send_button = tk.Button(self.window, text="Send", 
                                   command=self.send_message)
```

### 3. Protocol Extensions

```python
# JSON message protocol
import json

class AdvancedChatClient(ChatClient):
    def send_structured_message(self, message_type, content, metadata=None):
        """Send structured JSON message"""
        message = {
            'type': message_type,
            'content': content,
            'timestamp': time.time(),
            'metadata': metadata or {}
        }
        self.send_message(json.dumps(message))
        
    def handle_structured_message(self, raw_message):
        """Handle incoming JSON message"""
        try:
            message = json.loads(raw_message)
            message_type = message.get('type', 'text')
            
            if message_type == 'text':
                self._display_text_message(message)
            elif message_type == 'file':
                self._handle_file_transfer(message)
            elif message_type == 'system':
                self._handle_system_message(message)
                
        except json.JSONDecodeError:
            # Fallback to plain text
            self._display_plain_message(raw_message)
```

### 4. Advanced Features Roadmap

**Phase 1: Core Improvements**
- [ ] Message history/logging
- [ ] Reconnection handling
- [ ] Better error messages
- [ ] Configuration GUI

**Phase 2: Enhanced Features**  
- [ ] File transfer support
- [ ] Multiple chat rooms
- [ ] User presence indicators
- [ ] Message timestamps

**Phase 3: Advanced Features**
- [ ] End-to-end encryption
- [ ] Voice/video chat
- [ ] Plugin system
- [ ] Mobile app version

## Deployment

### 1. Packaging

```bash
# Create distribution package
python setup.py sdist bdist_wheel

# Install from source
pip install .

# Development install
pip install -e .
```

### 2. Docker Support (Future)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "client.py"]
```

### 3. Cross-Platform Build

```bash
# PyInstaller for executable
pip install pyinstaller

# Build standalone executable
pyinstaller --onefile --name chat-client client.py

# Build with config files included
pyinstaller --onefile --add-data "config:config" --name chat-client client.py
```

---

**Happy Coding! 🚀**
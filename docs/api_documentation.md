# API Documentation - Chat Client

## Overview

Chat Client là một ứng dụng Python để kết nối đến chat server và thực hiện các cuộc trò chuyện real-time. Client hỗ trợ tự động phát hiện server và có giao diện dòng lệnh thân thiện.

## Core Classes

### `ChatClient`

Lớp chính quản lý kết nối và giao tiếp với server.

```python
from src.chat_client import ChatClient

# Khởi tạo với auto-detection
client = ChatClient()

# Khởi tạo với thông tin cụ thể
client = ChatClient(host='192.168.1.100', port=8080, buffer_size=2048)
```

#### Constructor

```python
def __init__(self, host=None, port=None, buffer_size=None)
```

**Parameters:**
- `host` (str, optional): Server IP address. None để auto-detection
- `port` (int, optional): Server port. None để sử dụng config default  
- `buffer_size` (int, optional): Buffer size cho nhận tin nhắn. None để sử dụng config

#### Methods

##### Connection Methods

```python
def connect(self) -> bool
```
Kết nối đến server.
- **Returns:** True nếu thành công, False nếu thất bại

```python
def disconnect(self)
```
Ngắt kết nối an toàn và cleanup resources.

```python
def _test_connection(self, host: str, port: int, timeout: int = None) -> bool
```
Kiểm tra kết nối đến server trước khi connect chính thức.

##### User Input Methods

```python
def set_nickname(self) -> bool
```
Prompt user nhập nickname với validation.
- **Returns:** True nếu nickname hợp lệ

##### Messaging Methods

```python
def send_message(self, message: str) -> bool
```
Gửi tin nhắn đến server.
- **Parameters:** `message` - Nội dung tin nhắn
- **Returns:** True nếu gửi thành công

```python
def receive_messages(self)
```
Luồng nhận tin nhắn từ server (chạy trong thread riêng).

```python
def handle_user_input(self)
```
Xử lý input từ người dùng cho việc gửi tin nhắn và commands.

##### Threading Methods

```python
def start_receiving_thread(self)
```
Khởi tạo thread để nhận tin nhắn.

##### Main Method

```python
def start(self)
```
Entry point chính để chạy client với đầy đủ tính năng.

## Utility Functions

### Network Utilities

```python
from utils import test_server_connection, scan_network_for_servers

# Test kết nối
is_available = test_server_connection('192.168.1.100', 12345, timeout=5)

# Quét mạng tìm server
servers = scan_network_for_servers(port=12345, timeout=2)
```

### Validation Utilities

```python
from utils import validate_ip_address, validate_port, validate_nickname

# Validate IP
is_valid = validate_ip_address('192.168.1.100')  # True

# Validate port
is_valid = validate_port('8080')  # True

# Validate nickname
is_valid, message = validate_nickname('user123')  # (True, 'Valid')
```

### Configuration Utilities

```python
from config import get_default_server_info, get_buffer_size

# Lấy thông tin server mặc định
host, port = get_default_server_info()

# Lấy buffer size từ config  
buffer_size = get_buffer_size()
```

## Configuration

### Config File Structure

```ini
# config/client_config.ini

[server]
default_host = 127.0.0.1
default_port = 12345
timeout = 30
scan_timeout = 2

[client]
buffer_size = 1024
max_nickname_length = 20
auto_reconnect = false

[network]
auto_scan_enabled = true
priority_ips = 192.168.1.1,192.168.1.100,192.168.1.101
scan_range_start = 1
scan_range_end = 254

[ui]
show_timestamps = true
color_enabled = false
show_connection_menu = true
```

### Configuration Functions

```python
from config import load_config, get_connection_timeout

# Load toàn bộ config
config = load_config()

# Lấy timeout từ config
timeout = get_connection_timeout()  # 30 (seconds)

# Lấy max nickname length
max_len = get_max_nickname_length()  # 20
```

## Environment Variables

Client hỗ trợ các environment variables với ưu tiên cao nhất:

| Variable | Mô tả | Ví dụ |
|----------|-------|-------|
| `CHAT_SERVER_HOST` | Server IP address | `192.168.1.100` |
| `CHAT_SERVER_PORT` | Server port number | `8080` |

```bash
# Set server host và port mặc định
export CHAT_SERVER_HOST=192.168.1.100
export CHAT_SERVER_PORT=8080

# Chạy client (sẽ dùng env vars thay vì config file)
python3 client.py
```

**Priority Order (cao → thấp):**
1. 🌍 Environment Variables (`CHAT_SERVER_HOST`, `CHAT_SERVER_PORT`)
2. 📋 Config File (`config/client_config.ini`)  
3. 💻 Hard-coded defaults (`127.0.0.1:12345`)

## Error Handling

### Connection Errors

```python
try:
    client = ChatClient(host='invalid.host', port=12345)
    client.start()
except ConnectionRefusedError:
    print("Server không phản hồi")
except socket.timeout:
    print("Kết nối timeout")
except Exception as e:
    print(f"Lỗi không mong đợi: {e}")
```

### Input Validation Errors

```python
is_valid, error_msg = validate_nickname('user@invalid')
if not is_valid:
    print(f"Nickname không hợp lệ: {error_msg}")
```

## Usage Examples

### Basic Usage

```python
# Simple connection
client = ChatClient()
client.start()
```

### Advanced Usage

```python
# Custom configuration
client = ChatClient(
    host='192.168.1.100',
    port=8080,
    buffer_size=2048
)

# Manual connection steps
if client.connect():
    if client.set_nickname():
        client.start_receiving_thread()
        client.handle_user_input()
```

### Network Scanning

```python
from src.chat_client import _scan_for_servers

# Tìm server trong mạng
server_ip = _scan_for_servers(timeout=3, port=12345)
if server_ip:
    print(f"Found server at {server_ip}")
    client = ChatClient(host=server_ip)
    client.start()
```

## Exit Codes

- `0`: Thành công
- `1`: Lỗi kết nối hoặc lỗi chung
- `130`: Ngắt bằng Ctrl+C (KeyboardInterrupt)

## Thread Safety

- Message receiving chạy trong daemon thread
- Main thread xử lý user input
- Thread-safe disconnect khi user thoát
- Graceful cleanup khi program exit
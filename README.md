# Multi-User Chat Application - Client

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Client-side của ứng dụng chat đa người dùng với tính năng tự động phát hiện server và network scanning.

## 📋 Mô tả

Đây là phần client thông minh của ứng dụng chat đa người dùng, có khả năng tự động phát hiện server trong mạng và kết nối một cách linh hoạt.

## ✨ Tính năng chính

- 🔗 **Kết nối TCP cơ bản** - Kết nối đến chat server qua TCP/IP
- 💬 **Chat real-time** - Gửi và nhận tin nhắn tức thời
- 🧵 **Multi-threading** - Nhận tin nhắn không chặn việc gửi
- 🎯 **Smart Connection** - 4 tùy chọn kết nối linh hoạt
- � **Auto-discovery** - Tự động tìm server trong mạng LAN
- ⚙️ **Configurable** - Cấu hình linh hoạt qua file .ini
- 🌐 **Hỗ trợ environment variables** cho automation
- 🛡️ **Input validation** - Kiểm tra IP, port, nickname hợp lệ
- 🛡️ **Content Moderation** - Lọc nội dung không phù hợp và chống spam
- ⏱️ **Rate Limiting** - Giới hạn tần suất gửi tin nhắn
- � **User-friendly CLI** - Giao diện dòng lệnh thân thiện

## 🛠️ Yêu cầu hệ thống

## 📋 Yêu cầu hệ thống

- **Python 3.6+**
- **Thư viện built-in:** socket, threading, configparser, re, os

## 🛡️ Content Moderation

Client được trang bị hệ thống kiểm duyệt nội dung toàn diện:

### ✅ **Lọc nội dung:**
- Từ ngữ thô tục, không phù hợp → Thay bằng dấu sao hoặc từ chối
- Spam (lặp ký tự, chữ hoa, ký tự đặc biệt) → Từ chối
- Tin nhắn quá dài/quá ngắn → Từ chối

### ⏱️ **Rate Limiting:**
- Tối đa 5 tin nhắn trong 30 giây (có thể cấu hình)
- Chặn gửi spam tự động

### 📊 **Demo Content Moderation:**
```bash
# Demo tổng thể các tính năng
python3 examples/content_moderation_demo.py

# Test interactive content filter
python3 examples/test_content_filter.py
```

**Chi tiết:** [Content Moderation Guide](docs/content_moderation.md)

## 🚀 Cài đặt

1. **Clone repository:**
   ```bash
   git clone https://github.com/ncs-dev-vn/mmt-messaging-app-client.git
   cd mmt-messaging-app-client
   ```

2. **Tạo môi trường ảo (tùy chọn):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # hoặc
   venv\Scripts\activate     # Windows
   ```

## 📖 Sử dụng

### Khởi chạy client

```bash
python client.py
```

### Quy trình sử dụng

1. **Nhập thông tin server:**
   - Địa chỉ IP server (mặc định: 127.0.0.1)
   - Port server (mặc định: 12345)

2. **Nhập nickname:**
   - Tên hiển thị của bạn trong chat

3. **Bắt đầu chat:**
   - Gõ tin nhắn và nhấn Enter để gửi
   - Gõ "quit" hoặc "exit" để thoát
   - Nhấn Ctrl+C để thoát nhanh

### Ví dụ sử dụng

```
=== Multi-User Chat Client ===

Connection options:
1. Local server (127.0.0.1) - Same computer
2. Remote server - Enter IP manually
3. Quick connect - Smart defaults
4. Auto-scan local network (experimental)

Choose option (1-4, default=3): 4

🔍 Scanning for chat servers in local network...
   Scanning network: 192.168.1.1-254
   ✅ Server found at 192.168.1.100
✅ Found server at 192.168.1.100:12345

🔗 Connecting to 192.168.1.100:12345...
💬 After connecting, you can start chatting!
📝 Commands: type 'quit' to exit, Ctrl+C for quick exit
==================================================
Đã kết nối thành công với Server.
Nhập nickname của bạn: Alice
Xin chào mọi người!
Bob: Chào Alice! 
Charlie: Hi cả nhà!
quit
Đang ngắt kết nối...
```

## 📁 Cấu trúc dự án

```
mmt-messaging-app-client/
├── client.py              # Entry point chính
├── requirement.txt        # Yêu cầu đồ án
├── README.md              # Tài liệu này
├── LICENSE                # Giấy phép
│
├── src/                   # Source code chính
│   ├── __init__.py
│   └── chat_client.py     # Class ChatClient chính
│
├── config/                # Cấu hình
│   ├── __init__.py
│   └── client_config.ini  # File cấu hình
│
├── utils/                 # Tiện ích
│   ├── __init__.py        # Validation, formatting
│   └── network.py         # Network utilities
│
├── tests/                 # Unit tests
└── venv/                  # Virtual environment
```

## ⚙️ Cấu hình

Chỉnh sửa file `config/client_config.ini` để tùy chỉnh:

```ini
[server]
default_host = 127.0.0.1
default_port = 12345
timeout = 30

[client]
buffer_size = 1024
max_nickname_length = 20
auto_reconnect = false

[ui]
show_timestamps = true
color_enabled = false
```

## 🔧 API Documentation

### Class ChatClient

Lớp chính để quản lý kết nối thông minh và giao tiếp với server.

**Methods:**
- `_get_default_host()`: Tự động phát hiện server tốt nhất
- `_test_connection(host, port)`: Kiểm tra kết nối trước khi connect
- `connect()`: Thiết lập kết nối TCP với error handling
- `set_nickname()`: Nhập nickname với validation nâng cao
- `receive_messages()`: Luồng nhận tin nhắn (threading)
- `send_message(message)`: Gửi tin nhắn với error handling
- `handle_user_input()`: Xử lý input và commands
- `start_receiving_thread()`: Khởi tạo message thread
- `disconnect()`: Ngắt kết nối an toàn và cleanup
- `start()`: Chạy toàn bộ client với menu options

**Functions:**
- `_scan_for_servers(timeout)`: Quét mạng tìm server khả dụng
- `main()`: Entry point với menu lựa chọn kết nối

## 🐛 Xử lý lỗi

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `ConnectionRefusedError` | Server chưa chạy | Khởi động server trước |
| `Timeout` | Server không phản hồi | Kiểm tra IP/port và mạng |
| `Invalid IP` | Địa chỉ IP sai format | Nhập đúng format IP |
| `Invalid Port` | Port ngoài phạm vi 1-65535 | Sử dụng port hợp lệ |

## 🧪 Testing

```bash
# Chạy tests (khi có)
python -m pytest tests/

# Test thủ công với server local
python -m http.server 12345  # Server giả
python client.py             # Client test
```

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Dự án được phân phối dưới giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.

## 👥 Team

- **Phần Client:** Phát triển giao diện người dùng và kết nối
- **Phần Server:** Repository riêng biệt tại [mmt-messaging-app-server](https://github.com/ncs-dev-vn/mmt-messaging-app-server)

## 📞 Hỗ trợ

- 🐛 Báo lỗi: [Issues](https://github.com/ncs-dev-vn/mmt-messaging-app-client/issues)
- 💡 Góp ý tính năng: [Discussions](https://github.com/ncs-dev-vn/mmt-messaging-app-client/discussions)
- 📧 Email: support@chatapp.com

---

**⭐ Nếu project hữu ích, hãy cho một star!**
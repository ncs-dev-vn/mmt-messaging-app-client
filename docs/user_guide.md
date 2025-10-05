# User Guide - Multi-User Chat Client

## Giới thiệu

Đây là hướng dẫn sử dụng chi tiết cho ứng dụng Chat Client. Client này cho phép bạn kết nối đến chat server và tham gia các cuộc trò chuyện real-time.

## Cài đặt

### Yêu cầu hệ thống
- Python 3.6 trở lên
- Không cần cài đặt thư viện bên ngoài

### Cài đặt ứng dụng
```bash
# 1. Clone repository
git clone https://github.com/ncs-dev-vn/mmt-messaging-app-client.git
cd mmt-messaging-app-client

# 2. Chạy client
python3 client.py
```

## Hướng dẫn sử dụng

### 1. Khởi chạy ứng dụng

```bash
python3 client.py
```

Bạn sẽ thấy màn hình chào:
```
=== Multi-User Chat Client ===
✅ Configuration loaded successfully

Connection options:
1. Local server (127.0.0.1) - Same computer
2. Remote server - Enter IP manually
3. Quick connect - Smart defaults
4. Auto-scan local network (experimental)

Choose option (1-4, default=3):
```

### 2. Các tùy chọn kết nối

#### Option 1: Local Server
- **Khi nào dùng:** Server chạy trên cùng máy tính
- **Ưu điểm:** Nhanh, không cần setup mạng
- **Địa chỉ:** 127.0.0.1 (localhost)

```
Choose option (1-4, default=3): 1
🏠 Connecting to LOCAL server on port 12345
```

#### Option 2: Remote Server
- **Khi nào dùng:** Server ở máy khác trong mạng hoặc internet
- **Yêu cầu:** Biết địa chỉ IP của server
- **Nhập thông tin:** IP address và port

```
Choose option (1-4, default=3): 2
Enter server IP address: 192.168.1.100
Enter port (default=12345): 8080
🌐 Connecting to REMOTE server at 192.168.1.100:8080
```

#### Option 3: Quick Connect
- **Khi nào dùng:** Sử dụng cài đặt mặc định từ config
- **Ưu điểm:** Nhanh chóng, không cần nhập thông tin
- **Tự động:** Sử dụng smart detection

```
Choose option (1-4, default=3): 3
⚡ Quick connect mode (config: 127.0.0.1:12345)
```

#### Option 4: Auto-scan Network
- **Khi nào dùng:** Không biết IP của server
- **Ưu điểm:** Tự động tìm server trong mạng LAN
- **Lưu ý:** Có thể mất vài giây để scan

```
Choose option (1-4, default=3): 4
🔍 Scanning for chat servers in local network...
   Scanning network: 192.168.1.1-254 on port 12345
   ✅ Server found at 192.168.1.100:12345
✅ Found server at 192.168.1.100:12345
```

### 3. Nhập Nickname

Sau khi kết nối thành công, bạn cần nhập nickname:

```
Đã kết nối thành công với Server.
Nhập nickname của bạn: Alice
```

**Quy tắc nickname:**
- Không được để trống
- Tối đa 20 ký tự (có thể thay đổi trong config)
- Chỉ chứa chữ cái, số, dấu gạch dưới (_) và dấu gạch ngang (-)

### 4. Chat

Khi đã kết nối thành công, bạn có thể bắt đầu chat:

```
💬 After connecting, you can start chatting!
📝 Commands: type 'quit' to exit, Ctrl+C for quick exit
==================================================
[Alice đã tham gia phòng chat]
Xin chào mọi người!
Bob: Chào Alice!
Charlie: Hế lô cả nhà!
```

**Cách sử dụng:**
- Gõ tin nhắn → Nhấn Enter để gửi
- Tin nhắn từ người khác sẽ hiển thị tự động
- Gõ `quit` hoặc `exit` để thoát
- Nhấn `Ctrl+C` để thoát nhanh

### 5. Thoát khỏi chat

```
quit
Đang ngắt kết nối...
```

Hoặc nhấn `Ctrl+C`:
```
^C
Đang ngắt kết nối...
```

## Tùy chỉnh cấu hình

### File cấu hình

Chỉnh sửa file `config/client_config.ini`:

```ini
[server]
default_host = 192.168.1.100  # Thay đổi server mặc định
default_port = 8080           # Thay đổi port mặc định
timeout = 10                  # Giảm timeout nếu mạng nhanh

[client]
buffer_size = 2048           # Tăng buffer nếu tin nhắn dài
max_nickname_length = 15     # Giới hạn nickname ngắn hơn

[network]
auto_scan_enabled = false    # Tắt auto-scan nếu không cần
```

### Environment Variables

```bash
# Set server mặc định qua environment
export CHAT_SERVER_HOST=192.168.1.100
export CHAT_SERVER_PORT=8080
python3 client.py

# Client sẽ ưu tiên sử dụng IP và port từ environment variables
```

**Ưu tiên sử dụng:**
1. 🥇 Environment Variables (cao nhất)
2. 🥈 Config File  
3. 🥉 Hard-coded defaults (thấp nhất)

## Xử lý lỗi thường gặp

### 1. "Connection refused"
```
Lỗi: Không thể kết nối tới server. Lỗi: [Errno 61] Connection refused
```

**Nguyên nhân và giải pháp:**
- Server chưa chạy → Khởi động server trước
- IP/port sai → Kiểm tra lại địa chỉ server
- Firewall chặn → Tắt firewall hoặc mở port

### 2. "command not found: python"
```
zsh: command not found: python
```

**Giải pháp:**
- Thử `python3` thay vì `python`
- Cài đặt Python từ [python.org](https://python.org)

### 3. "No servers found"
```
❌ No servers found, falling back to localhost
```

**Nguyên nhân và giải pháp:**
- Không có server trong mạng LAN
- Server chạy port khác → Thay đổi port trong config
- Mạng bị chặn → Kiểm tra network security

### 4. "Nickname không hợp lệ"
```
❌ Nickname chỉ được chứa chữ, số, _ và -
```

**Giải pháp:**
- Không dùng ký tự đặc biệt (@, #, !, v.v.)
- Giữ độ dài dưới 20 ký tự
- Không để trống

## Tips và Tricks

### 1. Kết nối nhanh
```bash
# Set environment để không cần nhập IP mỗi lần
export CHAT_SERVER_HOST=192.168.1.100
export CHAT_SERVER_PORT=8080
echo "3" | python3 client.py  # Auto chọn option 3
```

### 2. Debug kết nối
```bash
# Test ping trước khi chạy client
ping 192.168.1.100

# Test port có mở không
telnet 192.168.1.100 12345
```

### 3. Multiple clients
```bash
# Mở nhiều terminal để test nhiều user
Terminal 1: python3 client.py  # Alice
Terminal 2: python3 client.py  # Bob
Terminal 3: python3 client.py  # Charlie
```

### 4. Tùy chỉnh nhanh
```bash
# Thay đổi port mặc định nhanh
sed -i 's/default_port = 12345/default_port = 8080/' config/client_config.ini
```

## Troubleshooting Advanced

### 1. Network Issues
```bash
# Kiểm tra network interface
ifconfig  # macOS/Linux
ipconfig  # Windows

# Kiểm tra routing
netstat -rn

# Test DNS
nslookup google.com
```

### 2. Python Issues
```bash
# Kiểm tra Python version
python3 --version

# Kiểm tra modules
python3 -c "import socket, threading; print('OK')"

# Test socket cơ bản
python3 -c "import socket; s=socket.socket(); print('Socket OK')"
```

### 3. Config Issues
```bash
# Kiểm tra config syntax
python3 -c "
import configparser
config = configparser.ConfigParser()
config.read('config/client_config.ini')
print('Config OK')
"
```

## FAQ

**Q: Client có thể kết nối qua internet không?**
A: Có, nhưng server cần có IP công khai và port forwarding.

**Q: Có thể chat với nhiều server cùng lúc không?**
A: Hiện tại không, mỗi instance client chỉ kết nối 1 server.

**Q: Tin nhắn có được mã hóa không?**
A: Hiện tại chưa, tin nhắn gửi dạng plain text qua TCP.

**Q: Client có lưu lịch sử chat không?**
A: Hiện tại không, tin nhắn chỉ hiển thị trong session hiện tại.

**Q: Có thể thay đổi giao diện không?**
A: Hiện tại chỉ CLI, có thể phát triển GUI trong tương lai.

---

**🎉 Chúc bạn có những cuộc trò chuyện vui vẻ!**
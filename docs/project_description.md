# Xây dựng ứng dụng Chat Client đa người dùng

**Thời gian:** 5 tuần  
**Vai trò:** Client-side Development

## Mục tiêu Client

- Hiểu và triển khai phần client trong mô hình client-server
- Sử dụng thư viện socket và threading của Python để kết nối server
- Xây dựng giao diện dòng lệnh thân thiện cho người dùng
- Xử lý kết nối mạng và giao tiếp với server

## Yêu cầu Client

### 1. Kết nối và Giao tiếp cơ bản
- **Nhiệm vụ:** Viết mã cho client có thể kết nối đến server qua TCP
- **Chức năng:**
  - Nhập địa chỉ IP và port của server
  - Nhập nickname người dùng
  - Gửi và nhận tin nhắn real-time
- **Kết quả cần đạt:** Client có thể kết nối và chat với server

### 2. Tính năng nâng cao
- **Tự động phát hiện server:** Quét mạng LAN tìm server khả dụng
- **Menu lựa chọn kết nối:** Local, Remote, Quick connect, Auto-scan
- **Xử lý lỗi mạnh mẽ:** Connection timeout, server unreachable
- **Threading:** Nhận tin nhắn không chặn việc gửi tin nhắn
- **Kết quả cần đạt:** Client thông minh, dễ sử dụng

### 3. Cấu hình và Tùy chỉnh
- **File cấu hình:** `config/client_config.ini` để tùy chỉnh
- **Environment variables:** Hỗ trợ CHAT_SERVER_HOST
- **Validation:** Kiểm tra IP, port, nickname hợp lệ
- **Kết quả cần đạt:** Client linh hoạt và có thể tùy chỉnh

---

## Cấu trúc dự án Client

```
mmt-messaging-app-client/
├── client.py              # Entry point chính
├── src/                   # Source code
│   ├── __init__.py
│   └── chat_client.py     # Class ChatClient chính
├── config/                # Cấu hình
│   ├── __init__.py
│   └── client_config.ini  # File cấu hình
├── utils/                 # Utilities
│   ├── __init__.py        # Validation, formatting
│   └── network.py         # Network utilities
├── tests/                 # Unit tests
├── docs/                  # Tài liệu
└── requirements.txt       # Dependencies
```

## Thư viện Python sử dụng

- **socket:** Giao tiếp mạng TCP/IP với server
- **threading:** Xử lý đồng thời nhận/gửi tin nhắn
- **configparser:** Đọc file cấu hình .ini
- **re:** Regular expressions cho validation
- **os:** Environment variables và file path utilities

## Tính năng đã implement

### ✅ Đã hoàn thành:
- [x] Kết nối TCP cơ bản đến server
- [x] Gửi và nhận tin nhắn real-time
- [x] Threading cho việc nhận tin nhắn
- [x] Menu lựa chọn kết nối (4 options)
- [x] Tự động phát hiện server trong mạng
- [x] Network scanning với multi-threading
- [x] Cấu hình linh hoạt qua file .ini
- [x] Enhanced input validation
- [x] Graceful error handling
- [x] Environment variable support
- [x] **Content moderation system** - Lọc nội dung không phù hợp
- [x] **Spam prevention** - Chống tin nhắn spam và lặp
- [x] **Rate limiting** - Giới hạn tần suất gửi tin nhắn
- [x] **Message validation** - Kiểm tra độ dài, format tin nhắn

### 🔄 Có thể mở rộng:
- [ ] GUI interface (PyQt/Tkinter)
- [ ] Message encryption
- [ ] File transfer capability
- [ ] Connection history
- [ ] Multiple server support
- [ ] Offline message queue

---

## Lưu ý phát triển

- **Tách biệt client/server:** Dự án này chỉ phát triển phần client
- **Server repository:** [mmt-messaging-app-server](https://github.com/ncs-dev-vn/mmt-messaging-app-server)
- **Testing:** Sử dụng unit tests và integration tests
- **Documentation:** Giữ README.md và docs/ được cập nhật
- **Code quality:** Tuân theo PEP 8 và best practices

## Hướng dẫn sử dụng

1. **Cài đặt và chạy:**
   ```bash
   python3 client.py
   ```

2. **Chọn kết nối:**
   - Option 1: Local server (127.0.0.1)
   - Option 2: Remote server (nhập IP thủ công)
   - Option 3: Quick connect (smart defaults)
   - Option 4: Auto-scan network

3. **Tùy chỉnh config:**
   ```ini
   # config/client_config.ini
   [server]
   default_host = 192.168.1.100
   default_port = 8080
   ```

4. **Environment variables:**
   ```bash
   export CHAT_SERVER_HOST=192.168.1.100
   export CHAT_SERVER_PORT=8080
   python3 client.py
   ```
# 💬 Multi-User Chat Client

Ứng dụng chat client hiện đại với giao diện terminal đầy màu sắc, hỗ trợ nhiều tính năng nâng cao.

## ✨ Tính năng chính

### 🔐 **Bảo mật & Validation**
- ✅ Nickname validation với quy tắc nghiêm ngặt
- ✅ Content filtering & profanity detection
- ✅ Spam protection
- ✅ Message length validation

### 🌐 **Kết nối thông minh**
- ✅ Auto-discovery servers trong LAN
- ✅ Network scanning với multi-threading  
- ✅ Fallback manual connection
- ✅ Connection timeout handling

### 🎨 **Giao diện đẹp mắt**
- ✅ Color-coded messages (tin nhắn có màu)
- ✅ Timestamp cho mọi tin nhắn
- ✅ Emoji và icon hỗ trợ
- ✅ Cross-platform color support

### ⚡ **Tính năng nâng cao**
- ✅ Queue system (hàng chờ khi server đầy)
- ✅ Command system (/help, /debug, /quit)
- ✅ Threaded message receiving
- ✅ Graceful disconnect
- ✅ Real-time message processing

## 🏗️ Cấu trúc dự án

```
mmt-messaging-app-client/
├── 📄 main.py                    # Entry point chính
├── 📄 README.md                  # Documentation
├── 📄 requirements.txt           # Python dependencies
├── 📄 .gitignore                 # Git ignore rules
└── 📁 src/                       # Source code
    ├── 📄 __init__.py
    ├── 📁 client/                # Client implementation
    │   ├── 📄 __init__.py
    │   ├── 📄 chat_client.py     # Core chat client
    │   └── 📄 message_handler.py # Message processing
    ├── 📁 config/                # Configuration
    │   ├── 📄 __init__.py
    │   ├── 📄 settings.py        # App settings
    │   └── 📄 network_scanner.py # Network discovery
    ├── 📁 ui/                    # User Interface
    │   ├── 📄 __init__.py
    │   ├── 📄 colors.py          # ANSI colors
    │   ├── 📄 formatters.py      # Message formatters
    │   └── 📄 ui_helpers.py      # UI utilities
    └── 📁 utils/                 # Utilities
        ├── 📄 __init__.py
        ├── 📄 validators.py      # Input validation
        └── 📄 content_filter.py  # Content filtering
```

## 🚀 Cài đặt và chạy

### **Yêu cầu hệ thống:**
- Python 3.7+ 
- Terminal hỗ trợ ANSI colors (macOS Terminal, Linux, Windows Terminal)

### **Cài đặt:**

```bash
# Clone hoặc download dự án
cd multi_user_chat/mmt-messaging-app-client

# Không cần cài đặt dependencies (sử dụng Python built-in)
# Optional: pip install -r requirements.txt
```

### **Chạy ứng dụng:**

```bash
# Chạy client
python main.py

# Hoặc với Python 3 explicit
python3 main.py
```

## 🎮 Hướng dẫn sử dụng

### **1. Kết nối Server**

Khi chạy, bạn sẽ được hỏi cách kết nối:

```
=== Cấu hình Server ===
1. Tự động quét mạng LAN
2. Nhập thủ công
Chọn phương thức (1/2) [mặc định: 2]:
```

**Tùy chọn 1:** Auto-discovery
- ✅ Tự động quét mạng LAN tìm chat servers
- ✅ Hiển thị danh sách servers có sẵn
- ✅ Chọn server từ danh sách

**Tùy chọn 2:** Manual input
- ✅ Nhập IP address hoặc hostname
- ✅ Nhập port number
- ✅ Validation input

### **2. Đặt Nickname**

```
Nhập nickname của bạn: YourName
```

**Quy tắc nickname:**
- Độ dài: 1-20 ký tự
- Chỉ chữ cái, số, dấu gạch dưới (_), gạch ngang (-)
- Không bắt đầu/kết thúc bằng ký tự đặc biệt
- Không được trùng với người khác

### **3. Chat Interface**

```
💬 HƯỚNG DẪN CHAT:
  • Tin nhắn của bạn: Màu xanh dương
  • Tin nhắn người khác: Màu xanh lá  
  • Thông báo server: Màu vàng
  • Cảnh báo: Màu cam
  • Lỗi/Từ chối: Màu đỏ
  • Gõ "/help" để xem các lệnh
  • Gõ "quit" hoặc "exit" để thoát
==================================================

> Hello everyone!
```

### **4. Commands hỗ trợ**

| Command | Mô tả | Màu hiển thị |
|---------|-------|-------------|
| `/help` | Hiển thị trợ giúp | 🟡 Vàng |
| `/debug` | Thông tin debug (host, nickname, status) | 🟡 Vàng |
| `/nick` | Hiển thị nickname hiện tại | 🟡 Vàng |
| `/setnick` | Đặt lại nickname | 🟡 Vàng |
| `quit` hoặc `exit` | Thoát khỏi chat | 🟡 Vàng |

**Lưu ý:** Commands luôn được hiển thị bằng màu vàng để dễ nhận biết đây là phản hồi từ hệ thống.

## 🎨 Giao diện và màu sắc

### **Hệ thống màu đơn giản (5 màu chính):**

- 🔵 **Tin nhắn của bạn (BLUE):** `[12:34:56] Bạn: Hello everyone!`
- 🟢 **Tin nhắn người khác (GREEN):** `[12:34:56] Alice: Hi there!`
- 🟡 **Thông báo server (YELLOW):** `[12:34:56] [SERVER] Alice đã tham gia phòng chat`
- 🟠 **Cảnh báo (ORANGE):** `⚠️ Tin nhắn quá dài, đã cắt bớt`
- 🔴 **Lỗi/Từ chối (RED):** `❌ Không thể kết nối đến server`

### **Chi tiết phân loại màu:**

#### **🔵 Màu xanh dương (Your Messages)**
```
[15:30:25] Bạn: Hello everyone! 👋
[15:30:28] Bạn: How is everyone doing today?
```

#### **🟢 Màu xanh lá (Other Users)**
```
[15:30:26] Alice: Hi there! Welcome to the chat
[15:30:29] Bob: Great to see new people joining
```

#### **🟡 Màu vàng (Server/Info/Success)**
```
✅ Đã kết nối thành công với Server (127.0.0.1:12345)
ℹ️ Đang kiểm tra trạng thái phòng chat...
[15:30:24] [SERVER] Alice đã tham gia phòng chat
```

#### **🟠 Màu cam (Warnings)**
```
⚠️ Cảnh báo: Đã lọc 1 từ không phù hợp
⚠️ Tin nhắn quá dài, chỉ hiển thị 500 ký tự đầu
⚠️ Đang thử kết nối lại...
```

#### **🔴 Màu đỏ (Errors/Rejected)**
```
❌ Nickname "admin" bị từ chối: Tên cấm
❌ Server từ chối kết nối
🚫 Bạn đã bị kick khỏi phòng chat
```

### **Lợi ích của color scheme mới:**
- ✅ **Đơn giản hóa:** Chỉ 5 màu thay vì 10+ màu trước đây
- ✅ **Dễ phân biệt:** Mỗi màu có ý nghĩa rõ ràng và nhất quán
- ✅ **Thân thiện với mắt:** Giảm visual clutter, không gây chói mắt
- ✅ **Accessible:** Tương thích tốt với các terminal và OS khác nhau
- ✅ **Professional:** UI sạch sẽ và chuyên nghiệp hơn

## 🛡️ Bảo mật và Content Filter

### **Nickname Validation:**
- Kiểm tra độ dài và ký tự hợp lệ
- Chặn các tên cấm (admin, server, system...)
- Validation realtime

### **Content Filtering:**
- **Profanity Filter:** Tự động lọc từ ngữ không phù hợp
- **Spam Detection:** Phát hiện spam patterns
- **Length Control:** Giới hạn độ dài tin nhắn
- **Link Blocking:** Chặn URLs không mong muốn

### **Ví dụ filtering với màu mới:**
```bash
> This is a damn good message
⚠️ Cảnh báo: Đã lọc 1 từ không phù hợp        # ORANGE - Warning
[12:34:56] Bạn: This is a **** good message   # BLUE - Your message
```

## 🌐 Network Discovery

### **Auto-discovery features:**
- Quét mạng LAN tự động
- Multi-threaded scanning
- Configurable ports: 12345, 8080, 3000, 9999, 5000, 8000
- Smart timeout handling

### **Ví dụ auto-discovery:**
```
🌐 Tự động tìm kiếm chat servers trong mạng LAN...
🔍 Đang quét mạng 192.168.1.0/24 trên các port [12345, 8080, 3000]...
✅ Tìm thấy server: 192.168.1.100:12345
✅ Tìm thấy server: 192.168.1.50:8080

🎉 Tìm thấy 2 server(s):
   1. 192.168.1.100:12345
   2. 192.168.1.50:8080

Chọn server (1-2) hoặc Enter để manual: 1
✅ Đã chọn server: 192.168.1.100:12345
```

## ⚙️ Configuration

### **Default Settings:**
```python
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 12345
DEFAULT_BUFFER_SIZE = 1024
DEFAULT_TIMEOUT = 30
MAX_NICKNAME_LENGTH = 20
MAX_MESSAGE_LENGTH = 500
```

### **Tùy chỉnh settings:**
Có thể chỉnh sửa trong `src/config/settings.py`

## 🐛 Troubleshooting

### **Lỗi thường gặp:**

**1. Import Error:**
```bash
❌ Lỗi import: attempted relative import beyond top-level package
```
**Giải pháp:** Đảm bảo chạy từ thư mục gốc với `python main.py`

**2. Connection Refused:**
```bash
❌ Server từ chối kết nối. Kiểm tra server có đang chạy không?
```
**Giải pháp:** Kiểm tra server đang chạy và port đúng

**3. Nickname Taken:**
```bash
❌ Nickname "John" đã được sử dụng bởi người khác
```
**Giải pháp:** Chọn nickname khác

**4. Terminal không hiển thị màu:**
- Sử dụng terminal hỗ trợ ANSI colors
- macOS: Terminal.app hoặc iTerm2
- Windows: Windows Terminal
- Linux: Hầu hết terminals

## 🤝 Đóng góp

### **Cách contribute:**
1. Fork dự án
2. Tạo feature branch
3. Commit changes
4. Push to branch  
5. Tạo Pull Request

### **Areas cần cải thiện:**
- [ ] GUI interface (tkinter/PyQt)
- [ ] File transfer support
- [ ] Voice chat integration
- [ ] Mobile app
- [ ] Web interface
- [ ] Encryption support

## 📝 Changelog

### **v1.0.0** (Current)
- ✅ Core chat functionality
- ✅ Auto-discovery network scanning
- ✅ Content filtering và validation
- ✅ Color-coded UI
- ✅ Command system
- ✅ Queue support
- ✅ Modular architecture

### **Planned Features:**
- 🔄 File sharing
- 🔄 Private messaging
- 🔄 Chat rooms
- 🔄 Message history
- 🔄 User profiles
- 🔄 Emoticons support


## 📄 License

MIT License - xem file LICENSE để biết chi tiết.

---

**Made with ❤️ for the community**

*Happy Chatting! 💬✨*
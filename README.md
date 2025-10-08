# 📚 Tài Liệu Dự Án - MMT Messaging App

## 🎯 Tổng Quan
Bộ tài liệu hoàn chỉnh cho **Ứng Dụng Chat Đa Người Dùng** - phiên bản tiếng Việt với các tính năng hiện đại như tự động khám phá mạng, lọc nội dung thông minh, và giao thức chat tùy chỉnh.

---

## 📖 Danh Mục Tài Liệu

### 👤 Dành cho Người Dùng Cuối
- **[Hướng Dẫn Người Dùng](./huong-dan-nguoi-dung.md)** 🚀
  - Cách cài đặt và sử dụng ứng dụng
  - Hướng dẫn kết nối tự động và thủ công
  - Xử lý sự cố thường gặp
  - Mẹo sử dụng hiệu quả

### 🏢 Dành cho Quản Lý Dự Án
- **[Mô Tả Dự Án](./mo-ta-du-an.md)** 📋
  - Tổng quan kiến trúc và mục tiêu
  - Công nghệ sử dụng và tính năng
  - Metrics hiệu năng và bảo mật
  - Roadmap phát triển tương lai

### 👩‍💻 Dành cho Lập Trình Viên
- **[Kỹ Thuật Chi Tiết](./ky-thuat-chi-tiet.md)** 🔧
  - Kiến trúc hệ thống và module analysis
  - Implementation details và API reference
  - Performance optimization và best practices
  - Error handling và debugging guidelines

### 🌐 Dành cho Kỹ Sư Mạng
- **[Giao Thức Chat](./giao-thuc-chat.md)** 📡
  - Protocol specification chi tiết
  - Message format và validation rules
  - Network security và anti-abuse measures
  - Future protocol extensions

---

## 🚀 Quick Start

### 📥 Người Dùng Mới
1. Đọc **[Hướng Dẫn Người Dùng](./huong-dan-nguoi-dung.md)** 
2. Chạy: `python3 run_client.py`
3. Chọn "Tự động quét mạng LAN"
4. Bắt đầu chat!

### 🔧 Lập Trình Viên Mới  
1. Đọc **[Mô Tả Dự Án](./mo-ta-du-an.md)** để hiểu tổng quan
2. Tìm hiểu **[Kỹ Thuật Chi Tiết](./ky-thuat-chi-tiet.md)** cho implementation
3. Xem **[Giao Thức Chat](./giao-thuc-chat.md)** để hiểu communication protocol

---

## 🎯 Tính Năng Nổi Bật

### 🔍 Auto-Discovery Network
- **Tự động quét mạng LAN** để tìm máy chủ chat
- **Multi-threaded scanning** với hiệu suất cao
- **Smart subnet detection** và IP range calculation

### 🛡️ Content Moderation  
- **Lọc từ ngữ không phù hợp** (20+ từ khóa cấm)
- **Anti-spam detection** với regex patterns
- **Input validation** đa cấp độ

### 📡 Custom Chat Protocol
- **SET_NICKNAME**: Đăng ký biệt danh (không broadcast)
- **CHAT**: Tin nhắn chat (broadcast toàn bộ)
- **UTF-8 encoding** hỗ trợ tiếng Việt

### 🌐 Network Flexibility
- **LAN discovery**: Tự động tìm server trong mạng nội bộ
- **Manual configuration**: Hỗ trợ IP/domain tùy chỉnh
- **Multiple server support**: Chọn từ danh sách servers khả dụng

---

## 📊 Thông Tin Kỹ Thuật

| Thông Số | Giá Trị | Mô Tả |
|-----------|---------|--------|
| **Ngôn ngữ** | Python 3.6+ | Zero external dependencies |
| **Kiến trúc** | Client-Server TCP | Socket programming |
| **Protocol** | Custom text-based | SET_NICKNAME + CHAT messages |
| **Encoding** | UTF-8 | Hỗ trợ tiếng Việt đầy đủ |
| **Threading** | Multi-threaded | Network scan + real-time chat |
| **Platform** | Cross-platform | Windows, macOS, Linux |

---

## 🔄 Quy Trình Phát Triển

### 🧪 Testing
```bash  
# Unit tests
python -m pytest tests/

# Integration tests  
python test_integration.py

# Network tests
python test_network_discovery.py
```

### 📝 Documentation Updates
1. **User Guide**: Cập nhật khi có tính năng mới
2. **Technical Docs**: Sync với code changes
3. **Protocol Spec**: Version control cho protocol changes
4. **Project Overview**: Update roadmap và metrics

### 🚀 Release Process
1. Update version numbers
2. Test all functionality 
3. Update documentation
4. Create release notes
5. Tag git release

---

## 🆘 Hỗ Trợ

### 🐛 Báo Lỗi
- **Issues**: Sử dụng GitHub Issues cho bug reports
- **Feature Requests**: Đề xuất tính năng mới qua Issues
- **Documentation**: Góp ý cải thiện tài liệu

### 💬 Community
- **Discussions**: GitHub Discussions cho Q&A
- **Contributing**: Đọc CONTRIBUTING.md (nếu có)
- **Code of Conduct**: Tuân thủ quy tắc ứng xử tích cực

---

## 📈 Roadmap

### ✅ Hoàn Thành (v2.0)
- ✅ Auto-discovery mạng LAN
- ✅ Content moderation system
- ✅ Custom chat protocol  
- ✅ Vietnamese documentation
- ✅ Error handling và recovery

### 🔄 Đang Phát Triển (v2.1)
- 🔄 GUI interface với tkinter
- 🔄 File sharing capability
- 🔄 Better emoji support
- 🔄 Chat history persistence

### 🔮 Tương Lai (v3.0+)
- 🔮 End-to-end encryption
- 🔮 Voice/video chat
- 🔮 Mobile app support
- 🔮 Cloud server deployment
- 🔮 Plugin system

---

## 📄 License và Credits

**License**: Open Source (xem LICENSE file)  
**Developed**: Vietnam 🇻🇳  
**Language**: Vietnamese (Tiếng Việt)  
**Community**: Dành cho cộng đồng developer Việt Nam

---

**📧 Liên hệ**: Tạo GitHub Issue để được hỗ trợ  
**🌟 Star**: Nếu project hữu ích, hãy star trên GitHub!  
**🔗 Share**: Chia sẻ với developer khác trong cộng đồng

---

*Cập nhật lần cuối: December 2024 - Version 2.0*
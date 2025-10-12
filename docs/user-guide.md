# User Guide

## 🚀 Bắt đầu

### Khởi động ứng dụng
```bash
python main.py
```

### Cấu hình kết nối

#### Auto-discovery (Khuyên dùng)
1. Chọn option `1` khi được hỏi
2. Ứng dụng sẽ tự động quét mạng LAN
3. Chọn server từ danh sách tìm thấy

#### Manual Configuration
1. Chọn option `2` khi được hỏi
2. Nhập server host (ví dụ: `192.168.1.100`)
3. Nhập server port (ví dụ: `12345`)

## 💬 Sử dụng Chat

### Đặt Nickname
- Nhập nickname khi được yêu cầu
- Nickname phải:
  - Từ 1-20 ký tự
  - Chỉ chứa chữ cái, số, `_`, `-`
  - Không bắt đầu/kết thúc bằng `_` hoặc `-`
  - Không trùng với người khác

### Gửi tin nhắn
- Gõ tin nhắn và nhấn Enter
- Tin nhắn sẽ hiển thị màu xanh dương (tin nhắn của bạn)
- Tin nhắn người khác hiển thị màu xanh lá

### Commands hệ thống

| Command | Mô tả |
|---------|-------|
| `/help` | Hiển thị danh sách commands |
| `/debug` | Hiển thị thông tin debug |
| `/nick` | Hiển thị nickname hiện tại |
| `/setnick` | Đặt lại nickname |
| `quit` hoặc `exit` | Thoát khỏi chat |

## 🎨 Giao diện - Hệ thống 5 màu đơn giản

### **Màu sắc tin nhắn**

#### **🔵 Xanh dương - Tin nhắn của bạn**
```
[15:30:25] Bạn: Hello everyone! 👋
[15:30:28] Bạn: How is everyone doing today?
```
**Sử dụng:** Tất cả tin nhắn bạn gửi trong chat

#### **🟢 Xanh lá - Tin nhắn người khác**
```
[15:30:26] Alice: Hi there! Welcome!
[15:30:29] Bob: Great to see new people
[15:30:31] Charlie: How's everyone doing?
```
**Sử dụng:** Tin nhắn từ các thành viên khác trong chat

#### **🟡 Vàng - Server/System Messages**
```
✅ Đã kết nối thành công với Server (127.0.0.1:12345)
ℹ️ Đang kiểm tra trạng thái phòng chat...
✅ Nickname "Alice" đã được chấp nhận!
[15:30:24] [SERVER] Bob đã tham gia phòng chat
[15:30:35] [SERVER] Charlie đã rời phòng chat
```
**Sử dụng:** 
- Thông báo kết nối/ngắt kết nối
- Thông báo server 
- Phản hồi commands
- Success messages

#### **🟠 Cam - Cảnh báo (Warnings)**
```
⚠️ Cảnh báo: Đã lọc 1 từ không phù hợp
⚠️ Tin nhắn quá dài, chỉ hiển thị 500 ký tự đầu
⚠️ Kết nối không ổn định, đang thử kết nối lại...
⚠️ Timeout khi chờ phản hồi từ server
```
**Sử dụng:**
- Content filtering warnings
- Network warnings
- Performance warnings
- Non-critical issues

#### **🔴 Đỏ - Lỗi/Từ chối (Errors/Rejected)**
```
❌ Nickname "admin" bị từ chối: Tên cấm
❌ Server từ chối kết nối. Kiểm tra server có đang chạy không?
🚫 Tin nhắn bị từ chối: Chứa nội dung không phù hợp
❌ Không thể gửi tin nhắn: Mất kết nối
🚫 Bạn đã bị kick khỏi phòng chat
```
**Sử dụng:**
- Connection errors
- Validation failures
- Rejected messages/nicknames
- Critical system errors

### **Thông tin hiển thị**
- **Timestamp**: `[HH:MM:SS]` cho mọi tin nhắn chat
- **Sender**: Tên người gửi (cho tin nhắn người khác)
- **You indicator**: "Bạn:" cho tin nhắn của bạn

## 🔄 Queue System

### Khi phòng chat đầy
1. Bạn sẽ vào hàng chờ
2. Hiển thị vị trí hàng chờ (màu vàng)
3. Không thể gửi tin nhắn (chỉ xem)
4. Khi có chỗ trống, tự động vào phòng

### Thông báo queue (màu vàng)
```
⏰ Đang chờ vào phòng chat... Vị trí hàng chờ: 3
⏰ Vị trí hàng chờ hiện tại: 2
✅ Bạn hiện đã kết nối với chat!
```

## 🛡️ Content Filtering

### Tự động lọc
- **Profanity**: Từ ngữ không phù hợp được thay bằng `***` + cảnh báo màu cam
- **Spam**: Ký tự lặp lại, chữ in hoa quá mức + cảnh báo màu cam  
- **Links**: URLs bị chặn + lỗi màu đỏ

### Ví dụ filtering
```bash
# Input
> This is damn good, but HELLLLOOOO there!!!

# Output
⚠️ Cảnh báo: Đã lọc 1 từ không phù hợp              # Cam - Warning
⚠️ Cảnh báo: Đã giảm spam (ký tự lặp và chữ hoa)    # Cam - Warning  
[15:45:12] Bạn: This is **** good, but Hello there!  # Xanh dương - Your message
```

### Giới hạn
- **Nickname**: Tối đa 20 ký tự
- **Message**: Tối đa 500 ký tự

## ⚠️ Lưu ý

### Color Scheme Benefits
- **Đơn giản**: Chỉ 5 màu dễ nhớ thay vì nhiều màu rối mắt
- **Nhất quán**: Cùng logic màu trong toàn bộ ứng dụng
- **Professional**: Giao diện sạch sẽ và chuyên nghiệp
- **Accessible**: Tương thích tốt với mọi terminal

### Best Practices
- Sử dụng nickname có ý nghĩa
- Tránh spam tin nhắn
- Tôn trọng người dùng khác
- Không chia sẻ thông tin cá nhân

### Terminal Compatibility
- **Recommended terminals**:
  - macOS: Terminal.app, iTerm2
  - Windows: Windows Terminal, PowerShell 
  - Linux: Most modern terminals
- **Fallback**: Nếu không hỗ trợ màu, sẽ hiển thị text thuần

## 🚪 Thoát ứng dụng

### Cách thoát
1. Gõ `quit` hoặc `exit`
2. Nhấn `Ctrl+C`
3. Đóng terminal/command prompt

### Auto cleanup
- Kết nối được đóng an toàn
- Server được thông báo về việc disconnect
- Resources được giải phóng tự động
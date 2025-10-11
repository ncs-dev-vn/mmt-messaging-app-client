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
| `quit` hoặc `exit` | Thoát khỏi chat |

## 🎨 Giao diện

### Màu sắc tin nhắn
- 🔵 **Xanh dương đậm**: Tin nhắn của bạn
- 🟢 **Xanh lá**: Tin nhắn của người khác  
- 🟡 **Vàng**: Thông báo server
- 🔴 **Đỏ**: Thông báo lỗi
- 🟠 **Cam**: Cảnh báo

### Thông tin hiển thị
- **Timestamp**: `[HH:MM:SS]` cho mọi tin nhắn
- **Sender**: Tên người gửi
- **Queue status**: Vị trí hàng chờ (nếu phòng đầy)

## 🔄 Queue System

### Khi phòng chat đầy
1. Bạn sẽ vào hàng chờ
2. Hiển thị vị trí hàng chờ
3. Không thể gửi tin nhắn (chỉ xem)
4. Khi có chỗ trống, tự động vào phòng

### Thông báo queue
- `⏰ Đang chờ vào phòng chat... Vị trí hàng chờ: X`
- `✅ Bạn hiện đã kết nối với chat!`

## 🛡️ Content Filtering

### Tự động lọc
- **Profanity**: Từ ngữ không phù hợp được thay bằng `***`
- **Spam**: Ký tự lặp lại, chữ in hoa quá mức
- **Links**: URLs bị chặn để tránh spam

### Giới hạn
- **Nickname**: Tối đa 20 ký tự
- **Message**: Tối đa 500 ký tự

## ⚠️ Lưu ý

### Best Practices
- Sử dụng nickname có ý nghĩa
- Tránh spam tin nhắn
- Tôn trọng người dùng khác
- Không chia sẻ thông tin cá nhân

### Troubleshooting
- Nếu mất kết nối: Ứng dụng sẽ tự động thông báo
- Nếu nickname bị từ chối: Thử nickname khác
- Nếu không thể gửi tin nhắn: Kiểm tra có đang trong queue không

## 🚪 Thoát ứng dụng

### Cách thoát
1. Gõ `quit` hoặc `exit`
2. Nhấn `Ctrl+C`
3. Đóng terminal/command prompt

### Auto cleanup
- Kết nối được đóng an toàn
- Server được thông báo về việc disconnect
- Resources được giải phóng tự động
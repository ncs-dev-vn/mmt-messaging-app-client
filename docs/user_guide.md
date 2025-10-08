# Hướng Dẫn Người Dùng - Ứng Dụng Chat Đa Người Dùng 🚀

## 📖 Tổng quan

Ứng dụng Chat hiện đại với khả năng **tự động tìm kiếm máy chủ**, **giao diện thân thiện**, và **hệ thống lọc nội dung** thông minh. Được thiết kế cho người dùng cuối với trải nghiệm đơn giản và trực quan.

## 🚀 Bắt Đầu Nhanh

### Bước 1: Khởi chạy ứng dụng
```bash
# Chạy ứng dụng chat
python3 run_client.py
```

### Bước 2: Chọn cách kết nối
```
=== Ứng Dụng Chat Đa Người Dùng ===
=== Cấu hình Máy chủ ===
1. Tự động quét mạng LAN    ← Khuyến nghị cho người mới
2. Nhập thủ công           ← Dành cho người dùng nâng cao

Chọn phương thức (1/2) [mặc định: 2]:
```

### Bước 3: Kết nối và chat
- Nhập biệt danh của bạn
- Bắt đầu chat với mọi người!

## 🌐 Cách Kết Nối Máy Chủ

### 🔍 Phương pháp 1: Tự động khám phá (Dễ nhất)

**Khi nào sử dụng**: Khi bạn không biết địa chỉ máy chủ cụ thể

```bash
# Chọn tùy chọn 1 khi được hỏi
Chọn phương thức (1/2): 1

# Ứng dụng sẽ tự động quét mạng
🔍 Đang quét mạng 192.168.1.0/24...
✅ Tìm thấy máy chủ: 192.168.1.100:12345
✅ Tìm thấy máy chủ: 192.168.1.200:8080

🎉 Tìm thấy 2 máy chủ:
   1. 192.168.1.100:12345
   2. 192.168.1.200:8080

# Chọn máy chủ từ danh sách
Chọn máy chủ (1-2): 1
```

**Ưu điểm**:
- ✅ Không cần biết địa chỉ IP
- ✅ Tự động tìm tất cả máy chủ trong mạng
- ✅ Hiển thị danh sách để lựa chọn
- ✅ Thích hợp cho mạng LAN/văn phòng

**Lưu ý**:
- Quá trình quét có thể mất 10-30 giây
- Cần kết nối mạng LAN với máy chủ chat
- Chỉ tìm máy chủ trong cùng subnet

### ⌨️ Phương pháp 2: Nhập thủ công (Chính xác)

**Khi nào sử dụng**: Khi bạn biết chính xác địa chỉ máy chủ

```bash
# Chọn tùy chọn 2 khi được hỏi  
Chọn phương thức (1/2): 2

--- Nhập thủ công ---
Nhập địa chỉ máy chủ [mặc định: 127.0.0.1]: chat.congty.com
Nhập cổng máy chủ [mặc định: 12345]: 8080
✅ Sẽ kết nối tới chat.congty.com:8080
```

**Ưu điểm**:
- ✅ Kết nối đến máy chủ bất kỳ (LAN/Internet)
- ✅ Tự động xác thực (IP, tên miền, dải cổng)  
- ✅ Hỗ trợ giá trị mặc định (nhấn Enter)
- ✅ Thích hợp cho máy chủ production

**Các định dạng địa chỉ hỗ trợ**:
- **IP cục bộ**: `192.168.1.100`, `10.0.0.5`
- **Localhost**: `127.0.0.1`, `localhost`
- **Tên miền**: `chat.example.com`, `server.local`
- **IP công khai**: `203.0.113.1`

## 👤 Thiết Lập Biệt Danh

### Quy tắc biệt danh:
```
✅ Được phép:
- Chữ cái: a-z, A-Z  
- Số: 0-9
- Ký tự đặc biệt: _ (gạch dưới), - (gạch ngang)
- Độ dài: 1-20 ký tự

❌ Không được phép:
- Ký tự đặc biệt khác: @, #, $, %, v.v.
- Khoảng trắng
- Biệt danh trống
- Quá 20 ký tự
```

### Ví dụ biệt danh hợp lệ:
```
✅ "Nam123"      ✅ "chat_user"    ✅ "Player-One"
✅ "admin"       ✅ "user_2024"    ✅ "TestUser"
✅ "a"           ✅ "ABC_XYZ"      ✅ "dev-team"
```

### Ví dụ biệt danh không hợp lệ:
```
❌ "user name"           (có khoảng trắng)
❌ "user@domain"         (có ký tự @)  
❌ "user#123"            (có ký tự #)
❌ ""                    (trống)
❌ "very_long_username_over_limit"  (quá dài)
```

## 💬 Gửi Tin Nhắn

### Tin nhắn hợp lệ:
- **Độ dài**: 2-500 ký tự
- **Nội dung**: Bất kỳ văn bản nào (sau khi lọc)
- **Ngôn ngữ**: Tiếng Việt, Tiếng Anh, Unicode

### Hệ thống lọc nội dung:

#### 🚫 Từ ngữ không phù hợp
```bash
# Ví dụ tin nhắn bị lọc:
Bạn gõ: "Xin chào loz mọi người"
Hiển thị: "⚠️ Cảnh báo: Đã lọc từ không phù hợp: loz"
Gửi đi: "Xin chào *** mọi người"
```

#### 🔁 Chống spam
```bash
# Các mẫu bị từ chối:
❌ "aaaaaaaaa"          (lặp ký tự)
❌ "XIN CHÀO MỌI NGƯỜI" (quá nhiều chữ hoa)
❌ "Hế lô!!!!!!!"       (quá nhiều dấu chấm than)
❌ "###@@@$$$"          (chỉ ký tự đặc biệt)
```

#### ✅ Tin nhắn bình thường
```bash
✅ "Xin chào mọi người!"
✅ "Hôm nay thế nào?"
✅ "Có ai online không?"
✅ "Thanks! 😊"
```

### Lệnh đặc biệt:
```bash
quit    # Thoát khỏi ứng dụng
exit    # Thoát khỏi ứng dụng  
```

## 🎯 Các Tình Huống Sử Dụng

### 🏢 Sử dụng trong văn phòng/công ty
```bash
# 1. Khởi chạy ứng dụng
python3 run_client.py

# 2. Chọn tự động quét mạng LAN
Chọn phương thức (1/2): 1

# 3. Chờ tìm máy chủ công ty
# 4. Chọn máy chủ từ danh sách
# 5. Đặt biệt danh (vd: "nguyen_van_a")
# 6. Bắt đầu chat với đồng nghiệp
```

### 🏠 Sử dụng tại nhà/mạng gia đình
```bash
# Kết nối đến máy chủ gia đình
Nhập địa chỉ máy chủ: 192.168.1.5
Nhập cổng máy chủ: 12345
```

### 🌐 Kết nối máy chủ từ xa (Internet)
```bash
# Kết nối qua Internet
Nhập địa chỉ máy chủ: chat.mydomain.com
Nhập cổng máy chủ: 443
```

### 🧪 Kiểm tra/phát triển
```bash
# Kết nối localhost để test
Nhập địa chỉ máy chủ: localhost  
Nhập cổng máy chủ: 12345
```

## 🔧 Xử Lý Sự Cố

### 🚨 Các lỗi thường gặp:

#### "Không tìm thấy máy chủ nào"
**Nguyên nhân**: Tự động quét không tìm thấy máy chủ
**Giải pháp**:
1. Chọn "Nhập thủ công"
2. Kiểm tra kết nối mạng
3. Đảm bảo máy chủ đang chạy
4. Thử với địa chỉ IP cụ thể

#### "Kết nối bị từ chối"  
**Nguyên nhân**: Máy chủ không chạy hoặc cổng sai
**Giải pháp**:
1. Kiểm tra máy chủ có đang chạy không
2. Xác thực địa chỉ và cổng
3. Kiểm tra tường lửa/firewall
4. Thử cổng khác (8080, 3000, 9999)

#### "Biệt danh không hợp lệ"
**Nguyên nhân**: Biệt danh vi phạm quy tắc
**Giải pháp**:
1. Chỉ sử dụng chữ, số, _, -
2. Không dùng khoảng trắng
3. Độ dài 1-20 ký tự
4. Không để trống

#### "Tin nhắn bị từ chối"
**Nguyên nhân**: Vi phạm quy tắc nội dung
**Giải pháp**:
1. Tránh từ ngữ thô tục
2. Không lặp ký tự (aaaa)
3. Hạn chế chữ hoa
4. Độ dài 2-500 ký tự

#### "Quét mạng quá chậm"
**Nguyên nhân**: Mạng lớn hoặc chậm
**Giải pháp**:
1. Đợi thêm 30-60 giây
2. Nhấn Ctrl+C để hủy
3. Chọn "Nhập thủ công"
4. Kiểm tra kết nối WiFi/mạng

## 📱 Giao Diện Người Dùng

### Biểu tượng và ý nghĩa:
```
🚀 - Khởi chạy/bắt đầu
🔍 - Đang tìm kiếm/quét
✅ - Thành công
❌ - Lỗi/thất bại  
⚠️ - Cảnh báo
💬 - Tin nhắn chat
👤 - Biệt danh/người dùng
🔗 - Kết nối
📡 - Mạng/kết nối
⏱️ - Thời gian/timeout
👋 - Chào/tạm biệt
```

### Màu sắc (nếu terminal hỗ trợ):
- **Xanh lá**: Thành công, kết nối OK
- **Đỏ**: Lỗi, thất bại
- **Vàng**: Cảnh báo, chú ý
- **Xanh dương**: Thông tin, hướng dẫn

## 🎓 Mẹo Sử Dụng

### Cho người mới:
1. **Luôn chọn "Tự động quét" trước** - dễ nhất cho người mới
2. **Đặt biệt danh đơn giản** - vd: "user1", "nam", "test_user"  
3. **Thử tin nhắn ngắn trước** - vd: "hello", "xin chào"
4. **Đọc cảnh báo kỹ** - hệ thống sẽ hướng dẫn khi có lỗi

### Cho người dùng nâng cao:
1. **Ghi nhớ địa chỉ máy chủ thường dùng** - tiết kiệm thời gian
2. **Sử dụng biệt danh nhất quán** - dễ nhận biết
3. **Kiểm tra log nếu có vấn đề** - debug hiệu quả
4. **Thử các cổng khác nhau** - 8080, 3000, 9999 nếu 12345 bận

### Bảo mật:
1. **Không chia sẻ thông tin nhạy cảm** trong chat
2. **Sử dụng biệt danh không tiết lộ thông tin cá nhân**
3. **Chỉ kết nối đến máy chủ tin tưởng**
4. **Báo cáo hành vi không phù hợp** nếu thấy

## 🔄 Quy Trình Chat Hoàn Chỉnh

```
1. 🚀 Khởi chạy: python3 run_client.py
2. 🌐 Chọn phương pháp kết nối (tự động/thủ công)
3. 🔍 Tìm/nhập thông tin máy chủ
4. 🔗 Kết nối đến máy chủ  
5. 👤 Đặt biệt danh hợp lệ
6. 💬 Bắt đầu chat
7. 📝 Gửi tin nhắn (có lọc nội dung)
8. 👋 Gõ "quit" để thoát
```

---

**Chúc bạn có những trải nghiệm chat vui vẻ! 🎉**

*Nếu gặp vấn đề, hãy tham khảo phần [Xử lý sự cố](#-xử-lý-sự-cố) hoặc liên hệ hỗ trợ kỹ thuật.*
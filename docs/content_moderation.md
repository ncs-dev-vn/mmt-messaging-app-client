# Content Moderation Features

## 🛡️ Tính năng kiểm duyệt nội dung

Chat client được trang bị hệ thống kiểm duyệt nội dung toàn diện để đảm bảo môi trường chat an toàn và văn minh.

## 🔧 Các tính năng chính

### 1. **Lọc từ ngữ không phù hợp**
- Tự động phát hiện và lọc từ thô tục, chửi bậy
- Thay thế bằng dấu sao (*) hoặc từ chối hoàn toàn
- Hỗ trợ cả tiếng Việt và tiếng Anh
- Có thể tùy chỉnh danh sách từ cấm

### 2. **Chống spam**
- Phát hiện tin nhắn lặp lại ký tự (aaaa, !!!!, ????)
- Giới hạn chữ hoa liên tục
- Phát hiện tin nhắn chỉ toàn ký tự đặc biệt
- Kiểm tra độ dài tin nhắn hợp lý

### 3. **Rate limiting (Giới hạn tần suất)**
- Tối đa 5 tin nhắn trong 30 giây (có thể cấu hình)
- Tự động chặn khi gửi quá nhanh
- Thông báo thời gian chờ còn lại

### 4. **Validation cơ bản**
- Tin nhắn không được để trống
- Giới hạn độ dài tối đa (mặc định 500 ký tự)
- Kiểm tra tin nhắn có ý nghĩa (ít nhất 2 ký tự)

## ⚙️ Cấu hình

### File `config/client_config.ini`:
```ini
[moderation]
enable_content_filter = true        # Bật/tắt lọc nội dung
max_messages_per_window = 5         # Số tin nhắn tối đa
message_rate_window = 30            # Khung thời gian (giây)
allow_inappropriate_words = false   # Cho phép từ không phù hợp (test)
filter_spam = true                  # Bật lọc spam

[client]
max_message_length = 500            # Độ dài tin nhắn tối đa
```

## 🚦 Các mức độ xử lý

### ✅ **Chấp nhận**
- Tin nhắn bình thường, văn minh
- Có emoji vừa phải
- Độ dài hợp lý

### ⚠️ **Cảnh báo + Lọc**
- Có 1-2 từ không phù hợp → Thay bằng dấu sao
- Người dùng nhận cảnh báo
- Tin nhắn vẫn được gửi sau khi lọc

### ❌ **Từ chối hoàn toàn**
- Quá nhiều từ không phù hợp (≥3)
- Tin nhắn spam (lặp ký tự, chữ hoa)
- Quá dài hoặc quá ngắn
- Gửi quá nhanh (rate limit)

## 📊 Thống kê và theo dõi

Hệ thống theo dõi:
- Số lần cảnh báo của user
- Thời gian gửi tin nhắn (cho rate limiting)
- Thống kê nội dung tin nhắn

## 🎯 Demo và Testing

### 1. **Chạy demo tổng thể:**
```bash
python3 examples/content_moderation_demo.py
```

### 2. **Test interactive:**
```bash
python3 examples/test_content_filter.py
```

### 3. **Test từng function:**
```python
from utils import validate_message_content

# Test tin nhắn bình thường
result = validate_message_content("Hello world!")
print(result)  # (True, 'Hello world!', 'OK')

# Test tin nhắn không phù hợp
result = validate_message_content("dm vcl")
print(result)  # (False, '', 'Tin nhắn chứa quá nhiều từ ngữ không phù hợp...')
```

## 🛠️ API Reference

### `validate_message_content(message)`
**Args:**
- `message` (str): Tin nhắn cần kiểm tra

**Returns:**
- `tuple`: `(is_valid, filtered_message, reason)`
  - `is_valid`: True nếu tin nhắn hợp lệ
  - `filtered_message`: Tin nhắn sau khi lọc
  - `reason`: Lý do từ chối hoặc cảnh báo

### `validate_message_frequency(message_times, max_messages, time_window)`
**Args:**
- `message_times` (list): Danh sách thời gian gửi tin nhắn
- `max_messages` (int): Số tin nhắn tối đa
- `time_window` (int): Khung thời gian (giây)

**Returns:**
- `tuple`: `(is_allowed, reason)`

### `clean_message_display(message)`
**Args:**
- `message` (str): Tin nhắn gốc

**Returns:**
- `str`: Tin nhắn đã làm sạch cho hiển thị an toàn

## 🔒 Bảo mật

### Các biện pháp bảo vệ:
1. **Input sanitization**: Loại bỏ ký tự điều khiển
2. **Length limiting**: Giới hạn độ dài để tránh buffer overflow
3. **Rate limiting**: Chống spam và DOS
4. **Content filtering**: Lọc nội dung độc hại

### Không lưu trữ:
- Không log nội dung tin nhắn
- Chỉ lưu metadata (thời gian, số lần cảnh báo)
- Không lưu thông tin cá nhân

## 🎛️ Tùy chỉnh

### Thêm từ khóa cấm:
```python
# Trong utils/__init__.py
INAPPROPRIATE_WORDS = [
    # Thêm từ mới vào đây
    'từ_cấm_mới',
    'inappropriate_word',
]
```

### Thay đổi spam patterns:
```python
# Trong utils/__init__.py
SPAM_PATTERNS = [
    r'(.)\1{4,}',     # Lặp lại 5+ lần
    r'[!?]{3,}',      # 3+ dấu cảm thán
    r'[A-Z]{10,}',    # 10+ chữ hoa liên tục
    # Thêm pattern mới...
]
```

## 💡 Best Practices

### Cho developers:
1. Test content moderation trước khi deploy
2. Monitor false positives và điều chỉnh
3. Cung cấp feedback rõ ràng cho users
4. Cho phép appeal/report các quyết định sai

### Cho users:
1. Sử dụng ngôn từ văn minh, tích cực
2. Tránh lặp lại ký tự không cần thiết
3. Không gửi tin nhắn quá nhanh
4. Báo cáo nếu hệ thống lọc nhầm

---

**🎉 Hệ thống content moderation giúp tạo môi trường chat an toàn và thân thiện cho mọi người!**
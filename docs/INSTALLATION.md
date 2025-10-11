# Installation Guide

## 📋 Yêu cầu hệ thống

### Minimum Requirements
- **Python:** 3.7+
- **OS:** Windows 10, macOS 10.14+, Linux (Ubuntu 18.04+)
- **RAM:** 512MB
- **Disk:** 50MB free space

### Recommended
- **Python:** 3.9+
- **RAM:** 1GB+
- **Network:** Stable internet connection

## 🚀 Cài đặt

### Phương pháp 1: Download & Run
```bash
# Download source code
git clone <repository-url>
cd mmt-messaging-app-client

# Run trực tiếp (không cần install dependencies)
python main.py
```

### Phương pháp 2: Virtual Environment (Khuyên dùng)
```bash
# Tạo virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run application
python main.py
```

### Phương pháp 3: System-wide
```bash
# Install dependencies (nếu có)
pip install -r requirements.txt

# Run application
python main.py
```

## 🔧 Cấu hình đầu tiên

1. **Chạy ứng dụng lần đầu:**
   ```bash
   python main.py
   ```

2. **Chọn phương thức kết nối:**
   - Option 1: Auto-scan LAN
   - Option 2: Manual input

3. **Nhập server info (nếu chọn manual):**
   ```
   Host: 127.0.0.1 (localhost)
   Port: 12345 (default)
   ```

## ✅ Kiểm tra cài đặt

```bash
# Test import modules
python -c "
import sys
sys.path.insert(0, 'src')
from client.chat_client import ChatClient
print('✅ Installation successful!')
"
```

## 🐛 Troubleshooting

### Lỗi Python không tìm thấy
```bash
# Kiểm tra Python version
python --version
python3 --version

# Sử dụng python3 nếu cần
python3 main.py
```

### Lỗi Module not found
```bash
# Kiểm tra cấu trúc thư mục
ls -la src/
ls -la src/client/

# Đảm bảo đang ở đúng thư mục
pwd
```

### Lỗi Permission denied (macOS/Linux)
```bash
# Add execute permission
chmod +x main.py

# Run with python explicitly
python main.py
```
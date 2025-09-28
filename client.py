import socket
import threading
import sys

# Khai báo hằng số cho server
HOST = '127.0.0.1'
PORT = 12345

# Tạo socket cho client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối tới server
try:
    client.connect((HOST, PORT))
    print('Đã kết nối thành công với Server.')
except socket.error as e:
    print(f"Lỗi: Không thể kết nối tới server. Lỗi: {e}")
    sys.exit()

# Nhập nickname từ người dùng
nickname = input("Nhập nickname của bạn: ").strip()
if not nickname:
    print('Nickname không được để trống.')
    sys.exit(1)
client.send(nickname.encode('utf-8'))

# Hàm để nhận tin nhắn từ server
def receive_messages():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print('Bạn đã mất kết nối với Server.')
                break
            message = data.decode('utf-8')
            print(message)
        except Exception:
            print('Bạn đã mất kết nối với Server.')
            break

# Luồng chính: gửi tin nhắn liên tục
def write_message():
    while True:
        try:
            message = input('')
            if message.strip().lower() in ['quit', 'exit']:
                print('Đang ngắt kết nối...')
                client.close()
                sys.exit(0)
            elif message.strip():
                # Gửi tin nhắn thông thường
                client.send(message.encode('utf-8'))
                # In lại tin nhắn của mình để người dùng thấy
                # Lưu ý: Tin nhắn này sẽ chỉ hiển thị ở máy của bạn
                # Những người khác sẽ thấy tin nhắn được server broadcast lại
                print(f"{nickname}: {message}")
            else:
                print('Không gửi tin nhắn rỗng.')
        except Exception:
            print('Không thể gửi tin nhắn. Đã mất kết nối với Server.')
            break

# Bắt đầu luồng nhận tin nhắn và luồng gửi tin nhắn
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True # Luồng sẽ tự thoát khi chương trình chính kết thúc
receive_thread.start()

write_message()
import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Server đang lắng nghe...')

conn, addr = server_socket.accept()
print('Kết nối từ:', addr)

nickname = conn.recv(1024).decode()
print(f'Nickname: {nickname}')

while True:
    try:
        message = conn.recv(1024)
        if not message:
            print('Client đã ngắt kết nối.')
            break
        msg_text = message.decode()
        print(f'{nickname}: {msg_text}')
        # Phản hồi lại client
        conn.send(f'{nickname}, bạn vừa gửi: {msg_text}'.encode())
    except Exception as e:
        print('Lỗi:', e)
        break

conn.close()
server_socket.close()
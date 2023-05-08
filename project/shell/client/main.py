import socket
import pickle

def recv_all(client_socket):
    data = bytearray()
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        data.extend(chunk)
        if data.endswith(b'ENDOFDATA'):
            data = data[:-9]
            break
    return data

def send_all(client_socket, data):
    data += b'ENDOFDATA'
    while data:
        bytes_sent = client_socket.send(data)
        data = data[bytes_sent:]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))

while True:
    username = 'secreu'
    function = input("请输入要发送的功能（功能1或功能2）：")
    data = input("请输入要发送的数据：")
    message = {'username': username, 'function': function, 'data': data}
    serialized_data = pickle.dumps(message)
    send_all(client_socket, serialized_data)

    response_data = recv_all(client_socket)
    response = pickle.loads(response_data)
    print("收到来自服务端的响应:", response)

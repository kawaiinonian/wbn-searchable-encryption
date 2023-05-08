import socket
import threading
import pickle

from server.consts import *
from server.c_server import *

def save_dict(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def read_dict(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

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

def send_all(client_socket: socket, data: bytes):
    data += b'ENDOFDATA'
    while data:
        bytes_sent = client_socket.send(data)
        data = data[bytes_sent:]

def handle_client(client_socket):
    while True:
        try:
            data = recv_all(client_socket)
            if not data:
                break
            message = pickle.loads(data)
            username = message['username']

            if message['function'] == 'ADD':
                tmp = message['data']
                try:
                    XSETS[username] = XSETS[username].items | tmp
                    re = 'Success'
                except Exception as e:
                    re = 'Error: ' + e
                response = {'username': username, 'function': 'ADD', 'data': re}
            elif message['function'] == 'ONLINE':
                tmp = message['data']
                try:
                    USETS[username] = USETS[username].items | tmp
                    re = 'Success'
                except Exception as e:
                    re = 'Error: ' + e
                response = {'username': username, 'function': 'ONLINE', 'data': re}
            elif message['function'] == 'OFFLINE':
                tmp = message['data']
                try:
                    c_svr.Aset_update(ASETS[username], tmp['aid'], tmp['alpha', tmp['aidA']])
                    re = 'Success'
                except Exception as e:
                    re = 'Error: ' + e
                response = {'username': username, 'function': 'OFFLINE', 'data': re}
            elif message['function'] == 'SEARCH':
                tmp = message['data']
                try:
                    token = tmp['token']
                    aid = tmp['aid']
                    re = c_svr.search(token, aid, USETS[username], ASETS[username], XSETS[username])
                except Exception as e:
                    re = 'Error: ' + e
                response = {'username': username, 'function': 'SEARCH', 'data': re}
            elif message['function'] == 'UPLOAD':
                response = '处理功能2的结果: ' + message['data']
            elif message['function'] == 'DOWNLOAD':
                response = '处理功能2的结果: ' + message['data']
            else:
                response = '未知功能: ' + message['data']

            serialized_data = pickle.dumps(response)
            send_all(client_socket, serialized_data)

        except Exception as e:
            print(f"客户端断开连接: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

if __name__ == "__main__": 
    libserver = "/home/secreu/wbn-searchable-encryption/project/core/libserver.so"
    c_svr = c_server(libserver)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen()

    clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

import socket
import threading
import pickle

import sys
import os
sys.path.append(os.getcwd() + "/project/shell/")

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
            if not data or message['dst'] != server:
                break
            message = pickle.loads(data)
            user_id = message['src']

            # Add
            if message['function'] == 'ADD':
                tmp = message['data']
                try:
                    XSETS[user_id] = XSETS[user_id].items | tmp
                    re = 'Success'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'ADD', 'data': re}

            # OnlineAuth
            elif message['function'] == 'ONLINE':
                tmp = message['data']
                try:
                    USETS[user_id] = USETS[user_id].items | tmp
                    re = 'Success'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'ONLINE', 'data': re}
            
            # OfflineAuth
            elif message['function'] == 'OFFLINE':
                tmp = message['data']
                try:
                    c_svr.Aset_update(ASETS[user_id], tmp['aid'], tmp['alpha', tmp['aidA']])
                    re = 'Success'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'OFFLINE', 'data': re}

            # Search
            elif message['function'] == 'SEARCH':
                tmp = message['data']
                try:
                    token = tmp['token']
                    aid = tmp['aid']
                    re = c_svr.search(token, aid, USETS[user_id], ASETS[user_id], XSETS[user_id])
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'SEARCH', 'data': re}

            # Upload Files
            elif message['function'] == 'UPLOAD':
                response = '处理功能2的结果: ' + message['data']

            # Download Files
            elif message['function'] == 'DOWNLOAD':
                response = '处理功能2的结果: ' + message['data']

            else:
                re = 'Error: What do you want to do?'
                response = {'src': server, 'dst': user_id, 'function': '', 'data': re}

            serialized_data = pickle.dumps(response)
            send_all(client_socket, serialized_data)

        except Exception as e:
            print(f"Client disconnects: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

if __name__ == "__main__": 
    server = "wbn"
    host = "127.0.0.1"
    port = 12345

    libserver = "/home/secreu/wbn-searchable-encryption/project/core/libserver.so"
    c_svr = c_server(libserver)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server begins listening on {host}: {port}")

    clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f"Client connects: {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

import socket
import pickle

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
SERVER_NAME = 'wbn'

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


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    # while True:
    username = 'secreu'
    server = 'wbn'
    function = 'ADD'
    data = {b'123': b'123'}
    message = {'src': username, 'dst': SERVER_NAME, 'function': function, 'data': data}
    serialized_data = pickle.dumps(message)
    send_all(client_socket, serialized_data)

    response_data = recv_all(client_socket)
    response = pickle.loads(response_data)
    print("Receive from server:", response)

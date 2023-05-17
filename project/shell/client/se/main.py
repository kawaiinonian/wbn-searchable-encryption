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


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))
    # while True:
    user_id = 'secreu'
    server = 'wbn'
    function = 'ADD'
    data = {b'123': b'123'}
    message = {'src': user_id, 'dst': server, 'function': function, 'data': data}
    serialized_data = pickle.dumps(message)
    send_all(client_socket, serialized_data)

    response_data = recv_all(client_socket)
    response = pickle.loads(response_data)
    print("Receive from server:", response)

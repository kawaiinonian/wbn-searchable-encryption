import socket
import threading
import pickle
import signal
import os
from datetime import datetime

from c_server import *
from mytree import *

XSETS = {}
USETS = {}
ASETS = {}

def save_pkl(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def read_pkl(path):
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
    global XSETS
    global USETS
    global ASETS

    while True:
        try:
            data = recv_all(client_socket)
            message = pickle.loads(data)
            if not data or message['dst'] != server:
                break
            user_id = message['src']

            # Add
            if message['function'] == 'ADD':
                print(f"[{datetime.now()}] 收到来自 <{user_id}> 的 <文件上传> 请求")
                tmp = message['data']
                try:
                    XSETS |= tmp[0]

                    print(f"[{datetime.now()}] 文件信息表 <XSET> 新增以下内容:")
                    print("-" * 20)
                    for key, value in tmp[0].items():
                        print(f'|<Xwd> {key}')
                        print(f'|<Ywd> {value}')
                        print("-" * 20)

                    if tmp[1] is not None:
                        path = 'enc_files/' + list(tmp[0].values())[0].replace(b'\x00', b'').decode('utf-8', errors='replace').replace('/', '')
                        # 存储加密的文件内容到本地文件
                        with open(path, 'wb') as f:
                            f.write(tmp[1])

                    re = 'SUCCESS'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'ADD', 'data': re}

            # Delete
            elif message['function'] == 'DELETE':
                print(f"[{datetime.now()}] 收到来自 <{user_id}> 的 <文件更新> 请求")
                tmp = message['data']
                try:
                    value_to_remove = list(tmp.values())[0]
                    removed_items = [(key, value) for key, value in XSETS.items() if value == value_to_remove]
                    print(f"[{datetime.now()}] 文件信息表 <XSET> 删除以下内容:")
                    print("-" * 20)
                    for (key, value) in removed_items:
                        print(f'|<Xwd> {key}')
                        print(f'|<Ywd> {value}')
                        print("-" * 20)
                        if key in XSETS.keys():
                            XSETS.pop(key)

                    re = 'SUCCESS'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'DELETE', 'data': re}

            # OnlineRevo
            elif message['function'] == 'ONLINEREVO':
                print(f"[{datetime.now()}] 收到来自 <{user_id}> 的 <撤销在线授权> 请求")
                (tmp, edge_list) = message['data']
                try:
                    keys_to_remove = tmp.keys()
                    removed_items = [(key, value) for key, value in USETS.items() if key in keys_to_remove]
                    print(f"[{datetime.now()}] DO-DU授权关系表 <USET> 删除以下内容:")
                    print("-" * 20)
                    for (key, value) in removed_items:
                        print(f'|<uid> {key}')
                        print(f'|<Ud>  {value}')
                        print("-" * 20)
                        if key in USETS.keys():
                            USETS.pop(key)

                    forest = build_forest(edge_list)
                    print("授权树变更为:")
                    for tree_id, root, edges in forest:
                        root_node = TreeNode(root)
                        print_tree(tree_id, root_node, edges)
                        print("\n" + "-" * 20)

                    re = 'SUCCESS'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'ONLINEREVO', 'data': re}

            # OfflineRevo
            elif message['function'] == 'OFFLINEREVO':
                print(f"[{datetime.now()}] 收到来自 <{user_id}> 的 <撤销离线授权> 请求")
                (tmp, edge_list) = message['data']
                try:
                    keys_to_remove = [tmp['aid']]
                    print(f"[{datetime.now()}] DU间授权关系表 <ASET> 删除以下键值:")
                    print("-" * 20)
                    while len(keys_to_remove) > 0:
                        dkeys = []
                        removed_items = []
                        for key, value in ASETS.items():
                            if key in keys_to_remove:
                                removed_items.append(key)
                                dkeys = list(set(dkeys + value.dlist))
                        
                        for key in removed_items:
                            if key in ASETS.keys():
                                print(f"|<aid> {key}")
                                print("-" * 20)
                                ASETS.pop(key)

                        keys_to_remove = dkeys
                    
                    forest = build_forest(edge_list)
                    print("授权树变更为:")
                    for tree_id, root, edges in forest:
                        root_node = TreeNode(root)
                        print_tree(tree_id, root_node, edges)
                        print("\n" + "-" * 20)

                    re = 'SUCCESS'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'OFFLINEREVO', 'data': re}

            # OnlineAuth
            elif message['function'] == 'ONLINE':
                print(f"[{datetime.now()}] 收到来自 <{user_id}> 的 <在线授权> 请求")
                (tmp, edge_list) = message['data']
                try:
                    USETS |= tmp

                    print(f"[{datetime.now()}] DO-DU授权信息表 <USET> 新增以下内容:")
                    print("-" * 20)
                    for key, value in tmp.items():
                        print(f'|<uid> {key}')
                        print(f'|<Ud>  {value}')
                        print("-" * 20)                   

                    forest = build_forest(edge_list)
                    print("授权树变更为:")
                    for tree_id, root, edges in forest:
                        root_node = TreeNode(root)
                        print_tree(tree_id, root_node, edges)
                        print("\n" + "-" * 20)

                    re = 'SUCCESS'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'ONLINE', 'data': re}
            
            # OfflineAuth
            elif message['function'] == 'OFFLINE':
                print(f"[{datetime.now()}] 收到来自 <{user_id}> 的 <离线授权> 请求")
                (tmp, edge_list) = message['data']
                try:
                    c_svr.Aset_update(ASETS, tmp['aid'], tmp['alpha'], tmp['aidA'])

                    print(f"[{datetime.now()}] DU间授权信息表 <ASET> 新增以下内容:")
                    print("-" * 20) 
                    print(f"|<aid> {tmp['aid']}")
                    print(f"|<alp> {tmp['alpha']}")
                    print("-" * 20) 

                    forest = build_forest(edge_list)
                    print("授权树变更为:")
                    for tree_id, root, edges in forest:
                        root_node = TreeNode(root)
                        print_tree(tree_id, root_node, edges)
                        print("\n" + "-" * 20)

                    re = 'SUCCESS'
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'OFFLINE', 'data': re}

            # Search
            elif message['function'] == 'SEARCH':
                print(f"[{datetime.now()}] 收到来自 <{user_id}> 的 <搜索> 请求")
                tmp = message['data']
                try:
                    token = tmp['token']
                    print(f"> 用户令牌:")
                    print("-" * 20) 
                    for (uid, stk) in token:
                        print(f'|<uid> {uid}')
                        print(f'|<stk> {stk}')
                        print("-" * 20)  
                    aid = tmp['aid']
                    if aid is not None:
                        print(f"> 用户离线授权索引:")
                        print("-" * 20) 
                        print(f"|<aid> {aid}")
                        print("-" * 20) 
                    re = c_svr.search(token, aid, USETS, ASETS, XSETS)
                    print("> 搜索结果:")
                    print("-" * 20) 
                    for (idx, ywd) in re:
                        print(f'|<idx> {idx}')
                        print(f'|<Ywd> {ywd}')
                        print("-" * 20)  
                except Exception as e:
                    re = f'Error: {e}'
                response = {'src': server, 'dst': user_id, 'function': 'SEARCH', 'data': re}

            else:
                re = 'Error: What do you want to do?'
                response = {'src': server, 'dst': user_id, 'function': '', 'data': re}

            serialized_data = pickle.dumps(response)
            send_all(client_socket, serialized_data)

        except Exception as e:
            print(f"[{datetime.now()}] 客户端断开连接: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

def handle_quit(signum, frame):
    global XSETS
    global USETS
    global ASETS

    try:
        print(f"[{datetime.now()}] Quiting......")
        while True:
            if not clients:
                if XSETS:
                    save_pkl(xPath, XSETS)
                if USETS:
                    save_pkl(uPath, USETS)
                if ASETS:
                    save_pkl(aPath, ASETS)
                exit(0)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    server = "wbn"
    host = "127.0.0.1"
    port = 12345

    libserver = "./libserver.so"
    c_svr = c_server(libserver)

    xPath = "sets/xsets.pkl"
    uPath = "sets/usets.pkl"
    aPath = "sets/asets.pkl"

    if os.path.exists(xPath):
        XSETS = read_pkl(xPath)
    if os.path.exists(uPath):
        USETS = read_pkl(uPath)
    if os.path.exists(aPath):
        ASETS = read_pkl(aPath)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[{datetime.now()}] 服务端监听于 {host}: {port}")

    clients = []

    signal.signal(signal.SIGINT, handle_quit)

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f"[{datetime.now()}] 客户端连接: {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

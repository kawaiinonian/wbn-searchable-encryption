import socket
import pickle
import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import JsonResponse
from mycloud import models

from se.skt import recv_all, send_all, SERVER_HOST, SERVER_PORT, SERVER_NAME
from se.datatype import LAMBDA, SEARCH_KEY, USER_KEY, USER_AUTH, DOC_KEY
from se.method import get_fd, get_key_from_bytes, get_d_from_bytes, get_element_from_bytes, get_word_from_bytes
from se.c_user import c_user
cusr = c_user('se/libclient.so')

from cryptography.fernet import Fernet
import base64

# 生成或使用固定的密钥，确保密钥长度为 32 个字节
SECRET = 'CrazyThursdayVme50'.encode()
SECRET_KEY = base64.urlsafe_b64encode(SECRET.ljust(32))
# 创建 Fernet 加密对象
fernet = Fernet(SECRET_KEY)

# Create your views here.


@login_required
@csrf_exempt
def upload(request):
    response = {}
    documents = models.Documents.objects.filter(user=request.user)
    response["documents"] = [d.doc for d in documents]
    response['username'] = request.user.username
    return render(request, "upload.html", response)


@login_required
@csrf_exempt
def delete(request):
    response = {}
    if request.method == 'POST':
        fun = 'DELETE'
        user = request.user
        username = user.username
        skey = models.SKey.objects.get(user=user)
        sk = SEARCH_KEY(
            get_key_from_bytes(skey.sk1), 
            get_key_from_bytes(skey.sk2), 
            get_key_from_bytes(skey.sk3)
        )
        documents = request.POST.get('documents')

        print(documents)

        vv = [b'0']
        file = [get_fd(vv, bytes(username.encode()).ljust(LAMBDA) + bytes(documents.encode()).ljust(LAMBDA))]

        print(sk)
        print(file)

        xset, num = cusr.updateData_generate(sk, file)
        xset = {bytes(x.xwd): bytes(x.ywd) for x in xset}

        print(xset)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = {'src': username, 'dst': SERVER_NAME, 'function': fun, 'data': xset}
        serialized_data = pickle.dumps(message)
        send_all(client_socket, serialized_data)
        res_data = recv_all(client_socket)
        res = pickle.loads(res_data)
        client_socket.close()

        print(res)

        response['error'] = '1'
        if res['data'] == 'SUCCESS':
            doc = models.Documents.objects.get(user=user, doc=documents)
            doc.delete()
            response['error'] = '0'
        response['msg'] = res['data']

        return JsonResponse(response)

@login_required
@csrf_exempt
def get_usernames(request):
    response = {}
    if request.method == 'GET':
        users = User.objects.all()
        usernames = [u.username for u in users]
        response['usernames'] = usernames
        return JsonResponse(response)


@login_required
@csrf_exempt
def search(request):
    response = {}
    if request.method == 'POST':
        fun = 'SEARCH'
        word = request.POST.get('word')
        if not word:
            return JsonResponse({'msg': '请提供检索的关键词', 'error': '1'})
        
        print(word)

        word = get_word_from_bytes(bytes(word.encode()))
        user = request.user
        username = user.username
        ukey = models.UKey.objects.get(user=user)
        uk = USER_KEY(
            get_key_from_bytes(ukey.uk1),
            get_key_from_bytes(ukey.uk2)
        )
        userauth = models.UsrAuth.objects.filter(user=user)
        if userauth is None:
            userauth = []
        else:
            userauth = [USER_AUTH(
                    get_d_from_bytes(o.d),
                    get_key_from_bytes(o.uid),
                    get_element_from_bytes(o.offtok)
                ) for o in userauth]
        dk = models.DocKey.objects.filter(user=user)

        for i in dk:
            print(i.id)
            print(i.d.decode())
            
        dockey = [DOC_KEY(
                get_d_from_bytes(d.d), 
                get_key_from_bytes(d.kdenc), 
                get_key_from_bytes(d.kd)
            ) for d in dk]

        ret_token, dockey = cusr.search_generate(word, uk, dockey, userauth)
        token = [(bytes(t.uid), bytes(t.stk)) for t in ret_token]
        key_dec = [{
            'd': bytes(k.d),
            'kdenc': bytes(k.kd_enc),
            'kd': bytes(k.kd)
        } for k in dockey]
        
        try:
            user_aid = models.Aid.objects.get(user=user)
            aid = user_aid.aid
        except:
            aid = None

        data = {'token': token, 'aid': aid}

        print(data)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = {'src': username, 'dst': SERVER_NAME, 'function': fun, 'data': data}
        serialized_data = pickle.dumps(message)
        send_all(client_socket, serialized_data)
        res_data = recv_all(client_socket)
        res = pickle.loads(res_data)
        client_socket.close()

        print(res['data'])

        documents = []
        for (i, ywd) in res['data']:
            print(i)
            print(key_dec[i]['d'])
            kdenc = key_dec[i]['kdenc']
            d = cusr.dec_ywd(kdenc, ywd)
            d = d.decode()
            documents.append(d)

        print(documents)
        
        response['documents'] = documents
        response['error'] = '0'
        if res['data'][:5] == 'Error':
            response['error'] = '1'
            response['msg'] = res['data']

        if len(documents) == 0 and response['error'] == '0':
            response['error'] = '1'
            response['msg'] = '没有匹配的文件'

        print(response)

        return JsonResponse(response)
    
    return render(request, "search.html", response)


@login_required
@csrf_exempt
def add(request):
    response = {}
    if request.method == 'POST':
        fun = 'ADD'
        user = request.user
        username = user.username
        skey = models.SKey.objects.get(user=user)
        sk = SEARCH_KEY(
            get_key_from_bytes(skey.sk1), 
            get_key_from_bytes(skey.sk2), 
            get_key_from_bytes(skey.sk3)
        )

        documents = request.POST.get('documents')
        documents = json.loads(documents)
        if 'file' in request.FILES:
            f = request.FILES['file']
            enc_f = fernet.encrypt(f.read())
        else:
            f = None
            enc_f = None

        print(documents)

        file = []
        k = list(documents.keys())[0]
        v = list(documents.values())[0]
        vv = []
        for w in v:
            if w != '':
                vv.append(bytes(w.encode()))
        file.append(get_fd(vv, bytes(username.encode()).ljust(LAMBDA) + bytes(k.encode()).ljust(LAMBDA)))
        doc = models.Documents.objects.create(user=user, doc=k)
        if f is not None:
            doc.file = f
        doc.save()
        
        print(sk)
        print(file)

        xset, num = cusr.updateData_generate(sk, file)
        xset = {bytes(x.xwd): bytes(x.ywd) for x in xset}

        print(xset)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = {'src': username, 'dst': SERVER_NAME, 'function': fun, 'data': (xset, enc_f)}
        serialized_data = pickle.dumps(message)
        send_all(client_socket, serialized_data)
        res_data = recv_all(client_socket)
        res = pickle.loads(res_data)
        client_socket.close()

        print(res)

        response['error'] = '1'
        if res['data'] == 'SUCCESS':
            response['error'] = '0'
        response['msg'] = res['data']

        return JsonResponse(response)


@login_required
@csrf_exempt
def online_revo(request):
    response = {}
    if request.method == 'GET':
        user = request.user
        ats = models.Auth.objects.filter(userA=user, authtype=0)
        usernames = []
        for a in ats:
            ubn = a.userB.username
            if ubn not in usernames:
                usernames.append(ubn)
        response['usernames'] = usernames
        print(usernames)
        return JsonResponse(response)
    
    elif request.method == 'POST':
        tar_name = request.POST.get('username')
        tar_user = User.objects.get(username=tar_name)
        if tar_user is None:
            return JsonResponse({'msg': '目标用户不存在', 'error': '1'})

        fun = 'ONLINEREVO'
        user = request.user
        username = user.username

        ats = models.Auth.objects.filter(userA=user, userB=tar_user, authtype=0)
        documents = []
        for a in ats:
            dd = a.doc
            if dd not in documents:
                documents.append(dd)
            a.delete()

        queue = [tar_user]
        while len(queue) > 0:
            usera = queue.pop(0)
            ats = models.Auth.objects.filter(userA=usera)
            for a in ats:
                userb = a.userB
                if userb not in queue:
                    queue.append(userb)
                a.delete()

        print(username)
        print(documents)
        
        skey = models.SKey.objects.get(user=user)
        sk = SEARCH_KEY(
            get_key_from_bytes(skey.sk1),
            get_key_from_bytes(skey.sk2),
            get_key_from_bytes(skey.sk3)
        )
        ukey = models.UKey.objects.get(user=tar_user)
        uk = USER_KEY(
            get_key_from_bytes(ukey.uk1),
            get_key_from_bytes(ukey.uk2)
        )

        doc = [bytes(username.encode()).ljust(LAMBDA) + bytes(d.encode()).ljust(LAMBDA) for d in documents]
        dockey, uset = cusr.online_auth(sk, uk, doc)
        uset = {bytes(u.uid): bytes(u.ud) for u in uset}

        print(dockey)
        print(uset)

        edge_dict = {}
        ats = models.Auth.objects.all()
        for a in ats:
            edge = (a.userA.username, a.userB.username)
            if a.doc in edge_dict:
                edge_dict[a.doc].append(edge)
            else:
                edge_dict[a.doc] = [edge]

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = {'src': username, 'dst': SERVER_NAME, 'function': fun, 'data': (uset, edge_dict)}
        serialized_data = pickle.dumps(message)
        send_all(client_socket, serialized_data)
        res_data = recv_all(client_socket)
        res = pickle.loads(res_data)
        client_socket.close()

        response['error'] = '1'
        if res['data'] == 'SUCCESS':
            response['error'] = '0'
        response['msg'] = res['data']

        return JsonResponse(response)


@login_required
@csrf_exempt
def offline_revo(request):
    response = {}
    if request.method == 'GET':
        user = request.user
        ats = models.Auth.objects.filter(userA=user, authtype=1)
        usernames = []
        for a in ats:
            ubn = a.userB.username
            if ubn not in usernames:
                usernames.append(ubn)
        response['usernames'] = usernames
        print(usernames)
        return JsonResponse(response)

    elif request.method == 'POST':
        tar_name = request.POST.get('username')
        tar_user = User.objects.get(username=tar_name)
        if tar_user is None:
            return JsonResponse({'msg': '目标用户不存在', 'error': '1'})

        fun = 'OFFLINEREVO'
        user = request.user
        username = user.username
        aida = None
        
        at = models.Auth.objects.get(userA=user, userB=tar_user, authtype=1)
        documents = at.doc
        at.delete()

        queue = [tar_user]
        while len(queue) > 0:
            usera = queue.pop(0)
            ats = models.Auth.objects.filter(userA=usera)
            for a in ats:
                userb = a.userB
                if userb not in queue:
                    queue.append(userb)
                a.delete()

        documents = documents.split( )
        doc = [bytes(documents[0].encode()).ljust(LAMBDA) + bytes(documents[1].encode()).ljust(LAMBDA)]

        print(doc)

        ub = get_key_from_bytes(bytes(tar_name.encode()))
        ukey1 = models.UKey.objects.get(user=user)
        uk1 = USER_KEY(
            get_key_from_bytes(ukey1.uk1),
            get_key_from_bytes(ukey1.uk2)
        )
        ukey2 = models.UKey.objects.get(user=tar_user)
        uk2 = USER_KEY(
            get_key_from_bytes(ukey2.uk1),
            get_key_from_bytes(ukey2.uk2)
        )
        userauth = models.UsrAuth.objects.filter(user=user)
        if userauth is None:
            userauth = []
        else:
            userauth = [USER_AUTH(
                    get_d_from_bytes(o.d),
                    get_key_from_bytes(o.uid),
                    get_element_from_bytes(o.offtok)
                ) for o in userauth]
        dockey = models.DocKey.objects.filter(user=user)
        dockey = [DOC_KEY(
                get_d_from_bytes(d.d), 
                get_key_from_bytes(d.kdenc), 
                get_key_from_bytes(d.kd)
            ) for d in dockey]

        aset, ret_auth, ret_key = cusr.offline_auth(uk1, uk2, doc, ub, dockey, userauth)

        print(aset.contents.aid)

        edge_dict = {}
        ats = models.Auth.objects.all()
        for a in ats:
            edge = (a.userA.username, a.userB.username)
            if a.doc in edge_dict:
                edge_dict[a.doc].append(edge)
            else:
                edge_dict[a.doc] = [edge]

        data = {'aid': bytes(aset.contents.aid), 'alpha': bytes(aset.contents.trapgate), 'aidA': aida}
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = {'src': username, 'dst': SERVER_NAME, 'function': fun, 'data': (data, edge_dict)}
        serialized_data = pickle.dumps(message)
        send_all(client_socket, serialized_data)
        res_data = recv_all(client_socket)
        res = pickle.loads(res_data)
        client_socket.close()

        response['error'] = '1'
        if res['data'] == 'SUCCESS':
            response['error'] = '0'
        response['msg'] = res['data']

        return JsonResponse(response)


@login_required
@csrf_exempt
def online_auth(request):
    response = {}
    if request.method == 'POST':
        tar_name = request.POST.get('username')
        tar_user = User.objects.get(username=tar_name)
        if tar_user is None:
            return JsonResponse({'msg': '目标用户不存在', 'error': '1'})

        fun = 'ONLINE'
        user = request.user
        username = user.username
        documents = request.POST.get('documents')

        print(username)
        print(documents)
        
        skey = models.SKey.objects.get(user=user)
        sk = SEARCH_KEY(
            get_key_from_bytes(skey.sk1),
            get_key_from_bytes(skey.sk2),
            get_key_from_bytes(skey.sk3)
        )
        ukey = models.UKey.objects.get(user=tar_user)
        uk = USER_KEY(
            get_key_from_bytes(ukey.uk1),
            get_key_from_bytes(ukey.uk2)
        )

        # doc = [bytes(username).ljust(LAMBDA) + bytes(d).ljust(LAMBDA) for d in documents]
        doc = [bytes(username.encode()).ljust(LAMBDA) + bytes(documents.encode()).ljust(LAMBDA)]
        dockey, uset = cusr.online_auth(sk, uk, doc)
        uset = {bytes(u.uid): bytes(u.ud) for u in uset}

        print(dockey)
        print(uset)
        
        for key in dockey:
            dk = models.DocKey.objects.create(
                user = tar_user,
                d = bytes(key.d),
                kd = bytes(key.kd),
                kdenc = bytes(key.kd_enc)
            )
            dk.save()
        at = models.Auth.objects.create(
            userA = user,
            userB = tar_user,
            authtype = 0,
            doc = documents
        )
        at.save()

        edge_dict = {}
        ats = models.Auth.objects.all()
        for a in ats:
            edge = (a.userA.username, a.userB.username)
            if a.doc in edge_dict:
                edge_dict[a.doc].append(edge)
            else:
                edge_dict[a.doc] = [edge]

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = {'src': username, 'dst': SERVER_NAME, 'function': fun, 'data': (uset, edge_dict)}
        serialized_data = pickle.dumps(message)
        send_all(client_socket, serialized_data)
        res_data = recv_all(client_socket)
        res = pickle.loads(res_data)
        client_socket.close()

        response['error'] = '1'
        if res['data'] == 'SUCCESS':
            response['error'] = '0'
        response['msg'] = res['data']

        return JsonResponse(response)


@login_required
@csrf_exempt
def offline_auth(request):
    response = {}
    if request.method == 'POST':
        tar_name = request.POST.get('username')
        tar_user = User.objects.get(username=tar_name)
        if tar_user is None:
            return JsonResponse({'msg': '目标用户不存在', 'error': '1'})

        fun = 'OFFLINE'
        user = request.user

        try:
            user_aid = models.Aid.objects.get(user=user)
            aida = user_aid.aid
        except:
            aida = None

        username = user.username
        document = request.POST.get('documents')
        documents = document.split( )
        # doc = [bytes(username).ljust(LAMBDA) + d.ljust(LAMBDA) for d in documents]
        doc = [bytes(documents[0].encode()).ljust(LAMBDA) + bytes(documents[1].encode()).ljust(LAMBDA)]
        print(doc)
        ub = get_key_from_bytes(bytes(tar_name.encode()))
        ukey1 = models.UKey.objects.get(user=user)
        uk1 = USER_KEY(
            get_key_from_bytes(ukey1.uk1),
            get_key_from_bytes(ukey1.uk2)
        )
        ukey2 = models.UKey.objects.get(user=tar_user)
        uk2 = USER_KEY(
            get_key_from_bytes(ukey2.uk1),
            get_key_from_bytes(ukey2.uk2)
        )
        userauth = models.UsrAuth.objects.filter(user=user)
        if userauth is None:
            userauth = []
        else:
            userauth = [USER_AUTH(
                    get_d_from_bytes(o.d),
                    get_key_from_bytes(o.uid),
                    get_element_from_bytes(o.offtok)
                ) for o in userauth]
        dockey = models.DocKey.objects.filter(user=user)
        dockey = [DOC_KEY(
                get_d_from_bytes(d.d), 
                get_key_from_bytes(d.kdenc), 
                get_key_from_bytes(d.kd)
            ) for d in dockey]

        aset, ret_auth, ret_key = cusr.offline_auth(uk1, uk2, doc, ub, dockey, userauth)

        at = models.Auth.objects.create(
            userA = user,
            userB = tar_user,
            authtype = 1,
            doc = documents[1]
        )
        at.save()
        ad = models.Aid.objects.create(
            user = tar_user,
            aid = bytes(aset.contents.aid)
        )
        ad.save()
        for key in ret_key:
            dk = models.DocKey.objects.create(
                user = tar_user,
                d = bytes(key.d),
                kd = bytes(key.kd),
                kdenc = bytes(key.kd_enc)
            )
            dk.save()
        for auth in ret_auth:
            au = models.UsrAuth.objects.create(
                user = tar_user,
                d = bytes(auth.d),
                uid = bytes(auth.uid),
                offtok = bytes(auth.offtok)
            )
            au.save()

        edge_dict = {}
        ats = models.Auth.objects.all()
        for a in ats:
            edge = (a.userA.username, a.userB.username)
            if a.doc in edge_dict:
                edge_dict[a.doc].append(edge)
            else:
                edge_dict[a.doc] = [edge]

        data = {'aid': bytes(aset.contents.aid), 'alpha': bytes(aset.contents.trapgate), 'aidA': aida}
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = {'src': username, 'dst': SERVER_NAME, 'function': fun, 'data': (data, edge_dict)}
        serialized_data = pickle.dumps(message)
        send_all(client_socket, serialized_data)
        res_data = recv_all(client_socket)
        res = pickle.loads(res_data)
        client_socket.close()

        response['error'] = '1'
        if res['data'] == 'SUCCESS':
            response['error'] = '0'
        response['msg'] = res['data']

        return JsonResponse(response)


@csrf_exempt
def register_login(request):
    response = {}
    if request.method == 'POST':
        type = request.POST.get('type')
        if type == '0':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username or not password:
                response['msg'] = '请提供用户名和密码'
                response['error'] = '1'
                return JsonResponse(response)
            obj_user = User.objects.filter(username=username).first()
            if obj_user:
                response['msg'] = '用户已存在'
                response['error'] = '1'
                return JsonResponse(response)
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )
                user.save()
                obj_user = User.objects.get(username=username)
                skey = models.SKey.objects.create(
                    user = obj_user,
                    sk1 = cusr.gen_key(),
                    sk2 = cusr.gen_key(),
                    sk3 = cusr.gen_key()
                )
                skey.save()
                ukey = models.UKey.objects.create(
                    user = obj_user,
                    uk1 = cusr.gen_key(),
                    uk2 = cusr.gen_key()
                )
                ukey.save()
                login(request, user)
                response['msg'] = '用户注册成功'
                response['error'] = '0'
                response['redirect'] = '/search/'
                return JsonResponse(response)
        elif type == '1':
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = authenticate(request, username=username, password=password)
                if user is None:
                    return JsonResponse({'error': '1', 'msg': '用户名或密码错误'})
                login(request, user)
                response['msg'] = 'success'
                response['error'] = '0'
                response['redirect'] = '/search/'
            except Exception as e:
                print(e)
                response['msg'] = '用户名或密码错误'
                response['error'] = '1'
            return JsonResponse(response)
    return render(request, "register_login.html", response)


@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'redirect': '/register_login/'})


@login_required
def update_password(request):
    response = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        try:
            obj_user = User.objects.get(username=username, password=old_password)
            obj_user.password = new_password
            obj_user.save()
            response['msg'] = 'success'
            response['error'] = '0'
        except Exception as e:
            response['msg'] = f'用户id或原密码错误: {e}'
            response['error'] = '1'
    return render(request, "register_login.html", response)


def greet(request):
    response = {}
    response['msg'] = 'Hello!'
    return render(request, "index.html", response)


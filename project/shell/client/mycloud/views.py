import socket
import pickle

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction
from mycloud import models

from se.skt import recv_all, send_all, SERVER_HOST, SERVER_PORT, SERVER_NAME
from se.datatype import LAMBDA, SEARCH_KEY
from se.method import get_fd
from se.c_user import c_user
cusr = c_user('se/libclient.so')

# Create your views here.

@login_required
@csrf_exempt
def search(request):
    response = {}
    if request.method == 'POST':
        pass
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
        sk = SEARCH_KEY(skey.sk1, skey.sk2, skey.sk3)
        documents = request.POST.get('documents')
        
        file = []
        for k, v in documents.items():
            file.append(get_fd(v, bytes(username).ljust(LAMBDA) + bytes(k).ljust(LAMBDA)))
        xset, num = cusr.updateData_generate(sk, file)
        xset = {bytes(x.xwd): bytes(x.ywd) for x in xset}

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message = {'src': username, 'dst': SERVER_NAME, 'function': fun, 'data': xset}
        serialized_data = pickle.dumps(message)
        send_all(client_socket, serialized_data)
        res_data = recv_all(client_socket)
        res = pickle.loads(res_data)

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
        user = request.user

    return render(request, "search.html", response)


@login_required
@csrf_exempt
def offline_auth(request):
    response = {}
    if request.method == 'POST':
        pass
    return render(request, "search.html", response)


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
            print(username)
            print(password)
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


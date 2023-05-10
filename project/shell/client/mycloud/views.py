from django.shortcuts import render
import hashlib
from django.http import JsonResponse
from django.db import transaction
from mycloud import models

# Create your views here.

def greet(request):
    response = {}
    name = request.GET.get('name')
    response['msg'] = 'Hello! ' + name
    return JsonResponse(response)


def register(request):
    response = {}
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        user_list = models.USERS.objects.filter(username=username)
        if user_list:
            response['msg'] = '用户名已经存在'
            response['error_num'] = 1
            response['redirect'] = 'register'   # 转入register
        else:
            down = models.USERS.objects.order_by('-userid')
            if down:
                userid = down[0].userid + 1
            else:
                userid = 100001
            user = models.USERS.objects.create(
                userid=userid,
                user_name=username,
                password=password
            )
            user.save()
            response['userid'] = userid
            response['msg'] = 'success'
            response['error_num'] = 0
            response['redirect'] = 'login'      # 转入login
    return JsonResponse(response)


def login(request):
    response = {}
    if request.method == 'GET':
        userid = request.GET.get('userid')
        password = request.GET.get('password')
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        try:
            obj_user = models.USERS.objects.get(userid=userid, password=password)
            response['msg'] = 'success'
            response['error_num'] = 0
            response['redirect'] = 'home'  # 转入home界面
        except Exception as e:
            response['msg'] = f'用户id或密码错误: {e}'
            response['error_num'] = 1
    return JsonResponse(response)


def update_password(request):
    response = {}
    if request.method == 'GET':
        userid = request.GET.get('userid')
        old_password = request.GET.get('old_password')
        new_password = request.GET.get('new_password')
        hl1 = hashlib.md5()
        hl1.update(old_password.encode(encoding='utf-8'))
        old_password = hl1.hexdigest()
        hl2 = hashlib.md5()
        hl2.update(new_password.encode(encoding='utf-8'))
        new_password = hl2.hexdigest()
        try:
            obj_user = models.USERS.objects.get(userid=userid, password=old_password)
            obj_user.password = new_password
            obj_user.save()
            response['msg'] = 'success'
            response['error_num'] = 0
            response['redirect'] = 'login'      # 重新登陆
        except Exception as e:
            response['msg'] = f'用户id或原密码错误: {e}'
            response['error_num'] = 1
            response['redirect'] = 'home'
    return JsonResponse(response)


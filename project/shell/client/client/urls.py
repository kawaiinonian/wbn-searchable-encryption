"""
URL configuration for client project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth import urls
from django.contrib import admin
from django.urls import path
from mycloud import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('greet/', views.greet),
    path('', views.register_login),
    path('register_login/', views.register_login),
    path('search/', views.search),
    path('upload/', views.upload),
    path('add/', views.add),
    path('get_usernames/', views.get_usernames),
    path('online_auth/', views.online_auth),
    path('offline_auth/', views.offline_auth),
    path('delete/', views.delete),
    path('online_revo/', views.online_revo),
    path('offline_revo/', views.offline_revo),
]

# 添加处理媒体文件的URL模式
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

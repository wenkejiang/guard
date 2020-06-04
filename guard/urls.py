"""guard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import views
from rest_framework_jwt.views import obtain_jwt_token

from users.views import *
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
# 配置注册的URL
router.register('register',UserRegViewset,basename='register')

# # 获取用户信息
# router.register('getInfo',UserViewset,basename='getInfo')

urlpatterns = [
    url(r'', include(router.urls)),
    #创建API文档
    url(r'docs/', include_docs_urls(title="测试平台")),
    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),
    # 获取用户信息
    url(r'^getInfo/', UserViewset.as_view({'get': 'retrieve'})),
    # 获取用户列表
    url(r'^getUserList/', UserViewset.as_view({'get': 'list'})),

    url(r'^deleteUser/', UserViewset.as_view(
        {'post': 'destroy'})),

]


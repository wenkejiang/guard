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
from rest_framework_jwt.views import obtain_jwt_token

from monitor.views import JobViewset, GitInfoViewset, ScriptViewset
from users.views import *
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# 配置注册的URL
router.register('register', UserRegViewset, basename='register')

# # Job信息
router.register('job', JobViewset, basename='monitorJob')

# # 获取git信息
router.register('getUrl', GitInfoViewset, basename='getUrl')

urlpatterns = [
    url(r'', include(router.urls)),
    # 创建API文档
    url(r'docs/', include_docs_urls(title="测试平台")),
    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),
    # 获取用户信息
    url(r'^getInfo/', UserViewset.as_view({'get': 'retrieve'})),
    # 获取用户列表
    url(r'^getUserList/', UserViewset.as_view({'get': 'list'})),

    # 获取git info数据入库
    url(r'^gitInfo/', GitInfoViewset.as_view({'get': 'git_info'}), name="gitInfo"),

    # 获取项目 info数据入库
    url(r'^projectInfo/', GitInfoViewset.as_view({'get': 'project_info'}), name="projectInfo"),

    url(r'^start_script/', ScriptViewset.as_view({'post': 'start_script'}), name="start_script"),

    url(r'^stop_script/', ScriptViewset.as_view({'get': 'stop_script'}), name="stop_script"),



    url(r'^deleteUser/', UserViewset.as_view(
        {'post': 'destroy'})),

]

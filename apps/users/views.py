import logging
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from users.serializers import UserRegSerializer, UserDetailSerializer
logger = logging.getLogger("log")


# Create your views here.

User = get_user_model()

class UserRegViewset(viewsets.ModelViewSet):
    """
    用户注册
    """
    queryset = User.objects.all()
    serializer_class = UserRegSerializer

class UserViewset(viewsets.ModelViewSet):
    """
    用户信息
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    filter_fields = ('username', 'name')


    def get_object(self):
        return self.request.user
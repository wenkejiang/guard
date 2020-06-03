import logging
# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.mixins import CreateModelMixin
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from users.serializers import UserRegSerializer, UserDetailSerializer

from utils.APIResponse import APIResponse

logger = logging.getLogger("log")

User = get_user_model()

class UserViewset(CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    queryset = User.objects.all()
    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list" :
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    def get_permissions(self):
        if self.action == "retrieve" or self.action == "list":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        logger.info("注册结果:{val}".format(val=re_dict))
        return APIResponse(200,"注册成功！",re_dict,status=status.HTTP_200_OK,headers=headers)


    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return APIResponse(200, "获取用户信息成功！", serializer.data, status=status.HTTP_200_OK, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        headers = self.get_success_headers(serializer.data)

        return APIResponse(200, "获取用户列表成功！", serializer.data, status=status.HTTP_200_OK, headers=headers)

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
User = get_user_model()



class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ("id", "name", "date_joined", "username",  "email")

class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
    ),
    password1 = serializers.CharField(
        style={'input_type': 'password'},help_text="确认密码", label="确认密码", write_only=True,
    )

    def validate(self, attrs):
        if attrs['password1'] != attrs['password']:
            raise ValidationError('两次密码输入不一致')
        del attrs['password1']
        # 对密码进行加密 make_password
        attrs['password'] = make_password(attrs['password'])
        return attrs


    class Meta:
        model = User
        fields = ("username", "email", "name","password","password1")

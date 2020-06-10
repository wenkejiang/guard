# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/6   
# 修改时间: 11:12 上午   
# IDE: PyCharm
from rest_framework import serializers

from monitor.models import Job, Git


class GitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Git
        fields = ("system",)

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

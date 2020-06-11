from datetime import datetime

from django.db import models


# Create your models here.

class Git(models.Model):
    """
    git项目和git地址
    """
    author = models.CharField(max_length=255, verbose_name="git作者")
    project_id = models.IntegerField(verbose_name="项目ID")
    system = models.CharField(max_length=255, default='', verbose_name="项目名称")
    git_url = models.CharField(max_length=255, verbose_name="Git_URL")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = 'git信息维护表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.system


class Job(models.Model):
    system = models.CharField(max_length=255, verbose_name="监控系统")
    job_name = models.CharField(max_length=255, verbose_name="任务名称")
    job_args = models.CharField(max_length=255, verbose_name="脚本地址")
    job_corn = models.CharField(max_length=255, verbose_name="脚本表达式")
    status = models.IntegerField('启用/禁用', default=0)
    author = models.CharField(max_length=255, verbose_name="作者")
    warning = models.CharField(max_length=255, verbose_name="警告人")
    env = models.CharField(max_length=255, default='qa')
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    def __str__(self):
        return self.job_name

    class Meta:
        verbose_name = "调度任务信息"
        verbose_name_plural = verbose_name
        ordering = ['-id']


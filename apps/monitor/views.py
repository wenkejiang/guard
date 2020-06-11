import datetime
import logging

from apscheduler.triggers.cron import CronTrigger
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from monitor.models import Job, Git
from monitor.operation.gitInfo import GitInfo
from monitor.operation.runJob import JobRunner
from monitor.operation.scriptFromGit import Script
from monitor.serializers import JobSerializer, GitSerializer
from utils.scheduler import scheduler

logger = logging.getLogger('log')

class JobViewset(viewsets.ModelViewSet):

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_fields = ('job_name', 'system', 'author')




class GitInfoViewset(viewsets.ModelViewSet):
    queryset = Git.objects.all()
    serializer_class = GitSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def git_info(self,request, *args, **kwargs):
        mgs = GitInfo().save_git_info()
        return Response(data=mgs)

    def project_info(self, request, *args, **kwargs):
        params = request.query_params
        mgs = GitInfo().get_project(params.get('groups_name'), params.get('project_name'))
        return Response(data=mgs)

class ScriptViewset(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def script(self, request, *args, **kwargs):
        """
        拉取数据，本地有就git pull 本地没有就git clone
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        params = request.data
        job_id = params.get('id')
        warning = params.get('warning')
        system = params.get('system')
        job_name = params.get('job_name')
        job_args = params.get('job_args')
        job_corn = params.get('job_corn')
        env = params.get('env')
        logger.info("----------开始拉取gitlab上的项目，有则更新，无则clone-------------")
        mgs = Script().get_script(system) # 拉取项目到本地
        logger.info("----------结束拉取gitlab上的项目，有则更新，无则clone-------------")

        try:
            if mgs:
                logger.info("----------开始调度执行任务-------------")
                scheduler.add_job(func=JobRunner().run, id=str(job_id), args=[system, warning, job_args, job_name, env],
                                  trigger=CronTrigger.from_crontab(job_corn), next_run_time=datetime.datetime.now(),
                                  replace_existing=True)
                Job.objects.filter(id=job_id).update(status='1')
                logger.info("----------调度执行任务完毕！执行成功-------------")
                return Response(data="调度执行成功")
            else:
                return Response(data="项目拉取失败,调度未执行")
        except Exception as e:
            logger.error(e)
            return Response(data="调度执行失败")










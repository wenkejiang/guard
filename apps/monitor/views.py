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

    def update(self, request, *args, **kwargs):
        try:
            info = request.data
            print(info)
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            # 只有运行中的调度需要更新，否则更新本地记录就可以
            logger.info("判断是否为启用的任务")
            job_obj = Job.objects.get(id=info["id"])
            if job_obj.status == 1:
                logger.info("--------------开始更新和执行任务------------------")
                scheduler.add_job(func=JobRunner().run, id=str(info["id"]),
                                  args=[info["system"], info["warning"], info["job_args"], info["job_name"], info["env"]],
                                  trigger=CronTrigger.from_crontab(info["job_corn"]), next_run_time=datetime.datetime.now(),
                                  replace_existing=True)
                logger.info("--------------更新和执行任务完成------------------")
            return Response(serializer.data)
        except Exception as e:
            logger.error(e)
            return Response("更新失败")



def perform_update(self, serializer):
    serializer.save()


def partial_update(self, request, *args, **kwargs):
    kwargs['partial'] = True
    return self.update(request, *args, **kwargs)


class GitInfoViewset(viewsets.ModelViewSet):
    queryset = Git.objects.all()
    serializer_class = GitSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def git_info(self, request, *args, **kwargs):
        mgs = GitInfo().save_git_info()
        return Response(data=mgs)

    def project_info(self, request, *args, **kwargs):
        params = request.query_params
        mgs = GitInfo().get_project(params.get('groups_name'), params.get('project_name'))
        return Response(data=mgs)


class ScriptViewset(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def start_script(self, request, *args, **kwargs):
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
        mgs = Script().get_script(system)  # 拉取项目到本地
        logger.info("----------结束拉取gitlab上的项目，有则更新，无则clone-------------")

        try:
            if mgs:
                logger.info("----------开始调度执行任务-------------")
                scheduler.add_job(func=JobRunner().run, id=str(job_id), args=[system, warning, job_args, job_name, env],
                                  trigger=CronTrigger.from_crontab(job_corn), next_run_time=datetime.datetime.now(),
                                  replace_existing=True)
                Job.objects.filter(id=job_id).order_by('id').update(status=1)
                logger.info("----------调度执行任务完毕！执行成功-------------")
                return Response(data="调度执行成功")
            else:
                return Response(data="项目拉取失败,调度未执行")
        except Exception as e:
            logger.error(e)
            return Response(data="调度执行失败")

    def stop_script(self, request, *args, **kwargs):
        try:
            params = request.query_params
            job_id = params.get('id')
            print(job_id)
            if scheduler.get_job(job_id=job_id):
                scheduler.remove_job(str(job_id))
            Job.objects.filter(id=job_id).order_by('id').update(status=0)
            logger.info("job_id={job_id}调度任务停止成功".format(job_id=job_id))
            return Response(data="调度任务停止成功")
        except Exception as e:
            logger.error(e)
            return Response(data="调度任务停止报错")





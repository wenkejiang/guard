from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from monitor.auto_operation.autoGitInfo import GitInfo
from monitor.models import Job, Git
from monitor.serializers import JobSerializer, GitSerializer

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






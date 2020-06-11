# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/11   
# 修改时间: 10:19 上午   
# IDE: PyCharm
import logging
import os

from guard import settings
from monitor.models import Git
from utils.gitUtil import Git_Cmd
logger = logging.getLogger('log')


class Script(object):

    def find_script(self, project_name):
        """
        传入项目名称，在本地的文件夹中查找该文件，存在返回true 不存在返回false
        :return: true
        """
        projects = os.listdir(settings.script_path)
        if project_name in projects:
            return True  # 存在
        else:
            return False  # 不存在

    def get_script(self, project_name):
        sgin = self.find_script(project_name)
        logger.info("本地是否存在项目:{val}".format(val=sgin))
        if self.find_script(project_name):
            logger.info("---------开始执行git pull操作---------------")
            script_projrct_path = settings.script_path + '/' + project_name
            git = Git_Cmd()
            git.get_pull_project(script_projrct_path, project_name)
            logger.info("---------执行git pull操作成功---------------")
            return True
        else:
            try:
                logger.info("---------开始执行git clone操作---------------")
                obj = Git.objects.get(system=project_name)
                project_path = obj.git_url
                git = Git_Cmd()
                git.get_clone_project(project_path, project_name)
                logger.info("---------执行git clone结束---------------")
                return True
            except Exception as e:
                logger.error("---------执行git clone报错---------------")
                logger.error(e)


if __name__ == "__main__":
    script = Script()
    print(script.find_script())

# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/6   
# 修改时间: 11:28 上午   
# IDE: PyCharm
import json
import logging
import os

import requests
import subprocess

from utils.utils import Utils

logger = logging.getLogger('log')

from guard import settings


class Git_Utils(object):
    """
    git地址接口
    通过API形式调用gitlab
    """

    def __init__(self, groups_id=settings.GROUPS_ID, private_token=settings.PRIVATE_TOKEN, groups_name=None,
                 project_name=None):
        self.groups_id = groups_id
        self.git_url = 'http://git.iqdnet.cn'
        self.private_token = private_token
        self.groups_name = groups_name
        self.project_name = project_name

    def get_git_info(self):
        """
        获取分组下的所有的项目名称和URL
        :return:
        """
        url_arg = '/api/v4/groups/{group_id}/projects?private_token={private_token}&simple=true'.format(
            group_id=self.groups_id, private_token=self.private_token)
        url = self.git_url + url_arg
        logger.info(url)
        response = requests.get(url=url)
        return json.loads(response.text)

    def get_project_info(self):
        """
        获取项目下的所有的文件
        :return:
        """
        url_arg = '/{groups_name}/{project_name}/files/master?format=json&private_token={private_token}'.format(
            groups_name=self.groups_name, project_name=self.project_name, private_token=self.private_token)
        url = self.git_url + url_arg
        logger.info(url)
        response = requests.get(url=url)
        return json.loads(response.text)


git_info = Git_Utils(groups_id=settings.GROUPS_ID, private_token=settings.PRIVATE_TOKEN)


class Git_Cmd(object):
    """
    执行git命令操作
    1.git pull
    2.git clone
    """

    def __init__(self, script_path=None, project_name=None, project_path=None, cmd=None):
        self.script_path = script_path
        self.project_name = project_name
        self.project_path = project_path
        self.cmd = cmd
        self.script_projrct_path = script_path+'/'+project_path

    def get_clone_project(self):
        try:
            os.chdir(self.script_path)
        except Exception as e:
            raise Exception(e)
        util = Utils()
        util.run_cmd('git clone {git}'.format(git=self.project_path))
        logger.info("本地没有，clone调度{val}成功！".format(val=self.project_name))

    def get_pull_project(self):
        """
        从git拉取项目文件到本地, 强制覆盖本地文件
        :param script_path: 本地存放脚本路径
        :param project_name: 项目名称
        :return:
        """
        try:
            os.chdir(self.script_projrct_path)
        except Exception as e:
            raise Exception(e)
        try:
            util = Utils()
            util.run_cmd("git fetch --all")
            util.run_cmd('git reset --hard origin/master')
            util.run_cmd('git pull')

            logger.info('已获取最新用例, 脚本路径：{path}'.format(path=self.project_name))
        except Exception as e:
            logger.error('执行git命令异常: {e}'.format(e=e))


if __name__ == "__main__":
    project_info = Git_Utils(groups_name="qa_automation", project_name="qding-merchant-cloud-test",
                             private_token=settings.PRIVATE_TOKEN)
    print(project_info.get_project_info())

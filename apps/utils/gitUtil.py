# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/6   
# 修改时间: 11:28 上午   
# IDE: PyCharm
import json
import logging

import requests
logger = logging.getLogger('log')

from guard import settings


class Git_Utils(object):
    """
    git地址接口
    """
    def __init__(self, groups_id=settings.GROUPS_ID, private_token=settings.PRIVATE_TOKEN, groups_name=None, project_name=None):
        self.groups_id = groups_id
        self.git_url = 'http://git.iqdnet.cn'
        self.private_token = private_token
        self.groups_name = groups_name
        self.project_name = project_name



    def get_git_info(self):
        url_arg = '/api/v4/groups/{group_id}/projects?private_token={private_token}&simple=true'.format(
            group_id=self.groups_id, private_token=self.private_token)
        url = self.git_url + url_arg
        logger.info(url)
        response = requests.get(url=url)
        return json.loads(response.text)

    def get_project_info(self):
        url_arg = '/{groups_name}/{project_name}/files/master?format=json&private_token={private_token}'.format(
            groups_name=self.groups_name, project_name=self.project_name, private_token=self.private_token)
        url = self.git_url + url_arg
        logger.info(url)
        response = requests.get(url=url)
        return json.loads(response.text)
git_info = Git_Utils(groups_id=settings.GROUPS_ID, private_token=settings.PRIVATE_TOKEN)


if __name__ == "__main__":
    project_info = Git_Utils(groups_name="qa_automation",project_name="qding-merchant-cloud-test",private_token=settings.PRIVATE_TOKEN)
    print(project_info.get_project_info())

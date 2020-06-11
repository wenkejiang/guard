# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/6   
# 修改时间: 12:02 下午   
# IDE: PyCharm
import logging

from monitor.models import Git
from utils.gitUtil import git_info, Git_Utils

logger = logging.getLogger('log')


class GitInfo(object):
    def save_git_info(self):
        infos = git_info.get_git_info()
        try:
            for info in infos:
                Git.objects.update_or_create(project_id=info['id'],
                                             defaults={'project_id': info['id'], 'system': info['name'],
                                                       'git_url': info['http_url_to_repo']})
            logger.info("保存git信息成功")
            return "保存git信息成功"
        except Exception as e:
            logger.error(e)
            logger.error("保存git信息报错")

    def get_project(self, groups_name, project_name):
        project = []
        project_info = Git_Utils(groups_name=groups_name, project_name=project_name)
        infos = project_info.get_project_info()
        for info in infos:
            if info.startswith("testcases") or info.startswith("testsuites"):
                project.append(info)
        print(project)
        return project


if __name__ == "__main__":
    project_info = GitInfo()
    print(project_info.get_project("qa_automation","qding-merchant-cloud-test"))

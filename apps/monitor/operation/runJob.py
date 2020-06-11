# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/11   
# 修改时间: 1:41 下午   
# IDE: PyCharm
import datetime
import logging
import os

from httprunner.api import HttpRunner

from guard import settings
from utils.resultUtil import Result
from utils.weChat import wechat

logger = logging.getLogger('log')

class JobRunner(object):

    def run(self, project_name, touser, script, job_name, env=None):
            runner = HttpRunner()
            script_project_path = settings.script_path + '/' + project_name
            os.chdir(script_project_path) # 切换到项目目录下
            try:
                if env:
                    env_path =  script_project_path + "/env/{val}.env".format(val=env)
                    result = runner.run(script, dot_env_path=env_path)
                else:
                    result = runner.run(script)
                failed_info = Result().get_failed_info(result, project_name, settings.target_path)
                Result().send_warning(failed_info, touser, project_name, job_name)
            except FileNotFoundError:
                msg = "**应用接口监控告警: {suite_name}**\n脚本名称: {job_name}\n异常信息: {stat}". \
                    format(suite_name=project_name, job_name=job_name, stat='脚本路径不存在, 请确认脚本是否上传git')
                wechat.send_message(msg, touser)
            except Exception as e:
                msg = "**应用接口监控告警: {suite_name}**\n脚本名称: {job_name}\n异常信息: {stat}". \
                    format(suite_name=project_name, job_name=job_name, stat=e)
                wechat.send_message(msg, touser)
                logger.error('执行目录{path}测试失败：{e}'.format(path=script, e=e))
            logger.info('job end at: {time}'.format(time=datetime.datetime.now()))


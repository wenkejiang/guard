# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/10   
# 修改时间: 6:45 下午   
# IDE: PyCharm
import logging
import subprocess

logger = logging.getLogger('log')

class Utils(object):


    def run_cmd(self, cmd):
        """
        cmd运行命令
        :return:
        """
        result = subprocess.getstatusoutput(cmd)
        if result[0] == 0:
            logger.info('执行shell命令成功：{shell}'.format(shell=cmd))
            return result[1]
        else:
            logger.error('执行shell命令异常: {cmd}'.format(cmd=cmd))

if __name__ == "__main__":
    u = Utils()
    print(u.run_cmd(""))

# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/11   
# 修改时间: 2:24 下午   
# IDE: PyCharm
import logging

from httprunner.report import gen_html_report

from utils.weChat import wechat
logger = logging.getLogger('log')


class Result(object):

    def get_failed_info(self, result, system, target_path):
        """
        获取失败用例
        :param target_path:
        :param system:
        :param result:
        :return:    脚本 xxx 运行结果异常：
        stat:{
                    "total":6,
                    "failures":2,
                    "errors":2,
                    "skipped":0,
                    "expectedFailures":0,
                    "unexpectedSuccesses":0,
                    "successes":2}
        详情请查看报告：xxxxx.html
        """
        failed_info = {}
        warning_tobe_send = {}
        if result['success'] is False:
            warning_tobe_send['result'] = result['stat']['testcases']

        failed_info['project_name'] = system
        failed_info['warning_tobe_send'] = warning_tobe_send
        if len(warning_tobe_send) > 0:
            failed_info['report_path'] = '{report_path}'.format(
                report_path=gen_html_report(result, report_dir=target_path))
        return failed_info


    def send_warning(self, failed_info, toUser, system, job_name):
        """
        发送警告信息
        :param toUser: 接收人
        :param system: 系统名称
        :param job_name: 任务名称
        :return:
        """
        if failed_info and len(failed_info.get('warning_tobe_send')) > 0:
            try:
                msg = "**应用接口监控告警: {suite_name}**\n脚本名称: {job_name}\n异常信息: {stat}\n详情请查看报告：[测试报告]({report_path})". \
                    format(suite_name=system, job_name=job_name, stat=failed_info.get('warning_tobe_send'),
                           report_path=failed_info.get('report_path'))
                # sendMail(msg)
                wechat.send_message(msg, toUser)
            except Exception as e:
                print(e)
                logger.error('告警发送失败：{e}'.format(e=e))
        else:
            logger.info('{job_name}测试通过'.format(job_name=job_name))




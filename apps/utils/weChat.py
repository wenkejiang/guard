# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/6   
# 修改时间: 12:25 上午   
# IDE: PyCharm
import json
import logging
import requests

logger = logging.getLogger('django')
from django.conf import settings


class WeChat(object):

    def __init__(self, corpid, secret, agentid):
        self.url = "https://qyapi.weixin.qq.com"
        self.corpid = corpid
        self.secret = secret
        self.agentid = agentid

    # 获取企业微信的 access_token
    def access_token(self):
        url_arg = '/cgi-bin/gettoken?corpid={id}&corpsecret={crt}'.format(
            id=self.corpid, crt=self.secret)
        url = self.url + url_arg
        response = requests.get(url=url)
        text = response.text
        self.token = json.loads(text)['access_token']

    # 构建消息格式
    def messages(self, msg, touser):
        values = {
            "touser": touser,
            "msgtype": 'markdown',
            "agentid": self.agentid,
            "markdown": {'content': msg},
            "safe": 0
        }
        self.msg = json.dumps(values)

    # 发送信息
    def send_message(self, msg, tousers):
        self.access_token()
        tousers = tousers.replace(' ', '').split(',')
        for touser in tousers:
            self.messages(msg, touser)

            send_url = '{url}/cgi-bin/message/send?access_token={token}'.format(
                url=self.url, token=self.token)
            response = requests.post(url=send_url, data=self.msg)
            errcode = json.loads(response.text)['errcode']

            if errcode == 0:
                logger.info('告警发送成功：{content}'.format(content=msg))
            else:
                logger.info('告警发送失败：{content}'.format(content=errcode))


wechat = WeChat(corpid=settings.CORPID, secret=settings.SECRET,
                agentid=settings.AGENTID)

# msg = '详情请查看报告：[测试报告]({report_path})'.format(
#     report_path='D:/workspace/python-project/api_check/httprunner_reports/20200301T140858.654570.html')
# wechat.send_message(msg, 'zhangwei02')


if __name__ == "__main__":
    wechat.send_message("2017", "jiangwenke")
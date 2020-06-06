# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/5   
# 修改时间: 11:50 下午   
# IDE: PyCharm
import sched

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler

#使用sqlalchemy作业存储器
from utils.weChat import wechat

url='mysql+pymysql://root:Dkaixy@917810@106.13.238.8:3306/guard?charset=utf8'


def my_listener(event):
    if event.exception:
        wechat.send_message('调度执行异常, 请检日志记录', 'zhangwei02,jiangwenke')


scheduler = BackgroundScheduler()

scheduler.add_jobstore("sqlalchemy", url=url)

scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()


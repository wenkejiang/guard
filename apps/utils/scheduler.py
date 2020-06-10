# -*- coding: utf-8 -*-
# 作者: jiangwenke
# 创建时间: 2020/6/5   
# 修改时间: 11:50 下午   
# IDE: PyCharm

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from utils.weChat import wechat

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///db.sqlite3')

}
job_defaults = {
    'coalesce': True,
    'max_instances': 2,
    'misfire_grace_time': 60
}
executors = {
    'default': ThreadPoolExecutor(10),  # 默认线程数
    'processpool': ProcessPoolExecutor(3)  # 默认进程
}


def my_listener(event):
    if event.exception:
        wechat.send_message('调度执行异常, 请检日志记录', 'zhangwei02,jiangwenke')


scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)


scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()

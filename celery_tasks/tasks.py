# -*- coding:utf-8 -*-
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
#再任务处理着一端加
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycode.settings')

app = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/8')

#定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    '''发送激活邮件'''

    subject = '标题'
    message =''
    html_message = '<h1>%s</h1>点击</br><a href="http://127.0.0.1:8003/active/%s">http://127.0.0.1:8003/active/%s</a>'%(username,token,token)
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    send_mail(subject,message,sender,receiver,html_message=html_message)

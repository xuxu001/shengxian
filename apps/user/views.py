from django.shortcuts import render,redirect,reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from apps.user.models import User
from django.conf import settings
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_register_active_email
import time
# Create your views here.

#/user/register


class RegisterView(View):
    def post(self,request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 进行数据校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完全'})

        # 验证邮箱

        if allow != 'on':
            return render(request, 'register.html', {"errmsg": '请同意'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 进行业务处理
        user = User.objects.create_user(username=username, password=password, email=email)
        user.is_active=0
        user.save()
        #加密
        print(time.time())
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()
        #发邮件
        send_register_active_email.delay(email,username,token)

        # 返回应答
        print(time.time())
        return redirect(reverse('goods:index'))
    def get(self,request):
        return render(request,'register.html')


class ActiveView(View):
    def get(self,request,token):
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.load(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('连接已过期')

#/user/login
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
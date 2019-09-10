# -*- coding:utf-8 -*-
from apps.user import views
from apps.user.views import RegisterView,ActiveView,LoginView

from django.urls import path,re_path

app_name = 'user'
urlpatterns = [
    path('register/',RegisterView.as_view(),name='regisrer'),
    path('login/',LoginView.as_view(),name='login'),
    # path('active/(?P<token>.*)',ActiveView.as_view(),name='active'),
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),

]

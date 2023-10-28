"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from loginApp import views
from django.views.decorators.csrf import csrf_exempt

app_name='loginApp'

urlpatterns = [
    #登录
    path('login/$', views.login_view, name='login_url'),
    #主页
    path('me/<str:submenu_id>/', views.user_view, name='user_url'),
    path('logout/$', views.logout_view, name='logout_url'),
    #注册
    path('signin/$', views.signin_view, name='signin_url'),
    #找回密码
    path('Repassword/',views.Repassword,name='Repassword'),
    path('Repassword2/',views.Repassword2,name='Repassword2'),
    path('sendcode/',views.send_code,name='sendcode'),
    path('testcode/',views.test_code,name='testcode'),
    path('Repassword3/',views.Repassword3,name='Repassword3'),
    path('del_ticket/<str:ticketid>/',views.del_ticket, name='del_ticket_url'),
    path('upload_avatar/', csrf_exempt(views.upload_avatar), name='upload_avatar'),
]

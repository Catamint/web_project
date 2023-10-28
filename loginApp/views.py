from django.shortcuts import render, HttpResponseRedirect,HttpResponse,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login, logout
from loginApp.utils import main as send
from productApp.models import jumbotron_base, user_exp, ticket_base
from django.http import JsonResponse
from imagekit.models import ProcessedImageField
import re
import json
# Create your views here.

def get_piece_dict():
    piece_dict={'id':[],
                'name':[],
                'intro':[],
                'label':[],
                'year':[],
                'status':[],
                'pics':[]
                }
    for piece in jumbotron_base.objects.all():
        piece_dict['id'].append(piece.movie.id)
        piece_dict['name'].append(piece.movie.name)
        if len(piece.movie.inform) < 200:
            piece_dict['intro'].append(piece.movie.inform)
        else:
            piece_dict['intro'].append(piece.movie.inform[0:200]+'...')
        if piece.pic == '':
            piece_dict['pics'].append(piece.movie.photo.url)
        else:
            piece_dict['pics'].append(piece.pic.url)
    
    len_dict = len(piece_dict['name'])
    return piece_dict, len_dict

#登录
def login_view(request):

    if request.GET.get("next", '') != '' and request.GET.get("next", '') != request.path:
        next=request.GET.get("next", '')
    else:
        next='/'

    if request.method == 'POST':
        piece_dict, len_dict = get_piece_dict()
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            return render(request,'login.html', {
                'piece_dict':json.dumps(piece_dict),
                'len_dict':len_dict,
                'error':'账号或密码错误',
                'submenu':'登录'
            })
    else:
        piece_dict, len_dict = get_piece_dict()
        return render(request, 'login.html', {
            'piece_dict':json.dumps(piece_dict),
            'len_dict':len_dict,
            'submenu':'登录'
            })
    
def logout_view(request):
    logout(request)
    return redirect('/')

#注册
def signin_view(request):

    data_list=User.objects.all()

    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        errors = {'username':'','password':'','pwd':''}
        flag = True
        if not re.match("^[A-Za-z0-9_]*$", username):
            errors['username'] = '用户名只能由字母,数字和下划线组成'
            flag=False
        else:
            for item in data_list:
                if username == item.username:
                    flag=False
                    errors['username']='此用户名已存在'

        if len(password) > 16 or len(password) < 6:
            flag = False
            errors['password'] = '密码长度应该在6到16位'
        
        if password != password2:
            flag=False
            errors['pwd']='两次密码输入不同'
        
        if not flag:
            piece_dict, len_dict = get_piece_dict()
            return render(request,'login.html',{
                'userid':errors['username'],
                'pwd':errors['password'],
                'piece_dict':json.dumps(piece_dict),
                'len_dict':len_dict,
                'submenu':'注册'
                })
        
        user = User.objects.create_user(username, email, password)
        exp = user_exp.objects.create(user=user)
        exp.save()
        return redirect('/u/login/$')
    else:
        piece_dict, len_dict = get_piece_dict()
        return render(request, 'login.html',{
                'piece_dict':json.dumps(piece_dict),
                'len_dict':len_dict,
                'submenu':'注册'
                })

def Repassword2(request):
    request.session['info'] = {'status':1}
    return render(request,'Repassword2.html')

#验证账号
def Repassword(request):
    errors={'username':''}
    status = request.session.get('info')['status']

    if request.method == 'POST' and status == 1:
        username = request.POST.get('username')
        data_list=User.objects.all()
        if username in [i.username for i in data_list]:
            request.session['info'] = {'username':username,'status':2}
            return render(request,'Repassword.html')
        else:
            errors['username']='用户不存在'
            if username == '':
                errors['username'] = '请输入用户名'
            return render(request,'Repassword2.html',{'errors':errors})
    else:
        return redirect('/u/Repassword2/')

#发送验证码
def send_code(request):
    errors={'email':'', 'code':''}
    status = request.session.get('info')['status']

    if request.method =='POST' and status == 2:
        username=request.session.get('info')['username']
        email=request.POST.get('email')
        data_list=User.objects.all()
        for item in data_list:
            if username == item.username and email == item.email:
                code = send(email)
                new_session = request.session.get('info')
                new_session['code'] = code
                new_session['email'] = email
                new_session['status'] = 3
                request.session['info'] = new_session
                return render(request,'Repassword.html')
        errors['email']='邮箱输入有误'
        return render(request,'Repassword.html',{'errors':errors})
    else:
        return redirect('/u/Repassword2/')

def test_code(request):
    errors={'email':'', 'code':''}
    if request.method =='POST':
        status = request.session.get('info')['status']
        if status == 2:
            errors['email']='请先获取验证码'
            return render(request,'Repassword.html',{'errors':errors})
        elif status == 3:
            code=request.POST.get('code')
            code2=request.session.get('info')['code']
            if code == code2:
                new_session = request.session.get('info')
                new_session['status'] = 4
                request.session['info'] = new_session
                return render(request,'Repassword3.html')
            else:
                errors['code']='验证码输入错误'
                return render(request,'Repassword.html',{'errors':errors,'display':False})
        else:
            print('status: ', status)
            return redirect('/u/Repassword2/')
    else:
        return redirect('/u/Repassword2/')

#重新输入密码
def Repassword3(request):
    status = request.session.get('info')['status']
    if request.method == 'POST' and status == 4:
        errors={'password':''}
        error={'password':''}
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        if len(password) > 16 or len(password) < 6:
            errors['password'] = '密码长度应该在6到16位'
            return render(request,'Repassword3.html',{'errors':errors['password']})
        
        if password != password2:
            error['password']='两次密码输入不同'
            return render(request,'Repassword3.html',{'error':error['password']})
        else:
            user=User.objects.get(username=request.session.get('info')['username'])
            user.set_password(password)
            user.save()
            request.session['info']={}
            return redirect('/u/login/$')

    else:
        return redirect('/u/Repassword2/')
    
    
submenu_dict={'info': '账户信息', 'order':'我的订单', 'favorites':'我的收藏'}
active_status_dict={'1':'added', '-1':'canceled'}

def user_view(request, submenu_id):
    user = get_object_or_404(User, id=request.user.id)

    if submenu_id == 'order':
        
        active_status='1'
        if 'active_status' in request.GET:
            active_status = request.GET['active_status']
            
        tickets=ticket_base.objects.filter(user=user, status=int(active_status))
        return render(request, 'user.html', {
            'user':user,
            'active_submenu': submenu_id,
            'productName':submenu_dict[submenu_id],
            'tickets':tickets,
            'active_status':active_status_dict[active_status]
        })
    else:
        return render(request, 'user.html', {
            'user':user,
            'active_submenu': submenu_id,
            'productName':submenu_dict[submenu_id],
        })

def del_ticket(request, ticketid):
    ticket = ticket_base.objects.get(id=ticketid)
    if request.user == ticket.user:
        ticket.status = -1
        ticket.save()
        return redirect('/u/me/order')
    else:
        return redirect('/u/login/$')
    
def upload_avatar(request):
    # 处理上传图片逻辑
    if request.method == 'POST' and request.FILES.get('avatar'):
        # 保存上传的图片、更新用户头像等操作
        avatar = request.FILES['avatar']
        user = get_object_or_404(User, id=request.user.id)
        user.other.photo.delete()
        user.other.photo = avatar
        user.other.save()
        # print(request.FILES.get('avatar'))
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
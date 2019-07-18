from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from apitest.models import Apitest, Apistep
from apptest.models import Appcase, Appcasestep
from bug.models import Bug
from products.models import Product

# login视图
from set.models import Set


def login(request):
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/home')
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error'})
    # else:
    #     context = {'error':'not fund this page'}
    #     return render(request, 'login.html', context)
    return render(request, 'login.html')


# home视图
def home(request):
    return render(request, 'home.html')


# 退出页面视图
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


# 产品管理视图
def product_manage(request):
    username = request.session.get('user', '')
    product_list = Product.objects.all()
    return render(request, "product_manage.html", {"user": username, "products": product_list})


# 创建apitest视图
@login_required
def apitest_manage(request):
    apitest_list = Apitest.objects.all()  # 读取所有流程接口数据
    username = request.session.get('user', '')  # 读取浏览器登陆session
    return render(request, "apitest_manage.html", {"user": username, "apitests": apitest_list})  # 定义流程接口数据的变量并返回前端


# 创建apistep视图
@login_required
def apistep_manage(request):
    username = request.session.get('user', '')
    apistep_list = Apistep.objects.all()
    return render(request, "apistep_manage.html", {"user": username, "apisteps": apistep_list})


# 创建单一接口视apis图
@login_required
def apis_manage(request):
    username = request.session.get('user', '')
    apis_list = Apistep.objects.all()
    return render(request, "apis_manage.html", {"user": username, "apiss": apis_list})


# 创建bug视图
def bug_manage(request):
    username = request.session.get('user', '')
    bug_list = Bug.objects.all()
    return render(request, "bug_manage.html", {"user": username, "bugs": bug_list})


# 创建set_manage视图
def set_manage(request):
    username = request.session.get('user', '')
    set_list = Set.objects.all()
    return render(request, "set_manage.html", {"user": username, "sets": set_list})


# 创建set_user视图
def set_user(request):
    user_list = User.objects.all()
    username = request.session.get('user', '')
    return render(request, "set_user.html", {"user": username, 'users': user_list})


# app用例管理
@login_required
def appcase_manage(request):
    appcase_list = Appcase.objects.all()
    username = request.session.get('user', '')  # 读取浏览器登录 Session
    return render(request, "appcase_manage.html", {"user": username, "appcases": appcase_list})


# App用例测试步骤
@login_required
def appcasestep_manage(request):
    username = request.session.get('user', '')
    appcasestep_list = Appcasestep.objects.all()
    return render(request, "appcasestep_manage.html", {"user": username, "appcasesteps": appcasestep_list})

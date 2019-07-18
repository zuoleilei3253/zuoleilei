"""autotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from apitest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),  #登陆目录
    path('home/',views.home),  #家目录
    path('logout/',views.logout),
    path('product_manage/',views.product_manage),
    path('apitest_manage/',views.apitest_manage),
    path('apistep_manage/',views.apistep_manage),
    path('apis_manage/',views.apis_manage),
    path('bug_manage/',views.bug_manage),
    path('user/',views.set_user),
    path('set_manage/',views.set_manage),
    path('appcase_manage/',views.appcase_manage),
    path('appcasestep_manage/',views.appcasestep_manage),
]



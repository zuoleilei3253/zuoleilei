from django.contrib import admin

from apptest.models import Appcase
from products.models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc', 'producter', 'create_time', 'id']


admin.site.register(Product)  # 把产品模块注册到Django admin后台并能显示


# app用例管理功能
class AppcaseAdmin(admin.TabularInline):
    list_display = ['appcasename', 'apptestresult', 'create_time', 'id', 'product']
    model = Appcase
    extra = 1


# app用例管理功能
class ProductAdmin(admin.ModelAdmin):
    list_display = ['productname', 'productdesc', 'create_time', 'id']
    inlines = [AppcaseAdmin]


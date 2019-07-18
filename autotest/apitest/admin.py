from django.contrib import admin

from apitest.models import Apistep, Apitest, Apis


# 创建step表内容
class ApistepAdmin(admin.TabularInline):
    list_display = ['apiname', 'apiurl', 'apiparamvalue', 'apimethod', 'apiresult', 'apistatus', 'create_time', 'id',
                    'apitest']
    model = Apistep
    extra = 1


# 创建test表内容
class ApitestAdmin(admin.ModelAdmin):
    list_display = ['apitestname', 'apitester', 'apitestresult', 'create_time', 'id']
    inlines = [ApistepAdmin]


admin.site.register(Apitest, ApitestAdmin)


# 创建apis表内容
class ApisAdmin(admin.TabularInline):
    list_display = ['apiname', 'apiurl', 'apiparamvalue', 'apimethod', 'apiresult', 'apistatus', 'create_time', 'id',
                    'product']


admin.site.register(Apis)  # 把apis注册到Django admin后台并能显示



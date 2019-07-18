from django.contrib import admin

from apptest.models import Appcasestep, Appcase


# 设置Appcasestep数据
class AppcasestepAdmin(admin.TabularInline):
    list_display = ['appteststep', 'apptestobjname', 'appfindmethod', 'appevelement', 'appoptmethod', 'appassertdata',
                    'apptestresult', 'create_time', 'id', 'appcase']
    model = Appcasestep
    extra = 1


# 设置appcase后台数据
class AppcaseAdmin(admin.ModelAdmin):
    list_display = ['appcasename', 'apptestresult', 'create_time', 'id']
    inlines = [AppcasestepAdmin]


admin.site.register(Appcase, AppcaseAdmin)


# ??? 3.9.3章APP用例管理功能


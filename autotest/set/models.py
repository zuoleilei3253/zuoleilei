from django.db import models


# 创建系统设置模块开发表：例如设置主机或URL及对应的值为变量
class Set(models.Model):
    setname = models.CharField('系统名称', max_length=64)  # 设置名称
    setvalue = models.CharField('系统设置', max_length=200)  # 设置值

    class Meta:
        verbose_name = '系统设置'
        verbose_name_plural = '系统设置'

    def __str__(self):
        return self.setname

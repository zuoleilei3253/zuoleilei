# Generated by Django 2.2.3 on 2019-07-17 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appcase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appcasename', models.CharField(max_length=200, verbose_name='用例名称')),
                ('apptestresult', models.BooleanField(verbose_name='测试结果')),
                ('apptester', models.CharField(max_length=16, verbose_name='测试负责人')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('Product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'verbose_name': 'app测试用例',
                'verbose_name_plural': 'app测试用例',
            },
        ),
        migrations.CreateModel(
            name='Appcasestep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appteststep', models.CharField(max_length=200, verbose_name='测试步骤')),
                ('apptestobjname', models.CharField(max_length=200, verbose_name='测试对象名称描述')),
                ('appfindmethod', models.CharField(max_length=200, verbose_name='定位方式')),
                ('appevelement', models.CharField(max_length=800, verbose_name='控件元素')),
                ('appoptmethod', models.CharField(max_length=200, verbose_name='操作方法')),
                ('apptestdata', models.CharField(max_length=200, null=True, verbose_name='测试数据')),
                ('appassertdata', models.CharField(max_length=200, verbose_name='验证数据')),
                ('apptestresult', models.BooleanField(verbose_name='测试结果')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('Appcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apptest.Appcase')),
            ],
        ),
    ]
